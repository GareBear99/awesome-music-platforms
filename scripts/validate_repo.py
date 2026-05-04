#!/usr/bin/env python3
"""Local validation for Awesome Music Platforms."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

required_files = [
    "README.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "docs/KEYWORD_MAP.md",
    "docs/GITHUB_TOPICS.md",
    "docs/REPOSITORY_LAUNCH_CHECKLIST.md",
    "data/platforms.json",
    "data/categories.json",
    "data/seo_keywords.json",
    "scripts/check_links.py",
]

errors = []
for rel in required_files:
    if not (ROOT / rel).exists():
        errors.append(f"missing required file: {rel}")

text = README.read_text(encoding="utf-8")
required_phrases = [
    "music platforms for independent artists",
    "best music distribution platforms",
    "best platforms to sell beats",
    "best platforms to sell sample packs",
    "sync licensing",
    "GareBear99 Audio Discovery Network",
]
for phrase in required_phrases:
    if phrase.lower() not in text.lower():
        errors.append(f"README missing SEO phrase: {phrase}")

for data_file in ["platforms.json", "categories.json", "seo_keywords.json"]:
    path = ROOT / "data" / data_file
    if path.exists():
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid JSON {data_file}: {exc}")

# Flag common awesome-list anti-patterns.
if "ref=" in text or "utm_" in text:
    errors.append("README appears to contain tracking/referral parameters; keep links clean")

if errors:
    print("Validation failed:")
    for e in errors:
        print("-", e)
    sys.exit(1)

print("Validation passed: awesome-music-platforms SEO/public-facing package is coherent.")
