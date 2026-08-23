# हिन्दू सामग्री pipeline

यो directory repository को content ETL pipeline हो।

## Pipeline

1. `sync-scriptures.py` — upstream structured scripture data ल्याउँछ र repository मा shards बनाउँछ।
2. `build-content-index.py` — `data/**/*.json` बाट unified search index बनाउँछ।
3. `.github/workflows/validate-data.yml` — JSON र duplicate IDs जाँच्छ।
4. `.github/workflows/build-search-index.yml` — data change पछि search index rebuild गर्छ।

## Content policy

- मूल शास्त्रीय पाठलाई AI-generated text ले overwrite नगर्नु।
- Nepali meaning/explanation अलग field मा राख्नु।
- प्रत्येक imported corpus को source, edition, translator र license preserve गर्नु।
- फरक परम्पराका कथाहरूलाई एउटै निर्विवाद historical fact जस्तो नदेखाउनु।
- Image मा source/author/license metadata राख्नु।

## Planned corpus order

Gita → Mahabharata → Valmiki Ramayana → Vedas → Upanishads → Puranas → stories/entities cross-linking.
