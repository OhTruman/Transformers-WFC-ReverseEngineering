"""Read-only: parse *PhysicalMaterialProperty exports (skipped by AssetTools authored.db, which drops classes ending in Property) from cooked packages.
Usage: python physprop.py Startup_int [...]  -> physprops.json next to this script"""
import sys,os,json
sys.path.insert(0,r'F:\Transformers Rebuild\AssetTools\scripts\wfc')
import ue3pkg, typed_props as tp
out={}
for name in sys.argv[1:]:
    p=ue3pkg.Package(os.path.join(r'F:\Transformers Rebuild\Game Dump\TransGame\CookedXenon',name+'.xxx'))
    r=tp.TypedReader(p)
    for i,e in enumerate(p.exports):
        c=p.class_name(e)
        if not c.endswith('PhysicalMaterialProperty'): continue
        tags,used=r.read_object(i+1)
        out[p.object_path(i+1)]={'class':c,'props':tp.simplify(tp.to_dict(tags))}
json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'physprops.json'),'w'),indent=1,default=str)
print(len(out))
