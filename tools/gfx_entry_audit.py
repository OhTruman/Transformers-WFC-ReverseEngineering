"""Per-movie GFx entry-point audit (read-only): runs as2dis.py on each Scaleform movie, collects every function
(`_global.X = function`, `name = function`, `function name()`), and for each records PlaySound cues, interp animations
(time / easing / props), timeline jumps (gotoAndPlay / gotoAndStop labels), attachMovie symbols, setTimeout/interval
delays, ExternalInterface calls, and the helper functions it calls (one level, by bare name, merged). Each _global entry
point is then grepped (read-only) in Rebuild/src: C = named in src (invoked), - = not.
Usage: python gfx_entry_audit.py <out_prefix> <movie.gfx> [...]   -> <out_prefix>.json / .md"""
import json, os, re, subprocess, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
REBUILD_SRC = r"F:\Transformers Rebuild\Rebuild\src"

def disasm(gfx):
    return subprocess.run([PY, os.path.join(HERE, "as2dis.py"), gfx], capture_output=True, text=True, errors="replace").stdout.splitlines()

ASSIGN = re.compile(r"^\s*[0-9a-f]{4}: ([A-Za-z_$][\w.$]*) = function\(")
NAMED = re.compile(r"^(\s*)[0-9a-f]{4}: function ([A-Za-z_$][\w$]*)\(")
ANON = re.compile(r"^(\s*)[0-9a-f]{4}: <anon> function \(")
SOUND = re.compile(r"PlaySound\('([^']+)'")
INTERP = re.compile(r"([\w.$\[\]']+)\.interp\(([\d.]+), '(\w+)', \d+, \{([^}]*)\}")
GOTO = re.compile(r"(gotoAnd(?:Play|Stop))\('?([^')]+)'?\)")
ATTACH = re.compile(r"attachMovie\('([^']+)'")
TIMER = re.compile(r"(setTimeout|setInterval)\([^,]+,\s*([\d.]+)")
EXT = re.compile(r"ExternalInterface\.call\('([^']+)'")
CALL = re.compile(r"(?<![\w.])(?:[\w$]+\.)*([A-Za-z_$][\w$]*)\(")

def parse(lines):
    funcs = {}; sprite = None; i = 0
    while i < len(lines):
        L = lines[i]
        if L.startswith("==== DoAction"):
            m = re.search(r"sprite=(\S+)", L); sprite = m.group(1) if m else None
        m = ANON.match(L) or NAMED.match(L)
        if m:
            ind = m.group(1); body = []; j = i + 1
            while j < len(lines) and not (lines[j].strip() == "}" and (len(lines[j]) - len(lines[j].lstrip())) <= len(ind) + 4):
                body.append(lines[j]); j += 1
            name = m.group(2) if m.re is NAMED else None
            k = j + 1
            if name is None and k < len(lines):
                a = ASSIGN.match(lines[k])
                if a: name = a.group(1)
            if name and name not in ("r0",):
                txt = "\n".join(body)
                funcs.setdefault(name, []).append({"sprite": sprite, "text": txt})
            i = j
        i += 1
    return funcs

def summarize(txt):
    return {"sounds": sorted(set(SOUND.findall(txt))),
            "interps": ["%s %ss %s {%s}" % (t, d, e, p.strip()[:60]) for t, d, e, p in INTERP.findall(txt)],
            "gotos": sorted(set("%s(%s)" % g for g in GOTO.findall(txt))),
            "attach": sorted(set(ATTACH.findall(txt))), "timers": ["%s %s ms" % t for t in TIMER.findall(txt)],
            "external": sorted(set(EXT.findall(txt))), "calls": sorted(set(CALL.findall(txt)))}

src_text = []
for dp, dn, fn in os.walk(REBUILD_SRC):
    for f in fn:
        if f == "CharacterAudio.inc": continue
        try: src_text.append(open(os.path.join(dp, f), "rb").read().decode("latin1"))
        except OSError: pass
def in_src(name):
    pats = ('"%s"' % name, "_global.%s" % name, "'%s'" % name)
    return "C" if any(p_ in t for t in src_text for p_ in pats) else "-"

