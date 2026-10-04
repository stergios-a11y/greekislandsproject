#!/usr/bin/env python3
"""Market data validator — run before every build (tools/build.py does).

Checks that a market pack is complete and consistent enough to build a site:
config, destinations, per-destination guides, clusters, homepage picks, theme.
ERRORS stop the build; WARNINGS are printed and the build continues.

    python3 tools/validate.py            # current market (MARKET env, default greece)
    python3 tools/validate.py --strict   # warnings count as errors
"""
import json
import math
import re
import sys

import market as M

ROOT = M.ROOT
errors, warnings = [], []
err = errors.append
warn = warnings.append

SCORE_DIMS = ('beach', 'hist', 'night', 'access', 'afford', 'car_need')
REQUIRED_BRAND = ('site_name', 'site_url', 'author', 'theme_color', 'logo', 'og_image', 'brand_words')
KNOWN_FEATURES = ('ferries', 'festivals', 'trip_cost', 'compare', 'itineraries', 'collections', 'match')
THEME_TOKENS = ('primary', 'primary-mid', 'primary-light', 'primary-pale', 'primary-dark',
                'surface', 'surface-2', 'surface-3', 'warm', 'warm-dark', 'warm-light', 'warm-pale',
                'highlight', 'secondary', 'ink', 'ink-1', 'ink-2', 'ink-3', 'ink-4', 'ink-5',
                'white', 'border', 'border-2', 'accent', 'font-ui', 'font-body', 'font-display')
FAR_KM = 60          # a stop further than this from its destination's centre is suspicious


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


# ---- market.json -------------------------------------------------------------------------
try:
    cfg = M.config()
except Exception as e:  # noqa: BLE001
    print(f'✗ markets/{M.MARKET}/market.json unreadable: {e}')
    sys.exit(1)

langs = cfg.get('languages') or []
if not langs:
    err('market.json: no languages')
codes = [l.get('code') for l in langs]
default = [l['code'] for l in langs if l.get('default')]
if len(default) != 1:
    err(f'market.json: exactly one default language needed, found {default or "none"}')
dl = default[0] if default else (codes[0] if codes else 'en')
for l in langs:
    for k in ('code', 'label', 'name'):
        if not l.get(k):
            err(f'market.json: language {l.get("code", "?")} missing "{k}"')
    if not l.get('default') and not l.get('prefix'):
        err(f'market.json: non-default language {l.get("code")} needs a URL "prefix" (e.g. "/el")')

brand = cfg.get('brand') or {}
for k in REQUIRED_BRAND:
    if not brand.get(k):
        err(f'market.json: brand.{k} missing')
if brand.get('site_url', '').endswith('/'):
    err('market.json: brand.site_url must not end with "/"')

feats = cfg.get('features') or {}
for k in feats:
    if k not in KNOWN_FEATURES:
        err(f'market.json: unknown feature "{k}" (known: {", ".join(KNOWN_FEATURES)})')

for section in ('nav', 'seo_nav', 'footer_links'):
    for item in cfg.get(section) or []:
        if dl not in (item.get('label') or {}):
            err(f'market.json: {section} item {item.get("href")} has no "{dl}" label')
        if item.get('feature') and item['feature'] not in KNOWN_FEATURES:
            err(f'market.json: {section} item {item.get("href")} has unknown feature "{item["feature"]}"')
for k, v in (cfg.get('strings') or {}).items():
    if dl not in v:
        err(f'market.json: strings.{k} has no "{dl}" text')

# ---- destinations ------------------------------------------------------------------------
dests = M.destinations()
if not dests:
    err('destinations.json: empty')
for key, d in dests.items():
    if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', key):
        err(f'destinations.json: key "{key}" must be lowercase-hyphenated (it becomes a URL)')
    if not d.get('name'):
        err(f'{key}: no name')
    if not (num(d.get('lat')) and num(d.get('lng')) and -90 <= d['lat'] <= 90 and -180 <= d['lng'] <= 180):
        err(f'{key}: lat/lng missing or out of range')
    for dim in SCORE_DIMS + ('total',):
        v = d.get(dim)
        if not num(v) or not 0 <= v <= 5:
            err(f'{key}: score "{dim}" must be a number 0–5 (got {v!r})')
    if not (isinstance(d.get('days'), int) and d['days'] >= 1):
        err(f'{key}: "days" must be a whole number ≥ 1')
    if not d.get('island_group'):
        warn(f'{key}: no island_group')

