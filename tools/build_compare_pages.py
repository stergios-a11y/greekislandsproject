#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ^ explicit declaration: this file contains Greek titles and descriptions, and
#   some interpreters refuse non-ASCII source without it (PEP 263).
"""Generate static, SEO-indexable comparison pages at /compare/<a>-vs-<b>/.

Each page is:
  - The same SPA shell as index.html (header, nav, footer, fonts, CSS)
  - The same #view-compare skeleton — radar chart, cards, etc. all render
    identically to /#compare when the SPA hydrates
  - A unique <title> + <meta description> + canonical URL per pair
  - The editorial verdict from vs_verdicts.json baked into the HTML so
    Google crawls it without executing JavaScript
  - The FAQ from vs_faqs.json (where present) baked into the HTML AND
    serialized as FAQPage JSON-LD in <head> for rich-snippet eligibility
  - An inline boot hint window.__INITIAL_COMPARE_PAIR so the SPA pre-fills
    the dropdowns on first paint, no flash of the default pair

The earlier teardown (commit 02e1f3b4) was driven by the OLD static pages
looking visually different from the SPA. This rebuild guarantees identical
appearance by reusing the same shell — only the URL changes.

Reads:  vs_verdicts.json, vs_faqs.json, island metadata in script.js
Writes: compare/<slug>/index.html, el/compare/<slug>/index.html
"""
import json
import re
from pathlib import Path

def _resolve_root():
    candidates = []
    try:
        candidates.append(Path(__file__).resolve().parent.parent)
    except NameError:
        pass
    candidates.append(Path.cwd())
    cwd = Path.cwd()
    for _ in range(4):
        candidates.append(cwd)
        cwd = cwd.parent
    for c in candidates:
        if (c / 'vs_verdicts.json').is_file() and (c / 'script.js').is_file():
            return c
    raise SystemExit(
        "Could not find project root. Run from inside the project, e.g. "
        "`cd ~/greekislandsproject && python3 tools/build_compare_pages.py`."
    )

ROOT = _resolve_root()
SITE_URL = 'https://aegeanblueprint.com'
ASSET_V = 70

from datetime import date as _date
YEAR = _date.today().year
TITLE_OVERRIDES = {('chania', 'rethymno'): ('Chania vs Rethymno {y}: Chania Wins on Beaches — Honest Pick', 'Χανιά ή Ρέθυμνο {y}: Τα Χανιά Κερδίζουν στις Παραλίες'), ('corfu', 'zakynthos'): ('Corfu vs Zakynthos {y}: Old Town or Better Beaches?', 'Κέρκυρα ή Ζάκυνθος {y}: Παλιά Πόλη ή Καλύτερες Παραλίες;'), ('mykonos', 'paros'): ('Mykonos vs Paros {y}: Same Nightlife, Half the Price', 'Μύκονος ή Πάρος {y}: Ίδια Νυχτερινή Ζωή, Μισή Τιμή'), ('kos', 'rhodes'): ('Kos vs Rhodes {y}: Rhodes for History, Kos for Easy', 'Κως ή Ρόδος {y}: Ρόδος για Ιστορία, Κως για Ευκολία'), ('corfu', 'rhodes'): ('Corfu vs Rhodes {y}: Two Old Towns, One Clear Winner', 'Κέρκυρα ή Ρόδος {y}: Δύο Παλιές Πόλεις, Ένας Νικητής'), ('kefalonia', 'zakynthos'): ('Kefalonia vs Zakynthos {y}: Quiet Coves or Party Coast?', 'Κεφαλονιά ή Ζάκυνθος {y}: Ήσυχοι Όρμοι ή Πάρτι;'), ('naxos', 'paros'): ('Naxos vs Paros {y}: Which Cyclade Actually Suits You?', 'Νάξος ή Πάρος {y}: Ποια Κυκλάδα σού Ταιριάζει Πραγματικά;'), ('ios', 'santorini'): ('Ios vs Santorini {y}: Caldera Views or Cheaper Nights?', 'Ίος ή Σαντορίνη {y}: Καλντέρα ή Φθηνότερες Νύχτες;'), ('milos', 'naxos'): ('Milos vs Naxos {y}: Strange Coastline or All-Rounder?', 'Μήλος ή Νάξος {y}: Παράξενη Ακτή ή Ολοκληρωμένο Νησί;')}
DESC_OVERRIDES = {('chania', 'rethymno'): ("Chania scores 4.8 to Rethymno's 3.8 — better beaches, better old town, more to do. But Rethymno is cheaper and quieter. Which one fits your trip, honestly.", 'Τα Χανιά βαθμολογούνται 4.8 έναντι 3.8 του Ρεθύμνου — καλύτερες παραλίες, καλύτερη παλιά πόλη. Το Ρέθυμνο όμως είναι φθηνότερο και πιο ήσυχο. Ειλικρινής σύγκριση.'), ('corfu', 'zakynthos'): ('Zakynthos has the better beaches (4.8 vs 3.9); Corfu has the far better old town (4.8 vs 2.5). Scored side by side on beaches, nightlife, access and price.', 'Η Ζάκυνθος έχει καλύτερες παραλίες (4.8 έναντι 3.9)· η Κέρκυρα πολύ καλύτερη παλιά πόλη (4.8 έναντι 2.5). Αναλυτική σύγκριση με βαθμολογίες.'), ('mykonos', 'paros'): ("Both score 5.0 for nightlife and Paros beats Mykonos on beaches — at a fraction of the cost. When Mykonos is still worth it, and when it isn't.", 'Και τα δύο 5.0 στη νυχτερινή ζωή, και η Πάρος κερδίζει στις παραλίες — με πολύ μικρότερο κόστος. Πότε αξίζει η Μύκονος και πότε όχι.'), ('kos', 'rhodes'): ('Rhodes wins overall (4.4 vs 3.7) on history and old town; Kos is flatter, cheaper and easier to get around by bike. Scored on beaches, nightlife and price.', 'Η Ρόδος κερδίζει συνολικά (4.4 έναντι 3.7) σε ιστορία και παλιά πόλη· η Κως είναι πιο επίπεδη, φθηνότερη και ευκολότερη με ποδήλατο. Με βαθμολογίες.'), ('corfu', 'rhodes'): ('Two UNESCO old towns compared: Rhodes edges it overall (4.4 vs 4.2) with the stronger medieval core, Corfu is greener with better food. Scored side by side.', 'Δύο παλιές πόλεις UNESCO: η Ρόδος υπερτερεί οριακά (4.4 έναντι 4.2) με ισχυρότερο μεσαιωνικό πυρήνα, η Κέρκυρα είναι πιο πράσινη με καλύτερο φαγητό.'), ('kefalonia', 'zakynthos'): ('Dead level overall at 4.1 each — Zakynthos for nightlife and Navagio, Kefalonia for quiet coves and mountains. The honest split, scored.', 'Ισοπαλία στο 4.1 — Ζάκυνθος για νυχτερινή ζωή και Ναυάγιο, Κεφαλονιά για ήσυχους όρμους και βουνά. Η ειλικρινής διαφορά, με βαθμολογίες.')}

