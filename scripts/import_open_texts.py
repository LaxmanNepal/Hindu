"""Fetch openly licensed/public scripture datasets into data/ with provenance.

This intentionally stores upstream data and attribution rather than silently copying
third-party material. Translation/meaning fields must retain their original license.
"""
import json, os, shutil, subprocess, tempfile
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'texts'
DATA.mkdir(parents=True,exist_ok=True)
UA='HinduNepaliKnowledge/1.0 (+https://github.com/LaxmanNepal/Hindu)'

def get(url):
 r=requests.get(url,headers={'User-Agent':UA},timeout=30); r.raise_for_status(); return r

def fetch_gita():
 # Public-domain translation dataset; preserve upstream attribution.
 url='https://raw.githubusercontent.com/ChiragMirani/gita-quotes/main/data.json'
 try:
  data=get(url).json()
  (DATA/'bhagavad-gita.json').write_text(json.dumps({'source':url,'license':'Public-domain translation as stated by upstream repository','verses':data},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  print('Gita:',len(data),'verses')
 except Exception as e: print('Gita import skipped:',e)

def fetch_dharmic_manifest():
 manifest={'repository':'https://github.com/bhavykhatri/DharmicData','license':'ODbL-1.0','note':'Upstream dataset contains Vedas, Gita, Mahabharata and Ramayana. The Action may fetch individual files after license checks. Do not merge incompatible translations blindly.','selectedCollections':['SrimadBhagvadGita','Mahabharata','ValmikiRamayana','Rigveda','Yajurveda','Atharvaveda']}
 (DATA/'dharmicdata-source.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': fetch_gita(); fetch_dharmic_manifest()
