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
import unicodedata
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
def load_island_clusters():
    """Parse ISLAND_CLUSTERS from script.js (written as valid JSON) and return
    (clusters, cluster_of) so the static pages match the SPA exactly."""
    text = (ROOT / 'script.js').read_text()
    m = re.search(r'const ISLAND_CLUSTERS = (\{[\s\S]*?\n\});', text)
    if not m:
        return {}, {}
    clusters = json.loads(m.group(1))
    cluster_of = {}
    for ck, c in clusters.items():
        for k in c.get('members', []):
            cluster_of[k] = ck
    return clusters, cluster_of


ISLAND_CLUSTERS, CLUSTER_OF = {}, {}


def _score_colour(s):
    """Mirror of scoreToColor() in script.js — same five bands."""
    s = s or 0
    return ('#1B5E20' if s >= 4.5 else '#4CAF50' if s >= 3.8 else
            '#8FAE3C' if s >= 3.5 else '#C4962A' if s >= 3.0 else '#C0522A')


def cluster_note_html(key, meta, lang):
    """Static twin of clusterNoteHtml() — the two-chip dual score."""
    ck = CLUSTER_OF.get(key)
    if not ck or not meta.get('total'):
        return ''
    c = ISLAND_CLUSTERS[ck]
    solo = meta['total']
    cname = (c.get('name_el') or c['name']) if lang == 'el' else c['name']
    if lang == 'el':
        a_lbl, b_lbl = 'μόνο του', 'με ' + cname
    else:
        a_lbl, b_lbl = 'on its own', 'with the ' + re.sub(r'^the ', '', cname)
    return (f'<span class="isl-dual">'
            f'<span class="isl-dual-chip"><b style="color:{_score_colour(solo)}">{solo:.1f}</b>'
            f'<i>{a_lbl}</i></span>'
            f'<span class="isl-dual-arrow">→</span>'
            f'<span class="isl-dual-chip up"><b style="color:{_score_colour(c["score"])}">{c["score"]:.1f}</b>'
            f'<i>{esc(b_lbl)}</i></span></span>')


def cluster_prose(key, meta, lang):
    """A short honest paragraph for the SEO body, explaining the dual score."""
    ck = CLUSTER_OF.get(key)
    if not ck or not meta.get('total'):
        return ''
    c = ISLAND_CLUSTERS[ck]
    cname = (c.get('name_el') or c['name']) if lang == 'el' else c['name']
    why = (c.get('why_el') or c.get('why', '')) if lang == 'el' else c.get('why', '')
    gw = c.get('gateway')
    gw_name = (ISLAND_META.get(gw, {}) or {}).get('name', gw or '')
    if lang == 'el':
        gw_name = GREEK_NAMES.get(gw, gw_name)
    gw_link = f'/el/island/{gw}/' if lang == 'el' else f'/island/{gw}/'
    rows = []
    for k in c.get('members', []):
        km = ISLAND_META.get(k, {}) or {}
        kname = GREEK_NAMES.get(k, km.get('name', k)) if lang == 'el' else km.get('name', k)
        role = ((c.get('roles', {}).get(k) or {}).get('el' if lang == 'el' else 'en')) or ''
        klink = f'/el/island/{k}/' if lang == 'el' else f'/island/{k}/'
        here = (' <em>' + ('— εδώ είσαι' if lang == 'el' else "— you&#39;re here") + '</em>') if k == key else ''
        sc = km.get('total') or 0
        cell = (f'<span class="cb-score" style="background:{_score_colour(sc)}">{sc:.1f}</span>'
                f'<span class="cb-text"><b>{esc(kname)}{here}</b><span>{esc(role)}</span></span>')
        rows.append(f'<div class="cb-row me">{cell}</div>' if k == key
                    else f'<a class="cb-row" href="{klink}">{cell}</a>')
    rows_html = ''.join(rows)
    gw_sc = (ISLAND_META.get(gw, {}) or {}).get('total') or 0
    days = c.get('days', 3)
    per = max(1, round(days / max(1, len(c.get('members', [])))))
    trip = ','.join(f'{k}:{per}' for k in c.get('members', []))
    tc_link = ('/el/trip-cost/' if lang == 'el' else '/trip-cost/') + '?i=' + trip
    if lang == 'el':
        head = 'Μέρος ' + esc(c.get('name_el_gen') or cname)
        base_lbl, days_lbl, cta = 'Βάση', 'ημέρες', '💶 Υπολόγισε αυτή τη διαδρομή'
    else:
        head = 'Part of ' + esc(cname)
        base_lbl, days_lbl, cta = 'Base', 'days', '💶 Budget this route'
    return (f'<section class="cluster-block" id="cluster-block">'
            f'<h2 class="cb-title">{head}</h2>'
            f'<p class="cb-why">{esc(why)}</p>'
            f'<a class="cb-base" href="{gw_link}"><span class="cb-base-lbl">{base_lbl}</span>'
            f'<span class="cb-score" style="background:{_score_colour(gw_sc)}">{gw_sc:.1f}</span>'
            f'<b>{esc(gw_name)}</b><span class="cb-days">{days} {days_lbl}</span></a>'
            f'<div class="cb-rows">{rows_html}</div>'
            f'<a class="cb-cta" href="{tc_link}">{cta}</a></section>')


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
ISLAND_CLUSTERS, CLUSTER_OF = load_island_clusters()
TITLE_OVERRIDES = {'ammouliani': ('Ammouliani {year} — Beaches, Drenia Islets & Mt Athos Views', 'Αμμουλιανή {year} — Παραλίες, Δρένια & Θέα στον Άθω'), 'meganisi': ('Meganisi {year} — Beaches, Getting There from Lefkada, Day Plan', 'Μεγανήσι {year} — Παραλίες, Πώς Πας από Λευκάδα, Πρόγραμμα'), 'kastos': ('Kastos {year} — Tiny, Car-Free: Is It Worth the Trip?', 'Καστός {year} — Μικροσκοπικός, Χωρίς Αυτοκίνητα: Αξίζει;'), 'kalamos': ('Kalamos {year} — Ionian Hideaway: Beaches, Boats, Honest Take', 'Κάλαμος {year} — Κρυφό Ιόνιο: Παραλίες, Βάρκες, Ειλικρινά'), 'othonoi': ("Othonoi {year} — Greece's Westernmost Isle: Caves & Beaches", 'Οθωνοί {year} — Το Δυτικότερο Νησί: Σπηλιές & Παραλίες'), 'pserimos': ('Pserimos {year} — One Beach, 84 Locals: Day Trip Guide', 'Ψέριμος {year} — Μια Παραλία, 84 Κάτοικοι: Οδηγός Εκδρομής'), 'mathraki': ('Mathraki {year} — 330 People, One Beach, No Crowds', 'Μαθράκι {year} — 330 Κάτοικοι, Μια Παραλία, Καθόλου Κόσμος'), 'telendos': ("Telendos {year} — Car-Free Rock off Kalymnos: What's There", 'Τέλενδος {year} — Βράχος Χωρίς Αυτοκίνητα: Τι Έχει'), 'arki': ('Arki {year} — 44 Residents, No Cars: Aegean at Its Emptiest', 'Αρκιοί {year} — 44 Κάτοικοι, Χωρίς Αυτοκίνητα: Άδειο Αιγαίο')}

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

# Mapping shared by interpret_facing. Mirrors FACING_MAP in i18n.js so both
# renderers produce identical wind-protection prose for the same data.
_FACING_MAP = {
    'north':     {'en': 'North-facing — fully exposed to the meltemi (the dominant summer N/NE wind); often choppy June–September',
                  'el': 'Με προσανατολισμό βόρειο — πλήρως εκτεθειμένη στο μελτέμι (τον κυρίαρχο καλοκαιρινό Β/ΒΑ άνεμο)· συχνά αγριεμένη Ιούνιο–Σεπτέμβριο'},
    'northeast': {'en': 'Northeast-facing — exposed to the meltemi (the dominant summer N/NE wind); often windy on meltemi days',
                  'el': 'Με προσανατολισμό βορειοανατολικό — εκτεθειμένη στο μελτέμι (τον κυρίαρχο καλοκαιρινό Β/ΒΑ άνεμο)· συχνά αγριεμένη τις μέρες μελτεμιού'},
    'east':      {'en': 'East-facing — mostly sheltered from the meltemi (the summer N/NE wind); can be choppy on the strongest NE days',
                  'el': 'Με προσανατολισμό ανατολικό — κυρίως προστατευμένη από το μελτέμι (τον καλοκαιρινό Β/ΒΑ άνεμο)· μπορεί να φουρτουνιάσει τις πιο δυνατές ΒΑ μέρες'},
    'southeast': {'en': 'Southeast-facing — sheltered from the meltemi (the summer N/NE wind); calm most days, exposed only to rare southern winds',
                  'el': 'Με προσανατολισμό νοτιοανατολικό — προστατευμένη από το μελτέμι (τον καλοκαιρινό Β/ΒΑ άνεμο)· ήρεμη τις περισσότερες μέρες, εκτεθειμένη μόνο σε σπάνιους νότιους ανέμους'},
    'south':     {'en': 'South-facing — sheltered from the meltemi (the summer N/NE wind); calm in summer, exposed only to rare southern winds',
                  'el': 'Με προσανατολισμό νότιο — προστατευμένη από το μελτέμι (τον καλοκαιρινό Β/ΒΑ άνεμο)· ήρεμη το καλοκαίρι, εκτεθειμένη μόνο σε σπάνιους νότιους ανέμους'},
    'southwest': {'en': 'Southwest-facing — sheltered from the meltemi (the summer N/NE wind); calm in summer, exposed only to rare S/SW winds',
                  'el': 'Με προσανατολισμό νοτιοδυτικό — προστατευμένη από το μελτέμι (τον καλοκαιρινό Β/ΒΑ άνεμο)· ήρεμη το καλοκαίρι, εκτεθειμένη μόνο σε σπάνιους Ν/ΝΔ ανέμους'},
    'west':      {'en': 'West-facing — sheltered from the meltemi (the summer N/NE wind); calm most summer days, sometimes choppy on rare westerly winds',
                  'el': 'Με προσανατολισμό δυτικό — προστατευμένη από το μελτέμι (τον καλοκαιρινό Β/ΒΑ άνεμο)· ήρεμη τις περισσότερες καλοκαιρινές μέρες, μερικές φορές φουρτουνιασμένη σε σπάνιους δυτικούς ανέμους'},
    'northwest': {'en': 'Northwest-facing — exposed to the meltemi (the dominant summer N/NE wind); often windy on meltemi days',
                  'el': 'Με προσανατολισμό βορειοδυτικό — εκτεθειμένη στο μελτέμι (τον κυρίαρχο καλοκαιρινό Β/ΒΑ άνεμο)· συχνά αγριεμένη τις μέρες μελτεμιού'},
}
# Abbreviations map to the full direction

# Ionian (Eptanisa) variant — no meltemi there; the summer wind is the
# maïstros, a NW afternoon sea breeze. Mirrors FACING_MAP_IONIAN in i18n.js.
_FACING_MAP_IONIAN = {
    'north':     {'en': "North-facing — open to the Ionian's afternoon maïstros (NW sea breeze); calmest in the morning",
                  'el': 'Με προσανατολισμό βόρειο — ανοιχτή στον απογευματινό μαΐστρο (τη ΒΔ θαλάσσια αύρα του Ιονίου)· πιο ήρεμη το πρωί'},
    'northeast': {'en': 'Northeast-facing — mostly sheltered from the afternoon maïstros (NW breeze); usually calm',
                  'el': 'Με προσανατολισμό βορειοανατολικό — κυρίως προστατευμένη από τον απογευματινό μαΐστρο (ΒΔ αύρα)· συνήθως ήρεμη'},
    'east':      {'en': "East-facing — sheltered from the Ionian's afternoon maïstros (NW breeze); typically calm all day",
                  'el': 'Με προσανατολισμό ανατολικό — προστατευμένη από τον απογευματινό μαΐστρο του Ιονίου (ΒΔ αύρα)· κατά κανόνα ήρεμη όλη μέρα'},
    'southeast': {'en': 'Southeast-facing — well sheltered; calm in summer, exposed only to rare southerlies',
                  'el': 'Με προσανατολισμό νοτιοανατολικό — καλά προστατευμένη· ήρεμη το καλοκαίρι, εκτεθειμένη μόνο σε σπάνιους νοτιάδες'},
    'south':     {'en': 'South-facing — sheltered from the prevailing NW winds; calm in summer, exposed only to rare southerlies',
                  'el': 'Με προσανατολισμό νότιο — προστατευμένη από τους επικρατούντες ΒΔ ανέμους· ήρεμη το καλοκαίρι, εκτεθειμένη μόνο σε σπάνιους νοτιάδες'},
    'southwest': {'en': 'Southwest-facing — calm mornings; picks up some of the afternoon maïstros (NW breeze) late in the day',
                  'el': 'Με προσανατολισμό νοτιοδυτικό — ήρεμα πρωινά· πιάνει λίγο τον απογευματινό μαΐστρο (ΒΔ αύρα) αργά τη μέρα'},
    'west':      {'en': "West-facing — exposed to the afternoon maïstros (the Ionian's NW summer breeze); glassy mornings, waves by late afternoon",
                  'el': 'Με προσανατολισμό δυτικό — εκτεθειμένη στον απογευματινό μαΐστρο (τη ΒΔ καλοκαιρινή αύρα του Ιονίου)· λάδι το πρωί, κυματάκι το απόγευμα'},
    'northwest': {'en': 'Northwest-facing — head-on to the afternoon maïstros (NW breeze); best swum in the morning',
                  'el': 'Με προσανατολισμό βορειοδυτικό — κόντρα στον απογευματινό μαΐστρο (ΒΔ αύρα)· καλύτερη για μπάνιο το πρωί'},
}

_FACING_ABBREV = {'n': 'north', 'ne': 'northeast', 'e': 'east', 'se': 'southeast',
                  's': 'south', 'sw': 'southwest', 'w': 'west', 'nw': 'northwest',
                  # Hybrid directions seen in the data — map to the nearest cardinal
                  'south-southwest': 'southwest', 'ssw': 'southwest',
                  'west-southwest': 'southwest', 'wsw': 'southwest',
                  'south-southeast': 'southeast', 'sse': 'southeast',
                  'east-southeast': 'southeast', 'ese': 'southeast',
                  'north-northeast': 'northeast', 'nne': 'northeast',
                  'east-northeast': 'northeast', 'ene': 'northeast',
                  'north-northwest': 'northwest', 'nnw': 'northwest',
                  'west-northwest': 'northwest', 'wnw': 'northwest'}

