"""Module-class census for the MP-relevant ParticleSystems (work/q/ps_refs.json: systems referenced from MP maps, weapons,
abilities/buffs, deaths/hit effects, chassis, anim notifies). Decodes every emitter LOD's compiled module stream with
AssetTools' pstream.system() (imported read-only, no bytecode written) and adds the tagged RequiredModule / TypeData classes.
Writes notes/data/particle_module_census.json."""
import sys, os, json, collections
sys.dont_write_bytecode = True
sys.path.insert(0, r"F:\Transformers Rebuild\AssetTools\scripts\wfc")
import pstream
refs = json.load(open(r"F:\Transformers Rebuild\RE-Workspace\work\q\ps_refs.json"))
out = {"systems": {}, "errors": {}}
for i, (ps, cats) in enumerate(sorted(refs.items())):
    try:
        s = pstream.system(ps)
    except Exception as ex:
        out["errors"][ps] = str(ex)[:200]; continue
    ems = []
    for e in s.get("emitters", []):
        lods = []
        for L in e.get("lods", []):
            lods.append({"lod": L.get("lod"), "typedata": (L.get("TypeDataModule") or L.get("type_data") or {}).get("class") if isinstance(L.get("TypeDataModule") or L.get("type_data"), dict) else L.get("type_data_class"),
                         "modules": [(m["module"], m.get("module_class"), (m.get("raw_flags") or [1, 1])[0]) for m in L.get("compiled_modules", [])],
                         "error": L.get("compiled_modules_error"), "complete": L.get("assignment_complete")})
        ems.append({"emitter": e.get("name") or e.get("emitter"), "lods": lods, "keys": sorted(e.keys())[:30]})
    out["systems"][ps] = {"cats": cats, "emitters": ems, "lod_keys": sorted(s["emitters"][0]["lods"][0].keys()) if s.get("emitters") and s["emitters"][0].get("lods") else []}
    if i % 25 == 0: print(i, ps, flush=True)
json.dump(out, open(r"F:\Transformers Rebuild\RE-Workspace\notes\data\particle_module_census.json", "w"), indent=0)
print("done", len(out["systems"]), "errors", len(out["errors"]))
