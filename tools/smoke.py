#!/usr/bin/env python3
"""Smoke test for the built site — one command, every page type.

    python3 tools/smoke.py              # static checks on every page in sitemap.xml (seconds)
    python3 tools/smoke.py --browser    # + loads one page of each type in a real browser

Static (no dependencies): every sitemap URL has a file; each page has a <title>, a meta
description, a canonical equal to its URL, a header and a footer (or the island SPA
skeleton); no unfilled template placeholders; JSON-LD parses; local CSS/JS it references
exist, and market-data.js / script.js / style.css versions match the homepage.

Browser (needs Playwright: pip3 install playwright && python3 -m playwright install chromium):
serves the folder on localhost, opens one page of every type at desktop and phone width,
and fails on any JavaScript error, a menu that doesn't open, or a page whose main feature
didn't render (island hydration, map markers, trip-cost estimate, compare cards, ferry
table, quiz). Analytics, ads and affiliate scripts are blocked so tests never count as visits.
"""
import argparse
import functools
import http.server
import json
import re
import sys
import threading
from collections import OrderedDict
from pathlib import Path
from urllib.parse import urlparse

import market as M

ROOT = M.ROOT
SITE = M.config()['brand']['site_url']
fails, notes = [], []


def fail(page, msg):
    fails.append(f'{page}: {msg}')


# ---------------------------------------------------------------- static
def sitemap_paths():
    xml = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
    return [urlparse(u).path for u in re.findall(r'<loc>([^<]+)</loc>', xml)]


def file_for(path):
    p = ROOT / path.lstrip('/')
    return p / 'index.html' if path.endswith('/') else p


def static_checks():
    idx = (ROOT / 'index.html').read_text(encoding='utf-8')
    want = {n: (re.search(n.replace('.', r'\.') + r'\?v=([0-9a-z]+)', idx) or [None, None])[1]
            for n in ('style.css', 'script.js', 'market-data.js')}
    paths = sitemap_paths()
    if not paths:
        fail('sitemap.xml', 'no URLs')
    seen = 0
    for path in paths:
        f = file_for(path)
        if not f.exists():
            fail(path, 'in sitemap but no file')
            continue
        seen += 1
        h = f.read_text(encoding='utf-8', errors='replace')
        if not re.search(r'<title>[^<]{5,}</title>', h):
            fail(path, 'no <title>')
        if not re.search(r'<meta name="description" content="[^"]{20,}"', h):
            fail(path, 'no meta description')
        can = re.search(r'<link rel="canonical" href="([^"]+)"', h)
        if not can:
            fail(path, 'no canonical')
        elif urlparse(can.group(1)).path != path:
            fail(path, f'canonical points elsewhere ({can.group(1)})')
        if not re.search(r'<header|class="seo-nav"', h):
            fail(path, 'no header')
        if not re.search(r'<footer|id="view-detail"', h):
            fail(path, 'no footer')
        left = re.findall(r'\{\{\s*\w+\s*\}\}|\{(?:lang_link|lang_label|privacy|privacy_label|credits|credits_label)\}', h)
        if left:
            fail(path, f'unfilled placeholders {sorted(set(left))[:3]}')
        for blob in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
            try:
                json.loads(blob)
            except ValueError:
                fail(path, 'JSON-LD does not parse')
        for name, v in want.items():
            for got in re.findall(name.replace('.', r'\.') + r'\?v=([0-9a-z]+)', h):
                if v and got != v:
                    fail(path, f'{name}?v={got}, homepage has v={v}')
        for ref in re.findall(r'(?:src|href)="(/[^"?#]+\.(?:css|js|json))(?:\?[^"]*)?"', h):
            if not (ROOT / ref.lstrip('/')).exists():
                fail(path, f'missing asset {ref}')
    return seen


# ---------------------------------------------------------------- browser
def page_type(path):
    """Group URLs by shape: language prefix stripped, destination keys and slugs → *."""
    for c in M.langs():
        pre = M.lang_prefix(c)
        if pre and path.startswith(pre + '/'):
            path = path[len(pre):]
            break
    segs = [s for s in path.strip('/').split('/') if s]
    return '/' + '/'.join(segs[:1] + ['*'] * (len(segs) - 1)) + ('/' if segs else '')


