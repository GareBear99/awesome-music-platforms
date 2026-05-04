#!/usr/bin/env python3
"""Simple markdown link checker for Awesome Music Platforms.

Default mode checks syntax and duplicate URLs without network access.
Use --online to make HTTP HEAD/GET requests where allowed.
"""
from pathlib import Path
import argparse, re, sys, urllib.request

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r'\[[^\]]+\]\((https?://[^\s)]+)\)')

def collect_links():
    links = []
    for path in ROOT.rglob('*.md'):
        if '.git' in path.parts:
            continue
        text = path.read_text(errors='ignore')
        for url in LINK_RE.findall(text):
            links.append((path.relative_to(ROOT), url))
    return links

def online_check(url):
    req = urllib.request.Request(url, method='HEAD', headers={'User-Agent':'awesome-music-platforms-link-check/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status < 400, str(r.status)
    except Exception as exc:
        try:
            req = urllib.request.Request(url, headers={'User-Agent':'awesome-music-platforms-link-check/1.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status < 400, str(r.status)
        except Exception as exc2:
            return False, str(exc2)[:160]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--online', action='store_true', help='perform live HTTP checks')
    args = parser.parse_args()
    links = collect_links()
    urls = [u for _, u in links]
    print(f'Found {len(links)} markdown links and {len(set(urls))} unique URLs.')
    duplicates = sorted({u for u in urls if urls.count(u) > 1})
    if duplicates:
        print(f'Duplicate URLs: {len(duplicates)}')
        for u in duplicates[:30]:
            print('  duplicate:', u)
    if args.online:
        failed = []
        for path, url in links:
            ok, info = online_check(url)
            print(('OK ' if ok else 'BAD'), info, path, url)
            if not ok:
                failed.append((path, url, info))
        if failed:
            print(f'Failed links: {len(failed)}')
            return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
