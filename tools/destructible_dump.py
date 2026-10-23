"""Read-only: print an HmDestructibleBlueprint's pieces, states (health, auto transition), links and non-debris effects.
usage: destructible_dump.py <blueprint opath>"""
import sqlite3, json, sys
db = sqlite3.connect(r"F:\Transformers Rebuild\AssetTools\manifests\authored.db")
def get(o):
    r = db.execute("select class,props from objects where opath=?", (o,)).fetchone()
    return (r[0], json.loads(r[1])) if r else (None, {})
root = sys.argv[1]
c, d = get(root)
print(root, {k: v for k, v in d.items() if k != 'PieceBlueprints'})
for pb in d.get('PieceBlueprints', []):
    c, p = get(pb)
    sts = p.get('StateBlueprints', [])
    print(' piece', p.get('PieceName'), {k: v for k, v in p.items() if k != 'StateBlueprints'})
    for i, sb in enumerate(sts):
        c, s = get(sb)
        print('  [%d] %s' % (i, sb.rsplit('.', 1)[1]), {k: v for k, v in s.items() if k not in ('LinkBlueprints',) and not (isinstance(v, list) and v and isinstance(v[0], str) and 'Effect' in v[0])})
        for lb in s.get('LinkBlueprints', []):
            lc, l = get(lb)
            tgt = l.get('TargetState') or l.get('DestinationState') or l
            print('      link', json.dumps({k: (v.rsplit('.', 1)[-1] if isinstance(v, str) else v) for k, v in l.items()})[:400])
        for k, v in s.items():
            if isinstance(v, list) and v and isinstance(v[0], str) and 'Effect' in v[0]:
                for e in v:
                    ec, ed = get(e)
                    if ec and 'Debris' not in ec:
                        print('      eff', ec, json.dumps({kk: vv for kk, vv in ed.items() if kk not in ('MeshTemplate', 'LightingOption', 'ShadowingOption')})[:260])