# ---- per-destination guides (islands/<key>.json) ---------------------------------------------
others = [c for c in codes if c != dl]
missing_tr = {c: 0 for c in others}
no_coords, far = [], []
for key, d in dests.items():
    p = ROOT / 'islands' / f'{key}.json'
    if not p.exists():
        err(f'{key}: guide islands/{key}.json missing')
        continue
    try:
        g = json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:  # noqa: BLE001
        err(f'islands/{key}.json: invalid JSON ({e})')
        continue
    if g.get('key') != key:
        err(f'islands/{key}.json: "key" is {g.get("key")!r}, expected {key!r}')
    for f in ('name', 'intro', 'itinerary'):
        if not g.get(f):
            err(f'islands/{key}.json: "{f}" missing')
    days = (g.get('itinerary') or {}).get('days') or []
    if not days:
        err(f'islands/{key}.json: itinerary has no days')
    months = (g.get('when_to_visit') or {}).get('months') or []
    if len(months) != 12:
        warn(f'{key}: when_to_visit needs 12 months (has {len(months)}) — month tags fall back to "ok"')
    centre = (d.get('lat'), d.get('lng'))
    points = [('stop', s) for day in days for s in day.get('stops', [])] + [('beach', b) for b in g.get('beaches') or []]
    for kind, s in points:
        if not s.get('name'):
            err(f'{key}: a {kind} has no name')
        if num(s.get('lat')) and num(s.get('lng')):
            dist = km(centre, (s['lat'], s['lng'])) if num(centre[0]) else 0
            if dist > FAR_KM:
                far.append(f'{key}: {kind} "{s.get("name")}" is {dist:.0f} km from the centre')
        else:
            no_coords.append(f'{key}: {kind} "{s.get("name")}"')
        for c in others:
            if s.get('desc') and not s.get(f'desc_{c}'):
                missing_tr[c] += 1
    for c in others:
        for f in ('name', 'intro', 'subtitle'):
            if g.get(f) and not g.get(f'{f}_{c}'):
                missing_tr[c] += 1
for x in no_coords:
    warn(f'no coordinates: {x}')
for x in far:
    warn(f'far from centre: {x}')
for c, n in missing_tr.items():
    if n:
        warn(f'{n} texts have no "{c}" translation')

# ---- clusters / home -----------------------------------------------------------------------
seen = {}
for ck, c in M.clusters().items():
    for k in c.get('members', []):
        if k not in dests:
            err(f'clusters.json: {ck} lists unknown destination "{k}"')
        if k in seen:
            err(f'clusters.json: "{k}" is in both {seen[k]} and {ck}')
        seen[k] = ck
h = M.home()
for f in h.get('featured', []):
    if f.get('key') not in dests:
        err(f'home.json: featured "{f.get("key")}" is not a destination')
for k in h.get('hero_keys', []):
    if k not in dests:
        err(f'home.json: hero key "{k}" is not a destination')

# ---- theme -----------------------------------------------------------------------------------
tp = M.MDIR / 'theme.css'
if not tp.exists():
    err(f'markets/{M.MARKET}/theme.css missing')
else:
    t = tp.read_text(encoding='utf-8')
    defined = set(re.findall(r'--([a-z][a-z0-9-]*)\s*:', t))
    for tok in THEME_TOKENS:
        if tok not in defined:
            err(f'theme.css: --{tok} not defined')
    if 'html.dark' not in t:
        warn('theme.css: no html.dark block — dark mode will reuse the light palette')
    css = (ROOT / 'style.css').read_text(encoding='utf-8')
    all_defined = set(re.findall(r'--([a-z][a-z0-9-]*)\s*:', css)) | defined
    undefined = sorted(set(re.findall(r'var\(--([a-z][a-z0-9-]*)', css)) - all_defined)
    if undefined:
        warn('style.css uses undefined tokens (fall back to browser defaults): ' + ', '.join('--' + u for u in undefined))

# ---- report ------------------------------------------------------------------------------------
strict = '--strict' in sys.argv
print(f'Validate market "{M.MARKET}": {len(dests)} destinations, languages {"/".join(codes)}')
SHOW = 25
for w in warnings[:SHOW]:
    print('  ⚠ ' + w)
if len(warnings) > SHOW:
    print(f'  ⚠ … and {len(warnings) - SHOW} more warnings')
for e in errors:
    print('  ✗ ' + e)
bad = errors or (strict and warnings)
print(('✗ FAILED' if bad else '✓ OK') + f' — {len(errors)} errors, {len(warnings)} warnings')
sys.exit(1 if bad else 0)
