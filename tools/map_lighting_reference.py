"""Per-MP-map authored lighting intent (read-only reference): sun / sky lights, top-10 placed lights (Brightness x Radius),
height fogs + constant-density fog volumes, post-process (governing world settings + PostProcessVolumes, with what our
build carries), character light environments (+ Beast light-environment volumes). Sources: ExtractedAssets VerticalSlice
Maps/<MAP>/lighting.json + postprocess.json, AssetTools authored.db, Rebuild work/render/<MAP>/lighting.json (ours).
Writes notes/data/map_lighting_reference.json + .md."""
import json, math, os, sqlite3, collections

ROOT = r"F:\Transformers Rebuild"
VS = os.path.join(ROOT, r"ExtractedAssets\VerticalSlice\Maps")
OURS = os.path.join(ROOT, r"Rebuild\work\render")
OUT = os.path.join(ROOT, r"RE-Workspace\notes\data\map_lighting_reference.json")
db = sqlite3.connect(os.path.join(ROOT, r"AssetTools\manifests\authored.db"))

def rgb(c): return "%d/%d/%d" % tuple(c["rgb"]) if isinstance(c, dict) and "rgb" in c else (
    "%d/%d/%d" % (c.get("R", 0), c.get("G", 0), c.get("B", 0)) if isinstance(c, dict) else str(c))
def yawpitch(d):
    if not d: return "-"
    x, y, z = d
    return "yaw %.1f° pitch %.1f°" % (math.degrees(math.atan2(y, x)), math.degrees(math.atan2(z, math.hypot(x, y))))
def short(o): return (o or "").replace(".TheWorld.PersistentLevel.", ":")

POST_KEYS = ("bEnableBloom", "Bloom_Scale", "Bloom_Threshold", "bEnableDOF", "DOF_FocusType", "DOF_FocusDistance", "DOF_FocusNearFalloff",
             "DOF_FocusFarFalloff", "DOF_MaxNearBlurAmount", "DOF_MaxFarBlurAmount", "DOF_FalloffExponent", "DOF_BlurKernelSize",
             "bEnableMotionBlur", "MotionBlur_Amount", "bEnableSceneEffect", "Scene_Desaturation", "Scene_HighLights", "Scene_MidTones",
             "Scene_Shadows", "ColorCorrectionTexture", "bAllowAmbientOcclusion")
def pv(v):
    if isinstance(v, dict) and set(v) >= {"X", "Y", "Z"}: return "(%g, %g, %g)" % (v["X"], v["Y"], v["Z"])
    if isinstance(v, list): return "(" + ", ".join("%g" % x if isinstance(x, (int, float)) else str(x) for x in v) + ")"
    if isinstance(v, float): return "%g" % v
    return str(v).split(".")[-1] if isinstance(v, str) and "." in v and "_p" in v else str(v)

res = {}
for m in sorted(os.listdir(VS)):
    if not m.startswith("MP_"): continue
    L = json.load(open(os.path.join(VS, m, "lighting.json"), encoding="utf-8"))
    P = json.load(open(os.path.join(VS, m, "postprocess.json"), encoding="utf-8"))
    O = json.load(open(os.path.join(OURS, m, "lighting.json"), encoding="utf-8"))
    g = L["globals"]
    sun = []
    for key in ("dominant_baked_directional", "dynamic_fill_directional", "dynamic_sky_light"):
        x = g.get(key)
        if not x: continue
        pr = x.get("props", {})
        sun.append({"role": key, "light": x.get("light"), "class": x.get("class"), "brightness": x.get("brightness"), "color": rgb(x.get("color")),
                    "lower_color": rgb(pr.get("LowerColor")) if pr.get("LowerColor") else None, "lower_brightness": pr.get("LowerBrightness"),
                    "direction_ue": x.get("direction_ue"), "channels": x.get("channels_on"),
                    "cast_shadows": pr.get("CastShadows", True), "cast_dynamic_shadows": pr.get("CastDynamicShadows", True)})
    pts = []
    for l in L["lights"]:
        if l["class"] not in ("PointLightComponent", "SpotLightComponent"): continue
        pr = l.get("props", {}); b = l.get("brightness") or pr.get("Brightness", 1.0); r = pr.get("Radius", 1024.0)
        if pr.get("bEnabled") is False: continue
        pts.append({"object": l.get("object"), "class": l["class"].replace("LightComponent", ""), "brightness": b, "radius": r,
                    "falloff": pr.get("FalloffExponent", 2.0), "color": rgb(l.get("color")), "location_ue": [round(v) for v in (l.get("location_ue") or [])],
                    "score": b * r, "dyn_shadow": pr.get("CastDynamicShadows", True)})
    pts.sort(key=lambda p: -p["score"])
    fogs = [{"component": f.get("component"), "height": f["props"].get("Height"), "density": f["props"].get("Density"),
             "color": rgb(f.get("color")), "light_brightness": f["props"].get("LightBrightness"), "start": f["props"].get("StartDistance"),
             "extinction": f["props"].get("ExtinctionDistance"), "enabled": f["props"].get("bEnabled", True)} for f in (g.get("height_fogs") or [])]
    fv = []
    for o, c, p in db.execute("select opath, class, props from objects where package like ? and class like 'FogVolume%Component'", (m + "%",)):
        d = json.loads(p)
        fv.append({"component": o, "class": c, **{k: d[k] for k in d if k in ("Density", "SimpleLightColor", "ApproxFogLightColor", "bAffectsTranslucency",
                                                                              "StartDistance", "Height", "HalfDensityHeight", "MaxDistance")}})
    ws = P["world_settings"]; gw = P.get("governing_world")
    wset = next((v.get("effective") for k, v in ws.items() if k.startswith(gw or "~")), None) or next(iter(ws.values()), {}).get("effective", {})
    vols = [{"volume": v["volume"], "priority": v["props"].get("Priority"), "unbound": v["props"].get("bUnbound", False),
             "settings": {k: v["props"].get("Settings", {}).get(k) for k in POST_KEYS}} for v in P["volumes"]]
    ours = O.get("postprocess", {})
    osrc = ours.get("source") if isinstance(ours.get("source"), dict) else {}
    ofog = O.get("fog") or {}
    beast = [o for (o,) in db.execute("select opath from objects where package like ? and class in ('BeastLightEnvironmentVolume','BeastLightEnvironmentBox')", (m + "%",))]
    chars = {}
    for k, v in (L.get("characters") or {}).items():
        chars[k] = {"light_environment": v.get("light_environment"), "props": v.get("light_environment_props"), "mesh_lighting": v.get("mesh_lighting")}
    res[m] = {"sun_sky": sun, "top_lights": pts[:10], "n_point_spot": len(pts), "height_fogs": fogs, "fog_volumes": fv,
              "governing_world": gw, "world_post": {k: wset.get(k) for k in POST_KEYS}, "post_volumes": vols,
              "ours_post": {k: ours.get("settings", {}).get(k) for k in POST_KEYS}, "ours_post_source": sorted(set(osrc.values()))[:3],
              "ours_fog": {k: ofog.get(k) for k in ("Height", "Density", "LightColor", "LightBrightness", "StartDistance")},
              "ours_lights": len(O.get("lights") or []), "characters": chars, "beast_volumes": beast}

