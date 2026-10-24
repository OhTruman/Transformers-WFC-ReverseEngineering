"""Read-only: Escalation spawn-zone order per map (the format of work/handoff/escalation_zone_order.json).
zone_actor_order = the TnSurvivalZoneVolumes in the PersistentLevel Actors array order (AllActors order);
initial_sorted   = per spawn type, the active zones sorted by SelfModifier score, descending, with the binary's
                   unstable MSVC qsort (tools/msvc_qsort.py) starting from actor order.
Zone flags / scores come from notes/data/escalation/<map>.json (tools/escalation_export.py).
Usage: python esc_zone_order.py <out.json> <MapName>=<BASE package .xxx path> ..."""
import os, sys, json, struct
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"F:\Transformers Rebuild\AssetTools\scripts\wfc")
import ue3pkg
from msvc_qsort import qsort

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TYPES = ["Standard", "ShortRange", "LongRange", "Air", "Boss"]


def actor_order(pkg_path):
    p = ue3pkg.Package(pkg_path)
    lvl = next(i for i, e in enumerate(p.exports, 1) if p.full_path(i) == "TheWorld.PersistentLevel")
    le = p.exports[lvl - 1]
    blob = p.data[le["serial_offset"]:le["serial_offset"] + le["serial_size"]]
    zones = []
    for i, e in enumerate(p.exports, 1):
        if p.class_name(e) == "TnSurvivalZoneVolume" and p.exports[e["outer"] - 1]["name"] == "PersistentLevel":
            k = blob.find(struct.pack(">i", i))
            zones.append((k, e["name"].split("_")[-1]))
    assert all(k >= 0 for k, _ in zones), "zone missing from the Actors array"
    return [z for _, z in sorted(zones)]


def sorted_initial(m, order):
    Z = {z["object"].split("_")[-1]: z for z in json.load(open(os.path.join(ROOT, "notes", "data", "escalation", "MP_ESC_%s.json" % m)))["zones"]}
    act = [z for z in order if Z[z]["Active"]]
    res = {}
    for t in TYPES:
        sc = lambda i: Z[act[i]]["SelfModifier"].get("EST_" + t, 0.0)
        comp = lambda a, b: 1 if sc(a) < sc(b) else (-1 if sc(a) > sc(b) else 0)
        res[t] = [act[i] for i in qsort(list(range(len(act))), comp)]
    return res


if __name__ == "__main__":
    out = {"zone_actor_order": {}, "initial_sorted": {}}
    for a in sys.argv[2:]:
        m, path = a.split("=", 1)
        out["zone_actor_order"][m] = actor_order(path)
        out["initial_sorted"][m] = sorted_initial(m, out["zone_actor_order"][m])
        print(m, len(out["zone_actor_order"][m]), "zones")
    json.dump(out, open(sys.argv[1], "w"), indent=1)
