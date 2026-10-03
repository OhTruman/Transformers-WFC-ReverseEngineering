"""Numeric emulator for straight-line Xenos pixel-shader ALU code (read-only analysis aid).
Decodes the same instruction fields as xenostrace.py, but evaluates float values.
Fetches are not emulated: the caller pre-loads the fetched values into registers (by instruction address)
via a `fetch_values` map {instr_addr: value}, written to the fetch's destination components.
Usage (library): emulate(blob, offset, consts={reg: (x,y,z,w)}, regs={(r,comp): v}, fetch_values={addr: v})
Returns the dict of exported oC0 components and the final register file.
"""
import math, struct
import xenosdis as X
B = X.bits


def emulate(d, H, consts, regs, fetch_values, ctab_off=0x28):
    M, cfs = X.find_microcode(d, H + ctab_off, H + 0x6000)
    lit = {}
    k = 1
    while k < 16:
        v = struct.unpack_from('>4f', d, M - 16 * k)
        if all(x == 0 for x in v) and k > 1 and all(x == 0 for x in struct.unpack_from('>4f', d, M - 16 * (k + 1))):
            break
        k += 1
    vecs = [struct.unpack_from('>4f', d, M - 16 * j) for j in range(k - 1, 0, -1)]
    while vecs and all(x == 0 for x in vecs[0]): vecs.pop(0)
    for i, v in enumerate(vecs): lit[256 - len(vecs) + i] = v
    C = dict(consts); C.update(lit)
    R = dict(regs)
    PS = [0.0]
    out = {}
    instrs = []
    for c in cfs:
        op = B(c, 44, 4)
        if op in (1, 2, 3, 4, 5, 6, 13, 14):
            addr, cnt, seq = B(c, 0, 12), B(c, 12, 3), B(c, 16, 12)
            for i in range(cnt):
                instrs.append((addr + i, B(seq, 2 * i, 1), struct.unpack_from('>3I', d, M + 12 * (addr + i))))
            if op in (2, 4, 6, 14): break

    def rd(reg, sel, neg, comp, absc):
        if sel:
            v = R.get((reg & 0x3F, comp), 0.0)
            if reg & 0x80: v = abs(v)
        else:
            v = C.get(reg, (0.0, 0.0, 0.0, 0.0))[comp]
        return -v if neg else v

    for a, isf, (w0, w1, w2) in instrs:
        if isf:
            op = B(w0, 0, 5)
            if op == 1 and a in fetch_values:
                dr = B(w0, 12, 6); dsw = B(w1, 0, 12)
                for i in range(4):
                    s = B(dsw, 3 * i, 3)
                    if s < 4: R[(dr, i)] = fetch_values[a]
            continue
        vdst = B(w0, 0, 6); absc = B(w0, 7, 1); sdst = B(w0, 8, 6); exp = B(w0, 15, 1)
        vmask = B(w0, 16, 4); smask = B(w0, 20, 4); vcl = B(w0, 24, 1); scl = B(w0, 25, 1); sop = B(w0, 26, 6)
        sws = [B(w1, 16, 8), B(w1, 8, 8), B(w1, 0, 8)]; negs = [B(w1, 26, 1), B(w1, 25, 1), B(w1, 24, 1)]
        regs_ = [B(w2, 16, 8), B(w2, 8, 8), B(w2, 0, 8)]; sels = [B(w2, 31, 1), B(w2, 30, 1), B(w2, 29, 1)]
        vop = B(w2, 24, 5)
        sat = lambda x: min(max(x, 0.0), 1.0)

        def sv(si, comp_dst):
            comp = (B(sws[si], 2 * comp_dst, 2) + comp_dst) & 3
            return rd(regs_[si], sels[si], negs[si], comp, absc)
        newR = {}
        if vmask:
            for i in range(4):
                if not (vmask >> i & 1): continue
                if vop in (15, 16):
                    n = 4 if vop == 15 else 3
                    e = sum(sv(0, j) * sv(1, j) for j in range(n))
                else:
                    a0, b0, c0 = sv(0, i), sv(1, i), sv(2, i)
                    e = {0: lambda: a0 + b0, 1: lambda: a0 * b0, 2: lambda: max(a0, b0), 3: lambda: min(a0, b0),
                         4: lambda: 1.0 if a0 == b0 else 0.0, 5: lambda: 1.0 if a0 > b0 else 0.0,
                         6: lambda: 1.0 if a0 >= b0 else 0.0, 7: lambda: 1.0 if a0 != b0 else 0.0,
                         8: lambda: a0 - math.floor(a0), 10: lambda: math.floor(a0),
                         11: lambda: a0 * b0 + c0,
                         12: lambda: b0 if a0 == 0 else c0, 13: lambda: b0 if a0 >= 0 else c0,
                         14: lambda: b0 if a0 > 0 else c0}[vop]()
                if vcl: e = sat(e)
                newR[(vdst, i)] = e
        a_c = (B(sws[2], 6, 2) + 3) & 3; b_c = B(sws[2], 0, 2) & 3
        if sop in (42, 43, 44, 45, 46, 47):
            tr = (sws[2] & 0x3C) | (sels[2] << 1) | (sop & 1)
            ca = rd(regs_[2], 0, negs[2], a_c, absc); tb = rd(tr, 1, 0, b_c, 0)
            se = {42: ca * tb, 43: ca * tb, 44: ca + tb, 45: ca + tb, 46: ca - tb, 47: ca - tb}[sop]
        elif sop == 50:
            se = PS[0]
        else:
            A = rd(regs_[2], sels[2], negs[2], a_c, absc); Bv = rd(regs_[2], sels[2], negs[2], b_c, absc)
            ps = PS[0]
            se = {0: lambda: A + Bv, 1: lambda: A + ps, 2: lambda: A * Bv, 3: lambda: A * ps,
                  5: lambda: max(A, Bv), 6: lambda: min(A, Bv), 7: lambda: 1.0 if A == 0 else 0.0,
                  8: lambda: 1.0 if A > 0 else 0.0, 9: lambda: 1.0 if A >= 0 else 0.0,
                  10: lambda: 1.0 if A != 0 else 0.0, 17: lambda: 1.0 / A if A else 0.0,
                  18: lambda: 1.0 / A if A else 0.0, 19: lambda: (1.0 / A) if A else float('inf'),
                  25: lambda: A - Bv, 26: lambda: A - ps, 40: lambda: math.sqrt(A)}.get(sop, lambda: float('nan'))()
        if scl: se = sat(se)
        PS[0] = se
        if smask:
            for i in range(4):
                if smask >> i & 1: newR[(sdst, i)] = se
        for k2, v in newR.items():
            if exp: out[k2[1]] = v
            else: R[k2] = v
    return out, R
