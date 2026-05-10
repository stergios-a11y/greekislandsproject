#!/usr/bin/env python3
"""
Aegean Blueprint — SEO pre-render script
=========================================
Generates static HTML pages for every island so Google can index them
individually. The SPA still works on top of these pages: once the page
loads, JavaScript takes over and the user gets the full interactive
experience.

Output:
  /island/{key}/index.html       (English)
  /el/island/{key}/index.html    (Greek)

Run:
  python3 tools/prerender.py

The main index.html and the JSON files in /islands/ are the source of truth.
"""
import json
import os
from datetime import datetime, timezone

def bump_build_date():
    """Update the BUILD_DATE constant in script.js to today (UTC)."""
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    script_path = ROOT / 'script.js' if 'ROOT' in dir() else None
    # Resolve script.js path lazily — same dir as this script's parent
    script_path = (
        (globals().get('ROOT') or __file__.rsplit('/', 2)[0])
    )
    import re as _re
    from pathlib import Path as _Path
    sp = _Path(__file__).resolve().parent.parent / 'script.js'
    if not sp.exists():
        print('  [warn] script.js not found at expected path')
        return
    src = sp.read_text()
    new_src = _re.sub(
        r"const BUILD_DATE = '[^']*';",
        f"const BUILD_DATE = '{today}';",
        src,
        count=1,
    )
    if new_src != src:
        sp.write_text(new_src)
        print(f'✓ BUILD_DATE bumped to {today}')
    else:
        print('  [info] BUILD_DATE not changed (already current or marker missing)')

import re
import html
from pathlib import Path

ROOT = Path(__file__).parent.parent
ISLANDS_DIR = ROOT / 'islands'
OUT_EN = ROOT / 'island'
OUT_EL = ROOT / 'el' / 'island'
SITEMAP_PATH = ROOT / 'sitemap.xml'

SITE_URL = 'https://aegeanblueprint.com'
SITE_NAME = 'Aegean Blueprint'

# ---------------------------------------------------------------------
# Pull the Greek name map directly from i18n.js so we keep one source
# of truth. Not perfect but good enough — file is stable JS object.
# ---------------------------------------------------------------------
def load_greek_names():
    """Extract the ISLAND_NAMES_EL object from i18n.js."""
    text = (ROOT / 'i18n.js').read_text()
    # Find the object assignment
    m = re.search(r'const ISLAND_NAMES_EL\s*=\s*\{(.*?)^\};', text, re.DOTALL | re.MULTILINE)
    if not m:
        return {}
    body = m.group(1)
    names = {}
    # Each line can have multiple 'key': 'value' pairs (e.g. "'paros': 'Πάρος', 'milos': 'Μήλος'")
    for mm in re.finditer(r"'([a-z-]+)':\s*'([^']+)'", body):
        names[mm.group(1)] = mm.group(2)
    return names

GREEK_NAMES = load_greek_names()

# ---------------------------------------------------------------------
# Pull each island's group + stats from script.js's ISLANDS_DATA
# ---------------------------------------------------------------------
def load_island_meta():
    """Extract ISLANDS_DATA from script.js."""
    text = (ROOT / 'script.js').read_text()
    # Find the ISLANDS_DATA block
    start = text.index('const ISLANDS_DATA = {')
    end = text.index('\n};\n', start)
    block = text[start:end]
    islands = {}
    for line in block.split('\n'):
        m = re.match(r'\s*"([a-z-]+)":\s*\{\s*name:"([^"]+)"', line)
        if not m:
            continue
        key = m.group(1)
        name = m.group(2)
        # Parse numeric fields. Keep it simple; we only need group, total, days.
        def grab(field):
            mm = re.search(rf'{field}:\s*(-?[\d.]+)', line)
            return float(mm.group(1)) if mm else None
        islands[key] = {
            'name': name,
            'total': grab('total'),
            'beach': grab('beach'),
            'hist': grab('hist'),
            'night': grab('night'),
            'access': grab('access'),
            'afford': grab('afford'),
            'car_need': grab('car_need'),
            'days': grab('days'),
            'area': grab('area'),
            'pop': grab('pop'),
            'lat': grab('lat'),
            'lng': grab('lng'),
            'group': (re.search(r'island_group:\s*"([^"]+)"', line) or ['', ''])[1],
            'has_airport': 'has_airport:true' in line,
            'drama':   'drama:true' in line,
            'hiking':  'hiking:true' in line,
            'springs': 'springs:true' in line,
            'chora':   'chora:true' in line,
            'sailing': 'sailing:true' in line,
        }
    return islands

ISLAND_META = load_island_meta()

import math

def similar_island_distance(a, b):
    """Mirrors similarIslandDistance() in script.js — same weights and signals."""
    d = 0.0
    for f in ('beach', 'hist', 'night', 'access', 'afford'):
        d += abs((a.get(f) or 0) - (b.get(f) or 0)) / 5
    char_w = {'drama': 1.2, 'hiking': 0.8, 'springs': 1.0, 'chora': 1.1, 'sailing': 0.7}
    for f, w in char_w.items():
        if bool(a.get(f)) != bool(b.get(f)):
            d += w
    if bool(a.get('has_airport')) != bool(b.get('has_airport')):
        d += 0.4
    d += abs((a.get('car_need') or 3) - (b.get('car_need') or 3)) / 5 * 0.4
    if a.get('group') and a.get('group') == b.get('group'):
        d -= 1.2
    pa = max(a.get('pop') or 1, 1)
    pb = max(b.get('pop') or 1, 1)
    d += abs(math.log10(pa) - math.log10(pb)) * 0.4
    d += abs((a.get('days') or 3) - (b.get('days') or 3)) * 0.2
    return d

def find_similar_islands(key, count=4):
    target = ISLAND_META.get(key)
    if not target: return []
    scored = [(k, similar_island_distance(target, m)) for k, m in ISLAND_META.items() if k != key]
    scored.sort(key=lambda x: x[1])
    return [k for k, _ in scored[:count]]


GREEK_GROUPS = {
    'Cyclades': 'Κυκλάδες',
    'Dodecanese': 'Δωδεκάνησα',
    'Ionian': 'Ιόνιο',
    'Sporades': 'Σποράδες',
    'NE Aegean': 'Β.Α. Αιγαίο',
    'Saronic': 'Σαρωνικός',
    'Crete': 'Κρήτη',
}

# ---------------------------------------------------------------------
# HTML rendering helpers — pick language version of a field
# ---------------------------------------------------------------------
def pick(obj, field, lang='en'):
    """Return obj[field+'_el'] if lang='el' and available, else obj[field]."""
    if lang == 'el' and obj.get(f'{field}_el'):
        return obj[f'{field}_el']
    return obj.get(field, '')

def esc(s):
    """Escape HTML in a string for safe insertion."""
    return html.escape(str(s)) if s is not None else ''

def strip_html(s):
    """Strip HTML tags and decode entities. Used for places where structured
    data or meta needs plain text — e.g. JSON-LD `description`. Whitespace is
    collapsed."""
    if not s:
        return ''
    # Drop tags entirely
    text = re.sub(r'<[^>]+>', '', str(s))
    # Decode entities (&amp;, &nbsp;, etc.)
    text = html.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()

def truncate_at_word(s, limit):
    """Truncate at a word boundary, no trailing ellipsis. Used for JSON-LD
    description fields where Google has a length cap but we don't want a
    visible "..."."""
    if len(s) <= limit:
        return s
    cut = s[:limit].rsplit(' ', 1)[0]
    # Trim trailing punctuation that looks awkward mid-sentence
    return cut.rstrip(' ,;:—–-')

def safe_html(s):
    """Allow simple <a href="...">, <strong>, and <em> tags in descriptions,
    escape everything else. This lets island authors include real hyperlinks
    and emphasis inline without exposing them to XSS."""
    if s is None:
        return ''
    escaped = html.escape(str(s))
    # Restore <a href="..."> (href is the only allowed attribute)
    escaped = re.sub(
        r'&lt;a\s+href=(?:&quot;|")([^&"]+)(?:&quot;|")\s*(?:target=(?:&quot;|")_blank(?:&quot;|")\s*)?(?:rel=(?:&quot;|")[^&"]*(?:&quot;|")\s*)?&gt;',
        r'<a href="\1" target="_blank" rel="noopener noreferrer">',
        escaped
    )
    escaped = escaped.replace('&lt;/a&gt;', '</a>')
    # Restore <strong> and <em> as-is
    for tag in ('strong', 'em', 'b', 'i'):
        escaped = escaped.replace(f'&lt;{tag}&gt;', f'<{tag}>')
        escaped = escaped.replace(f'&lt;/{tag}&gt;', f'</{tag}>')
    return escaped

def localized_name(key, data, meta, lang='en'):
    """Return the display name for an island in the target language."""
    if lang == 'el' and key in GREEK_NAMES:
        return GREEK_NAMES[key]
    # JSON might have a name_el override
    if lang == 'el' and data.get('name_el'):
        return data['name_el']
    return data.get('name') or meta.get('name') or key.title()

# ---------------------------------------------------------------------
# When-to-visit section — mirrors buildWhenToVisitSection() in script.js.
# 12-month seasonality grid + summary paragraph. Each month has a tag
# (perfect/great/ok/avoid) and a short bilingual "why" caption.
# ---------------------------------------------------------------------
WTV_I18N = {
    'en': {
        'title': 'When to Visit',
        'months': ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
        'tags': {'perfect': 'Perfect', 'great': 'Great', 'ok': 'OK', 'avoid': 'Avoid'},
    },
    'el': {
        'title': 'Πότε να Πας',
        'months': ['Ιαν','Φεβ','Μάρ','Απρ','Μάι','Ιούν','Ιούλ','Αύγ','Σεπ','Οκτ','Νοέ','Δεκ'],
        'tags': {'perfect': 'Τέλεια', 'great': 'Καλά', 'ok': 'Μέτρια', 'avoid': 'Απόφυγε'},
    },
}

