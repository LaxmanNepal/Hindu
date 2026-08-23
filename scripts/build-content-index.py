import json, pathlib
from datetime import datetime, timezone
root=pathlib.Path('data'); out=[]
for p in root.rglob('*.json'):
    if 'sources/sync-manifest' in str(p) or 'search-index' in str(p): continue
    try: d=json.loads(p.read_text(encoding='utf-8'))
    except: continue
    def walk(x):
        if isinstance(x,dict):
            title=x.get('title') or x.get('name') or x.get('chapterName')
            ident=x.get('id')
            if ident and title: out.append({'id':ident,'title':title,'path':str(p),'type':x.get('type') or p.parent.name,'description':x.get('description') or x.get('summary') or x.get('nepaliMeaning') or ''})
            for v in x.values(): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(d)
seen={}; [seen.setdefault(x['id'],x) for x in out]
result={'version':1,'language':'ne','generated_at':datetime.now(timezone.utc).isoformat(),'count':len(seen),'items':sorted(seen.values(),key=lambda x:x['title'])}
(root/'search-index.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('Generated',len(seen),'search records')
