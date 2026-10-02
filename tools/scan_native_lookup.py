"""Recover UE3 native function registrations (FNativeFunctionLookup tables).

Layout (CONFIRMED at 0x837098b0): arrays of {wchar_t* name, void* func} terminated by {0,0}.
name = "int" + <C++ class> + "exec" + <UnrealScript function>.
Writes data/native_functions.tsv.
"""
import os, struct, collections
from xeximg import Image, ROOT

img = Image()
_, dstart, ddata, _ = img.block("_data")
rd0, rd1 = img.range("_rdata")
tx0, tx1 = img.range("_text")

# 12-byte member-pointer tables: slot filled at runtime by CRT initializers (see xcemu.py)
xc = {}
with open(os.path.join(ROOT, "work", "xc_writes.tsv")) as f:
    next(f)
    for line in f:
        _, _, a, sz, v = line.rstrip("
").split("	")
        if sz == "8" and v != "?":
            xc[int(a, 16)] = int(v, 16) >> 32

rows = []
for i in range(0, len(ddata) - 12, 4):
    a, z1, z2 = struct.unpack_from(">III", ddata, i)
    if rd0 <= a < rd1 and z1 == 0 and z2 == 0 and (dstart + i + 4) in xc:
        s = img.wstr(a)
        if s and s.startswith("int") and "exec" in s[3:]:
            body = s[3:]
            k = body.find("exec", 1)
            rows.append((dstart + i, xc[dstart + i + 4], body[:k], body[k + 4:]))

for i in range(0, len(ddata) - 8, 4):
    a, b = struct.unpack_from(">II", ddata, i)
    if rd0 <= a < rd1 and tx0 <= b < tx1:
        s = img.wstr(a)
        if s and s.startswith("int") and "exec" in s[3:]:
            body = s[3:]
            k = body.find("exec", 1)
            cls, fn = body[:k], body[k + 4:]
            rows.append((dstart + i, b, cls, fn))

os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
with open(os.path.join(ROOT, "data", "native_functions.tsv"), "w", encoding="utf-8") as f:
    f.write("table_entry\tfunc\tclass\texec_function\n")
    for e, b, c, fn in rows:
        f.write("0x%08x\t0x%08x\t%s\t%s\n" % (e, b, c, fn))

cnt = collections.Counter(r[2] for r in rows)
print("entries:", len(rows), "classes:", len(cnt), "unique funcs:", len(set(r[1] for r in rows)))
for c, n in cnt.most_common(25):
    print(n, c)
