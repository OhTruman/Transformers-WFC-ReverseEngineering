"""Top time-driven surfaces by visibility, with crop coordinates (read-only). Input: notes/data/time_material_audit.json.
Score = placed surface proxy x weight: per placed instance and mesh section, (bbox diagonal of that glTF primitive in m x
the instance scale)^2, summed (decals: width x height in m^2), x weight (3 = the time term reaches EmissiveColor or Opacity of an unlit / translucent material,
2 = it reaches DiffuseColor / Normal, 1 = otherwise). Location: the first placed component of that material in
ExtractedAssets/VerticalSlice/Maps/<MAP>/props.json (component ue_matrix translation; decals / emitters by actor),
plus the instance count. Camera: the nearest player start (spawnpoints.json) with the UE yaw / pitch that faces the
target. Max 3 per map. Writes notes/data/time_offenders.json + .md."""
import json, math, os, collections
CONTENT = r"F:\Transformers Rebuild\ExtractedAssets"
_gb = {}
def section_diags(gltf):
    """bbox diagonal (m) of each primitive of a glTF (section order)."""
    if gltf in _gb: return _gb[gltf]
    out = []
    try:
        g = json.load(open(os.path.join(CONTENT, gltf), encoding="utf-8"))
        for prim in g["meshes"][0]["primitives"]:
            a = g["accessors"][prim["attributes"]["POSITION"]]
            out.append(math.dist(a["min"], a["max"]))
    except (OSError, KeyError, ValueError, IndexError): pass
    _gb[gltf] = out; return out

ROOT = r"F:\Transformers Rebuild"
VS = os.path.join(ROOT, r"ExtractedAssets\VerticalSlice\Maps")
OUT = os.path.join(ROOT, r"RE-Workspace\notes\data\time_offenders.json")
A = json.load(open(os.path.join(ROOT, r"RE-Workspace\notes\data\time_material_audit.json")))

def weight(r):
    o = r["outputs"]
    if ("EmissiveColor" in o or "Opacity" in o) and (r["lighting"] == "MLM_Unlit" or (r["blend_mode"] or "") not in ("BLEND_Opaque", "BLEND_Masked")):
        return 3
    if "EmissiveColor" in o: return 3
    if "DiffuseColor" in o or "Normal" in o: return 2
    return 1

cands = []
for m, rows in A["maps"].items():
    pj = json.load(open(os.path.join(VS, m, "props.json"), encoding="utf-8"))
    sp = json.load(open(os.path.join(VS, m, "spawnpoints.json"), encoding="utf-8"))["points"]
    starts = [p for p in sp if "PlayerStart" in p.get("class", "") and p.get("location_ue")]
    comp = {}
    for p in pj["props"]:
        if p.get("component"): comp[p["component"].lower()] = p["ue_matrix"][3][:3]
        else: comp[(p["sublevel"] + ".TheWorld.PersistentLevel." + p["actor"]).lower()] = p.get("location_ue")
    bymat = collections.defaultdict(list); area = collections.Counter()
    for p in pj["props"]:
        loc = p["ue_matrix"][3][:3] if p.get("component") else p.get("location_ue")
        sc = max(math.sqrt(sum(x * x for x in p["ue_matrix"][i][:3])) for i in range(3))
        diags = section_diags(p.get("gltf") or "")
        ov = p.get("material_overrides") or []
        for i, s_ in enumerate(p.get("section_materials") or []):
            s_ = (ov[i] if i < len(ov) and ov[i] else s_)
            if not s_: continue
            bymat[s_].append(loc)
            area[s_] += ((diags[i] if i < len(diags) else (diags[0] if diags else 1.0)) * sc) ** 2
    for d in pj["decals"]:
        bymat[d.get("material")].append(d.get("location_ue")); area[d.get("material")] += ((d.get("width") or 0) / 100.0) * ((d.get("height") or 0) / 100.0)
    for r in rows:
        if not area.get(r["material"]): continue
        locs = [x for x in bymat.get(r["material"], []) if x]
        if not locs:
            for c in r["components"]:
                key = c.split("#")[0].lower()
                if key in comp and comp[key]: locs.append(comp[key])
                else:
                    act = ".".join(c.split("#")[0].split(".")[:4]).lower()
                    if act in comp and comp[act]: locs.append(comp[act])
        tgt = locs[0] if locs else None
        cam = None
        if tgt and starts:
            s = min(starts, key=lambda p: sum((a - b) ** 2 for a, b in zip(p["location_ue"], tgt)))
            dx, dy, dz = (t - c for t, c in zip(tgt, s["location_ue"]))
            dist = math.sqrt(dx * dx + dy * dy + dz * dz)
            cam = {"start": s["actor"], "location_ue": s["location_ue"], "dist_uu": round(dist),
                   "yaw_ue": round(math.atan2(dy, dx) * 32768 / math.pi) % 65536,
                   "pitch_ue": round(math.atan2(dz, math.hypot(dx, dy)) * 32768 / math.pi)}
        srcs = sorted({s for v in r["outputs"].values() for s in v})
        cands.append({"map": m, "material": r["material"], "master": r["master"], "ours": r["ours"], "score": round(area[r["material"]] * weight(r)), "area_m2": round(area[r["material"]]),
                      "tris": r["tris"], "draws": r["draws"], "outputs": sorted(r["outputs"]), "sources": srcs,
                      "instances": len(locs), "target_ue": [round(x) for x in tgt] if tgt else None, "camera": cam})

cands.sort(key=lambda c: -c["score"])
top, per = [], collections.Counter()
for c in cands:                                     # one per map first (every map represented), then by score, max 3 / map
    if per[c["map"]] == 0 and c["target_ue"]: top.append(c); per[c["map"]] += 1
for c in cands:
    if len(top) >= 20: break
    if c in top or per[c["map"]] >= 3 or not c["target_ue"]: continue
    top.append(c); per[c["map"]] += 1
top.sort(key=lambda c: -c["score"])
json.dump({"top": top, "all_ranked": cands[:200]}, open(OUT, "w"), indent=1)
L = ["| # | Map | Material (master) | Time sources -> outputs | Surface proxy m² (weight) | Target UE (x, y, z) / instances | Camera: nearest start, dist, yaw / pitch (UE units) |",
     "|---|---|---|---|---|---|---|"]
for i, c in enumerate(top, 1):
    cam = c["camera"] or {}
    L.append("| %d | %s | %s (%s) | %s -> %s | %d (×%d) | %s / %d | %s @ %s, %s uu, %s / %s |" % (
        i, c["map"], c["material"], c["master"].split(".")[-1], "; ".join(c["sources"])[:160], ", ".join(c["outputs"]),
        c["area_m2"], c["score"] // max(c["area_m2"], 1), c["target_ue"], c["instances"], cam.get("start"), [round(x) for x in cam.get("location_ue", [])],
        cam.get("dist_uu"), cam.get("yaw_ue"), cam.get("pitch_ue")))
open(OUT.replace(".json", ".md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print(len(cands), "candidates;", len(top), "top")