def build_when_to_visit_html(data, lang='en'):
    """Mirror script.js buildWhenToVisitSection. Empty string if missing.

    Renders an alternating-caption ribbon: 12 ribbon cells in a row, with
    captions above (odd months: Jan/Mar/May/Jul/Sep/Nov) and below
    (even months: Feb/Apr/Jun/Aug/Oct/Dec). Each caption spans 2 columns
    so it has ~100px horizontal room; tick marks (CSS pseudo-elements)
    point at the specific month each caption describes.

    Mobile users get a horizontal-scroll wrapper so the ribbon stays a
    continuous timeline rather than wrapping to two rows.
    """
    w = data.get('when_to_visit')
    if not w or not isinstance(w.get('months'), list) or len(w['months']) != 12:
        return ''

    labels = WTV_I18N[lang]
    above_caps = []
    below_caps = []
    ribbon_cells = []

    for i, m in enumerate(w['months']):
        tag = (m.get('tag') or 'ok').lower()
        why = pick(m, 'why', lang) or ''

        cap_class = ''
        if tag == 'perfect':
            cap_class = ' wtv-cap-peak'
        elif tag in ('avoid', 'ok'):
            cap_class = ' wtv-cap-muted'

        if i % 2 == 0:
            above_caps.append(f'<div class="wtv-cap-above{cap_class}"><span class="wtv-cap-text">{esc(why)}</span></div>')
        else:
            below_caps.append(f'<div class="wtv-cap-below{cap_class}"><span class="wtv-cap-text">{esc(why)}</span></div>')

        ribbon_cells.append(
            f'<div class="wtv-cell wtv-{esc(tag)}" title="{esc(why)}">'
            f'{esc(labels["months"][i])}</div>'
        )

    summary = pick(w, 'summary', lang) or ''
    summary_html = f'<p class="wtv-summary">{safe_html(summary)}</p>' if summary else ''

    tags_present = {(m.get('tag') or 'ok').lower() for m in w['months']}
    legend_order = ['perfect', 'great', 'ok', 'avoid']
    legend_items = ''.join(
        f'<span class="wtv-legend-item"><span class="wtv-legend-swatch wtv-{t}"></span>{esc(labels["tags"][t])}</span>'
        for t in legend_order if t in tags_present
    )

    ribbon_inner = ''.join(above_caps) + ''.join(ribbon_cells) + ''.join(below_caps)

    # Vertical layout for mobile — 12 rows, one per month
    vertical_rows = []
    for i, m in enumerate(w['months']):
        tag = (m.get('tag') or 'ok').lower()
        why = pick(m, 'why', lang) or ''
        vertical_rows.append(
            f'<div class="wtv-vrow wtv-v-{esc(tag)}">'
            f'<div class="wtv-vmonth">{esc(labels["months"][i])}</div>'
            f'<div class="wtv-vbar wtv-{esc(tag)}" title="{esc(labels["tags"].get(tag, ""))}"></div>'
            f'<div class="wtv-vwhy">{esc(why)}</div>'
            f'</div>'
        )
    vertical_inner = ''.join(vertical_rows)

    return (
        f'<details class="seo-wtv wtv-section" open>'
        f'<summary class="wtv-title">{esc(labels["title"])}</summary>'
        f'{summary_html}'
        f'<div class="wtv-ribbon-wrap"><div class="wtv-ribbon">{ribbon_inner}</div></div>'
        f'<div class="wtv-vertical">{vertical_inner}</div>'
        f'<div class="wtv-legend">{legend_items}</div>'
        f'</details>'
    )

# ---------------------------------------------------------------------
# Local & seasonal section — mirrors buildLocalSection() in script.js.
# Renders specialties / crafts / festivals that the SPA shows but Google
# previously didn't see. Each item supports an optional `image` field
# (80x80 thumbnail, served by Cloudinary URL transforms).
# ---------------------------------------------------------------------
LOCAL_I18N = {
    'en': {
        'section_title': 'Local & Seasonal',
        'specialties': 'Local Specialties',
        'crafts': 'Crafts & Souvenirs',
        'festivals': 'Festivals & Events',
    },
    'el': {
        'section_title': 'Τοπικά & Εποχιακά',
        'specialties': 'Τοπικά Προϊόντα',
        'crafts': 'Χειροτεχνία & Αναμνηστικά',
        'festivals': 'Πανηγύρια & Εκδηλώσεις',
    },
}

def build_local_html(data, lang='en'):
    """Mirror script.js buildLocalSection. Empty string if no local content."""
    specs = data.get('specialties') or []
    crafts = data.get('crafts') or []
    fests = data.get('festivals') or []
    if not specs and not crafts and not fests:
        return ''

    labels = LOCAL_I18N[lang]

    def render_item(item):
        name = pick(item, 'name', lang) or ''
        desc = pick(item, 'desc', lang) or ''
        when = pick(item, 'when', lang) or ''
        image = item.get('image') or ''
        when_html = f'<span class="seo-local-when">{esc(when)}</span>' if when else ''
        if image:
            image_html = (
                f'<img class="seo-local-image" src="{esc(image)}" '
                f'alt="{esc(name)}" loading="lazy" width="80" height="80">'
            )
            wrap_class = 'seo-local-item seo-local-item-with-image'
        else:
            image_html = ''
            wrap_class = 'seo-local-item'
        desc_html = f'<div class="seo-local-desc">{safe_html(desc)}</div>' if desc else ''
        return (
            f'<div class="{wrap_class}">'
            f'{image_html}'
            f'<div class="seo-local-text">'
            f'<div class="seo-local-name">{esc(name)}{when_html}</div>'
            f'{desc_html}'
            f'</div>'
            f'</div>'
        )

    def block(title, items, icon):
        if not items:
            return ''
        rendered = ''.join(render_item(it) for it in items)
        return (
            f'<div class="seo-local-block">'
            f'<h3 class="seo-local-heading">'
            f'<span class="seo-local-icon" aria-hidden="true">{icon}</span>'
            f'{esc(title)}</h3>'
            f'<div class="seo-local-items">{rendered}</div>'
            f'</div>'
        )

    inner = (
        block(labels['specialties'], specs, '🍽')
        + block(labels['crafts'], crafts, '🧵')
        + block(labels['festivals'], fests, '🎉')
    )
    return (
        f'<section class="seo-local">'
        f'<h2>{esc(labels["section_title"])}</h2>'
        f'{inner}'
        f'</section>'
    )

# ---------------------------------------------------------------------
# JSON-LD structured data — this is how we win rich snippets
# ---------------------------------------------------------------------
def find_hero_image(data):
    """Return (url, alt-source-name) for the first available photo in the island data,
    or (None, None) if no photo exists. Used as the prerendered SEO body hero image."""
    # Try itinerary stops first — they have higher-quality on-island photos
    for day in (data.get('itinerary') or {}).get('days') or []:
        for stop in day.get('stops') or []:
            if stop.get('photo'):
                return stop['photo'], stop.get('name', '')
    # Fall back to first beach photo
    for b in data.get('beaches') or []:
        if b.get('photo'):
            return b['photo'], b.get('name', '')
    return None, None


def gr_in(data):
    """Build the Greek 'στον/στην/στο/στους/στις/στα + accusative-name' phrase.

    Reads name_accusative_el and gender_el from the island JSON. Falls back to
    name_el (nominative) and feminine if either field is missing — better to
    produce slightly-wrong Greek than to crash.

    Genders: m | f | n | plm | plf | pln
    Articles: στον | στην | στο | στους | στις | στα

    For feminine accusative singular we always use 'στην' (the safe rule —
    final -ν is grammatically required before vowels and κ/π/τ/ξ/ψ/μπ/ντ/γκ
    and is optional but accepted elsewhere; "always στην" is what most modern
    Greek writing does and is never wrong).
    """
    acc = data.get('name_accusative_el') or data.get('name_el') or ''
    gender = data.get('gender_el') or 'f'
    article = {
        'm':   'στον',
        'f':   'στην',
        'n':   'στο',
        'plm': 'στους',
        'plf': 'στις',
        'pln': 'στα',
    }.get(gender, 'στην')
    return f'{article} {acc}'


def gr_subj(data):
    """Build the Greek nominative subject phrase: 'η Άνδρος', 'το Καστελλόριζο'…

    For Q5-style sentences where the island is the grammatical subject and we
    want a gender-neutral predicate that doesn't need adjective agreement.
    """
    name_el = data.get('name_el') or ''
    gender = data.get('gender_el') or 'f'
    article = {
        'm':   'ο',
        'f':   'η',
        'n':   'το',
        'plm': 'οι',
        'plf': 'οι',
        'pln': 'τα',
    }.get(gender, 'η')
    return f'{article} {name_el}'


def gr_is_plural(data):
    """True if the island's grammatical number is plural (Παξοί, Σπέτσες, Κουφονήσια…)."""
    return (data.get('gender_el') or '').startswith('pl')


