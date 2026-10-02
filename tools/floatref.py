"""Find functions that load given float constants (lfs/lfd via lis+offset) and intersect.
Usage: python floatref.py 1.9 2.4 0.08 ..."""
import sys, struct, bisect, collections
from xeximg import Image
from ppcrefs import load, index_by_target
img = Image()
_, _, pdata, _ = img.block("_pdata")
starts = sorted(struct.unpack_from(">I", pdata, i)[0] for i in range(0, len(pdata)-7, 8))
def fstart(a):
    i = bisect.bisect_right(starts, a) - 1; return starts[i] if i >= 0 else 0
idx = index_by_target(load(img))
r0, r1 = img.range("_rdata"); _, _, rd, _ = img.block("_rdata")
vals = [float(x) for x in sys.argv[1:]]
per = {}
for v in vals:
    pat = struct.pack(">f", v)
    addrs = [r0 + i for i in range(0, len(rd) - 3, 4) if rd[i:i+4] == pat]
    fs = collections.Counter()
    for a in addrs:
        for ins in idx.get(a, []): fs[fstart(ins)] += 1
    per[v] = fs
    print(v, "consts", len(addrs), "funcs", len(fs))
common = set.intersection(*(set(f) for f in per.values()))
for f in sorted(common): print(hex(f), [per[v][f] for v in vals])
