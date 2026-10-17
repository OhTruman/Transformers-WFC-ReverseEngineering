"""Read-only census of the Kismet classes used by the campaign's levels (authored.db, packages of the AssetTools campaign
chapter manifests), classified against:
  (a) referenced by the Rebuild runtime source (F:\\Transformers Rebuild\\Rebuild\\src, read-only; token match, instance suffixes
      stripped),
  (b) named in an RE-Workspace handoff doc but not in the runtime,
  (c) neither.
Each class also gets its implementation kind from the decompiled script (work/script/decomp*): 'script' (has an Activated /
Update / custom script body), 'native' (only native stubs or no script functions: the handler lives in C++), 'data'
(SequenceVariable / Sequence containers / InterpData), 'event' (SequenceEvent: fired by others).
Usage: python campaign_kismet_classes.py <out.json>"""
import os, re, sys, json, sqlite3, collections, glob
sys.dont_write_bytecode = True
RW = r"F:\Transformers Rebuild\RE-Workspace"
CAMP = r"F:\Transformers Rebuild\AssetTools\manifests\campaign"
SRC = r"F:\Transformers Rebuild\Rebuild\src"
db = sqlite3.connect(r"F:\Transformers Rebuild\AssetTools\manifests\authored.db")

# chapter -> packages (levels + companion packages from the AssetTools chapter manifests)
chap_pk = {}
for f in sorted(glob.glob(os.path.join(CAMP, "*_assets.json"))):
    d = json.load(open(f))
    ch = d.get("chapter") or os.path.basename(f).split("_")[0]
    pk = set((d.get("levels") or {}).get("per_level", {}))   # level packages; companions (_LM / _LOC) carry no Kismet
    chap_pk[ch] = pk

KISMET = re.compile(r"^(Seq|TnSeq|HmSeq|SeqAct|Sequence|InterpData)|Seq(Act|Event|Cond|Var)_")
census = collections.defaultdict(lambda: {"count": 0, "chapters": collections.Counter()})
seqs = 0
for ch, pks in chap_pk.items():
    for pk in pks:
        for (cl,) in db.execute("select class from objects where package=?", (pk,)):
            if not KISMET.search(cl): continue
            census[cl]["count"] += 1; census[cl]["chapters"][ch] += 1
            if cl == "Sequence": seqs += 1

# runtime references
tok = re.compile(r"\b(?:Tn|Hm)?Seq(?:Act|Event|Cond|Var)_[A-Za-z0-9_]+|\bTnSeq[A-Za-z]+_[A-Za-z0-9_]+|\bSequence[A-Za-z]*\b")
rt = collections.defaultdict(set)
for root, _, files in os.walk(SRC):
    for fn in files:
        if not fn.endswith((".cpp", ".h", ".inc", ".hpp")): continue
        p = os.path.join(root, fn)
        for t in tok.findall(open(p, encoding="utf-8", errors="ignore").read()):
            rt[re.sub(r"_\d+$", "", t)].add(os.path.relpath(p, SRC))

# handoff docs
docs = {}
for f in glob.glob(os.path.join(RW, "work", "handoff", "*.md")):
    docs[os.path.basename(f)] = open(f, encoding="utf-8", errors="ignore").read()

# decompiled script per class
dec = {}
for d in glob.glob(os.path.join(RW, "work", "script", "decomp*")):
    for f in glob.glob(os.path.join(d, "*.txt")):
        b = os.path.basename(f)[:-4]
        cls = b.split(".", 1)[1] if "." in b else b
        if not re.match(r"^[A-Za-z0-9_]+$", cls): continue
        dec.setdefault(cls, []).append(f)


def kind(cl):
    if cl.startswith(("SeqVar_", "TnSeqVar_", "HmSeqVar_")) or cl in ("Sequence", "SequenceFrame", "SequenceFrameWrapped",
                                                                         "InterpData", "PrefabSequence") or cl.startswith("Interp"):
        return "data"
    if "SeqEvent_" in cl or cl.startswith(("TnSeqEvent", "HmSeqEvent")): return "event"
    fs = dec.get(cl)
    if not fs: return "native"
    body = "".join(open(f, encoding="utf-8", errors="ignore").read() for f in fs)
    fns = re.findall(r"^function \S+\.(\w+)\s+\(script (\d+) bytes\)", body, re.M)
    real = [n for n, sz in fns if int(sz) > 12 and n not in ("GetObjClassVersion", "CheckForErrors", "GetObjName")]
    return "script" if any(n in ("Activated", "Update", "Deactivated", "OnReceivedImpulse") for n in real) or len(real) >= 2 else "native"


rows = []
for cl, v in census.items():
    in_rt = cl in rt
    in_docs = sorted(n for n, t in docs.items() if re.search(r"\b" + re.escape(cl) + r"\b", t))
    status = "a" if in_rt else ("b" if in_docs else "c")
    rows.append({"class": cl, "count": v["count"], "chapters": dict(sorted(v["chapters"].items())), "status": status,
                 "kind": kind(cl), "runtime_files": sorted(rt.get(cl, []))[:6], "handoff_docs": in_docs[:6]})
rows.sort(key=lambda r: (r["status"], -r["count"]))
summ = collections.Counter((r["status"], r["kind"]) for r in rows)
out = {"chapters": {k: sorted(v) for k, v in chap_pk.items()}, "sequence_objects": seqs, "classes": len(rows),
       "instances": sum(r["count"] for r in rows),
       "summary": {"%s/%s" % k: v for k, v in sorted(summ.items())},
       "instances_by_status": {s: sum(r["count"] for r in rows if r["status"] == s) for s in "abc"}, "rows": rows}
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(out["classes"], "classes,", out["instances"], "instances,", seqs, "Sequence objects"); print(out["summary"]); print(out["instances_by_status"])
