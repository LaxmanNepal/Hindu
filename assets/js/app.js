const $=s=>document.querySelector(s);
let content={quotes:[],scriptures:[],stories:[],mantras:[],meta:{}};
async function load(){try{const r=await fetch('data/content.json',{cache:'no-store'});content=await r.json();render();}catch(e){console.error(e)}}
function pick(a){return a[Math.floor(Math.random()*a.length)]}
function render(){
 const q=pick(content.quotes)||{};$('#quoteText').textContent=q.text||'धर्मको मार्गमा ज्ञान र विवेकसँग अघि बढौँ।';$('#quoteSource').textContent=q.source||'सनातन ज्ञान संग्रह';
 $('#dateNepali').textContent=content.meta.todayNepali||'आज';$('#festivalText').textContent=content.meta.tithi||'आजको तिथि सामग्री अद्यावधिक हुँदैछ।';
 $('#scriptureList').innerHTML=content.scriptures.slice(0,8).map(x=>`<a class="book-card" href="pages/scriptures.html"><small>${x.type||'शास्त्र'}</small><strong>${x.name}</strong><span>${x.description||''}</span></a>`).join('');
 $('#storyList').innerHTML=content.stories.slice(0,4).map(x=>`<article class="story-card"><b>${x.icon||'🪔'}</b><h3>${x.title}</h3><p>${x.summary||''}</p></article>`).join('');
 $('#mantraList').innerHTML=content.mantras.slice(0,5).map(x=>`<article class="mantra"><strong>${x.name}</strong><span>${x.text}</span></article>`).join('');
}
$('#shuffleBtn').addEventListener('click',()=>{const q=pick(content.quotes)||{};$('#quoteText').textContent=q.text||'';$('#quoteSource').textContent=q.source||''});
$('#searchToggle').onclick=()=>{$('#searchInput').focus();window.scrollTo({top:0,behavior:'smooth'})};$('#navSearch').onclick=()=>setTimeout(()=>$('#searchInput').focus(),100);
$('#searchInput').addEventListener('keydown',e=>{if(e.key==='Enter'){const q=e.target.value.trim().toLowerCase();if(!q)return;const all=[...content.scriptures,...content.stories,...content.mantras];const found=all.filter(x=>JSON.stringify(x).toLowerCase().includes(q));alert(found.length?`${found.length} सामग्री भेटियो। विस्तृत खोज पृष्ठ चाँडै थपिँदैछ।`:'यो शब्दको सामग्री भेटिएन।') }});
load();
