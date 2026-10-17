"""Per-weapon firing-presentation audit: authored muzzle flash / tracer / impact / shell eject / anim notifies /
recoil + camera kick for every MP weapon (TransWeapons.ini TnDataProvider_Weapon), plus a read-only grep of the
Rebuild tree (src, data, work/render/**/*.json) for each authored asset leaf name.
Writes notes/data/weapon_presentation_audit.json. Usage: python weapon_presentation_audit.py"""
import json, os, re, sqlite3, collections

ROOT = r"F:\Transformers Rebuild"
DB = os.path.join(ROOT, r"AssetTools\manifests\authored.db")
INI = os.path.join(ROOT, r"ExtractedAssets\config\Coalesced_ini.json")
REBUILD = os.path.join(ROOT, "Rebuild")
OUT = os.path.join(ROOT, r"RE-Workspace\notes\data\weapon_presentation_audit.json")

db = sqlite3.connect(DB)
def get(o):
    r = db.execute("select class, props from objects where opath=?", (o,)).fetchone()
    return (r[0], json.loads(r[1])) if r else (None, {})

def cdo(cls):
    for pkg in ("TransContent", "TransGame"):
        c, d = get("%s.Default__%s" % (pkg, cls))
        if c: return d
    return {}

def resolve(cls, key):
    """Walk the class chain via authored.db class_path is not stored, so fall back to TransContent/TransGame CDO."""
    return cdo(cls).get(key)

ini = json.load(open(INI, encoding="utf-8"))
weapons = []
for f, secs in ini.items():
    for s, vals in secs.items():
        if s.endswith("TnDataProvider_Weapon"):
            weapons.append((s.split(" ")[0], vals["ObjectPath"][0]))

# notifies by package: sequence name -> list of notify descriptions
notifies = collections.defaultdict(lambda: collections.defaultdict(list))
seqname = {}
for o, c, p in db.execute("select opath, class, props from objects where substr(opath,1,4)='WEP_' and class='AnimSequence'"):
    seqname[o] = json.loads(p).get("SequenceName")
for o, c, p in db.execute("select opath, class, props from objects where substr(opath,1,4)='WEP_' and class like '%Notify%'"):
    d = json.loads(p); seq = o.rsplit(".", 1)[0]; pkg = o.split(".")[0]
    what = d.get("ParticleSystemTemplate") or d.get("SoundCue") or d.get("ProjectileClass") or d.get("Option")
    sock = d.get("SocketName")
    notifies[pkg][seqname.get(seq, seq.split(".")[-1])].append("%s:%s%s" % (c.replace("HmAnimNotify_", "").replace("TnAnimNotify_", ""),
                                                                            str(what).split(".")[-1], "@" + sock if sock else ""))

def leaf(v): return str(v).split(".")[-1] if v else None

