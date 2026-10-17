"""Transformation / boost presentation audit per MP chassis (notes/data/mp_chassis_roster.json, 33 chassis):
ROBODEF -> vehicle form blueprint (HoverFX / BoostFx / JumpFX / DamagedFX), the vehicle and robot SoundEventSets (boost /
jump / transform events), the camera strategy set's transform strategies (+ Blend* values), and the AnimNotifies of the
Transform_* sequences in the robot's AnimSets. Each asset leaf is grepped (read-only) in Rebuild src / data /
work/render json. Writes notes/data/transform_presentation_audit.json + .md."""
import json, os, re, sqlite3, collections

ROOT = r"F:\Transformers Rebuild"
db = sqlite3.connect(os.path.join(ROOT, r"AssetTools\manifests\authored.db"))
REBUILD = os.path.join(ROOT, "Rebuild")
OUT = os.path.join(ROOT, r"RE-Workspace\notes\data\transform_presentation_audit.json")
roster = json.load(open(os.path.join(ROOT, r"RE-Workspace\notes\data\mp_chassis_roster.json")))["chassis"]

def get(o):
    r = db.execute("select class, props from objects where opath=?", (o,)).fetchone() if o else None
    return (r[0], json.loads(r[1])) if r else (None, {})

def leaf(v): return str(v).split(".")[-1] if v else None

seq_by_pkg = collections.defaultdict(dict)
for o, p in db.execute("select opath, props from objects where class='AnimSequence'"):
    n = json.loads(p).get("SequenceName")
    if n and (n.startswith("Transform_") or n.startswith("Boost") or "Dodge" in n or n.startswith("Hover")):
        seq_by_pkg[o.split(".")[0] + "." + o.split(".")[1]][n] = o
def notifies(seq_path):
    res = []
    for o, c, p in db.execute("select opath, class, props from objects where opath like ? and class like '%Notify%'", (seq_path + ".%",)):
        d = json.loads(p); w = d.get("ParticleSystemTemplate") or d.get("SoundCue") or d.get("CameraShake")
        if w is None and "Sound" not in c and "Effect" not in c: continue
        res.append("%s:%s%s" % (c.replace("HmAnimNotify_", "").replace("TnAnimNotify_", ""), leaf(w), "@" + d["SocketName"] if d.get("SocketName") else ""))
    return sorted(set(res))

corpus = []
for base in ("src", "data", os.path.join("work", "render")):
    for dp, dn, fn in os.walk(os.path.join(REBUILD, base)):
        for f in fn:
            if (base.startswith("work") and not f.endswith(".json")) or f == "texture_formats.json": continue
            p = os.path.join(dp, f)
            try: corpus.append((os.path.relpath(p, REBUILD), open(p, "rb").read().decode("latin1")))
            except OSError: pass
_gc = {}
def g(name):
    if not name or name == "None": return "?"
    if name in _gc: return _gc[name]
    h = [rel for rel, t in corpus if name in t]
    s = ("C" if any(x.startswith("src") and "CharacterAudio.inc" not in x for x in h) else "") + \
        ("E" if any("CharacterAudio.inc" in x for x in h) else "") + ("R" if any(x.startswith(("work", "data")) for x in h) else "")
    _gc[name] = s or "-"; return _gc[name]

def fxlist(lst): return ["%s@%s" % (leaf(x.get("ParticleSystemTemplate")), x.get("Socket")) for x in (lst or []) if isinstance(x, dict)]

rows = []
for ch in roster:
    rc, R = get(ch["ObjectPath"])
    vpath = R.get("TransformerVehicle")
    vc, V = get(vpath)
    _, VS = get(V.get("SoundEventSet"))
    _, RS = get(R.get("SoundEventSet"))
    vs = {leaf(e.get("Event")): leaf(e.get("Sound")) for e in VS.get("SoundEventSet", []) if e.get("Sound") and re.search(r"Boost|Jump|Transform|Hover|Land", str(e.get("Event")))}
    rs = {leaf(e.get("Event")): leaf(e.get("Sound")) for e in RS.get("SoundEventSet", []) if e.get("Sound") and re.search(r"Transform|Dodge|Hover|Jump|Land", str(e.get("Event")))}
    _, CS = get(R.get("Cameras"))
    cams = {}
    for st in CS.get("Strategies", []):
        t = leaf(st.get("Type"))
        if t and ("Transform" in t or t in ("TnDrivingCameraStrategyType", "TnHoveringCameraStrategyType", "TnOverTheShoulderCameraStrategyType")):
            _, SD = get(st.get("Strategy"))
            cams[t.replace("CameraStrategyType", "")] = {"strategy": leaf(st.get("Strategy")) or leaf(st.get("StrategyClass")),
                                                        **{k: v for k, v in SD.items() if "Blend" in k or "Transition" in k}}
    anim = {}
    for aset in (R.get("AnimSets") or []):
        for n, sp in seq_by_pkg.get(aset, {}).items():
            if n.startswith("Transform_To"):
                nt = notifies(sp)
                if nt: anim[n] = nt
    assets = set(fxlist(V.get("HoverFX")) + fxlist(V.get("BoostFx")) + fxlist(V.get("JumpFX")) + fxlist(V.get("DamagedFX")))
    rows.append({"chassis": ch["UniqueId"], "iconic": ch.get("UniqueIconicId"), "robodef": ch["ObjectPath"], "form": vc, "vehicle": vpath,
                 "hover_fx": fxlist(V.get("HoverFX")), "boost_fx": fxlist(V.get("BoostFx")), "jump_fx": fxlist(V.get("JumpFX")),
                 "damaged_fx": fxlist(V.get("DamagedFX")), "veh_sounds": vs, "robot_sounds": rs, "cameras": cams, "transform_notifies": anim,
                 "acrobatics": leaf(R.get("AcrobaticsManagerBlueprint")), "momentum": leaf(R.get("MomentumBlueprint"))})

json.dump(rows, open(OUT, "w"), indent=1, default=str)

def cg(items): return ", ".join(sorted({"%s [%s]" % (i, g(i.split("@")[0])) for i in items})) or "none"
L = ["| Chassis (iconic, form) | Boost FX | Hover / jump FX | Boost / jump sounds (vehicle set) | Transform anim notifies (robot AnimSets) | Transform cameras (to robot / to vehicle) |", "|---|---|---|---|---|---|"]
for r in rows:
    nts = sorted({x for v in r["transform_notifies"].values() for x in v})
    nt = ", ".join("%s [%s]" % (x, g(x.split(":")[1].split("@")[0])) for x in nts) or "none"
    cams = r["cameras"]
    tr, tv = cams.get("TnTransformToRobo", {}), cams.get("TnTransformToVehicle", {})
    cam = "%s (%s s) / %s (%s s) [%s]" % (tr.get("strategy"), tr.get("TransitionTime"), tv.get("strategy"), tv.get("TransitionTime"), g(tv.get("strategy")))
    L.append("| %s (%s, %s) | %s | %s | %s | %s | %s |" % (r["chassis"], r["iconic"], (r["form"] or "").replace("FormBlueprint", ""), cg(r["boost_fx"]),
             cg(r["hover_fx"] + r["jump_fx"]), ", ".join("%s=%s [%s]" % (k.replace("Auto_", ""), v, g(v)) for k, v in sorted(r["veh_sounds"].items())) or "none",
             nt, cam))
open(OUT.replace(".json", ".md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print(len(rows), "chassis ->", OUT)
