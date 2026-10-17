"""Read-only: export every LensFlare template (CDO defaults merged per element) and every placed LensFlareComponent with its
LensFlareSource actor transform, from authored.db, to notes/data/lens_flares.json.
Distribution values are the cooked FRawDistribution lookup tables, unchanged (decode as for particle distributions).
Usage: python lensflare_export.py [out.json]"""
import sys, json, sqlite3
sys.dont_write_bytecode = True
OUT = sys.argv[1] if len(sys.argv) > 1 else r"F:\Transformers Rebuild\RE-Workspace\notes\data\lens_flares.json"
db = sqlite3.connect(r"F:\Transformers Rebuild\AssetTools\manifests\authored.db")
props = lambda o: json.loads((db.execute("select props from objects where opath=?", (o,)).fetchone() or ["{}"])[0] or "{}")

cdo = props("Engine.Default__LensFlare")
cdo_el = cdo["SourceElement"]


def element(e):
    out = dict(cdo_el); out.update(e)
    for k, v in e.items():                                   # partially authored distributions keep the CDO's other fields
        if isinstance(v, dict) and isinstance(cdo_el.get(k), dict):
            m = dict(cdo_el[k]); m.update(v); out[k] = m
    return out


templates = {}
for o, p in db.execute("select opath, props from objects where class='LensFlare'"):
    d = json.loads(p)
    t = {k: v for k, v in cdo.items() if k != "SourceElement"}
    t.update({k: v for k, v in d.items() if k not in ("SourceElement", "Reflections", "ThumbnailImage", "ThumbnailImageOutOfDate",
                                                     "CurveEdSetup")})
    t["SourceElement"] = element(d.get("SourceElement", {}))
    t["Reflections"] = [element(e) for e in d.get("Reflections", [])]
    templates[o] = t

placed = []
for pk, o, p in db.execute("select package, opath, props from objects where class='LensFlareComponent'"):
    owner = o.rsplit(".", 1)[0]
    a = props(owner)
    placed.append({"package": pk, "component": o, "owner": owner, "template": json.loads(p).get("Template"),
                   "component_props": json.loads(p),
                   "location": a.get("Location"), "rotation": a.get("Rotation"), "draw_scale": a.get("DrawScale"),
                   "draw_scale3d": a.get("DrawScale3D"), "owner_props": {k: v for k, v in a.items() if k not in ("Components",)}})
json.dump({"lensflare_cdo": cdo, "component_cdo": props("Engine.Default__LensFlareComponent"), "templates": templates,
           "placements": placed}, open(OUT, "w"), indent=1)
print(len(templates), "templates,", len(placed), "placements ->", OUT)