# --- Saronic day-trip set + the three Evia regions -------------------------
# The default template would produce "Evia (Central) vs Evia (North)", which
# reads badly and wastes the title. All six get a verdict-led title instead.
TITLE_OVERRIDES.update({
    ('agistri', 'salamis'): (
        "Agistri vs Salamina {y}: Only One Is Worth Swimming In",
        'Αγκίστρι ή Σαλαμίνα {y}: Μόνο στο Ένα Αξίζει το Μπάνιο'),
    ('aegina', 'salamis'): (
        "Aegina vs Salamina {y}: Closest Isn't Best",
        'Αίγινα ή Σαλαμίνα {y}: Το Πιο Κοντινό Δεν Είναι Καλύτερο'),
    ('agistri', 'poros'): (
        'Agistri vs Poros {y}: Better Swimming or Better Town?',
        'Αγκίστρι ή Πόρος {y}: Καλύτερο Μπάνιο ή Καλύτερη Πόλη;'),
    ('evia-central', 'evia-north'): (
        'Central vs North Evia {y}: No Ferry or No Bills?',
        'Κεντρική ή Βόρεια Εύβοια {y}: Χωρίς Πλοίο ή Χωρίς Έξοδα;'),
    ('evia-north', 'evia-south'): (
        'North vs South Evia {y}: South Wins on Beaches',
        'Βόρεια ή Νότια Εύβοια {y}: Ο Νότος Κερδίζει στις Παραλίες'),
    ('evia-central', 'evia-south'): (
        'Central vs South Evia {y}: Ancient Sites or Best Beaches?',
        'Κεντρική ή Νότια Εύβοια {y}: Αρχαία ή Καλύτερες Παραλίες;'),
})
DESC_OVERRIDES.update({
    ('agistri', 'salamis'): (
        "Agistri scores 3.4 to Salamina's 2.8, and the gap is water: 3.5 for beaches "
        'against 2.0. Salamina has the 480 BC battle and a 15-minute ferry. Honest pick.',
        'Το Αγκίστρι βαθμολογείται 3.4 έναντι 2.8 της Σαλαμίνας, και η διαφορά είναι το νερό: '
        '3.5 στις παραλίες έναντι 2.0. Η Σαλαμίνα έχει τη ναυμαχία και 15 λεπτά πλοίο.'),
    ('aegina', 'salamis'): (
        'Aegina wins 3.3 to 2.8 on the Temple of Aphaia, Perdika fish tavernas and easier '
        'ferries. Salamina is closer and cheaper. Neither is a beach island — 2.5 vs 2.0.',
        'Η Αίγινα κερδίζει 3.3 έναντι 2.8 με τον Ναό της Αφαίας, τις ψαροταβέρνες της Πέρδικας '
        'και ευκολότερα πλοία. Η Σαλαμίνα είναι πιο κοντά και φθηνότερη. Καμία για παραλίες.'),
    ('agistri', 'poros'): (
        "Poros edges it 3.5 to 3.4 on town and culture (4.2 vs 2.5); Agistri wins beaches "
        '(3.5 vs 3.0), price and needs no car at all. Swim on Agistri, stay on Poros.',
        'Ο Πόρος υπερτερεί 3.5 έναντι 3.4 σε πόλη και πολιτισμό (4.2 έναντι 2.5)· το Αγκίστρι '
        'κερδίζει σε παραλίες (3.5 έναντι 3.0), τιμή, και δεν θέλει καθόλου αυτοκίνητο.'),
    ('evia-central', 'evia-north'): (
        'Central Evia scores 3.9 to 3.6: no ferry at all via the Chalkida bridge, plus ancient '
        'Eretria and Mt Dirfys. North Evia is cheapest on the island (4.8) with thermal springs.',
        'Η Κεντρική Εύβοια βαθμολογείται 3.9 έναντι 3.6: χωρίς πλοίο μέσω της Χαλκίδας, με την '
        'αρχαία Ερέτρια και τη Δίρφη. Η Βόρεια είναι η φθηνότερη (4.8) με ιαματικές πηγές.'),
    ('evia-north', 'evia-south'): (
        'South Evia wins 3.9 to 3.6 on the best beaches on the island (4.6 vs 3.8) and the '
        'Dimosari gorge. North Evia is cheaper (4.8) with the Edipsos thermal springs.',
        'Η Νότια Εύβοια κερδίζει 3.9 έναντι 3.6 με τις καλύτερες παραλίες του νησιού (4.6 έναντι '
        '3.8) και το φαράγγι του Δημοσάρη. Η Βόρεια είναι φθηνότερη (4.8) με τα Λουτρά Αιδηψού.'),
    ('evia-central', 'evia-south'): (
        'A real tie at 3.9 each. Central wins culture (4.5 vs 3.5) and needs no ferry; South '
        'wins beaches decisively (4.6 vs 3.5) plus Mt Ochi and Karystos. Scored side by side.',
        'Πραγματική ισοπαλία στο 3.9. Η Κεντρική κερδίζει στον πολιτισμό (4.5 έναντι 3.5) και δεν '
        'θέλει πλοίο· η Νότια κερδίζει καθαρά στις παραλίες (4.6 έναντι 3.5), με Όχη και Κάρυστο.'),
})

# --- Dodecanese + NE Aegean decisions --------------------------------------
TITLE_OVERRIDES.update({
    ('karpathos', 'kos'): (
        'Karpathos vs Kos {y}: Wild Beaches or Easy Flights?',
        'Κάρπαθος ή Κως {y}: Άγριες Παραλίες ή Εύκολες Πτήσεις;'),
    ('chios', 'samos'): (
        'Chios vs Samos {y}: Mastic Villages or Ancient Engineering?',
        'Χίος ή Σάμος {y}: Μαστιχοχώρια ή Αρχαία Μηχανική;'),
})
DESC_OVERRIDES.update({
    ('karpathos', 'kos'): (
        "Karpathos wins on beaches (4.4 vs 4.0) and emptiness; Kos wins on access 4.6 to 2.0 "
        '— direct flights, flat cycling, the Asklepion. The honest Dodecanese decision.',
        'Η Κάρπαθος κερδίζει στις παραλίες (4.4 έναντι 4.0) και στην ερημιά· η Κως στην πρόσβαση '
        '4.6 έναντι 2.0 — απευθείας πτήσεις, ποδήλατο, Ασκληπιείο. Ειλικρινής σύγκριση.'),
    ('chios', 'samos'): (
        'Chios edges it 3.6 to 3.3 on the mastic villages and Nea Moni (culture 4.7); Samos is '
        'greener with better beaches, the Eupalinos Tunnel and Ephesus an hour away.',
        'Η Χίος υπερτερεί 3.6 έναντι 3.3 με τα Μαστιχοχώρια και τη Νέα Μονή (πολιτισμός 4.7)· η '
        'Σάμος είναι πιο πράσινη με καλύτερες παραλίες, το Ευπαλίνειο και την Έφεσο μία ώρα μακριά.'),
})