rows = []
for uid, cpath in weapons:
    cls = cpath.split(".")[-1]
    W = cdo(cls)
    mesh_path = W.get("WeaponMeshTemplate"); data_path = W.get("MultiplayerData") or W.get("PlayerData"); sp_path = W.get("PlayerData")
    _, M = get(mesh_path) if mesh_path else (None, {})
    _, D = get(data_path) if data_path else (None, {})
    pkg = (mesh_path or "").split(".")[0]
    light = get(M["MuzzleFlashLight"])[1] if M.get("MuzzleFlashLight") else {}
    owner = get(D["OwnerAnimations"])[1] if D.get("OwnerAnimations") else {}
    proj = []
    for pr in D.get("WeaponProjectiles") or []:
        pc = cdo(leaf(pr)) if pr else {}
        proj.append({"class": leaf(pr), **{k: leaf(v) for k, v in pc.items() if any(t in k for t in ("Trail", "Explosion", "Flight", "Impact", "ProjFlight", "Effect")) and isinstance(v, str)}})
    n = {k: v for k, v in notifies.get(pkg, {}).items()}
    rows.append({
        "id": uid, "class": cls, "mesh": mesh_path, "data": data_path, "sp_data": sp_path,
        "sp_differs": {k: (get(sp_path)[1].get(k), D.get(k)) for k in ("RecoilCameraParams", "CameraShakeParams", "WeaponReloadAnimTime", "FireIntervalModifier") if sp_path and sp_path != data_path and get(sp_path)[1].get(k) != D.get(k)},
        "effects_type": leaf(M.get("WeaponEffectsType")),
        "muzzle_flashes": [(m.get("WeaponEventType"), leaf(m.get("PSTemplate")), m.get("PSLoops")) for m in M.get("MuzzleFlashes") or []],
        "muzzle_sockets": M.get("MuzzleFlashSockets"),
        "muzzle_light": {k: light.get(k) for k in ("Brightness", "Radius", "LightColor") if k in light} or None,
        "muzzle_flash_duration": M.get("MuzzleFlashDuration"),
        "tracers": [(t.get("WeaponEventType"), leaf(t.get("TracerTemplate"))) for t in M.get("TracerTemplates") or []],
        "default_squib": leaf(M.get("DefaultSquib")), "squib_pct": M.get("ImpactSquibPercentage"), "squib_max": M.get("ImpactSquibMaxCount"),
        "default_decal": leaf((M.get("DefaultDecal") or {}).get("Material")),
        "impact_sound": leaf(M.get("DefaultImpactSound")), "bullet_by": leaf(M.get("BulletBySound")),
        "event_anims": {a.get("WeaponEventType"): a.get("AnimName") for a in M.get("WeaponEventAnims") or []},
        "notifies": n,
        "projectiles": proj or None,
        "spine_recoil": M.get("SpineRecoil"), "hand_recoil": M.get("RightHandRecoil"),
        "camera_recoil": D.get("RecoilCameraParams"), "camera_shake": D.get("CameraShakeParams"),
        "heat": {"HeatPerShot": M.get("HeatPerShot"), "HeatCooldownTime": M.get("HeatCooldownTime")},
        "reload_time": D.get("WeaponReloadAnimTime"),
        "owner_anims": {k: v for k, v in owner.items() if isinstance(v, (str, list)) and "Anim" in k} or None,
    })

# grep Rebuild (read-only): src (text), data, work/render/**/*.json
corpus = []
for base in ("src", "data", os.path.join("work", "render")):
    for dp, dn, fn in os.walk(os.path.join(REBUILD, base)):
        for f in fn:
            if base.startswith("work") and not f.endswith(".json"): continue
            p = os.path.join(dp, f)
            try:
                if os.path.getsize(p) > 50_000_000: continue
                corpus.append((os.path.relpath(p, REBUILD), open(p, "rb").read().decode("latin1")))
            except OSError: pass

def present(name):
    if not name: return None
    hits = [rel for rel, txt in corpus if name in txt]
    return hits[:3] if hits else []

for r in rows:
    g = {}
    for key in ("muzzle", "tracer", "default_squib", "default_decal", "impact_sound", "shell"):
        if key == "muzzle": names = [m[1] for m in r["muzzle_flashes"]]
        elif key == "tracer": names = [t[1] for t in r["tracers"]]
        elif key == "shell": names = [x.split(":")[1].split("@")[0] for v in r["notifies"].values() for x in v if "Shell" in x]
        else: names = [r[key]]
        names = [x for x in dict.fromkeys(names) if x]
        g[key] = {x: present(x) for x in names}
    g["reload_anim"] = {r["event_anims"].get("WP_Reload"): present(r["event_anims"].get("WP_Reload"))} if r["event_anims"].get("WP_Reload") else {}
    g["class"] = {r["class"]: present(r["class"])}
    r["grep"] = g

json.dump(rows, open(OUT, "w"), indent=1, default=str)
print(len(rows), "weapons ->", OUT, "; corpus files", len(corpus))