def build_faq(key, data, meta, lang='en'):
    """Build a FAQPage JSON-LD object pulling from existing island data.

    Generates 3-5 Q&As that match real search queries:
    - When to visit (from WTV summary)
    - How long to stay (from days field)
    - How to get there (from getting_there summary)
    - Best beaches (from top beach names)
    - Suitability (from scores: hiking, families, nightlife, etc.)
    """
    name = localized_name(key, data, meta, lang)
    qas = []

    # Q1: When to visit
    wtv = data.get('when_to_visit') or {}
    wtv_summary = pick(wtv, 'summary', lang) or ''
    if wtv_summary:
        # Trim to first ~2 sentences for a focused answer
        first_sentences = re.split(r'(?<=[.!?])\s+', wtv_summary.strip())
        answer = ' '.join(first_sentences[:2])[:400]
        if lang == 'el':
            q = f'Πότε είναι η καλύτερη εποχή για επίσκεψη {gr_in(data)};'
        else:
            q = f'When is the best time to visit {name}?'
        qas.append((q, answer))

    # Q2: How long to stay
    days = meta.get('days')
    if days:
        days_int = int(days)
        if lang == 'el':
            q = f'Πόσες μέρες χρειάζομαι {gr_in(data)};'
            day_word = 'μέρα' if days_int == 1 else 'μέρες'
            a = f'Συνιστούμε {days_int} {day_word} για να δείτε τα κύρια αξιοθέατα χωρίς βιασύνη.'
        else:
            q = f'How many days do I need in {name}?'
            a = f'We suggest {days_int} days to cover the main highlights without rushing.'
        qas.append((q, a))

    # Q3: How to get there
    gt = data.get('getting_there') or {}
    gt_summary = pick(gt, 'summary', lang) or ''
    if gt_summary:
        first_sentences = re.split(r'(?<=[.!?])\s+', gt_summary.strip())
        answer = ' '.join(first_sentences[:2])[:400]
        if lang == 'el':
            q = f'Πώς πάω {gr_in(data)};'
        else:
            q = f'How do I get to {name}?'
        qas.append((q, answer))

    # Q4: Best beaches (only if at least 2 beaches in data)
    beaches = data.get('beaches') or []
    if len(beaches) >= 2:
        names = [pick(b, 'name', lang) or b.get('name', '') for b in beaches[:3] if b.get('name')]
        names = [n for n in names if n]
        if names:
            joined = ', '.join(names[:-1]) + (' and ' if lang == 'en' else ' και ') + names[-1] if len(names) > 1 else names[0]
            if lang == 'el':
                q = f'Ποιες είναι οι καλύτερες παραλίες {gr_in(data)};'
                a = f'Οι κορυφαίες παραλίες είναι {joined}.'
            else:
                q = f'What are the best beaches in {name}?'
                a = f'The top beaches are {joined}.'
            qas.append((q, a))

    # Q5: Suitability (one based on dominant character)
    if meta.get('hiking') and (meta.get('beach') or 0) >= 4:
        if lang == 'el':
            q = f'Έχει καλές διαδρομές πεζοπορίας {gr_in(data)};'
            verb = 'συνδυάζουν' if gr_is_plural(data) else 'συνδυάζει'
            a = f'Ναι — {gr_subj(data)} {verb} εξαιρετικές παραλίες με μονοπάτια και ορεινά τοπία.'
        else:
            q = f'Is {name} good for hiking?'
            a = f'Yes — {name} combines great beaches with serious hiking trails and mountain scenery.'
        qas.append((q, a))
    elif (meta.get('night') or 0) >= 4:
        if lang == 'el':
            q = f'Έχει νυχτερινή ζωή {gr_in(data)};'
            verb = 'έχουν' if gr_is_plural(data) else 'έχει'
            a = f'Ναι — {gr_subj(data)} {verb} σημαντική νυχτερινή ζωή, ιδίως τους καλοκαιρινούς μήνες.'
        else:
            q = f'Does {name} have nightlife?'
            a = f'Yes — {name} has a significant nightlife scene, especially in peak summer months.'
        qas.append((q, a))
    elif (meta.get('access') or 5) <= 2.5:
        if lang == 'el':
            q = f'Είναι δύσκολο να φτάσει κανείς {gr_in(data)};'
            subj = gr_subj(data)
            subj_cap = subj[:1].upper() + subj[1:]  # "η Άνδρος" -> "Η Άνδρος"
            verb = 'βρίσκονται' if gr_is_plural(data) else 'βρίσκεται'
            a = f'{subj_cap} {verb} σχετικά μακριά — λιγότερα δρομολόγια και λιγότεροι τουρίστες.'
        else:
            q = f'Is {name} hard to reach?'
            a = f'{name} is relatively remote — fewer ferries, fewer tourists, and a quieter feel.'
        qas.append((q, a))

    if not qas:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in qas
        ],
    }


def build_structured_data(key, data, meta, lang='en'):
    """
    Build a list of JSON-LD objects for Google.
    We emit:
      - TouristDestination (the island)
      - TouristTrip (the itinerary)
      - BreadcrumbList
      - FAQPage (if we had FAQs; skip for now)
    """
    url = f'{SITE_URL}/island/{key}/' if lang == 'en' else f'{SITE_URL}/el/island/{key}/'
    name = localized_name(key, data, meta, lang)
    intro = pick(data, 'intro', lang) or ''
    # Clean intro to plain text — strip HTML, collapse whitespace.
    # JSON-LD descriptions must be plain text; raw HTML (e.g. embedded <a> tags
    # in the intro) breaks the structured data when the slice cuts mid-tag.
    intro_plain = strip_html(intro)

    destination = {
        "@context": "https://schema.org",
        "@type": "TouristDestination",
        "name": name,
        "description": truncate_at_word(intro_plain, 500),
        "url": url,
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": meta.get('lat'),
            "longitude": meta.get('lng'),
        },
        "containedInPlace": {
            "@type": "Country",
            "name": "Greece"
        },
    }
    # NOTE: aggregateRating is NOT valid on TouristDestination per schema.org.
    # Google Search Console flags it as "Invalid object type for field <parent_node>".
    # Our internal dimension scores (beach/culture/nightlife/etc) aren't real reviews
    # anyway, so Google would discount them. Removed to keep the schema clean.

    # Itinerary → TouristTrip
    trip = None
    if 'itinerary' in data and data['itinerary'].get('days'):
        days = data['itinerary']['days']
        itinerary_list = []
        for day in days:
            day_title = pick(day, 'title', lang)
            itinerary_list.append({
                "@type": "ListItem",
                "position": day.get('day', 1),
                "item": {
                    "@type": "TouristAttraction",
                    "name": f"Day {day.get('day', 1)}: {day_title}",
                }
            })
        trip = {
            "@context": "https://schema.org",
            "@type": "TouristTrip",
            "name": f"{len(days)}-day {name} itinerary",
            "description": pick(data.get('itinerary', {}), 'subtitle', lang) or truncate_at_word(intro_plain, 200),
            "itinerary": {
                "@type": "ItemList",
                "numberOfItems": len(itinerary_list),
                "itemListElement": itinerary_list,
            },
            "touristType": "leisure",
        }

    # Breadcrumb — two levels (Home → Island). The "group" mid-level was removed
    # because it pointed at the same URL as Home, which broke Google's breadcrumb
    # validation ("Invalid object type for field <parent_node>").
    breadcrumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1,
             "name": "Home" if lang == 'en' else 'Αρχική',
             "item": SITE_URL + ('/' if lang == 'en' else '/el/')},
            {"@type": "ListItem", "position": 2, "name": name, "item": url},
        ],
    }

    out = [destination, breadcrumbs]
    if trip:
        out.append(trip)
    faq = build_faq(key, data, meta, lang)
    if faq:
        out.append(faq)
    return out

# ---------------------------------------------------------------------
# Meta tags
# ---------------------------------------------------------------------
def build_title(key, data, meta, lang='en'):
    """Unique, keyword-rich page title."""
    name = localized_name(key, data, meta, lang)
    days = int(meta.get('days') or 0) if meta.get('days') else 0
    if lang == 'el':
        if days:
            return f"{name} — Οδηγός {days} ημερών, παραλίες, δρομολόγιο | Aegean Blueprint"
        return f"{name} — Ταξιδιωτικός οδηγός | Aegean Blueprint"
    else:
        if days:
            return f"{name} Travel Guide — {days}-Day Itinerary, Beaches & What to Do | Aegean Blueprint"
        return f"{name} Travel Guide — What to Do, Where to Stay | Aegean Blueprint"

def build_description(key, data, meta, lang='en'):
    """Build a meta description targeting ~110-160 chars.

    Strategy:
      1. Add complete sentences until adding another would exceed 160 chars.
      2. If we're still under 110 (lots of unused space) AND there's a next
         sentence we didn't include, add a word-boundary-truncated prefix of it
         with an ellipsis. Better to use SERP real estate than leave it blank.
      3. Special edge: if the first sentence alone is over 160, soft-truncate it.
    """
    TARGET_MIN = 110
    TARGET_MAX = 160

    intro = pick(data, 'intro', lang) or ''
    clean = re.sub(r'\s+', ' ', intro).strip()
    sentences = re.split(r'(?<=[.!?])\s+', clean)
    if not sentences:
        return clean[:TARGET_MAX]

    # Step 1: fit complete sentences
    out = ''
    consumed_count = 0
    for s in sentences:
        candidate = (out + ' ' + s).strip() if out else s
        if len(candidate) <= TARGET_MAX:
            out = candidate
            consumed_count += 1
        else:
            break

    # Step 3 (handle first): if the first sentence alone is too long
    if not out:
        first = sentences[0]
        out = first[:TARGET_MAX - 1].rsplit(' ', 1)[0] + '…'
        return out

    # Step 2: if we have room and another sentence exists, add a truncated prefix
    if len(out) < TARGET_MIN and consumed_count < len(sentences):
        extra = sentences[consumed_count]
        room = TARGET_MAX - len(out) - 1   # joining space
        if room > 30:                       # only worth it if we can add something meaningful
            if len(extra) <= room:
                out = (out + ' ' + extra).strip()
            else:
                snippet = extra[:room - 1].rsplit(' ', 1)[0]
                out = (out + ' ' + snippet + '…').strip()

    return out

# ---------------------------------------------------------------------
# Pre-rendered body content — this is what Google crawls
# ---------------------------------------------------------------------
def auto_link_islands(html_text, current_key, lang='en'):
    """Find mentions of OTHER island names in prose text and convert to internal links.
    Rules:
      - Only link the first occurrence per page (avoids spammy repeated links)
      - Never self-link (skip the current island)
      - Skip mentions already inside <a> tags
      - Skip mentions inside HTML attributes (alt="...", title="...")
      - Use word boundaries — won't match "Naxos" inside "Naxosomething"
    Returns the HTML with links added.
    """
    if not html_text:
        return html_text

    # Build (canonical-key, display-name) list, sorted by name LENGTH desc so
    # longer names match before shorter substrings (e.g. "Agios Efstratios"
    # before "Agios" if there were such collision).
    candidates = []
    for k, m in ISLAND_META.items():
        if k == current_key:
            continue
        # Get the display name in the right language
        if lang == 'el':
            name = GREEK_NAMES.get(k, m.get('name', ''))
        else:
            name = m.get('name', '')
        if not name:
            continue
        # Skip names that are common nouns or sub-string traps. None in our set
        # currently — all 78 island names are distinctive — but worth filtering
        # in future if we add e.g. "Crete" which appears as both an island and a region.
        candidates.append((k, name))

    candidates.sort(key=lambda x: -len(x[1]))

    # Track which keys we've already linked so each destination gets at most ONE link
    linked = set()
    href_prefix = '/island/' if lang == 'en' else '/el/island/'

    # We want to skip text inside existing tags. Approach: split by tag boundaries,
    # only process the text-content segments. This is simpler than a full HTML parser.
    parts = re.split(r'(<[^>]+>)', html_text)
    # Track whether we are currently inside an <a>...</a>
    inside_a = False
    out_parts = []
    for part in parts:
        if part.startswith('<'):
            # It's a tag — track <a>/</a> state
            tag_lower = part.lower()
            if tag_lower.startswith('<a ') or tag_lower == '<a>':
                inside_a = True
            elif tag_lower == '</a>':
                inside_a = False
            out_parts.append(part)
            continue

        if inside_a:
            # Don't link inside existing anchors
            out_parts.append(part)
            continue

        # Process this text segment — try each unlinked candidate
        new_part = part
        for k, name in candidates:
            if k in linked:
                continue
            # Word-boundary match, case-sensitive (island names are proper nouns)
            pattern = r'\b' + re.escape(name) + r'\b'
            m = re.search(pattern, new_part)
            if m:
                # Replace ONLY the first occurrence
                start, end = m.span()
                href = f'{href_prefix}{k}/'
                link_html = f'<a href="{href}">{name}</a>'
                new_part = new_part[:start] + link_html + new_part[end:]
                linked.add(k)
        out_parts.append(new_part)

    return ''.join(out_parts)


