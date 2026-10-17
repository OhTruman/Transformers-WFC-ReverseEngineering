"""Read-only: for every cooked map / Startup package, parse the material shader maps inside ShaderCache exports and list, per
vertex factory, the (shader type, shader GUID) entries. Packages are read directly (no pickle cache).

Record layout (verified against bUsesDistortion): a material's shader map comes BEFORE its label.
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
REC = re.compile(rb"(DecalMaterial|MaterialInstanceConstant|Material) ([A-Za-z0-9_.]+)\x00")
DIST_PS = "TDistortionMeshPixelShaderFDistortMeshAccumulatePolicy"


def chain(d, nm, k, n, stop):
    """Parse n VF blocks from k, each = u32 count, count x 32-byte entries, then the VF FName the entries belong to.
    Return (end, {VF: entries}) or None if the bytes do not form such a chain."""
    vf = {}
    for _ in range(n):
        if k + 4 > stop: return None
        c = struct.unpack_from(">I", d, k)[0]
        if c >= 64: return None
        k += 4; ents = []
        for _ in range(c):
            if k + 32 > stop: return None
            t, z = struct.unpack_from(">II", d, k)
            if not (z == 0 and t < len(nm) and "Shader" in str(nm[t])): return None
            ents.append([str(nm[t]), d[k + 8:k + 24].hex()]); k += 32
        if k + 8 > stop: return None
        x, z = struct.unpack_from(">II", d, k)
        if not (z == 0 and 0 <= x < len(nm) and "VertexFactory" in str(nm[x])): return None
        vf[str(nm[x])] = ents; k += 8
    return k, vf


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
            for k in range(lo, label - 3):              # u32 N (VF block count), then N blocks ending exactly at the label
                n = struct.unpack_from(">I", d, k)[0]
                if not 0 < n < 64: continue
                r = chain(d, nm, k + 4, n, label)
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
