"""Loose float-constant user finder: lfs/lfd whose base reg came from `lis` (any distance within the function).
Usage: python floatref2.py 1.9 2.4 0.08"""
import sys, struct, bisect, collections
from xeximg import Image
img = Image()
t0, _ = img.range("_text"); _, _, text, _ = img.block("_text")
w = struct.unpack(">%dI" % (len(text)//4), text[:len(text)//4*4])
_, _, pdata, _ = img.block("_pdata")
starts = sorted(struct.unpack_from(">I", pdata, i)[0] for i in range(0, len(pdata)-7, 8))
sset = set(starts)
r0, r1 = img.range("_rdata"); _, _, rd, _ = img.block("_rdata")
want = {}
for x in sys.argv[1:]:
    v = float(x); pat = struct.pack(">f", v)
    for i in range(0, len(rd) - 3, 4):
        if rd[i:i+4] == pat: want[r0 + i] = v
per = collections.defaultdict(collections.Counter)
hi = {}; cur = None
for i, ins in enumerate(w):
    a = t0 + 4*i
    if a in sset: hi = {}; cur = a
    op = ins >> 26; rd_ = (ins >> 21) & 31; ra = (ins >> 16) & 31; imm = ins & 0xFFFF
    if op == 15 and ra == 0: hi[rd_] = imm << 16; continue
    if op in (48, 50) and ra in hi:
        tgt = (hi[ra] + (imm - 0x10000 if imm & 0x8000 else imm)) & 0xFFFFFFFF
        if tgt in want: per[cur][want[tgt]] += 1
vals = [float(x) for x in sys.argv[1:]]
rows = sorted(per.items(), key=lambda kv: -len(kv[1]))
for f, c in rows[:25]: print(hex(f), dict(c))
