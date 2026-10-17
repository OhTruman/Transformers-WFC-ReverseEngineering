"""Read-only: per MP map, every reverb / mixer Kismet action with its preset name (read from the cooked SoundMixerPresetName
export, because authored.db leaves most of those objects empty), the chain of Kismet ops that reaches it, back to the
originating events (through SeqAct_Delay / AmbientAudioZone / ActivateRemoteEvent -> SeqEvent_RemoteEvent by EventName), the
trigger volumes behind Touch events, and the preset definitions (SoundConfig.SoundMixerProperties MixerPresets + per-category DSP).
Usage: python mp_reverb_export.py <outdir>   -> <outdir>/<MAP>.json"""
import os, sys, json, struct, sqlite3, collections
sys.dont_write_bytecode = True
sys.path.insert(0, r"F:\Transformers Rebuild\AssetTools\scripts\wfc")
import ue3pkg

DUMP = r"F:\Transformers Rebuild\Game Dump\TransGame\CookedXenon"
MAPS = ["MP_ESC_BrokenHope", "MP_ESC_Remnant", "MP_IAC_Berth", "MP_IAC_Rust", "MP_IAC_Seed", "MP_IAC_Streets", "MP_KON_Molten",
        "MP_ORB_Debris", "MP_UND_Complex", "MP_UND_Gorge"]
PREFIX = {"MP_ORB_Debris": "MP_ORB_"}                     # Debris packages are MP_ORB_Art_m / MP_ORB_Audio_m / ...
ACTIONS = ("SeqAct_Reverb", "SeqAct_Mixer")
db = sqlite3.connect(r"F:\Transformers Rebuild\AssetTools\manifests\authored.db")

mixer = json.loads(db.execute("select props from objects where opath='SoundConfig.SoundMixerProperties'").fetchone()[0])
PRESETS = {m["Name"]: m for m in mixer["MixerPresets"]}
DSP = collections.defaultdict(dict)                      # preset -> {category: dsp}
DEFAULT_DSP = {}
for c in mixer["SoundCategories"]:
    for dp in c.get("DSPPresets") or []:
        if dp["Name"] == "Default": DEFAULT_DSP[c["Name"]] = dp
        else: DSP[dp["Name"]][c["Name"]] = dp


def preset_names(pkg):
    """{object path: PresetName} for every SoundMixerPresetName export, parsed from the tagged property in the package."""
    p = ue3pkg.Package(os.path.join(DUMP, pkg + ".xxx")); d = p.data; nm = [str(n) for n in p.names]; out = {}
    for i, e in enumerate(p.exports, 1):
        if p.class_name(e) != "SoundMixerPresetName": continue
        b = d[e["serial_offset"]:e["serial_offset"] + e["serial_size"]]
        for k in range(0, len(b) - 31, 4):                # tag: FName PresetName, FName NameProperty, i32 size, i32 index, FName value
            x, y = struct.unpack_from(">II", b, k)
            if y == 0 and x < len(nm) and nm[x] == "PresetName":
                v = struct.unpack_from(">I", b, k + 24)[0]
                out[p.object_path(i)] = nm[v] if v < len(nm) else None; break
        else:
            out[p.object_path(i)] = None
    return out


def trim_dsp(dp):
    return {k: dp[k] for k in ("Volume", "LowPass", "Echo", "Reverb") if k in dp}


