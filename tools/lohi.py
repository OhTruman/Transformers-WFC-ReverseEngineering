"""Loose address-materialisation search: any D-form insn whose 16-bit imm completes target's low half,
where the base register was set by `lis` to the matching high half within WINDOW insns before
(no clobber tracking). Catches refs ppcrefs.py misses because the lis is far away.
Usage: python lohi.py 0x820c740c [...]"""
import sys, struct
from xeximg import Image
WINDOW = 600
img = Image()
t0, _ = img.range("_text"); _, _, text, _ = img.block("_text")
w = struct.unpack(">%dI" % (len(text)//4), text[:len(text)//4*4])
for t in sys.argv[1:]:
    v = int(t, 16); lo = v & 0xFFFF; hi = (v >> 16) + (1 if lo & 0x8000 else 0)
    hi &= 0xFFFF
    for i, ins in enumerate(w):
        op = ins >> 26
        if op not in (14, 32, 48, 50, 34, 40) or (ins & 0xFFFF) != lo: continue
        ra = (ins >> 16) & 31
        for j in range(i-1, max(0, i-WINDOW), -1):
            p = w[j]
            if p >> 26 == 15 and ((p >> 21) & 31) == ra and ((p >> 16) & 31) == 0:
                if p & 0xFFFF == hi: print(t, "insn", hex(t0+4*i), "lis@", hex(t0+4*j))
                break