def interpret_facing(raw_facing, lang, ionian=False):
    """Turn a beach `facing` value into a traveler-friendly wind-protection
    sentence. Mirrors interpretFacing() in i18n.js. See that function for
    rationale. Falls back to the raw value for unmatched edge cases."""
    if not raw_facing:
        return ''
    head = str(raw_facing)
    # Drop any descriptive suffix introduced by em-dash or " - " or " — ".
    # Use a regex so we don't confuse the dash inside "South-facing" with
    # a separator dash.
    import re as _re
    head = _re.split(r'\s+[—–-]\s+', head, 1)[0]
    # Strip a trailing "-facing" / " facing" if present.
    head = _re.sub(r'[-\s]facing$', '', head, flags=_re.IGNORECASE).strip().lower()
    if head in _FACING_ABBREV:
        head = _FACING_ABBREV[head]
    mapped = (_FACING_MAP_IONIAN if ionian else _FACING_MAP).get(head)
    if mapped:
        return mapped.get('el' if lang == 'el' else 'en', raw_facing)
    return raw_facing

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

def _wtv_heading(data, lang):
    """Query-shaped section heading: 'Best time to visit Milos' / EL accusative."""
    if lang == 'el':
        acc = data.get('name_accusative_el') or data.get('name_el') or data.get('name', '')
        return f'Καλύτερη εποχή για {acc}'
    return f'Best time to visit {data.get("name", "")}'

WTV_I18N = {
    'en': {
        'title': 'When to Visit',
        'months': ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
        'tags': {'perfect': 'Best', 'great': 'Great', 'ok': 'OK', 'avoid': 'Avoid'},
    },
    'el': {
        'title': 'Πότε να Πας',
        'months': ['Ιαν','Φεβ','Μάρ','Απρ','Μάι','Ιούν','Ιούλ','Αύγ','Σεπ','Οκτ','Νοέ','Δεκ'],
        'tags': {'perfect': 'Τέλεια', 'great': 'Καλά', 'ok': 'Μέτρια', 'avoid': 'Απόφυγε'},
    },
}