# --- NE Aegean + the four missing Sporades pairs ---------------------------
TITLE_OVERRIDES.update({
    ('lemnos', 'lesvos'): (
        'Lemnos vs Lesvos {y}: Better Beaches or More Island?',
        'Λήμνος ή Λέσβος {y}: Καλύτερες Παραλίες ή Πιο Πολύ Νησί;'),
    ('alonnisos', 'skiathos'): (
        'Alonnisos vs Skiathos {y}: Monk Seals or Party Beaches?',
        'Αλόννησος ή Σκιάθος {y}: Φώκιες ή Παραλίες με Πάρτι;'),
    ('skiathos', 'skyros'): (
        'Skiathos vs Skyros {y}: Not Actually the Same Trip',
        'Σκιάθος ή Σκύρος {y}: Δεν Είναι το Ίδιο Ταξίδι'),
    ('skopelos', 'skyros'): (
        'Skopelos vs Skyros {y}: Pine Forest or Cycladic Chora?',
        'Σκόπελος ή Σκύρος {y}: Πευκοδάσος ή Κυκλαδίτικη Χώρα;'),
    ('alonnisos', 'skyros'): (
        'Alonnisos vs Skyros {y}: Marine Park or Living Folklore?',
        'Αλόννησος ή Σκύρος {y}: Θαλάσσιο Πάρκο ή Ζωντανή Παράδοση;'),
})
DESC_OVERRIDES.update({
    ('lemnos', 'lesvos'): (
        "Lesvos scores 4.0 to Lemnos's 3.7 on culture (4.7 vs 3.5) — but Lemnos has better "
        'beaches (4.3 vs 4.0) and fits three days where Lesvos needs six. Scored side by side.',
        'Η Λέσβος βαθμολογείται 4.0 έναντι 3.7 στον πολιτισμό (4.7 έναντι 3.5) — αλλά η Λήμνος έχει '
        'καλύτερες παραλίες (4.3 έναντι 4.0) και χωράει σε τρεις μέρες όπου η Λέσβος θέλει έξι.'),
    ('alonnisos', 'skiathos'): (
        'Nearly level at 3.9 vs 3.8 with almost the same beach score — so it comes down to crowds '
        'and cost. Skiathos flies direct; Alonnisos has the marine park and is cheaper.',
        'Σχεδόν ισοπαλία 3.9 έναντι 3.8 με σχεδόν ίδια βαθμολογία παραλιών — κρίνεται στον κόσμο και '
        'το κόστος. Η Σκιάθος έχει απευθείας πτήσεις· η Αλόννησος το θαλάσσιο πάρκο και φθηνότερα.'),
    ('skiathos', 'skyros'): (
        'Both are Sporades but not on the same ferry network — Skiathos from Volos, Skyros from '
        'Kymi. Skiathos wins beaches 4.6 to 4.0; Skyros wins culture 3.8 to 2.0.',
        'Και οι δύο Σποράδες αλλά όχι στο ίδιο δίκτυο πλοίων — Σκιάθος από Βόλο, Σκύρος από Κύμη. '
        'Η Σκιάθος κερδίζει στις παραλίες 4.6 έναντι 4.0· η Σκύρος στον πολιτισμό 3.8 έναντι 2.0.'),
    ('skopelos', 'skyros'): (
        'Skopelos edges it 3.6 to 3.4 on pine forest and beaches (4.2 vs 4.0); Skyros is cheaper '
        'with stronger culture (3.8 vs 3.2) and a chora that looks Cycladic. Not combinable.',
        'Η Σκόπελος υπερτερεί 3.6 έναντι 3.4 με πευκοδάσος και παραλίες (4.2 έναντι 4.0)· η Σκύρος '
        'είναι φθηνότερη με ισχυρότερο πολιτισμό (3.8 έναντι 3.2) και κυκλαδίτικη χώρα.'),
    ('alonnisos', 'skyros'): (
        'The two quietest Sporades. Alonnisos wins 3.8 to 3.4 on beaches and the marine park; '
        'Skyros on culture (3.8 vs 3.0), price and the goat-mask carnival.',
        'Οι δύο ησυχότερες Σποράδες. Η Αλόννησος κερδίζει 3.8 έναντι 3.4 σε παραλίες και θαλάσσιο '
        'πάρκο· η Σκύρος στον πολιτισμό (3.8 έναντι 3.0), στην τιμή και στο καρναβάλι.'),
})

VERDICTS = json.loads((ROOT / 'vs_verdicts.json').read_text(encoding='utf-8'))
FAQS_PATH = ROOT / 'vs_faqs.json'
FAQS = json.loads(FAQS_PATH.read_text(encoding='utf-8')) if FAQS_PATH.exists() else {}

def load_island_meta():
    js = (ROOT / 'script.js').read_text(encoding='utf-8')
    meta = {}
    for m in re.finditer(
        r'^\s*"([a-z-]+)"\s*:\s*\{\s*name\s*:\s*"([^"]+)"[^}]*island_group\s*:\s*"([^"]+)"',
        js, re.MULTILINE
    ):
        meta[m.group(1)] = {'name': m.group(2), 'group': m.group(3)}
    return meta

def load_island_names_el():
    js = (ROOT / 'i18n.js').read_text(encoding='utf-8')
    m = re.search(r'const\s+ISLAND_NAMES_EL\s*=\s*\{(.*?)\};', js, re.DOTALL)
    if not m:
        return {}
    out = {}
    for ml in re.finditer(r"'([a-z-]+)'\s*:\s*'([^']+)'", m.group(1)):
        out[ml.group(1)] = ml.group(2)
    return out

META = load_island_meta()
NAMES_EL = load_island_names_el()

def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;')
                  .replace('>', '&gt;').replace('"', '&quot;'))

def parse_pair_key(pk):
    return tuple(pk.split('__', 1))

def slug_for_pair(a, b):
    a, b = sorted([a, b])
    return f'{a}-vs-{b}'

def render_faq_jsonld(faqs):
    if not faqs:
        return ''
    schema = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {'@type': 'Question', 'name': item['q'],
             'acceptedAnswer': {'@type': 'Answer', 'text': item['a']}}
            for item in faqs
        ]
    }
    return ('<script type="application/ld+json">'
            + json.dumps(schema, ensure_ascii=False, separators=(',', ':'))
            + '</script>')

# ---------------------------------------------------------------------------
# Related-comparisons widget + hub page helpers (added R2)
# ---------------------------------------------------------------------------