def samples():
    """One URL per page type per language, from the sitemap."""
    out = OrderedDict()
    for path in sitemap_paths():
        lang = next((c for c in M.langs() if M.lang_prefix(c) and path.startswith(M.lang_prefix(c) + '/')), M.default_lang())
        out.setdefault((page_type(path), lang), path)
    first = next(iter(M.destinations()))
    for k, path in out.items():
        if k[0] == '/trip-cost/':   # deep link like the island pages use, so an estimate shows at once
            out[k] = f'{path}?i={first}%3A3'
    return out


BLOCK = re.compile(r'googletagmanager|google-analytics|googlesyndication|doubleclick|emrldtp|tp-em|travelpayouts')

# feature checks: page type -> JS returning '' when fine, else a reason
FEATURE = {
    '/': """() => document.querySelectorAll('.leaflet-marker-icon, .leaflet-interactive, .island-marker').length ? '' : 'no map markers'""",
    '/island/*/': """() => { const d = document.getElementById('view-detail');
        return d && getComputedStyle(d).display !== 'none' && (document.getElementById('island-name')||{}).textContent ? '' : 'island page did not hydrate'; }""",
    '/trip-cost/': """() => /\\d/.test((document.getElementById('tc-stick-v')||{}).textContent||'') ? '' : 'no cost estimate'""",
    '/compare/*/': """() => (document.getElementById('compare-cards')||{children:[]}).children.length ? '' : 'no compare cards'""",
    '/ferries/': """() => document.querySelectorAll('.ferry-table tbody tr').length ? '' : 'no ferry rows'""",
    '/match/': """() => document.querySelector('a[href*="#match"]') ? '' : 'no quiz link'""",
}


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve():
    h = functools.partial(_Quiet, directory=str(ROOT))
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f'http://127.0.0.1:{srv.server_address[1]}'


def browser_checks(chromium_path=None):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('  Playwright not installed — run:  pip3 install playwright && python3 -m playwright install chromium')
        return False
    srv, base = serve()
    todo = samples()
    print(f'  browser: {len(todo)} page types × 2 widths')
    with sync_playwright() as pw:
        b = pw.chromium.launch(**({'executable_path': chromium_path} if chromium_path else {}))
        for (ptype, lang), path in todo.items():
            for w, h in ((1366, 900), (390, 844)):
                ctx = b.new_context(viewport={'width': w, 'height': h})
                p = ctx.new_page()
                errs = []
                p.on('pageerror', lambda e, errs=errs: errs.append(str(e).split('\n')[0]))
                p.route(BLOCK, lambda r: r.abort())
                label = f'{path} @{w}px'
                try:
                    p.goto(base + path, wait_until='load', timeout=30000)
                    p.wait_for_timeout(1300)
                except Exception as e:  # noqa: BLE001
                    fail(label, f'did not load ({str(e).splitlines()[0]})')
                    ctx.close()
                    continue
                for e in errs:
                    fail(label, f'JS error: {e}')
                if w < 800:
                    ok = p.evaluate("""() => { const b = document.getElementById('menu-toggle-btn'), n = document.getElementById('main-nav');
                        if (!b || !n || !b.offsetParent) return true; b.click(); return n.classList.contains('open'); }""")
                    if not ok:
                        fail(label, 'mobile menu does not open')
                elif ptype in FEATURE:
                    why = p.evaluate(FEATURE[ptype])
                    if why:
                        fail(label, why)
                ctx.close()
        b.close()
    srv.shutdown()
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--browser', action='store_true', help='also load one page of each type in Chromium')
    ap.add_argument('--chromium', help='path to a Chromium binary (optional)')
    a = ap.parse_args()
    print(f'Smoke test — market "{M.MARKET}"')
    n = static_checks()
    print(f'  static: {n} pages checked')
    if a.browser:
        browser_checks(a.chromium)
    for f in fails[:40]:
        print('  ✗ ' + f)
    if len(fails) > 40:
        print(f'  ✗ … and {len(fails) - 40} more')
    print(('✗ FAILED' if fails else '✓ OK') + f' — {len(fails)} problems')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