def build_when_to_visit_html(data, lang='en'):
    """Mirror script.js buildWhenToVisitSection. Empty string if missing.

    Renders the redesigned clean layout: a single-row 12-month colored ribbon,
    preceded by a highlights summary line ("Best: Jun, Sep · Avoid: Oct-May"),
    followed by an optional "Limited service: …" line if any months have the
    `limited: true` flag set.

    Mobile uses a vertical 12-row list (.wtv-vertical) instead of the ribbon.
    """
    w = data.get('when_to_visit')
    if not w or not isinstance(w.get('months'), list) or len(w['months']) != 12:
        return ''

    labels = WTV_I18N[lang]
    month_abbr = labels['months']  # ['Jan','Feb',…] or ['Ιαν','Φεβ',…]
    tag_labels = labels['tags']    # {'perfect':'Best',…}
    limited_label = 'Limited service' if lang == 'en' else 'Περιορισμένη λειτουργία'

    # Ribbon cells — wtv-limited modifier dims the cell visually
    ribbon_cells = []
    for i, m in enumerate(w['months']):
        tag = (m.get('tag') or 'ok').lower()
        why = pick(m, 'why', lang) or ''
        is_limited = m.get('limited') is True
        prefix = f'{limited_label} — ' if is_limited else ''
        cls = f'wtv-cell wtv-{tag}' + (' wtv-limited' if is_limited else '')
        ribbon_cells.append(
            f'<div class="{cls}" title="{esc(month_abbr[i])} — {esc(prefix + why)}">'
            f'{esc(month_abbr[i])}</div>'
        )

    # Group months by tag for the highlights summary
    tag_groups = {'perfect': [], 'great': [], 'ok': [], 'avoid': []}
    for i, m in enumerate(w['months']):
        tag = (m.get('tag') or 'ok').lower()
        if tag in tag_groups:
            tag_groups[tag].append(i)

    def fmt_month_list(indices):
        """Format indices as 'Jun, Sep' or 'Oct-May' if contiguous (handles wrap)."""
        if not indices:
            return ''
        if len(indices) <= 3:
            return ', '.join(month_abbr[i] for i in indices)
        sorted_ix = sorted(indices)
        max_gap = 0
        gap_start = -1
        for j in range(len(sorted_ix) - 1):
            g = sorted_ix[j+1] - sorted_ix[j]
            if g > max_gap:
                max_gap = g
                gap_start = j
        wrap_gap = (12 - sorted_ix[-1] - 1) + sorted_ix[0] + 1
        if max_gap == 1 and wrap_gap > 1:
            return f'{month_abbr[sorted_ix[0]]}–{month_abbr[sorted_ix[-1]]}'
        if max_gap > 1 and wrap_gap == 1 and len(sorted_ix) == 12 - (max_gap - 1):
            first = sorted_ix[gap_start + 1]
            last = sorted_ix[gap_start]
            return f'{month_abbr[first]}–{month_abbr[last]}'
        return ', '.join(month_abbr[i] for i in sorted_ix)

    highlight_order = ['perfect', 'great', 'ok', 'avoid']
    highlight_items = []
    for t in highlight_order:
        if tag_groups[t]:
            highlight_items.append(
                f'<span class="wtv-hl-item wtv-hl-{t}">'
                f'<strong>{esc(tag_labels[t])}:</strong> {esc(fmt_month_list(tag_groups[t]))}'
                f'</span>'
            )
    highlight_html = '<span class="wtv-hl-sep">·</span>'.join(highlight_items)

    # Separate "Limited service: Jan, Feb…" line
    limited_indices = [i for i, m in enumerate(w['months']) if m.get('limited') is True]
    limited_line = (
        f'<div class="wtv-limited-note"><strong>{esc(limited_label)}:</strong> '
        f'{esc(fmt_month_list(limited_indices))}</div>'
        if limited_indices else ''
    )
    highlights_bar = (
        f'<div class="wtv-highlights">{highlight_html}</div>{limited_line}'
        if highlight_html else limited_line
    )

    summary = pick(w, 'summary', lang) or ''
    summary_html = f'<p class="wtv-summary">{safe_html(summary)}</p>' if summary else ''

    tags_present = {(m.get('tag') or 'ok').lower() for m in w['months']}
    legend_items = ''.join(
        f'<span class="wtv-legend-item"><span class="wtv-legend-swatch wtv-{t}"></span>{esc(tag_labels[t])}</span>'
        for t in highlight_order if t in tags_present
    )

    # Vertical mobile list
    vertical_rows = []
    for i, m in enumerate(w['months']):
        tag = (m.get('tag') or 'ok').lower()
        why = pick(m, 'why', lang) or ''
        is_limited = m.get('limited') is True
        badge = (
            f'<span class="wtv-v-limited-badge" title="{esc(limited_label)}">·</span>'
            if is_limited else ''
        )
        cls = f'wtv-vrow wtv-v-{tag}' + (' wtv-v-limited' if is_limited else '')
        vertical_rows.append(
            f'<div class="{cls}">'
            f'<div class="wtv-vmonth">{esc(month_abbr[i])}</div>'
            f'<div class="wtv-vbar wtv-{tag}" title="{esc(tag_labels.get(tag, ""))}"></div>'
            f'<div class="wtv-vwhy">{badge}{esc(why)}</div>'
            f'</div>'
        )
    vertical_inner = ''.join(vertical_rows)
    ribbon_inner = ''.join(ribbon_cells)

    return (
        f'<details class="seo-wtv wtv-section" open>'
        f'<summary class="wtv-title">{esc(_wtv_heading(data, lang))}</summary>'
        f'{summary_html}'
        f'{highlights_bar}'
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
    # A top-level `hero_photo` overrides the auto-pick (a hand-chosen main image).
    if data.get('hero_photo'):
        return data['hero_photo'], ''
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


def hero_src_1280(url):
    """Large hero rendition — mirrors heroSrc() in script.js exactly, so the
    static first-paint image is the same file the SPA hero uses (cache hit,
    no visual swap on hydration)."""
    if not url:
        return url
    if 'res.cloudinary.com' in url:
        return re.sub(r'/upload/(?:[^/]*/)?v(\d+)/',
                      r'/upload/w_1280,h_560,c_fill,q_auto,f_auto/v\1/', url)
    # Wikimedia only serves FIXED thumb widths; 1280 is the hero bucket.
    if '/thumb/' in url:
        return re.sub(r'/\d+px-', '/1280px-', url)
    m = re.match(r'^(https?://upload\.wikimedia\.org/wikipedia/[a-z]+)/([0-9a-f])/([0-9a-f]{2})/([^/]+)$', url)
    if m:
        return f'{m.group(1)}/thumb/{m.group(2)}/{m.group(3)}/{m.group(4)}/1280px-{m.group(4)}'
    return url


# Localized island-group names — mirrors groupName()/i18n group.* in the SPA.
GROUP_NAMES_EL = {
    'Cyclades': 'Κυκλάδες', 'Dodecanese': 'Δωδεκάνησα', 'Saronic': 'Σαρωνικός',
    'Sporades': 'Σποράδες', 'Ionian': 'Ιόνιο', 'NE Aegean': 'Β.Α. Αιγαίο',
    'Crete': 'Κρήτη', 'Evia': 'Εύβοια', 'Other': 'Άλλα',
}

# Car-reliance chip labels — mirrors car.* i18n keys (index 1-5 = rounded car_need).
CAR_LABELS = {
    'en': ['', 'Not needed', 'Optional', 'Useful', 'Recommended', 'Essential'],
    'el': ['', 'Δεν χρειάζεται', 'Προαιρετικό', 'Χρήσιμο', 'Συνιστάται', 'Απαραίτητο'],
}


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
    Build a list of JSON-LD objects for Google. Aims for Rich Results eligibility.
    We emit:
      - TouristDestination (the island itself)
      - TouristTrip (the itinerary, with day-by-day descriptions + overnight coords)
      - Article (the travel guide as an editorial piece, with author + dates)
      - BreadcrumbList
      - FAQPage (if FAQs present)

    All objects include dateModified pulled from the JSON file's git/mtime,
    so re-edits surface as fresh-content signals to Google.
    """
    url = f'{SITE_URL}/island/{key}/' if lang == 'en' else f'{SITE_URL}/el/island/{key}/'
    name = localized_name(key, data, meta, lang)
    intro = pick(data, 'intro', lang) or ''
    intro_plain = strip_html(intro)
    # Pull the last-modified date from git log (or mtime fallback)
    last_modified = file_lastmod(ISLANDS_DIR / f'{key}.json')

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

    # Itinerary → TouristTrip with enriched day-by-day descriptions.
    # Each day now includes a description (from the day's `subtitle` or first stop),
    # geographic coordinates (from the day's overnight stop if known), and a list
    # of subAttractions (the day's stops, each with name and coords).
    trip = None
    if 'itinerary' in data and data['itinerary'].get('days'):
        days = data['itinerary']['days']
        itinerary_list = []
        for day in days:
            day_num = day.get('day', 1)
            day_title = pick(day, 'title', lang)
            # Day description — prefer day.subtitle if present, fall back to first stop desc
            day_desc = pick(day, 'subtitle', lang) or ''
            if not day_desc and day.get('stops'):
                first_stop = day['stops'][0]
                day_desc = pick(first_stop, 'desc', lang) or ''
            day_desc = strip_html(day_desc)
            # Day-level attraction: aggregate of the stops visited
            stops = day.get('stops', []) or []
            day_attraction = {
                "@type": "TouristAttraction",
                "name": f"Day {day_num}: {day_title}" if lang == 'en' else f"Μέρα {day_num}: {day_title}",
            }
            if day_desc:
                day_attraction["description"] = truncate_at_word(day_desc, 250)
            # Geo: use the first stop's coords if available (gives Google a real location)
            for s in stops:
                if isinstance(s, dict) and s.get('lat') is not None and s.get('lng') is not None:
                    day_attraction["geo"] = {
                        "@type": "GeoCoordinates",
                        "latitude": s['lat'],
                        "longitude": s['lng'],
                    }
                    break
            # subAttractions: each individual stop (named places). Google can use
            # these for rich-snippet day-by-day rendering when supported.
            sub_attractions = []
            for s in stops[:8]:  # cap at 8 per day to keep payload reasonable
                if not isinstance(s, dict): continue
                stop_name = pick(s, 'name', lang) or ''
                if not stop_name: continue
                sub = {"@type": "TouristAttraction", "name": stop_name}
                if s.get('lat') is not None and s.get('lng') is not None:
                    sub["geo"] = {"@type": "GeoCoordinates", "latitude": s['lat'], "longitude": s['lng']}
                sub_attractions.append(sub)
            if sub_attractions:
                day_attraction["subjectOf"] = sub_attractions
            itinerary_list.append({
                "@type": "ListItem",
                "position": day_num,
                "item": day_attraction,
            })
        trip = {
            "@context": "https://schema.org",
            "@type": "TouristTrip",
            "name": (f"{len(days)}-day {name} itinerary" if lang == 'en'
                     else f"Δρομολόγιο {len(days)} ημερών — {name}"),
            "description": pick(data.get('itinerary', {}), 'subtitle', lang) or truncate_at_word(intro_plain, 200),
            "itinerary": {
                "@type": "ItemList",
                "numberOfItems": len(itinerary_list),
                "itemListElement": itinerary_list,
            },
            "touristType": "leisure",
            "dateModified": last_modified,
        }

    # Article schema — positions the page as an editorial travel guide for
    # Google's Article rich results. headline + author + dates are the
    # required fields; image is a strong recommended one (we use the OG image).
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": build_title(key, data, meta, lang).rsplit(' | ', 1)[0],  # strip " | Aegean Blueprint"
        "description": truncate_at_word(intro_plain, 200),
        "url": url,
        "image": f'{SITE_URL}/og/{key}.jpg',
        "datePublished": last_modified,  # we don't track first-publish separately
        "dateModified": last_modified,
        "author": {
            "@type": "Person",
            "name": "Stergios Gousios",
            "url": SITE_URL + ('/' if lang == 'en' else '/el/') + 'mission/',
        },
        "publisher": {
            "@type": "Organization",
            "name": "Aegean Blueprint",
            "logo": {
                "@type": "ImageObject",
                "url": f'{SITE_URL}/logo.png',
            },
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": url,
        },
        "inLanguage": "en" if lang == 'en' else "el",
    }

    # Breadcrumb — two levels (Home → Island).
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

    out = [destination, article, breadcrumbs]
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
    """Unique, keyword-rich page title.

    CTR pass (Jul 2026): GSC showed island pages at position 7-10 earning half
    the expected CTR. Hooks added: current year (freshness signal), "Beaches
    Ranked" (concrete promise), "Honest" (the brand differentiator). Most
    important words front-loaded so they survive SERP truncation (~60 chars).
    """
    from datetime import date as _d
    year = _d.today().year
    name = localized_name(key, data, meta, lang)
    # CTR pass (Jul 2026): tiny islands ranked p6-12 but earned <1.5% CTR with
    # the generic template. Bespoke, expectation-setting titles instead.
    ov = TITLE_OVERRIDES.get(key)
    if ov:
        return f"{(ov[1] if lang == 'el' else ov[0]).format(year=year)} | Aegean Blueprint"
    days = int(meta.get('days') or 0) if meta.get('days') else 0
    if lang == 'el':
        if days:
            return f"{name} {year} — Παραλίες με βαθμολογία, πρόγραμμα {days} ημερών | Aegean Blueprint"
        return f"{name} {year} — Ειλικρινής ταξιδιωτικός οδηγός | Aegean Blueprint"
    else:
        if days:
            return f"{name} Travel Guide {year} — Beaches Ranked, {days}-Day Itinerary | Aegean Blueprint"
        return f"{name} Travel Guide {year} — Honest Scores, What's Worth It | Aegean Blueprint"

def build_description(key, data, meta, lang='en'):
    """Meta description: the island's own first intro sentence (relevance,
    query-term bolding) + a punchy promise of what the page delivers (CTR).
    Target <= 160 chars."""
    TARGET_MAX = 160
    days = int(meta.get('days') or 0) if meta.get('days') else 0
    if lang == 'el':
        hook = (f"Παραλίες με βαθμολογία, πρόγραμμα {days} ημερών, πού να φας — ειλικρινά, χωρίς φλυαρίες."
                if days else "Παραλίες, διαμονή, τι αξίζει — ειλικρινά, χωρίς φλυαρίες.")
    else:
        hook = (f"Beaches rated, a {days}-day plan, where to eat — honest, no fluff."
                if days else "Beaches, where to stay, what's worth it — honest, no fluff.")
    intro = pick(data, 'intro', lang) or ''
    clean = re.sub(r'\s+', ' ', intro).strip()
    # split only when the next word starts with a capital — keeps abbreviations
    # like 'τ.χλμ.' or 'Mt.' from ending the sentence early
    first = re.split(r'(?<=[.!?])\s+(?=[A-ZΑ-ΩΆΈΉΊΌΎΏ«"0-9])', clean)[0] if clean else ''
    budget = TARGET_MAX - len(hook) - 1
    if len(first) > budget:
        first = first[:budget].rsplit(' ', 1)[0].rstrip(',;—-· ') + '…'
    return (first + ' ' + hook).strip()


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
        _cp = cluster_prose(key, meta, lang)
        if _cp:
            rating_text = rating_text + '\n' + _cp

    # Last-updated line — signals to readers (and Google) that the guide is
    # actively maintained. Pulled from git log (committer date) on the
    # underlying JSON file, so edits to itinerary/beaches/specialties show
    # up as a fresh date here.
    last_updated_iso = file_lastmod(ISLANDS_DIR / f'{key}.json')
    last_updated_human = ''
    try:
        dt = datetime.strptime(last_updated_iso, '%Y-%m-%d')
        if lang == 'el':
            month_names_el = ['Ιανουαρίου','Φεβρουαρίου','Μαρτίου','Απριλίου','Μαΐου','Ιουνίου',
                              'Ιουλίου','Αυγούστου','Σεπτεμβρίου','Οκτωβρίου','Νοεμβρίου','Δεκεμβρίου']
            last_updated_human = f'{dt.day} {month_names_el[dt.month - 1]} {dt.year}'
        else:
            last_updated_human = dt.strftime('%B %-d, %Y')
    except Exception:
        last_updated_human = last_updated_iso  # fall back to ISO

    if last_updated_human:
        label = 'Τελευταία ενημέρωση' if lang == 'el' else 'Last updated'
        last_updated_html = (
            f'<p class="seo-lastupdated">'
            f'<time datetime="{esc(last_updated_iso)}">{label}: <strong>{esc(last_updated_human)}</strong></time>'
            f'</p>'
        )
    else:
        last_updated_html = ''

    # "Good for / Maybe skip if" orientation block — renders between the
    # intro and getting-there if the island has a suited_for field. Two short
    # lists of original editorial content; strong signal of a real guide.
    suited_for_html = ''
    sf = data.get('suited_for')
    if sf:
        good = sf.get('good_el' if lang == 'el' else 'good', []) or []
        skip = sf.get('skip_el' if lang == 'el' else 'skip', []) or []
        if good or skip:
            good_title = 'Ιδανικό για' if lang == 'el' else 'Good for'
            skip_title = 'Σκέψου αλλιώς αν' if lang == 'el' else 'Maybe skip if'
            good_li = ''.join(f'<li>{esc(x)}</li>' for x in good)
            skip_li = ''.join(f'<li>{esc(x)}</li>' for x in skip)
            suited_for_html = (
                f'<section class="seo-suited">'
                f'<div class="seo-suited-col">'
                f'<h2>{good_title}</h2><ul>{good_li}</ul>'
                f'</div>'
                f'<div class="seo-suited-col">'
                f'<h2>{skip_title}</h2><ul>{skip_li}</ul>'
                f'</div>'
                f'</section>'
            )

    # Getting-there section (between intro and itinerary) — v2 schema: pills + summary + tip
    # Audience pitches — generic mechanism for "X for {audience}" SEO targeting
    # (e.g. "Naxos for families", "Milos for hikers", "Hydra for couples").
    # Each entry in data['audience'] is keyed by audience name and contains
    # markdown-light prose in 'en' and 'el'. Renders one <section> per pitch,
    # using a localized heading and **bold** subheaders inside the prose.
    audience_html = ''
    audience_obj = data.get('audience') or {}
    if audience_obj:
        # Label map: audience-key → (EN heading suffix, EL heading suffix).
        # EN: "{Name} for {audience}". EL uses gender-aware preposition + accusative.
        # Add new audiences here as they're added to islands.
        AUDIENCE_LABELS = {
            'families':  ('for families',  'για οικογένειες'),
            'couples':   ('for couples',   'για ζευγάρια'),
            'hikers':    ('for hikers',    'για πεζοπόρους'),
            'solo':      ('for solo travelers', 'για μοναχικούς ταξιδιώτες'),
            'foodies':   ('for foodies',   'για καλοφαγάδες'),
            'first_time':('for first-time visitors', 'για πρώτη επίσκεψη'),
        }
        audience_blocks = []
        for audience_key, audience_data in audience_obj.items():
            text = audience_data.get('el' if lang == 'el' else 'en', '')
            if not text:
                continue
            label_en, label_el = AUDIENCE_LABELS.get(audience_key, (audience_key, audience_key))
            heading = f'{name} {label_en}' if lang == 'en' else f'{name} {label_el}'
            paras = [p.strip() for p in text.split('\n\n') if p.strip()]
            html_paras = []
            for p in paras:
                p_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', esc(p))
                html_paras.append(f'<p>{p_html}</p>')
            audience_blocks.append(
                f'<section class="seo-audience" data-audience="{esc(audience_key)}">'
                f'<h2>{esc(heading)}</h2>'
                f'{"".join(html_paras)}'
                f'</section>'
            )
        audience_html = ''.join(audience_blocks)

    # The summary is split into a visible first sentence ("lead") and a
    # collapsible "rest", rendered as a native <details> element. This
    # declutters the page without removing any content from the HTML —
    # Google still indexes everything inside <details> normally.
    getting_there_html = ''
    gt = data.get('getting_there')
    if gt and gt.get('pills'):
        gt_label = 'Getting there' if lang == 'en' else 'Πώς θα φτάσεις'
        tip_label = 'Tip' if lang == 'en' else 'Συμβουλή'
        more_label = 'Read full route' if lang == 'en' else 'Διαβάστε αναλυτικά'

        pills = gt.get('pills_el' if lang == 'el' else 'pills', [])
        summary = gt.get('summary_el' if lang == 'el' else 'summary', '')
        tip = gt.get('tip_el' if lang == 'el' else 'tip')

        pill_html = ''
        if pills:
            pill_spans = ''.join(f'<span class="seo-gt-pill">{esc(p)}</span>' for p in pills)
            pill_html = f'<div class="seo-gt-pills">{pill_spans}</div>'

        # Split summary into lead (visible) + rest (collapsed). Strategy:
        # accumulate sentences into the lead until we have >= 80 chars, OR until
        # we hit the second sentence-end after a substantive opening. This
        # avoids the case where the lead is a useless "No airport." stub.
        lead_html = ''
        rest_html = ''
        if summary:
            sentences = re.split(r'([.!?:](?:\s+|$))', summary)
            # Recombine sentences: pairs of (text, terminator)
            recombined = []
            buf = ''
            for token in sentences:
                buf += token
                if re.match(r'^[.!?:](\s+|$)', token):
                    recombined.append(buf)
                    buf = ''
            if buf:
                recombined.append(buf)
            # Collect lead sentences until length budget reached
            lead = ''
            rest = ''
            for i, sent in enumerate(recombined):
                if len(lead) >= 80:
                    rest = ''.join(recombined[i:]).strip()
                    break
                lead += sent
            else:
                lead = summary
            lead = lead.rstrip()
            # If the "rest" is trivially short, don't hide it behind a toggle —
            # the toggle costs the user a click for nothing. Threshold ~50 chars
            # accounts for paragraphs where the second sentence is just a short
            # clarifier; longer rests genuinely declutter.
            if rest and len(rest) < 60:
                lead = (lead + ' ' + rest).strip()
                rest = ''
            if rest:
                lead_html = f'<p class="seo-gt-summary seo-gt-lead">{esc(lead)}</p>'
                rest_html = f'<p class="seo-gt-summary seo-gt-rest">{esc(rest)}</p>'
            else:
                lead_html = f'<p class="seo-gt-summary seo-gt-lead">{esc(lead)}</p>'

        tip_html = f'<p class="seo-gt-tip"><strong>{tip_label}:</strong> {esc(tip)}</p>' if tip else ''

        # Wrap rest + tip in a <details> so users can declutter but content
        # stays in the DOM at load (full SEO indexing). Only render the
        # <details> if there's actually rest content or a tip to hide.
        more_html = ''
        if rest_html or tip_html:
            more_html = (
                f'<details class="seo-gt-more">'
                f'<summary>{more_label}</summary>'
                f'{rest_html}'
                f'{tip_html}'
                f'</details>'
            )

        # Detailed long-form content — for islands targeting "how to get to X"
        # search queries. When `getting_there.detailed` is present in the JSON,
        # we override the section heading with the literal query phrase
        # ("How to get to {Name}") and render the full prose below the pills.
        # The detailed content uses markdown-light formatting (paragraphs +
        # **bold** subheaders), which we convert to HTML here.
        detailed_raw = gt.get('detailed') or {}
        detailed_text = detailed_raw.get('el' if lang == 'el' else 'en', '')
        detailed_html = ''
        if detailed_text:
            # Convert simple markdown to HTML: each blank-line-separated chunk
            # becomes a <p>, with **bold** → <strong>. Keeps it as one section
            # with semantic prose paragraphs (better for SEO than a single
            # giant <p>).
            paras = [p.strip() for p in detailed_text.split('\n\n') if p.strip()]
            html_paras = []
            for p in paras:
                # Process bold markers
                p_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', esc(p))
                # un-escape the strong tags we just inserted (esc() escaped the
                # raw text first; the regex substitution adds tags that aren't
                # text). Pattern: we ran esc on the whole string, so the **bold**
                # asterisks are still there literally. Now wrap them.
                html_paras.append(f'<p>{p_html}</p>')
            detailed_html = ''.join(html_paras)

        if pill_html or lead_html or detailed_html:
            # If detailed content is present, use the SEO-targeted heading and
            # show the full prose instead of the truncated lead/more pattern.
            if detailed_html:
                if lang == 'en':
                    seo_heading = f'How to get to {name}'
                else:
                    # Greek needs accusative case + gender-aware preposition:
                    #   feminine (η Φολέγανδρος) → "στη Φολέγανδρο"
                    #   masculine (ο Πόρος) → "στον Πόρο"
                    #   neuter (το Ηράκλειο) → "στο Ηράκλειο"
                    #   plural (τα Κύθηρα) → "στα Κύθηρα"
                    # Fall back to nominative + "στη" if no accusative provided.
                    acc = data.get('name_accusative_el') or name
                    gender = (data.get('gender_el') or 'f').lower()
                    prep_map = {'f': 'στη', 'm': 'στον', 'n': 'στο', 'p': 'στα'}
                    prep = prep_map.get(gender, 'στη')
                    seo_heading = f'Πώς να πας {prep} {acc}'
                getting_there_html = (
                    f'<section class="seo-getting-there">'
                    f'<h2>{esc(seo_heading)}</h2>'
                    f'{pill_html}'
                    f'{detailed_html}'
                    f'</section>'
                )
            else:
                getting_there_html = (
                    f'<section class="seo-getting-there">'
                    f'<h2>{gt_label}</h2>'
                    f'{pill_html}'
                    f'{lead_html}'
                    f'{more_html}'
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
                drive = pick(s, 'drive', lang)
                drive_html = f'<br><span class="seo-stop-drive">🚗 {esc(drive)}</span>' if drive else ''
                stop_items.append(f'<li><strong>{stime} · {sname}</strong>{drive_html}<br>{sdesc}</li>')
            # Meal-timing cues at each meal's slot in the route
            _foods = day.get('food')
            _foods = _foods if isinstance(_foods, list) else ([_foods] if _foods else [])
            _cuelist = []
            for f in _foods:
                if not (f.get('meal') or f.get('desc')): continue
                _meal = ((f.get('meal_el') if lang == 'el' else f.get('meal')) or '').lower()
                _area = (f.get('area_el') if lang == 'el' else f.get('area')) or ''
                _lab = 'Στάση για' if lang == 'el' else 'Stop for'
                _see = 'δες «Φαγητό & Ποτό» πιο κάτω' if lang == 'el' else 'see Eat & Drink below'
                _cue = f'<li class="seo-meal-cue">🍴 {_lab} {esc(_meal)}' + (f' · {esc(_area)}' if _area else '') + f' — {_see}</li>'
                _ai = next((i for i, x in enumerate(stops) if x.get('name') == f.get('after')), None)
                _cuelist.append((_ai if _ai is not None else len(stops) - 1, _cue))
            for _ai, _cue in sorted(_cuelist, key=lambda t: -t[0]):
                stop_items.insert(_ai + 1, _cue)

            overnight_label = 'Overnight' if lang == 'en' else 'Διανυκτέρευση'
            drive_label = 'Drive' if lang == 'en' else 'Οδήγηση'
            day_label = 'Day' if lang == 'en' else 'Μέρα'

            meta_parts = []
            if overnight:
                # Departure-day detection — render bare word without "Overnight:" prefix.
                # Matches "Departure" / "Αναχώρηση" (case- and accent-insensitive).
                normalised = unicodedata.normalize('NFD', overnight).lower()
                normalised = ''.join(c for c in normalised if not unicodedata.combining(c))
                is_departure = normalised.startswith('departure') or normalised.startswith('αναχωρηση')
                if is_departure:
                    meta_parts.append(f'<strong>{overnight}</strong>')
                else:
                    meta_parts.append(f'{overnight_label}: <strong>{overnight}</strong>')
            if km not in (None, '', 0) and drive_mins not in (None, '', 0):
                meta_parts.append(f'{drive_label}: {km} km, ~{drive_mins} min')
            meta_line_html = f'<p class="seo-day-meta">{" · ".join(meta_parts)}</p>' if meta_parts else ''
            # Eat & Drink block (food + nightlife), separated from the routed stops
            nightlife_txt = safe_html(pick(day, 'nightlife', lang))
            ed_rows = ''
            for food in _foods:
                if not (food.get('meal') or food.get('desc')): continue
                meal = (food.get('meal_el') if lang == 'el' else food.get('meal')) or ('Φαγητό' if lang == 'el' else 'Food')
                area = (food.get('area_el') if lang == 'el' else food.get('area')) or ''
                fdesc = safe_html(pick(food, 'desc', lang))
                head = f'{meal} · {area}' if area else meal
                ed_rows += f'<div class="ed-row"><span class="ed-icon">🍴</span><div class="ed-text"><div class="ed-head">{esc(head)}</div><div class="ed-body">{fdesc}</div></div></div>'
            if nightlife_txt:
                nl_title = 'Nightlife' if lang == 'en' else 'Νυχτερινή ζωή'
                ed_rows += f'<div class="ed-row"><span class="ed-icon">🍸</span><div class="ed-text"><div class="ed-head">{nl_title}</div><div class="ed-body">{nightlife_txt}</div></div></div>'
            ed_title = 'Φαγητό & Ποτό' if lang == 'el' else 'Eat & Drink'
            eatdrink_html = f'<div class="itin-eatdrink"><div class="ed-title">{ed_title}</div>{ed_rows}</div>' if ed_rows else ''

            day_blocks.append(f'''
<section class="seo-day">
  <h3>{day_label} {day_num}: {day_title}</h3>
  {meta_line_html}
  <ol class="seo-stops">
    {"".join(stop_items)}
  </ol>
  {eatdrink_html}
</section>''')

        itinerary_html = f'<section class="seo-itinerary"><h2>{heading}</h2>{"".join(day_blocks)}</section>'

    # Beaches section
    beaches_html = ''
    if beaches:
        # If `beaches_intro` is present in the JSON, the page is targeting the
        # "best beach in X" search query. Use the SEO heading and render the
        # intro prose (declarative top pick + runners-up) above the beach list.
        # Otherwise keep the existing "Top beaches of X" heading and just the list.
        beaches_intro_obj = data.get('beaches_intro') or {}
        beaches_intro_text = beaches_intro_obj.get('el' if lang == 'el' else 'en', '')
        intro_html = ''
        if beaches_intro_text:
            paras = [p.strip() for p in beaches_intro_text.split('\n\n') if p.strip()]
            html_paras = []
            for p in paras:
                p_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', esc(p))
                html_paras.append(f'<p>{p_html}</p>')
            intro_html = f'<div class="seo-beaches-intro">{"".join(html_paras)}</div>'
            heading = f'Best beach in {name}' if lang == 'en' else f'Καλύτερη παραλία — {name}'
        else:
            heading = f'Top beaches of {name}' if lang == 'en' else f'Κορυφαίες παραλίες — {name}'
        beach_blocks = []
        for b in beaches:
            bname = esc(pick(b, 'name', lang))
            bdesc = safe_html(pick(b, 'desc', lang))
            btype = esc(pick(b, 'type', lang))
            blen = esc(pick(b, 'length', lang))
            bdepth = esc(pick(b, 'depth', lang))
            bfacing = esc(interpret_facing(pick(b, 'facing', lang), lang,
                                            ionian=(meta.get('group') == 'Ionian')))
            bfac = esc(pick(b, 'facilities', lang))
            beach_blocks.append(f'''
<article class="seo-beach">
  <h3>{bname}</h3>
  <p>{bdesc}</p>
  <dl>
    <dt>{'Type' if lang=='en' else 'Τύπος'}</dt><dd>{btype}</dd>
    <dt>{'Length' if lang=='en' else 'Μήκος'}</dt><dd>{blen}</dd>
    <dt>{'Depth' if lang=='en' else 'Βάθος'}</dt><dd>{bdepth}</dd>
    <dt>{'Wind protection' if lang=='en' else 'Προστασία από αέρα'}</dt><dd>{bfacing}</dd>
    <dt>{'Facilities' if lang=='en' else 'Υποδομές'}</dt><dd>{bfac}</dd>
  </dl>
</article>''')
        beaches_html = f'<section class="seo-beaches"><h2>{heading}</h2>{intro_html}{"".join(beach_blocks)}</section>'

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
        # Immersive hero — same classes as the SPA hero from buildIslandPage()
        # in script.js, so the first paint matches the hydrated page (no swap
        # flash). Real <img> (.isl-hero-img) instead of a CSS background so
        # crawlers get an indexable image with alt text; same 1280 rendition
        # the SPA requests, so hydration is a cache hit.
        grp_raw = meta.get('group') or ''
        grp = (GROUP_NAMES_EL.get(grp_raw, grp_raw) if lang == 'el' else grp_raw)
        hero_tag = pick(data, 'subtitle', lang) or ''
        score_html = (f'<span class="isl-hero-score">{meta["total"]:.1f}<small>/5</small></span>'
                      if meta.get('total') else '')
        chips = []
        if meta.get('area'):
            chips.append(f'<span class="isl-chip">📍 {int(meta["area"]):,} km²</span>')
        if meta.get('pop'):
            chips.append(f'<span class="isl-chip">👥 {int(meta["pop"]):,}</span>')
        if meta.get('days'):
            chips.append(f'<span class="isl-chip">🗓 {int(meta["days"])} {"μέρες" if lang == "el" else "days"}</span>')
        if meta.get('has_airport'):
            chips.append(f'<span class="isl-chip">✈ {"Αεροδρόμιο" if lang == "el" else "Airport"}</span>')
        car_lbl = CAR_LABELS['el' if lang == 'el' else 'en'][round(meta['car_need'])] if meta.get('car_need') else ''
        if car_lbl:
            chips.append(f'<span class="isl-chip">🚗 {car_lbl}</span>')
        chips_html = f'<div class="isl-hero-chips">{"".join(chips)}</div>' if chips else ''
        hero_html = f'''<div class="isl-hero">
    <img class="isl-hero-img" src="{esc(hero_src_1280(hero_url))}" alt="{esc(alt)}" fetchpriority="high" width="1280" height="560">
    <div class="isl-hero-scrim"></div>
    <div class="isl-hero-body">
      {f'<div class="isl-hero-eyebrow">{esc(grp)}</div>' if grp else ''}
      <div class="isl-hero-nrow"><h1 class="isl-hero-name">{esc(name)}</h1>{score_html}</div>
      {f'<p class="isl-hero-tag">{esc(hero_tag)}</p>' if hero_tag else ''}
      {cluster_note_html(key, meta, lang)}
      {chips_html}
    </div>
  </div>'''

    # With the immersive hero the <h1> lives on the hero itself; the header
    # block below it keeps the crawlable text lines (subtitle, rating,
    # last-updated). Photo-less islands keep the original full header.
    # The hero is excluded from island auto-linking (placeholder swapped back
    # in after the pass): a link inside the hero tagline would render as a
    # default-styled link over the photo and waste the one-link-per-island
    # budget on markup that's replaced at hydration anyway.
    if hero_url:
        header_html = f'''@@ISL_HERO@@
  <div class="seo-header seo-header-under">
    {subtitle_html}
    {rating_text}
    {last_updated_html}
  </div>'''
    else:
        header_html = f'''<div class="seo-header">
    <h1>{esc(name)}</h1>
    {subtitle_html}
    {rating_text}
    {last_updated_html}
  </div>'''

    body_html = f'''
<article class="seo-island-content">
  {header_html}
  <section class="seo-intro">
    <p>{safe_html(intro)}</p>
  </section>
  {suited_for_html}
  {audience_html}
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
    linked = auto_link_islands(body_html, key, lang)
    if hero_url:
        linked = linked.replace('@@ISL_HERO@@', hero_html, 1)
    return linked

# ---------------------------------------------------------------------
# Page shell
# ---------------------------------------------------------------------
def render_page(key, data, meta, lang='en'):
    _hero_url, _ = find_hero_image(data)
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
{f'<link rel="preload" as="image" href="{esc(hero_src_1280(_hero_url))}" fetchpriority="high">' if _hero_url else ''}
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
<link rel="stylesheet" href="{asset_prefix}style.css?v=47">
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
  .isl-cluster-note {{ margin: 6px 0 0; font-size: 13.5px; color: rgba(255,255,255,.94); text-shadow: 0 1px 10px rgba(0,0,0,.5); }}
  .isl-cluster-note b {{ font-weight: 800; }}
  .seo-lastupdated {{
    color: var(--ink-3, #777); font-size: var(--text-tiny, 12px);
    margin: 2px 0 0; font-style: italic;
  }}
  .seo-lastupdated time {{ color: inherit; }}
  .seo-lastupdated strong {{ font-weight: 600; font-style: normal; color: var(--ink-2, #333); }}
  .seo-intro p {{ font-size: var(--text-sub, 18px); }}
  .seo-suited {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 24px 0;
  }}
  .seo-suited-col {{
    padding: 16px 18px; border-radius: 10px;
    border: 1px solid #e5e5e5; background: #fff;
  }}
  .seo-suited-col:first-child {{ border-left: 3px solid #2E7D32; }}
  .seo-suited-col:last-child {{ border-left: 3px solid #C0522A; }}
  .seo-suited-col h2 {{
    font-size: 14px; text-transform: uppercase; letter-spacing: 0.05em;
    margin: 0 0 10px;
  }}
  .seo-suited-col:first-child h2 {{ color: #2E7D32; }}
  .seo-suited-col:last-child h2 {{ color: #C0522A; }}
  .seo-suited-col ul {{ margin: 0; padding-left: 18px; }}
  .seo-suited-col li {{
    font-size: 14px; line-height: 1.55; color: #444; margin-bottom: 6px;
  }}
  @media (max-width: 600px) {{
    .seo-suited {{ grid-template-columns: 1fr; gap: 12px; }}
  }}
  .seo-hero {{ margin: 16px 0 24px; }}
  .seo-hero img {{ display: block; box-shadow: 0 2px 12px rgba(0,0,0,0.10); }}
  .seo-itinerary, .seo-beaches, .seo-related, .seo-getting-there, .seo-local, .seo-audience {{ margin-top: 36px; }}
  .seo-itinerary h2, .seo-beaches h2, .seo-related h2, .seo-getting-there h2, .seo-local h2, .seo-audience h2 {{
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
  /* Detailed getting_there paragraphs (when getting_there.detailed is present).
     Inline **strong** acts as subheaders inside the prose. */
  .seo-getting-there p {{
    margin: 0 0 14px;
    font-size: var(--text-body, 16px);
    line-height: 1.65;
    color: var(--ink-2, #333);
  }}
  .seo-getting-there p strong {{
    color: var(--ink-1, #222);
    display: inline;
  }}
  /* Audience pitches ("X for families/couples/hikers/..."). Same long-form
     prose style as the detailed getting_there variant. */
  .seo-audience p {{
    margin: 0 0 14px;
    font-size: var(--text-body, 16px);
    line-height: 1.65;
    color: var(--ink-2, #333);
  }}
  .seo-audience p strong {{
    color: var(--ink-1, #222);
    display: inline;
  }}
  /* beaches_intro: the declarative top-pick prose above the per-beach list */
  .seo-beaches-intro p {{
    margin: 0 0 14px;
    font-size: var(--text-body, 16px);
    line-height: 1.65;
    color: var(--ink-2, #333);
  }}
  .seo-beaches-intro p strong {{ color: var(--ink-1, #222); }}
  .seo-beaches-intro p:last-child {{ margin-bottom: 18px; }}
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

  /* Top nav — styled to match the main SPA header (teal gradient banner)
     while keeping the minimal 4-link layout. So someone coming from search
     gets the same visual brand presence as the live site. */
  .seo-nav {{
    background: linear-gradient(135deg, #0B8FAC 0%, #076880 100%);
    box-shadow: 0 2px 12px rgba(11,143,172,0.25);
    border-bottom: none;
    position: sticky; top: 0; z-index: 1000;
    margin-bottom: 0;
  }}
  .seo-nav-inner {{
    max-width: 1280px; margin: 0 auto; padding: 14px 24px;
    display: flex; justify-content: space-between; align-items: center;
    font-family: var(--sans, sans-serif);
  }}
  .seo-nav-brand {{
    display: flex; align-items: center; gap: 12px;
    text-decoration: none; color: #fff; font-weight: 700;
    font-family: var(--serif, Georgia, serif);
    font-size: 20px;
  }}
  .seo-nav-brand img {{
    width: 40px; height: 40px;
  }}
  .seo-nav-brand:hover {{ opacity: 0.92; color: #fff; text-decoration: none; }}
  .seo-nav-links {{ display: flex; gap: 24px; align-items: center; }}
  .seo-nav-links a {{
    color: #fff; text-decoration: none; font-weight: 600;
    font-size: var(--text-small, 14px);
    opacity: 0.95;
    transition: opacity 0.15s;
  }}
  .seo-nav-links a:hover {{ opacity: 1; text-decoration: underline; color: #fff; }}
  .seo-nav-lang {{
    background: none; border: 1px solid rgba(255,255,255,0.4);
    color: #fff; padding: 4px 10px; border-radius: 4px;
    text-decoration: none; font-size: 13px; white-space: nowrap;
    margin-left: 8px;
  }}
  .seo-nav-lang:hover {{
    background: rgba(255,255,255,0.12); color: #fff; text-decoration: none;
  }}
  @media (max-width: 600px) {{
    .seo-nav-inner {{ flex-direction: column; gap: 10px; padding: 12px 16px; }}
    .seo-nav-links {{ gap: 14px; font-size: var(--text-meta, 13px); flex-wrap: wrap; justify-content: center; }}
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
<script async data-cfasync="false" data-noptimize="1" data-no-defer="1" src="https://emrldtp.com/NTUxOTU3.js?t=551957"></script>
</head>
<body data-island-key="{key}" data-lang="{lang}">

<!-- Top navigation bar — teal banner matching the main SPA header -->
<nav class="seo-nav">
  <div class="seo-nav-inner">
    <a href="{('/' if lang == 'en' else '/el/')}" class="seo-nav-brand">
      <img src="/logo-hero.svg" alt="Aegean Blueprint" width="40" height="40">
      <span>Aegean Blueprint</span>
    </a>
    <div class="seo-nav-links">
      <a href="{('/' if lang == 'en' else '/el/')}#data">{'All Islands' if lang == 'en' else 'Όλα τα Νησιά'}</a>
      <a href="{('/' if lang == 'en' else '/el/')}#compare">{'Compare' if lang == 'en' else 'Σύγκριση'}</a>
      <a href="{('/' if lang == 'en' else '/el/')}#match">{'Quiz' if lang == 'en' else 'Quiz'}</a>
      <a href="{(f'/el/island/{key}/' if lang == 'en' else f'/island/{key}/')}" class="seo-nav-lang">
        🌐 {'EL' if lang == 'en' else 'EN'}
      </a>
    </div>
  </div>
</nav>

<!-- The page now hydrates into the full SPA experience. The SEO content
     below (#seo-fallback) is what crawlers see; once the SPA boots, it
     populates the hidden <main id="view-detail"> skeleton and a small
     bootstrap script swaps them — no flash, full interactivity.
     Tag '{key}' is the island key the SPA needs for routing. -->
<div id="seo-fallback">
{body}

<!-- Call-to-action to get users into the interactive SPA -->
<div class="seo-cta-box">
  <h3>{'Want to compare islands or take the matching quiz?' if lang == 'en' else 'Θέλεις να συγκρίνεις νησιά ή να κάνεις το quiz;'}</h3>
  <p>{'Our interactive tools help you filter, compare side-by-side, and find the perfect island for your trip.' if lang == 'en' else 'Τα διαδραστικά μας εργαλεία σε βοηθούν να φιλτράρεις, να συγκρίνεις και να βρεις το ιδανικό νησί.'}</p>
  <div class="seo-cta-buttons">
    <a href="{('/' if lang == 'en' else '/el/')}#compare" class="seo-cta-btn">{'↔ Compare islands' if lang == 'en' else '↔ Σύγκρινε νησιά'}</a>
    <a href="{('/match/' if lang == 'en' else '/el/match/')}" class="seo-cta-btn">{'🎯 Take the quiz' if lang == 'en' else '🎯 Κάνε το quiz'}</a>
    <a href="{('/' if lang == 'en' else '/el/')}" class="seo-cta-btn">{'🗺 Explore map' if lang == 'en' else '🗺 Εξερεύνησε χάρτη'}</a>
    <a href="{('/trip-cost/' if lang == 'en' else '/el/trip-cost/')}?i={key}:{int(meta.get('days') or 3)}" class="seo-cta-btn">{f"💶 What do {int(meta.get('days') or 3)} days here cost?" if lang == 'en' else f"💶 Πόσο κοστίζουν {int(meta.get('days') or 3)} μέρες εδώ;"}</a>
  </div>
</div>

<!-- Footer -->
<footer class="seo-footer">
  <p>© 2026 Aegean Blueprint · <a href="{('/el/island/' if lang == 'en' else '/island/')}{key}/">{'Ελληνικά' if lang == 'en' else 'English'}</a> · <a href="{'/privacy/' if lang == 'en' else '/el/privacy/'}">{'Privacy' if lang == 'en' else 'Απόρρητο'}</a> · <a href="{'/#mission' if lang == 'en' else '/el/#mission'}">{'Mission' if lang == 'en' else 'Στόχος'}</a></p>
</footer>
</div><!-- /#seo-fallback -->

<!-- SPA view-detail skeleton — populated by script.js renderIslandPage(),
     hidden until hydration kicks in (display:none below is removed by the
     SPA after it boots). Mirrors the structure in /index.html exactly. -->
<main id="view-detail" class="view-section" style="display:none;">
  <div class="detail-container">
    <div class="detail-grid">

      <div class="detail-hero-wrap">
        <div id="island-hero-slot"></div>
        <div class="detail-hero-top">
          <button class="glass-btn detail-back-glass" id="detail-back-btn" data-i18n="detail.back">{'← Back to Map' if lang == 'en' else '← Πίσω στον Χάρτη'}</button>
          <div class="detail-hero-actions">
            <button class="glass-btn glass-ic" id="detail-shortlist-btn" onclick="toggleShortlist()" title="{'Save' if lang == 'en' else 'Αποθήκευση'}" aria-label="{'Save' if lang == 'en' else 'Αποθήκευση'}">☆</button>
            <button class="glass-btn glass-ic" id="detail-compare-btn" title="{'Compare' if lang == 'en' else 'Σύγκρινε'}" aria-label="{'Compare' if lang == 'en' else 'Σύγκρινε'}">⇄</button>
            <button class="glass-btn glass-ic" id="detail-share-btn" onclick="copyIslandLink()" title="{'Copy link' if lang == 'en' else 'Αντιγραφή'}" aria-label="{'Copy link' if lang == 'en' else 'Αντιγραφή'}">↗</button>
          </div>
        </div>
        <h2 id="island-name" hidden></h2>
        <div class="island-meta-pill" id="island-meta-info" hidden></div>
      </div>

      <div class="detail-actionbar">
        <a class="ferry-btn" id="detail-ferry-btn" target="_blank" rel="noopener" data-i18n="detail.bookferry">{'🚢 Book ferry tickets' if lang == 'en' else '🚢 Κράτηση πλοίου'}</a>
        <a class="car-btn" id="detail-car-btn" target="_blank" rel="noopener sponsored" data-i18n="detail.rentcar">{'🚗 Rent a car' if lang == 'en' else '🚗 Ενοικίαση αυτοκινήτου'}</a>
        <span class="actionbar-spacer"></span>
        <button class="glass-ic-solid" id="detail-print-btn" onclick="printIsland()" title="{'Print' if lang == 'en' else 'Εκτύπωση'}" aria-label="{'Print' if lang == 'en' else 'Εκτύπωση'}">🖨</button>
      </div>

      <div class="detail-main">
        <div id="island-mini-map"></div>
        <div id="island-guide"></div>
      </div>

      <aside class="detail-sidebar">
        <div class="sidebar-box blueprint-box">
          <div class="blueprint-eyebrow" data-i18n="detail.ratings">{'Blueprint Ratings' if lang == 'en' else 'Βαθμολογίες'}</div>
          <div class="blueprint-scorerow">
            <svg class="blueprint-ring" viewBox="0 0 70 70" width="62" height="62" aria-hidden="true">
              <circle cx="35" cy="35" r="30" fill="none" stroke="var(--marble-2)" stroke-width="7"></circle>
              <circle id="blueprint-ring-fill" cx="35" cy="35" r="30" fill="none" stroke="var(--aegean)" stroke-width="7" stroke-linecap="round" stroke-dasharray="188.5" stroke-dashoffset="188.5" transform="rotate(-90 35 35)"></circle>
              <text id="blueprint-ring-num" x="35" y="41" text-anchor="middle" font-family="Nunito, sans-serif" font-weight="800" font-size="19" fill="var(--ink-1)">–</text>
            </svg>
            <div class="blueprint-verdict">
              <span class="blueprint-verdict-main" id="blueprint-verdict"></span>
              <span class="blueprint-verdict-sub" id="blueprint-verdict-sub"></span>
            </div>
          </div>
          <a href="#how-we-score" onclick="navMission(event)" class="how-we-score-link" data-i18n="scoring.howlink">{'how we score' if lang == 'en' else 'πώς βαθμολογούμε'}</a>
          <div class="rating-list">
            <div class="rating-item"><span class="rating-label" data-i18n="sidebar.beach">{'Beach Quality' if lang == 'en' else 'Παραλίες'}</span><div class="stars-outer"><div id="star-beach" class="stars-inner"></div></div><span class="rating-val" id="val-beach"></span></div>
            <div class="rating-item"><span class="rating-label" data-i18n="sidebar.culture">{'Culture &amp; History' if lang == 'en' else 'Πολιτισμός'}</span><div class="stars-outer"><div id="star-hist" class="stars-inner"></div></div><span class="rating-val" id="val-hist"></span></div>
            <div class="rating-item"><span class="rating-label" data-i18n="sidebar.night">{'Night Life' if lang == 'en' else 'Νυχτερινή Ζωή'}</span><div class="stars-outer"><div id="star-night" class="stars-inner"></div></div><span class="rating-val" id="val-night"></span></div>
            <div class="rating-item"><span class="rating-label" data-i18n="sidebar.access">{'Access Ease' if lang == 'en' else 'Πρόσβαση'}</span><div class="stars-outer"><div id="star-access" class="stars-inner"></div></div><span class="rating-val" id="val-access"></span></div>
            <div class="rating-item"><span class="rating-label" data-i18n="sidebar.afford">{'Price Level' if lang == 'en' else 'Επίπεδο Τιμών'}</span><div class="stars-outer"><div id="star-afford" class="stars-inner"></div></div><span class="rating-val" id="val-afford"></span></div>
            <div class="rating-item rating-item-car" title="" id="rating-item-car"><span class="rating-label" data-i18n="sidebar.car">{'Car reliance' if lang == 'en' else 'Ανάγκη Αυτοκινήτου'}</span><span class="rating-val" id="val-car"></span></div>
          </div>
          <div class="blueprint-divider"></div>
          <div id="sidebar-stats" class="blueprint-stats">
            <div class="stat-line"><span data-i18n="detail.area">{'Land Area:' if lang == 'en' else 'Έκταση:'}</span> <strong id="stat-area"></strong></div>
            <div class="stat-line"><span data-i18n="detail.population">{'Population:' if lang == 'en' else 'Πληθυσμός:'}</span> <strong id="stat-pop"></strong></div>
            <div class="stat-line"><span data-i18n="detail.group">{'Group:' if lang == 'en' else 'Νησιωτικό Σύμπλεγμα:'}</span> <strong id="stat-group"></strong></div>
            <div class="stat-line"><span data-i18n="detail.suggestedstay">{'Suggested stay:' if lang == 'en' else 'Προτεινόμενη Διαμονή:'}</span> <strong id="stat-days"></strong></div>
          </div>
        </div>
      </aside>

    </div>
  </div>
</main>

<!-- SPA hydration — load Leaflet + Chart.js + i18n + script.js, then swap
     the SEO fallback for the hydrated view-detail. The home-base URL for
     the back button is overridden because the SPA's default 'navigateTo
     home' just sets a hash on the current path, which would re-trigger
     this island page. -->
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="{asset_prefix}i18n.js?v=42"></script>
<script src="{asset_prefix}script.js?v=69"></script>
<script>
  // Static-page hydration handoff: once script.js loads and renderIslandPage
  // populates view-detail, hide the SEO fallback and show view-detail.
  // Polls up to 10 seconds (50 attempts × 200ms) — should be more than enough
  // even on slow connections. If polling exhausts, logs a diagnostic so we
  // can see why the SPA didn't populate.
  (function() {{
    var ISLAND_KEY = '{key}';
    function tryHandoff() {{
      var detail = document.getElementById('view-detail');
      var nameEl = document.getElementById('island-name');
      // Hand off only once the SPA has actually populated the island name
      // — that's the signal that renderIslandPage() finished.
      if (detail && nameEl && nameEl.textContent.trim()) {{
        document.getElementById('seo-fallback').style.display = 'none';
        detail.style.display = '';
        // Override the back button to go to the actual homepage URL,
        // not just push a hash on the current path (which would re-trigger).
        var backBtn = document.getElementById('detail-back-btn');
        if (backBtn) {{
          backBtn.onclick = function(e) {{
            if (e) e.preventDefault();
            window.location.href = '{('/' if lang == 'en' else '/el/')}';
          }};
        }}
        return true;
      }}
      return false;
    }}
    var attempts = 0;
    var iv = setInterval(function() {{
      if (tryHandoff()) {{
        clearInterval(iv);
      }} else if (++attempts > 50) {{
        clearInterval(iv);
        console.warn('[hydration] handoff did not complete in 10s. Island:', ISLAND_KEY);
      }}
    }}, 200);
  }})();
</script>
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
def generate_ferries_page(island_keys):
    """Build a static ferries hub page (EN + EL) at /ferries/index.html.

    Pulls the FERRY_GRAPH array out of script.js by regex — single source of
    truth, no data duplication. Builds a sortable table of all ferry routes
    departing from each mainland port (Piraeus, Rafina, Lavrio, Patras, etc.).

    Why static HTML rather than another SPA view: this page targets generic
    queries like "ferries from Athens to Greek islands" and needs to be a
    real indexable URL, not a `#hash`. Same approach as /festivals/.
    """
    # Parse FERRY_GRAPH out of script.js. Each entry looks like:
    #   { a: 'piraeus', b: 'mykonos', dur: 285, freq: 'high', plo: 30, phi: 65, note: "..." },
    script_path = ROOT / 'script.js'
    script_text = script_path.read_text(encoding='utf-8')
    graph_block_match = re.search(r'const FERRY_GRAPH = \[([\s\S]+?)\n\];', script_text)
    if not graph_block_match:
        print('  ⚠  Could not find FERRY_GRAPH in script.js — skipping ferries page')
        return 0
    block = graph_block_match.group(1)
    routes = []
    # Each route line:  { a: 'piraeus', b: 'mykonos', dur: 285, freq: 'high', plo: 30, phi: 65, note: "..." }
    for m in re.finditer(
        r"\{\s*a:\s*'([^']+)',\s*b:\s*'([^']+)',\s*dur:\s*(\d+),\s*freq:\s*'(\w+)',\s*plo:\s*(\d+),\s*phi:\s*(\d+)(?:,\s*note:\s*\"([^\"]*)\")?",
        block
    ):
        routes.append({
            'a': m.group(1), 'b': m.group(2),
            'dur': int(m.group(3)),
            'freq': m.group(4),
            'plo': int(m.group(5)), 'phi': int(m.group(6)),
            'note': m.group(7) or '',
        })
    if not routes:
        print('  ⚠  FERRY_GRAPH parsed empty — skipping ferries page')
        return 0

    # Pull a mapping of island-key → display name from ISLANDS_DATA (also in script.js).
    # Quick-and-dirty: regex out each `"key": { name:"Name", ...`.
    isl_block_match = re.search(r'const ISLANDS_DATA = \{([\s\S]+?)\n\};', script_text)
    name_map = {}
    if isl_block_match:
        for m in re.finditer(r'"([\w-]+)":\s*\{\s*name:\s*"([^"]+)"', isl_block_match.group(1)):
            name_map[m.group(1)] = m.group(2)

    # Hand-curated mainland-port labels (these aren't in ISLANDS_DATA — they're departure ports)
    PORT_LABELS = {
        'piraeus':  {'en': 'Piraeus',  'el': 'Πειραιάς'},
        'rafina':   {'en': 'Rafina',   'el': 'Ραφήνα'},
        'lavrio':   {'en': 'Lavrio',   'el': 'Λαύριο'},
        'patras':   {'en': 'Patras',   'el': 'Πάτρα'},
        'kyllini':  {'en': 'Kyllini',  'el': 'Κυλλήνη'},
        'igoumenitsa': {'en': 'Igoumenitsa', 'el': 'Ηγουμενίτσα'},
        'alexandroupoli': {'en': 'Alexandroupoli', 'el': 'Αλεξανδρούπολη'},
        'kavala':   {'en': 'Kavala',   'el': 'Καβάλα'},
        'volos':    {'en': 'Volos',    'el': 'Βόλος'},
        'agios-konstantinos': {'en': 'Agios Konstantinos', 'el': 'Άγιος Κωνσταντίνος'},
        'thessaloniki': {'en': 'Thessaloniki', 'el': 'Θεσσαλονίκη'},
        'neapoli':  {'en': 'Neapoli (Voion)', 'el': 'Νεάπολη (Βοιών)'},
        'gythio':   {'en': 'Gythio',   'el': 'Γύθειο'},
        'pounta':   {'en': 'Pounta',   'el': 'Πούντα'},
        'perama':   {'en': 'Perama',   'el': 'Πέραμα'},
    }

    # The mainland ports we care about — order matters for the page sections
    MAINLAND_ORDER = ['piraeus', 'rafina', 'lavrio', 'patras', 'kyllini',
                      'igoumenitsa', 'agios-konstantinos', 'volos',
                      'thessaloniki', 'kavala', 'alexandroupoli',
                      'neapoli', 'gythio']
    # Routes grouped by origin (mainland port)
    routes_by_origin = {}
    for r in routes:
        if r['a'] in MAINLAND_ORDER:
            routes_by_origin.setdefault(r['a'], []).append(r)
    # Sort each origin's routes by duration ascending (quickest first)
    for o in routes_by_origin:
        routes_by_origin[o].sort(key=lambda r: r['dur'])

    def fmt_duration(mins):
        if mins < 60:
            return f'{mins} min'
        h = mins // 60
        m = mins % 60
        return f'{h}h {m:02d}m' if m else f'{h}h'

    def fmt_freq(freq, lang):
        labels = {
            'en': {'high': 'Daily+', 'med': 'Most days', 'low': '2-4/week'},
            'el': {'high': 'Καθημερινά+', 'med': 'Σχεδόν καθημερινά', 'low': '2-4/εβδ.'}
        }
        return labels[lang].get(freq, freq)

    def island_link(key, lang):
        """Return an HTML link to the island detail page; falls back to plain text."""
        name = name_map.get(key, key.title())
        # Mainland port — render as plain text
        if key in PORT_LABELS:
            return esc(PORT_LABELS[key][lang])
        # Some island keys are valid; some (eg 'piraeus') aren't
        if key in island_keys:
            path = f'/el/island/{key}/' if lang == 'el' else f'/island/{key}/'
            return f'<a href="{path}">{esc(name)}</a>'
        return esc(name)

    # Build the page for each language
    island_count = len(island_keys)
    for lang in ['en', 'el']:
        is_el = (lang == 'el')
        if is_el:
            title = 'Πλοία προς τα Ελληνικά Νησιά από Αθήνα — όλες οι διαδρομές | Aegean Blueprint'
            description = f'Πλοία από Πειραιά, Ραφήνα και Λαύριο προς {island_count} νησιά. Διάρκεια, συχνότητα, τιμές. Ενημερωμένος οδηγός για το 2026.'
            intro = ('Σχεδόν όλα τα νησιά του Αιγαίου και του Ιονίου είναι προσβάσιμα με πλοίο '
                     'από την Αθήνα — αλλά το λιμάνι έναρξης κάνει μεγάλη διαφορά. Ο '
                     '<strong>Πειραιάς</strong> εξυπηρετεί τα περισσότερα Κυκλάδες, Δωδεκάνησα, '
                     'Κρήτη και την υπόλοιπη Ελλάδα — είναι το μεγάλο λιμάνι, με μεγαλύτερες '
                     'ουρές και πιο αργές διαδρομές. Η <strong>Ραφήνα</strong> είναι μικρότερη, '
                     'γρηγορότερη για τις βόρειες Κυκλάδες (Άνδρος, Τήνος, Μύκονος, Πάρος, Νάξος). '
                     'Το <strong>Λαύριο</strong> εξυπηρετεί λίγες αλλά συγκεκριμένες προορισμούς '
                     '(Κέα, Κύθνος και την οδηγική σύνδεση προς τις βόρειες Κυκλάδες).')
            port_subtitle = 'Διαδρομές από κάθε λιμάνι'
            head_dest = 'Προορισμός'
            head_dur = 'Διάρκεια'
            head_freq = 'Συχνότητα'
            head_price = 'Τιμή (€)'
            head_note = 'Σημείωση'
            booking_intro = ('<strong>Κρατήσεις:</strong> Για τις περισσότερες διαδρομές μπορείς '
                             'να αγοράσεις εισιτήριο επί τόπου στο λιμάνι την ίδια μέρα. Το '
                             'καλοκαίρι έχει κίνηση — έλα 60-90 λεπτά πριν την αναχώρηση. '
                             'Για κράτηση online συνιστούμε το ')
            ferryhopper_link = '<a href="https://www.ferryhopper.com/" target="_blank" rel="noopener">Ferryhopper</a>.'
            crosslink_text = ('Σχεδιάζεις διαδρομή πολλαπλών νησιών; Δες τον '
                              '<a href="/el/#hopping">διαδραστικό χάρτη και σχεδιαστή διαδρομών</a> '
                              'και τις <a href="/el/#hopping">προτεινόμενες διαδρομές νησοπορίας</a>.')
        else:
            title = 'Ferries from Athens to the Greek Islands — all routes | Aegean Blueprint'
            description = f'Ferries from Piraeus, Rafina, and Lavrio to {island_count} islands. Duration, frequency, fare. Up-to-date guide for 2026.'
            intro = ('Almost every Aegean and Ionian island is reachable by ferry from Athens — '
                     'but the departure port matters. <strong>Piraeus</strong> serves most '
                     'Cyclades, Dodecanese, Crete, and northern Aegean — it\'s the big port, '
                     'with longer queues and (usually) slower overnight ferries. '
                     '<strong>Rafina</strong> is smaller, quicker for the northern Cyclades '
                     '(Andros, Tinos, Mykonos, Paros, Naxos), and worth the slight drive from '
                     'central Athens if you\'re heading there. <strong>Lavrio</strong> serves '
                     'a few specific destinations (Kea, Kythnos, and the driving connection '
                     'to the northern Cyclades).')
            port_subtitle = 'Routes from each port'
            head_dest = 'Destination'
            head_dur = 'Duration'
            head_freq = 'Frequency'
            head_price = 'Price (€)'
            head_note = 'Notes'
            booking_intro = ('<strong>Booking:</strong> For most routes, you can buy your ticket '
                             'at the port the same day. Summer is busier — arrive 60-90 minutes '
                             'before departure. For online booking we recommend ')
            ferryhopper_link = '<a href="https://www.ferryhopper.com/" target="_blank" rel="noopener">Ferryhopper</a>.'
            crosslink_text = ('Planning a multi-island hop? See our '
                              '<a href="/#hopping">interactive ferry network map and route planner</a> '
                              'and <a href="/#hopping">curated island-hopping itineraries</a>.')

        # Build port sections
        port_sections = []
        for port in MAINLAND_ORDER:
            port_routes = routes_by_origin.get(port, [])
            if not port_routes:
                continue
            port_name = PORT_LABELS[port][lang]
            rows = []
            for r in port_routes:
                # Skip mainland-to-mainland (e.g. Piraeus → Perama)
                if r['b'] in PORT_LABELS and r['b'] not in island_keys:
                    continue
                rows.append(
                    '<tr>'
                    f'<td class="ferry-dest">{island_link(r["b"], lang)}</td>'
                    f'<td>{fmt_duration(r["dur"])}</td>'
                    f'<td>{fmt_freq(r["freq"], lang)}</td>'
                    f'<td>€{r["plo"]}-{r["phi"]}</td>'
                    f'<td class="ferry-note">{esc(r["note"])}</td>'
                    '</tr>'
                )
            if not rows:
                continue
            port_anchor = f'port-{port}'
            port_sections.append(
                f'<section class="ferry-port" id="{port_anchor}">'
                f'<h2>{esc(port_name)}</h2>'
                '<div class="ferry-table-wrap"><table class="ferry-table">'
                # colgroup makes table-layout:fixed work — column widths come
                # from the col elements, not from inspecting cell content.
                '<colgroup>'
                '<col class="ferry-col-dest">'
                '<col class="ferry-col-dur">'
                '<col class="ferry-col-freq">'
                '<col class="ferry-col-price">'
                '<col class="ferry-col-note">'
                '</colgroup>'
                f'<thead><tr><th>{head_dest}</th><th>{head_dur}</th><th>{head_freq}</th><th>{head_price}</th><th>{head_note}</th></tr></thead>'
                f'<tbody>{"".join(rows)}</tbody>'
                '</table></div>'
                '</section>'
            )

        # Quick-jump nav to each port section
        port_nav_items = []
        for port in MAINLAND_ORDER:
            if routes_by_origin.get(port):
                port_nav_items.append(
                    f'<a href="#port-{port}">{esc(PORT_LABELS[port][lang])}</a>'
                )
        port_nav = ' · '.join(port_nav_items)

        url_en = f'{SITE_URL}/ferries/'
        url_el = f'{SITE_URL}/el/ferries/'
        url = url_el if is_el else url_en

        nav_label_map = {
            'map':       ('Map',       'Χάρτης'),
            'data':      ('Islands Data', 'Στοιχεία Νησιών'),
            'compare':   ('Compare',   'Σύγκριση'),
            'festivals': ('Festivals', 'Γιορτές'),
            'ferries':   ('Ferries',   'Πλοία'),
            'hopping':   ('Ferries & Hopping', 'Πλοία & Νησοπορία'),
            'match':     ('Match Me', 'Βρες το Νησί σου'),
            'tripcost':  ('Budget', 'Μπάτζετ'),
            'shortlist': ('⭐ My Shortlist', '⭐ Η Λίστα μου'),
            'mission':   ('Mission',   'Στόχος'),
            'privacy':   ('Privacy',   'Απόρρητο'),
        }
        def navlbl(k):
            return nav_label_map[k][1 if is_el else 0]

        html_out = (
            '<!DOCTYPE html>\n'
            f'<html lang="{"el" if is_el else "en"}">\n'
            '<head>\n'
            '<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f'<title>{esc(title)}</title>\n'
            f'<meta name="description" content="{esc(description)}">\n'
            '<meta name="theme-color" content="#0B8FAC">\n'
            '<meta name="author" content="Stergios Gousios">\n'
            f'<link rel="canonical" href="{url}">\n'
            f'<link rel="alternate" hreflang="en" href="{url_en}">\n'
            f'<link rel="alternate" hreflang="el" href="{url_el}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{url_en}">\n'
            '<link rel="icon" href="/favicon.ico" sizes="any">\n'
            '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
            '<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">\n'
            '<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png">\n'
            '<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">\n'
            '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
            '<meta name="apple-mobile-web-app-title" content="Aegean Blueprint">\n'
            '<link rel="manifest" href="/site.webmanifest">\n'
            '<meta property="og:type" content="website">\n'
            f'<meta property="og:title" content="{esc(title)}">\n'
            f'<meta property="og:description" content="{esc(description)}">\n'
            f'<meta property="og:url" content="{url}">\n'
            f'<meta property="og:locale" content="{"el_GR" if is_el else "en_US"}">\n'
            '<script>if(localStorage.getItem("darkMode")==="true"){document.documentElement.classList.add("dark");}</script>\n'
            '<link rel="stylesheet" href="/style.css">\n'
            '<style>\n'
            '  body { background: var(--bg, #fff); color: var(--ink, #222); font-family: var(--sans, system-ui), sans-serif; margin: 0; }\n'
            '  .ferry-page { max-width: 1100px; margin: 0 auto; padding: 32px 24px 64px; }\n'
            '  .ferry-page > h1 { font-family: var(--serif, Georgia), serif; font-size: 36px; margin: 0 0 8px; }\n'
            '  .ferry-intro { font-size: 17px; color: var(--ink-1, #444); line-height: 1.55; margin: 0 0 24px; max-width: 760px; }\n'
            '  .ferry-nav { background: var(--marble, #f6f4ee); padding: 12px 16px; border-radius: 12px; font-size: 14px; margin-bottom: 32px; line-height: 1.8; }\n'
            '  .ferry-nav-label { display: block; font-weight: 700; color: var(--ink-2, #333); margin-bottom: 4px; }\n'
            '  .ferry-nav a { color: var(--aegean-dark, #076880); text-decoration: none; font-weight: 600; }\n'
            '  .ferry-nav a:hover { text-decoration: underline; }\n'
            '  .ferry-port { margin-bottom: 40px; }\n'
            '  .ferry-port h2 { font-family: var(--serif, Georgia), serif; font-size: 26px; margin: 0 0 16px; padding-bottom: 6px; border-bottom: 2px solid var(--aegean, #0B8FAC); }\n'
            '  .ferry-table-wrap { overflow-x: auto; }\n'
            '  /* table-layout: fixed + explicit column widths ensures all tables\n'
            '     across port sections share the same column proportions, regardless\n'
            '     of content length. Without this, each table auto-sizes its columns\n'
            '     to its own content, so a section with short notes ends up with\n'
            '     much narrower columns than one with long notes — looks broken. */\n'
            '  .ferry-table { width: 100%; border-collapse: collapse; font-size: 14px; table-layout: fixed; }\n'
            '  .ferry-table col.ferry-col-dest  { width: 25%; }\n'
            '  .ferry-table col.ferry-col-dur   { width: 12%; }\n'
            '  .ferry-table col.ferry-col-freq  { width: 14%; }\n'
            '  .ferry-table col.ferry-col-price { width: 12%; }\n'
            '  .ferry-table col.ferry-col-note  { width: 37%; }\n'
            '  .ferry-table thead th { text-align: left; padding: 10px 12px; background: var(--marble, #f6f4ee); color: var(--ink-2, #333); font-weight: 700; border-bottom: 2px solid var(--border, #e5e1d8); white-space: nowrap; }\n'
            '  .ferry-table tbody td { padding: 10px 12px; border-bottom: 1px solid var(--border, #eee); vertical-align: top; word-wrap: break-word; overflow-wrap: break-word; }\n'
            '  .ferry-table tbody tr:hover { background: var(--aegean-pale, rgba(11,143,172,0.05)); }\n'
            '  .ferry-table a { color: var(--aegean-dark, #076880); font-weight: 600; text-decoration: none; }\n'
            '  .ferry-table a:hover { text-decoration: underline; }\n'
            '  .ferry-dest { font-weight: 600; }\n'
            '  .ferry-note { color: var(--ink-3, #888); font-size: 13px; }\n'
            '  .ferry-footer { background: var(--marble, #f6f4ee); padding: 20px 24px; border-radius: 12px; font-size: 15px; line-height: 1.6; color: var(--ink-1, #444); margin-top: 32px; }\n'
            '  .ferry-footer p { margin: 0; }\n'
            '  .ferry-footer a { color: var(--aegean-dark, #076880); font-weight: 600; }\n'
            '  @media (max-width: 600px) {\n'
            '    .ferry-page { padding: 20px 16px 48px; }\n'
            '    .ferry-page > h1 { font-size: 28px; }\n'
            '    .ferry-table thead th, .ferry-table tbody td { padding: 8px 6px; font-size: 13px; }\n'
            '    .ferry-note { display: none; }\n'  # Notes are hidden on mobile — saves horizontal space.
            '  }\n'
            '  html.dark body { background: #1a1a1a; color: #eee; }\n'
            '  html.dark .ferry-table thead th { background: #2a2a2a; border-bottom-color: #444; }\n'
            '  html.dark .ferry-table tbody td { border-bottom-color: #333; }\n'
            '  html.dark .ferry-table tbody tr:hover { background: rgba(11,143,172,0.12); }\n'
            '  html.dark .ferry-nav, html.dark .ferry-footer { background: #2a2a2a; }\n'
            '</style>\n'
            '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9298260273942245" crossorigin="anonymous"></script>\n'
            '<script>\n'
            '  (function(){ if (window.matchMedia(\'(max-width: 899.98px)\').matches) { window.adsbygoogle = window.adsbygoogle || []; window.adsbygoogle.push = function(){}; } })();\n'
            '</script>\n'
            '<script async data-cfasync="false" data-noptimize="1" data-no-defer="1" src="https://emrldtp.com/NTUxOTU3.js?t=551957"></script>\n'
            '</head>\n<body>\n'
            '<header>\n'
            '  <div class="header-content">\n'
            f'    <a class="logo-wrapper" href="/{"el/" if is_el else ""}" style="text-decoration: none;">\n'
            '      <img src="/logo-hero.svg" id="site-logo" alt="Aegean Blueprint logo">\n'
            '      <span id="brand-text"><span class="brand-word">Aegean</span> <span class="brand-word">Blueprint</span></span>\n'
            '    </a>\n'
            '    <div class="menu-toggle" id="menu-toggle-btn"><span></span><span></span><span></span></div>\n'
            '    <nav class="top-nav" id="main-nav">\n'
            f'      <a href="/{"el/" if is_el else ""}#compare">{navlbl("compare")}</a>\n'
            f'      <a href="/{"el/" if is_el else ""}#match">{navlbl("match")}</a>\n'
            f'      <a href="/{"el/" if is_el else ""}trip-cost/">{navlbl("tripcost")}</a>\n'
            f'      <a href="/{"el/" if is_el else ""}#hopping" class="active">{navlbl("hopping")}</a>\n'
            f'      <a href="/{"el/" if is_el else ""}festivals/">{navlbl("festivals")}</a>\n'
            f'      <a href="/{"el/" if is_el else ""}#data">{navlbl("data")}</a>\n'
            f'      <a href="/{"el/" if is_el else ""}#mission">{navlbl("mission")}</a>\n'
            f'      <a href="/{"el/" if is_el else ""}#shortlist">{navlbl("shortlist")}</a>\n'
            '    </nav>\n'
            f'    <a class="lang-toggle-static" href="{"/ferries/" if is_el else "/el/ferries/"}" style="background: none; border: 1px solid rgba(255,255,255,0.4); color: #fff; padding: 4px 10px; border-radius: 4px; text-decoration: none; font-size: 13px; white-space: nowrap;">'
            f'<span style="margin-right: 4px;">🌐</span>{"EN" if is_el else "EL"}</a>\n'
            '  </div>\n'
            '</header>\n'
            '<main class="ferry-page">\n'
            f'  <h1>{esc(title.rsplit(" | ", 1)[0])}</h1>\n'
            f'  <p class="ferry-intro">{intro}</p>\n'
            f'  <div class="ferry-nav"><span class="ferry-nav-label">{esc(port_subtitle)}</span>{port_nav}</div>\n'
            + '\n'.join(port_sections) +
            f'\n  <div class="ferry-footer"><p>{booking_intro}{ferryhopper_link}</p><p style="margin-top: 12px;">{crosslink_text}</p></div>\n'
            '<div class="cta-affiliate"><a class="ferry-btn" href="https://www.ferryhopper.com/" target="_blank" rel="noopener sponsored">' + ('🚢 Κράτηση εισιτηρίων' if is_el else '🚢 Book ferry tickets') + '</a><a class="car-btn" href="https://www.discovercars.com/?a_aid=antaran2" target="_blank" rel="noopener sponsored">' + ('🚗 Ενοικίαση αυτοκινήτου' if is_el else '🚗 Rent a car') + '</a></div>\n'
            '</main>\n'
            '<script>\n'
            '  /* Mobile hamburger toggle */\n'
            '  document.getElementById("menu-toggle-btn").addEventListener("click", function(){ document.getElementById("main-nav").classList.toggle("open"); });\n'
            '</script>\n'
            '</body>\n</html>\n'
        )

        out_path = ROOT / ('el/ferries/index.html' if is_el else 'ferries/index.html')
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html_out, encoding='utf-8')

    return len(routes)


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

    # Build the compact "what's on now" index for the home page strip
    generate_whats_on_index(keys)
    print(f'✓ whats-on.json regenerated')

    # Build the hero-photo manifest (key -> first on-island photo) for card thumbnails
    generate_hero_photos_index(keys)
    print(f'✓ hero-photos.json regenerated')

    # Build the festivals calendar page (static HTML, EN + EL)
    n_fests = generate_festivals_page(keys)
    print(f'✓ festivals/ page regenerated ({n_fests} festivals)')

    # Build the ferries hub page (static HTML, EN + EL)
    n_routes = generate_ferries_page(keys)
    print(f'✓ ferries/ page regenerated ({n_routes} routes)')

    # Regenerate sitemap LAST — needs other generators to have run first.
    generate_sitemap(keys)
    print(f'✓ Sitemap regenerated with {len(keys)} islands + static pages')

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
        _isl_hero_url, _ = find_hero_image(d)
        _isl_hero = hero_src_1280(_isl_hero_url) if _isl_hero_url else ''
        for fest in (d.get('festivals') or []):
            if not isinstance(fest, dict): continue
            months = sorted(parse_when_to_months(fest.get('when', '')))
            all_fests.append({
                'island': key,
                'island_hero': _isl_hero,
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

    island_count = len(island_keys)
    for lang in ['en', 'el']:
        is_el = (lang == 'el')
        month_names = MONTH_NAMES_EL if is_el else MONTH_NAMES_EN
        if is_el:
            title = f'Γιορτές & Πανηγύρια Νησιών {datetime.now().year} — αναλυτικό ημερολόγιο | Aegean Blueprint'
            intro = (f'Θρησκευτικές γιορτές, πανηγύρια και παραδοσιακές εκδηλώσεις σε όλα τα {island_count} ελληνικά νησιά. '
                     'Για τις κινητές γιορτές, οι ημερομηνίες είναι ρυθμισμένες για το 2027. '
                     'Το ημερολόγιο είναι ο καλύτερος τρόπος να σχεδιάσεις ταξίδι γύρω από κάτι συγκεκριμένο.')
            # Self-contained meta description (≤160 chars). Don't slice `intro` —
            # it's body copy and slicing truncates mid-sentence.
            meta_desc = (f'Θρησκευτικές γιορτές και πανηγύρια σε όλα τα {island_count} ελληνικά νησιά. '
                         'Κινητές ημερομηνίες ρυθμισμένες για το 2027. Σχεδίασε το ταξίδι σου γύρω από κάτι αυθεντικό.')
            h1 = 'Γιορτές & Πανηγύρια — Ημερολόγιο'
        else:
            title = f'Greek Island Festivals {datetime.now().year} — full calendar | Aegean Blueprint'
            intro = (f'Religious feasts, panigiria, and traditional celebrations across all {island_count} Greek islands. '
                     'Dates pinned to 2027 where movable. The calendar is the single best way to plan a trip '
                     'around something specific — most of these festivals are the deepest-rooted experiences '
                     'an island offers.')
            # Self-contained meta description (≤160 chars).
            meta_desc = (f'Religious feasts and panigiria across all {island_count} Greek islands. Movable dates pinned to 2027. '
                         'The calendar is the deepest way to plan a trip.')
            h1 = f'Greek Island Festivals {datetime.now().year} — full calendar'

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

                photo_src = f.get('photo') or f.get('image') or ''
                photo_html = ''
                if photo_src:
                    photo_html = '<img class="fest-photo" src="' + esc(photo_src) + '" alt="' + esc(fest_name) + '" loading="lazy">'

                months_attr = ','.join(str(m) for m in f['months'])
                card_html = (
                    '<article class="fest-card" data-island="' + esc(f['island']) + '" data-months="' + months_attr + '">'
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

        # --- Festivals UX: filters + "happening now & soon" ---
        L_month  = 'Μήνας' if is_el else 'Month'
        L_island = 'Νησί' if is_el else 'Island'
        L_all    = 'Όλα' if is_el else 'All'
        L_clear  = 'Καθαρισμός' if is_el else 'Clear'
        L_soon   = 'Τώρα & προσεχώς' if is_el else 'Happening now & soon'
        L_this   = 'Αυτόν τον μήνα' if is_el else 'This month'
        L_next   = 'Τον επόμενο μήνα' if is_el else 'Next month'
        L_none   = 'Καμία γιορτή δεν ταιριάζει με τα φίλτρα.' if is_el else 'No festivals match these filters.'

        _isl_names = {}
        for _f in all_fests:
            if is_el:
                _isl_names[_f['island']] = GREEK_NAMES.get(_f['island'], ISLAND_META.get(_f['island'], {}).get('name', _f['island']))
            else:
                _isl_names[_f['island']] = ISLAND_META.get(_f['island'], {}).get('name', _f['island'])
        _island_options = sorted(_isl_names.items(), key=lambda kv: kv[1])
        _present_months = sorted({m for f in all_fests for m in f['months']})
        _month_opts = ''.join('<option value="' + str(m) + '">' + month_names[m-1] + '</option>' for m in _present_months)
        _island_opts = ''.join('<option value="' + k + '">' + esc(nm) + '</option>' for k, nm in _island_options)

        filter_html = (
            '<div class="fest-controls">'
            + '<select id="fest-f-month" aria-label="' + esc(L_month) + '"><option value="">' + esc(L_month) + ': ' + esc(L_all) + '</option>' + _month_opts + '</select>'
            + '<select id="fest-f-island" aria-label="' + esc(L_island) + '"><option value="">' + esc(L_island) + ': ' + esc(L_all) + '</option>' + _island_opts + '</select>'
            + '<button type="button" class="fest-clear" id="fest-f-clear">' + esc(L_clear) + '</button>'
            + '</div>'
            + '<section class="fest-soon" id="fest-soon" hidden><h2>' + esc(L_soon) + '</h2><div class="fest-cards" id="fest-soon-cards"></div></section>'
            + '<p class="fest-noresults" id="fest-noresults">' + esc(L_none) + '</p>'
        )

        soon_script = (
            '<script>\n(function(){\n'
            '  var monthSel=document.getElementById("fest-f-month"),islandSel=document.getElementById("fest-f-island"),clearBtn=document.getElementById("fest-f-clear"),noRes=document.getElementById("fest-noresults");\n'
            '  var sections=[].slice.call(document.querySelectorAll(".fest-month"));\n'
            '  var cards=[].slice.call(document.querySelectorAll(".fest-month .fest-card"));\n'
            '  function apply(){var m=monthSel.value,isl=islandSel.value,any=false;\n'
            '    cards.forEach(function(c){var okM=!m||(","+c.getAttribute("data-months")+",").indexOf(","+m+",")>-1;var okI=!isl||c.getAttribute("data-island")===isl;var show=okM&&okI;c.classList.toggle("is-hidden",!show);if(show)any=true;});\n'
            '    sections.forEach(function(s){s.classList.toggle("is-hidden",s.querySelectorAll(".fest-card:not(.is-hidden)").length===0);});\n'
            '    noRes.style.display=any?"none":"block";}\n'
            '  monthSel.addEventListener("change",apply);islandSel.addEventListener("change",apply);\n'
            '  clearBtn.addEventListener("click",function(){monthSel.value="";islandSel.value="";apply();});\n'
            '  var now=new Date(),cm=now.getMonth()+1,nm=cm===12?1:cm+1,picked=[];\n'
            '  var soon=document.getElementById("fest-soon"),soonCards=document.getElementById("fest-soon-cards");\n'
            '  function pick(month,tagText,tagClass){cards.forEach(function(c){if(picked.indexOf(c)>-1)return;if((","+c.getAttribute("data-months")+",").indexOf(","+month+",")>-1){picked.push(c);var clone=c.cloneNode(true);clone.classList.remove("is-hidden");var tag=document.createElement("span");tag.className="fest-soon-tag "+tagClass;tag.textContent=tagText;var txt=clone.querySelector(".fest-text");if(txt)txt.insertBefore(tag,txt.firstChild);soonCards.appendChild(clone);}});}\n'
            '  pick(cm,' + json.dumps(L_this, ensure_ascii=False) + ',"this");pick(nm,' + json.dumps(L_next, ensure_ascii=False) + ',"next");\n'
            '  if(soonCards.children.length>0)soon.hidden=false;\n'
            '})();\n</script>\n'
        )
        # --- end Festivals UX block ---

        # Event structured data (schema.org) — one Event per festival with a parseable date.
        _events = []
        for _f in all_fests:
            _start, _end = festival_iso_dates(_f['when'])
            if not _start:
                continue
            if is_el:
                _iname = GREEK_NAMES.get(_f['island'], ISLAND_META.get(_f['island'], {}).get('name', _f['island']))
                _fname = _f['name_el'] or _f['name']
                _fdesc = strip_html(_f['desc_el'] or _f['desc'])
            else:
                _iname = ISLAND_META.get(_f['island'], {}).get('name', _f['island'])
                _fname = _f['name']
                _fdesc = strip_html(_f['desc'])
            _ev = {
                "@context": "https://schema.org",
                "@type": "Event",
                "name": _fname,
                "startDate": _start,
                "eventStatus": "https://schema.org/EventScheduled",
                "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                "location": {"@type": "Place", "name": f"{_iname}, Greece",
                             "address": {"@type": "PostalAddress", "addressLocality": _iname, "addressCountry": "GR"}},
                "description": truncate_at_word(_fdesc, 280),
                "url": SITE_URL + ('/el/island/' if is_el else '/island/') + _f['island'] + '/',
            }
            # endDate: explicit range end when parseable, otherwise the event is
            # single-day so it ends the day it starts (GSC 'missing endDate').
            _ev["endDate"] = _end or _start
            # image: festival's own photo, else the island's hero photo
            # (GSC 'missing image' — a real photo of the place the event happens).
            _img = _f.get('photo') or _f.get('island_hero')
            if _img:
                _ev["image"] = _img
            _events.append(_ev)
        schema_html = ('<script type="application/ld+json">' + json.dumps(_events, ensure_ascii=False) + '</script>\n') if _events else ''

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
            '  .fest-controls { display:flex; flex-wrap:wrap; gap:10px; margin:0 0 28px; align-items:center; }\n'
            '  .fest-controls select, .fest-controls input { font:inherit; font-size:14px; padding:8px 12px; border:1px solid var(--border,#e5e1d8); border-radius:10px; background:var(--white,#fff); color:inherit; }\n'
            '  .fest-controls input { flex:1; min-width:160px; }\n'
            '  .fest-clear { cursor:pointer; border:none; background:none; color:var(--aegean-dark,#076880); font-weight:600; font-size:13px; padding:8px; }\n'
            '  .fest-soon { margin:0 0 36px; }\n'
            '  .fest-soon > h2 { font-family:var(--serif,Georgia),serif; font-size:22px; margin:0 0 14px; }\n'
            '  .fest-soon-tag { display:block; width:fit-content; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.5px; color:#fff; background:var(--aegean,#0B8FAC); border-radius:999px; padding:2px 9px; margin:0 0 8px; }\n'
            '  .fest-soon-tag.next { background:var(--ink-3,#888); }\n'
            '  .fest-card { transition:transform .12s ease, box-shadow .12s ease; }\n'
            '  .fest-card:hover { transform:translateY(-2px); box-shadow:0 6px 18px rgba(0,0,0,.10); }\n'
            '  .fest-noresults { display:none; padding:24px; text-align:center; color:var(--ink-3,#888); font-size:15px; }\n'
            '  .fest-month.is-hidden, .fest-card.is-hidden { display:none !important; }\n'
            '  html.dark .fest-controls select, html.dark .fest-controls input { background:#2a2a2a; border-color:#444; color:#eee; }\n'
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
            + schema_html
            + '<script async data-cfasync="false" data-noptimize="1" data-no-defer="1" src="https://emrldtp.com/NTUxOTU3.js?t=551957"></script>\n'
            + '</head>\n<body>\n'
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
            '      <a href="/' + ('el/' if is_el else '') + '#compare">' + ('Σύγκριση' if is_el else 'Compare') + '</a>\n'
            '      <a href="/' + ('el/' if is_el else '') + '#match">' + ('Βρες το Νησί σου' if is_el else 'Match Me') + '</a>\n'
            '      <a href="/' + ('el/' if is_el else '') + 'trip-cost/">' + ('Μπάτζετ' if is_el else 'Budget') + '</a>\n'
            '      <a href="/' + ('el/' if is_el else '') + '#hopping">' + ('Πλοία & Νησοπορία' if is_el else 'Ferries & Hopping') + '</a>\n'
            '      <a href="/' + ('el/' if is_el else '') + 'festivals/" class="active">' + ('Γιορτές' if is_el else 'Festivals') + '</a>\n'
            '      <a href="/' + ('el/' if is_el else '') + '#data">' + ('Στοιχεία Νησιών' if is_el else 'Islands Data') + '</a>\n'
            '      <a href="/' + ('el/' if is_el else '') + '#mission">' + ('Στόχος' if is_el else 'Mission') + '</a>\n'
            '      <a href="/' + ('el/' if is_el else '') + '#shortlist">' + ('⭐ Η Λίστα μου' if is_el else '⭐ My Shortlist') + '</a>\n'
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
            + ('  <p class="fest-nav" style="margin-top:-20px">'
               + ('Ανά μήνα: ' if is_el else 'By month: ')
               + ' · '.join(f'<a href="/{"el/" if is_el else ""}festivals/{slug}/">{el_n if is_el else en_n}</a>'
                            for slug, en_n, el_n in [('may','May','Μάιος'),('june','June','Ιούνιος'),('july','July','Ιούλιος'),('august','August','Αύγουστος'),('september','September','Σεπτέμβριος')])
               + ' &nbsp;·&nbsp; <a href="/' + ('el/' if is_el else '') + 'festivals/ikaria-panigiria/"><strong>'
               + ('Τα πανηγύρια της Ικαρίας →' if is_el else 'The panigiria of Ikaria →') + '</strong></a></p>\n')
            + filter_html + '\n'
            '  ' + ''.join(month_blocks) + '\n'
            '</main>\n'
            '<div class="cta-affiliate"><a class="ferry-btn" href="https://www.ferryhopper.com/" target="_blank" rel="noopener sponsored">' + ('🚢 Κράτηση εισιτηρίων' if is_el else '🚢 Book ferry tickets') + '</a><a class="car-btn" href="https://www.discovercars.com/?a_aid=antaran2" target="_blank" rel="noopener sponsored">' + ('🚗 Ενοικίαση αυτοκινήτου' if is_el else '🚗 Rent a car') + '</a></div>\n'
            '<footer style="text-align:center;padding:24px 16px;font-size:13px;color:#888;border-top:1px solid #e5e5e5;margin-top:40px;">\n'
            '  <p style="margin:0;">© 2026 Aegean Blueprint · <a href="' + ('/el/privacy/' if is_el else '/privacy/') + '" style="color:#888;text-decoration:none;">' + ('Απόρρητο' if is_el else 'Privacy') + '</a></p>\n'
            '</footer>\n'
            + soon_script
            + '</body>\n</html>'
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


def generate_hero_photos_index(island_keys):
    """Map island key -> {url, credit} for the first available on-island photo.
    Lets the SPA show photo thumbnails on island cards (quiz results) without
    fetching each island's full JSON. Tiny file."""
    def _credit_for(d, url):
        for day in (d.get('itinerary') or {}).get('days') or []:
            for s in day.get('stops') or []:
                if s.get('photo') == url:
                    return s.get('photo_credit', '')
        for b in d.get('beaches') or []:
            if b.get('photo') == url:
                return b.get('photo_credit', '')
        return ''
    index = {}
    for key in sorted(island_keys):
        try:
            d = json.loads((ISLANDS_DIR / f'{key}.json').read_text())
        except Exception:
            continue
        url, _subject = find_hero_image(d)
        if not url:
            continue
        entry = {'url': url}
        credit = _credit_for(d, url)
        if credit:
            entry['credit'] = credit
        index[key] = entry
    out_path = ROOT / 'hero-photos.json'
    out_path.write_text(json.dumps(index, ensure_ascii=False, separators=(',', ':')))
    return out_path