def render_body(key, data, meta, lang='en'):
    """The visible, crawlable HTML for the island."""
    name = localized_name(key, data, meta, lang)
    intro = pick(data, 'intro', lang) or ''
    subtitle = pick(data.get('itinerary', {}), 'subtitle', lang) or ''
    days_count = len(data.get('itinerary', {}).get('days', []))
    beaches = data.get('beaches', [])

    # Rating block
    rating = meta.get('total')
    rating_text = ''
    if rating:
        if lang == 'el':
            rating_text = f'<p class="seo-rating">Συνολική βαθμολογία: <strong>{rating:.1f}/5</strong> · {int(meta["area"]) if meta.get("area") else ""} km² · {int(meta["pop"]) if meta.get("pop") else ""} κάτοικοι</p>'
        else:
            rating_text = f'<p class="seo-rating">Overall rating: <strong>{rating:.1f}/5</strong> · {int(meta["area"]) if meta.get("area") else ""} km² · {int(meta["pop"]) if meta.get("pop") else ""} residents</p>'

    # Getting-there section (between intro and itinerary) — v2 schema: pills + summary + tip
    getting_there_html = ''
    gt = data.get('getting_there')
    if gt and gt.get('pills'):
        gt_label = 'Getting there' if lang == 'en' else 'Πώς θα φτάσεις'
        tip_label = 'Tip' if lang == 'en' else 'Συμβουλή'

        pills = gt.get('pills_el' if lang == 'el' else 'pills', [])
        summary = gt.get('summary_el' if lang == 'el' else 'summary', '')
        tip = gt.get('tip_el' if lang == 'el' else 'tip')

        pill_html = ''
        if pills:
            pill_spans = ''.join(f'<span class="seo-gt-pill">{esc(p)}</span>' for p in pills)
            pill_html = f'<div class="seo-gt-pills">{pill_spans}</div>'

        summary_html = f'<p class="seo-gt-summary">{esc(summary)}</p>' if summary else ''
        tip_html = f'<p class="seo-gt-tip"><strong>{tip_label}:</strong> {esc(tip)}</p>' if tip else ''

        if pill_html or summary_html:
            getting_there_html = (
                f'<section class="seo-getting-there">'
                f'<h2>{gt_label}</h2>'
                f'{pill_html}'
                f'{summary_html}'
                f'{tip_html}'
                f'</section>'
            )

    # Itinerary section
    itinerary_html = ''
    if days_count:
        heading = f'{days_count}-day itinerary for {name}' if lang == 'en' else f'Δρομολόγιο {days_count} ημερών — {name}'
        day_blocks = []
        for day in data['itinerary']['days']:
            day_num = day.get('day', 1)
            day_title = esc(pick(day, 'title', lang))
            overnight = esc(pick(day, 'overnight', lang))
            km = day.get('km', '')
            drive_mins = day.get('drive_mins', '')
            stops = day.get('stops', [])

            stop_items = []
            for s in stops:
                sname = esc(pick(s, 'name', lang))
                sdesc = safe_html(pick(s, 'desc', lang))
                stime = esc(s.get('time', ''))
                stop_items.append(f'<li><strong>{stime} · {sname}</strong><br>{sdesc}</li>')

            overnight_label = 'Overnight' if lang == 'en' else 'Διανυκτέρευση'
            drive_label = 'Drive' if lang == 'en' else 'Οδήγηση'
            day_label = 'Day' if lang == 'en' else 'Μέρα'

            meta_parts = []
            if overnight:
                meta_parts.append(f'{overnight_label}: <strong>{overnight}</strong>')
            if km not in (None, '', 0) and drive_mins not in (None, '', 0):
                meta_parts.append(f'{drive_label}: {km} km, ~{drive_mins} min')
            meta_line_html = f'<p class="seo-day-meta">{" · ".join(meta_parts)}</p>' if meta_parts else ''

            day_blocks.append(f'''
<section class="seo-day">
  <h3>{day_label} {day_num}: {day_title}</h3>
  {meta_line_html}
  <ol class="seo-stops">
    {"".join(stop_items)}
  </ol>
</section>''')

        itinerary_html = f'<section class="seo-itinerary"><h2>{heading}</h2>{"".join(day_blocks)}</section>'

    # Beaches section
    beaches_html = ''
    if beaches:
        heading = f'Top beaches of {name}' if lang == 'en' else f'Κορυφαίες παραλίες — {name}'
        beach_blocks = []
        for b in beaches:
            bname = esc(pick(b, 'name', lang))
            bdesc = safe_html(pick(b, 'desc', lang))
            btype = esc(pick(b, 'type', lang))
            blen = esc(pick(b, 'length', lang))
            bdepth = esc(pick(b, 'depth', lang))
            bfacing = esc(pick(b, 'facing', lang))
            bfac = esc(pick(b, 'facilities', lang))
            beach_blocks.append(f'''
<article class="seo-beach">
  <h3>{bname}</h3>
  <p>{bdesc}</p>
  <dl>
    <dt>{'Type' if lang=='en' else 'Τύπος'}</dt><dd>{btype}</dd>
    <dt>{'Length' if lang=='en' else 'Μήκος'}</dt><dd>{blen}</dd>
    <dt>{'Depth' if lang=='en' else 'Βάθος'}</dt><dd>{bdepth}</dd>
    <dt>{'Facing' if lang=='en' else 'Προσανατολισμός'}</dt><dd>{bfacing}</dd>
    <dt>{'Facilities' if lang=='en' else 'Υποδομές'}</dt><dd>{bfac}</dd>
  </dl>
</article>''')
        beaches_html = f'<section class="seo-beaches"><h2>{heading}</h2>{"".join(beach_blocks)}</section>'

    # Local & seasonal — specialties / crafts / festivals (only renders if any present)
    local_html = build_local_html(data, lang)

    # When-to-visit — 12-month seasonality grid (only renders if data.when_to_visit present)
    wtv_html = build_when_to_visit_html(data, lang)

    # Similar islands — character-aware similarity (mirrors script.js findSimilarIslands)
    related = find_similar_islands(key, count=4)
    related_links = []
    for rk in related:
        rname = GREEK_NAMES.get(rk, ISLAND_META[rk]['name']) if lang == 'el' else ISLAND_META[rk]['name']
        href = f'/el/island/{rk}/' if lang == 'el' else f'/island/{rk}/'
        related_links.append(f'<a href="{href}">{esc(rname)}</a>')
    related_heading = 'Islands like this one' if lang == 'en' else 'Παρόμοια νησιά'
    related_html = ''
    if related_links:
        related_html = f'<section class="seo-related"><h2>{related_heading}</h2><p>{" · ".join(related_links)}</p></section>'

    # Compose full body
    subtitle_html = f'<p class="seo-subtitle">{esc(subtitle)}</p>' if subtitle else ''

    # Hero image — first available photo from itinerary stops or beaches
    hero_url, hero_subject = find_hero_image(data)
    hero_html = ''
    if hero_url:
        if lang == 'el':
            alt = f'{name} — {hero_subject}' if hero_subject else f'{name}, ελληνικό νησί'
        else:
            alt = f'{name} — {hero_subject}' if hero_subject else f'{name}, Greek island'
        hero_html = (
            f'<figure class="seo-hero">'
            f'<img src="{esc(hero_url)}" alt="{esc(alt)}" loading="lazy" '
            f'width="800" height="500" style="width:100%;height:auto;border-radius:8px">'
            f'</figure>'
        )

    body_html = f'''
<article class="seo-island-content">
  <div class="seo-header">
    <h1>{esc(name)}</h1>
    {subtitle_html}
    {rating_text}
  </div>
  {hero_html}
  <section class="seo-intro">
    <p>{safe_html(intro)}</p>
  </section>
  {getting_there_html}
  {wtv_html}
  {itinerary_html}
  {beaches_html}
  {local_html}
  {related_html}
</article>'''

    # Post-process: auto-link mentions of OTHER island names to their pages.
    # Done as a final pass so it works across all sections (intro, GT summary,
    # WTV summary, captions). One link per destination island per page.
    return auto_link_islands(body_html, key, lang)

