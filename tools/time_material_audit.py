"""Time-driven material audit (read-only). For every material our MP map builds translated (Rebuild work/render/<MAP>/
materials_glsl.json keys) plus every material the renderer drew (active_dump.jsonl), resolve the master Material in
authored.db and walk its graph from the connected outputs (static switches resolved with the values our translation
recorded in info.switches, else the expression default; material functions followed through their output / input pins). Time sources that reach an
output: Panner / Rotator (implicit time, or a Time input that itself depends on time), Time, FlipBookSample (the
TextureFlipBook's grid / FrameRate / FBMethod), TextureSampleParameterMovie, and Sine / Cosine whose input depends on time.
Ours (per material): K = our GLSL references m.time (info.uses), D = authored time reaches an output but our GLSL has no
time term, E = our translation errored, ? = drawn but not translated. Also: the MP map packages' matinee material-param
tracks. Writes notes/data/time_material_audit.json + .md."""
import json, os, sqlite3, collections

ROOT = r"F:\Transformers Rebuild"
RENDER = os.path.join(ROOT, r"Rebuild\work\render")
OUT = os.path.join(ROOT, r"RE-Workspace\notes\data\time_material_audit.json")
db = sqlite3.connect(os.path.join(ROOT, r"AssetTools\manifests\authored.db"))

objs = {}
for o, c, p in db.execute("select opath, class, props from objects where class like 'Material%' or class in ('TextureFlipBook')"):
    objs[o] = (c, json.loads(p))

OUTPUTS = ("DiffuseColor", "DiffusePower", "EmissiveColor", "SpecularColor", "SpecularPower", "Opacity", "OpacityMask",
           "Distortion", "TwoSidedLightingMask", "TwoSidedLightingColor", "Normal", "CustomLighting", "CustomSkylightDiffuse",
           "AnisotropicDirection", "WorldPositionOffset", "WorldDisplacement", "TessellationMultiplier", "SubsurfaceInscatteringColor",
           "SubsurfaceAbsorptionColor", "SubsurfaceScatteringRadius")
TIMECLS = {"MaterialExpressionTime", "MaterialExpressionFlipBookSample", "MaterialExpressionTextureSampleParameterMovie"}

def master_of(path):
    seen = [];  p = path
    while p in objs and objs[p][0] != "Material" and p not in seen:
        seen.append(p); p = objs[p][1].get("Parent")
    return p if p in objs and objs[p][0] == "Material" else None

def refs(props):
    """(expression, output index) for every input reference in an expression's properties."""
    out = []
    def rec(v):
        if isinstance(v, dict):
            e = v.get("Expression")
            if isinstance(e, str): out.append((e, int(v.get("ExpressionOutputIndex") or 0)))
            for k, x in v.items():
                if k != "Expression": rec(x)
        elif isinstance(v, list):
            for x in v: rec(x)
    rec(props); return out

def fref(v): return v.get("ref") if isinstance(v, dict) else v

