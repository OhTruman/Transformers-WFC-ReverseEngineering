"""Emulate MSVC CRT dynamic initializers (__xc_a..__xc_z) of default.xex.

Runs each initializer with a tiny PPC64 integer/FP-move subset interpreter. Calls (bl) are not
followed: volatile registers become UNKNOWN. Stores into the image's .data range are recorded.
Output: work/xc_writes.tsv  (init_func, store_insn, addr, size, value_hex, known)
"""
import os, struct, sys
from xeximg import Image, ROOT

U = None  # unknown marker
M64 = (1 << 64) - 1


def sx16(v):
    return v - 0x10000 if v & 0x8000 else v


def rotl64(v, n):
    n &= 63
    return ((v << n) | (v >> (64 - n))) & M64


def mask64(mb, me):
    if mb <= me:
        m = ((1 << (64 - mb)) - 1) & ~((1 << (63 - me)) - 1)
    else:
        m = ((1 << (64 - mb)) - 1) | (~((1 << (63 - me)) - 1) & M64)
    return m & M64


class Emu:
    def __init__(self, img):
        self.img = img
        self.d0, self.d1 = img.range("_data")
        self.t0, self.t1 = img.range("_text")
        self.writes = []

    def rd(self, mem, addr, size):
        bs = []
        for i in range(size):
            if addr + i in mem:
                bs.append(mem[addr + i])
            else:
                d, o = self.img.find(addr + i)
                if d is None or addr + i >= 0x70000000 and addr + i < 0x80000000:
                    return U
                bs.append(d[o])
            if bs[-1] is U:
                return U
        return int.from_bytes(bytes(bs), "big")

    def wr(self, mem, addr, size, val, pc, fn):
        for i in range(size):
            mem[addr + i] = U if val is U else (val >> (8 * (size - 1 - i))) & 0xFF
        if self.d0 <= addr < self.d1:
            self.writes.append((fn, pc, addr, size, val))

    def run(self, fn, maxsteps=200000):
        r = [U] * 32
        f = [U] * 32
        r[1] = 0x7FFF0000
        mem = {}
        lr = 0xDEAD0000
        pc = fn
        ctr = U
        for _ in range(maxsteps):
            if pc == lr or not (self.t0 <= pc < self.t1):
                return "ret"
            ins = self.img.u32(pc)
            op = ins >> 26
            rt = (ins >> 21) & 31
            ra = (ins >> 16) & 31
            rb = (ins >> 11) & 31
            imm = ins & 0xFFFF
            npc = pc + 4

            def ea_d():
                base = 0 if ra == 0 else r[ra]
                return U if base is U else (base + sx16(imm)) & 0xFFFFFFFF

            def ea_ds():
                base = 0 if ra == 0 else r[ra]
                return U if base is U else (base + sx16(imm & ~3)) & 0xFFFFFFFF

            if op == 14:  # addi
                r[rt] = sx16(imm) & M64 if ra == 0 else (U if r[ra] is U else (r[ra] + sx16(imm)) & M64)
            elif op == 15:  # addis
                v = (sx16(imm) << 16) & M64
                r[rt] = v if ra == 0 else (U if r[ra] is U else (r[ra] + v) & M64)
                if ra == 0:
                    r[rt] &= 0xFFFFFFFF if not (imm & 0x8000) else M64
            elif op in (24, 25):  # ori/oris  (rs=rt field, ra=dest)
                sh = 16 if op == 25 else 0
                r[ra] = U if r[rt] is U else r[rt] | (imm << sh)
            elif op in (28, 29):  # andi./andis.
                sh = 16 if op == 29 else 0
                r[ra] = U if r[rt] is U else r[rt] & (imm << sh)
            elif op in (26, 27):  # xori/xoris
                sh = 16 if op == 27 else 0
                r[ra] = U if r[rt] is U else r[rt] ^ (imm << sh)
            elif op in (32, 34, 40, 42):  # lwz lbz lhz lha
                sz = {32: 4, 34: 1, 40: 2, 42: 2}[op]
                a = ea_d()
                r[rt] = U if a is U else self.rd(mem, a, sz)
            elif op in (33, 35, 41):  # lwzu lbzu lhzu
                sz = {33: 4, 35: 1, 41: 2}[op]
                a = ea_d()
                r[rt] = U if a is U else self.rd(mem, a, sz)
                r[ra] = a
            elif op in (36, 38, 44, 37, 39, 45):  # stw stb sth (+u)
                sz = {36: 4, 37: 4, 38: 1, 39: 1, 44: 2, 45: 2}[op]
                a = ea_d()
                if a is not U:
                    v = r[rt]
                    self.wr(mem, a, sz, U if v is U else v & ((1 << (8 * sz)) - 1), pc, fn)
                if op in (37, 39, 45):
                    r[ra] = a
            elif op == 58:  # ld/ldu/lwa
                a = ea_ds()
                sub = ins & 3
                if sub in (0, 1):
                    r[rt] = U if a is U else self.rd(mem, a, 8)
                    if sub == 1:
                        r[ra] = a
                else:
                    v = U if a is U else self.rd(mem, a, 4)
                    r[rt] = U if v is U else (v - (1 << 32) if v & 0x80000000 else v) & M64
            elif op == 62:  # std/stdu
                a = ea_ds()
                if a is not U:
                    self.wr(mem, a, 8, r[rt], pc, fn)
                if ins & 3 == 1:
                    r[ra] = a
            elif op in (48, 49):  # lfs
                a = ea_d()
                f[rt] = U if a is U else ("s", self.rd(mem, a, 4))
                if op == 49: r[ra] = a
            elif op in (50, 51):  # lfd
                a = ea_d()
                f[rt] = U if a is U else ("d", self.rd(mem, a, 8))
                if op == 51: r[ra] = a
            elif op in (52, 53):  # stfs
                a = ea_d()
                v = f[rt]
                if a is not U:
                    if v is U or v[1] is U:
                        val = U
                    elif v[0] == "s":
                        val = v[1]
                    else:
                        val = struct.unpack(">I", struct.pack(">f", struct.unpack(">d", v[1].to_bytes(8, "big"))[0]))[0]
                    self.wr(mem, a, 4, val, pc, fn)
                if op == 53: r[ra] = a
            elif op in (54, 55):  # stfd
                a = ea_d()
                v = f[rt]
                if a is not U:
                    if v is U or v[1] is U:
                        val = U
                    elif v[0] == "d":
                        val = v[1]
                    else:
                        val = struct.unpack(">Q", struct.pack(">d", struct.unpack(">f", v[1].to_bytes(4, "big"))[0]))[0]
                    self.wr(mem, a, 8, val, pc, fn)
                if op == 55: r[ra] = a
            elif op == 30:  # rld*
                sub = (ins >> 2) & 7
                sh = ((ins >> 11) & 31) | (((ins >> 1) & 1) << 5)
                mb = ((ins >> 6) & 31) | (((ins >> 5) & 1) << 5)
                rs = rt
                if r[rs] is U:
                    r[ra] = U
                else:
                    rot = rotl64(r[rs], sh)
                    if sub == 0:
                        r[ra] = rot & mask64(mb, 63)
                    elif sub == 1:
                        r[ra] = rot & mask64(0, mb)
                    elif sub == 2:
                        r[ra] = rot & mask64(mb, 63 - sh)
                    elif sub == 3:
                        m = mask64(mb, 63 - sh)
                        r[ra] = U if r[ra] is U else (rot & m) | (r[ra] & ~m & M64)
                    else:
                        r[ra] = U
            elif op == 21:  # rlwinm
                rs = rt
                sh = rb
                mb = (ins >> 6) & 31
                me = (ins >> 1) & 31
                if r[rs] is U:
                    r[ra] = U
                else:
                    v = r[rs] & 0xFFFFFFFF
                    v = ((v << sh) | (v >> (32 - sh))) & 0xFFFFFFFF if sh else v
                    m = mask64(mb + 32, me + 32)
                    r[ra] = v & m
            elif op == 31:
                xo = (ins >> 1) & 0x3FF
                if xo == 444:  # or / mr
                    r[ra] = U if r[rt] is U or r[rb] is U else r[rt] | r[rb]
                elif xo == 339 or xo == 467:  # mfspr / mtspr
                    spr = ((ins >> 16) & 31) | (((ins >> 11) & 31) << 5)
                    if xo == 339:
                        r[rt] = lr if spr == 8 else (ctr if spr == 9 else U)
                    else:
                        if spr == 9:
                            ctr = r[rt]
                elif xo == 266:  # add
                    r[rt] = U if r[ra] is U or r[rb] is U else (r[ra] + r[rb]) & M64
                elif xo == 40:  # subf
                    r[rt] = U if r[ra] is U or r[rb] is U else (r[rb] - r[ra]) & M64
                elif xo in (151, 407, 215, 663, 727, 149):  # stwx sthx stbx stfsx stfdx stdx
                    sz = {151: 4, 407: 2, 215: 1, 663: 4, 727: 8, 149: 8}[xo]
                    base = 0 if ra == 0 else r[ra]
                    if base is not U and r[rb] is not U and xo in (151, 407, 215, 149):
                        a = (base + r[rb]) & 0xFFFFFFFF
                        v = r[rt]
                        self.wr(mem, a, sz, U if v is U else v & ((1 << (8 * sz)) - 1), pc, fn)
                elif xo in (23, 279, 87, 21):  # lwzx lhzx lbzx ldx
                    sz = {23: 4, 279: 2, 87: 1, 21: 8}[xo]
                    base = 0 if ra == 0 else r[ra]
                    r[rt] = U if base is U or r[rb] is U else self.rd(mem, (base + r[rb]) & 0xFFFFFFFF, sz)
                elif xo in (0, 32, 598, 854, 86, 54, 278, 246, 1014):  # cmp/cmpl/sync/eieio/dcb*
                    pass
                else:
                    if rt < 32:
                        r[rt] = U
                    r[ra] = U
            elif op == 18:  # b / bl
                li = ins & 0x03FFFFFC
                if li & 0x02000000:
                    li -= 0x04000000
                tgt = (pc + li) & 0xFFFFFFFF if not (ins & 2) else li & 0xFFFFFFFF
                if ins & 1:  # bl: do not follow
                    for i in (0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12):
                        r[i] = U
                    for i in range(14):
                        f[i] = U
                else:
                    if self.t0 <= tgt < self.t1 and tgt not in (fn,):
                        npc = tgt  # tail call / jump
                    else:
                        return "jump-out"
            elif op == 16:  # bc: assume not taken unless unconditional
                bo = rt
                if bo & 0x14 == 0x14:
                    bd = sx16(imm & 0xFFFC)
                    npc = pc + bd
            elif op == 19:
                xo = (ins >> 1) & 0x3FF
                if xo == 16:  # bclr
                    if rt & 0x14 == 0x14:
                        return "ret"
                elif xo == 528:  # bcctr
                    return "bcctr"
            elif op in (10, 11, 7, 8, 12, 13, 59, 63, 4, 2, 3, 17, 20, 23, 31, 47, 46):
                if op in (7, 8, 12, 13, 20, 23):
                    r[ra if op in (20, 23) else rt] = U
                elif op == 46:  # lmw
                    for i in range(rt, 32):
                        r[i] = U
                elif op == 63 and ((ins >> 1) & 0x3FF) == 72:  # fmr
                    f[rt] = f[rb]
                elif op in (59, 63):
                    f[rt] = U
            else:
                return "unsupported op %d @%x" % (op, pc)
            r[0] = r[0]
            pc = npc
        return "steps"


