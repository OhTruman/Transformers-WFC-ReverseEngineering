"""Read-only: for every cooked map / Startup package, find the material shader maps ("Material <path>" /
"MaterialInstanceConstant <path>" records inside ShaderCache exports) of the requested materials and list, per vertex factory,
the (shader type, shader GUID) entries. Packages are read directly (no pickle cache).
Usage: python shadermap_scan.py <out.json> <name-substring>[,...]  -> json {pkg: [{kind, name, vf: {VF: [[type, guid], ...]}}]}"""
import os, re, sys, json, struct
sys.dont_write_bytecode = True
sys.path.insert(0, r"F:\Transformers Rebuild\AssetTools\scripts\wfc")
import ue3pkg

DUMP = r"F:\Transformers Rebuild\Game Dump\TransGame\CookedXenon"
out, want = sys.argv[1], sys.argv[2].split(",")
REC = re.compile(rb"(MaterialInstanceConstant|Material) ([A-Za-z0-9_.]+)\x00")
res = {}
pkgs = sorted(f for f in os.listdir(DUMP) if f.endswith("_m.xxx") or f.startswith("Startup"))
for n, f in enumerate(pkgs):
    try:
        p = ue3pkg.Package(os.path.join(DUMP, f))
    except Exception as ex:
        print("ERR", f, ex, flush=True); continue
    d = p.data; nm = p.names
    caches = [(e["serial_offset"], e["serial_offset"] + e["serial_size"]) for e in p.exports if p.class_name(e) == "ShaderCache"]
    if not caches: continue
    hits = []
    for a, b in caches:
        for m in REC.finditer(d, a, b):
            name = m.group(2).decode()
            if not any(w in name for w in want): continue
            end = d.find(b"Material", m.end(), b); end = b if end < 0 else end
            vf = {}; k = m.end() + 16
            while k < end - 12:
                x, z, c = struct.unpack_from(">III", d, k)
                if z == 0 and 0 < x < len(nm) and "VertexFactory" in str(nm[x]) and 0 < c < 64:
                    ents = []; j = k + 12
                    for _ in range(c):
                        t, z2 = struct.unpack_from(">II", d, j)
                        ents.append([str(nm[t]) if z2 == 0 and t < len(nm) else "?", d[j + 8:j + 24].hex()]); j += 32
                    vf[str(nm[x])] = ents; k = j
                else:
                    k += 4
            hits.append({"kind": m.group(1).decode(), "name": name, "vf": vf})
    if hits: res[f] = hits
    if n % 25 == 0: print(n, len(pkgs), f, flush=True)
json.dump(res, open(out, "w"), indent=1)
print("done", len(res))
