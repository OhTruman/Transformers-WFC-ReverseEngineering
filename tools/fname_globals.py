"""Recover the hardcoded-FName global table filled by Function_83612160 (CONFIRMED pattern):
   lis rX,HI ; (addi|subi) r4,rX,LO  -> wide string ;  addi r3,r31,OFF ; bl FName::Init(0x82bacd78)
   r31 = 0x83826580, so FName global = 0x83826580+OFF.
Writes data/fname_globals.tsv (global, string_va, string)."""
import os, struct
from xeximg import Image, ROOT
img = Image()
t0, _ = img.range("_text"); _, _, text, _ = img.block("_text")
F0, F1 = 0x83612160, 0x83640000
BASE = 0x83826580
w = struct.unpack(">%dI" % ((F1-F0)//4), text[F0-t0:F1-t0])
hi = {}; pend = None; rows = []
def sx(v): return v-0x10000 if v & 0x8000 else v
for i, ins in enumerate(w):
    op = ins >> 26; rd = (ins >> 21) & 31; ra = (ins >> 16) & 31; imm = ins & 0xFFFF
    if op == 15 and ra == 0: hi[rd] = imm << 16
    elif op == 14 and rd == 4 and ra in hi: pend = (hi[ra] + sx(imm)) & 0xFFFFFFFF
    elif op == 14 and rd == 3 and ra == 31:
        if pend is not None:
            rows.append((BASE + sx(imm), pend, img.wstr(pend) or img.astr(pend) or "?"))
        pend = None
os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
with open(os.path.join(ROOT, "data", "fname_globals.tsv"), "w", encoding="utf-8") as f:
    f.write("global\tstring_va\tname\n")
    for g, s, n in rows: f.write("0x%08x\t0x%08x\t%s\n" % (g, s, n))
print(len(rows))
