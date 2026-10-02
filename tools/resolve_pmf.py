"""Resolve native PMF slots that CRT emulation missed: find the store to <entry+4> (via lis/stw pair) and the
code address materialised just before it. Updates data/native_functions_full.tsv in place (source=pmfscan)."""
import os, bisect
from xeximg import Image, ROOT
from ppcrefs import load
img = Image(); t0, t1 = img.range("_text")
a = load(img)
pairs = [(a[i], a[i+1]) for i in range(0, len(a), 2)]
by_tgt = {}
for ins, tgt in pairs: by_tgt.setdefault(tgt, []).append(ins)
code_by_ins = sorted((ins, tgt) for ins, tgt in pairs if t0 <= tgt < t1)
keys = [c[0] for c in code_by_ins]
path = os.path.join(ROOT, "data", "native_functions_full.tsv")
lines = open(path, encoding="utf-8").read().splitlines()
out = [lines[0]]; fixed = 0
for ln in lines[1:]:
    f = ln.split("\t")
    if f[1] == "0x00000000":
        slot = int(f[0], 16) + 4
        for ins in by_tgt.get(slot, []):
            j = bisect.bisect_left(keys, ins) - 1
            if j >= 0 and ins - keys[j] <= 0x30:
                f[1] = "0x%08x" % code_by_ins[j][1]; f[2] = "pmfscan"; fixed += 1; break
    out.append("\t".join(f))
open(path, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("fixed", fixed)
