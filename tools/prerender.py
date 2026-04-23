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
    for line in body.split('\n'):
        mm = re.match(r"\s*'([a-z-]+)':\s*'([^']+)',?", line)
        if mm:
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
            'days': grab('days'),
            'area': grab('area'),
            'pop': grab('pop'),
            'lat': grab('lat'),
            'lng': grab('lng'),
            'group': (re.search(r'island_group:\s*"([^"]+)"', line) or ['', ''])[1],
            'has_airport': 'has_airport:true' in line,
        }
    return islands

ISLAND_META = load_island_meta()

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
# JSON-LD structured data — this is how we win rich snippets
# ---------------------------------------------------------------------
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
    # Clean intro to plain text
    intro_plain = re.sub(r'\s+', ' ', intro).strip()

    destination = {
        "@context": "https://schema.org",
        "@type": "TouristDestination",
        "name": name,
        "description": intro_plain[:500],
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
    # Add rating aggregated from our dimension scores
    if meta.get('total'):
        destination["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": round(meta['total'], 1),
            "bestRating": 5,
            "worstRating": 1,
            "ratingCount": 1
        }

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
            "description": pick(data.get('itinerary', {}), 'subtitle', lang) or intro_plain[:200],
            "itinerary": itinerary_list,
            "touristType": "leisure",
        }

    # Breadcrumb
    breadcrumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1,
             "name": "Home" if lang == 'en' else 'Αρχική',
             "item": SITE_URL + ('/' if lang == 'en' else '/el/')},
            {"@type": "ListItem", "position": 2,
             "name": GREEK_GROUPS.get(meta['group'], meta['group']) if lang == 'el' else meta['group'],
             "item": SITE_URL + ('/' if lang == 'en' else '/el/')},
            {"@type": "ListItem", "position": 3, "name": name, "item": url},
        ],
    }

    out = [destination, breadcrumbs]
    if trip:
        out.append(trip)
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
    """155-char meta description. Must be compelling — it's the search snippet."""
    intro = pick(data, 'intro', lang) or ''
    # Strip any HTML-like chars, normalize whitespace
    clean = re.sub(r'\s+', ' ', intro).strip()
    # Prefer first sentence or first 150 chars
    m = re.match(r'^([^.!?]{40,200}[.!?])', clean)
    snippet = m.group(1) if m else clean[:155]
    if len(snippet) > 160:
        snippet = snippet[:157].rsplit(' ', 1)[0] + '…'
    return snippet