class Walk:
    """Graph walk with material-function frames: a call's output index selects the OutputBlock pin; an InputBlock pin
    inside the function resolves to the call's matching input in the caller's frame."""
    def __init__(self, switches): self.sw = switches; self.memo = {}
    def inputs(self, path, out, ctx):
        c, p = objs.get(path, (None, {}))
        if c == "MaterialExpressionStaticSwitchParameter":
            val = self.sw.get(p.get("ParameterName"), bool(p.get("DefaultValue", False)))
            v = p.get("A" if val else "B") or {}
            return [(v["Expression"], int(v.get("ExpressionOutputIndex") or 0), ctx)] if v.get("Expression") else []
        if c == "MaterialExpressionFunction":
            f = fref(p.get("Function")); fp = objs.get(f, (None, {}))[1]
            ob = objs.get(fref(fp.get("OutputBlock")), (None, {}))[1]
            pins = ob.get("Pins") or []
            pin = next((x for x in pins if x.get("Id") == out), pins[out] if out < len(pins) else None)
            e = ((pin or {}).get("Input") or {})
            return [(e["Expression"], int(e.get("ExpressionOutputIndex") or 0), ctx + ((path, f),))] if e.get("Expression") else []
        if c == "MaterialExpressionIOBlock" and ctx:
            call, f = ctx[-1]
            if fref(objs.get(f, (None, {}))[1].get("InputBlock")) == path:
                ins = objs[call][1].get("Inputs") or []
                ib = p.get("Pins") or []
                k = next((i for i, x in enumerate(ib) if x.get("Id") == out), out)
                e = ins[k] if k < len(ins) else {}
                return [(e["Expression"], int(e.get("ExpressionOutputIndex") or 0), ctx[:-1])] if e.get("Expression") else []
            return []
        return [(e, o, ctx) for e, o in refs({k: v for k, v in p.items() if k not in ("Texture",)})]
    def timed(self, path, out=0, ctx=(), stack=()):
        """(depends_on_time, [time-source records]) for the subtree at path (output out, function frame ctx)."""
        key = (path, out, ctx)
        if key in self.memo: return self.memo[key]
        if key in stack or path not in objs or len(stack) > 400: return (False, [])
        c, p = objs[path]; st = stack + (key,)
        subs = [self.timed(e, o, cx, st) for e, o, cx in self.inputs(path, out, ctx)]
        dep = any(s[0] for s in subs); recs = [r for s in subs for r in s[1]]
        n = c.replace("MaterialExpression", "")
        where = ("" if not ctx else " in " + ctx[-1][1].split(".")[-1])
        def tin_live():
            t = p.get("Time") or {}
            return (not t.get("Expression")) or self.timed(t["Expression"], int(t.get("ExpressionOutputIndex") or 0), ctx, st)[0], bool(t.get("Expression"))
        if c == "MaterialExpressionPanner":
            live, has = tin_live()
            if live: dep = True; recs.append("Panner(%g, %g)%s%s" % (p.get("SpeedX", 0), p.get("SpeedY", 0), " time-in" if has else "", where))
        elif c == "MaterialExpressionRotator":
            live, has = tin_live()
            if live: dep = True; recs.append("Rotator(%g rad/s @%g,%g)%s" % (p.get("Speed", 0.25), p.get("CenterX", 0.5), p.get("CenterY", 0.5), where))
        elif c == "MaterialExpressionTime":
            dep = True; recs.append("Time" + where)
        elif c == "MaterialExpressionFlipBookSample":
            t = fref(p.get("Texture")); fb = objs.get(t, (None, {}))[1]
            dep = True; recs.append("FlipBook(%s %dx%d @%g fps%s)%s" % (str(t).split(".")[-1], fb.get("HorizontalImages", 1), fb.get("VerticalImages", 1),
                                                                       fb.get("FrameRate", 4.0), ", " + fb["FBMethod"] if fb.get("FBMethod") else "", where))
        elif c == "MaterialExpressionTextureSampleParameterMovie":
            dep = True; recs.append("Movie(%s)" % p.get("ParameterName"))
        elif c in ("MaterialExpressionSine", "MaterialExpressionCosine") and dep:
            recs.append("%s(period %g)%s" % (n, p.get("Period", 1.0), where))
        self.memo[key] = (dep, recs); return self.memo[key]

def audit_material(master, switches):
    w = Walk(switches); outs = {}
    _, mp = objs[master]
    for o in OUTPUTS:
        v = mp.get(o) if isinstance(mp.get(o), dict) else {}
        if not v.get("Expression"): continue
        dep, recs = w.timed(v["Expression"], int(v.get("ExpressionOutputIndex") or 0))
        if dep: outs[o] = sorted(collections.Counter(recs).items())
    return outs

result = {"time_source_ours": "WfcPipeline.cpp:8561 time_ = steady_clock seconds since the first rendered frame (process lifetime; "
                              "never paused, not reset on map change); WFC_LOCKSTEP: (frameNo - lockBase) / 60",
          "maps": {}}
