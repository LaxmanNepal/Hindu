(() => {
  const root = document.createElement('nav');
  root.className = 'knowledge-nav';
  root.setAttribute('aria-label','मुख्य ज्ञान संग्रह');
  const base = location.pathname.includes('/pages/') ? '' : 'pages/';
  const items = [
    ['🏠','गृह',base === 'pages/' ? '../' : './'],
    ['📜','वेद',base+'veda.html'],
    ['🪷','गीता',base+'gita.html'],
    ['🪔','भगवान्',base+'bhagwan.html'],
    ['📿','मन्त्र',base+'mantras.html'],
    ['📖','कथा',base+'stories.html'],
    ['🌙','पञ्चाङ्ग',base+'panchang.html'],
    ['📚','शास्त्र',base+'scriptures.html']
  ];
  root.innerHTML = items.map(([icon,label,href]) => `<a href="${href}"><span>${icon}</span>${label}</a>`).join('');
  document.body.insertBefore(root, document.body.firstChild);
})();
