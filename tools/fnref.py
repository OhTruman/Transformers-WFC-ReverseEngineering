"""Find code references to hardcoded-FName globals (base 0x83826580, see fname_globals.py).
Pattern: lis rA,0x8382 ; addi rB,rA,0x6580 ; ... (addi|lwz|ld) rX,OFF(rB)   (also direct lis/addi to global).
Usage: python fnref.py <Name> [...]"""
import sys, struct, bisect, os
from xeximg import Image, ROOT
img = Image()
t0, _ = img.range("_text"); _, _, text, _ = img.block("_text")
w = struct.unpack(">%dI" % (len(text)//4), text[:len(text)//4*4])
_, _, pdata, _ = img.block("_pdata")
starts = sorted(struct.unpack_from(">I", pdata, i)[0] for i in range(0, len(pdata)-7, 8))
def fstart(a):
    i = bisect.bisect_right(starts, a) - 1; return starts[i] if i >= 0 else 0
names = {}
for line in open(os.path.join(ROOT, "data", "fname_globals.tsv"), encoding="utf-8").read().splitlines()[1:]:
    g, s, n = line.split("\t"); names.setdefault(n, []).append(int(g, 16))
BASE = 0x83826580
want = {}
for n in sys.argv[1:]:
    for g in names.get(n, []): want[g - BASE] = n
base_regs = {}
for i, ins in enumerate(w):
    op = ins >> 26; rd = (ins >> 21) & 31; ra = (ins >> 16) & 31; imm = ins & 0xFFFF
    if op == 15 and ra == 0:
        base_regs[rd] = ("hi", imm, i)
        continue
    if op == 14 and ra in base_regs and base_regs[ra][0] == "hi" and i - base_regs[ra][2] < 64:
        full = ((base_regs[ra][1] << 16) + (imm - 0x10000 if imm & 0x8000 else imm)) & 0xFFFFFFFF
        if full == BASE:
            base_regs[rd] = ("base", 0, i); continue
        if full - BASE in want:
            print(want[full - BASE], hex(t0 + 4*i), "func", hex(fstart(t0 + 4*i)))
    if op in (14, 32, 58) and ra in base_regs and base_regs[ra][0] == "base" and i - base_regs[ra][2] < 400:
        off = imm - 0x10000 if imm & 0x8000 else imm
        if op == 58: off &= ~3
        if off in want:
            print(want[off], hex(t0 + 4*i), "func", hex(fstart(t0 + 4*i)))
