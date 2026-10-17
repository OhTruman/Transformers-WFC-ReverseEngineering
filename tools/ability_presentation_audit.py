"""Ability presentation audit: for every MP ability (TransCustomization.ini TnDataProvider_Ability) collect the
authored presentation assets reachable from the ability CDO (trigger anim / sound / effect, buffs, spawned actors,
projectiles, blueprints; recursive over object references), the trigger anim's AnimNotifies (by SequenceName across
all packages), cooldown / resource values, and grep each asset leaf name in the Rebuild tree (read-only).
Writes notes/data/ability_presentation_audit.json + .md. Usage: python ability_presentation_audit.py"""
import json, os, re, sqlite3, collections

ROOT = r"F:\Transformers Rebuild"
db = sqlite3.connect(os.path.join(ROOT, r"AssetTools\manifests\authored.db"))
ini = json.load(open(os.path.join(ROOT, r"ExtractedAssets\config\Coalesced_ini.json"), encoding="utf-8"))
REBUILD = os.path.join(ROOT, "Rebuild")
OUT = os.path.join(ROOT, r"RE-Workspace\notes\data\ability_presentation_audit.json")

def get(o):
    r = db.execute("select class, props from objects where opath=?", (o,)).fetchone()
    return (r[0], json.loads(r[1])) if r else (None, {})

def cdo_of(cls_path):
    pkg, cls = cls_path.rsplit(".", 1)
    c, d = get("%s.Default__%s" % (pkg, cls))
    return ("%s.Default__%s" % (pkg, cls), d) if c else (None, {})

FX = re.compile(r"(_FX|\.FX\.)", re.I)
def kind(v):
    leaf = v.split(".")[-1]
    if FX.search(v) and ("FX_" in v or leaf.endswith("_FX")): return "fx"
    if v.startswith(("BL_", "SoundEvents", "SoundCue")) or re.match(r"^BL_|^[A-Z_]+\.[A-Z0-9_]+$", v): return "sound"
    if leaf.endswith(("_MAT", "_MATINST", "_MAT_INST", "_MIC")): return "material"
    if leaf.endswith(("_GFX",)) or "GFx" in v: return "gfx"
    return None

def collect(path, d, out, depth, seen):
    for k, v in d.items():
        vals = v if isinstance(v, list) else [v]
        for x in vals:
            if isinstance(x, dict):
                collect(path, x, out, depth, seen); continue
            if not isinstance(x, str): continue
            kd = kind(x)
            if kd: out[kd].add(x)
            # follow sub-objects / classes / blueprints
            if depth > 0 and x not in seen and "." in x and not kd:
                seen.add(x)
                c, dd = get(x)
                if not c and re.match(r"^(TransGame|TransContent|HM_Engine)\.[A-Za-z0-9_]+$", x):
                    p2, dd = cdo_of(x); c = bool(p2)
                if c:
                    if c == "PointLightComponent" or "Light" in str(c):
                        out["light"].add(json.dumps({kk: dd.get(kk) for kk in ("Brightness", "Radius", "LightColor") if kk in dd}))
                    collect(x, dd, out, depth - 1, seen)

seqs = collections.defaultdict(list)
for o, p in db.execute("select opath, props from objects where class='AnimSequence'"):
    n = json.loads(p).get("SequenceName")
    if n: seqs[n].append(o)
def notifies_for(anim):
    res = set()
    for s in seqs.get(anim, []):
        for o, c, p in db.execute("select opath, class, props from objects where opath like ? and class like '%Notify%'", (s + ".%",)):
            d = json.loads(p)
            w = d.get("ParticleSystemTemplate") or d.get("SoundCue") or d.get("ProjectileClass")
            res.add("%s:%s%s" % (c.replace("HmAnimNotify_", "").replace("TnAnimNotify_", ""), str(w).split(".")[-1],
                                 "@" + d["SocketName"] if d.get("SocketName") else ""))
    return sorted(res)