# ---------------------------------------------------------------------
# Page shell
# ---------------------------------------------------------------------
def render_page(key, data, meta, lang='en'):
    """Full HTML document for one island."""
    name = localized_name(key, data, meta, lang)
    title = build_title(key, data, meta, lang)
    description = build_description(key, data, meta, lang)
    url = f'{SITE_URL}/island/{key}/' if lang == 'en' else f'{SITE_URL}/el/island/{key}/'
    url_en = f'{SITE_URL}/island/{key}/'
    url_el = f'{SITE_URL}/el/island/{key}/'
    body = render_body(key, data, meta, lang)
    schema = build_structured_data(key, data, meta, lang)
    schema_json = json.dumps(schema, ensure_ascii=False, separators=(',', ':'))

    # Base path for loading CSS/JS/logos — relative to site root.
    # Since these pages are deeper in the tree, we need absolute paths.
    base = '/' if lang == 'en' else '/el/'
    # Assets live at root for en and /el/* for greek-versioned copies? No — we use root.
    asset_prefix = '/'  # both languages reference root-level assets

    html_lang = lang
    og_locale = 'en_US' if lang == 'en' else 'el_GR'
    alt_lang = 'el' if lang == 'en' else 'en'
    alt_url = url_el if lang == 'en' else url_en

    # Modified date — from the underlying JSON file's mtime, so per-island freshness
    # is reflected in the article:modified_time meta (used by Google for E-E-A-T).
    modified_date = file_lastmod(ISLANDS_DIR / f'{key}.json')

    return f'''<!DOCTYPE html>
<html lang="{html_lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="theme-color" content="#0B8FAC">
<meta name="author" content="Stergios Gousios">
<meta property="article:author" content="Stergios Gousios">
<meta property="article:modified_time" content="{modified_date}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{url_en}">
<link rel="alternate" hreflang="el" href="{url_el}">
<link rel="alternate" hreflang="x-default" href="{url_en}">
<link rel="icon" href="{asset_prefix}favicon.ico" sizes="any">
<link rel="icon" href="{asset_prefix}favicon.svg" type="image/svg+xml">
<link rel="icon" type="image/png" sizes="32x32" href="{asset_prefix}favicon-32.png">
<link rel="icon" type="image/png" sizes="96x96" href="{asset_prefix}favicon-96.png">
<link rel="icon" type="image/png" sizes="16x16" href="{asset_prefix}favicon-16.png">
<link rel="apple-touch-icon" href="{asset_prefix}apple-touch-icon.png">
<meta name="apple-mobile-web-app-title" content="Aegean Blueprint">
<link rel="manifest" href="{asset_prefix}site.webmanifest">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/og/{key}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:locale" content="{og_locale}">
<meta property="og:locale:alternate" content="{('el_GR' if lang=='en' else 'en_US')}">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{SITE_URL}/og/{key}.jpg">

<!-- Structured data -->
<script type="application/ld+json">{schema_json}</script>

<!-- SPA assets — load the same CSS as the main site so the SEO body blends visually -->
<link rel="stylesheet" href="{asset_prefix}style.css?v=24">
<style>
  /* Minimal SEO body styling — these elements exist only in pre-rendered pages */
  .seo-island-content {{
    max-width: 900px; margin: 40px auto; padding: 24px;
    font-family: var(--sans, sans-serif); color: var(--ink-1, #111);
    line-height: 1.65;
  }}
  .seo-island-content h1 {{
    font-family: var(--display, serif); font-size: var(--text-hero, 32px); margin: 0 0 6px;
  }}
  .seo-subtitle {{ color: var(--ink-3, #555); font-style: italic; margin: 0 0 12px; }}
  .seo-rating {{ color: var(--ink-2, #333); font-size: var(--text-small, 14px); }}
  .seo-intro p {{ font-size: var(--text-sub, 18px); }}
  .seo-hero {{ margin: 16px 0 24px; }}
  .seo-hero img {{ display: block; box-shadow: 0 2px 12px rgba(0,0,0,0.10); }}
  .seo-itinerary, .seo-beaches, .seo-related, .seo-getting-there, .seo-local {{ margin-top: 36px; }}
  .seo-itinerary h2, .seo-beaches h2, .seo-related h2, .seo-getting-there h2, .seo-local h2 {{
    font-family: var(--display, serif); font-size: var(--text-section, 24px); margin: 0 0 16px;
    border-bottom: 2px solid var(--aegean, #0B8FAC); padding-bottom: 6px;
  }}
  .seo-gt-pills {{
    display: flex; flex-wrap: wrap; gap: 6px; margin: 0 0 12px;
  }}
  .seo-gt-pill {{
    background: rgba(11,143,172,0.08);
    color: var(--aegean, #0B8FAC);
    font-size: var(--text-tiny, 12px);
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 12px;
    white-space: nowrap;
  }}
  .seo-gt-summary {{
    margin: 0 0 10px;
    font-size: var(--text-small, 14px);
    color: var(--ink-2, #333);
    line-height: 1.6;
  }}
  .seo-gt-tip {{
    margin: 0;
    padding: 8px 12px;
    background: rgba(11,143,172,0.04);
    border-left: 3px solid var(--aegean, #0B8FAC);
    border-radius: 0 4px 4px 0;
    font-size: var(--text-small, 14px);
    color: var(--ink-2, #333);
    font-style: italic;
    line-height: 1.5;
  }}
  .seo-gt-tip strong {{ font-style: normal; color: var(--aegean, #0B8FAC); }}
  .seo-day {{ margin-bottom: 24px; }}
  .seo-day h3 {{ font-size: var(--text-sub, 18px); margin: 0 0 4px; }}
  .seo-day-meta {{ color: var(--ink-3, #555); font-size: var(--text-meta, 13px); margin: 0 0 10px; }}
  .seo-stops {{ padding-left: 20px; }}
  .seo-stops li {{ margin-bottom: 10px; font-size: var(--text-body, 16px); }}
  .seo-beach {{
    margin: 0 -24px;
    padding: 18px 24px;
    background: rgba(11,143,172,0.05);
    border-top: 1px solid rgba(11,143,172,0.12);
  }}
  .seo-beach:last-of-type {{ border-bottom: 1px solid rgba(11,143,172,0.12); }}
  .seo-beach h3 {{ margin: 0 0 8px; font-size: var(--text-sub, 18px); }}
  .seo-beach p {{ margin: 0 0 12px; }}
  .seo-beach dl {{ display: grid; grid-template-columns: 120px 1fr; gap: 4px 12px; font-size: var(--text-meta, 13px); margin: 0; }}
  .seo-beach dt {{ font-weight: 600; color: var(--ink-3, #555); }}
  .seo-beach dd {{ margin: 0; }}
  .seo-local-block {{ margin-bottom: 24px; }}
  .seo-local-heading {{
    font-family: var(--display, serif); font-size: var(--text-sub, 18px); margin: 0 0 10px;
    color: var(--ink-1, #222);
  }}
  .seo-local-icon {{ margin-right: 6px; }}
  .seo-local-items {{ display: flex; flex-direction: column; gap: 12px; }}
  .seo-local-item {{
    display: flex; gap: 12px; align-items: flex-start;
    padding: 10px 0;
  }}
  .seo-local-item + .seo-local-item {{ border-top: 1px solid rgba(11,143,172,0.10); }}
  .seo-local-image {{
    width: 80px; height: 80px; flex: 0 0 80px;
    border-radius: 6px; object-fit: cover;
  }}
  .seo-local-text {{ flex: 1; min-width: 0; }}
  .seo-local-name {{
    font-weight: 600; font-size: var(--text-body, 16px); margin: 0 0 4px;
    color: var(--ink-1, #222);
  }}
  .seo-local-when {{
    margin-left: 8px; font-weight: 400;
    color: var(--ink-3, #555); font-size: var(--text-meta, 13px);
  }}
  .seo-local-desc {{
    font-size: var(--text-small, 14px); color: var(--ink-2, #333);
    line-height: 1.5; margin: 0;
  }}
  .seo-related a {{ color: var(--aegean, #0B8FAC); text-decoration: none; font-weight: 600; margin: 0 2px; }}
  .seo-related a:hover {{ text-decoration: underline; }}

  /* Top nav */
  .seo-nav {{
    max-width: 1100px; margin: 0 auto; padding: 16px 24px;
    display: flex; justify-content: space-between; align-items: center;
    font-family: var(--sans, sans-serif); border-bottom: 1px solid #e5e5e5;
  }}
  .seo-nav-brand {{
    display: flex; align-items: center; gap: 10px;
    text-decoration: none; color: #111; font-weight: 700; font-size: var(--text-sub, 18px);
  }}
  .seo-nav-links {{ display: flex; gap: 20px; }}
  .seo-nav-links a {{
    color: #0B8FAC; text-decoration: none; font-weight: 600; font-size: var(--text-small, 14px);
  }}
  .seo-nav-links a:hover {{ text-decoration: underline; }}
  @media (max-width: 600px) {{
    .seo-nav {{ flex-direction: column; gap: 12px; }}
    .seo-nav-links {{ gap: 14px; font-size: var(--text-meta, 13px); }}
  }}

  /* CTA box */
  .seo-cta-box {{
    max-width: 900px; margin: 40px auto; padding: 28px 24px;
    background: linear-gradient(135deg, rgba(11,143,172,0.08), rgba(11,143,172,0.02));
    border-radius: 14px; text-align: center; font-family: var(--sans, sans-serif);
  }}
  .seo-cta-box h3 {{ font-family: var(--display, serif); font-size: var(--text-section, 24px); margin: 0 0 8px; color: #111; }}
  .seo-cta-box p {{ color: #555; margin: 0 0 20px; }}
  .seo-cta-buttons {{ display: flex; gap: 12px; flex-wrap: wrap; justify-content: center; }}
  .seo-cta-btn {{
    display: inline-block; padding: 12px 20px; background: #0B8FAC; color: #fff;
    text-decoration: none; border-radius: 10px; font-weight: 600; font-size: var(--text-small, 14px);
    transition: transform 0.15s;
  }}
  .seo-cta-btn:hover {{ transform: translateY(-2px); color: #fff; text-decoration: none; }}

  /* Footer */
  .seo-footer {{
    max-width: 900px; margin: 40px auto 20px; padding: 20px 24px;
    border-top: 1px solid #e5e5e5; text-align: center;
    color: #777; font-size: var(--text-meta, 13px); font-family: var(--sans, sans-serif);
  }}
  .seo-footer a {{ color: #0B8FAC; text-decoration: none; }}
  .seo-footer p {{ margin: 4px 0; }}
</style>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9298260273942245" crossorigin="anonymous"></script>
<script>
  /* Desktop-only ads: suppress on viewports below 900px. */
  (function(){{
    if (window.matchMedia('(max-width: 899.98px)').matches) {{
      window.adsbygoogle = window.adsbygoogle || [];
      window.adsbygoogle.push = function(){{}};
    }}
  }})();
</script>
</head>
<body data-island-key="{key}" data-lang="{lang}">

<!-- Top navigation bar -->
<nav class="seo-nav">
  <a href="{('/' if lang == 'en' else '/el/')}" class="seo-nav-brand">
    <img src="{asset_prefix}logo.png" alt="Aegean Blueprint" width="36" height="36">
    <span>Aegean Blueprint</span>
  </a>
  <div class="seo-nav-links">
    <a href="{('/' if lang == 'en' else '/el/')}">{'Map' if lang == 'en' else 'Χάρτης'}</a>
    <a href="{('/' if lang == 'en' else '/el/')}#data">{'All Islands' if lang == 'en' else 'Όλα τα Νησιά'}</a>
    <a href="{('/' if lang == 'en' else '/el/')}#compare">{'Compare' if lang == 'en' else 'Σύγκριση'}</a>
    <a href="{('/' if lang == 'en' else '/el/')}#match">{'Quiz' if lang == 'en' else 'Quiz'}</a>
  </div>
</nav>

<!-- Pre-rendered content -->
{body}

<!-- Call-to-action to get users into the interactive SPA -->
<div class="seo-cta-box">
  <h3>{'Want to compare islands or take the matching quiz?' if lang == 'en' else 'Θέλεις να συγκρίνεις νησιά ή να κάνεις το quiz;'}</h3>
  <p>{'Our interactive tools help you filter, compare side-by-side, and find the perfect island for your trip.' if lang == 'en' else 'Τα διαδραστικά μας εργαλεία σε βοηθούν να φιλτράρεις, να συγκρίνεις και να βρεις το ιδανικό νησί.'}</p>
  <div class="seo-cta-buttons">
    <a href="{('/' if lang == 'en' else '/el/')}#compare" class="seo-cta-btn">{'↔ Compare islands' if lang == 'en' else '↔ Σύγκρινε νησιά'}</a>
    <a href="{('/' if lang == 'en' else '/el/')}#match" class="seo-cta-btn">{'🎯 Take the quiz' if lang == 'en' else '🎯 Κάνε το quiz'}</a>
    <a href="{('/' if lang == 'en' else '/el/')}" class="seo-cta-btn">{'🗺 Explore map' if lang == 'en' else '🗺 Εξερεύνησε χάρτη'}</a>
  </div>
</div>

<!-- Footer -->
<footer class="seo-footer">
  <p>© 2026 {'Stergios Gousios · Aegean Blueprint' if lang == 'en' else 'Στέργιος Γούσιος · Aegean Blueprint'}</p>
  <p><a href="{('/el/island/' if lang == 'en' else '/island/')}{key}/">{'Ελληνικά' if lang == 'en' else 'English'}</a> · <a href="{'/privacy/' if lang == 'en' else '/el/privacy/'}">{'Privacy' if lang == 'en' else 'Απόρρητο'}</a></p>
</footer>

<!--
  Self-contained SEO page. The rich content above is the canonical version
  of this island guide — meant to rank in Google. Users who want the
  interactive map, comparison tool, or quiz can click through to the SPA.
  No JS redirect, no DOM surgery — just a clean page.
-->
<script>
// Track that someone viewed this page (same GA as main site)
(function() {{
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=G-FMFWLRM2J9';
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  function gtag(){{ dataLayer.push(arguments); }}
  gtag('js', new Date());
  gtag('config', 'G-FMFWLRM2J9');
}})();
</script>

</body>
</html>
'''