# Manually curated "featured" pairs for the hub page hero — the highest-demand
# comparison queries. Order matters (most-searched first).
FEATURED_PAIR_KEYS = [
    'rhodes__santorini',
    'naxos__santorini',
    'paros__santorini',
    'mykonos__santorini',
    'chania__santorini',
    'mykonos__rhodes',
    'ios__mykonos',
    'corfu__rhodes',
]

def _is_longform(pair_key):
    """A pair is 'long-form' if its EN verdict exceeds 3000 chars."""
    return len((VERDICTS.get(pair_key, {}).get('en') or '')) > 3000

def build_island_to_pairs_index():
    """Returns {island_slug: [pair_key, ...]} for all known pairs."""
    idx = {}
    for pk in VERDICTS.keys():
        try:
            a, b = parse_pair_key(pk)
        except Exception:
            continue
        idx.setdefault(a, []).append(pk)
        idx.setdefault(b, []).append(pk)
    return idx

PAIRS_BY_ISLAND = build_island_to_pairs_index()

def select_related_pairs(pair_key, k=4):
    """For a given pair, return up to k other pair_keys to recommend.

    Strategy: 2 pairs containing island A + 2 containing island B,
    preferring long-form pairs. Dedupe and exclude the current pair.
    """
    try:
        a, b = parse_pair_key(pair_key)
    except Exception:
        return []

    def candidates_for(island):
        return sorted(
            (p for p in PAIRS_BY_ISLAND.get(island, []) if p != pair_key),
            key=lambda p: (not _is_longform(p), p),  # long-form first, then alpha
        )

    a_cands = candidates_for(a)
    b_cands = candidates_for(b)

    out = []
    for i in range(max(len(a_cands), len(b_cands))):
        if i < len(a_cands) and a_cands[i] not in out and len(out) < k:
            out.append(a_cands[i])
        if i < len(b_cands) and b_cands[i] not in out and len(out) < k:
            out.append(b_cands[i])
        if len(out) >= k:
            break
    return out

def render_related_widget(pair_key, lang):
    """Renders a 'Related comparisons' card grid at the bottom of a compare page."""
    related = select_related_pairs(pair_key, k=4)
    if not related:
        return ''
    heading = 'Related comparisons' if lang == 'en' else 'Σχετικές συγκρίσεις'

    cards = []
    for pk in related:
        a, b = parse_pair_key(pk)
        slug = slug_for_pair(a, b)
        if lang == 'el':
            name_a = NAMES_EL.get(a, META[a]['name'])
            name_b = NAMES_EL.get(b, META[b]['name'])
            href = f'/el/compare/{slug}/'
            sep = 'ή'
        else:
            name_a = META[a]['name']
            name_b = META[b]['name']
            href = f'/compare/{slug}/'
            sep = 'vs'
        cards.append(
            f'<a class="compare-related-card" href="{esc(href)}">'
            f'<span class="compare-related-pair">{esc(name_a)} <em>{sep}</em> {esc(name_b)}</span>'
            f'<span class="compare-related-arrow" aria-hidden="true">→</span>'
            f'</a>'
        )
    return (
        f'<div class="compare-related">'
        f'<h3 class="compare-related-heading">{heading}</h3>'
        f'<div class="compare-related-grid">{"".join(cards)}</div>'
        f'</div>'
    )

def render_faq_html(faqs, lang):
    if not faqs:
        return ''
    items = []
    for item in faqs:
        items.append(
            f'<details><summary>{esc(item["q"])}</summary>'
            f'<p>{esc(item["a"])}</p></details>'
        )
    heading = 'Common questions' if lang == 'en' else 'Συχνές ερωτήσεις'
    return (f'<div class="compare-faq">'
            f'<h3 class="compare-faq-heading">{heading}</h3>'
            f'{"".join(items)}</div>')