# Mirror of script.js parse — used at build time to pre-compute month coverage per festival
_MONTH_NAMES = {
    'january':1, 'jan':1, 'february':2, 'feb':2, 'march':3, 'mar':3, 'april':4, 'apr':4,
    'may':5, 'june':6, 'jun':6, 'july':7, 'jul':7, 'august':8, 'aug':8,
    'september':9, 'sept':9, 'sep':9, 'october':10, 'oct':10, 'november':11, 'nov':11,
    'december':12, 'dec':12,
}
_MONTHS_EN = {'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,
              'july':7,'august':8,'september':9,'october':10,'november':11,'december':12}
def festival_iso_dates(when_str, year=2027):
    """Best-effort (startDate, endDate) ISO strings from a festival 'when' string.
    Returns (None, None) when no explicit day+month can be found (vague ranges)."""
    s = when_str or ''
    ym = re.search(r'(20\d\d)', s)
    yr = int(ym.group(1)) if ym else year
    low = s.lower()
    # range "D[-/–]D Month"
    rm = re.search(r'(\d{1,2})\s*[\u2013\-]\s*(\d{1,2})\s+([a-z]+)', low)
    if rm and rm.group(3) in _MONTHS_EN:
        mo = _MONTHS_EN[rm.group(3)]
        return f"{yr}-{mo:02d}-{int(rm.group(1)):02d}", f"{yr}-{mo:02d}-{int(rm.group(2)):02d}"
    # single "D Month"
    sm = re.search(r'(\d{1,2})\s+([a-z]+)', low)
    if sm and sm.group(2) in _MONTHS_EN:
        mo = _MONTHS_EN[sm.group(2)]
        return f"{yr}-{mo:02d}-{int(sm.group(1)):02d}", None
    # "Month D"
    sm2 = re.search(r'\b([a-z]+)\s+(\d{1,2})\b', low)
    if sm2 and sm2.group(1) in _MONTHS_EN:
        mo = _MONTHS_EN[sm2.group(1)]
        return f"{yr}-{mo:02d}-{int(sm2.group(2)):02d}", None
    return None, None


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