json.dump(res, open(OUT, "w"), indent=1, default=str)

L = []
for m, r in res.items():
    L += ["", "### %s" % m, "", "**Sun / sky** (UE direction = light travel direction)", "",
          "| Role | Light | Brightness | Colour sRGB | Lower (sky) | Direction | Channels | Shadows (static / dyn) |", "|---|---|---|---|---|---|---|---|"]
    for s in r["sun_sky"]:
        L.append("| %s | %s | %g | %s | %s | %s %s | %s | %s / %s |" % (s["role"], s["light"], s["brightness"] or 0, s["color"],
                 "%s × %s" % (s["lower_color"], s["lower_brightness"]) if s["lower_color"] else "-", pv(s["direction_ue"]), yawpitch(s["direction_ue"]),
                 ",".join(s["channels"] or []), s["cast_shadows"], s["cast_dynamic_shadows"]))
    L += ["", "**Top 10 placed lights** (Brightness × Radius; %d enabled point / spot lights; ours loads %d lights)" % (r["n_point_spot"], r["ours_lights"]), "",
          "| # | Light | Type | Brightness | Radius uu | Falloff | Colour | Location UE |", "|---|---|---|---|---|---|---|---|"]
    for i, p in enumerate(r["top_lights"], 1):
        L.append("| %d | %s | %s | %g | %g | %g | %s | %s |" % (i, short(p["object"]), p["class"], p["brightness"], p["radius"], p["falloff"], p["color"], p["location_ue"]))
    L += ["", "**Fog**", "", "| Component | Height uu | Density | Inscatter colour × brightness | Start | Extinction | Ours |", "|---|---|---|---|---|---|---|"]
    for f in r["height_fogs"]:
        mine = r["ours_fog"].get("Height") is not None and abs((r["ours_fog"]["Height"] or 0) - (f["height"] or 0)) < 1
        L.append("| %s | %g | %g | %s × %g | %g | %g | %s |" % (short(f["component"]), f["height"] or 0, f["density"] or 0, f["color"], f["light_brightness"] or 0,
                 f["start"] or 0, f["extinction"] or 0, "loaded" if mine else "-"))
    for f in r["fog_volumes"]:
        L.append("| %s (%s) | - | %s | %s | - | - | - |" % (short(f["component"]), f["class"].replace("FogVolume", "").replace("Component", ""), f.get("Density"), rgb(f.get("ApproxFogLightColor") or f.get("SimpleLightColor"))))
    if not r["height_fogs"] and not r["fog_volumes"]: L.append("| none | | | | | | |")
    L += ["", "**Post-process** (world = governing %s TnWorldInfo effective; volumes; ours = Rebuild lighting.json postprocess.settings, source %s)" % (r["governing_world"], ", ".join(short(x) for x in r["ours_post_source"]) or "-"), ""]
    hdr = ["Setting", "World"] + ["%s (prio %s%s)" % (short(v["volume"]).split(":")[-1], v["priority"], ", unbound" if v["unbound"] else "") for v in r["post_volumes"]] + ["Ours"]
    L += ["| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
    for k in POST_KEYS:
        row = [k, pv(r["world_post"].get(k))] + [pv(v["settings"].get(k)) for v in r["post_volumes"]] + [pv(r["ours_post"].get(k))]
        L.append("| " + " | ".join(row) + " |")
    L += ["", "**Characters**: " + "; ".join("%s: %s (%s)" % (k, short(v["light_environment"]), ", ".join("%s %s" % (a, pv(b)) for a, b in (v["props"] or {}).items() if a != "NormalizedSampleOffsets"))
                                             for k, v in r["characters"].items()) + ("; Beast light-environment volumes: %s" % ", ".join(short(b) for b in r["beast_volumes"]) if r["beast_volumes"] else "; no Beast light-environment volume")]
open(OUT.replace(".json", ".md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print({m: (len(r["sun_sky"]), len(r["height_fogs"]), len(r["fog_volumes"]), len(r["post_volumes"])) for m, r in res.items()})
