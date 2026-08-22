import json
import os
import time
from datetime import date
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "content.json"
DEITIES = ROOT / "data" / "deities.json"
UA = "HinduNepaliKnowledge/2.2 (GitHub Actions; public project)"
TIMEOUT = 20

TOPICS = {
    "भगवद्गीता": "Bhagavad_Gita", "महाभारत": "Mahabharata", "रामायण": "Ramayana",
    "वेद": "Vedas", "सरस्वती": "Saraswati", "पुराण": "Puranas", "उपनिषद्": "Upanishads",
    "कृष्ण": "Krishna", "राम": "Rama", "शिव": "Shiva", "विष्णु": "Vishnu",
    "गणेश": "Ganesha", "दुर्गा": "Durga", "हनुमान": "Hanuman", "लक्ष्मी": "Lakshmi",
    "पार्वती": "Parvati", "काली": "Kali", "ब्रह्मा": "Brahma", "इन्द्र": "Indra",
    "सूर्य": "Surya", "अग्नि": "Agni", "वायु": "Vayu", "वरुण": "Varuna",
}

SEARCH_TOPICS = [
    "वेद हिन्दू धर्म", "भगवद्गीता श्लोक अर्थ", "महाभारत कथा पात्र", "रामायण कथा पात्र",
    "१८ पुराण हिन्दू धर्म", "सरस्वती देवी कथा", "हिन्दू तिथि पर्व पञ्चाङ्ग", "हिन्दू मन्त्र स्तोत्र",
    "शैव वैष्णव शाक्त परम्परा", "हिन्दू देवी देवता कथा परम्परा",
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
    url = f"https://{language}.wikipedia.org/api/rest_v1/page/summary/{quote(title, safe='')}"
    x = get_json(url)
    if not x:
        return None
    page = x.get("content_urls", {}).get("desktop", {}).get("page")
    return {
        "topic": title, "language": language, "source": "Wikipedia",
        "title": x.get("title", title), "summary": x.get("extract", ""),
        "url": page or f"https://{language}.wikipedia.org/wiki/{quote(title)}",
        "license": "CC BY-SA (Wikipedia content; see source page)",
    }


def google_search(query):
    key, cx = os.getenv("GOOGLE_API_KEY"), os.getenv("GOOGLE_CSE_ID")
    if not key or not cx:
        return []
    x = get_json("https://www.googleapis.com/customsearch/v1", {
        "key": key, "cx": cx, "q": query, "num": 10, "safe": "active", "lr": "lang_ne"
    })
    if not x:
        return []
    return [{"title": i.get("title", ""), "url": i.get("link", ""),
             "snippet": i.get("snippet", ""), "query": query, "source": "Google Search"}
            for i in x.get("items", []) if i.get("link")]


def commons_image(query):
    """Find a Wikimedia Commons image and retain attribution metadata."""
    params = {
        "action": "query", "generator": "search", "gsrsearch": query,
        "gsrnamespace": 6, "gsrlimit": 5, "prop": "imageinfo",
        "iiprop": "url|extmetadata", "iiurlwidth": 900, "format": "json",
    }
    x = get_json("https://commons.wikimedia.org/w/api.php", params)
    pages = (x or {}).get("query", {}).get("pages", {})
    candidates = []
    for p in pages.values():
        info = (p.get("imageinfo") or [{}])[0]
        url = info.get("thumburl") or info.get("url")
        if not url:
            continue
        meta = info.get("extmetadata") or {}
        candidates.append({
            "image": url,
            "imagePage": "https://commons.wikimedia.org/wiki/" + quote(p.get("title", "").replace(" ", "_"), safe="_:/"),
            "imageLicense": (meta.get("LicenseShortName") or {}).get("value", ""),
            "imageArtist": (meta.get("Artist") or {}).get("value", ""),
        })
    return candidates[0] if candidates else None


def calendar_today():
    today = date.today()
    bs_year = today.year + (57 if today.month >= 4 else 56)
    yearly = get_json(f"https://api-nepalicalendar.leapcell.app/calendar/{bs_year}")
    if not isinstance(yearly, dict):
        return None
    month_names = ["बैशाख", "जेठ", "असार", "श्रावण", "भाद्र", "आश्विन", "कार्तिक", "मंसिर", "पौष", "माघ", "फाल्गुण", "चैत्र"]
    for month_key, payload in yearly.items():
        if not isinstance(payload, dict):
            continue
        metadata = payload.get("metadata", {})
        en_label = str(metadata.get("en", ""))
        if not any(token in en_label for token in [today.strftime("%b"), today.strftime("%B")]):
            continue
        for day in payload.get("days", []):
            if str(day.get("e", "")).zfill(2) == f"{today.day:02d}":
                bs_month = metadata.get("np") or month_names[int(month_key) - 1]
                return {"dateNepali": f"{bs_month} {day.get('n') or ''}, {bs_year}", "bsYear": bs_year,
                        "bsMonth": int(month_key), "bsDay": day.get("n") or "", "tithi": day.get("t", ""),
                        "festival": day.get("f", ""), "holiday": bool(day.get("h")), "adDate": today.isoformat()}
    return None


def unique(items, key):
    seen, result = set(), []
    for item in items:
        value = item.get(key)
        if value and value not in seen:
            seen.add(value)
            result.append(item)
    return result


def update_deity_images():
    if not DEITIES.exists():
        return 0
    items = json.loads(DEITIES.read_text(encoding="utf-8"))
    changed = 0
    for deity in items:
        query = deity.get("imageQuery") or (deity.get("name", "") + " Hindu deity")
        result = commons_image(query)
        if result:
            for key, value in result.items():
                if value:
                    deity[key] = value
            deity["imageSource"] = "Wikimedia Commons"
            changed += 1
        time.sleep(0.15)
    DEITIES.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def main():
    data = json.loads(OUT.read_text(encoding="utf-8"))
    data.setdefault("meta", {})

    wiki_sources = []
    for nepali, english in TOPICS.items():
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
        data["panchang"] = {"today": today, "source": "Nepali Calendar API", "sourceUrl": "https://github.com/S4NKALP/nepali-calendar-api"}
        data["meta"]["todayNepali"] = today["dateNepali"]
        data["meta"]["tithi"] = "तिथि: " + today.get("tithi", "") + (" · " + today["festival"] if today.get("festival") else "")

    image_count = update_deity_images()
    data["sources"] = unique(wiki_sources, "url")[:150]
    data["googleResults"] = unique(google_results, "url")[:150]
    data["meta"]["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    data["meta"]["sourceCount"] = len(data["sources"]) + len(data["googleResults"])
    data["meta"]["deityImagesUpdated"] = image_count
    data["meta"]["pipeline"] = "Wikipedia/Wikimedia + Wikimedia Commons images + optional Google discovery + Nepali Calendar dataset; source-attributed, non-destructive updates"
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {OUT}: {data['meta']['sourceCount']} sources; {image_count} deity images")


if __name__ == "__main__":
    main()
