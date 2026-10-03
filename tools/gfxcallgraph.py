"""Read-only: build a Scaleform<->UnrealScript callback table for WFC UI movies.
AS->engine: ExternalInterface names 'Iface.Method' declared in the HmInterface* AS2 packages, matched
            against the constant pools of each movie's own (non-__Packages) DoAction/DoInitAction code
            (pool membership of both the interface name and the method name = referenced).
engine->AS: '_global.*' / 'root.*' string literals in decompiled UnrealScript (work/script/decomp) and
            authored defaults (authored.db), attributed to the class that holds them.
Also records fscommand strings ('FSCommand:' / GFxEvent_FsCommand in maps are separate).
usage: gfxcallgraph.py out.json
"""
import glob, os, sys, json, re, sqlite3
sys.path.insert(0, os.path.dirname(__file__)); import gfxpool
GFX = r"F:\Transformers Rebuild\ExtractedAssets\content"
DECOMP = os.path.join(os.path.dirname(__file__), '..', 'work', 'script', 'decomp')
DB = r"F:\Transformers Rebuild\AssetTools\manifests\authored.db"

def movie_pools(f):
    b = gfxpool.load(f); off = 8 + gfxpool.rect_len(b, 8) + 4
    lib, own, exports = [], [], {}
    for kind, sid, pl in gfxpool.walk(b, off, len(b), 0):
        if kind == 'Export':
            for cid, name in pl[0]: exports[cid] = name
            continue
        for p in pl:
            (lib if kind == 'DoInitAction' and str(exports.get(sid, '')).startswith('__Packages.Hm') else own).append((kind, sid, p))
    return lib, own, exports

def main(out):
    res = {'movies': {}, 'interfaces': {}, 'engine_to_as': {}}
    parsed = {}
    for f in sorted(glob.glob(os.path.join(GFX, 'UI_GFx*', '*.gfx'))):
        key = os.path.basename(os.path.dirname(f)) + '.' + os.path.basename(f)[:-4]
        try: parsed[key] = movie_pools(f)
        except Exception as e: res['movies'][key] = {'error': str(e)}; continue
        for _, _, p in parsed[key][0]:
            for s in p:
                if re.fullmatch(r'[A-Za-z]+\.[A-Za-z_]+', s):
                    i, m = s.split('.'); res['interfaces'].setdefault(i, set()).add(m)
    for key, (lib, own, exports) in parsed.items():
        calls, strings = set(), set()
        for kind, sid, p in own:
            ps = set(p)
            for i, ms in res['interfaces'].items():
                if i in ps:
                    for m in ms & ps: calls.add(i + '.' + m)
            for s in p:
                if s.startswith('$UIText.') or s.startswith('<'): strings.add(s)
        res['movies'][key] = {'as_to_engine': sorted(calls), 'localized_and_datastore_strings': sorted(strings),
                              'exports': sorted(v for v in exports.values() if not v.startswith('__Packages'))}
    res['interfaces'] = {k: sorted(v) for k, v in res['interfaces'].items()}
    for f in glob.glob(os.path.join(DECOMP, '*.txt')):
        cls = os.path.basename(f)[:-4]
        for line in open(f, encoding='utf-8', errors='replace'):
            for s in re.findall(r'"(_global\.[A-Za-z0-9_\.]+|root\.[A-Za-z0-9_\.]+)"', line):
                res['engine_to_as'].setdefault(s, set()).add(cls)
    try:
        c = sqlite3.connect(DB)
        for o, p in c.execute("select opath, props from objects where props like '%_global.%'"):
            for s in re.findall(r'_global\.[A-Za-z0-9_]+', p):
                res['engine_to_as'].setdefault(s, set()).add(o)
    except Exception as e: res['engine_to_as_db_error'] = str(e)
    res['engine_to_as'] = {k: sorted(v) for k, v in sorted(res['engine_to_as'].items())}
    json.dump(res, open(out, 'w'), indent=1)

if __name__ == '__main__': main(sys.argv[1])
