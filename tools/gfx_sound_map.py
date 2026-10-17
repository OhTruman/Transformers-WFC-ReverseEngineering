"""Read-only: per Scaleform movie, every Sound.PlaySound cue with the function (and sprite) it sits in, plus the
open / close / show / hide / transition interps. Each cue is grepped in Rebuild src + data (C = src code, D = data json,
- = neither). Usage: python gfx_sound_map.py <out_prefix> <movie.gfx> [...]  -> <out_prefix>.json / .md"""
import os, re, sys, json, subprocess, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REBUILD = r"F:\Transformers Rebuild\Rebuild"
ANON = re.compile(r"^(\s*)[0-9a-f]{4}: <anon> function \(")
NAMED = re.compile(r"^(\s*)[0-9a-f]{4}: function ([A-Za-z_$][\w$]*)\(")
ASSIGN = re.compile(r"^\s*[0-9a-f]{4}: ([A-Za-z_$][\w.$]*) = function\(")
SOUND = re.compile(r"PlaySound\('([^']+)'")
INTERP = re.compile(r"([\w.$\[\]']+)\.interp\(([\d.]+), '(\w+)', \d+, \{([^}]*)\}")
TRANS = re.compile(r"(open|close|show|hide|transition|onload|focus|select|accept|back|tab|navigate|enter|exit)", re.I)

def disasm(g): return subprocess.run([sys.executable, os.path.join(HERE, "as2dis.py"), g], capture_output=True, text=True, errors="replace").stdout.splitlines()

def functions(lines):
    out = []; sprite = None; i = 0
    top = collections.defaultdict(list)
    while i < len(lines):
        L = lines[i]
        if L.startswith("==== DoAction"):
            m = re.search(r"sprite=(\S+)", L); sprite = m.group(1) if m else None
        m = ANON.match(L) or NAMED.match(L)
        if m:
            ind = m.group(1); j = i + 1; body = []
            while j < len(lines) and not (lines[j].strip() == "}" and len(lines[j]) - len(lines[j].lstrip()) <= len(ind) + 4):
                body.append(lines[j]); j += 1
            name = m.group(2) if m.re is NAMED else None
            if name is None and j + 1 < len(lines):
                a = ASSIGN.match(lines[j + 1]); name = a.group(1) if a else "<anon>"
            out.append((sprite, name, "\n".join(body))); i = j
        else:
            top[sprite].append(L)
        i += 1
    for sp, ls in top.items(): out.append((sp, "<timeline>", "\n".join(ls)))
    return out

corpus = []
for base in ("src", "data"):
    for dp, dn, fn in os.walk(os.path.join(REBUILD, base)):
        for f in fn:
            if f == "CharacterAudio.inc": continue
            try: corpus.append((base, open(os.path.join(dp, f), "rb").read().decode("latin1")))
            except OSError: pass
def g(name):
    s = ("C" if any(b == "src" and name in t for b, t in corpus) else "") + ("D" if any(b == "data" and name in t for b, t in corpus) else "")
    return s or "-"

res = {}
for gfx in sys.argv[2:]:
    fs = functions(disasm(gfx))
    snd = collections.defaultdict(set); trans = []
    for sp, name, body in fs:
        for c in SOUND.findall(body): snd[c].add("%s@%s" % (name.split(".")[-1], sp))
        if TRANS.search(name or ""):
            for t, d, e, p in INTERP.findall(body):
                trans.append("%s: %s %ss %s {%s}" % (name.split(".")[-1], t, d, e, p.strip()[:50]))
    res[os.path.basename(gfx)] = {"sounds": {k: sorted(v) for k, v in sorted(snd.items())}, "sound_grep": {k: g(k) for k in snd},
                                  "transitions": sorted(set(trans))[:40]}
json.dump(res, open(sys.argv[1] + ".json", "w"), indent=1)
L = []
allc = collections.defaultdict(set)
for m, r in res.items():
    for c, ctx in r["sounds"].items(): allc[c].add(m.replace("_GFX.gfx", ""))
L += ["| UI cue | Ours | Movies | Where (function@sprite, first 4) |", "|---|---|---|---|"]
for c in sorted(allc):
    where = sorted({x for m, r in res.items() for x in r["sounds"].get(c, [])})
    L.append("| %s | %s | %s | %s |" % (c, g(c), ", ".join(sorted(allc[c])), "; ".join(where[:4])))
L += ["", "| Movie | Transition interps (open / close / show / hide / focus …) |", "|---|---|"]
for m, r in res.items():
    L.append("| %s | %s |" % (m.replace(".gfx", ""), ("; ".join(r["transitions"][:8]) or "-").replace("|", "/")))
open(sys.argv[1] + ".md", "w", encoding="utf-8").write("\n".join(L) + "\n")
print(len(allc), "cues across", len(res), "movies")
