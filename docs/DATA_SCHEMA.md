# Data Schema

The repo includes machine-readable data so future tools can generate pages, validate categories, or build a searchable frontend.

## `data/platforms.json`

Expected fields:

```json
{
  "name": "Bandcamp",
  "url": "https://bandcamp.com/",
  "category": "Creator Storefronts",
  "description": "Artist-first platform for selling music, merch, digital albums, vinyl, cassettes, and fan-supported releases.",
  "best_for": ["direct sales", "albums", "merch"],
  "pricing_model": "free/revenue-share/paid options vary",
  "tags": ["artist-storefront", "direct-sales"]
}
```

Not every existing entry has every field yet. The schema is intentionally forward-compatible.
