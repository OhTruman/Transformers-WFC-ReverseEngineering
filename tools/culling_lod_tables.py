"""Read-only: CAMPAIGN_CULLING_LOD_RE §7 tables from authored.db + campaign_streaming_order.json + next_map Kismet.
Per map package: primitive components, CachedCullDistance histogram; CullDistanceVolume tables; skeletal meshes with >1 LOD;
actors hidden at load (bHidden) per chapter; Kismet ToggleHidden(Hide) fired from start events; per streaming state the
visible-level primitive totals.
Usage: python culling_lod_tables.py <out.json>"""
import os, sys, json, sqlite3, collections
sys.dont_write_bytecode = True
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = "file:///F:/Transformers Rebuild/AssetTools/manifests/authored.db?mode=ro"
NEXT = r"F:\Transformers Rebuild\AssetTools\manifests\next_map"
PRIMS = {"StaticMeshComponent", "SkeletalMeshComponent", "ParticleSystemComponent", "DecalComponent", "ModelComponent",
         "SpeedTreeComponent", "InstancedStaticMeshComponent", "FracturedStaticMeshComponent", "TerrainComponent",
         "HmSkeletalMeshComponent", "HmLightMappedSkeletalMeshComponent", "SpriteComponent"}
BUCKETS = [0, 1000, 2000, 4000, 8000, 16000, 32000, 1e12]


def bucket(v):
    for i in range(len(BUCKETS) - 1):
        if BUCKETS[i] < v <= BUCKETS[i + 1]: return "%d-%s" % (BUCKETS[i], "inf" if BUCKETS[i + 1] > 1e11 else int(BUCKETS[i + 1]))
    return "0 (never)"


def main(out):
    so = json.load(open(os.path.join(ROOT, "work", "handoff", "campaign_streaming_order.json")))
    pkgs = set(so)
    for ch, d in so.items():
        for lv in d["states"].values(): pkgs |= {l for l, _ in lv}
    db = sqlite3.connect(DB, uri=True)
    esc = {r[0] for r in db.execute("select distinct package from objects where package like 'MP_ESC_%'")}
    pkgs |= esc
    prim = collections.defaultdict(lambda: {"prims": 0, "culled": 0, "hist": collections.Counter(), "by_class": collections.Counter()})
    hidden = collections.defaultdict(collections.Counter)
    for pkg, cls, props in db.execute("select package, class, props from objects"):
        if pkg not in pkgs or not props: continue
        if cls in PRIMS or cls.endswith("MeshComponent"):
            if "Default__" in props[:0]: pass
            d = json.loads(props); P = prim[pkg]
            P["prims"] += 1; P["by_class"][cls] += 1
            c = d.get("CachedCullDistance", 0) or 0
            if c > 0: P["culled"] += 1
            P["hist"][bucket(c)] += 1
        elif '"bHidden":true' in props and not cls.endswith("Component"):
            hidden[pkg][cls] += 1
    vols = []
    for o, p in db.execute("select opath, props from objects where class='CullDistanceVolume'"):
        d = json.loads(p or "{}")
        vols.append({"volume": o, "CullDistances": d.get("CullDistances"), "bEnabled": d.get("bEnabled", True)})
    skel = []
    for o, p in db.execute("select opath, props from objects where class='SkeletalMesh'"):
        d = json.loads(p or "{}"); li = d.get("LODInfo") or []
        if len(li) > 1: skel.append({"mesh": o, "lods": len(li), "DisplayFactor": [x.get("DisplayFactor") for x in li]})
    # Kismet: ToggleHidden 'Hide' reached within 3 hops of a start event
    khide = {}
    for ch in list(so) + sorted({p.split("_BASE")[0].split("_Base")[0] for p in esc}):
        f = os.path.join(NEXT, ch.replace("_Base_m", "").replace("_BASE_m", "") + "_kismet.json")
        if not os.path.exists(f):
            alt = [x for x in os.listdir(NEXT) if x.lower().startswith(ch.split("_")[0].lower() + "_") and x.endswith("_kismet.json")]
            if not alt: continue
            f = os.path.join(NEXT, alt[0])
        k = json.load(open(f)); ops = {o["object"]: o for arr in k["levels"].values() for o in arr}
        res = collections.Counter()
        for p, o in ops.items():
            if o["class"] not in ("SeqEvent_PreGameplaySetup", "SeqEvent_GameplayStarted", "SeqEvent_LevelLoaded"): continue
            stack = [(p, 0)]; seen = set()
            while stack:
                cur, dep = stack.pop()
                if cur in seen or dep > 3: continue
                seen.add(cur)
                for ls in ops.get(cur, {}).get("outputs", {}).values():
                    for l in ls:
                        n = ops.get(l["op"])
                        if not n: continue
                        if n["class"] == "SeqAct_ToggleHidden" and l.get("input_index", 0) == 0:
                            res[n["object"].split(".")[0]] += sum(len(v) for v in n.get("variables", {}).values())
                        stack.append((l["op"], dep + 1))
        khide[os.path.basename(f)] = dict(res)
    states = {}
    for ch, d in so.items():
        states[ch] = {s: {"visible_levels": sum(1 for _, v in lv if v),
                          "prims": sum(prim[l]["prims"] for l, v in lv if v) + prim[ch]["prims"],
                          "culled": sum(prim[l]["culled"] for l, v in lv if v) + prim[ch]["culled"]}
                      for s, lv in d["states"].items()}
    res = {"per_package": {k: {"prims": v["prims"], "with_cull_distance": v["culled"], "hist": dict(v["hist"]),
                               "by_class": dict(v["by_class"].most_common(6))} for k, v in sorted(prim.items())},
           "cull_distance_volumes": vols, "skeletal_multi_lod": skel,
           "hidden_at_load": {k: dict(v.most_common(8)) for k, v in sorted(hidden.items())},
           "kismet_hide_at_start": khide, "per_state": states}
    json.dump(res, open(out, "w"), indent=1)
    return res


if __name__ == "__main__":
    r = main(sys.argv[1])
    print("packages", len(r["per_package"]), "volumes", len(r["cull_distance_volumes"]), "skel multi-LOD", len(r["skeletal_multi_lod"]))
