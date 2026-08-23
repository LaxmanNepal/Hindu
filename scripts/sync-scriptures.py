import json, os, urllib.request
from datetime import datetime, timezone

ROOT='data'
os.makedirs(f'{ROOT}/texts/gita',exist_ok=True)
os.makedirs(f'{ROOT}/stories',exist_ok=True)
os.makedirs(f'{ROOT}/sources',exist_ok=True)
GITA_URL='https://raw.githubusercontent.com/ChiragMirani/gita-quotes/main/docs/data.json'

def fetch(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Hindu-Nepali-Knowledge/1.0'})
    with urllib.request.urlopen(req,timeout=90) as r: return json.loads(r.read().decode('utf-8'))

def dump(path,data):
    with open(path,'w',encoding='utf-8') as f: json.dump(data,f,ensure_ascii=False,indent=2)

data=fetch(GITA_URL)
verses=data.get('verses',[])
if len(verses)<700: raise RuntimeError(f'Gita corpus unexpectedly small: {len(verses)} verses')
out={'id':'bhagavad-gita','title':'श्रीमद्भगवद्गीता','language':'sa','total_verses':len(verses),'source':data.get('source',GITA_URL),'source_repository':'https://github.com/ChiragMirani/gita-quotes','retrieved_at':datetime.now(timezone.utc).isoformat(),'license_note':'Preserve upstream attribution and license requirements when redistributing this corpus.','verses':verses}
dump(f'{ROOT}/texts/bhagavad-gita.json',out)
by_chapter={}
for v in verses:
    chapter=str(v.get('chapter') or v.get('chapter_number') or 'unknown'); by_chapter.setdefault(chapter,[]).append(v)
for chapter,items in by_chapter.items():
    path=f'{ROOT}/texts/gita/chapter-{int(chapter):02d}.json' if chapter.isdigit() else f'{ROOT}/texts/gita/chapter-{chapter}.json'
    dump(path,{'scripture':'bhagavad-gita','chapter':int(chapter) if chapter.isdigit() else chapter,'verses':items})
stories={'version':2,'language':'ne','purpose':'हिन्दू कथाहरूलाई स्रोत, पात्र, ग्रन्थ र सम्बन्धित श्लोकसँग जोड्ने index.','updated_at':datetime.now(timezone.utc).isoformat(),'stories':[{'id':'story-samudra-manthan','title':'समुद्रमन्थन','source_texts':['भागवत पुराण','विष्णु पुराण'],'entities':['विष्णु','शिव','लक्ष्मी','देवता','असुर']},{'id':'story-prahlada-narasimha','title':'प्रह्लाद र नृसिंह','source_texts':['भागवत पुराण'],'entities':['प्रह्लाद','नृसिंह','हिरण्यकशिपु']},{'id':'story-dhruva','title':'ध्रुवको तपस्या','source_texts':['भागवत पुराण'],'entities':['ध्रुव','विष्णु']},{'id':'story-govardhana','title':'गोवर्धन धारण','source_texts':['भागवत पुराण'],'entities':['कृष्ण','इन्द्र']},{'id':'story-kaliya','title':'कालिय दमन','source_texts':['भागवत पुराण'],'entities':['कृष्ण','कालिय']},{'id':'story-rama-lanka','title':'राम–रावण युद्ध','source_texts':['वाल्मीकि रामायण'],'entities':['राम','सीता','हनुमान','रावण']},{'id':'story-hanuman-lanka','title':'हनुमानको लङ्का यात्रा','source_texts':['वाल्मीकि रामायण'],'entities':['हनुमान','राम','सीता']},{'id':'story-draupadi-svayamvara','title':'द्रौपदी स्वयंवर','source_texts':['महाभारत'],'entities':['द्रौपदी','अर्जुन','पाण्डव']},{'id':'story-karna','title':'कर्णको जीवनकथा','source_texts':['महाभारत'],'entities':['कर्ण','कुन्ती','सूर्य','अर्जुन']},{'id':'story-abhimanyu','title':'अभिमन्यु र चक्रव्यूह','source_texts':['महाभारत'],'entities':['अभिमन्यु','अर्जुन','कृष्ण']}]}
dump(f'{ROOT}/stories/index.json',stories)
dump(f'{ROOT}/sources/sync-manifest.json',{'generated_at':datetime.now(timezone.utc).isoformat(),'corpora':[{'id':'bhagavad-gita','status':'complete','verse_count':len(verses),'source_repository':'https://github.com/ChiragMirani/gita-quotes'},{'id':'story-index','status':'curated-index','record_count':len(stories['stories'])}]})
print(f'Scripture sync complete: {len(verses)} Gita verses')