# ---------------------------------------------------------------------
# Main generation loop
# ---------------------------------------------------------------------
def main():
    OUT_EN.mkdir(parents=True, exist_ok=True)
    OUT_EL.mkdir(parents=True, exist_ok=True)

    # Bump BUILD_DATE in script.js so the "Last updated" footer stamp is fresh
    bump_build_date()

    count = 0
    keys = []
    for jf in sorted(ISLANDS_DIR.glob('*.json')):
        if jf.stem == 'TEMPLATE':
            continue
        key = jf.stem
        if key not in ISLAND_META:
            print(f'  [skip] {key} — not in ISLANDS_DATA')
            continue
        data = json.loads(jf.read_text())
        meta = ISLAND_META[key]
        keys.append(key)

        # English
        en_page = render_page(key, data, meta, lang='en')
        out_dir = OUT_EN / key
        out_dir.mkdir(exist_ok=True)
        (out_dir / 'index.html').write_text(en_page)

        # Greek
        el_page = render_page(key, data, meta, lang='el')
        out_dir_el = OUT_EL / key
        out_dir_el.mkdir(exist_ok=True)
        (out_dir_el / 'index.html').write_text(el_page)

        count += 1

    print(f'✓ Generated {count} islands × 2 languages = {count*2} pages')

    # Regenerate sitemap with clean URLs
    generate_sitemap(keys)
    print(f'✓ Sitemap regenerated with {len(keys)} islands + static pages')

    # Build the compact "what's on now" index for the home page strip
    generate_whats_on_index(keys)
    print(f'✓ whats-on.json regenerated')

    # Build the festivals calendar page (static HTML, EN + EL)
    n_fests = generate_festivals_page(keys)
    print(f'✓ festivals/ page regenerated ({n_fests} festivals)')

    # Inject (or refresh) the static SEO island list at the bottom of each
    # homepage. Without this, the SPA's island links are JS-rendered and
    # Google's crawler can't easily discover them — pages get stuck in
    # "Discovered – currently not indexed" for weeks.
    n_inject = inject_homepage_seo_links(keys)
    print(f'✓ Homepage SEO link blocks updated ({n_inject} islands × 2 languages)')

def inject_homepage_seo_links(island_keys):
    """Inject (or refresh) a static <nav> of every island page into both homepages.

    Why: the homepage SPA renders its island links via JavaScript only. Google
    crawls JS but slowly, and PageRank flows poorly through JS-only links.
    A visually-hidden static <nav> with all 78 island URLs lets the crawler
    discover and index every page on the first HTML pass.

    The block is bounded by HTML comment markers so prerender can safely
    overwrite it on every run. Hand-edits between the markers will be lost
    on the next prerender — edit content elsewhere, or change this function.

    The 'visually-hidden' class clips content off-screen but keeps it in the
    accessibility tree and crawlable. This is the standard 'sr-only' pattern
    (used by GitHub, MDN, etc.); Google does not penalize it.

    Returns count of islands listed (per language).
    """
    START = '<!-- SEO_ISLAND_LIST_START -->'
    END   = '<!-- SEO_ISLAND_LIST_END -->'

    def build_block(lang):
        """Build the <nav> fragment for the given language."""
        # Pull each island's display name in the right language. Sort by the
        # display name (so Greek pages list alphabetically in Greek).
        items = []
        for key in island_keys:
            jf = ISLANDS_DIR / f'{key}.json'
            try:
                data = json.loads(jf.read_text(encoding='utf-8'))
            except Exception:
                continue
            display = data.get('name_el' if lang == 'el' else 'name', key)
            href = f'/el/island/{key}/' if lang == 'el' else f'/island/{key}/'
            items.append((display, href))
        items.sort(key=lambda x: x[0].lower())

        if lang == 'el':
            heading = 'Όλα τα νησιά'
        else:
            heading = 'All islands'

        lines = [START]
        lines.append(f'<nav class="visually-hidden" aria-label="{esc(heading)}">')
        lines.append(f'  <h2>{esc(heading)}</h2>')
        lines.append('  <ul>')
        for display, href in items:
            lines.append(f'    <li><a href="{href}">{esc(display)}</a></li>')
        lines.append('  </ul>')
        lines.append('</nav>')
        lines.append(END)
        return '\n'.join(lines)

    def upsert(path, lang):
        """Insert the block, or replace existing one between markers."""
        text = path.read_text(encoding='utf-8')
        block = build_block(lang)
        if START in text and END in text:
            # Replace existing
            pre  = text.split(START, 1)[0]
            post = text.split(END, 1)[1]
            new  = pre + block + post
        else:
            # First-time insert: place just before </body>
            if '</body>' not in text:
                print(f'  [skip] {path}: no </body> tag found')
                return
            new = text.replace('</body>', block + '\n</body>', 1)
        if new != text:
            path.write_text(new, encoding='utf-8')

    upsert(ROOT / 'index.html', 'en')
    upsert(ROOT / 'el' / 'index.html', 'el')
    return len(island_keys)


