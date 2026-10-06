"""Read-only: print a UE3 material input (EmissiveColor, OpacityMask, ...) as an expression tree from authored.db.
Usage: python matgraph.py <Material opath> <InputName>   (shared nodes printed once, later refs marked (*); [n] = output index: 1=R 2=G 3=B 4=A)"""
import sqlite3,json,sys
db=sqlite3.connect(r'F:\Transformers Rebuild\AssetTools\manifests\authored.db')
M=sys.argv[1]; root=sys.argv[2]
ex={o:(c,json.loads(p or '{}')) for o,c,p in db.execute("select opath,class,props from objects where opath like ?",(M+'.%',))}
top=json.loads(db.execute("select props from objects where opath=?",(M,)).fetchone()[0])
names={}
def nm(o): return o.split('.')[-1].replace('MaterialExpression','')
SKIP={'EditorX','EditorY','ExpressionGUID','bRealtimePreview','Desc','Group'}
def expr(ref,depth,seen):
    if not isinstance(ref,dict) or 'Expression' not in ref: return repr(ref)
    o=ref['Expression']; oi=ref.get('ExpressionOutputIndex',0)
    if o not in ex: return nm(o)+'?'
    c,d=ex[o]; n=nm(o)
    tag=n+('[%d]'%oi if oi else '')
    for m in 'RGBA':
        if ref.get('Mask'+m): tag+='.'+m
    if o in seen:
        print("  "*depth+tag+"(*)"); return tag
    seen.add(o)
    args={k:v for k,v in d.items() if k not in SKIP}
    inner=[]
    for k,v in args.items():
        if isinstance(v,dict) and 'Expression' in v: inner.append((k,v))
    flat={k:v for k,v in args.items() if not (isinstance(v,dict) and 'Expression' in v) and k not in('Inputs','Outputs')}
    s='  '*depth+tag+' '+json.dumps(flat)[:200]+(' desc='+d['Desc'] if 'Desc' in d else '')
    print(s)
    if c=='MaterialExpressionFunction':
        for i,inp in enumerate(d.get('Inputs',[])):
            print('  '*(depth+1)+'in%d:'%i); expr(inp,depth+2,seen)
    for k,v in inner:
        print('  '*(depth+1)+k+':'); expr(v,depth+2,seen)
    return tag
expr(top[root],0,set())