def render_page(pair_key, lang):
    a, b = parse_pair_key(pair_key)
    if a not in META or b not in META:
        raise ValueError(f"Unknown island in pair {pair_key}: {a} / {b}")

    slug = slug_for_pair(a, b)

    if lang == 'el':
        name_a = NAMES_EL.get(a, META[a]['name'])
        name_b = NAMES_EL.get(b, META[b]['name'])
    else:
        name_a = META[a]['name']
        name_b = META[b]['name']

    verdict_entry = VERDICTS.get(pair_key, {})
    verdict_html = verdict_entry.get('el' if lang == 'el' else 'en', '') or ''
    faq_entry = FAQS.get(pair_key, {})
    faqs = faq_entry.get('el' if lang == 'el' else 'en', []) or []

    if lang == 'en':
        _ov = TITLE_OVERRIDES.get((a, b)) or TITLE_OVERRIDES.get((b, a))
        if _ov:
            page_title = _ov[0].format(y=YEAR) + ' | Aegean Blueprint'
        else:
            page_title = f'{name_a} vs {name_b}: Which Greek Island Should You Visit? | Aegean Blueprint'
        _od = DESC_OVERRIDES.get((a, b)) or DESC_OVERRIDES.get((b, a))
        if _od:
            page_desc = _od[0]
        else:
            page_desc = (f'{name_a} vs {name_b} — side-by-side comparison of beaches, '
                         f'culture, nightlife, access, and price. Practical recommendations '
                         f'for choosing the right island for your trip.')
        h1_text = f'{name_a} vs {name_b}'
        subtitle = 'Side-by-side comparison — beaches, culture, atmosphere, and the practical question of which one suits your trip.'
        verdict_heading = 'Our verdict'
        og_locale = 'en_US'
    else:
        _ov = TITLE_OVERRIDES.get((a, b)) or TITLE_OVERRIDES.get((b, a))
        if _ov:
            page_title = _ov[1].format(y=YEAR) + ' | Aegean Blueprint'
        else:
            page_title = f'{name_a} ή {name_b}: Ποιο ελληνικό νησί να διαλέξεις; | Aegean Blueprint'
        _od = DESC_OVERRIDES.get((a, b)) or DESC_OVERRIDES.get((b, a))
        if _od:
            page_desc = _od[1]
        else:
            page_desc = (f'{name_a} ή {name_b} — αναλυτική σύγκριση παραλιών, πολιτισμού, '
                         f'νυχτερινής ζωής, πρόσβασης και τιμών. Πρακτικές συμβουλές για '
                         f'να επιλέξεις το σωστό νησί για το ταξίδι σου.')
        h1_text = f'{name_a} ή {name_b}'
        subtitle = 'Λεπτομερής σύγκριση — παραλίες, πολιτισμός, ατμόσφαιρα, και η πρακτική επιλογή του νησιού που ταιριάζει στο ταξίδι σου.'
        verdict_heading = 'Η ετυμηγορία μας'
        og_locale = 'el_GR'

    en_url = f'{SITE_URL}/compare/{slug}/'
    el_url = f'{SITE_URL}/el/compare/{slug}/'
    canonical = el_url if lang == 'el' else en_url

    faq_jsonld = render_faq_jsonld(faqs)

    if verdict_html or faqs:
        prerendered_verdict = (
            f'<h3 class="compare-verdict-heading">{esc(verdict_heading)}</h3>'
            f'{verdict_html}'
            f'{render_faq_html(faqs, lang)}'
            f'{render_related_widget(pair_key, lang)}'
        )
        verdict_display = ''
    else:
        prerendered_verdict = ''
        verdict_display = 'display:none;'

    init_pair = json.dumps([a, b])

    if lang == 'el':
        nav_items = [
            ('/el/#compare', 'Σύγκριση', 'nav-compare'),
            ('/el/#match', 'Ταίριαξέ με', 'nav-match'),
            ('/el/trip-cost/', 'Μπάτζετ', 'nav-tripcost'),
            ('/el/#hopping', 'Πλοία & Νησοπορία', 'nav-hopping'),
            ('/el/festivals/', 'Γιορτές', 'nav-festivals'),
            ('/el/#data', 'Στοιχεία Νησιών', 'nav-data'),
            ('/el/#mission', 'Στόχος', 'nav-mission'),
            ('/el/#shortlist', '⭐ Λίστα μου', 'nav-shortlist'),
        ]
        home_url = '/el/'
        privacy_link = '<a href="/el/privacy/" data-i18n="footer.privacy">Απόρρητο</a> · <a href="/el/#mission">Στόχος</a>'
    else:
        nav_items = [
            ('/#compare', 'Compare', 'nav-compare'),
            ('/#match', 'Match Me', 'nav-match'),
            ('/trip-cost/', 'Budget', 'nav-tripcost'),
            ('/#hopping', 'Ferries & Hopping', 'nav-hopping'),
            ('/festivals/', 'Festivals', 'nav-festivals'),
            ('/#data', 'Islands Data', 'nav-data'),
            ('/#mission', 'Mission', 'nav-mission'),
            ('/#shortlist', '⭐ My Shortlist', 'nav-shortlist'),
        ]
        home_url = '/'
        privacy_link = '<a href="/privacy/" data-i18n="footer.privacy">Privacy</a> · <a href="/#mission">Mission</a>'

    nav_html = '\n        '.join(
        f'<a href="{esc(href)}" id="{nav_id}">{esc(label)}</a>'
        for href, label, nav_id in nav_items
    )

    page_css = '''
  #view-compare > h2[data-i18n="compare.title"],
  #view-compare > p.compare-intro {
    display: none;
  }
  .vs-page-h1 {
    font-family: var(--display, Georgia, serif);
    font-size: 32px;
    margin: 0 0 6px;
    color: var(--ink-1, #222);
  }
  .vs-page-sub {
    font-size: 16px;
    color: var(--ink-2, #555);
    margin: 0 0 24px;
    line-height: 1.5;
  }
  @media (max-width: 600px) {
    .vs-page-h1 { font-size: 26px; }
    .vs-page-sub { font-size: 15px; }
  }
  /* Related comparisons widget */
  .compare-related {
    margin-top: 32px;
    padding-top: 24px;
    border-top: 1px solid var(--marble-3, #e0e0e0);
  }
  .compare-related-heading {
    font-family: var(--display, Georgia, serif);
    font-size: var(--text-h3, 20px);
    margin: 0 0 16px;
    color: var(--ink-1, #222);
  }
  .compare-related-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
  .compare-related-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 16px;
    background: var(--marble, #fafafa);
    border: 1px solid var(--marble-3, #e0e0e0);
    border-radius: 8px;
    text-decoration: none;
    color: var(--ink-1, #222);
    transition: background 0.15s, border-color 0.15s;
  }
  .compare-related-card:hover {
    background: var(--marble-2, #f0f0f0);
    border-color: var(--ink-3, #999);
  }
  .compare-related-pair {
    font-size: var(--text-body, 15px);
    line-height: 1.3;
  }
  .compare-related-pair em {
    font-style: normal;
    color: var(--ink-2, #555);
    font-size: var(--text-small, 13px);
    margin: 0 4px;
  }
  .compare-related-arrow {
    color: var(--ink-2, #555);
    margin-left: 12px;
    flex-shrink: 0;
  }
  @media (max-width: 600px) {
    .compare-related-grid { grid-template-columns: 1fr; }
  }
'''

    og_image = f'{SITE_URL}/og-image.png'

    html = f'''<!DOCTYPE html>
<html lang="{'el' if lang == 'el' else 'en'}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(page_title)}</title>
<meta name="description" content="{esc(page_desc)}">
<meta name="theme-color" content="#0B8FAC">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="el" href="{el_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(page_title)}">
<meta property="og:description" content="{esc(page_desc)}">
<meta property="og:image" content="{og_image}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{og_locale}">
<meta property="og:site_name" content="Aegean Blueprint">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(page_title)}">
<meta name="twitter:description" content="{esc(page_desc)}">
<meta name="twitter:image" content="{og_image}">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-FMFWLRM2J9"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-FMFWLRM2J9');</script>
<script>if(localStorage.getItem("darkMode")==="true"){{document.documentElement.classList.add("dark");}}</script>
<link rel="stylesheet" href="/style.css?v={ASSET_V}">
<style>{page_css}</style>
{faq_jsonld}
<script async data-cfasync="false" data-noptimize="1" data-no-defer="1" src="https://emrldtp.com/NTUxOTU3.js?t=551957"></script>
</head>
<body>

<div id="loading-overlay" style="display:none;">
  <div class="loading-inner">
    <img src="/logo.svg" alt="Aegean Blueprint logo" id="loading-logo">
    <div class="loading-spinner"></div>
    <p>Loading…</p>
  </div>
</div>

<header>
  <div class="header-content">
    <a href="{home_url}" class="logo-wrapper">
      <img src="/logo-hero.svg" id="site-logo" alt="Aegean Blueprint logo">
      <span id="brand-text"><span class="brand-word">Aegean</span> <span class="brand-word">Blueprint</span></span>
    </a>
    <div class="menu-toggle" id="menu-toggle-btn"><span></span><span></span><span></span></div>
    <nav class="top-nav" id="main-nav">
        {nav_html}
    </nav>
    <div class="lang-dropdown" id="lang-dropdown">
      <button class="lang-toggle" id="lang-toggle-btn" aria-label="Switch language" aria-haspopup="true" aria-expanded="false">
        <span class="lang-globe">🌐</span>
        <span class="lang-current" id="lang-current">{'EL' if lang == 'el' else 'EN'}</span>
        <span class="lang-caret">▾</span>
      </button>
      <div class="lang-menu" id="lang-menu" role="menu">
        <a href="#" class="lang-option" data-lang="en" role="menuitem"><span class="lang-option-flag">🇬🇧</span> English</a>
        <a href="#" class="lang-option" data-lang="el" role="menuitem"><span class="lang-option-flag">🇬🇷</span> Ελληνικά</a>
      </div>
    </div>
    <button class="dark-mode-toggle" id="dark-mode-btn" aria-label="Toggle dark mode">☾</button>
  </div>
</header>

<main id="view-compare" class="view-section content-page">
  <h1 class="vs-page-h1">{esc(h1_text)}</h1>
  <p class="vs-page-sub">{esc(subtitle)}</p>
  <h2 data-i18n="compare.title">Compare Islands</h2>
  <p class="compare-intro" data-i18n="compare.intro">Select two islands to compare side-by-side.</p>
  <div class="compare-selectors">
    <select id="compare-select-a"><option value="" data-i18n="compare.optionA">— Island A —</option></select>
    <span class="vs-label" data-i18n="compare.vs">vs</span>
    <select id="compare-select-b"><option value="" data-i18n="compare.optionB">— Island B —</option></select>
  </div>
  <div id="compare-container">
    <div id="compare-placeholder" class="compare-placeholder" style="display:none;" data-i18n="compare.placeholder">Select two islands above to start comparing.</div>
    <div id="compare-content">
      <div class="compare-radar-wrap">
        <canvas id="compare-radar-chart" role="img" aria-label="Radar chart comparing two islands"></canvas>
      </div>
      <div class="compare-cards" id="compare-cards"></div>
      <div class="compare-section-label" data-i18n="compare.extra_title">Character &amp; practicalities</div>
      <div id="compare-extra" class="compare-extra"></div>
      <div class="compare-section-label" data-i18n="compare.wtv_title">When to visit — overlap</div>
      <div id="compare-wtv" class="compare-wtv"></div>
      <div id="compare-verdict" class="compare-verdict" style="{verdict_display}">{prerendered_verdict}</div>
    </div>
  </div>
</main>

<div class="cta-affiliate"><a class="ferry-btn" href="https://www.ferryhopper.com/" target="_blank" rel="noopener sponsored" data-i18n="detail.bookferry">🚢 Book ferry tickets</a><a class="car-btn" href="https://www.discovercars.com/?a_aid=antaran2" target="_blank" rel="noopener sponsored" data-i18n="detail.rentcar">🚗 Rent a car</a></div>
<footer id="site-footer">
  <div class="footer-line">
    <span class="footer-copy" data-i18n="footer.copyright">© 2026 Aegean Blueprint</span> · {privacy_link}<span class="footer-updated" id="footer-updated"></span>
  </div>
</footer>

<script>
window.__INITIAL_COMPARE_PAIR = {init_pair};
</script>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script src="/i18n.js?v=41"></script>
<script src="/script.js?v={ASSET_V}"></script>
</body>
</html>
'''
    return html


