import csv, json, re
from pathlib import Path
from generate_grantha_dataset import GROUPS
from complete_grantha_dataset import EXTRA

FINAL_EXTRA='''पाञ्चरात्ररत्न-संहिता पाञ्चरात्रसार-संहिता नारायणतत्त्व-संहिता'''.split()

def build():
    rows=[]; seen=set(); non_suffix={'धर्मशास्त्र/धर्मसूत्र','दर्शनग्रन्थ','योगग्रन्थ','तन्त्र','स्तोत्र/कवच','काव्य/नाट्यग्रन्थ','शास्त्र/वेदाङ्ग','क्षेत्रीय भक्तिग्रन्थ','भक्तिदर्शन/ग्रन्थ'}
    for names,typ,suffix,author,subject,tradition in GROUPS:
        for name in names:
            title=name if typ in non_suffix else name+' '+suffix; key=re.sub(r'\s+','',title)
            if key in seen: continue
            seen.add(key); rows.append({'id':f'HG{len(rows)+1:04d}','nepali_name':title,'sanskrit_name':title,'author_rishi':author,'subject':subject,'type':typ,'tradition':tradition})
    for title in EXTRA+FINAL_EXTRA:
        key=re.sub(r'\s+','',title)
        if key in seen: continue
        seen.add(key); rows.append({'id':f'HG{len(rows)+1:04d}','nepali_name':title,'sanskrit_name':title,'author_rishi':'पाञ्चरात्र परम्परा/परम्परागत','subject':'वैष्णव आगम, संहिता, मन्दिर-उपासना, मन्त्र र तत्त्व','type':'पाञ्चरात्र संहिता','tradition':'वैष्णव/पाञ्चरात्र'})
    if len(rows)<1000: raise RuntimeError(f'Only {len(rows)} records generated')
    return rows

root=Path(__file__).resolve().parents[1]; out=root/'data'; out.mkdir(exist_ok=True); rows=build()
meta={'title':'१,०००+ हिन्दू ग्रन्थ ज्ञानकोश','language':'ne','count':len(rows),'updated':'2026-08-29','note':'सूचीमा श्रुति, स्मृति, इतिहास, पुराण, आगम, तन्त्र, दर्शन, योग, स्तोत्र, संस्कृत साहित्य, वेदाङ्ग/शास्त्र र क्षेत्रीय भक्तिसाहित्य समेटिएका छन्। प्राचीन ग्रन्थमा लेखकत्व/वर्गीकरण परम्पराअनुसार फरक हुन सक्छ।'}
(out/'granthas.json').write_text(json.dumps({'meta':meta,'granthas':rows},ensure_ascii=False,indent=2),encoding='utf-8')
with (out/'granthas.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=['id','nepali_name','sanskrit_name','author_rishi','subject','type','tradition']); w.writeheader(); w.writerows(rows)
print('Generated',len(rows),'records')