# Bump this whenever a TEMPLATE change materially alters every island page
# (redesigns, new sections, changed markup). Island <lastmod> in the sitemap
# becomes max(JSON git date, this date) — so Google learns the pages changed
# even when the underlying JSON didn't. Last bump: island-page immersive hero
# + when-to-visit ribbon + Ionian wind wording.
TEMPLATE_LASTMOD = '2026-07-18'

def file_lastmod(path):
    """Return ISO-8601 date for when the file was last meaningfully changed.

    Strategy: prefer `git log -1 --format=%cI` of the file's committer date —
    this reflects when content actually changed, not when the file was touched
    locally (mtime resets on git pull, cp, checkout, etc).

    Falls back to file mtime if git is unavailable or the path isn't tracked
    (e.g., when running this script outside the repo's working tree, or in
    sandboxes that only have the files without history).
    """
    # Try git first
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%cI', '--', str(path)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=2,
        )
        if result.returncode == 0 and result.stdout.strip():
            # git outputs ISO 8601 like '2026-05-31T17:22:14+00:00' — keep only date
            return result.stdout.strip().split('T', 1)[0]
    except Exception:
        pass
    # Fall back to file mtime
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

    # Static pages: language homepages + dedicated landing pages
    # (/#data, /#compare, etc. are SPA hash routes, NOT separate URLs)
    static_pages = [
        ('/', '/el/', 1.0, today),
        ('/festivals/', '/el/festivals/', 0.8, today),
        ('/ferries/', '/el/ferries/', 0.8, today),
        ('/trip-cost/', '/el/trip-cost/', 0.8, today),
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
        # max(): content edits bump per-island; TEMPLATE_LASTMOD covers
        # site-wide template changes that alter every page's HTML.
        lastmod = max(file_lastmod(json_path), TEMPLATE_LASTMOD)
        add_url_pair(f'/island/{key}/', f'/el/island/{key}/', 0.7, lastmod)

    lines.append('</urlset>')
    SITEMAP_PATH.write_text('\n'.join(lines) + '\n')

if __name__ == '__main__':
    main()
