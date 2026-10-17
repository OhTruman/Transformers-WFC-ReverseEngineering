"""Read-only: for every cooked map / Startup package, parse the material shader maps inside ShaderCache exports and list, per
vertex factory, the (shader type, shader GUID) entries. Packages are read directly (no pickle cache).

Record layout (verified against bUsesDistortion on MP_IAC_Streets_BASE_m): a material's per-VF lists come BEFORE its label.
  [VF block]* [FString "Material <path>" / "MaterialInstanceConstant <path>"] [material GUID] ...
  VF block = FName(VF) (u32 index, u32 0), u32 count, count x 32-byte entries (FName type, GUID, FName type); the last VF
  key right before the label has no count.
Only the contiguous chain of VF blocks that ends exactly at the label's FString length prefix is attributed to the material, so
shader bodies (which also carry VF FNames) are never read as map entries.

Usage: python shadermap_scan.py <out.json> <name-substring>[,...]        -> {pkg: [{kind, name, vf: {VF: [[type, guid], ...]}}]}
       python shadermap_scan.py <out.json> --distortion-allowlist        -> {pkg: [{kind, name, vf: [VF, ...]}]} for maps whose
                                                                           chain lists TDistortionMeshPixelShaderFDistortMeshAccumulatePolicy"""
import os, re, sys, json, struct
sys.dont_write_bytecode = True
sys.path.insert(0, r"F:\Transformers Rebuild\AssetTools\scripts\wfc")
import ue3pkg

DUMP = r"F:\Transformers Rebuild\Game Dump\TransGame\CookedXenon"
REC = re.compile(rb"(MaterialInstanceConstant|Material) ([A-Za-z0-9_.]+)\x00")
DIST_PS = "TDistortionMeshPixelShaderFDistortMeshAccumulatePolicy"


def chain(d, nm, k, stop):
    """Parse contiguous VF blocks from k; return (end, {VF: entries}) or None if the bytes at k are not a VF block."""
    vf = {}
    while k + 8 <= stop:
        if k + 8 == stop:                               # the map's last VF key carries no count (terminal block before the label)
            x, z = struct.unpack_from(">II", d, k)
            if z == 0 and 0 <= x < len(nm) and "VertexFactory" in str(nm[x]): vf.setdefault(str(nm[x]), []); k = stop
            break
        x, z, c = struct.unpack_from(">III", d, k)
        if not (z == 0 and 0 <= x < len(nm) and "VertexFactory" in str(nm[x]) and 0 <= c < 64):
            break
        ents = []; j = k + 12
        for _ in range(c):
            if j + 32 > stop: return None
            t, z2 = struct.unpack_from(">II", d, j)
            ents.append([str(nm[t]) if z2 == 0 and t < len(nm) else "?", d[j + 8:j + 24].hex()]); j += 32
        vf[str(nm[x])] = ents; k = j
    return (k, vf) if vf else None


def maps(p, want):
    d = p.data; nm = p.names; out = []
    for a, b in [(e["serial_offset"], e["serial_offset"] + e["serial_size"]) for e in p.exports if p.class_name(e) == "ShaderCache"]:
        ms = list(REC.finditer(d, a, b))
        for i, m in enumerate(ms):
            name = m.group(2).decode()
            if not any(w in name for w in want): continue
            label = m.start() - 4                       # FString length prefix
            lo = ms[i - 1].end() + 16 if i else a
            got = None
            for k in range(lo, label - 11, 4):
                x, z = struct.unpack_from(">II", d, k)
                if z != 0 or not (0 <= x < len(nm)) or "VertexFactory" not in str(nm[x]): continue
                r = chain(d, nm, k, label)
                if r and r[0] == label: got = r[1]; break
            if got is not None:
                out.append({"kind": m.group(1).decode(), "name": name, "vf": {v: e for v, e in got.items() if e}})
    return out


if __name__ == "__main__":
    outp = sys.argv[1]
    allow = sys.argv[2] == "--distortion-allowlist"
    want = [""] if allow else sys.argv[2].split(",")
    res = {}
    pkgs = sorted(f for f in os.listdir(DUMP) if f.endswith("_m.xxx") or f.startswith("Startup"))
    for n, f in enumerate(pkgs):
        try:
            p = ue3pkg.Package(os.path.join(DUMP, f))
        except Exception as ex:
            print("ERR", f, ex, flush=True); continue
        hits = maps(p, want)
        if allow:
            hits = [{"kind": h["kind"], "name": h["name"], "vf": sorted(v for v, e in h["vf"].items() if any(t == DIST_PS for t, g in e))}
                    for h in hits]
            hits = [h for h in hits if h["vf"]]
        if hits: res[f[:-4]] = hits
        if n % 25 == 0: print(n, len(pkgs), f, flush=True)
    json.dump(res, open(outp, "w"), indent=1)
    print("done", len(res))
