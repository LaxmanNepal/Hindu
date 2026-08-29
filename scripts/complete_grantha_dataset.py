import csv, json, re
from pathlib import Path
from generate_grantha_dataset import GROUPS

EXTRA = '''नारायणोत्तर-संहिता नारायणकल्प-संहिता नरसिंहपाद्म-संहिता ज्ञानार्णव-संहिता तन्त्रतिलक-संहिता त्रयशतोत्तर-संहिता दुर्वासा-संहिता नरसिंह-संहिता नारायण-संहिता बृहस्पति-महातन्त्रम् बोधायन-तन्त्रम् ब्रह्म-तन्त्रम् महाकाल-पाञ्चरात्रम् महासानत्कुमार-संहिता माहेश्वर-तन्त्रम् श्री-शास्त्रम् श्रीकालपरा-संहिता श्रीधर-संहिता सङ्कर्षण-संहिता सनक-संहिता सनत्-संहिता सनन्द-संहिता सात्यकि-तन्त्रम् सारसमुच्चय-संहिता साम्वर्त-संहिता सुदर्शन-संहिता सुपर्णप्रश्न-संहिता हयग्रीव-तन्त्रम् हंसपारमेश्वर-संहिता हिरण्यगर्भ-संहिता कालोत्तर-संहिता श्रीमन्नारायण-संहिता विश्वेश्वर-संहिता वैहायसी-संहिता शुकप्रश्न-संहिता शौनक-संहिता शौनकीय-संहिता वृद्धपाद्म-संहिता वासुदेव-संहिता विश्व-संहिता विष्णुतत्त्व-संहिता विष्णुरहस्य-संहिता विष्णुमन्दिर-संहिता विष्णुसिद्धान्त-संहिता विष्वक्सेन-संहिता विहगेन्द्र-संहिता विहगेश्वर-संहिता पद्मनाभ-संहिता पद्मोद्भव-संहिता परमेष्ठ्य-संहिता पाराशर्य-संहिता पूर्ण-संहिता प्रद्युम्न-संहिता प्रह्लाद-संहिता बलपौष्कर-संहिता बृहद्ब्रह्म-संहिता भृगुसंहिता गोविन्द-संहिता गौतम-संहिता जयॊत्तर-संहिता'''.split()


def build():
    rows, seen = [], set()
    non_suffix={'धर्मशास्त्र/धर्मसूत्र','दर्शनग्रन्थ','योगग्रन्थ','तन्त्र','स्तोत्र/कवच','काव्य/नाट्यग्रन्थ','शास्त्र/वेदाङ्ग','क्षेत्रीय भक्तिग्रन्थ','भक्तिदर्शन/ग्रन्थ'}
    for names, typ, suffix, author, subject, tradition in GROUPS:
        for name in names:
            title=name if typ in non_suffix else name+' '+suffix
            key=re.sub(r'\s+','',title)
            if key in seen: continue
            seen.add(key)
            rows.append({'id':f'HG{len(rows)+1:04d}','nepali_name':title,'sanskrit_name':title,'author_rishi':author,'subject':subject,'type':typ,'tradition':tradition})
    for title in EXTRA:
        key=re.sub(r'\s+','',title)
        if key in seen: continue
        seen.add(key)
        rows.append({'id':f'HG{len(rows)+1:04d}','nepali_name':title,'sanskrit_name':title,'author_rishi':'पाञ्चरात्र परम्परा/परम्परागत','subject':'वैष्णव आगम, संहिता, मन्दिर-उपासना, मन्त्र र तत्त्व','type':'पाञ्चरात्र संहिता','tradition':'वैष्णव/पाञ्चरात्र'})
    if len(rows)<1000: raise RuntimeError(f'Only {len(rows)} records generated')
    return rows

root=Path(__file__).resolve().parents[1]; out=root/'data'; out.mkdir(exist_ok=True)
rows=build(); meta={'title':'१,०००+ हिन्दू ग्रन्थ ज्ञानकोश','language':'ne','count':len(rows),'updated':'2026-08-29','note':'सूचीमा श्रुति, स्मृति, इतिहास, पुराण, आगम, तन्त्र, दर्शन, योग, स्तोत्र, संस्कृत साहित्य, वेदाङ्ग/शास्त्र र क्षेत्रीय भक्तिसाहित्य समेटिएका छन्। प्राचीन ग्रन्थमा लेखकत्व/वर्गीकरण परम्पराअनुसार फरक हुन सक्छ।'}
(out/'granthas.json').write_text(json.dumps({'meta':meta,'granthas':rows},ensure_ascii=False,indent=2),encoding='utf-8')
with (out/'granthas.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=['id','nepali_name','sanskrit_name','author_rishi','subject','type','tradition']); w.writeheader(); w.writerows(rows)
print('Generated',len(rows),'records')
