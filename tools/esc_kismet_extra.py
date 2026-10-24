"""Read-only: the Escalation map Kismet that is NOT reached from TnSeqEvent_SurvivalGenerator / _SurvivalEvents (those are in
notes/data/escalation/<map>.json "events"): doors, hazards, sentries, zone managers, vignettes, triggered by touch / remote events /
det packs / gameplay start. Skips console (debug) events, the crate prefabs (HmDestructibleStateNotification ->
SpawnPickupRewards), pickup-status vending sequences and the audio-only area sequences.
Usage: python esc_kismet_extra.py <outdir> <authored.db> <Map>=<package prefix> ..."""
import os, sys, json, sqlite3, collections
sys.dont_write_bytecode = True

SKIP_EV = {"SeqEvent_Console", "TnSeqEvent_SurvivalGenerator", "TnSeqEvent_SurvivalEvents", "SeqEvent_HmDestructibleStateNotification",
           "SeqEvent_PickupStatusChange", "SeqEvent_SequenceActivated", "SeqEvent_LevelLoaded"}
AUDIO = {"SeqAct_PlaySound", "SeqAct_PlayPlayerPositionalSound", "SeqAct_AmbientAudioZone", "SeqAct_Reverb", "SeqAct_PlayMusic",
         "SeqAct_StopMusic", "SeqAct_PlayFlybySound", "SeqAct_SetSoundMode", "SeqAct_Delay", "SeqAct_Gate", "SeqAct_Switch",
         "SeqEvent_UnTouch", "SeqEvent_Touch", "SeqEvent_SequenceActivated", "Sequence"}
short = lambda o: o.split(".")[-1] if isinstance(o, str) else o


def seqpath(o):
    """The op's sequence below Main_Sequence ("" for the root): disambiguates instanced prefab sequences."""
    p = o.split(".")
    return ".".join(p[p.index("Main_Sequence") + 1:-1]) if "Main_Sequence" in p else ""


def export(db, pre):
    objs = {}
    for o, c, p in db.execute("select opath, class, props from objects where package like ?", (pre + "%",)):
        objs[o] = (c, json.loads(p or "{}"))
    succ, remote = collections.defaultdict(list), collections.defaultdict(list)
    for o, (c, d) in objs.items():
        for L in d.get("OutputLinks") or []:
            for l in L.get("Links") or []:
                if l.get("LinkedOp"): succ[o].append((L.get("LinkDesc"), l["LinkedOp"], l.get("InputLinkIdx", 0)))
        if c == "SeqEvent_RemoteEvent": remote[d.get("EventName")].append(o)
    for o, (c, d) in objs.items():
        if c == "SeqAct_ActivateRemoteEvent":
            scope = o.rsplit(".", 1)[0] + "." if d.get("bLocalEvent") else ""  # bLocalEvent: only events in its own sequence
            for ev in remote.get(d.get("EventName"), []):
                if ev.startswith(scope): succ[o].append(("remote:" + str(d.get("EventName")), ev, 0))

    def ovars(d):
        res = {}
        for v in d.get("VariableLinks") or []:
            vals = []
            for lv in v.get("LinkedVariables") or []:
                vc, vd = objs.get(lv, ("?", {}))
                vals.append(short(vd.get("ObjValue")) if vd.get("ObjValue") else
                            (vd.get("FindVarName") or vd.get("VarName") or vd.get("IntValue", vd.get("FloatValue", short(lv)))))
            if vals: res[v.get("LinkDesc")] = vals
        return res

    def walk(start, maxn=300):
        seen, order, stack = set(), [], [(start, None, 0, 0)]
        while stack and len(order) < maxn:
            cur, via, inp, depth = stack.pop()
            if (cur, inp) in seen or depth > 25: continue
            seen.add((cur, inp))
            c, d = objs.get(cur, ("?", {}))
            ins = [l.get("LinkDesc") for l in d.get("InputLinks") or []]
            order.append({"op": short(cur), "seq": seqpath(cur), "class": c, "via": via, "input": ins[inp] if inp < len(ins) else inp, "depth": depth,
                          "comment": d.get("ObjComment"), "vars": ovars(d),
                          **({"Duration": 1.0} if c == "SeqAct_Delay" and "Duration" not in d else {}),  # CDO default
                          **{k: d[k] for k in ("EventName", "Duration", "DamageAmount", "HealAmount", "PowerToAdd", "ValueA", "ValueB",
                                               "bOpen", "MaxTriggerCount", "ReTriggerDelay", "bPlayerOnly", "bEnabled") if k in d}})
            for desc, nxt, idx in succ.get(cur, []):
                stack.append((nxt, "%s.%s" % (short(cur), desc), idx, depth + 1))
        return order

    out = []
    for o, (c, d) in sorted(objs.items()):
        if "Main_Sequence" not in o or not (c.startswith("SeqEvent") or c.startswith("TnSeqEvent")) or c in SKIP_EV: continue
        if "Default__" in o or "_prefab_Seq" in o: continue
        down = walk(o)
        if all(s["class"] in AUDIO for s in down): continue
        seq = ".".join(o.split(".")[o.split(".").index("Main_Sequence") + 1:-1]) or "(root)"
        out.append({"sequence": seq, "event": short(o), "class": c, "originator": short(d.get("Originator")), "comment": d.get("ObjComment"),
                    "props": {k: d[k] for k in ("MaxTriggerCount", "ReTriggerDelay", "bPlayerOnly", "bEnabled", "EventName", "ClassProximityTypes")
                              if k in d},
                    "vars": ovars(d), "downstream": down})
    return out


if __name__ == "__main__":
    od, dbp = sys.argv[1], sys.argv[2]
    db = sqlite3.connect("file:///" + dbp.replace("\\", "/") + "?mode=ro", uri=True)
    for a in sys.argv[3:]:
        m, pre = a.split("=", 1)
        r = export(db, pre)
        json.dump({"map": m, "mechanisms": r}, open(os.path.join(od, m + "_kismet_extra.json"), "w"), indent=1)
        print(m, len(r), "entry events:", sorted(collections.Counter(x["sequence"].split(".")[0] for x in r).items()))
