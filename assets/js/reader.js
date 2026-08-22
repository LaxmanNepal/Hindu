(() => {
  const cfg = window.HINDU_READER || {};
  const root = document.querySelector('[data-reader]');
  if (!root || !cfg.src) return;
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const q = new URLSearchParams(location.search);
  const wanted = q.get('v') || '';
  fetch(cfg.src).then(r => r.json()).then(data => {
    const verses = Array.isArray(data) ? data : (data.verses || data.items || []);
    const list = verses.map((v,i)=>({...v,_i:i}));
    const shown = wanted ? list.filter(v => String(v.id||v.number||v.verse||'') === wanted) : list.slice(0, cfg.limit || 30);
    root.innerHTML = shown.length ? shown.map(v => `<article class="verse-card"><div class="verse-meta">${esc(v.chapterName || v.chapter || '')}${v.number||v.verse ? ` · श्लोक ${esc(v.number||v.verse)}`:''}</div><h2>${esc(v.title||'श्लोक')}</h2><div class="sanskrit">${esc(v.sanskrit||v.text||v.sloka||'')}</div>${v.transliteration?`<p class="transliteration">${esc(v.transliteration)}</p>`:''}${v.nepaliMeaning||v.meaning?`<div class="meaning"><b>नेपाली अर्थ</b><p>${esc(v.nepaliMeaning||v.meaning)}</p></div>`:''}${v.explanation?`<div class="meaning"><b>सरल व्याख्या</b><p>${esc(v.explanation)}</p></div>`:''}<div class="verse-actions"><button data-copy="${esc(v.sanskrit||v.text||v.sloka||'')}">प्रतिलिपि</button><button data-share="${esc(v.title||'श्लोक')}">सेयर</button></div></article>`).join('') : '<div class="empty">सामग्री भेटिएन।</div>';
    root.querySelectorAll('[data-copy]').forEach(b=>b.onclick=()=>navigator.clipboard?.writeText(b.dataset.copy).then(()=>{b.textContent='प्रतिलिपि भयो';setTimeout(()=>b.textContent='प्रतिलिपि',1200)}));
    root.querySelectorAll('[data-share]').forEach(b=>b.onclick=()=>navigator.share?navigator.share({title:b.dataset.share,url:location.href}):navigator.clipboard?.writeText(location.href));
  }).catch(()=>root.innerHTML='<div class="empty">स्रोत सामग्री अहिले उपलब्ध छैन।</div>');
})();
