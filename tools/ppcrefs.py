"""Find code that materialises a 32-bit address via PPC  lis rX,HI ; (addi|ori|lwz|lfs|stw...) rY,LO(rX).

Index is built once over .text and cached in work/addr_refs.bin (pairs of u32: insn_va, target_va).
Usage:  python ppcrefs.py 0x822c24c8 [...]
"""
import os, sys, struct, array
from xeximg import Image, ROOT

CACHE = os.path.join(ROOT, "work", "addr_refs.bin")

# D-form opcodes whose 16-bit signed displacement completes a lis
DFORM = {14: "addi", 24: "ori", 32: "lwz", 34: "lbz", 40: "lhz", 42: "lha", 36: "stw", 38: "stb",
         44: "sth", 48: "lfs", 50: "lfd", 52: "stfs", 54: "stfd", 58: "ld", 62: "std"}


def build(img):
    t0, _ = img.range("_text")
    _, _, text, _ = img.block("_text")
    n = len(text) // 4
    w = struct.unpack(">%dI" % n, text[: n * 4])
    out = array.array("I")
    hi = {}  # reg -> (hi value, index)
    for i, ins in enumerate(w):
        op = ins >> 26
        rd = (ins >> 21) & 31
        ra = (ins >> 16) & 31
        imm = ins & 0xFFFF
        if op == 15 and ra == 0:  # lis rd, imm
            hi[rd] = (imm << 16, i)
            continue
        if op in DFORM and ra in hi and i - hi[ra][1] <= 48:
            lo = imm - 0x10000 if (imm & 0x8000 and op != 24) else imm
            tgt = (hi[ra][0] + lo) & 0xFFFFFFFF
            out.append(t0 + i * 4)
            out.append(tgt)
        # crude invalidation: a non-store write to rd kills its hi
        if op not in (36, 38, 44, 52, 54, 62) and rd in hi and hi[rd][1] != i and op not in (16, 18, 19):
            if not (op in DFORM and ra == rd):
                hi.pop(rd, None)
            elif op in DFORM:
                hi.pop(rd, None)
        if op == 18 and (ins & 1):  # bl clobbers volatile regs
            for r in list(hi):
                if r <= 12:
                    hi.pop(r)
    with open(CACHE, "wb") as f:
        out.byteswap() if sys.byteorder == "big" else None
        out.tofile(f)
    return out


def load(img=None):
    if not os.path.exists(CACHE):
        return build(img or Image())
    a = array.array("I")
    with open(CACHE, "rb") as f:
        a.frombytes(f.read())
    return a


def index_by_target(a):
    d = {}
    for i in range(0, len(a), 2):
        d.setdefault(a[i + 1], []).append(a[i])
    return d


if __name__ == "__main__":
    img = Image()
    a = load(img)
    idx = index_by_target(a)
    print("pairs:", len(a) // 2)
    for t in sys.argv[1:]:
        v = int(t, 16)
        print(hex(v), [hex(x) for x in idx.get(v, [])])