def find_xc_tables(img):
    """Contiguous runs of .data/.rdata words that each point to a function start in .text near the CRT init area."""
    t0, t1 = img.range("_text")
    runs = []
    for nm in ("_data", "_rdata"):
        _, s, d, _ = img.block(nm)
        n = len(d) // 4
        w = struct.unpack(">%dI" % n, d[: n * 4])
        i = 0
        while i < n:
            j = i
            while j < n and (0x83600000 <= w[j] < t1 or w[j] == 0):
                j += 1
            nonzero = [x for x in w[i:j] if x]
            if len(nonzero) >= 20:
                runs.append((s + i * 4, s + j * 4, nonzero))
            i = j + 1
    return runs


if __name__ == "__main__":
    img = Image()
    emu = Emu(img)
    runs = find_xc_tables(img)
    fns = []
    for a, b, lst in runs:
        print("table %x-%x  %d entries" % (a, b, len(lst)))
        fns += lst
    stat = {}
    for fn in fns:
        res = emu.run(fn)
        stat[res.split(" @")[0]] = stat.get(res.split(" @")[0], 0) + 1
    print(stat)
    out = os.path.join(ROOT, "work", "xc_writes.tsv")
    with open(out, "w") as fo:
        fo.write("init\tinsn\taddr\tsize\tvalue\n")
        for fn, pc, a, sz, v in emu.writes:
            fo.write("0x%08x\t0x%08x\t0x%08x\t%d\t%s\n" % (fn, pc, a, sz, "?" if v is U else "%0*x" % (sz * 2, v)))
    print("writes:", len(emu.writes), "known:", sum(1 for w in emu.writes if w[4] is not U))