for m in sorted(os.listdir(RENDER)):
    gp = os.path.join(RENDER, m, "materials_glsl.json")
    if not m.startswith("MP_") or not os.path.exists(gp): continue
    G = json.load(open(gp, encoding="utf-8"))
    drawn = collections.defaultdict(lambda: {"draws": 0, "tris": 0, "blend": set(), "comps": []})
    ad = os.path.join(RENDER, m, "active_dump.jsonl")
    if os.path.exists(ad):
        for L in open(ad, encoding="utf-8"):
            try: r = json.loads(L)
            except ValueError: continue
            mat = r.get("material")
            if not mat: continue
            d = drawn[mat]; d["draws"] += 1; d["tris"] += r.get("tris") or 0; d["blend"].add(r.get("blend"))
            if len(d["comps"]) < 6 and not r.get("authored_hidden"): d["comps"].append(r.get("component"))
    rows = []
    for mat in sorted(set(G) | set(drawn)):
        g = G.get(mat); info = (g or {}).get("info") or {}
        master = info.get("master") or master_of(mat)
        if not master or master not in objs: continue
        outs = audit_material(master, info.get("switches") or {})
        if not outs: continue
        if g is None: ours = "?"
        elif g.get("error"): ours = "E"
        else: ours = "K" if "time" in (info.get("uses") or []) else "D"
        approx = sorted({s for v in outs.values() for s, _ in v if "TFBM_" in s and "TFBM_UL_ROW" not in s})
        dd = drawn.get(mat, {"draws": 0, "tris": 0, "blend": set(), "comps": []})
        rows.append({"material": mat, "master": master, "ours": ours, "outputs": {k: [s for s, _ in v] for k, v in outs.items()},
                     "approx": approx, "lighting": info.get("lighting_model"), "blend_mode": info.get("blend_mode"),
                     "draws": dd["draws"], "tris": dd["tris"], "components": dd["comps"], "error": (g or {}).get("error")})
    result["maps"][m] = rows

# matinee material-parameter tracks in the MP map packages (Kismet / matinee driven MIC params)
tracks = []
for o, c, p, pk in db.execute("select opath, class, props, package from objects where substr(package,1,3)='MP_' and class in "
                              "('InterpTrackFloatMaterialParam','InterpTrackVectorMaterialParam','InterpTrackFloatProp','InterpTrackVectorProp',"
                              "'InterpTrackColorProp','InterpTrackLinearColorProp')"):
    d = json.loads(p); tr = d.get("FloatTrack") or d.get("VectorTrack") or {}
    pts = tr.get("Points") or []
    tracks.append({"track": o, "class": c, "param": d.get("ParamName") or d.get("PropertyName"),
                   "targets": d.get("Materials") or d.get("TargetMaterials"), "keys": len(pts),
                   "span": [pts[0].get("InVal"), pts[-1].get("InVal")] if pts else None,
                   "values": [pt.get("OutVal") for pt in pts][:6]})
result["matinee_tracks"] = tracks
json.dump(result, open(OUT, "w"), indent=1, default=str)

L = ["Ours: K = our GLSL keeps a time term (m.time; time source: %s), D = time dropped, E = translation error, ? = drawn, not translated. "
     "K means the term exists, not that speed / phase match. approx = FlipBook FBMethod other than TFBM_UL_ROW (ours is always row order)."
     % result["time_source_ours"], ""]
tot = collections.Counter()
for m, rows in result["maps"].items():
    c = collections.Counter(r["ours"] for r in rows); tot.update(c)
    L += ["### %s: %d time-driven materials (%s)" % (m, len(rows), ", ".join("%s %d" % kv for kv in sorted(c.items()))), "",
          "| Material (master) | Ours | Time sources by output | Draws / tris | Lighting / blend |", "|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["ours"] == "K", -r["tris"])):
        srcs = "; ".join("%s: %s" % (o, ", ".join(v)) for o, v in r["outputs"].items())
        L.append("| %s (%s) | %s%s | %s | %d / %d | %s / %s |" % (r["material"], r["master"].split(".")[-1], r["ours"],
                 " approx" if r["approx"] else "", srcs.replace("|", "/"), r["draws"], r["tris"],
                 (r["lighting"] or "").replace("MLM_", ""), (r["blend_mode"] or "").replace("BLEND_", "")))
    L.append("")
L += ["### Matinee property / material-parameter tracks in the MP map packages", "", "| Track | Class | Param / property | Keys (span s) | Values |", "|---|---|---|---|---|"]
for t in tracks:
    L.append("| %s | %s | %s | %d (%s) | %s |" % (t["track"], t["class"].replace("InterpTrack", ""), t["param"], t["keys"], t["span"], str(t["values"])[:120]))
open(OUT.replace(".json", ".md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print(dict(tot), "tracks", len(tracks))
