"""Build work/handoff/distortion_allowlist.json + distortion_allowlist/<MAP>.json from a `shadermap_scan.py --distortion-allowlist` result.
Masters are resolved through the authored.db Parent chain; mp_maps = union over the map's packages + Startup_FRA / Startup_int.
Usage: python distortion_allowlist.py <scan.json>"""
import os, sys, json, sqlite3
sys.dont_write_bytecode = True
OUT = r"F:\Transformers Rebuild\RE-Workspace\work\handoff"
MAPS = ["MP_ESC_BrokenHope", "MP_ESC_Remnant", "MP_IAC_Berth", "MP_IAC_Rust", "MP_IAC_Seed", "MP_IAC_Streets", "MP_KON_Molten",
        "MP_ORB_Debris", "MP_UND_Complex", "MP_UND_Gorge"]
SCHEMA = ("distortion_allowlist v3 (2026-10-18; v2 VF labels were shifted by one block, see SHADERMAP_VF_LABEL_CORRECTION_RE.md): "
          "packages = {package: [{material (as labelled in the cooked shader map), master (resolved via authored.db Parent chain), "
          "vf: [vertex factories whose map lists TDistortionMeshPixelShaderFDistortMeshAccumulatePolicy]}]}; mp_maps = {MP map: "
          "[{material: MASTER path, vf: [...]}]} = union over the map's BASE/ART/AUDIO packages + Startup_FRA/Startup_int. "
          "Absent (material, VF) = no distortion pass cooked. Tools: RE-Workspace/tools/shadermap_scan.py --distortion-allowlist, "
          "tools/distortion_allowlist.py.")

db = sqlite3.connect(r"F:\Transformers Rebuild\AssetTools\manifests\authored.db")


def master(path):
    seen = set()
    while path and path not in seen:
        seen.add(path)
        r = db.execute("select class, props from objects where opath=?", (path,)).fetchone()
        if not r or r[0] != "MaterialInstanceConstant": return path
        path = json.loads(r[1] or "{}").get("Parent") or path
    return path


scan = json.load(open(sys.argv[1]))
pk = {p: [{"material": h["name"], "master": master(h["name"]), "vf": h["vf"]} for h in hs] for p, hs in sorted(scan.items())}
mp = {}
for m in MAPS:
    acc = {}
    for p, hs in pk.items():
        if p.lower().startswith(m.lower() + "_") or p in ("Startup_FRA", "Startup_int"):
            for h in hs: acc.setdefault(h["master"], set()).update(h["vf"])
    mp[m] = [{"material": k, "vf": sorted(v)} for k, v in sorted(acc.items())]
json.dump({"schema": SCHEMA, "packages": pk, "mp_maps": mp}, open(os.path.join(OUT, "distortion_allowlist.json"), "w"), indent=1)
for m, v in mp.items():
    json.dump({"map": m, "materials": v}, open(os.path.join(OUT, "distortion_allowlist", m + ".json"), "w"), indent=1)
print({m: len(v) for m, v in mp.items()})
