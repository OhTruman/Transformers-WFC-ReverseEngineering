"""Melee presentation audit: for every player TnMeleeSet referenced by MP chassis ROBODEFs, list each attack (type, weapon
types, anim, damage, impulse, dash) with the anim's AnimNotifies in the chassis' AnimSets (sounds, effects, damage sweeps,
camera shakes with params), plus the SharedHitEffectPlayer hit / block FX + sounds for the melee damage types.
Grep (read-only) of each asset leaf in Rebuild src / data / work/render json.
Writes notes/data/melee_presentation_audit.json + .md."""
import json, os, re, sqlite3, collections

ROOT = r"F:\Transformers Rebuild"
db = sqlite3.connect(os.path.join(ROOT, r"AssetTools\manifests\authored.db"))
REBUILD = os.path.join(ROOT, "Rebuild")
OUT = os.path.join(ROOT, r"RE-Workspace\notes\data\melee_presentation_audit.json")
roster = json.load(open(os.path.join(ROOT, r"RE-Workspace\notes\data\mp_chassis_roster.json")))["chassis"]

def get(o):
    r = db.execute("select class, props from objects where opath=?", (o,)).fetchone() if o else None
    return (r[0], json.loads(r[1])) if r else (None, {})
def leaf(v): return str(v).split(".")[-1] if v else None

# melee set -> chassis using it, and their AnimSets
sets = collections.defaultdict(lambda: {"chassis": [], "animsets": set()})
for ch in roster:
    _, R = get(ch["ObjectPath"])
    ms = R.get("MeleeSet")
    if ms:
        sets[ms]["chassis"].append(ch["UniqueId"]); sets[ms]["animsets"].update(R.get("AnimSets") or [])

seq_index = collections.defaultdict(list)
for o, p in db.execute("select opath, props from objects where class='AnimSequence'"):
    n = json.loads(p).get("SequenceName")
    if not n: continue
    seq_index[(o.split(".")[0] + "." + o.split(".")[1], n)].append(o)
    m = re.match(r"^(.*)_0\d$", n)          # numbered variants Melee_Axe_01.._03 resolve the base name (H: random variant)
    if m: seq_index[(o.split(".")[0] + "." + o.split(".")[1], m.group(1))].append(o)

def notifies(animsets, anim):
    res = set()
    for a in animsets:
        for sp in seq_index.get((a, anim), []):
            for o, c, p in db.execute("select opath, class, props from objects where opath like ? and class like '%Notify%'", (sp + ".%",)):
                d = json.loads(p); cl = c.replace("HmAnimNotify_", "").replace("TnAnimNotify_", "")
                if "CameraShake" in c:
                    sp_ = d.get("ShakeParams", {}); res.add("CameraShake(I %.2g, roll %.2g, fall %.2g)" % (sp_.get("Intensity", 0), sp_.get("Roll", 0), sp_.get("ShakeFalloffDuration", 0)))
                    continue
                w = d.get("ParticleSystemTemplate") or d.get("SoundCue")
                if w is None and cl not in ("ImpactDamageSweep", "DamageSweep"): continue
                res.add("%s:%s%s" % (cl, leaf(w) or "", "@" + d["SocketName"] if d.get("SocketName") else ""))
    return sorted(res)

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
    if not name: return "?"
    if name in _gc: return _gc[name]
    h = [rel for rel, t in corpus if name in t]
    s = ("C" if any(x.startswith("src") and "CharacterAudio.inc" not in x for x in h) else "") + \
        ("E" if any("CharacterAudio.inc" in x for x in h) else "") + ("R" if any(x.startswith(("work", "data")) for x in h) else "")
    _gc[name] = s or "-"; return _gc[name]

rows = []
for ms, info in sorted(sets.items()):
    _, M = get(ms)
    for a in M.get("Attacks", []):
        nt = notifies(info["animsets"], a.get("AnimName"))
        dash = a.get("AttackDash") or {}
        rows.append({"set": leaf(ms), "chassis": info["chassis"], "type": (a.get("MeleeType") or "").replace("MELEE_", ""),
                     "weapons": [w.replace("MWT_", "") for w in a.get("MeleeWeaponTypes") or []], "anim": a.get("AnimName"),
                     "damage": a.get("Damage"), "dtype": leaf(a.get("DamageType")), "impulse": a.get("Impulse"),
                     "dash": "%g for %g s (end x%g)" % (dash.get("Speed", 0), dash.get("Time", 0), dash.get("EndVelocityScaler", 0)),
                     "ground_speed_mult": a.get("GroundSpeedMultiplier"), "allow_flight": a.get("AllowFlight"), "notifies": nt})

_, H = get("TR_HitEffectPlayer_p.SharedHitEffectPlayer")
melee_dt = {r["dtype"] for r in rows}
hits = [{"dtype": leaf(e.get("DamageType")), "fx": leaf(e.get("PSTemplate")), "block_fx": leaf(e.get("BlockEffect")),
         "hit_sound": leaf(e.get("HitSound")), "block_sound": leaf(e.get("BlockSound")), "camera": leaf(e.get("CameraEffect")), "retrigger": e.get("RetriggerTime")}
        for e in H.get("Effects", []) if leaf(e.get("DamageType")) in melee_dt | {"TnDamageTypeMeleeBerzerk", "TnDamageTypeShoulderSlam", "TnDamageTypeWeakMelee", "TnDamageTypeRammed"}]
json.dump({"attacks": rows, "hit_effects": hits}, open(OUT, "w"), indent=1, default=str)

def nfmt(nt): return "; ".join("%s [%s]" % (x, g(x.split(":")[1].split("@")[0])) if ":" in x and x.split(":")[1].split("@")[0] else x for x in nt) or "none"
L = ["| Melee set (chassis) | Attack (weapon types) | Anim [grep] | Damage / type / impulse | Dash (speed, time, end scale) | Notifies: sounds / FX / sweeps / camera shake |", "|---|---|---|---|---|---|"]
for r in rows:
    L.append("| %s (%d chassis) | %s (%s) | %s [%s] | %g / %s / %g | %s | %s |" % (r["set"], len(r["chassis"]), r["type"], ",".join(r["weapons"]), r["anim"], g(r["anim"]),
             r["damage"] or 0, r["dtype"], r["impulse"] or 0, r["dash"], nfmt(r["notifies"])))
L += ["", "| Hit damage type | Hit FX | Block FX | Hit sound | Block sound | Camera effect | Retrigger |", "|---|---|---|---|---|---|---|"]
for h in hits:
    L.append("| %s | %s [%s] | %s [%s] | %s [%s] | %s [%s] | %s | %s |" % (h["dtype"], h["fx"], g(h["fx"]), h["block_fx"], g(h["block_fx"]), h["hit_sound"], g(h["hit_sound"]),
             h["block_sound"], g(h["block_sound"]), h["camera"], h["retrigger"]))
open(OUT.replace(".json", ".md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print(len(rows), "attacks,", len(hits), "hit rows ->", OUT)
