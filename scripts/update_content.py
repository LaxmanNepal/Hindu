import json
import os
import time
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "content.json"
UA = "HinduNepaliKnowledge/2.0 (GitHub Actions; public project)"
TIMEOUT = 20

TOPICS = {
    "भगवद्गीता": "Bhagavad_Gita",
    "महाभारत": "Mahabharata",
    "रामायण": "Ramayana",
    "वेद": "Vedas",
    "सरस्वती": "Saraswati",
    "पुराण": "Puranas",
    "उपनिषद्": "Upanishads",
    "कृष्ण": "Krishna",
    "राम": "Rama",
    "शिव": "Shiva",
    "विष्णु": "Vishnu",
    "गणेश": "Ganesha",
    "दुर्गा": "Durga",
    "हनुमान": "Hanuman",
}

SEARCH_TOPICS = [
    "वेद हिन्दू धर्म",
    "भगवद्गीता श्लोक अर्थ",
    "महाभारत कथा पात्र",
    "रामायण कथा पात्र",
    "१८ पुराण हिन्दू धर्म",
    "सरस्वती देवी कथा",
    "हिन्दू तिथि पर्व पञ्चाङ्ग",
    "हिन्दू मन्त्र स्तोत्र",
]


def get_json(url, params=None):
    try:
        r = requests.get(url, params=params, headers={"User-Agent": UA}, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as exc:
        print(f"WARN: {url}: {exc}")
        return None


def wikipedia(language, title):
    base = f"https://{language}.wikipedia.org/api/rest_v1/page/summary/{quote(title, safe='')}"
    x = get_json(base)
    if not x:
        return None
    urls = x.get("content_urls", {}).get("desktop", {})
    return {
        "topic": title,
        "language": language,
        "source": "Wikipedia",
        "title": x.get("title", title),
        "summary": x.get("extract", ""),
        "url": urls.get("page", f"https://{language}.wikipedia.org/wiki/{quote(title)}"),
        "license": "CC BY-SA (Wikipedia content; see source page)",
    }


def google_search(query):
    key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_CSE_ID")
    if not key or not cx:
        return []
    x = get_json(
        "https://www.googleapis.com/customsearch/v1",
        {"key": key, "cx": cx, "q": query, "num": 10, "safe": "active", "lr": "lang_ne"},
    )
    if not x:
        return []
    return [
        {
            "title": i.get("title", ""),
            "url": i.get("link", ""),
            "snippet": i.get("snippet", ""),
            "query": query,
            "source": "Google Search",
        }
        for i in x.get("items", [])
        if i.get("link")
    ]


def calendar_today():
    # Public open-source service with BS date, tithi and festival metadata.
    x = get_json("https://api-nepalicalendar.leapcell.app/today")
    if isinstance(x, dict):
        return x
    return None


def unique(items, key):
    seen = set()
    result = []
    for item in items:
        value = item.get(key)
        if value and value not in seen:
            seen.add(value)
            result.append(item)
    return result


def main():
    data = json.loads(OUT.read_text(encoding="utf-8"))
    data.setdefault("meta", {})

    wiki_sources = []
    for nepali, english in TOPICS.items():
        # Prefer Nepali Wikipedia; fall back to English when a Nepali article is absent.
        item = wikipedia("ne", nepali) or wikipedia("en", english)
        if item:
            item["topicNepali"] = nepali
            wiki_sources.append(item)
        time.sleep(0.2)

    google_results = []
    for query in SEARCH_TOPICS:
        google_results.extend(google_search(query))

    today = calendar_today()
    if today:
        data["panchang"] = {
            "today": today,
            "source": "Nepali Calendar API",
            "sourceUrl": "https://github.com/S4NKALP/nepali-calendar-api",
        }
        # Keep the UI useful even if the API changes field names.
        data["meta"]["todayNepali"] = today.get("dateNepali") or today.get("bs") or today.get("nepaliDate") or data["meta"].get("todayNepali", "")
        data["meta"]["tithi"] = today.get("tithi") or today.get("tithiNepali") or data["meta"].get("tithi", "")

    data["sources"] = unique(wiki_sources, "url")[:100]
    data["googleResults"] = unique(google_results, "url")[:100]
    data["meta"]["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    data["meta"]["sourceCount"] = len(data["sources"]) + len(data["googleResults"])
    data["meta"]["pipeline"] = "Wikipedia/Wikimedia + optional Google Search + Nepali calendar; source-attributed, non-destructive updates"

    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {OUT}: {data['meta']['sourceCount']} external sources")


if __name__ == "__main__":
    main()
