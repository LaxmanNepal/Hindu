const $ = (s) => document.querySelector(s);
let content = { quotes: [], scriptures: [], stories: [], mantras: [], sources: [], googleResults: [], meta: {} };

const esc = (value = "") => String(value).replace(/[&<>'"]/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;","\"":"&quot;"}[c]));
const pick = (a = []) => a.length ? a[Math.floor(Math.random() * a.length)] : null;

async function load() {
  try {
    const r = await fetch("data/content.json", { cache: "no-store" });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    content = await r.json();
    render();
  } catch (error) {
    console.error(error);
    const q = $("#quoteText");
    if (q) q.textContent = "ज्ञानको दीप आफैँभित्र प्रज्वलित गरौँ।";
    const s = $("#quoteSource");
    if (s) s.textContent = "सनातन ज्ञान";
  }
}

function renderQuote() {
  const q = pick(content.quotes) || {};
  if ($("#quoteText")) $("#quoteText").textContent = q.text || "धर्मको मार्गमा ज्ञान र विवेकसँग अघि बढौँ।";
  if ($("#quoteSource")) $("#quoteSource").textContent = q.source || "सनातन ज्ञान संग्रह";
}

function render() {
  renderQuote();
  if ($("#dateNepali")) $("#dateNepali").textContent = content.meta.todayNepali || "आजको मिति";
  if ($("#festivalText")) $("#festivalText").textContent = content.meta.tithi || "आजको तिथि तथा पर्वको जानकारी अद्यावधिक हुँदैछ।";

  if ($("#scriptureList")) {
    $("#scriptureList").innerHTML = (content.scriptures || []).slice(0, 12).map((x) =>
      `<a class="book-card" href="pages/scriptures.html"><small>${esc(x.type || "शास्त्र")}</small><strong>${esc(x.name)}</strong><span>${esc(x.description || "")}</span></a>`
    ).join("");
  }

  if ($("#storyList")) {
    $("#storyList").innerHTML = (content.stories || []).slice(0, 8).map((x) =>
      `<article class="story-card"><b>${esc(x.icon || "🪔")}</b><h3>${esc(x.title)}</h3><p>${esc(x.summary || "")}</p></article>`
    ).join("");
  }

  if ($("#mantraList")) {
    $("#mantraList").innerHTML = (content.mantras || []).slice(0, 8).map((x) =>
      `<article class="mantra"><strong>${esc(x.name)}</strong><span>${esc(x.text)}</span>${x.meaning ? `<small>${esc(x.meaning)}</small>` : ""}</article>`
    ).join("");
  }
}

function search(query) {
  const q = query.trim().toLocaleLowerCase("ne");
  if (!q) return [];
  const local = [
    ...(content.scriptures || []).map((x) => ({ ...x, kind: "शास्त्र" })),
    ...(content.stories || []).map((x) => ({ ...x, kind: "कथा" })),
    ...(content.mantras || []).map((x) => ({ ...x, kind: "मन्त्र" })),
    ...(content.quotes || []).map((x) => ({ ...x, name: x.source, description: x.text, kind: "श्लोक/ज्ञान" }))
  ];
  return local.filter((x) => JSON.stringify(x).toLocaleLowerCase("ne").includes(q));
}

function openSearchResults(query) {
  const results = search(query);
  const old = document.querySelector("#searchResults");
  if (old) old.remove();
  const box = document.createElement("section");
  box.id = "searchResults";
  box.className = "section search-results-section";
  box.innerHTML = `<div class="section-head"><div><span class="eyebrow">खोज परिणाम</span><h2>“${esc(query)}”</h2></div><span class="text-link">${results.length} भेटियो</span></div>` +
    (results.length ? `<div class="story-grid">${results.slice(0, 30).map((x) => `<article class="story-card"><small>${esc(x.kind)}</small><h3>${esc(x.name || x.title)}</h3><p>${esc(x.description || x.summary || x.text || "")}</p></article>`).join("")}</div>` : `<article class="quote-card"><p>यो खोजका लागि स्थानीय सामग्री भेटिएन।</p><footer>अर्को शब्द वा नाम प्रयोग गर्नुहोस्।</footer></article>`);
  document.querySelector("main").prepend(box);
  box.scrollIntoView({ behavior: "smooth", block: "start" });
}

$("#shuffleBtn")?.addEventListener("click", renderQuote);
$("#searchToggle")?.addEventListener("click", () => { $("#searchInput")?.focus(); window.scrollTo({ top: 0, behavior: "smooth" }); });
$("#navSearch")?.addEventListener("click", () => setTimeout(() => $("#searchInput")?.focus(), 100));
$("#searchInput")?.addEventListener("keydown", (e) => { if (e.key === "Enter") openSearchResults(e.target.value); });

load();
