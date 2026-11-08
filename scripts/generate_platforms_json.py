#!/usr/bin/env python3
"""Regenerate data/platforms.json from the README category sections.

The README is the source of truth for platform names, URLs, categories,
and descriptions. The JSON used to be a hand-kept 15-entry seed (updated
2026-05-04) while the README grew to 100+ entries, so the two drifted.
This script rebuilds the JSON from the README so they stay in sync.

Rules:
  - Only the 14 platform category sections are parsed (from
    "Streaming & Listening Platforms" through "Open Source Music Projects").
  - One entry per platform name (case-insensitive); first occurrence wins.
  - The 15 originally hand-curated entries keep their curated `best_for`
    text and category (except Spotify, normalized to the README heading
    "Streaming & Listening Platforms"); new entries get `description`
    copied verbatim from the README instead of an invented `best_for`.
  - Entries are ordered by first appearance in the README.

Run from the repo root: python3 scripts/generate_platforms_json.py
Then verify with: python3 scripts/validate_repo.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
OUT = ROOT / "data" / "platforms.json"

FIRST_SECTION = "## Streaming & Listening Platforms"
LAST_SECTION = "## Open Source Music Projects"

ENTRY_RE = re.compile(r"^\s*-\s+\[([^\]]+)\]\((https?://[^)\s]+)\)\s*-\s*(.+?)\s*$")
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")

# Categories normalized to the README heading (categories.json uses these).
CATEGORY_NORMALIZE = {
    "Streaming & Listening": "Streaming & Listening Platforms",
}


def main():
    lines = README.read_text(encoding="utf-8").splitlines()
    in_range = False
    category = None
    entries = []  # (name, url, category, description) in README order
    for line in lines:
        m = HEADING_RE.match(line)
        if m:
            heading = m.group(1)
            if heading == FIRST_SECTION.lstrip("# "):
                in_range = True
            elif in_range and heading not in (
                "Streaming & Listening Platforms",
                "Independent Artist Platforms",
                "Music Distribution",
                "Sample Pack & Loop Marketplaces",
                "Beat Selling Platforms",
                "Music Licensing & Sync",
                "Promotion & Discovery",
                "Creator Storefronts",
                "Music Video & Short-Form Platforms",
                "Analytics & Artist Tools",
                "Music Communities",
                "Audio Plugin & Producer Resources",
                "Music Visualization Tools",
                "Open Source Music Projects",
            ):
                in_range = False
            category = heading if in_range else None
            continue
        if not in_range or category is None:
            continue
        em = ENTRY_RE.match(line)
        if em:
            name, url, desc = em.group(1), em.group(2), em.group(3)
            entries.append((name, url, category, desc))

    existing = {}
    if OUT.exists():
        old = json.loads(OUT.read_text(encoding="utf-8"))
        for p in old.get("platforms", []):
            existing[p["name"].lower()] = p

    seen = set()
    platforms = []
    for name, url, category, desc in entries:
        key = name.lower()
        if key in seen:
            continue
        seen.add(key)
        old = existing.get(key)
        if old is not None:
            entry = dict(old)
            entry["url"] = url
            entry["category"] = CATEGORY_NORMALIZE.get(
                old.get("category", category), old.get("category", category)
            )
            platforms.append(entry)
        else:
            platforms.append(
                {
                    "name": name,
                    "url": url,
                    "category": category,
                    "description": desc,
                }
            )

    data = {
        "schema": "awesome-music-platforms.platforms.v1",
        "updated": "2026-11-08",
        "generated_from": "README.md category sections via scripts/generate_platforms_json.py",
        "platforms": platforms,
    }
    OUT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(platforms)} platforms to {OUT.relative_to(ROOT)}")
    missing_old = [k for k in existing if k not in seen]
    if missing_old:
        print(f"NOTE: {len(missing_old)} previously-listed names not in README: {missing_old}")


if __name__ == "__main__":
    main()
