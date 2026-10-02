"""Robust UE3 native registration scan (supersedes scan_native_lookup.py coverage).
For every wide string 'int<Class>exec<Func>' find .data pointers to it; the function pointer is
 (a) u32 at ref+4 if it is code, else (b) the CRT-initialised 8-byte member pointer at ref+4 (work/xc_writes.tsv).
Writes data/native_functions_full.tsv"""
import os, re, struct
from xeximg import Image, ROOT
img = Image()
t0, t1 = img.range("_text")
xc = {}
for line in open(os.path.join(ROOT, "work", "xc_writes.tsv")).read().splitlines()[1:]:
    f = line.split("\t")
    if f[3] == "8" and f[4] != "?": xc[int(f[2], 16)] = int(f[4], 16) >> 32
strs = {}
for name, start, data, ex in img.blocks:
    if ex or name != "_rdata": continue
    for m in re.finditer(rb"\x00i\x00n\x00t(?:\x00[\x20-\x7e]){4,}\x00\x00", data):
        s = m.group()[1:-2][::2].decode()
        if "exec" in s[3:]: strs[start + m.start()] = s
rows = []
_, d0, dd, _ = img.block("_data")
for i in range(0, len(dd) - 4, 4):
    a = struct.unpack_from(">I", dd, i)[0]
    if a in strs:
        ref = d0 + i
        f = img.u32(ref + 4)
        src = "direct"
        if not (f and t0 <= f < t1):
            f = xc.get(ref + 4); src = "xcinit"
        body = strs[a][3:]; k = body.find("exec", 1)
        rows.append((ref, f or 0, src, body[:k], body[k + 4:]))
with open(os.path.join(ROOT, "data", "native_functions_full.tsv"), "w", encoding="utf-8") as fo:
    fo.write("table_entry\tfunc\tsource\tclass\texec_function\n")
    for r in rows: fo.write("0x%08x\t0x%08x\t%s\t%s\t%s\n" % r)
print("strings", len(strs), "entries", len(rows), "resolved", sum(1 for r in rows if r[1]))
