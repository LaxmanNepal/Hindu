import json, os, time, urllib.request, urllib.error
from pathlib import Path

INPUT=Path('data/texts/bhagavad-gita.json')
OUTPUT=Path('data/texts/bhagavad-gita-nepali.json')
API='https://generativelanguage.googleapis.com/v1beta/models/gemini-3.7-flash:generateContent'
BATCH=20


def call_gemini(key, verses):
    compact=[]
    for v in verses:
        compact.append({
            'id': v.get('id') or v.get('verse') or v.get('number'),
            'chapter': v.get('chapter') or v.get('chapter_number'),
            'verse': v.get('verse') or v.get('verse_number') or v.get('number'),
            'sanskrit': v.get('sanskrit') or v.get('text') or v.get('sloka') or v.get('devanagari'),
            'english': v.get('translation') or v.get('english') or v.get('meaning') or ''
        })
    prompt='''तपाईं संस्कृत भगवद्गीताका विद्वान नेपाली सम्पादक हुनुहुन्छ। तलका श्लोकहरूको मौलिक नेपाली भावार्थ र सरल व्याख्या लेख्नुहोस्। मूल श्लोकको अर्थ नबिगार्नुहोस्। कुनै नयाँ धार्मिक दाबी नथप्नुहोस्। प्रत्येक input को id जस्ताको तस्तै फर्काउनुहोस्। केवल वैध JSON array दिनुहोस्। प्रत्येक वस्तुमा id, nepali_meaning, nepali_explanation र key_teaching हुनुपर्छ। nepali_meaning संक्षिप्त तर अर्थपूर्ण होस्; nepali_explanation 1–3 वाक्य होस्; key_teaching एक वाक्य होस्। यो 'शाब्दिक प्रमाणित नेपाली अनुवाद' भनेर दाबी नगर्नुहोस्; यो मौलिक नेपाली भावार्थ हो।\n\nINPUT:\n''' + json.dumps(compact, ensure_ascii=False)
    body=json.dumps({'contents':[{'parts':[{'text':prompt}]}],'generationConfig':{'responseMimeType':'application/json','temperature':0.2,'maxOutputTokens':12000}},ensure_ascii=False).encode()
    req=urllib.request.Request(API,data=body,headers={'Content-Type':'application/json','x-goog-api-key':key},method='POST')
    with urllib.request.urlopen(req,timeout=180) as r:
        data=json.loads(r.read().decode())
    text=data['candidates'][0]['content']['parts'][0]['text']
    return json.loads(text)


def main():
    key=os.environ.get('GEMINI_API_KEY')
    if not key: raise SystemExit('GEMINI_API_KEY secret is required')
    if not INPUT.exists(): raise SystemExit('Run scripture sync first: data/texts/bhagavad-gita.json is missing')
    source=json.loads(INPUT.read_text(encoding='utf-8'))
    verses=source.get('verses', source if isinstance(source,list) else [])
    existing={}
    if OUTPUT.exists():
        old=json.loads(OUTPUT.read_text(encoding='utf-8'))
        existing={str(x['id']):x for x in old.get('verses',[]) if x.get('id')}
    pending=[v for v in verses if str(v.get('id') or v.get('verse') or v.get('number')) not in existing]
    print(f'Total: {len(verses)}, existing: {len(existing)}, pending: {len(pending)}')
    for i in range(0,len(pending),BATCH):
        batch=pending[i:i+BATCH]
        for attempt in range(3):
            try:
                rows=call_gemini(key,batch); break
            except Exception as e:
                print('attempt failed:',e)
                if attempt==2: raise
                time.sleep(10*(attempt+1))
        for row in rows:
            existing[str(row['id'])]=row
        ordered=[]
        for v in verses:
            ident=str(v.get('id') or v.get('verse') or v.get('number'))
            if ident in existing:
                merged=dict(v); merged.update(existing[ident]); ordered.append(merged)
        payload={'id':'bhagavad-gita','title':'श्रीमद्भगवद्गीता','language':'ne','translation_type':'मौलिक नेपाली भावार्थ तथा सरल व्याख्या','source_scripture':'data/texts/bhagavad-gita.json','total_verses':len(ordered),'verses':ordered}
        OUTPUT.parent.mkdir(parents=True,exist_ok=True); OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
        print(f'Generated {min(i+BATCH,len(pending))}/{len(pending)}')
        time.sleep(2)
    print('Nepali Gita corpus complete:',len(existing))

if __name__=='__main__': main()