def generate_festivals_page(island_keys):
    """Build a 12-month festival calendar page (EN + EL) at /festivals/index.html.
    Static HTML — festivals don't change often, and the page is a real SEO surface
    for queries like 'greek island festivals 2027' or 'panigiri august'.
    """
    # Collect all festivals across islands
    all_fests = []
    for key in island_keys:
        json_path = ISLANDS_DIR / f'{key}.json'
        try:
            d = json.loads(json_path.read_text())
        except Exception:
            continue
        for fest in (d.get('festivals') or []):
            if not isinstance(fest, dict): continue
            months = sorted(parse_when_to_months(fest.get('when', '')))
            all_fests.append({
                'island': key,
                'name': fest.get('name', ''),
                'name_el': fest.get('name_el') or fest.get('name', ''),
                'when': fest.get('when', ''),
                'when_el': fest.get('when_el') or fest.get('when', ''),
                'desc': fest.get('desc', ''),
                'desc_el': fest.get('desc_el') or fest.get('desc', ''),
                'photo': fest.get('photo', ''),
                'months': months,
                'sort_key': months[0] if months else 13,
            })

    all_fests.sort(key=lambda f: (f['sort_key'], f['name']))

    MONTH_NAMES_EN = ['January','February','March','April','May','June','July',
                      'August','September','October','November','December']
    MONTH_NAMES_EL = ['Ιανουάριος','Φεβρουάριος','Μάρτιος','Απρίλιος','Μάιος','Ιούνιος','Ιούλιος',
                      'Αύγουστος','Σεπτέμβριος','Οκτώβριος','Νοέμβριος','Δεκέμβριος']

    for lang in ['en', 'el']:
        is_el = (lang == 'el')
        month_names = MONTH_NAMES_EL if is_el else MONTH_NAMES_EN
        if is_el:
            title = 'Γιορτές & Πανηγύρια Νησιών — αναλυτικό ημερολόγιο | Aegean Blueprint'
            intro = ('Θρησκευτικές γιορτές, πανηγύρια και παραδοσιακές εκδηλώσεις σε όλα τα 78 ελληνικά νησιά. '
                     'Για τις κινητές γιορτές, οι ημερομηνίες είναι ρυθμισμένες για το 2027. '
                     'Το ημερολόγιο είναι ο καλύτερος τρόπος να σχεδιάσεις ταξίδι γύρω από κάτι συγκεκριμένο.')
            # Self-contained meta description (≤160 chars). Don't slice `intro` —
            # it's body copy and slicing truncates mid-sentence.
            meta_desc = ('Θρησκευτικές γιορτές και πανηγύρια σε όλα τα 78 ελληνικά νησιά. '
                         'Κινητές ημερομηνίες ρυθμισμένες για το 2027. Σχεδίασε το ταξίδι σου γύρω από κάτι αυθεντικό.')
            h1 = 'Γιορτές & Πανηγύρια — Ημερολόγιο'
        else:
            title = 'Greek Island Festivals — full calendar | Aegean Blueprint'
            intro = ('Religious feasts, panigiria, and traditional celebrations across all 78 Greek islands. '
                     'Dates pinned to 2027 where movable. The calendar is the single best way to plan a trip '
                     'around something specific — most of these festivals are the deepest-rooted experiences '
                     'an island offers.')
            # Self-contained meta description (≤160 chars).
            meta_desc = ('Religious feasts and panigiria across all 78 Greek islands. Movable dates pinned to 2027. '
                         'The calendar is the deepest way to plan a trip.')
            h1 = 'Greek Island Festivals — full calendar'

        url = f'{SITE_URL}/' + ('el/' if is_el else '') + 'festivals/'

        # Build month sections
        month_blocks = []
        for m in range(1, 13):
            # Show each festival only in its EARLIEST month — multi-month festivals
            # (e.g. Apokries spanning Feb-Mar) used to appear twice. Now they appear
            # in their first month only, with their date string showing the full span.
            month_fests = [f for f in all_fests if f['months'] and f['months'][0] == m]
            if not month_fests:
                continue
            heading = month_names[m - 1]
            cards = []
            for f in month_fests:
                if is_el:
                    island_name = GREEK_NAMES.get(f['island'], ISLAND_META.get(f['island'], {}).get('name', f['island']))
                else:
                    island_name = ISLAND_META.get(f['island'], {}).get('name', f['island'])
                island_href = '/' + ('el/' if is_el else '') + 'island/' + f['island'] + '/'
                fest_name = f['name_el'] if is_el else f['name']
                when_text = f['when_el'] if is_el else f['when']
                desc_text = f['desc_el'] if is_el else f['desc']

                photo_html = ''
                if f.get('photo'):
                    photo_html = '<img class="fest-photo" src="' + esc(f['photo']) + '" alt="' + esc(fest_name) + '" loading="lazy">'

                card_html = (
                    '<article class="fest-card">'
                    + photo_html
                    + '<div class="fest-text">'
                    + '<a class="fest-island" href="' + island_href + '">' + esc(island_name) + '</a>'
                    + '<h3 class="fest-name">' + esc(fest_name) + '</h3>'
                    + '<p class="fest-when">' + esc(when_text) + '</p>'
                    + '<p class="fest-desc">' + esc(desc_text) + '</p>'
                    + '</div></article>'
                )
                cards.append(card_html)

            section_html = (
                '<section class="fest-month" id="month-' + str(m) + '">'
                + '<h2 class="fest-month-heading">' + heading
                + ' <span class="fest-month-count">(' + str(len(month_fests)) + ')</span></h2>'
                + '<div class="fest-cards">' + ''.join(cards) + '</div>'
                + '</section>'
            )
            month_blocks.append(section_html)

        # Quick-jump links — count matches the earliest-month-only display logic
        nav_links = []
        for m in range(1, 13):
            count = sum(1 for f in all_fests if f['months'] and f['months'][0] == m)
            if count > 0:
                short_name = month_names[m - 1][:3]
                nav_links.append('<a href="#month-' + str(m) + '">' + short_name + ' (' + str(count) + ')</a>')
        nav_html = ' · '.join(nav_links)

        page_html = (
            '<!DOCTYPE html>\n<html lang="' + lang + '">\n<head>\n'
            '<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            '<title>' + esc(title) + '</title>\n'
            '<meta name="description" content="' + esc(meta_desc) + '">\n'
            '<meta name="theme-color" content="#0B8FAC">\n'
            '<meta name="author" content="Stergios Gousios">\n'
            '<link rel="canonical" href="' + url + '">\n'
            '<link rel="alternate" hreflang="en" href="' + SITE_URL + '/festivals/">\n'
            '<link rel="alternate" hreflang="el" href="' + SITE_URL + '/el/festivals/">\n'
            '<link rel="alternate" hreflang="x-default" href="' + SITE_URL + '/festivals/">\n'
            '<link rel="icon" href="/favicon.ico" sizes="any">\n'
            '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
            '<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">\n'
            '<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png">\n'
            '<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">\n'
            '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
            '<meta name="apple-mobile-web-app-title" content="Aegean Blueprint">\n'
            '<link rel="manifest" href="/site.webmanifest">\n'
            '<meta property="og:type" content="website">\n'
            '<meta property="og:title" content="' + esc(title) + '">\n'
            '<meta property="og:description" content="' + esc(meta_desc) + '">\n'
            '<meta property="og:url" content="' + url + '">\n'
            '<meta property="og:locale" content="' + ('el_GR' if is_el else 'en_US') + '">\n'
            # Apply dark mode preference from localStorage BEFORE stylesheet loads.
            # Otherwise users who enabled dark mode on the home page would briefly
            # flash the light theme on this page. Tiny inline script — no JS file needed.
            '<script>if(localStorage.getItem("darkMode")==="true"){document.documentElement.classList.add("dark");}</script>\n'
            '<link rel="stylesheet" href="/style.css">\n'
            '<style>\n'
            '  body { background: var(--bg, #fff); color: var(--ink, #222); font-family: var(--sans, system-ui), sans-serif; margin: 0; }\n'
            '  .fest-page { max-width: 1100px; margin: 0 auto; padding: 32px 24px 64px; }\n'
            '  .fest-page > h1 { font-family: var(--serif, Georgia), serif; font-size: 36px; margin: 0 0 8px; }\n'
            '  .fest-intro { font-size: 17px; color: var(--ink-1, #444); line-height: 1.5; margin: 0 0 24px; max-width: 720px; }\n'
            '  .fest-nav { background: var(--marble, #f6f4ee); padding: 12px 16px; border-radius: 12px; font-size: 14px; margin-bottom: 32px; }\n'
            '  .fest-nav a { color: var(--aegean-dark, #076880); text-decoration: none; font-weight: 600; }\n'
            '  .fest-nav a:hover { text-decoration: underline; }\n'
            '  .fest-month { margin-bottom: 40px; }\n'
            '  .fest-month-heading { font-family: var(--serif, Georgia), serif; font-size: 26px; margin: 0 0 16px; padding-bottom: 6px; border-bottom: 2px solid var(--aegean, #0B8FAC); }\n'
            '  .fest-month-count { color: var(--ink-3, #888); font-weight: 400; font-size: 16px; }\n'
            '  .fest-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }\n'
            '  .fest-card { display: flex; gap: 14px; padding: 16px; background: var(--white, #fff); border: 1px solid var(--border, #e5e1d8); border-radius: 12px; }\n'
            '  .fest-photo { width: 96px; height: 96px; object-fit: cover; border-radius: 8px; flex-shrink: 0; }\n'
            '  .fest-text { flex: 1; min-width: 0; }\n'
            '  .fest-island { font-size: 13px; font-weight: 600; color: var(--aegean-dark, #076880); text-decoration: none; text-transform: uppercase; letter-spacing: 0.5px; }\n'
            '  .fest-island:hover { text-decoration: underline; }\n'
            '  .fest-name { font-family: var(--serif, Georgia), serif; font-size: 18px; margin: 4px 0; line-height: 1.25; }\n'
            '  .fest-when { font-size: 13px; color: var(--accent, #FF6B6B); font-weight: 600; margin: 0 0 8px; }\n'
            '  .fest-desc { font-size: 14px; color: var(--ink-1, #555); line-height: 1.5; margin: 0; }\n'
            '  @media (max-width: 600px) {\n'
            '    .fest-page { padding: 20px 16px 48px; }\n'
            '    .fest-page > h1 { font-size: 28px; }\n'
            '    .fest-card { flex-direction: column; }\n'
            '    .fest-photo { width: 100%; height: 160px; }\n'
            '  }\n'
            '  html.dark body { background: #1a1a1a; color: #eee; }\n'
            '  html.dark .fest-card { background: #2a2a2a; border-color: #444; }\n'
            '  html.dark .fest-nav { background: #333; }\n'
            '</style>\n'
            '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9298260273942245" crossorigin="anonymous"></script>\n'
            '<script>\n'
            '  /* Desktop-only ads: suppress on viewports below 900px. */\n'
            '  (function(){\n'
            '    if (window.matchMedia(\'(max-width: 899.98px)\').matches) {\n'
            '      window.adsbygoogle = window.adsbygoogle || [];\n'
            '      window.adsbygoogle.push = function(){};\n'
            '    }\n'
            '  })();\n'
            '</script>\n'
            '</head>\n<body>\n'
            # Match the main-site header exactly. Same classes, same CSS in style.css.
            # Difference: nav links go to /index.html#hash so they switch SPA view on
            # the home page, festivals link is real (active here), language toggle is
            # a single tappable EN/EL link rather than the SPA dropdown (no JS available).
            '<header>\n'
            '  <div class="header-content">\n'
            '    <a class="logo-wrapper" href="/' + ('el/' if is_el else '') + '" style="text-decoration: none;">\n'
            '      <img src="/logo-hero.svg" id="site-logo" alt="Aegean Blueprint logo">\n'
            '      <span id="brand-text"><span class="brand-word">Aegean</span> <span class="brand-word">Blueprint</span></span>\n'
            '    </a>\n'
            # Hamburger — needed for mobile, since style.css hides .top-nav under 860px.
            # Without it the nav disappears with no way to open it. JS handler below.
            '    <div class="menu-toggle" id="menu-toggle-btn"><span></span><span></span><span></span></div>\n'
            '    <nav class="top-nav" id="main-nav">\n'
            '      <a href="/' + ('el/' if is_el else '') + '">' + ('Χάρτης' if is_el else 'Map') + '</a>\n'
            '      <a href="/' + ('el/' if is_el else '') + '#data">' + ('Στοιχεία Νησιών' if is_el else 'Islands Data') + '</a>\n'
            '      <a href="/' + ('el/' if is_el else '') + '#compare">' + ('Σύγκριση' if is_el else 'Compare') + '</a>\n'
            '      <a href="/' + ('el/' if is_el else '') + 'festivals/" class="active">' + ('Γιορτές' if is_el else 'Festivals') + '</a>\n'
            '      <a href="/' + ('el/' if is_el else '') + '#hopping">' + ('Νησοπορία' if is_el else 'Island Hopping') + '</a>\n'
            '      <a href="/' + ('el/' if is_el else '') + '#international">' + ('Διεθνώς' if is_el else 'International') + '</a>\n'
            '      <a href="/' + ('el/' if is_el else '') + '#match">' + ('Βρες το Νησί σου' if is_el else 'Match Me') + '</a>\n'
            '      <a href="/' + ('el/' if is_el else '') + '#shortlist">' + ('⭐ Η Λίστα μου' if is_el else '⭐ My Shortlist') + '</a>\n'
            '      <a href="/' + ('el/' if is_el else '') + '#mission">' + ('Στόχος' if is_el else 'Mission') + '</a>\n'
            '      <a href="' + ('/el/privacy/' if is_el else '/privacy/') + '" class="nav-utility">' + ('Απόρρητο' if is_el else 'Privacy') + '</a>\n'
            '    </nav>\n'
            '    <a class="lang-toggle-static" href="' + ('/festivals/' if is_el else '/el/festivals/') + '" style="background: none; border: 1px solid rgba(255,255,255,0.4); color: #fff; padding: 4px 10px; border-radius: 4px; text-decoration: none; font-size: 13px; white-space: nowrap;">'
            '<span style="margin-right: 4px;">🌐</span>' + ('EN' if is_el else 'EL') + '</a>\n'
            '  </div>\n'
            '</header>\n'
            # Tiny inline script to wire the hamburger. Mirrors the toggleMenu() function
            # in script.js so the festivals page works without loading the full SPA bundle.
            '<script>\n'
            '  (function(){\n'
            '    var btn = document.getElementById("menu-toggle-btn");\n'
            '    var nav = document.getElementById("main-nav");\n'
            '    if (btn && nav) {\n'
            '      btn.addEventListener("click", function(){\n'
            '        nav.classList.toggle("open");\n'
            '        btn.classList.toggle("open");\n'
            '      });\n'
            '    }\n'
            '  })();\n'
            '</script>\n'
            '<main class="fest-page">\n'
            '  <h1>' + h1 + '</h1>\n'
            '  <p class="fest-intro">' + esc(intro) + '</p>\n'
            '  <nav class="fest-nav">' + nav_html + '</nav>\n'
            '  ' + ''.join(month_blocks) + '\n'
            '</main>\n'
            '<footer style="text-align:center;padding:24px 16px;font-size:13px;color:#888;border-top:1px solid #e5e5e5;margin-top:40px;">\n'
            '  <p style="margin:4px 0;">© 2026 ' + ('Στέργιος Γούσιος · Aegean Blueprint' if is_el else 'Stergios Gousios · Aegean Blueprint') + '</p>\n'
            '  <p style="margin:4px 0;"><a href="' + ('/el/privacy/' if is_el else '/privacy/') + '" style="color:#888;text-decoration:none;">' + ('Απόρρητο' if is_el else 'Privacy') + '</a></p>\n'
            '</footer>\n'
            '</body>\n</html>'
        )

        out_dir = ROOT / ('el/festivals' if is_el else 'festivals')
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / 'index.html').write_text(page_html, encoding='utf-8')

    return len(all_fests)