# ---- markdown table (grep classes: C = src code, E = embedded asset JSON in src/game/CharacterAudio.inc,
#      R = work/render json / data, - = no hit; texture_formats.json ignored)
def cls_hits(h):
    if h is None: return ""
    h = [x for x in h if "texture_formats.json" not in x]
    s = ("C" if any(x.startswith("src") and "CharacterAudio.inc" not in x for x in h) else "") + \
        ("E" if any("CharacterAudio.inc" in x for x in h) else "") + \
        ("R" if any(x.startswith(("work", "data")) for x in h) else "")
    return s or "-"

def grepall(name):
    if not name: return None
    return [rel for rel, txt in corpus if name in txt]

def fmt(names):
    return ", ".join("%s [%s]" % (n, cls_hits(grepall(n))) for n in names if n) or "none"

def vec(r): return "(%g,%g,%g)" % (r.get("X", 0), r.get("Y", 0), r.get("Z", 0)) if r else "0"
lines = ["| Weapon | FX type | Muzzle flash (light) | Tracer / projectile | Impact squib / decal / sound | Shell eject | Reload / overheat (anim: notifies) | Spine / hand recoil (dur, rot amp) | Camera recoil / shake |",
         "|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    mf = fmt([m[1] for m in r["muzzle_flashes"]])
    lt = r["muzzle_light"]; mf += " (light %s/%s)" % (lt.get("Brightness", "-"), lt.get("Radius", "-")) if lt else ""
    tr = fmt([t[1] for t in r["tracers"]]) if r["tracers"] else ("proj " + ", ".join(str(p["class"]) for p in r["projectiles"] or []) + " [%s]" % cls_hits(grepall((r["projectiles"] or [{}])[0].get("class"))) if r["projectiles"] else "none")
    imp = "%s / %s / %s" % (fmt([r["default_squib"]]) if r["default_squib"] else "none", fmt([r["default_decal"]]) if r["default_decal"] else "none", r["impact_sound"] or "none")
    imp += " (%.0f%%, max %s)" % ((r["squib_pct"] or 1.0) * 100, r["squib_max"] or 10)
    shell = sorted({x.split(":")[1] for v in r["notifies"].values() for x in v if "Shell" in x or "Magazine" in x})
    sh = fmt([s.split("@")[0] for s in shell]) + (" @" + shell[0].split("@")[1] if shell and "@" in shell[0] else "") if shell else "none"
    rl = []
    for key in ("WP_Reload", "WP_Overheat"):
        a = r["event_anims"].get(key)
        if a: rl.append("%s: %s" % (a, "; ".join(r["notifies"].get(a, [])) or "-"))
    oh = [k for k in r["notifies"] if k.endswith("Overheat")]
    for k in oh:
        if not any(k in x for x in rl): rl.append("%s: %s" % (k, "; ".join(r["notifies"][k])))
    rl = " / ".join(rl) + (" [anim %s]" % cls_hits(grepall(r["event_anims"].get("WP_Reload"))) if r["event_anims"].get("WP_Reload") else "") if rl else "none"
    sp, hd = r["spine_recoil"], r["hand_recoil"]
    rc = "%s %s / %s %s" % (sp.get("TimeDuration", 0.33) if sp else "-", vec(sp.get("RotAmplitude")) if sp else "", hd.get("TimeDuration", 0.33) if hd else "-", vec(hd.get("RotAmplitude")) if hd else "")
    cr, cs = r["camera_recoil"] or {}, r["camera_shake"] or {}
    cam = "pitch %s fov %s t %s d %s / I %s roll %s fall %s" % (cr.get("PitchAdjustmentDeg", 0), cr.get("FovAdjustment", 0), cr.get("RecoilTime", "-"), cr.get("RecoilDelay", "-"),
                                                         cs.get("Intensity", "-"), cs.get("Roll", "-"), cs.get("ShakeFalloffDuration", "-"))
    lines.append("| %s (%s) | %s | %s | %s | %s | %s | %s | %s | %s |" % (r["id"], r["class"], r["effects_type"] or "(CDO)", mf, tr, imp, sh, rl, rc, cam))
open(OUT.replace(".json", ".md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("table ->", OUT.replace(".json", ".md"))
