import json, os, urllib.request
ROOT='data'
os.makedirs(f'{ROOT}/texts',exist_ok=True)
os.makedirs(f'{ROOT}/stories',exist_ok=True)
SOURCES={'bhagavad-gita.json':'https://raw.githubusercontent.com/ChiragMirani/gita-quotes/main/docs/data.json'}
def fetch(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Hindu-Nepali-Knowledge/1.0'})
    with urllib.request.urlopen(req,timeout=60) as r: return json.loads(r.read().decode('utf-8'))
for filename,url in SOURCES.items():
    data=fetch(url)
    out={'title':'श्रीमद्भगवद्गीता','source':data.get('source',url),'source_repository':'ChiragMirani/gita-quotes','license_note':'See upstream repository LICENSE/README before redistribution.','total_verses':data.get('total_verses',len(data.get('verses',[]))),'verses':data.get('verses',[])}
    with open(f'{ROOT}/texts/{filename}','w',encoding='utf-8') as f: json.dump(out,f,ensure_ascii=False,indent=2)
stories={'version':1,'language':'ne','note':'कथा-सूचीमा स्रोत-आधारित कथा/घटना IDs राखिन्छन्। विस्तृत मूलग्रन्थ छुट्टै corpus मा राखिन्छ।','stories':[]}
with open(f'{ROOT}/stories/index.json','w',encoding='utf-8') as f: json.dump(stories,f,ensure_ascii=False,indent=2)
print('Scripture sync complete')
