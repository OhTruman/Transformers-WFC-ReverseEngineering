"""Read-only: dump WFC AI character definitions (TnAiCharacterDefinition) with their GOAP action/goal blueprints,
sensor sets (incl. threat evaluators / tactical pickers) and action overrides, resolved from authored.db, plus
the AI weapon data (*_AI_WEPDATA). Output: notes/data/ai_definitions.json, notes/data/ai_weapon_data.json.
Usage: python ai_definitions_extract.py"""
import json, os, sqlite3
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db = sqlite3.connect(r"F:\Transformers Rebuild\AssetTools\manifests\authored.db")
OUT = os.path.join(ROOT, "notes", "data")


def P(o):
    r = db.execute("select class,props from objects where opath=?", (o,)).fetchone()
    return (r[0], json.loads(r[1] or "{}")) if r else (None, {})


def resolve(o, depth=0, seen=None):
    """Expand an object reference into {class, props}, recursing into subobject refs (paths under o)."""
    seen = seen if seen is not None else set()
    if not isinstance(o, str) or o in seen or depth > 4:
        return o
    seen.add(o)
    c, d = P(o)
    if c is None:
        return o

    def fix(v):
        if isinstance(v, str) and v.startswith(o + "."):
            return resolve(v, depth + 1, seen)
        if isinstance(v, list):
            return [fix(x) for x in v]
        if isinstance(v, dict):
            return {k: fix(x) for k, x in v.items()}
        return v
    return {"_path": o, "_class": c, **{k: fix(v) for k, v in d.items() if k not in ("SearchSpace",)}}


defs = {}
for (o,) in db.execute("select opath from objects where class='TnAiCharacterDefinition'"):
    c, d = P(o)
    entry = {"props": {k: v for k, v in d.items() if k not in ("SearchSpace", "ActionSet", "GoalSet", "SensorSet", "ActionOverrides")}}
    for k in ("ActionSet", "GoalSet"):
        s = d.get(k)
        if s:
            sc, sd = P(s)
            key = "ActionBlueprints" if k == "ActionSet" else "GoalBlueprints"
            entry[k] = {"_path": s, "blueprints": [resolve(b) for b in sd.get(key, [])]}
    s = d.get("SensorSet")
    if s:
        sc, sd = P(s)
        entry["SensorSet"] = {"_path": s, "sensors": [resolve(x) for x in sd.get("Sensors", [])],
                              "dynamic": [resolve(x) for x in P(sd["DynamicSensorSet"])[1].get("Sensors", [])] if sd.get("DynamicSensorSet") else []}
    entry["ActionOverrides"] = [resolve(x) for x in d.get("ActionOverrides", [])]
    defs[o] = entry
json.dump(defs, open(os.path.join(OUT, "ai_definitions.json"), "w"), indent=1)

wd = {}
for o, c, p in db.execute("select opath,class,props from objects where substr(opath,-11)='_AI_WEPDATA'"):
    wd[o] = {"class": c, **json.loads(p or "{}")}
json.dump(wd, open(os.path.join(OUT, "ai_weapon_data.json"), "w"), indent=1)
print("definitions", len(defs), "ai weapon data", len(wd))

# ---- behaviour summary: action blueprint class -> definitions using it + distinct parameter sets
import collections
use = collections.defaultdict(set); params = collections.defaultdict(collections.Counter)


def walk(bp, defname):
    c = bp.get("_class"); use[c].add(defname.split(".")[-1])
    p = {k: v for k, v in bp.items() if not k.startswith("_") and k not in ("ActionSet", "GoalSet", "EditVersion")}
    params[c][json.dumps(p, sort_keys=True, default=str)] += 1
    for sub in ("ActionSet",):
        if isinstance(bp.get(sub), dict):
            for x in bp[sub].get("ActionBlueprints", []):
                if isinstance(x, dict):
                    walk(x, defname)


for n, e in defs.items():
    for b in e.get("ActionSet", {}).get("blueprints", []):
        if isinstance(b, dict):
            walk(b, n)
summary = {c: {"definitions": sorted(use[c]), "param_sets": [{"count": k, "params": json.loads(p)} for p, k in params[c].most_common()]}
           for c in sorted(use, key=lambda c: -len(use[c]))}
json.dump(summary, open(os.path.join(OUT, "ai_behavior_summary.json"), "w"), indent=1)
print("behaviour classes", len(summary))
