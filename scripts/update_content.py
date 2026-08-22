import json, os, re, time
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'content.json'
UA='HinduNepaliKnowledge/1.0 (GitHub Actions; public project)'

WIKI={
 'भगवद्गीता':'Bhagavad_Gita','महाभारत':'Mahabharata','रामायण':'Ramayana','वेद':'Vedas','सरस्वती':'Saraswati','पुराण':'Puranas','उपनिषद्':'Upanishads','कृष्ण':'Krishna','राम':'Rama'
}

def wiki(title):
    r=requests.get('https://en.wikipedia.org/api/rest_v1/page/summary/'+requests.utils.quote(title),headers={'User-Agent':UA},timeout=20)
    if r.ok:
        x=r.json(); return {'title':x.get('title'), 'summary':x.get('extract',''), 'url':x.get('content_urls',{}).get('desktop',{}).get('page')}
    return None

def google_search(query):
    key=os.getenv('GOOGLE_API_KEY'); cx=os.getenv('GOOGLE_CSE_ID')
    if not key or not cx: return []
    p={'key':key,'cx':cx,'q':query,'num':10,'safe':'active','lr':'lang_ne'}
    r=requests.get('https://www.googleapis.com/customsearch/v1',params=p,headers={'User-Agent':UA},timeout=20)
    if not r.ok: return []
    return [{'title':i.get('title'),'url':i.get('link'),'snippet':i.get('snippet','')} for i in r.json().get('items',[])]

def main():
    data=json.loads(OUT.read_text(encoding='utf-8'))
    sources=[]
    for nep,eng in WIKI.items():
        x=wiki(eng)
        if x: sources.append({'topic':nep,'source':'Wikipedia','url':x['url'],'summary':x['summary']})
        time.sleep(.25)
    google=[]
    for q in ['वेद हिन्दू धर्म','भगवद्गीता श्लोक अर्थ नेपाली','महाभारत कथा','रामायण कथा','हिन्दू तिथि पर्व','सरस्वती देवी कथा','पुराण कथा']:
        google.extend(google_search(q))
    data['meta']['updatedAt']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    data['meta']['sourceCount']=len(sources)+len(google)
    data['sources']=sources[:50]
    data['googleResults']=google[:50]
    OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__': main()