def update_sitemap(slugs):
    """Add per-pair URLs to sitemap.xml. Idempotent — replaces the block on re-runs."""
    sitemap_path = ROOT / 'sitemap.xml'
    if not sitemap_path.exists():
        return 0
    xml = sitemap_path.read_text(encoding='utf-8')

    START = '<!-- BEGIN AUTO-GENERATED COMPARE PAGES -->'
    END = '<!-- END AUTO-GENERATED COMPARE PAGES -->'
    today = '2026-06-06'

    entries = []
    # Hub pages first (higher priority than individual comparisons)
    for path in ('/compare/', '/el/compare/'):
        entries.append(
            f'<url><loc>{SITE_URL}{path}</loc>'
            f'<lastmod>{today}</lastmod>'
            f'<changefreq>weekly</changefreq>'
            f'<priority>0.7</priority></url>'
        )
    for slug in sorted(slugs):
        for path in (f'/compare/{slug}/', f'/el/compare/{slug}/'):
            entries.append(
                f'<url><loc>{SITE_URL}{path}</loc>'
                f'<lastmod>{today}</lastmod>'
                f'<changefreq>monthly</changefreq>'
                f'<priority>0.6</priority></url>'
            )
    block = START + '\n  ' + '\n  '.join(entries) + '\n  ' + END

    if START in xml and END in xml:
        new_xml = re.sub(
            re.escape(START) + r'.*?' + re.escape(END),
            block, xml, count=1, flags=re.DOTALL
        )
    else:
        new_xml = xml.replace('</urlset>', '  ' + block + '\n</urlset>')

    sitemap_path.write_text(new_xml, encoding='utf-8')
    return len(entries)


