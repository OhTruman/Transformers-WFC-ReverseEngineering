"""Per-chapter streaming order export (read-only): authored.db LevelStreamingState / Checkpoint / SeqAct_SetStreamingState
+ WorldInfo.InitialStreamingState, plus the menu checkpoint list from TransLevels.ini. Writes work/handoff/campaign_streaming_order.json."""
import sqlite3, json, re, collections, os
DB = r"F:\Transformers Rebuild\AssetTools\manifests\authored.db"
INI = r"F:\Transformers Rebuild\ExtractedAssets\config\Coalesced_ini\TransGame\Config\Xenon\Cooked\TransLevels.ini"
OUT = os.path.join(os.path.dirname(__file__), '..', 'work', 'handoff', 'campaign_streaming_order.json')
CH = {'A1_IAC_Base_m': 96, 'A2_KON_Base_m': 97, 'A3_COR_Base_m': 98, 'A4_ORB_Base_m': 99, 'A5_TRY_Base_m': 100,
      'D1_ORB_Base_m': 101, 'D2_COR_Base_m': 102, 'D3A_IAC_Base_m': 103, 'D3B_IAC_Base_m': 104, 'D5_OME_BASE_m': 105}
db = sqlite3.connect(DB)
ini = open(INI, encoding='utf-8', errors='ignore').read()
menu = collections.defaultdict(list)
for name, body in re.findall(r'^\[([^\]]+) TnDataProvider_Checkpoint\]\s*\n(.*?)(?=^\[|\Z)', ini, re.M | re.S):
    kv = dict(l.split('=', 1) for l in body.splitlines() if '=' in l and not l.startswith(';'))
    menu[int(kv.get('MapId', -1))].append({'id': name, 'path': kv.get('CheckpointPath', '').replace('|', '.')})
out = {}
for base, mid in CH.items():
    pkg = base.split('_m')[0]
    like = base[:7] + '%' if not base.startswith('D3') else base[:8] + '%'
    states = {}
    for o, p in db.execute("select opath,props from objects where class='LevelStreamingState' and lower(opath) like ?", (base.lower() + '.%',)):
        d = json.loads(p); states[o.split('.')[-1]] = [(l['LevelName'], bool(l.get('LevelVisible'))) for l in d.get('Levels', [])]
    wi = db.execute("select props from objects where class='WorldInfo' and opath like ?", (base + '.TheWorld.%',)).fetchone()
    init = (json.loads(wi[0]).get('InitialStreamingState') or '').split('.')[-1] if wi else None
    cps = []
    for o, p in db.execute("select opath,props from objects where class='Checkpoint' and lower(opath) like ?", (base.lower() + '.%',)):
        d = json.loads(p)
        cps.append({'checkpoint': o.split('.')[-1], 'display_order': d.get('DisplayOrder', 0), 'state': (d.get('StreamingState') or '').split('.')[-1],
                    'aux_spawns': len(d.get('AuxilliarySpawnPoints') or []), 'actions': [a.split('.')[-1] for a in d.get('Actions') or []]})
    cps.sort(key=lambda c: c['display_order'])
    mpaths = [m['path'].lower() for m in menu[mid]]
    for c in cps:
        full = (base + '.TheWorld.PersistentLevel.' + c['checkpoint']).lower()
        c['menu_index'] = mpaths.index(full) if full in mpaths else None
    sets = []
    for o, p in db.execute("select opath,props from objects where class='SeqAct_SetStreamingState' and opath like ?", (base[:4] + '%',)):
        d = json.loads(p); st = (d.get('StreamingState') or '')
        if st.lower().startswith(base.lower() + '.'): sets.append({'op': o.split('PersistentLevel.')[-1], 'state': st.split('.')[-1]})
    out[base] = {'map_id': mid, 'initial_state': init, 'states': states, 'checkpoints_in_display_order': cps,
                 'menu_checkpoints': menu[mid], 'set_streaming_ops': sorted(sets, key=lambda s: s['op'])}
json.dump(out, open(OUT, 'w'), indent=1)
for b, v in out.items():
    print(b, 'init', v['initial_state'], 'states', len(v['states']), 'checkpoints', len(v['checkpoints_in_display_order']),
          'menu', sum(1 for c in v['checkpoints_in_display_order'] if c['menu_index'] is not None), 'setops', len(v['set_streaming_ops']))
