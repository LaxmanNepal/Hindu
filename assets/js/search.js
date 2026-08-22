(() => {
  const q = document.querySelector('#q');
  const out = document.querySelector('#results');
  const sources = [
    ['../data/deities.json','deities','भगवान्'],
    ['../data/hindu-knowledge.json','entries','ज्ञान'],
    ['../data/hindu-encyclopedia.json','entries','विश्वकोश'],
    ['../data/content.json','stories','कथा'],
    ['../data/content.json','mantras','मन्त्र'],
    ['../data/scriptures.json','scriptures','शास्त्र']
  ];
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let all=[];
  Promise.all(sources.map(async ([url,key,type])=>{try{const d=await fetch(url).then(r=>r.json());const a=Array.isArray(d)?d:(d[key]||[]);return a.map(x=>({...x,_type:type,_blob:JSON.stringify(x).toLowerCase()}));}catch{return []}})).then(groups=>{all=groups.flat();render('')});
  function render(term){const t=term.trim().toLowerCase();const hits=t?all.filter(x=>x._blob.includes(t)):all.slice(0,18);out.innerHTML=hits.length?hits.map(x=>{const title=x.name||x.title||x.deity||x.chapter_name||x.sanskrit||'ज्ञान';const body=x.summary||x.description||x.meaning||x.story||x.text||x.content||'';return `<article class="story-card"><span class="eyebrow">${esc(x._type)}</span><h3>${esc(title)}</h3><p>${esc(String(body).slice(0,300))}</p></article>`}).join(''):`<p>यस खोजका लागि सामग्री भेटिएन। अर्को शब्द प्रयोग गर्नुहोस्।</p>`}
  q.addEventListener('input',e=>render(e.target.value));
})();