# ---------------------------------------------------------------------
# Pre-rendered body content — this is what Google crawls
# ---------------------------------------------------------------------
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
            day_blocks.append(f'''
<section class="seo-day">
  <h3>{day_label} {day_num}: {day_title}</h3>
  <p class="seo-day-meta">{overnight_label}: <strong>{overnight}</strong> · {drive_label}: {km} km, ~{drive_mins} min</p>
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

    # Related islands (internal linking — SEO gold)
    group = meta.get('group', '')
    related = [k for k, m in ISLAND_META.items()
               if k != key and m.get('group') == group and m.get('total')]
    related.sort(key=lambda k: -ISLAND_META[k]['total'])
    related = related[:6]
    related_links = []
    for rk in related:
        rname = GREEK_NAMES.get(rk, ISLAND_META[rk]['name']) if lang == 'el' else ISLAND_META[rk]['name']
        href = f'/el/island/{rk}/' if lang == 'el' else f'/island/{rk}/'
        related_links.append(f'<a href="{href}">{esc(rname)}</a>')
    group_label = GREEK_GROUPS.get(group, group) if lang == 'el' else group
    related_heading = f'Other islands in the {group_label}' if lang == 'en' else f'Άλλα νησιά στα/στο {group_label}'
    related_html = ''
    if related_links:
        related_html = f'<section class="seo-related"><h2>{related_heading}</h2><p>{" · ".join(related_links)}</p></section>'

    # Compose full body
    subtitle_html = f'<p class="seo-subtitle">{esc(subtitle)}</p>' if subtitle else ''
    return f'''
<article class="seo-island-content">
  <header>
    <h1>{esc(name)}</h1>
    {subtitle_html}
    {rating_text}
  </header>
  <section class="seo-intro">
    <p>{safe_html(intro)}</p>
  </section>
  {itinerary_html}
  {beaches_html}
  {related_html}
</article>'''

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

    return f'''<!DOCTYPE html>
<html lang="{html_lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="theme-color" content="#0B8FAC">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{url_en}">
<link rel="alternate" hreflang="el" href="{url_el}">
<link rel="alternate" hreflang="x-default" href="{url_en}">
<link rel="icon" href="{asset_prefix}logo.png">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/logo.png">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:locale" content="{og_locale}">
<meta property="og:locale:alternate" content="{('el_GR' if lang=='en' else 'en_US')}">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{SITE_URL}/logo.png">

<!-- Structured data -->
<script type="application/ld+json">{schema_json}</script>

<!-- SPA assets — load the same CSS as the main site so the SEO body blends visually -->
<link rel="stylesheet" href="{asset_prefix}style.css?v=16">
<style>
  /* Minimal SEO body styling — these elements exist only in pre-rendered pages */
  .seo-island-content {{
    max-width: 900px; margin: 40px auto; padding: 24px;
    font-family: var(--sans, sans-serif); color: var(--ink-1, #111);
    line-height: 1.65;
  }}
  .seo-island-content h1 {{
    font-family: var(--display, serif); font-size: 42px; margin: 0 0 6px;
  }}
  .seo-subtitle {{ color: var(--ink-3, #555); font-style: italic; margin: 0 0 12px; }}
  .seo-rating {{ color: var(--ink-2, #333); font-size: 14px; }}
  .seo-intro p {{ font-size: 17px; }}
  .seo-itinerary, .seo-beaches, .seo-related {{ margin-top: 36px; }}
  .seo-itinerary h2, .seo-beaches h2, .seo-related h2 {{
    font-family: var(--display, serif); font-size: 28px; margin: 0 0 16px;
    border-bottom: 2px solid var(--aegean, #0B8FAC); padding-bottom: 6px;
  }}
  .seo-day {{ margin-bottom: 24px; }}
  .seo-day h3 {{ font-size: 20px; margin: 0 0 4px; }}
  .seo-day-meta {{ color: var(--ink-3, #555); font-size: 13px; margin: 0 0 10px; }}
  .seo-stops {{ padding-left: 20px; }}
  .seo-stops li {{ margin-bottom: 10px; font-size: 15px; }}
  .seo-beach {{ margin-bottom: 24px; padding: 18px; background: rgba(11,143,172,0.05); border-radius: 10px; }}
  .seo-beach h3 {{ margin: 0 0 8px; font-size: 19px; }}
  .seo-beach p {{ margin: 0 0 12px; }}
  .seo-beach dl {{ display: grid; grid-template-columns: 120px 1fr; gap: 4px 12px; font-size: 13px; margin: 0; }}
  .seo-beach dt {{ font-weight: 600; color: var(--ink-3, #555); }}
  .seo-beach dd {{ margin: 0; }}
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
    text-decoration: none; color: #111; font-weight: 700; font-size: 17px;
  }}
  .seo-nav-links {{ display: flex; gap: 20px; }}
  .seo-nav-links a {{
    color: #0B8FAC; text-decoration: none; font-weight: 600; font-size: 14px;
  }}
  .seo-nav-links a:hover {{ text-decoration: underline; }}
  @media (max-width: 600px) {{
    .seo-nav {{ flex-direction: column; gap: 12px; }}
    .seo-nav-links {{ gap: 14px; font-size: 13px; }}
  }}

  /* CTA box */
  .seo-cta-box {{
    max-width: 900px; margin: 40px auto; padding: 28px 24px;
    background: linear-gradient(135deg, rgba(11,143,172,0.08), rgba(11,143,172,0.02));
    border-radius: 14px; text-align: center; font-family: var(--sans, sans-serif);
  }}
  .seo-cta-box h3 {{ font-family: var(--display, serif); font-size: 24px; margin: 0 0 8px; color: #111; }}
  .seo-cta-box p {{ color: #555; margin: 0 0 20px; }}
  .seo-cta-buttons {{ display: flex; gap: 12px; flex-wrap: wrap; justify-content: center; }}
  .seo-cta-btn {{
    display: inline-block; padding: 12px 20px; background: #0B8FAC; color: #fff;
    text-decoration: none; border-radius: 10px; font-weight: 600; font-size: 14px;
    transition: transform 0.15s;
  }}
  .seo-cta-btn:hover {{ transform: translateY(-2px); color: #fff; text-decoration: none; }}

  /* Footer */
  .seo-footer {{
    max-width: 900px; margin: 40px auto 20px; padding: 20px 24px;
    border-top: 1px solid #e5e5e5; text-align: center;
    color: #777; font-size: 13px; font-family: var(--sans, sans-serif);
  }}
  .seo-footer a {{ color: #0B8FAC; text-decoration: none; }}
  .seo-footer p {{ margin: 4px 0; }}
</style>
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
  <p><a href="{('/el/island/' if lang == 'en' else '/island/')}{key}/">{'Ελληνικά' if lang == 'en' else 'English'}</a></p>
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

def generate_sitemap(island_keys):
    """Build a comprehensive sitemap with the new clean URLs."""
    static_paths = [
        ('', 1.0),           # homepage
        ('data', 0.8),       # islands data table
        ('compare', 0.7),
        ('hopping', 0.8),
        ('international', 0.7),
        ('match', 0.6),
        ('mission', 0.4),
    ]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">')

    for path, prio in static_paths:
        url_en = f'{SITE_URL}/' if not path else f'{SITE_URL}/#{path}'
        url_el = f'{SITE_URL}/el/' if not path else f'{SITE_URL}/el/#{path}'
        lines.append('  <url>')
        lines.append(f'    <loc>{url_en}</loc>')
        lines.append(f'    <priority>{prio}</priority>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{url_en}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="el" href="{url_el}"/>')
        lines.append('  </url>')

    # Islands — use the new clean URLs
    for key in sorted(island_keys):
        url_en = f'{SITE_URL}/island/{key}/'
        url_el = f'{SITE_URL}/el/island/{key}/'
        lines.append('  <url>')
        lines.append(f'    <loc>{url_en}</loc>')
        lines.append(f'    <priority>0.7</priority>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{url_en}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="el" href="{url_el}"/>')
        lines.append('  </url>')

    lines.append('</urlset>')
    SITEMAP_PATH.write_text('\n'.join(lines) + '\n')

if __name__ == '__main__':
    main()
