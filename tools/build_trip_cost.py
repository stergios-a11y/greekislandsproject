#!/usr/bin/env python3
"""Build the /trip-cost/ and /el/trip-cost/ pages — the trip cost calculator.

Data sources:
  - costs.json            room/meal/car/boat values per island + pricing rules (_meta)
  - script.js             ISLANDS_DATA: lat/lng, island_group, car_need, has_airport
  - islands/*.json        name_el + hero_photo (thumbnails)

Ferry fares are estimated from real inter-island distances (haversine),
calibrated against known economy fares (Piraeus-Paros EUR36-60, Paros-Naxos
EUR9-15, Piraeus-Santorini EUR40-75). Cross-group legs are priced via the
mainland. This gives honest bands, not quotes.

Run AFTER tools/build_costs.py (needs a fresh costs.json).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = 'https://aegeanblueprint.com'
STYLE_V = 35  # keep in sync with index.html

# ---------------------------------------------------------------- data


def parse_islands_data():
    """Extract lat/lng/group/car_need/has_airport/name from script.js ISLANDS_DATA."""
    s = (ROOT / 'script.js').read_text(encoding='utf-8')
    start = s.index('const ISLANDS_DATA = {')
    end = s.index('\n};', start)
    block = s[start:end]
    out = {}
    for m in re.finditer(r'"([a-z-]+)":\s*\{([^}]+)\}', block):
        key, body = m.group(1), m.group(2)
        def f(name, cast=float):
            mm = re.search(name + r':\s*([\d.]+)', body)
            return cast(mm.group(1)) if mm else None
        name = re.search(r'name:"([^"]+)"', body)
        group = re.search(r'island_group:"([^"]+)"', body)
        out[key] = {
            'name': name.group(1) if name else key.title(),
            'lat': f('lat'), 'lng': f('lng'),
            'car_need': f('car_need') or 0,
            'air': 'has_airport:true' in body.replace(' ', ''),
            'group': group.group(1) if group else '',
        }
    return out


def thumb(url):
    """Cloudinary hero URL -> small card thumbnail."""
    if not url:
        return ''
    return url.replace('/image/upload/', '/image/upload/w_300,h_240,c_fill,g_auto,q_auto,f_auto/', 1)


def build_dataset():
    costs = json.loads((ROOT / 'costs.json').read_text(encoding='utf-8'))
    meta, cost_islands = costs['_meta'], costs['islands']
    geo = parse_islands_data()
    data = {}
    for key, c in cost_islands.items():
        g = geo.get(key)
        if not g:
            print(f'  ! {key}: in costs.json but not in ISLANDS_DATA — skipped')
            continue
        ij = json.loads((ROOT / 'islands' / f'{key}.json').read_text(encoding='utf-8'))
        boat = c.get('boat')
        if boat:
            # try to find a Greek title for the boat day among the itinerary days
            name_el = None
            for d in (ij.get('itinerary', {}) or {}).get('days', []):
                if d.get('title') == boat['name'] and d.get('title_el'):
                    name_el = d['title_el']
            boat = {'n': boat['name'], 'nel': name_el or boat['name'], 'pp': boat['pp']}
        data[key] = {
            'n': g['name'],
            'nel': ij.get('name_el') or g['name'],
            'img': thumb(ij.get('hero_photo') or ''),
            'lat': g['lat'], 'lng': g['lng'],
            'g': g['group'], 'cn': g['car_need'], 'air': g['air'],
            'room': c['room'], 'meal': c['meal_pp_mid'], 'car': c['car_day'],
            'boat': boat,
        }
    return meta, data


# ---------------------------------------------------------------- strings

STR = {
    'en': {
        'lang': 'en', 'base': '/', 'other': '/el/trip-cost/', 'lang_label': 'EL',
        'title': 'Greek Island Trip Cost Calculator — ferries, rooms, car, food | Aegean Blueprint',
        'desc': 'Build your island route and get an honest cost estimate: ferry fares, room prices by month, car hire, food — for all 88 Greek islands. No fake precision.',
        'h1': 'What will your island trip cost?',
        'sub': 'Build your route, set your nights, and get an honest estimate — ferry fares from real distances, room prices by month, no fake precision. Then book the pieces that need booking.',
        'presets': 'Start from a route', 'when_who': 'When & who', 'travellers': 'Travellers',
        'noneu': '🌍 Travelling from outside the EU', 'noneu_small': '(adds eSIM & insurance)',
        'comfort': 'Comfort',
        'tier_budget': 'Budget', 'tier_budget_s': 'rooms & gyros',
        'tier_mid': 'Mid-range', 'tier_mid_s': 'nice room, taverna dinners',
        'tier_comfort': 'Comfort', 'tier_comfort_s': 'boutique, no counting',
        'months': {'apr': 'April', 'may': 'May', 'jun': 'June', 'jul': 'July', 'aug': 'August', 'sep': 'September', 'oct': 'October'},
        'add_island': 'Add an island:', 'add_ph': 'Type an island…',
        'departure': 'departure', 'back_to': 'back to', 'ferry_to': 'ferry to',
        'via_mainland': 'via mainland — no direct ferry likely', 'fly_hint': '✈ flying is often cheaper',
        'ionian_gate': 'nearest mainland port (drive or KTEL bus from Athens)',
        'nights': 'nights', 'night': 'night', 'car': '🚗 car', 'boat_day': '⛵ boat day',
        'rooms_per_night': 'rooms', 'per_night': '/night',
        'carless_note': 'No car on {n} (car-reliant) — we price a central room so you can walk to things (+{p}%).',
        'estimate': 'Your trip estimate',
        'li_ferries': 'Ferries', 'li_legs': 'legs', 'li_pax': 'pax', 'book_ferry': 'Book on Ferryhopper →',
        'li_rooms': 'Rooms', 'central': '(central)',
        'li_car': 'Car', 'days': 'days', 'book_car': 'Compare on Discover Cars →',
        'li_fuel': 'Fuel', 'li_boat': 'Boat days', 'boat_rec': 'our recommended trips',
        'li_food': 'Food & drink', 'food_s': 'pp/day', 'li_esim': 'eSIM — Greece data', 'esim_s': '10GB plan', 'book_esim': 'Get eSIM →',
        'li_insurance': 'Travel insurance', 'ins_days': 'days',
        'total': 'Total (excl. flights)', 'pp': 'per person',
        'cta_ferry': '🚢 Book ferries', 'cta_car': '🚗 Get the car',
        'assume': '<b>How we estimate:</b> economy ferry fares from real route distances · room prices for a decent double in {month} · one taverna meal + breakfast/snacks per day · car only where you toggled it. Museums, sunbeds and cocktails are yours.',
        'honest': 'Every figure is a typical price, not a quote — expect real prices roughly ±20% either side, set by ferry companies and hotels, not us. Book early for July–August; ferries sell out.',
        'guide': 'guide →',
        'remove': 'Remove',
        'footer_privacy': 'Privacy', 'footer_mission': 'Mission', 'footer_lang': 'Ελληνικά',
        'nav': [('/#compare', 'Compare'), ('/#match', 'Match Me'), ('/trip-cost/', 'Trip Cost', True),
                ('/#hopping', 'Ferries & Hopping'), ('/festivals/', 'Festivals'),
                ('/#data', 'Islands Data'), ('/#shortlist', '⭐ My Shortlist')],
        'preset_defs': [
            ('classic', '🏛 Cyclades First-Timer', 'Paros · Naxos · Santorini — 8 nights'),
            ('beach', '🏖 Beach Chaser', 'Milos · Ios — 7 nights'),
            ('easy', '⛵ Easy Pair', 'Paros · Naxos — 7 nights'),
            ('ionian', '🌲 Ionian Green', 'Lefkada · Meganisi — 6 nights'),
        ],
    },
    'el': {
        'lang': 'el', 'base': '/el/', 'other': '/trip-cost/', 'lang_label': 'EN',
        'title': 'Υπολογιστής Κόστους Ταξιδιού στα Ελληνικά Νησιά — πλοία, δωμάτια, αυτοκίνητο | Aegean Blueprint',
        'desc': 'Φτιάξε τη διαδρομή σου και δες μια ειλικρινή εκτίμηση κόστους: εισιτήρια πλοίων, δωμάτια ανά μήνα, ενοικίαση αυτοκινήτου, φαγητό — και για τα 88 νησιά.',
        'h1': 'Πόσο θα κοστίσει το ταξίδι σου στα νησιά;',
        'sub': 'Φτιάξε τη διαδρομή, όρισε τις νύχτες και δες μια ειλικρινή εκτίμηση — ναύλα από πραγματικές αποστάσεις, τιμές δωματίων ανά μήνα, χωρίς ψεύτικη ακρίβεια. Μετά κλείσε ό,τι χρειάζεται κράτηση.',
        'presets': 'Ξεκίνα από μια διαδρομή', 'when_who': 'Πότε & ποιοι', 'travellers': 'Ταξιδιώτες',
        'noneu': '🌍 Ταξιδεύεις από χώρα εκτός ΕΕ', 'noneu_small': '(προσθέτει eSIM & ασφάλεια)',
        'comfort': 'Άνεση',
        'tier_budget': 'Οικονομικά', 'tier_budget_s': 'δωμάτια & γύρος',
        'tier_mid': 'Μεσαία', 'tier_mid_s': 'καλό δωμάτιο, ταβέρνες',
        'tier_comfort': 'Άνετα', 'tier_comfort_s': 'boutique, χωρίς μέτρημα',
        'months': {'apr': 'Απρίλιος', 'may': 'Μάιος', 'jun': 'Ιούνιος', 'jul': 'Ιούλιος', 'aug': 'Αύγουστος', 'sep': 'Σεπτέμβριος', 'oct': 'Οκτώβριος'},
        'add_island': 'Πρόσθεσε νησί:', 'add_ph': 'Γράψε ένα νησί…',
        'departure': 'αναχώρηση', 'back_to': 'επιστροφή', 'ferry_to': 'πλοίο προς',
        'via_mainland': 'μέσω στεριάς — μάλλον χωρίς απευθείας πλοίο', 'fly_hint': '✈ συχνά συμφέρει αεροπορικώς',
        'ionian_gate': 'κοντινότερο λιμάνι στεριάς (οδικώς / ΚΤΕΛ από Αθήνα)',
        'nights': 'νύχτες', 'night': 'νύχτα', 'car': '🚗 αυτοκίνητο', 'boat_day': '⛵ ημέρα σκάφους',
        'rooms_per_night': 'δωμάτια', 'per_night': '/νύχτα',
        'carless_note': 'Χωρίς αυτοκίνητο στη {n} (το χρειάζεται) — υπολογίζουμε κεντρικό δωμάτιο για να πηγαίνεις παντού με τα πόδια (+{p}%).',
        'estimate': 'Η εκτίμηση του ταξιδιού σου',
        'li_ferries': 'Πλοία', 'li_legs': 'διαδρομές', 'li_pax': 'άτομα', 'book_ferry': 'Κράτηση στο Ferryhopper →',
        'li_rooms': 'Δωμάτια', 'central': '(κεντρικό)',
        'li_car': 'Αυτοκίνητο', 'days': 'μέρες', 'book_car': 'Σύγκριση στο Discover Cars →',
        'li_fuel': 'Καύσιμα', 'li_boat': 'Ημέρες σκάφους', 'boat_rec': 'οι προτεινόμενες εκδρομές μας',
        'li_food': 'Φαγητό & ποτό', 'food_s': 'ανά άτομο/μέρα', 'li_esim': 'eSIM — δεδομένα Ελλάδα', 'esim_s': 'πακέτο 10GB', 'book_esim': 'Πάρε eSIM →',
        'li_insurance': 'Ταξιδιωτική ασφάλεια', 'ins_days': 'μέρες',
        'total': 'Σύνολο (χωρίς αεροπορικά)', 'pp': 'ανά άτομο',
        'cta_ferry': '🚢 Κράτηση πλοίων', 'cta_car': '🚗 Κλείσε αυτοκίνητο',
        'assume': '<b>Πώς υπολογίζουμε:</b> οικονομικά ναύλα από πραγματικές αποστάσεις · τιμές για ένα καλό δίκλινο τον {month} · ένα γεύμα ταβέρνας + πρωινό/σνακ τη μέρα · αυτοκίνητο μόνο όπου το ενεργοποίησες. Μουσεία, ξαπλώστρες και κοκτέιλ δικά σου.',
        'honest': 'Κάθε ποσό είναι τυπική τιμή, όχι προσφορά — οι πραγματικές τιμές κινούνται περίπου ±20%, και τις ορίζουν ακτοπλοϊκές και ξενοδοχεία, όχι εμείς. Για Ιούλιο–Αύγουστο κλείσε νωρίς· τα πλοία εξαντλούνται.',
        'guide': 'οδηγός →',
        'remove': 'Αφαίρεση',
        'footer_privacy': 'Απόρρητο', 'footer_mission': 'Στόχος', 'footer_lang': 'English',
        'nav': [('/el/#compare', 'Σύγκριση'), ('/el/#match', 'Βρες το Νησί σου'), ('/el/trip-cost/', 'Κόστος Ταξιδιού', True),
                ('/el/#hopping', 'Πλοία & Νησοπορία'), ('/el/festivals/', 'Γιορτές'),
                ('/el/#data', 'Στοιχεία Νησιών'), ('/el/#shortlist', '⭐ Η Λίστα μου')],
        'preset_defs': [
            ('classic', '🏛 Πρώτη φορά Κυκλάδες', 'Πάρος · Νάξος · Σαντορίνη — 8 νύχτες'),
            ('beach', '🏖 Κυνηγός παραλιών', 'Μήλος · Ίος — 7 νύχτες'),
            ('easy', '⛵ Εύκολο δίδυμο', 'Πάρος · Νάξος — 7 νύχτες'),
            ('ionian', '🌲 Πράσινο Ιόνιο', 'Λευκάδα · Μεγανήσι — 6 νύχτες'),
        ],
    },
}

PRESETS_JS = """{
 classic:[{k:'paros',n:3,c:false,b:true},{k:'naxos',n:3,c:true,b:false},{k:'santorini',n:2,c:false,b:true}],
 beach:[{k:'milos',n:4,c:true,b:true},{k:'ios',n:3,c:false,b:false}],
 easy:[{k:'paros',n:4,c:true,b:false},{k:'naxos',n:3,c:false,b:false}],
 ionian:[{k:'lefkada',n:4,c:true,b:false},{k:'meganisi',n:2,c:false,b:true}]
}"""


# ---------------------------------------------------------------- page

def render_page(lang, meta, data):
    t = STR[lang]
    is_el = lang == 'el'
    url = f'{SITE_URL}/el/trip-cost/' if is_el else f'{SITE_URL}/trip-cost/'
    url_en, url_el = f'{SITE_URL}/trip-cost/', f'{SITE_URL}/el/trip-cost/'

    active_attr = ' class="active"'
    nav_html = '\n      '.join(
        f'<a href="{item[0]}"{active_attr if len(item) > 2 else ""}>{item[1]}</a>'
        for item in t['nav']
    )
    presets_html = '\n          '.join(
        f'<span class="tc-chip tc-preset{" on" if k == "classic" else ""}" data-p="{k}">{lbl}<br><small>{sub}</small></span>'
        for k, lbl, sub in t['preset_defs']
    )
    months_html = ''.join(
        f'<span class="tc-chip{" on" if m == "jun" else ""}" data-m="{m}">{name}</span>'
        for m, name in t['months'].items()
    )

    # strings needed inside JS
    js_t = {k: t[k] for k in (
        'departure', 'back_to', 'ferry_to', 'via_mainland', 'fly_hint', 'ionian_gate',
        'nights', 'night', 'car', 'boat_day', 'rooms_per_night', 'per_night', 'carless_note',
        'estimate', 'li_ferries', 'li_legs', 'li_pax', 'book_ferry', 'li_rooms', 'central',
        'li_car', 'days', 'book_car', 'li_fuel', 'li_boat', 'boat_rec', 'li_food', 'food_s',
        'li_esim', 'esim_s', 'book_esim', 'li_insurance', 'ins_days', 'total', 'pp',
        'cta_ferry', 'cta_car',
        'assume', 'honest', 'guide', 'remove',
        'tier_budget', 'tier_mid', 'tier_comfort',
    )}
    js_t['months'] = t['months']

    schema = json.dumps({
        '@context': 'https://schema.org', '@type': 'WebApplication',
        'name': 'Greek Island Trip Cost Calculator' if not is_el else 'Υπολογιστής Κόστους Ταξιδιού στα Ελληνικά Νησιά',
        'url': url, 'applicationCategory': 'TravelApplication',
        'operatingSystem': 'Web',
        'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'EUR'},
    }, ensure_ascii=False)

    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t['title']}</title>
<meta name="description" content="{t['desc']}">
<meta name="theme-color" content="#0B8FAC">
<meta name="author" content="Stergios Gousios">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{url_en}">
<link rel="alternate" hreflang="el" href="{url_el}">
<link rel="alternate" hreflang="x-default" href="{url_en}">
<meta property="og:title" content="{t['h1']}">
<meta property="og:description" content="{t['desc']}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE_URL}/og/naxos.jpg">
<link rel="icon" href="/logo-hero.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css?v={STYLE_V}">
<script type="application/ld+json">{schema}</script>
<style>
.tc-page{{max-width:1120px;margin:0 auto;padding:0 22px 60px;font-family:'Nunito Sans',sans-serif}}
.tc-head{{margin:30px 0 6px}}
.tc-head h1{{font-family:'Alegreya',serif;font-weight:800;font-size:34px;margin:0}}
.tc-head p{{color:var(--ink-3,#637080);font-size:14.5px;margin-top:6px;max-width:680px}}
.tc-grid{{display:grid;grid-template-columns:1fr 380px;gap:24px;margin-top:22px;align-items:start}}
.tc-ctrl{{background:var(--card-bg,#fff);border-radius:16px;box-shadow:0 4px 18px rgba(26,35,50,.09);padding:16px 18px;margin-bottom:14px}}
.tc-ctrl h3{{font-family:'Nunito',sans-serif;font-weight:800;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3,#637080);margin:0 0 10px}}
.tc-chips{{display:flex;gap:8px;flex-wrap:wrap}}
.tc-chip{{border:1.5px solid rgba(26,35,50,.13);background:var(--card-bg,#fff);border-radius:14px;padding:7px 15px;font-weight:700;font-size:13px;cursor:pointer;color:var(--ink-2,#2E3D50);user-select:none}}
.tc-chip small{{font-weight:600;color:var(--ink-3,#637080)}}
.tc-chip.on{{border-color:#0B8FAC;background:rgba(200,238,245,.55);color:#076880}}
.tc-trav{{display:flex;align-items:center;gap:14px}}
.tc-step{{display:flex;align-items:center;gap:10px;background:rgba(232,247,251,.9);border-radius:999px;padding:4px}}
.tc-step button{{width:30px;height:30px;border:0;border-radius:50%;background:#fff;font-weight:800;font-size:16px;cursor:pointer;color:#076880;box-shadow:0 1px 4px rgba(26,35,50,.15)}}
.tc-step span{{font-weight:800;font-size:15px;min-width:20px;text-align:center;color:var(--ink-1,#1A2332)}}
.tc-sw{{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;font-weight:700;color:var(--ink-3,#637080);cursor:pointer;user-select:none}}
.tc-sw .s{{width:34px;height:20px;border-radius:999px;background:rgba(26,35,50,.15);position:relative;transition:background .15s;flex-shrink:0}}
.tc-sw .s::after{{content:'';position:absolute;top:2px;left:2px;width:16px;height:16px;border-radius:50%;background:#fff;transition:left .15s}}
.tc-sw.on .s{{background:#0B8FAC}}
.tc-sw.on .s::after{{left:16px}}
.tc-leg{{display:flex;align-items:center;gap:10px;padding:8px 4px;color:var(--ink-3,#637080);font-size:13px;font-weight:700}}
.tc-leg .l{{flex:0 0 26px;text-align:center;font-size:16px}}
.tc-leg .fp{{margin-left:auto;font-weight:800;color:var(--ink-2,#2E3D50);white-space:nowrap}}
.tc-leg .hint{{font-weight:600;font-size:11px;color:#C6421F}}
.tc-card{{display:flex;gap:14px;background:var(--card-bg,#fff);border-radius:16px;box-shadow:0 4px 18px rgba(26,35,50,.09);padding:12px;align-items:center}}
.tc-card img{{width:92px;height:72px;object-fit:cover;border-radius:10px;flex-shrink:0;background:#dde8ec}}
.tc-cb{{flex:1;min-width:0}}
.tc-cn{{font-family:'Alegreya',serif;font-weight:700;font-size:19px;color:var(--ink-1,#1A2332)}}
.tc-cn a{{font-family:'Nunito Sans',sans-serif;font-size:11.5px;font-weight:700;color:#0B8FAC;text-decoration:none;margin-left:8px}}
.tc-cs{{font-size:12px;color:var(--ink-3,#637080);margin-top:1px}}
.tc-cc{{display:flex;gap:14px;align-items:center;margin-top:8px;flex-wrap:wrap}}
.tc-n{{display:flex;align-items:center;gap:8px;font-size:13px;font-weight:700;color:var(--ink-2,#2E3D50)}}
.tc-n button{{width:24px;height:24px;border:1.5px solid #C8EEF5;background:var(--card-bg,#fff);border-radius:50%;cursor:pointer;font-weight:800;color:#076880}}
.tc-warn{{font-size:11.5px;color:#C6421F;margin-top:6px;font-weight:700}}
.tc-x{{border:0;background:transparent;color:var(--ink-4,#A0ADB8);font-size:17px;cursor:pointer;align-self:flex-start}}
.tc-add{{display:flex;gap:8px;align-items:center;margin:10px 0 0 40px;flex-wrap:wrap;position:relative}}
.tc-add>span{{font-size:12.5px;font-weight:800;color:var(--ink-3,#637080)}}
.tc-addbtn{{border:1.5px dashed #0B8FAC;background:rgba(232,247,251,.9);color:#076880;border-radius:999px;padding:6px 14px;font-weight:800;font-size:12.5px;cursor:pointer}}
.tc-search{{border:1.5px solid rgba(26,35,50,.15);border-radius:999px;padding:7px 14px;font-size:13px;font-family:inherit;min-width:170px;background:var(--card-bg,#fff);color:var(--ink-1,#1A2332)}}
.tc-sug{{position:absolute;top:100%;left:0;margin-top:6px;background:var(--card-bg,#fff);border-radius:12px;box-shadow:0 10px 30px rgba(26,35,50,.25);z-index:50;min-width:230px;max-height:260px;overflow:auto;display:none}}
.tc-sug div{{padding:9px 14px;font-size:13.5px;font-weight:700;cursor:pointer;color:var(--ink-1,#1A2332)}}
.tc-sug div:hover{{background:rgba(200,238,245,.5)}}
.tc-sum{{background:var(--card-bg,#fff);border-radius:18px;box-shadow:0 10px 34px rgba(26,35,50,.14);padding:20px;position:sticky;top:16px}}
.tc-sum h2{{font-family:'Alegreya',serif;font-weight:800;font-size:21px;margin:0 0 2px;color:var(--ink-1,#1A2332)}}
.tc-ss{{font-size:12px;color:var(--ink-3,#637080);margin-bottom:14px}}
.tc-li{{display:grid;grid-template-columns:22px 1fr 96px;column-gap:8px;align-items:start;padding:9px 0;border-bottom:1px dashed rgba(26,35,50,.12);font-size:13.5px}}
.tc-li .lbl{{color:var(--ink-2,#2E3D50);font-weight:600;min-width:0}}
.tc-li .lbl small{{display:block;color:var(--ink-4,#A0ADB8);font-size:11px;font-weight:600;overflow:hidden;text-overflow:ellipsis}}
.tc-li .amt{{font-weight:800;white-space:nowrap;text-align:right;font-variant-numeric:tabular-nums;color:var(--ink-1,#1A2332)}}
.tc-li .bk{{grid-column:2/4;justify-self:end;margin-top:5px;font-size:11px;font-weight:800;color:#C6421F;white-space:nowrap;text-decoration:none;background:#FEF2EE;padding:3px 9px;border-radius:999px}}
.tc-tot{{display:flex;align-items:baseline;margin-top:14px}}
.tc-tot .t1{{font-family:'Nunito',sans-serif;font-weight:800;font-size:15px;color:var(--ink-1,#1A2332)}}
.tc-tot .amt{{margin-left:auto;font-family:'Nunito',sans-serif;font-weight:800;font-size:24px;color:#076880}}
.tc-pp{{text-align:right;font-size:12px;color:var(--ink-3,#637080);margin-top:2px}}
.tc-assume{{margin-top:14px;background:rgba(232,247,251,.9);border-radius:12px;padding:11px 13px;font-size:11.5px;color:var(--ink-2,#2E3D50);line-height:1.55}}
.tc-assume b{{color:#076880}}
.tc-honest{{margin-top:10px;font-size:11px;color:var(--ink-4,#A0ADB8);font-style:italic;line-height:1.5}}
.tc-ctas{{display:flex;gap:8px;margin-top:14px}}
.tc-cta{{flex:1;text-align:center;border-radius:12px;padding:11px 8px;font-family:'Nunito',sans-serif;font-weight:800;font-size:13.5px;text-decoration:none}}
.tc-cta.f{{background:#E8522A;color:#fff}}
.tc-cta.c{{background:#0B8FAC;color:#fff}}
@media(max-width:900px){{.tc-grid{{grid-template-columns:1fr}}.tc-sum{{position:static}}.tc-add{{margin-left:0}}}}
.seo-footer{{font-size:13px;color:var(--ink-3,#637080)}}
.seo-footer a{{color:#0B8FAC;text-decoration:none}}
</style>
</head>
<body>
<header>
  <div class="header-content">
    <a class="logo-wrapper" href="{t['base']}" style="text-decoration: none;">
      <img src="/logo-hero.svg" id="site-logo" alt="Aegean Blueprint logo">
      <span id="brand-text"><span class="brand-word">Aegean</span> <span class="brand-word">Blueprint</span></span>
    </a>
    <div class="menu-toggle" id="menu-toggle-btn"><span></span><span></span><span></span></div>
    <nav class="top-nav" id="main-nav">
      {nav_html}
    </nav>
    <a class="lang-toggle-static" href="{t['other']}" style="background: none; border: 1px solid rgba(255,255,255,0.4); color: #fff; padding: 4px 10px; border-radius: 4px; text-decoration: none; font-size: 13px; white-space: nowrap;"><span style="margin-right: 4px;">🌐</span>{t['lang_label']}</a>
  </div>
</header>

<main class="tc-page">
  <div class="tc-head">
    <h1>{t['h1']}</h1>
    <p>{t['sub']}</p>
  </div>

  <div class="tc-grid">
    <div>
      <div class="tc-ctrl">
        <h3>{t['presets']}</h3>
        <div class="tc-chips" id="tc-presets">
          {presets_html}
        </div>
      </div>

      <div class="tc-ctrl">
        <h3>{t['when_who']}</h3>
        <div style="display:flex;gap:26px;flex-wrap:wrap;align-items:center">
          <div class="tc-chips" id="tc-months">{months_html}</div>
          <div class="tc-trav">
            <span style="font-size:13px;font-weight:700;color:var(--ink-3,#637080)">{t['travellers']}</span>
            <div class="tc-step"><button id="tc-pax-minus">−</button><span id="tc-pax">2</span><button id="tc-pax-plus">+</button></div>
          </div>
        </div>
        <div style="margin-top:12px">
          <span class="tc-sw" id="tc-noneu"><span class="s"></span> {t['noneu']} <small style="font-weight:600;color:var(--ink-4,#A0ADB8)">{t['noneu_small']}</small></span>
        </div>
        <div style="margin-top:12px">
          <h3 style="margin-bottom:8px">{t['comfort']}</h3>
          <div class="tc-chips" id="tc-tiers">
            <span class="tc-chip" data-t="budget">{t['tier_budget']}<br><small>{t['tier_budget_s']}</small></span>
            <span class="tc-chip on" data-t="mid">{t['tier_mid']}<br><small>{t['tier_mid_s']}</small></span>
            <span class="tc-chip" data-t="comfort">{t['tier_comfort']}<br><small>{t['tier_comfort_s']}</small></span>
          </div>
        </div>
      </div>

      <div id="tc-route"></div>

      <div class="tc-add">
        <span>{t['add_island']}</span>
        <input class="tc-search" id="tc-search" placeholder="{t['add_ph']}" autocomplete="off">
        <div class="tc-sug" id="tc-sug"></div>
        <span id="tc-quick"></span>
      </div>
    </div>

    <div class="tc-sum" id="tc-summary"></div>
  </div>
</main>

<footer class="seo-footer" style="max-width:1120px;margin:0 auto;padding:20px 22px">
  <p>© 2026 Aegean Blueprint · <a href="{url_el if not is_el else url_en}">{t['footer_lang']}</a> · <a href="{'/el/privacy/' if is_el else '/privacy/'}">{t['footer_privacy']}</a> · <a href="{'/el/#mission' if is_el else '/#mission'}">{t['footer_mission']}</a></p>
</footer>

<script>
document.getElementById("menu-toggle-btn").addEventListener("click",function(){{var n=document.getElementById("main-nav");n.classList.toggle("open");this.classList.toggle("open");}});

// ---------------- data (generated by tools/build_trip_cost.py) ----------------
const LANG={json.dumps(lang)};
const T={json.dumps(js_t, ensure_ascii=False)};
const CFG={json.dumps({k: meta[k] for k in ('season_room', 'season_car', 'range_lo', 'range_hi', 'meal_budget', 'meal_comfort', 'carless_central_premium', 'fuel_per_day')})};
const ISL={json.dumps(data, ensure_ascii=False, separators=(',', ':'))};
const PRESETS={PRESETS_JS};
const QUICK=['santorini','milos','ios','folegandros','sifnos'];
const GATES={{'Piraeus':{{lat:37.942,lng:23.646,en:'Piraeus (Athens)',el:'Πειραιάς (Αθήνα)'}},'Volos':{{lat:39.362,lng:22.942,en:'Volos / Ag. Konstantinos',el:'Βόλος / Αγ. Κωνσταντίνος'}}}};

// ---------------- model ----------------
const iname=k=>LANG==='el'?(ISL[k].nel||ISL[k].n):ISL[k].n;
function haversine(a,b){{const R=6371,d=Math.PI/180;const dLat=(b.lat-a.lat)*d,dLng=(b.lng-a.lng)*d;
  const h=Math.sin(dLat/2)**2+Math.cos(a.lat*d)*Math.cos(b.lat*d)*Math.sin(dLng/2)**2;return 2*R*Math.asin(Math.sqrt(h));}}
function nmFare(km){{const nm=km/1.852;
  return [Math.min(85,Math.max(7,Math.round(7+0.33*nm))),Math.min(120,Math.max(12,Math.round(12+0.55*nm)))];}}
function gateOf(k){{const g=ISL[k].g;
  if(g==='Sporades')return GATES.Volos;
  if(g==='Ionian')return null; // local mainland port, priced flat
  return GATES.Piraeus;}}
// fare between two points of the trip; 'M' = mainland start/end
function legInfo(a,b){{
  const isl=a==='M'?b:a, other=a==='M'?a:b;
  if(a==='M'||b==='M'){{
    const k=a==='M'?b:a, gate=gateOf(k);
    if(!gate)return{{f:[15,40],label:T.ionian_gate,fly:false}};
    const f=nmFare(haversine(gate,ISL[k]));
    const fly=ISL[k].air&&f[1]>=60;
    return{{f:f,label:gate[LANG],fly:fly}};
  }}
  if(ISL[a].g===ISL[b].g){{return{{f:nmFare(haversine(ISL[a],ISL[b])),label:null,fly:false}};}}
  // cross-group: via mainland = two legs
  const ga=gateOf(a),gb=gateOf(b);
  const fa=ga?nmFare(haversine(ga,ISL[a])):[15,40];
  const fb=gb?nmFare(haversine(gb,ISL[b])):[15,40];
  const f=[fa[0]+fb[0],fa[1]+fb[1]];
  return{{f:f,label:T.via_mainland,fly:(ISL[a].air&&ISL[b].air)}};
}}
const eur=n=>'€'+Math.round(n).toLocaleString(LANG==='el'?'el-GR':'en-GB');
const rnd=n=>n<100?Math.round(n/5)*5:Math.round(n/10)*10;
const mid=f=>(f[0]+f[1])/2;

// ---------------- state ----------------
let state={{month:'jun',pax:2,tier:'mid',nonEU:false,trip:JSON.parse(JSON.stringify(PRESETS.classic))}};
// URL params: ?i=milos:4:c:b,ios:3&m=aug&pax=2&tier=mid
(function(){{
  const q=new URLSearchParams(location.search);
  try{{const saved=localStorage.getItem('tc-state');if(saved&&!q.get('i')){{state=JSON.parse(saved);}}}}catch(e){{}}
  if(q.get('i')){{
    const trip=q.get('i').split(',').map(s=>{{const p=s.split(':');
      return ISL[p[0]]?{{k:p[0],n:Math.min(14,Math.max(1,parseInt(p[1])||3)),c:p.includes('c'),b:p.includes('b')}}:null;}}).filter(Boolean);
    if(trip.length)state.trip=trip;
  }}
  if(q.get('m')&&CFG.season_room[q.get('m')])state.month=q.get('m');
  if(q.get('pax'))state.pax=Math.min(8,Math.max(1,parseInt(q.get('pax'))||2));
  if(['budget','mid','comfort'].includes(q.get('tier')))state.tier=q.get('tier');
  if(!CFG.season_room[state.month])state.month='jun';
  state.trip=(state.trip||[]).filter(t=>ISL[t.k]);
  if(!state.trip.length)state.trip=JSON.parse(JSON.stringify(PRESETS.classic));
}})();
function sync(){{
  try{{localStorage.setItem('tc-state',JSON.stringify(state));}}catch(e){{}}
  const i=state.trip.map(t=>t.k+':'+t.n+(t.c?':c':'')+(t.b?':b':'')).join(',');
  history.replaceState(null,'','?i='+i+'&m='+state.month+'&pax='+state.pax+'&tier='+state.tier);
}}

// per-tier room price for an island in the selected month
function roomNight(k){{return ISL[k].room[state.tier]*CFG.season_room[state.month];}}
function mealDay(k){{const m=ISL[k].meal;return state.tier==='budget'?m*CFG.meal_budget:state.tier==='comfort'?m*CFG.meal_comfort:m;}}

// ---------------- render ----------------
function render(){{
  document.getElementById('tc-pax').textContent=state.pax;
  document.querySelectorAll('#tc-months .tc-chip').forEach(c=>c.classList.toggle('on',c.dataset.m===state.month));
  document.querySelectorAll('#tc-tiers .tc-chip').forEach(c=>c.classList.toggle('on',c.dataset.t===state.tier));
  document.getElementById('tc-noneu').classList.toggle('on',state.nonEU);

  const sR=CFG.season_room[state.month],sC=CFG.season_car[state.month];
  let h='';
  const first=state.trip[0].k,last=state.trip[state.trip.length-1].k;
  const dep=legInfo('M',first);
  h+=`<div class="tc-leg"><span class="l">🛳</span> ${{dep.label||''}} — ${{T.departure}} ${{dep.fly?'<span class="hint">'+T.fly_hint+'</span>':''}}<span class="fp">€${{rnd(mid(dep.f))}} pp</span></div>`;
  state.trip.forEach((t,i)=>{{
    const isl=ISL[t.k],rn=roomNight(t.k);
    const guide=(LANG==='el'?'/el':'')+'/island/'+t.k+'/';
    h+=`<div class="tc-card">
      ${{isl.img?`<img src="${{isl.img}}" alt="${{iname(t.k)}}" loading="lazy">`:''}}
      <div class="tc-cb">
        <div class="tc-cn">${{iname(t.k)}}<a href="${{guide}}">${{T.guide}}</a></div>
        <div class="tc-cs">${{T.rooms_per_night}} ${{eur(rnd(rn))}}${{T.per_night}} · ${{T.months[state.month]}}</div>
        <div class="tc-cc">
          <span class="tc-n"><button data-a="n-" data-i="${{i}}">−</button> ${{t.n}} ${{t.n===1?T.night:T.nights}} <button data-a="n+" data-i="${{i}}">+</button></span>
          ${{isl.car?`<span class="tc-sw ${{t.c?'on':''}}" data-a="car" data-i="${{i}}"><span class="s"></span> ${{T.car}}</span>`:''}}
          ${{isl.boat?`<span class="tc-sw ${{t.b?'on':''}}" data-a="boat" data-i="${{i}}"><span class="s"></span> ${{T.boat_day}} <small>€${{isl.boat.pp}} pp</small></span>`:''}}
        </div>
        ${{(!t.c&&isl.cn>=4&&isl.car)?`<div class="tc-warn">${{T.carless_note.replace('{{n}}',iname(t.k)).replace('{{p}}',Math.round((CFG.carless_central_premium-1)*100))}}</div>`:''}}
      </div>
      <button class="tc-x" data-a="rm" data-i="${{i}}" title="${{T.remove}}">✕</button>
    </div>`;
    const next=state.trip[i+1];
    if(next){{const li=legInfo(t.k,next.k);
      h+=`<div class="tc-leg"><span class="l">⛴</span> ${{T.ferry_to}} ${{iname(next.k)}}${{li.label?' <small>('+li.label+')</small>':''}} ${{li.fly?'<span class="hint">'+T.fly_hint+'</span>':''}}<span class="fp">€${{rnd(mid(li.f))}} pp</span></div>`;}}
  }});
  const ret=legInfo(last,'M');
  h+=`<div class="tc-leg"><span class="l">🛳</span> ${{T.back_to}} ${{ret.label||''}}<span class="fp">€${{rnd(mid(ret.f))}} pp</span></div>`;
  document.getElementById('tc-route').innerHTML=h;

  // quick-add buttons
  document.getElementById('tc-quick').innerHTML=QUICK.filter(k=>!state.trip.some(t=>t.k===k)).slice(0,3)
    .map(k=>`<button class="tc-addbtn" data-add="${{k}}">+ ${{iname(k)}}</button>`).join(' ');

  // ---------------- totals (single typical figures) ----------------
  const nightsTotal=state.trip.reduce((a,t)=>a+t.n,0);
  let tot=0,li='';
  const line=(ic,lbl,small,amt,book,url)=>`<div class="tc-li"><span>${{ic}}</span><span class="lbl">${{lbl}}<small>${{small}}</small></span><span class="amt">${{eur(rnd(amt))}}</span>${{book?`<a class="bk" href="${{url}}" target="_blank" rel="noopener sponsored">${{book}}</a>`:''}}</div>`;
  // ferries
  let fsum=0;const legs=[['M',first],...state.trip.slice(0,-1).map((t,i)=>[t.k,state.trip[i+1].k]),[last,'M']];
  legs.forEach(([a,b])=>{{fsum+=mid(legInfo(a,b).f)*state.pax;}});
  li+=line('⛴',T.li_ferries,`${{legs.length}} ${{T.li_legs}} × ${{state.pax}} ${{T.li_pax}}`,fsum,T.book_ferry,'https://www.ferryhopper.com/'+(LANG==='el'?'el/':'en/'));
  tot+=fsum;
  // rooms
  let rsum=0;
  state.trip.forEach(t=>{{const rn=roomNight(t.k);
    const mult=(!t.c&&ISL[t.k].cn>=4&&ISL[t.k].car)?CFG.carless_central_premium:1;
    rsum+=rn*t.n*mult;}});
  li+=line('🛏',`${{T.li_rooms}} — ${{nightsTotal}} ${{T.nights}}`,state.trip.map(t=>`${{iname(t.k)}} ${{t.n}}${{(!t.c&&ISL[t.k].cn>=4&&ISL[t.k].car)?' '+T.central:''}}`).join(' · '),rsum,null);
  tot+=rsum;
  // car + fuel
  let csum=0,cd=0;
  state.trip.forEach(t=>{{if(t.c&&ISL[t.k].car){{csum+=ISL[t.k].car*sC*t.n;cd+=t.n;}}}});
  if(cd){{li+=line('🚗',`${{T.li_car}} — ${{cd}} ${{T.days}}`,state.trip.filter(t=>t.c&&ISL[t.k].car).map(t=>iname(t.k)).join(' · '),csum,T.book_car,'https://www.discovercars.com/?a_aid=antaran2');tot+=csum;
    const fuel=cd*CFG.fuel_per_day;
    li+=line('⛽',T.li_fuel,`€${{CFG.fuel_per_day}}/${{LANG==='el'?'μέρα':'day'}} × ${{cd}} ${{T.days}}`,fuel,null);tot+=fuel;}}
  // boat days
  let bsum=0,boats=[];
  state.trip.forEach(t=>{{const b=ISL[t.k].boat;if(b&&t.b){{bsum+=b.pp*state.pax;boats.push(LANG==='el'?b.nel:b.n);}}}});
  if(boats.length){{li+=line('⛵',T.li_boat,boats.join(' · ')+' — '+T.boat_rec,bsum,null);tot+=bsum;}}
  // food
  let msum=0;
  state.trip.forEach(t=>{{msum+=mealDay(t.k)*state.pax*t.n;}});
  li+=line('🍴',T.li_food,`${{eur(Math.round(mealDay(first)))}} ${{T.food_s}}`,msum,null);
  tot+=msum;
  // non-EU extras
  if(state.nonEU){{
    const esim=state.pax*18;li+=line('📶',T.li_esim,`${{state.pax}}× ${{T.esim_s}}`,esim,T.book_esim,'https://www.airalo.com/greece-esim');tot+=esim;
    const ins=state.pax*(nightsTotal+1)*3;li+=line('🛡',T.li_insurance,`${{state.pax}}× ${{nightsTotal+1}} ${{T.ins_days}}`,ins,null);tot+=ins;}}

  document.getElementById('tc-summary').innerHTML=`
    <h2>${{T.estimate}}</h2>
    <div class="tc-ss">${{state.pax}} ${{T.li_pax}} · ${{nightsTotal}} ${{T.nights}} · ${{T.months[state.month]}} · ${{({{budget:T.tier_budget,mid:T.tier_mid,comfort:T.tier_comfort}})[state.tier]}}</div>
    ${{li}}
    <div class="tc-tot"><span class="t1">${{T.total}}</span><span class="amt">${{eur(rnd(tot))}}</span></div>
    <div class="tc-pp">${{eur(rnd(tot/state.pax))}} ${{T.pp}}</div>
    <div class="tc-ctas">
      <a class="tc-cta f" href="https://www.ferryhopper.com/${{LANG==='el'?'el/':'en/'}}" target="_blank" rel="noopener sponsored">${{T.cta_ferry}}</a>
      <a class="tc-cta c" href="https://www.discovercars.com/?a_aid=antaran2" target="_blank" rel="noopener sponsored">${{T.cta_car}}</a>
    </div>
    <div class="tc-assume">${{T.assume.replace('{{month}}',T.months[state.month])}}</div>
    <div class="tc-honest">${{T.honest}}</div>`;
  sync();
}}

// ---------------- events ----------------
document.getElementById('tc-presets').addEventListener('click',e=>{{const c=e.target.closest('.tc-preset');if(!c)return;
  document.querySelectorAll('#tc-presets .tc-preset').forEach(x=>x.classList.remove('on'));c.classList.add('on');
  state.trip=JSON.parse(JSON.stringify(PRESETS[c.dataset.p]));render();}});
document.getElementById('tc-months').addEventListener('click',e=>{{const c=e.target.closest('.tc-chip');if(c){{state.month=c.dataset.m;render();}}}});
document.getElementById('tc-tiers').addEventListener('click',e=>{{const c=e.target.closest('.tc-chip');if(c){{state.tier=c.dataset.t;render();}}}});
document.getElementById('tc-noneu').addEventListener('click',()=>{{state.nonEU=!state.nonEU;render();}});
document.getElementById('tc-pax-minus').addEventListener('click',()=>{{state.pax=Math.max(1,state.pax-1);render();}});
document.getElementById('tc-pax-plus').addEventListener('click',()=>{{state.pax=Math.min(8,state.pax+1);render();}});
document.getElementById('tc-route').addEventListener('click',e=>{{
  const el=e.target.closest('[data-a]');if(!el)return;const i=+el.dataset.i,t=state.trip[i];
  if(el.dataset.a==='n-')t.n=Math.max(1,t.n-1);
  else if(el.dataset.a==='n+')t.n=Math.min(14,t.n+1);
  else if(el.dataset.a==='car')t.c=!t.c;
  else if(el.dataset.a==='boat')t.b=!t.b;
  else if(el.dataset.a==='rm'){{if(state.trip.length>1)state.trip.splice(i,1);}}
  render();}});
document.getElementById('tc-quick').addEventListener('click',e=>{{const b=e.target.closest('[data-add]');
  if(b&&!state.trip.some(t=>t.k===b.dataset.add)){{state.trip.push({{k:b.dataset.add,n:3,c:false,b:false}});render();}}}});

// island search autocomplete
const sIn=document.getElementById('tc-search'),sUl=document.getElementById('tc-sug');
function norm(s){{return s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');}}
sIn.addEventListener('input',()=>{{
  const q=norm(sIn.value.trim());
  if(q.length<2){{sUl.style.display='none';return;}}
  const hits=Object.keys(ISL).filter(k=>!state.trip.some(t=>t.k===k))
    .filter(k=>norm(ISL[k].n).startsWith(q)||norm(ISL[k].nel).startsWith(q)||norm(ISL[k].n).includes(q)||norm(ISL[k].nel).includes(q))
    .sort((a,b)=>(norm(iname(a)).startsWith(q)?0:1)-(norm(iname(b)).startsWith(q)?0:1)).slice(0,7);
  sUl.innerHTML=hits.map(k=>`<div data-k="${{k}}">${{iname(k)}} <small style="color:var(--ink-4,#A0ADB8)">${{ISL[k].g}}</small></div>`).join('');
  sUl.style.display=hits.length?'block':'none';}});
sUl.addEventListener('click',e=>{{const d=e.target.closest('[data-k]');if(!d)return;
  state.trip.push({{k:d.dataset.k,n:3,c:false,b:false}});sIn.value='';sUl.style.display='none';render();}});
document.addEventListener('click',e=>{{if(!e.target.closest('.tc-add'))sUl.style.display='none';}});

render();
</script>
</body>
</html>
'''


def main():
    meta, data = build_dataset()
    for lang, path in (('en', ROOT / 'trip-cost'), ('el', ROOT / 'el' / 'trip-cost')):
        path.mkdir(parents=True, exist_ok=True)
        (path / 'index.html').write_text(render_page(lang, meta, data), encoding='utf-8')
    print(f'✓ Trip-cost pages built: /trip-cost/ + /el/trip-cost/ ({len(data)} islands)')


if __name__ == '__main__':
    sys.exit(main())