def generate_whats_on_index(island_keys):
    """Build a compact JSON index for the home page 'what\'s on now' strip.
    Contains, per island: perfect months (1-12), festivals with month-coverage and name.
    Tiny file (~10KB for 78 islands) so home page loads it fast.
    """
    index = {}
    for key in sorted(island_keys):
        json_path = ISLANDS_DIR / f'{key}.json'
        try:
            d = json.loads(json_path.read_text())
        except Exception:
            continue

        # Collect months tagged 'perfect' (1-indexed for human readability)
        wtv_months = (d.get('when_to_visit') or {}).get('months') or []
        perfect = [i+1 for i, m in enumerate(wtv_months) if isinstance(m, dict) and m.get('tag') == 'perfect']
        great   = [i+1 for i, m in enumerate(wtv_months) if isinstance(m, dict) and m.get('tag') == 'great']

        # Collect festivals with parsed month coverage
        festivals = []
        for fest in (d.get('festivals') or []):
            if not isinstance(fest, dict): continue
            when = fest.get('when', '')
            festivals.append({
                'name': fest.get('name', ''),
                'name_el': fest.get('name_el', ''),
                'when': when,
                'when_el': fest.get('when_el', ''),
                'months': sorted(parse_when_to_months(when)),
            })

        if perfect or great or festivals:
            entry = {}
            if perfect:    entry['perfect'] = perfect
            if great:      entry['great'] = great
            if festivals:  entry['festivals'] = festivals
            index[key] = entry

    out_path = ROOT / 'whats-on.json'
    out_path.write_text(json.dumps(index, ensure_ascii=False, separators=(',',':')))
    return out_path


# Mirror of script.js parse — used at build time to pre-compute month coverage per festival
_MONTH_NAMES = {
    'january':1, 'jan':1, 'february':2, 'feb':2, 'march':3, 'mar':3, 'april':4, 'apr':4,
    'may':5, 'june':6, 'jun':6, 'july':7, 'jul':7, 'august':8, 'aug':8,
    'september':9, 'sept':9, 'sep':9, 'october':10, 'oct':10, 'november':11, 'nov':11,
    'december':12, 'dec':12,
}
def parse_when_to_months(when_str):
    """Return set of month numbers (1-12) the festival likely covers."""
    if not when_str: return set()
    s = when_str.lower()
    months = set()
    for name, num in _MONTH_NAMES.items():
        if re.search(r'\b' + name + r'\b', s):
            months.add(num)
    range_match = re.search(r'(\w+)\s+through\s+(?:early\s+)?(\w+)', s)
    if range_match:
        a = _MONTH_NAMES.get(range_match.group(1)); b = _MONTH_NAMES.get(range_match.group(2))
        if a and b:
            months.update(range(a, b+1) if a <= b else list(range(a, 13)) + list(range(1, b+1)))
    dash_match = re.search(r'(\w+)\s*[\u2013-]\s*(\w+)', s)
    if dash_match:
        a = _MONTH_NAMES.get(dash_match.group(1)); b = _MONTH_NAMES.get(dash_match.group(2))
        if a and b:
            months.update(range(a, b+1) if a <= b else list(range(a, 13)) + list(range(1, b+1)))
    # Movable feasts — only use the keyword fallback if NO explicit month was found.
    # Once we've added explicit "20 June 2027" dates, those win.
    if not months:
        if 'easter' in s or 'whitsun' in s or 'pentecost' in s:
            months.update([4, 5])
        if 'pre-lent' in s or 'apokries' in s:
            months.update([2, 3])
    return months


def file_lastmod(path):
    """Return ISO-8601 date for the modification time of a file. Falls back to today."""
    try:
        ts = path.stat().st_mtime
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%Y-%m-%d')
    except Exception:
        return datetime.now(timezone.utc).strftime('%Y-%m-%d')

def generate_sitemap(island_keys):
    """Build a sitemap with proper hreflang alternates per Google's guidelines.

    Each unique URL gets its own <url> entry whose <loc> matches that URL.
    Includes <lastmod> per URL — for island pages, derived from the underlying
    JSON file's mtime, so Google sees per-island freshness on each redeploy.
    For static pages, uses today's UTC date.

    Hash-fragment URLs (e.g. /#data) are NOT included — Google ignores
    everything after '#', so they're treated as duplicates of the homepage.
    """
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    # Static pages: just the two language homepages. The internal SPA views
    # (/#data, /#compare, etc.) are NOT separate URLs to a search engine.
    static_pages = [
        ('/', '/el/', 1.0, today),
        ('/festivals/', '/el/festivals/', 0.8, today),
        ('/privacy/', '/el/privacy/', 0.3, today),
    ]

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">')

    def add_url_pair(en_path, el_path, priority, lastmod):
        """Emit two <url> entries (one EN, one EL) with reciprocal hreflang alternates."""
        url_en = f'{SITE_URL}{en_path}'
        url_el = f'{SITE_URL}{el_path}'
        # English entry
        lines.append('  <url>')
        lines.append(f'    <loc>{url_en}</loc>')
        lines.append(f'    <lastmod>{lastmod}</lastmod>')
        lines.append(f'    <priority>{priority}</priority>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{url_en}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="el" href="{url_el}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url_en}"/>')
        lines.append('  </url>')
        # Greek entry — its OWN entry, with its OWN <loc>
        lines.append('  <url>')
        lines.append(f'    <loc>{url_el}</loc>')
        lines.append(f'    <lastmod>{lastmod}</lastmod>')
        lines.append(f'    <priority>{priority}</priority>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{url_en}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="el" href="{url_el}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url_en}"/>')
        lines.append('  </url>')

    # Static homepages (EN + EL)
    for en_path, el_path, prio, lastmod in static_pages:
        add_url_pair(en_path, el_path, prio, lastmod)

    # Islands — each one gets BOTH an EN entry and an EL entry. Per-island
    # lastmod comes from the JSON file mtime so editing one island only bumps
    # that one's freshness signal in the sitemap.
    for key in sorted(island_keys):
        json_path = ISLANDS_DIR / f'{key}.json'
        lastmod = file_lastmod(json_path)
        add_url_pair(f'/island/{key}/', f'/el/island/{key}/', 0.7, lastmod)

    lines.append('</urlset>')
    SITEMAP_PATH.write_text('\n'.join(lines) + '\n')

if __name__ == '__main__':
    main()