def export(m):
    pre = PREFIX.get(m, m + "_")
    pkgs = [r[0] for r in db.execute("select distinct package from objects where package like ?", (pre + "%",))]
    objs = {}
    for pk in pkgs:
        for o, c, p in db.execute("select opath, class, props from objects where package=?", (pk,)):
            objs[o] = (c, json.loads(p or "{}"))
    names = {}
    for pk in pkgs:
        if any(c in ACTIONS for c, _ in objs.values()):
            try: names.update(preset_names(pk))
            except Exception as ex: print("  pkg", pk, ex)
    # graph
    preds = collections.defaultdict(list)                # op -> [(src op, output link desc)]
    remote_ev = collections.defaultdict(list)            # EventName -> [SeqEvent_RemoteEvent]
    for o, (c, d) in objs.items():
        for L in d.get("OutputLinks") or []:
            for l in L.get("Links") or []:
                if l.get("LinkedOp"): preds[l["LinkedOp"]].append((o, L.get("LinkDesc"), l.get("InputLinkIdx", 0)))
        if c == "SeqEvent_RemoteEvent": remote_ev[d.get("EventName")].append(o)
    for o, (c, d) in objs.items():                       # ActivateRemoteEvent -> RemoteEvent by name
        if c == "SeqAct_ActivateRemoteEvent":
            for ev in remote_ev.get(d.get("EventName"), []):
                preds[ev].append((o, "remote:" + str(d.get("EventName")), 0))

    def sources(op):
        out, seen, stack = [], set(), [(op, [])]
        while stack:
            cur, path = stack.pop()
            if cur in seen or len(path) > 12: continue
            seen.add(cur)
            c, d = objs.get(cur, ("?", {}))
            if c.startswith("SeqEvent") and c != "SeqEvent_RemoteEvent":
                ev = {"event": cur.split(".")[-1], "class": c, "comment": d.get("ObjComment"), "path": path}
                orig = d.get("Originator")
                if orig and orig in objs:
                    oc, od = objs[orig]
                    ev["originator"] = {"actor": orig.split(".")[-1], "class": oc, "location": od.get("Location"),
                                        "draw_scale": od.get("DrawScale"), "draw_scale3d": od.get("DrawScale3D")}
                ev["flags"] = {k: d.get(k) for k in ("bLocalPlayerOnly", "bClientSideOnly", "bForceOverlapping", "MaxTriggerCount",
                                                     "ReTriggerDelay", "ClassProximityTypes", "IgnoredClassProximityTypes") if k in d}
                out.append(ev); continue
            for src, desc, idx in preds.get(cur, []):
                sc = objs.get(src, ("?", {}))[0]
                stack.append((src, [{"op": src.split(".")[-1], "class": sc, "output": desc,
                                     "comment": objs.get(src, ("?", {}))[1].get("ObjComment")}] + path))
        return out

    acts = []
    for o, (c, d) in sorted(objs.items()):
        if c not in ACTIONS: continue
        ref = d.get("ReverbMixerPreset") or d.get("Preset")
        name = names.get(ref)
        ins = collections.Counter(idx for _, _, idx in preds.get(o, []))
        acts.append({"action": o.split(".")[-1], "class": c, "sequence": o.rsplit(".", 1)[0].split("PersistentLevel.")[-1],
                     "comment": d.get("ObjComment"), "preset": name,
                     "inputs_used": {("Enable" if i == 0 else "Disable") if c == "SeqAct_Mixer" else "Activate": n for i, n in ins.items()},
                     "sources": sources(o)})
    used = sorted({a["preset"] for a in acts if a["preset"]})
    pres = {}
    for n in used:
        mp = PRESETS.get(n)
        pres[n] = {"mixer_preset": mp, "is_reverb": n.startswith(("REVERB", "REVERB_TANS")),
                   "dsp_by_category": {cat: trim_dsp(dp) for cat, dp in DSP.get(n, {}).items()}}
    return {"map": m, "packages": pkgs, "actions": acts, "presets": pres}


if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    summ = {}
    for m in MAPS:
        r = export(m)
        json.dump(r, open(os.path.join(out, m + ".json"), "w"), indent=1)
        rv = [a for a in r["actions"] if a["class"] == "SeqAct_Reverb"]
        summ[m] = {"reverb_actions": len(rv), "named": sum(1 for a in rv if a["preset"]), "presets": len(r["presets"]),
                   "unreached": sum(1 for a in r["actions"] if not a["sources"])}
        print(m, summ[m], flush=True)
    json.dump({"default_dsp": {k: trim_dsp(v) for k, v in DEFAULT_DSP.items()}, "summary": summ},
              open(os.path.join(out, "_default_and_summary.json"), "w"), indent=1)