sys.path.insert(0, HERE)
import gfxpool
def exports(gfx):
    b = gfxpool.load(gfx); off = 8 + gfxpool.rect_len(b, 8) + 4; ex = {}
    for kind, sid, pl in gfxpool.walk(b, off, len(b), 0):
        if kind == "Export":
            for cid, name in pl[0]: ex[name] = str(cid)
    return ex
def sprite_text(lines):
    st = collections.defaultdict(list); cur = None
    for L in lines:
        if L.startswith("==== DoAction"):
            m = re.search(r"sprite=(\S+)", L); cur = m.group(1) if m else None; continue
        st[cur].append(L)
    return {k: "\n".join(v) for k, v in st.items()}

INFRA = {"addInterp", "createInterpController", "findInterpValue", "removeInterpController", "updateInterpObjects", "GetPointMultiplierColor"}
out_prefix = sys.argv[1]; result = {}
for gfx in sys.argv[2:]:
    lines = disasm(gfx)
    funcs = parse(lines); ex = exports(gfx); stext = sprite_text(lines)
    entries = {}
    for name, defs in funcs.items():
        if not name.startswith("_global.") or name.split(".")[1].startswith("Hm") or name.split(".")[1] in INFRA: continue
        s = summarize("\n".join(d["text"] for d in defs))
        # one level of helper calls: merge their sounds / interps / gotos
        # helpers only from the same sprite(s) as the entry's own definition
        my_sprites = {d["sprite"] for d in defs}
        helpers = []
        for c in s["calls"]:
            if c in ("interp", "setColor") or "_global." + c == name: continue
            hdefs = [d for n_, ds in funcs.items() if n_.split(".")[-1] == c for d in ds if d["sprite"] in my_sprites]
            if not hdefs: continue
            helpers.append(c); hs = summarize("\n".join(d["text"] for d in hdefs))
            for k in ("sounds", "interps", "gotos", "attach", "timers"):
                s[k] = sorted(set(s[k]) | set(("%s: " % c + x) if k == "interps" else x for x in hs[k]))
        # attached / exported symbols: summarize that symbol's own sprite code (its onLoad / timeline script)
        sym = {}
        for a in s["attach"]:
            cid = ex.get(a)
            if cid and cid in stext:
                ss = summarize(stext[cid]); sym[a] = {k: ss[k] for k in ("sounds", "interps", "gotos", "timers")}
        s["symbols"] = sym
        s["helpers"] = helpers; s["sprites"] = sorted({str(d["sprite"]) for d in defs})
        s["ours"] = in_src(name.split(".")[1]); del s["calls"]
        entries[name.split(".")[1]] = s
    result[os.path.basename(gfx)] = entries

json.dump(result, open(out_prefix + ".json", "w"), indent=1)
L = []
for movie, entries in result.items():
    L += ["", "### %s (%d entry points)" % (movie, len(entries)), "",
          "| Entry point | Ours | Sounds | Animation (interp: target time easing {props}) / timeline | Spawned symbols / timers / engine calls |",
          "|---|---|---|---|---|"]
    for n, s in sorted(entries.items()):
        anim = "; ".join(s["interps"][:6]) + (" …(+%d)" % (len(s["interps"]) - 6) if len(s["interps"]) > 6 else "")
        if s["gotos"]: anim += ("; " if anim else "") + ", ".join(s["gotos"][:4])
        symtxt = []
        for a, ss in s.get("symbols", {}).items():
            bits = (["snd " + ",".join(ss["sounds"])] if ss["sounds"] else []) + (ss["interps"][:3]) + (ss["gotos"][:2]) + ss["timers"][:2]
            symtxt.append("%s{%s}" % (a, "; ".join(bits)) if bits else a)
        other = ", ".join(symtxt + [a for a in s["attach"] if a not in s.get("symbols", {})] + s["timers"] + ["→" + e for e in s["external"]])
        snd = sorted(set(s["sounds"]) | {x for ss in s.get("symbols", {}).values() for x in ss["sounds"]})
        L.append("| %s | %s | %s | %s | %s |" % (n, s["ours"], ", ".join(snd) or "-", anim.replace("|", "/") or "-", other.replace("|", "/") or "-"))
open(out_prefix + ".md", "w", encoding="utf-8").write("\n".join(L) + "\n")
print({m: len(e) for m, e in result.items()})