def render_hub_page(lang, valid_pairs):
    """Render the /compare/ landing page listing all comparison pairs.

    Groups: featured (hand-picked top 8) → by-region (same-group pairs) →
    cross-region. Long-form pairs surfaced first within each region.
    """
    valid_set = set(valid_pairs)

    # Featured: hand-picked, but only include those that actually exist
    featured = [pk for pk in FEATURED_PAIR_KEYS if pk in valid_set]

    # Group same-region pairs by their (shared) island_group, and collect
    # cross-region pairs separately
    by_region = {}  # group name -> list of pair_keys
    cross_region = []  # list of pair_keys
    for pk in valid_pairs:
        a, b = parse_pair_key(pk)
        ga = META[a]['group']
        gb = META[b]['group']
        if ga == gb:
            by_region.setdefault(ga, []).append(pk)
        else:
            cross_region.append(pk)

    # Sort within each section: long-form first, then alpha
    def sort_pairs(pks):
        return sorted(pks, key=lambda p: (not _is_longform(p), p))

    for g in by_region:
        by_region[g] = sort_pairs(by_region[g])
    cross_region = sort_pairs(cross_region)

    # Region display order (most comparisons / highest interest first)
    region_order = ['Cyclades', 'Crete', 'Ionian', 'Dodecanese',
                    'Saronic', 'NE Aegean', 'Sporades', 'Evia', 'Other']

    # Labels per language
    if lang == 'el':
        page_title = 'Συγκρίσεις ελληνικών νησιών | Aegean Blueprint'
        page_desc = ('Όλες οι αναλυτικές συγκρίσεις ελληνικών νησιών — '
                     'παραλίες, κουλτούρα, νυχτερινή ζωή, πρόσβαση, τιμές. '
                     'Επίλεξε το σωστό νησί για το ταξίδι σου.')
        h1_text = 'Συγκρίσεις ελληνικών νησιών'
        subtitle = ('Όλες οι αναλυτικές συγκρίσεις μας — οργανωμένες ανά περιοχή. '
                    'Κάθε σύγκριση εξετάζει παραλίες, ιστορία, φαγητό, κόστος, '
                    'και την πρακτική επιλογή του νησιού που ταιριάζει στο ταξίδι σου.')
        featured_label = 'Δημοφιλείς συγκρίσεις'
        cross_region_label = 'Συγκρίσεις μεταξύ περιοχών'
        region_labels = {
            'Cyclades': 'Κυκλάδες', 'Crete': 'Κρήτη', 'Ionian': 'Ιόνιο',
            'Dodecanese': 'Δωδεκάνησα', 'Saronic': 'Σαρωνικός',
            'NE Aegean': 'ΒΑ Αιγαίο', 'Sporades': 'Σποράδες',
            'Evia': 'Εύβοια', 'Other': 'Άλλα',
        }
        sep = 'ή'
        href_prefix = '/el/compare/'
        canonical = f'{SITE_URL}/el/compare/'
        en_url = f'{SITE_URL}/compare/'
        el_url = canonical
        og_locale = 'el_GR'
    else:
        page_title = 'Greek Island Comparisons | Aegean Blueprint'
        page_desc = ('Side-by-side comparisons of Greek islands — beaches, '
                     'culture, nightlife, access, and price. Pick the right '
                     'island for your trip.')
        h1_text = 'Greek Island Comparisons'
        subtitle = ('All our side-by-side island comparisons, organized by region. '
                    'Each one covers beaches, history, food, cost, and the '
                    'practical question of which island suits your trip.')
        featured_label = 'Featured comparisons'
        cross_region_label = 'Cross-region comparisons'
        region_labels = {
            'Cyclades': 'Cyclades', 'Crete': 'Crete', 'Ionian': 'Ionian',
            'Dodecanese': 'Dodecanese', 'Saronic': 'Saronic',
            'NE Aegean': 'North-East Aegean', 'Sporades': 'Sporades',
            'Evia': 'Evia', 'Other': 'Other',
        }
        sep = 'vs'
        href_prefix = '/compare/'
        canonical = f'{SITE_URL}/compare/'
        en_url = canonical
        el_url = f'{SITE_URL}/el/compare/'
        og_locale = 'en_US'

    def render_card(pk):
        a, b = parse_pair_key(pk)
        slug = slug_for_pair(a, b)
        if lang == 'el':
            name_a = NAMES_EL.get(a, META[a]['name'])
            name_b = NAMES_EL.get(b, META[b]['name'])
        else:
            name_a = META[a]['name']
            name_b = META[b]['name']
        href = f'{href_prefix}{slug}/'
        longform_badge = ''
        if _is_longform(pk):
            tag_label = 'Αναλυτική' if lang == 'el' else 'In-depth'
            longform_badge = f'<span class="hub-card-tag">{tag_label}</span>'
        return (
            f'<a class="hub-card" href="{esc(href)}">'
            f'<span class="hub-card-pair">{esc(name_a)} <em>{sep}</em> {esc(name_b)}</span>'
            f'{longform_badge}'
            f'<span class="hub-card-arrow" aria-hidden="true">→</span>'
            f'</a>'
        )

    def render_section(label, pks, section_id=None):
        if not pks:
            return ''
        id_attr = f' id="{section_id}"' if section_id else ''
        cards = ''.join(render_card(pk) for pk in pks)
        return (
            f'<section class="hub-section"{id_attr}>'
            f'<h2 class="hub-section-heading">{esc(label)} '
            f'<span class="hub-section-count">({len(pks)})</span></h2>'
            f'<div class="hub-grid">{cards}</div>'
            f'</section>'
        )

    # Build all sections
    sections_html = []
    if featured:
        sections_html.append(render_section(featured_label, featured, section_id='featured'))
    for region in region_order:
        if region in by_region:
            sections_html.append(render_section(region_labels[region], by_region[region]))
    if cross_region:
        sections_html.append(render_section(cross_region_label, cross_region))

    # Navigation (same structure as compare pages)
    if lang == 'el':
        nav_items = [
            ('/el/#compare', 'Σύγκριση', 'nav-compare'),
            ('/el/#match', 'Ταίριαξέ με', 'nav-match'),
            ('/el/trip-cost/', 'Μπάτζετ', 'nav-tripcost'),
            ('/el/#hopping', 'Πλοία & Νησοπορία', 'nav-hopping'),
            ('/el/festivals/', 'Γιορτές', 'nav-festivals'),
            ('/el/#data', 'Στοιχεία Νησιών', 'nav-data'),
            ('/el/#mission', 'Στόχος', 'nav-mission'),
            ('/el/#shortlist', '⭐ Λίστα μου', 'nav-shortlist'),
        ]
        privacy_link = '<a href="/el/privacy/" data-i18n="footer.privacy">Απόρρητο</a> · <a href="/el/#mission">Στόχος</a>'
    else:
        nav_items = [
            ('/#compare', 'Compare', 'nav-compare'),
            ('/#match', 'Match Me', 'nav-match'),
            ('/trip-cost/', 'Budget', 'nav-tripcost'),
            ('/#hopping', 'Ferries & Hopping', 'nav-hopping'),
            ('/festivals/', 'Festivals', 'nav-festivals'),
            ('/#data', 'Islands Data', 'nav-data'),
            ('/#mission', 'Mission', 'nav-mission'),
            ('/#shortlist', '⭐ My Shortlist', 'nav-shortlist'),
        ]
        privacy_link = '<a href="/privacy/" data-i18n="footer.privacy">Privacy</a> · <a href="/#mission">Mission</a>'

    nav_html = '\n        '.join(
        f'<a href="{esc(href)}" id="{nav_id}">{esc(label)}</a>'
        for href, label, nav_id in nav_items
    )

    page_css = '''
  main.hub-main { max-width: 960px; margin: 0 auto; padding: 32px 20px 64px; }
  .hub-hero { margin-bottom: 40px; }
  .hub-h1 {
    font-family: var(--display, Georgia, serif);
    font-size: var(--text-hero, 32px);
    margin: 0 0 8px;
    color: var(--ink-1, #222);
    line-height: 1.15;
  }
  .hub-sub {
    font-size: var(--text-body, 16px);
    line-height: 1.55;
    color: var(--ink-2, #555);
    margin: 0;
    max-width: 720px;
  }
  .hub-section { margin-bottom: 36px; }
  .hub-section-heading {
    font-family: var(--display, Georgia, serif);
    font-size: var(--text-h2, 22px);
    margin: 0 0 14px;
    color: var(--ink-1, #222);
    border-bottom: 1px solid var(--marble-3, #e0e0e0);
    padding-bottom: 6px;
  }
  .hub-section-count {
    font-size: var(--text-small, 14px);
    color: var(--ink-3, #888);
    font-weight: normal;
    margin-left: 4px;
  }
  .hub-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 10px;
  }
  .hub-card {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 14px 16px;
    background: var(--marble, #fff);
    border: 1px solid var(--marble-3, #e0e0e0);
    border-radius: 8px;
    text-decoration: none;
    color: var(--ink-1, #222);
    transition: background 0.15s, border-color 0.15s, transform 0.15s;
  }
  .hub-card:hover {
    background: var(--marble-2, #f0f0f0);
    border-color: var(--ink-3, #999);
    transform: translateY(-1px);
  }
  .hub-card-pair {
    font-size: var(--text-body, 15px);
    line-height: 1.3;
    flex: 1;
  }
  .hub-card-pair em {
    font-style: normal;
    color: var(--ink-2, #555);
    font-size: var(--text-small, 13px);
    margin: 0 4px;
  }
  .hub-card-tag {
    color: var(--aegean-dark, #076880);
    background: var(--aegean-light, #C8EEF5);
    flex-shrink: 0;
    font-size: 10.5px;
    font-weight: 800;
    padding: 2px 8px;
    border-radius: 999px;
    letter-spacing: 0.03em;
    text-transform: uppercase;
  }
  .hub-card-arrow {
    color: var(--ink-2, #555);
    flex-shrink: 0;
  }
'''

    og_image = f'{SITE_URL}/og-image.png'

    html = f'''<!DOCTYPE html>
<html lang="{'el' if lang == 'el' else 'en'}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(page_title)}</title>
<meta name="description" content="{esc(page_desc)}">
<meta name="theme-color" content="#0B8FAC">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="el" href="{el_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(page_title)}">
<meta property="og:description" content="{esc(page_desc)}">
<meta property="og:image" content="{og_image}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{og_locale}">
<meta property="og:site_name" content="Aegean Blueprint">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-FMFWLRM2J9"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-FMFWLRM2J9');</script>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css?v={ASSET_V}">
<style>{page_css}</style>
<script async data-cfasync="false" data-noptimize="1" data-no-defer="1" src="https://emrldtp.com/NTUxOTU3.js?t=551957"></script>
</head>
<body>
<header>
  <div class="header-content">
    <a class="logo-wrapper" href="{'/el/' if lang == 'el' else '/'}" style="text-decoration: none;">
      <img src="/logo-hero.svg" id="site-logo" alt="Aegean Blueprint logo">
      <span id="brand-text"><span class="brand-word">Aegean</span> <span class="brand-word">Blueprint</span></span>
    </a>
    <div class="menu-toggle" id="menu-toggle-btn"><span></span><span></span><span></span></div>
    <nav class="top-nav" id="main-nav">
        {nav_html}
    </nav>
    <a class="lang-toggle-static" href="{'/compare/' if lang == 'el' else '/el/compare/'}" style="background: none; border: 1px solid rgba(255,255,255,0.4); color: #fff; padding: 4px 10px; border-radius: 4px; text-decoration: none; font-size: 13px; white-space: nowrap;"><span style="margin-right: 4px;">🌐</span>{'EN' if lang == 'el' else 'EL'}</a>
  </div>
</header>

<main class="hub-main">
  <div class="hub-hero">
    <h1 class="hub-h1">{esc(h1_text)}</h1>
    <p class="hub-sub">{esc(subtitle)}</p>
  </div>
  {''.join(sections_html)}
</main>

<div class="cta-affiliate"><a class="ferry-btn" href="https://www.ferryhopper.com/" target="_blank" rel="noopener sponsored" data-i18n="detail.bookferry">🚢 Book ferry tickets</a><a class="car-btn" href="https://www.discovercars.com/?a_aid=antaran2" target="_blank" rel="noopener sponsored" data-i18n="detail.rentcar">🚗 Rent a car</a></div>
<footer id="site-footer">
  <div class="footer-line">
    <span class="footer-copy" data-i18n="footer.copyright">© 2026 Aegean Blueprint</span> · {privacy_link}<span class="footer-updated" id="footer-updated"></span>
  </div>
</footer>

<script src="/i18n.js?v=41"></script>
<script>
  (function() {{
    var btn = document.getElementById("menu-toggle-btn");
    if (btn) btn.addEventListener("click", function() {{ document.getElementById("main-nav").classList.toggle("open"); }});
  }})();
</script>
</body>
</html>
'''
    return html



