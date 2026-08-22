(() => {
  const links = [
    ['⌂','गृह','../index.html'],['📜','वेद','veda.html'],['🪷','गीता','gita.html'],['🪔','भगवान्','bhagwan.html'],['📿','मन्त्र','mantras.html'],['📖','कथा','stories.html'],['🌙','पञ्चाङ्ग','panchang.html'],['📚','शास्त्र','scriptures.html']
  ];
  const nav = document.querySelector('[data-site-nav]');
  if (!nav) return;
  nav.innerHTML = links.map(([i,n,u])=>`<a href="${u}"><span>${i}</span>${n}</a>`).join('');
})();
