import sys,struct,re,collections
sys.path.insert(0,r"F:\Transformers Rebuild\RE-Workspace\tools")
import pkgload, xenosdis as X
pk=sys.argv[1]
p=pkgload.load(pk); d=p.data
stats=collections.Counter(); ex=[]
for i,e in enumerate(p.exports,1):
    if p.class_name(e)!='ShaderCache': continue
    o=e['serial_offset']; blob=d[o:o+e['serial_size']]
    pos=0
    while True:
        h=blob.find(b'\x10\x2a\x11\x00',pos)
        if h<0: break
        pos=h+4
        try:
            ver,tgt,cs=X.parse_ctab(blob,h+0x28)
            names={c[0] for c in cs}
            if 'SceneColorBiasFactor' not in names: continue
            M,cfs=X.find_microcode(blob,h+0x28,h+0x6000)
            if not M: stats['nomc']+=1; continue
            lines=X.disasm(blob,M,cfs)
        except Exception as err:
            stats['err']+=1; continue
        w=[l for l in lines if 'oC0' in l]
        rgb=[l for l in w if re.search(r'oC0\.[xyz_]*[xyz]',l)]
        sat=any('_sat' in l for l in rgb)
        kind=('lit' if any(n.startswith(('LightColor','DirectLight','LightAttenuation','UpperSkyColor')) for n in names) else 'unlit')
        stats[(kind,'rgb_sat' if sat else 'rgb_nosat')]+=1
        if len(ex)<6 and not sat: ex.append((hex(o+h),sorted(names)[:8],rgb[-2:]))
        if sat and stats[('satex',)]<4: stats[('satex',)]+=1; print("SAT",hex(o+h),sorted(names)[:10],rgb[-3:])
print(pk,dict(stats))
for x in ex: print(x)