def cleanup_leftover_dirs(current_slugs):
    """Remove compare/<slug>/ and el/compare/<slug>/ dirs that exist on disk
    but aren't in the current generation set. Protects against stale pages
    from earlier builds lingering and competing in search results.

    Only deletes dirs matching the *-vs-* pattern (paranoia — we never want
    to nuke anything outside the comparison-page namespace)."""
    current = set(current_slugs)
    removed = 0
    for parent in ('compare', 'el/compare'):
        dir_path = ROOT / parent
        if not dir_path.exists():
            continue
        for entry in dir_path.iterdir():
            if not entry.is_dir():
                continue
            name = entry.name
            # Safety guard: only touch dirs that look like comparison slugs
            if '-vs-' not in name:
                continue
            if name in current:
                continue
            # Leftover — remove it
            import shutil
            shutil.rmtree(entry)
            removed += 1
    return removed


def main():
    pair_keys = sorted(VERDICTS.keys())
    valid_pairs = []
    skipped = []
    for pk in pair_keys:
        a, b = parse_pair_key(pk)
        if a in META and b in META:
            valid_pairs.append(pk)
        else:
            skipped.append(pk)

    print(f"Generating static compare pages for {len(valid_pairs)} pairs ({len(skipped)} skipped)")

    slugs = []
    for pk in valid_pairs:
        a, b = parse_pair_key(pk)
        slug = slug_for_pair(a, b)
        slugs.append(slug)

        en_path = ROOT / 'compare' / slug / 'index.html'
        en_path.parent.mkdir(parents=True, exist_ok=True)
        en_path.write_text(render_page(pk, 'en'), encoding='utf-8')

        el_path = ROOT / 'el' / 'compare' / slug / 'index.html'
        el_path.parent.mkdir(parents=True, exist_ok=True)
        el_path.write_text(render_page(pk, 'el'), encoding='utf-8')

    print(f"✓ Wrote {len(valid_pairs) * 2} HTML files ({len(valid_pairs)} EN + {len(valid_pairs)} EL)")

    # Write hub pages (/compare/index.html and /el/compare/index.html)
    en_hub_path = ROOT / 'compare' / 'index.html'
    en_hub_path.parent.mkdir(parents=True, exist_ok=True)
    en_hub_path.write_text(render_hub_page('en', valid_pairs), encoding='utf-8')

    el_hub_path = ROOT / 'el' / 'compare' / 'index.html'
    el_hub_path.parent.mkdir(parents=True, exist_ok=True)
    el_hub_path.write_text(render_hub_page('el', valid_pairs), encoding='utf-8')

    print(f"✓ Wrote 2 hub pages (/compare/ and /el/compare/)")

    if skipped:
        print(f"⚠ Skipped pairs with unknown islands:")
        for pk in skipped:
            print(f"   - {pk}")

    removed = cleanup_leftover_dirs(slugs)
    if removed:
        print(f"✓ Cleaned up {removed} leftover comparison dirs (stale from earlier builds)")

    added = update_sitemap(slugs)
    if added:
        print(f"✓ Sitemap updated ({added} URL entries)")

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
