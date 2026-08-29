const esc = (s='') => String(s).replace(/[&<>\"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[c]));
const app=document.querySelector('#app'), q=document.querySelector('#q'), typeFilter=document.querySelector('#typeFilter'), traditionFilter=document.querySelector('#traditionFilter'), stats=document.querySelector('#catalogStats');
let rows=[];

function render(){
  const term=(q?.value||'').trim().toLocaleLowerCase('ne');
  const type=typeFilter?.value||'', tradition=traditionFilter?.value||'';
  const filtered=rows.filter(x=>{
    const hay=[x.nepali_name,x.sanskrit_name,x.author_rishi,x.subject,x.type,x.tradition].join(' ').toLocaleLowerCase('ne');
    return (!term||hay.includes(term))&&(!type||x.type===type)&&(!tradition||x.tradition===tradition);
  });
  if(stats) stats.innerHTML=`<div><span class="eyebrow">ज्ञानकोश</span><h2>${rows.length.toLocaleString('ne-NP')} ग्रन्थ</h2></div><span class="text-link">${filtered.length.toLocaleString('ne-NP')} परिणाम</span>`;
  if(!filtered.length){app.innerHTML='<div class="empty">खोजीसँग मिल्ने ग्रन्थ भेटिएन।</div>';return;}
  app.innerHTML=`<section class="section"><div class="story-grid">${filtered.slice(0,200).map((x,i)=>`<article class="story-card grantha-card"><small>${esc(x.type)} · ${esc(x.tradition)}</small><h3>${esc(x.nepali_name)}</h3><p><strong>संस्कृत:</strong> ${esc(x.sanskrit_name)}</p><p><strong>लेखक/ऋषि:</strong> ${esc(x.author_rishi)}</p><p><strong>विषय:</strong> ${esc(x.subject)}</p><footer>#${i+1} · ${esc(x.id)}</footer></article>`).join('')}</div>${filtered.length>200?`<p class="catalog-more">पहिलो २०० परिणाम देखाइएको छ। थप सटीक परिणामका लागि खोज वा फिल्टर प्रयोग गर्नुहोस्।</p>`:''}</section>`;
}

function fillFilters(){
  const types=[...new Set(rows.map(x=>x.type))].sort((a,b)=>a.localeCompare(b,'ne'));
  const traditions=[...new Set(rows.map(x=>x.tradition))].sort((a,b)=>a.localeCompare(b,'ne'));
  typeFilter.innerHTML='<option value="">सबै प्रकार</option>'+types.map(x=>`<option>${esc(x)}</option>`).join('');
  traditionFilter.innerHTML='<option value="">सबै परम्परा</option>'+traditions.map(x=>`<option>${esc(x)}</option>`).join('');
}

Promise.all([
  fetch('../data/granthas.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error(r.status);return r.json();})
]).then(([d])=>{rows=d.granthas||[];fillFilters();render();}).catch(err=>{console.error(err);app.innerHTML='<div class="empty">ग्रन्थ डेटा लोड हुन सकेन। JSON/CSV फाइल उपलब्ध नभएको वा अपडेट भइरहेको हुन सक्छ।</div>';if(stats)stats.innerHTML='<div><span class="eyebrow">त्रुटि</span><h2>डेटा लोड भएन</h2></div>';});
q?.addEventListener('input',render); typeFilter?.addEventListener('change',render); traditionFilter?.addEventListener('change',render);
