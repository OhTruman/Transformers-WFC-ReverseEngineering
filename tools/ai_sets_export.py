"""Read-only: export the GOAP action / goal sets and sensor sets referenced by the Escalation AI templates (TnAiCharacterDefinition
in TR_AiEscalation_p / TR_SpiderDec_AI_p): each blueprint's class and its authored (non-default) properties, plus the class-default
values of the same blueprint class for reference.
Usage: python ai_sets_export.py <out.json>"""
import sys, json, sqlite3
sys.dont_write_bytecode = True
db = sqlite3.connect(r"F:\Transformers Rebuild\AssetTools\manifests\authored.db")


def obj(o):
    r = db.execute("select class, props from objects where opath=?", (o,)).fetchone()
    return (r[0], json.loads(r[1] or "{}")) if r else (None, {})


def find(name):
    """Resolve a blueprint reference (full path or tail) to its object path."""
    r = db.execute("select opath from objects where opath=?", (name,)).fetchone()
    if r: return r[0]
    r = db.execute("select opath from objects where opath like ?", ("%." + name.split(".")[-1],)).fetchone()
    return r[0] if r else None


def cdo(cls):
    r = db.execute("select props from objects where opath like ?", ("%.Default__" + cls,)).fetchone()
    return json.loads(r[0] or "{}") if r else {}


out = {"templates": {}, "sets": {}}
for o, p in db.execute("select opath, props from objects where class='TnAiCharacterDefinition' and "
                       "(opath like 'TR_AiEscalation_p.%' or opath like 'TR_SpiderDec_AI_p.%')"):
    d = json.loads(p or "{}")
    out["templates"][o] = {k: d.get(k) for k in ("ActionSet", "GoalSet", "SensorSet", "PawnClass", "ActionOverrides",
                                                 "HeavyDamageThreshold", "HeavyDamageThresholdEnabled", "LootClassification")}
    out["templates"][o]["Character"] = d.get("AiCharacterDataResolved", {})
    for key in ("ActionSet", "GoalSet", "SensorSet"):
        s = d.get(key)
        if s and s not in out["sets"]:
            c, sd = obj(s)
            items = sd.get("ActionBlueprints") or sd.get("GoalBlueprints") or sd.get("Sensors") or []
            ent = []
            for it in items:
                path = find(it) if isinstance(it, str) else None
                bc, bp = obj(path) if path else (None, {})
                ent.append({"ref": it, "class": bc, "props": bp, "class_default": cdo(bc) if bc else {}})
            out["sets"][s] = {"class": c, "items": ent, "extra": {k: v for k, v in sd.items()
                                                                   if k not in ("ActionBlueprints", "GoalBlueprints", "Sensors")}}
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(len(out["templates"]), "templates", len(out["sets"]), "sets",
      sum(len(s["items"]) for s in out["sets"].values()), "items")
