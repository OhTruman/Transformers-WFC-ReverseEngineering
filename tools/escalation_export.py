"""Read-only: export the Escalation (SV) data for MP_ESC_BrokenHope / MP_ESC_Remnant from authored.db:
spawn list (enemy table, waves, timings), generators (name key, PowerLevels, DrainRate, location), the TnSurvivalGame /
GRI / respawn class defaults, and for every TnSeqEvent_SurvivalGenerator / TnSeqEvent_SurvivalEvents the Kismet reached
downstream (forward walk over output links, through ActivateRemoteEvent -> SeqEvent_RemoteEvent, Delay, Gate, Switch ...),
listing each action with its class, the input it receives, its comment and its object variables (targets).
Usage: python escalation_export.py <outdir>"""
import os, sys, json, sqlite3, collections
sys.dont_write_bytecode = True
db = sqlite3.connect(r"F:\Transformers Rebuild\AssetTools\manifests\authored.db")
MAPS = {"MP_ESC_BrokenHope": "MP_ESC_BrokenHope_", "MP_ESC_Remnant": "MP_ESC_Remnant_"}
props = lambda o: json.loads((db.execute("select props from objects where opath=?", (o,)).fetchone() or ["{}"])[0] or "{}")


def short(o): return o.split(".")[-1] if isinstance(o, str) else o


def export(m, pre):
    pkgs = [r[0] for r in db.execute("select distinct package from objects where package like ?", (pre + "%",))]
    objs = {}
    for pk in pkgs:
        for o, c, p in db.execute("select opath, class, props from objects where package=?", (pk,)):
            objs[o] = (c, json.loads(p or "{}"))
    out = {"map": m, "packages": pkgs}
    sl = [(o, d) for o, (c, d) in objs.items() if c == "TnSurvivalSpawnList"]
    cdo = props("TransGame.Default__TnSurvivalSpawnList")
    out["spawn_list"] = [{"object": o, "defaults_from_cdo": {k: v for k, v in cdo.items() if k not in d}, **d} for o, d in sl]
    out["generators"] = [{"object": short(o), **{k: d.get(k) for k in ("LocalizedGeneratorNameKey", "PowerLevels", "DrainRate", "Location",
                                                                       "ActivationVolume", "Tag")}}
                         for o, (c, d) in sorted(objs.items()) if c == "TnSurvivalGenerator" and "Default__" not in o]
    zcdo = props("TransGame.Default__TnSurvivalZoneVolume")
    out["zones"] = [{"object": short(o), "Active": d.get("Active", zcdo.get("Active")),
                     "SelfModifier": {m["SpawnType"]: m["Score"] for m in d.get("SelfModifier", zcdo.get("SelfModifier", []))},
                     "ZoneChanges": [{"zone": short(z["ZoneToChange"]), **{c["SpawnType"]: c["ScoreChange"] for c in z.get("ScoreChanges", [])}}
                                     for z in d.get("ZoneChanges", [])],
                     "SpawnPoints": len(d.get("PossibleSpawnPoints", [])), "Location": d.get("Location")}
                    for o, (c, d) in sorted(objs.items()) if c == "TnSurvivalZoneVolume" and "Default__" not in o]
    # Kismet graph
    succ = collections.defaultdict(list)
    remote = collections.defaultdict(list)
    for o, (c, d) in objs.items():
        for L in d.get("OutputLinks") or []:
            for l in L.get("Links") or []:
                if l.get("LinkedOp"): succ[o].append((L.get("LinkDesc"), l["LinkedOp"], l.get("InputLinkIdx", 0)))
        if c == "SeqEvent_RemoteEvent": remote[d.get("EventName")].append(o)
    for o, (c, d) in objs.items():
        if c == "SeqAct_ActivateRemoteEvent":
            for ev in remote.get(d.get("EventName"), []): succ[o].append(("remote:" + str(d.get("EventName")), ev, 0))

    def ovars(d):
        res = {}
        for v in d.get("VariableLinks") or []:
            vals = []
            for lv in v.get("LinkedVariables") or []:
                vc, vd = objs.get(lv, ("?", {}))
                vals.append(short(vd.get("ObjValue")) if vd.get("ObjValue") else (vd.get("FindVarName") or vd.get("VarName") or short(lv)))
            if vals: res[v.get("LinkDesc")] = vals
        return res

    def walk(start, maxn=400):
        seen, order, stack = set(), [], [(start, None, 0, 0)]
        while stack and len(order) < maxn:
            cur, via, inp, depth = stack.pop()
            key = (cur, inp)
            if key in seen or depth > 25: continue
            seen.add(key)
            c, d = objs.get(cur, ("?", {}))
            ins = [l.get("LinkDesc") for l in d.get("InputLinks") or []]
            order.append({"op": short(cur), "class": c, "via": via, "input": ins[inp] if inp < len(ins) else inp, "depth": depth,
                          "comment": d.get("ObjComment"), "vars": ovars(d),
                          **{k: d[k] for k in ("EventName", "Duration", "PowerToAdd", "ForcedForm", "bOpen") if k in d}})
            for desc, nxt, idx in succ.get(cur, []):
                stack.append((nxt, "%s.%s" % (short(cur), desc), idx, depth + 1))
        return order

    evs = []
    for o, (c, d) in sorted(objs.items()):
        if c in ("TnSeqEvent_SurvivalGenerator", "TnSeqEvent_SurvivalEvents"):
            evs.append({"event": short(o), "class": c, "originator": short(d.get("Originator")), "comment": d.get("ObjComment"),
                        "outputs": [L.get("LinkDesc") for L in d.get("OutputLinks") or []],
                        "props": {k: v for k, v in d.items() if k not in ("OutputLinks", "InputLinks", "VariableLinks", "ParentSequence",
                                                                           "Originator", "ObjComment")},
                        "downstream": walk(o)})
    out["events"] = evs
    return out


if __name__ == "__main__":
    od = sys.argv[1]; os.makedirs(od, exist_ok=True)
    common = {"TnSurvivalGame": props("TransContent.Default__TnSurvivalGame"),
              "TnGameReplicationInfoSurvival": props("TransContent.Default__TnGameReplicationInfoSurvival"),
              "TnRespawnHelperWave": props("TransGame.Default__TnRespawnHelperWave"),
              "TnSurvivalSpawnList": props("TransGame.Default__TnSurvivalSpawnList"),
              "TnSurvivalGenerator": props("TransContent.Default__TnSurvivalGenerator")}
    json.dump(common, open(os.path.join(od, "_class_defaults.json"), "w"), indent=1)
    for m, pre in MAPS.items():
        r = export(m, pre)
        json.dump(r, open(os.path.join(od, m + ".json"), "w"), indent=1)
        print(m, "zones", len(r["zones"]), "generators", len(r["generators"]), "events", len(r["events"]), "spawnlists", len(r["spawn_list"]))