corpus = []
for base in ("src", "data", os.path.join("work", "render")):
    for dp, dn, fn in os.walk(os.path.join(REBUILD, base)):
        for f in fn:
            if base.startswith("work") and not f.endswith(".json"): continue
            if f == "texture_formats.json": continue
            p = os.path.join(dp, f)
            try: corpus.append((os.path.relpath(p, REBUILD), open(p, "rb").read().decode("latin1")))
            except OSError: pass
def gclass(name):
    h = [rel for rel, t in corpus if name in t]
    s = ("C" if any(x.startswith("src") and "CharacterAudio.inc" not in x for x in h) else "") + \
        ("E" if any("CharacterAudio.inc" in x for x in h) else "") + ("R" if any(x.startswith(("work", "data")) for x in h) else "")
    return s or "-"

rows = []
for f, secs in ini.items():
    for s, v in secs.items():
        if not s.endswith("TnDataProvider_Ability"): continue
        uid = s.split(" ")[0]; cpath = v["ObjectPath"][0]
        p, d = cdo_of(cpath)
        out = collections.defaultdict(set)
        collect(p, d, out, 3, set())
        # classes the ability script spawns by literal (e.g. TnBarrierSpawnable, TnRollerMineAbility)
        sf = os.path.join(ROOT, r"RE-Workspace\work\script\decomp", "TransGame.%s.txt" % cpath.split(".")[-1])
        script_refs = sorted(set(re.findall(r"obj'([A-Za-z0-9_]+)'", open(sf).read()))) if os.path.exists(sf) else []
        for ref in script_refs:
            for pk in ("TransGame", "TransContent"):
                p2, d2 = cdo_of("%s.%s" % (pk, ref))
                if p2: collect(p2, d2, out, 3, set()); break
        anim = (d.get("OnTriggerAnimParams") or {}).get("AnimName")
        nt = notifies_for(anim) if anim else []
        for n in nt:
            w = n.split(":")[1].split("@")[0]
            if w == "None": continue
            (out["fx"] if w.endswith("_FX") else out["sound"]).add(w)
        rows.append({"id": uid, "class": cpath.split(".")[-1], "specialty": v.get("SpecialtyRestriction", ["?"])[0],
                     "cooldown": d.get("Cooldown"), "resource": d.get("ResourceRequired"), "anim": anim,
                     "trigger_sound": d.get("OnTriggerSound"), "trigger_fx": d.get("OnTriggerEffect"), "trigger_socket": d.get("OnTriggerEffectSocket"),
                     "buffs": [x for x in [d.get("BuffToAdd")] + (d.get("BuffsToApply") or []) + (d.get("EffectBuffs") or []) if x],
                     "spawns": [x for x in (d.get("InventoryTypeToSpawn"), d.get("ProjectileType"), d.get("PawnFactory")) if x] + script_refs,
                     "notifies": [n for n in nt if ":None" not in n or "@" in n],
                     "assets": {k: sorted(v) for k, v in out.items()},
                     "grep": {k: {a.split(".")[-1]: gclass(a.split(".")[-1]) for a in v} for k, v in out.items() if k != "light"},
                     "grep_class": gclass(cpath.split(".")[-1])})
json.dump(rows, open(OUT, "w"), indent=1, default=str)

def cell(r, k):
    g = r["grep"].get(k, {})
    return ", ".join("%s [%s]" % (a, c) for a, c in sorted(g.items())) or "none"
L = ["| Ability (specialty) [class grep] | Cooldown / resource | Trigger anim + notifies | FX (all reachable) | Sounds | Materials / lights | Buffs / spawns |", "|---|---|---|---|---|---|---|"]
for r in rows:
    L.append("| %s (%s) [%s] | %s / %s | %s: %s | %s | %s | %s %s | %s |" % (
        r["id"], r["specialty"], r["grep_class"], r["cooldown"], r["resource"], r["anim"] or "-", "; ".join(r["notifies"]) or "-",
        cell(r, "fx"), cell(r, "sound"), cell(r, "material"), " ".join(r["assets"].get("light", [])) or "",
        ", ".join((x if isinstance(x, str) else str(x.get("BuffClass", x))).split(".")[-1] for x in r["buffs"] + r["spawns"]) or "-"))
open(OUT.replace(".json", ".md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print(len(rows), "abilities ->", OUT)
