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
STYLE_V = 62  # keep in sync with index.html

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
            'beach': f('beach') or 0, 'hist': f('hist') or 0, 'night': f('night') or 0,
            'access': f('access') or 0, 'total': f('total') or 0,
            'days': f('days', int) or 3,
        }
    return out


def thumb(url):
    """Hero URL -> small card thumbnail (replaces any existing Cloudinary transform)."""
    if not url:
        return ''
    if '/image/upload/' in url:
        return re.sub(r'/image/upload/(?:[a-zA-Z]+_[^/]+/)?',
                      '/image/upload/w_300,h_240,c_fill,g_auto,q_auto,f_auto/', url, count=1)
    return url  # non-Cloudinary (e.g. Wikimedia) — use as-is


def build_dataset():
    costs = json.loads((ROOT / 'costs.json').read_text(encoding='utf-8'))
    meta, cost_islands = costs['_meta'], costs['islands']
    heroes = json.loads((ROOT / 'hero-photos.json').read_text(encoding='utf-8'))
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
            'img': thumb(ij.get('hero_photo') or (heroes.get(key) or {}).get('url') or ''),
            'lat': g['lat'], 'lng': g['lng'],
            'g': g['group'], 'cn': g['car_need'], 'air': g['air'],
            'days': int(g.get('days') or 3),
            'room': c['room'], 'meal': c['meal_pp_mid'], 'car': c['car_day'],
            'boat': boat,
            'b': g['beach'], 'tot': g['total'],
        }
    return meta, data


# ---------------------------------------------------------------- strings

STR = {
    'en': {
        'lang': 'en', 'base': '/', 'other': '/el/trip-cost/', 'lang_label': 'EL',
        'title': 'Greek Island Budget Planner — ferries, rooms, car, food | Aegean Blueprint',
        'desc': 'Build your island route and get an honest cost estimate: ferry fares, room prices by month, car hire, food — for all 83 Greek islands. No fake precision.',
        'h1': 'What will your island trip cost?',
        'sub': 'Six quick questions and you get an honest estimate — ferry fares from real distances, room prices for your actual dates, no fake precision. Start with one island; add more if you are hopping.',
        'when_who': 'When & who', 'travellers': 'Travellers',
        's1': 'When do you leave?', 's1_s': 'exact start date — prices and ferry legs follow it',
        's2': 'How many of you?', 's3': 'What kind of trip?',
        's4': 'Where do you start?', 's4_s': 'pick your first island',
        's5': 'Add another island', 's5_s': 'ones that fit this route',
        's6': 'Extras', 's6_s': 'own car on the ferries, non-EU add-ons',
        'unsure': 'Not sure yet — pick a month',
        'arrive_q': 'How will you get there?',
        'near_none': 'Remove a stop to reach a different region.',
        'add_more': '⛴ Add another island', 'add_more_s': 'ferry legs and totals appear automatically',
        'which_island': 'Island', 'change_island': 'change',
        'row_nights': 'Nights', 'row_when': 'When',
        'advanced': 'More options', 'adv_s': 'arrival, vehicle, exact dates',
        'veh_default': 'Vehicle (applies to every island)',
        'fly_off': 'No airport on your first or last island — ferry only.',
        'one_hint': 'Pricing one island. Switch to island hopping to add ferry legs between stops.',
        'noneu': '🌍 Travelling from outside the EU', 'noneu_small': '(adds eSIM & insurance)',
        'step_when': '1 · When & who', 'step_how': '2 · Getting there & around', 'step_comfort': '3 · Comfort',
        'arrive_by': 'Arrive & leave by',
        'arr_ferry': '🛳 Ferry', 'arr_ferry_s': 'from the mainland ports',
        'arr_fly': '✈ Plane', 'arr_fly_s': 'where there’s an airport',
        'around': 'Getting around the islands',
        'veh_own': '🚙 My own car', 'veh_own_s': 'ferried from the mainland',
        'veh_rentcar': '🚗 Rent a car', 'veh_rentmoto': '🛵 Rent a scooter', 'veh_none2': '🚶 No vehicle',
        'li_carferry': 'Car on ferries', 'carferry_s': 'vehicle fee ×',
        'comfort': 'Comfort',
        'tier_budget': 'Budget', 'tier_budget_s': 'rooms & gyros',
        'tier_mid': 'Mid-range', 'tier_mid_s': 'nice room, taverna dinners',
        'tier_comfort': 'Comfort', 'tier_comfort_s': 'boutique, no counting',
        'months': {'apr': 'April', 'may': 'May', 'jun': 'June', 'jul': 'July', 'aug': 'August', 'sep': 'September', 'oct': 'October'},
        'add_island': 'Add an island:', 'add_ph': 'Choose an island…',
        'add_far': 'Islands far from this route are hidden — remove a stop to change region.',
        'empty_trip': 'Your route is empty — add an island below to start.',
        'departure': 'departure', 'back_to': 'back to', 'ferry_to': 'ferry to',
        'via_mainland': 'via mainland — no direct ferry likely', 'fly_hint': '✈ flying is often cheaper',
        'ionian_gate': 'nearest mainland port (drive or KTEL bus from Athens)',
        'nights': 'nights', 'night': 'night', 'car': '🚗 car', 'boat_day': '⛵ boat day',
        'rooms_per_night': 'rooms', 'per_night': '/night',
        'carless_note': 'No car on {n} (car-reliant) — we price a central room so you can walk to things (+{p}%).',
        'estimate': 'Your trip estimate',
        'li_ferries': 'Ferries', 'li_legs': 'legs', 'li_pax': 'pax', 'book_ferry': 'Book on Ferryhopper →',
        'from_port': 'from', 'ionian_gate_s': 'local mainland port',
        'li_rooms': 'Rooms', 'central': '(central)',
        'li_car': 'Car', 'days': 'days', 'book_car': 'Compare on Discover Cars →',
        'li_vehicle': 'Vehicle hire', 'li_flights': 'Domestic flights', 'total_fly': 'Total (excl. int’l flights)',
        'veh_none': 'On foot / bus', 'veh_moto': 'Scooter / ATV', 'veh_car': 'Car',
        'li_fuel': 'Fuel', 'li_boat': 'Boat days', 'boat_rec': 'our recommended trips',
        'li_food': 'Food & drink', 'food_s': 'pp/day', 'li_esim': 'eSIM — Greece data', 'esim_s': '10GB plan', 'book_esim': 'Get eSIM →',
        'li_insurance': 'Travel insurance', 'ins_days': 'days',
        'total': 'Total (excl. flights)', 'pp': 'per person',
        'cta_ferry': '🚢 Book ferries', 'cta_car': '🚗 Get the car',
        'assume': '<b>How we estimate:</b> economy ferry fares from real route distances · room prices for a decent double in {month} · one taverna meal + breakfast/snacks per day · car only where you toggled it. Museums, sunbeds and cocktails are yours.',
        'honest': 'Every figure is a typical price, not a quote — expect real prices roughly ±20% either side, set by ferry companies and hotels, not us. Book early for July–August; ferries sell out.',
        'guide': 'guide →',
        'remove': 'Remove',
        'exact_dates': '📅 Exact dates', 'dates_opt': 'optional — sharpens prices per month and fills in booking links',
        'book_room': 'book rooms →',
        'swaps_title': '💡 Smart swaps', 'swaps_sub': 'Same region, better value — based on this site\u2019s scores and your current settings.',
        'swap_save': 'save', 'swap_more': 'spend', 'swap_apply': 'Swap', 'swap_instead': 'instead of',
        'swap_overall': 'overall', 'swap_beach': 'beaches',
        'footer_privacy': 'Privacy', 'footer_mission': 'Mission', 'footer_lang': 'Ελληνικά',
        'nav': [('/#compare', 'Compare'), ('/#match', 'Match Me'), ('/trip-cost/', 'Budget', True),
                ('/#hopping', 'Ferries & Hopping'), ('/festivals/', 'Festivals'),
                ('/#data', 'Islands Data'), ('/#mission', 'Mission'), ('/#shortlist', '⭐ My Shortlist')],
    },
    'el': {
        'lang': 'el', 'base': '/el/', 'other': '/trip-cost/', 'lang_label': 'EN',
        'title': 'Μπάτζετ Ταξιδιού στα Ελληνικά Νησιά — πλοία, δωμάτια, αυτοκίνητο | Aegean Blueprint',
        'desc': 'Φτιάξε τη διαδρομή σου και δες μια ειλικρινή εκτίμηση κόστους: εισιτήρια πλοίων, δωμάτια ανά μήνα, ενοικίαση αυτοκινήτου, φαγητό — και για τα 88 νησιά.',
        'h1': 'Πόσο θα κοστίσει το ταξίδι σου στα νησιά;',
        'sub': 'Έξι γρήγορες ερωτήσεις και έχεις μια ειλικρινή εκτίμηση — ναύλα από πραγματικές αποστάσεις, τιμές δωματίων για τις δικές σου ημερομηνίες, χωρίς ψεύτικη ακρίβεια. Ξεκίνα με ένα νησί και πρόσθεσε κι άλλα αν κάνεις νησοπορία.',
        'when_who': 'Πότε & ποιοι', 'travellers': 'Ταξιδιώτες',
        's1': 'Πότε φεύγεις;', 's1_s': 'ακριβής ημερομηνία — οι τιμές και τα δρομολόγια την ακολουθούν',
        's2': 'Πόσοι είστε;', 's3': 'Τι είδους ταξίδι;',
        's4': 'Από πού ξεκινάς;', 's4_s': 'διάλεξε το πρώτο σου νησί',
        's5': 'Πρόσθεσε κι άλλο νησί', 's5_s': 'αυτά που ταιριάζουν στη διαδρομή',
        's6': 'Έξτρα', 's6_s': 'δικό σου αυτοκίνητο στα πλοία, επιλογές εκτός ΕΕ',
        'unsure': 'Δεν ξέρω ακόμα — διάλεξε μήνα',
        'arrive_q': 'Πώς θα πας;',
        'near_none': 'Αφαίρεσε στάση για να πας σε άλλη περιοχή.',
        'add_more': '⛴ Πρόσθεσε κι άλλο νησί', 'add_more_s': 'τα ακτοπλοϊκά και τα σύνολα εμφανίζονται αυτόματα',
        'which_island': 'Νησί', 'change_island': 'αλλαγή',
        'row_nights': 'Νύχτες', 'row_when': 'Πότε',
        'advanced': 'Περισσότερες επιλογές', 'adv_s': 'άφιξη, όχημα, ακριβείς ημερομηνίες',
        'veh_default': 'Όχημα (ισχύει για κάθε νησί)',
        'fly_off': 'Δεν υπάρχει αεροδρόμιο στο πρώτο ή στο τελευταίο νησί — μόνο πλοίο.',
        'one_hint': 'Υπολογισμός για ένα νησί. Άλλαξε σε νησοπορία για να προσθέσεις ακτοπλοϊκά μεταξύ στάσεων.',
        'noneu': '🌍 Ταξιδεύεις από χώρα εκτός ΕΕ', 'noneu_small': '(προσθέτει eSIM & ασφάλεια)',
        'step_when': '1 · Πότε & ποιοι', 'step_how': '2 · Μετάβαση & μετακίνηση', 'step_comfort': '3 · Άνεση',
        'arrive_by': 'Άφιξη & αναχώρηση με',
        'arr_ferry': '🛳 Πλοίο', 'arr_ferry_s': 'από τα λιμάνια της στεριάς',
        'arr_fly': '✈ Αεροπλάνο', 'arr_fly_s': 'όπου υπάρχει αεροδρόμιο',
        'around': 'Μετακίνηση στα νησιά',
        'veh_own': '🚙 Το αυτοκίνητό μου', 'veh_own_s': 'με το πλοίο από τη στεριά',
        'veh_rentcar': '🚗 Ενοικίαση αυτοκινήτου', 'veh_rentmoto': '🛵 Ενοικίαση μηχανακιού', 'veh_none2': '🚶 Χωρίς όχημα',
        'li_carferry': 'Αυτοκίνητο στα πλοία', 'carferry_s': 'ναύλος οχήματος ×',
        'comfort': 'Άνεση',
        'tier_budget': 'Οικονομικά', 'tier_budget_s': 'δωμάτια & γύρος',
        'tier_mid': 'Μεσαία', 'tier_mid_s': 'καλό δωμάτιο, ταβέρνες',
        'tier_comfort': 'Άνετα', 'tier_comfort_s': 'boutique, χωρίς μέτρημα',
        'months': {'apr': 'Απρίλιος', 'may': 'Μάιος', 'jun': 'Ιούνιος', 'jul': 'Ιούλιος', 'aug': 'Αύγουστος', 'sep': 'Σεπτέμβριος', 'oct': 'Οκτώβριος'},
        'add_island': 'Πρόσθεσε νησί:', 'add_ph': 'Διάλεξε νησί…',
        'add_far': 'Νησιά μακριά από τη διαδρομή σου κρύβονται — αφαίρεσε στάση για να αλλάξεις περιοχή.',
        'empty_trip': 'Η διαδρομή σου είναι άδεια — πρόσθεσε ένα νησί για να ξεκινήσεις.',
        'departure': 'αναχώρηση', 'back_to': 'επιστροφή', 'ferry_to': 'πλοίο προς',
        'via_mainland': 'μέσω στεριάς — μάλλον χωρίς απευθείας πλοίο', 'fly_hint': '✈ συχνά συμφέρει αεροπορικώς',
        'ionian_gate': 'κοντινότερο λιμάνι στεριάς (οδικώς / ΚΤΕΛ από Αθήνα)',
        'nights': 'νύχτες', 'night': 'νύχτα', 'car': '🚗 αυτοκίνητο', 'boat_day': '⛵ ημέρα σκάφους',
        'rooms_per_night': 'δωμάτια', 'per_night': '/νύχτα',
        'carless_note': 'Χωρίς αυτοκίνητο στη {n} (το χρειάζεται) — υπολογίζουμε κεντρικό δωμάτιο για να πηγαίνεις παντού με τα πόδια (+{p}%).',
        'estimate': 'Η εκτίμηση του ταξιδιού σου',
        'li_ferries': 'Πλοία', 'li_legs': 'διαδρομές', 'li_pax': 'άτομα', 'book_ferry': 'Κράτηση στο Ferryhopper →',
        'from_port': 'από', 'ionian_gate_s': 'τοπικό λιμάνι στεριάς',
        'li_rooms': 'Δωμάτια', 'central': '(κεντρικό)',
        'li_car': 'Αυτοκίνητο', 'days': 'μέρες', 'book_car': 'Σύγκριση στο Discover Cars →',
        'li_vehicle': 'Ενοικίαση οχήματος', 'li_flights': 'Πτήσεις εσωτερικού', 'total_fly': 'Σύνολο (χωρίς διεθνείς πτήσεις)',
        'veh_none': 'Πεζή / λεωφορείο', 'veh_moto': 'Μηχανάκι / ATV', 'veh_car': 'Αυτοκίνητο',
        'li_fuel': 'Καύσιμα', 'li_boat': 'Ημέρες σκάφους', 'boat_rec': 'οι προτεινόμενες εκδρομές μας',
        'li_food': 'Φαγητό & ποτό', 'food_s': 'ανά άτομο/μέρα', 'li_esim': 'eSIM — δεδομένα Ελλάδα', 'esim_s': 'πακέτο 10GB', 'book_esim': 'Πάρε eSIM →',
        'li_insurance': 'Ταξιδιωτική ασφάλεια', 'ins_days': 'μέρες',
        'total': 'Σύνολο (χωρίς αεροπορικά)', 'pp': 'ανά άτομο',
        'cta_ferry': '🚢 Κράτηση πλοίων', 'cta_car': '🚗 Κλείσε αυτοκίνητο',
        'assume': '<b>Πώς υπολογίζουμε:</b> οικονομικά ναύλα από πραγματικές αποστάσεις · τιμές για ένα καλό δίκλινο τον {month} · ένα γεύμα ταβέρνας + πρωινό/σνακ τη μέρα · αυτοκίνητο μόνο όπου το ενεργοποίησες. Μουσεία, ξαπλώστρες και κοκτέιλ δικά σου.',
        'honest': 'Κάθε ποσό είναι τυπική τιμή, όχι προσφορά — οι πραγματικές τιμές κινούνται περίπου ±20%, και τις ορίζουν ακτοπλοϊκές και ξενοδοχεία, όχι εμείς. Για Ιούλιο–Αύγουστο κλείσε νωρίς· τα πλοία εξαντλούνται.',
        'guide': 'οδηγός →',
        'remove': 'Αφαίρεση',
        'exact_dates': '📅 Ακριβείς ημερομηνίες', 'dates_opt': 'προαιρετικό — ακριβέστερες τιμές ανά μήνα και έτοιμοι σύνδεσμοι κράτησης',
        'book_room': 'κράτηση δωματίων →',
        'swaps_title': '💡 Έξυπνες εναλλαγές', 'swaps_sub': 'Ίδια περιοχή, καλύτερη σχέση — βάσει των βαθμολογιών του site και των επιλογών σου.',
        'swap_save': 'κερδίζεις', 'swap_more': 'επιπλέον', 'swap_apply': 'Αλλαγή', 'swap_instead': 'αντί για',
        'swap_overall': 'συνολικά', 'swap_beach': 'παραλίες',
        'footer_privacy': 'Απόρρητο', 'footer_mission': 'Στόχος', 'footer_lang': 'English',
        'nav': [('/el/#compare', 'Σύγκριση'), ('/el/#match', 'Βρες το Νησί σου'), ('/el/trip-cost/', 'Μπάτζετ', True),
                ('/el/#hopping', 'Πλοία & Νησοπορία'), ('/el/festivals/', 'Γιορτές'),
                ('/el/#data', 'Στοιχεία Νησιών'), ('/el/#mission', 'Στόχος'), ('/el/#shortlist', '⭐ Η Λίστα μου')],
    },
}



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
        'li_vehicle', 'li_flights', 'total_fly', 'veh_none', 'veh_moto', 'veh_car', 'add_far', 'from_port', 'ionian_gate_s',
        'li_carferry', 'carferry_s', 'li_legs', 'empty_trip',
        'assume', 'honest', 'guide', 'remove', 'book_room',
        'swaps_title', 'swaps_sub', 'swap_save', 'swap_more', 'swap_apply', 'swap_instead', 'swap_overall', 'swap_beach',
        'tier_budget', 'tier_mid', 'tier_comfort',
    )}
    js_t['months'] = t['months']

    schema = json.dumps({
        '@context': 'https://schema.org', '@type': 'WebApplication',
        'name': 'Greek Island Budget Planner' if not is_el else 'Μπάτζετ Ταξιδιού στα Ελληνικά Νησιά',
        'url': url, 'applicationCategory': 'TravelApplication',
        'operatingSystem': 'Web',
        'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'EUR'},
    }, ensure_ascii=False)

    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-FMFWLRM2J9"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-FMFWLRM2J9');</script>
<script>window.localStorage&&document.documentElement.classList.toggle("dark",localStorage.getItem("darkMode")===null?window.matchMedia("(prefers-color-scheme: dark)").matches:localStorage.getItem("darkMode")==="true")</script>
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
.tc-subl{{font-size:11px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:var(--ink-4,#A0ADB8);margin:0 0 8px}}
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
.tc-seg{{display:inline-flex;background:rgba(232,247,251,.9);border-radius:999px;padding:3px;gap:2px}}
.tc-seg button{{border:0;background:transparent;font-size:14px;padding:4px 10px;border-radius:999px;cursor:pointer;opacity:.55}}
.tc-seg button.on{{background:#fff;opacity:1;box-shadow:0 1px 4px rgba(26,35,50,.2)}}
.tc-swaps-box{{background:linear-gradient(180deg,rgba(7,104,128,.05),transparent);border:1px solid var(--line,#E4EBF0);border-radius:14px;padding:14px 16px;margin:14px 0}}
.tc-swap{{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:9px 0;border-top:1px dashed var(--line,#E4EBF0)}}
.tc-swap:first-of-type{{border-top:none}}
.tc-swap-t{{flex:1 1 150px;font-size:14px}}
.tc-swap-t small{{color:var(--ink-4,#A0ADB8);font-weight:600}}
.tc-swap-d{{font-size:13px;white-space:nowrap}}
.tc-swap-b{{border:1.5px solid #076880;background:transparent;color:#076880;font:inherit;font-size:13px;font-weight:700;padding:6px 12px;border-radius:9px;cursor:pointer}}
.tc-swap-b:hover{{background:#076880;color:#fff}}
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
/* --- Aug 2026: six-step flow --- */
.tc-step-c{{border:1.5px solid var(--line,#DFE6EC);border-radius:16px;background:var(--card,#fff);padding:16px 18px;margin:0 0 12px}}
.tc-step-c[hidden]{{display:none!important}}
.tc-step-c>h3,.tc-step-c>summary{{margin:0 0 12px;font-size:16px;font-weight:800;display:flex;align-items:center;gap:10px;flex-wrap:wrap;list-style:none;cursor:default}}
.tc-step-c>summary{{cursor:pointer;margin-bottom:0}}
.tc-step-c>summary::-webkit-details-marker{{display:none}}
.tc-step-c[open]>summary{{margin-bottom:12px}}
.tc-step-c>h3>i,.tc-step-c>summary>i{{font-style:normal;flex:none;width:24px;height:24px;border-radius:50%;background:#0B8FAC;color:#fff;font-size:13px;display:inline-flex;align-items:center;justify-content:center}}
.tc-step-c>h3>small,.tc-step-c>summary>small{{flex:1 1 100%;font-size:12.5px;font-weight:600;color:var(--ink-4,#A0ADB8);margin-left:34px}}
.tc-srow{{display:flex;gap:14px;align-items:center;flex-wrap:wrap}}
.tc-date{{font:inherit;font-size:15px;font-weight:700;padding:10px 12px;border:1.5px solid var(--line,#DFE6EC);border-radius:12px;background:var(--card,#fff);color:inherit}}
.tc-link{{font:inherit;font-size:13.5px;font-weight:700;color:#0B8FAC;background:none;border:0;cursor:pointer;text-decoration:underline;padding:0}}
.tc-f-isl{{position:relative;max-width:340px}}
.tc-f-isl .tc-search{{width:100%}}
#tc-isug,#tc-sug{{position:absolute;top:100%;left:0;right:0;z-index:30}}
.tc-note{{margin-top:8px;font-size:12.5px;color:var(--ink-4,#A0ADB8)}}
.tc-advbody{{padding:2px 0 4px}}
.tc-advrow{{display:flex;gap:22px;flex-wrap:wrap;align-items:center;margin-top:16px}}
</style>
<script async data-cfasync="false" data-noptimize="1" data-no-defer="1" src="https://emrldtp.com/NTUxOTU3.js?t=551957"></script>
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
      <!-- Six steps, revealed as you go. Aug 2026: the controls used to sit in
           four simultaneous blocks; now each answer opens the next question. -->
      <section class="tc-step-c" data-step="1">
        <h3><i>1</i>{t['s1']}<small>{t['s1_s']}</small></h3>
        <div class="tc-srow">
          <input type="date" id="tc-date" class="tc-date">
          <button class="tc-link" id="tc-unsure">{t['unsure']}</button>
        </div>
        <div class="tc-chips" id="tc-months" hidden>{months_html}</div>
      </section>

      <section class="tc-step-c" data-step="2" hidden>
        <h3><i>2</i>{t['s2']}</h3>
        <div class="tc-step"><button id="tc-pax-minus">−</button><span id="tc-pax">2</span><button id="tc-pax-plus">+</button></div>
      </section>

      <section class="tc-step-c" data-step="3" hidden>
        <h3><i>3</i>{t['s3']}</h3>
        <div class="tc-chips" id="tc-tiers">
          <span class="tc-chip" data-t="budget">{t['tier_budget']}<br><small>{t['tier_budget_s']}</small></span>
          <span class="tc-chip on" data-t="mid">{t['tier_mid']}<br><small>{t['tier_mid_s']}</small></span>
          <span class="tc-chip" data-t="comfort">{t['tier_comfort']}<br><small>{t['tier_comfort_s']}</small></span>
        </div>
      </section>

      <section class="tc-step-c" data-step="4" hidden>
        <h3><i>4</i>{t['s4']}<small>{t['s4_s']}</small></h3>
        <div class="tc-f tc-f-isl">
          <input class="tc-search" id="tc-island" placeholder="{t['add_ph']}" autocomplete="off">
          <div class="tc-sug" id="tc-isug"></div>
        </div>
        <div id="tc-arrwrap" hidden>
          <div class="tc-subl">{t['arrive_q']}</div>
          <div class="tc-chips" id="tc-arr">
            <span class="tc-chip on" data-arr="ferry">{t['arr_ferry']}<br><small>{t['arr_ferry_s']}</small></span>
            <span class="tc-chip" data-arr="fly">{t['arr_fly']}<br><small>{t['arr_fly_s']}</small></span>
          </div>
          <div class="tc-note" id="tc-flynote" hidden>{t['fly_off']}</div>
        </div>
      </section>

      <div id="tc-route"></div>

      <section class="tc-step-c" data-step="5" hidden>
        <h3><i>5</i>{t['s5']}<small>{t['s5_s']}</small></h3>
        <span id="tc-quick"></span>
        <div class="tc-f tc-f-isl" style="margin-top:10px">
          <input class="tc-search" id="tc-search" placeholder="{t['add_ph']}" autocomplete="off">
          <div class="tc-sug" id="tc-sug"></div>
        </div>
      </section>

      <div id="tc-swaps"></div>

      <details class="tc-adv tc-step-c" id="tc-adv" data-step="6" hidden>
        <summary><i>6</i>{t['s6']} <small>{t['s6_s']}</small></summary>
        <div class="tc-advbody">
          <div class="tc-subl">{t['veh_default']}</div>
          <div class="tc-chips" id="tc-veh">
            <span class="tc-chip" data-veh="own">{t['veh_own']}<br><small>{t['veh_own_s']}</small></span>
            <span class="tc-chip" data-veh="car">{t['veh_rentcar']}</span>
            <span class="tc-chip" data-veh="moto">{t['veh_rentmoto']}</span>
            <span class="tc-chip" data-veh="none">{t['veh_none2']}</span>
          </div>
          <div class="tc-advrow">
            <span class="tc-sw" id="tc-noneu"><span class="s"></span> {t['noneu']} <small style="font-weight:600;color:var(--ink-4,#A0ADB8)">{t['noneu_small']}</small></span>
          </div>
        </div>
      </details>
    </div>

    <div class="tc-sum" id="tc-summary"></div>
  </div>
</main>

<footer class="seo-footer" style="max-width:1120px;margin:0 auto;padding:20px 22px">
  <p>© 2026 Aegean Blueprint · <a href="{url_el if not is_el else url_en}">{t['footer_lang']}</a> · <a href="{'/el/privacy/' if is_el else '/privacy/'}">{t['footer_privacy']}</a></p>
</footer>

<script>
document.getElementById("menu-toggle-btn").addEventListener("click",function(){{var n=document.getElementById("main-nav");n.classList.toggle("open");this.classList.toggle("open");}});

// ---------------- data (generated by tools/build_trip_cost.py) ----------------
const LANG={json.dumps(lang)};
const T={json.dumps(js_t, ensure_ascii=False)};
const CFG={json.dumps({k: meta[k] for k in ('season_room', 'season_car', 'range_lo', 'range_hi', 'meal_budget', 'meal_comfort', 'carless_central_premium', 'fuel_per_day', 'moto_factor')})};
const ISL={json.dumps(data, ensure_ascii=False, separators=(',', ':'))};
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
// Explicit combination rules, then the generic group/distance rule.
const COMPAT_W={{kythira:['antikythera','elafonisos'],antikythera:['kythira','elafonisos'],elafonisos:['kythira','antikythera'],ammouliani:['thasos','samothrace']}};
function pairOK(a,b){{
  if(COMPAT_W[a]||COMPAT_W[b]){{
    if(COMPAT_W[a]&&!COMPAT_W[a].includes(b))return false;
    if(COMPAT_W[b]&&!COMPAT_W[b].includes(a))return false;
    return true; // whitelisted pairs are allowed regardless of distance
  }}
  const ga=ISL[a].g,gb=ISL[b].g;
  if((ga==='Saronic')!==(gb==='Saronic'))return false;              // Saronic only with Saronic
  const es=g=>g==='Sporades'||g==='Evia';
  if(es(ga)!==es(gb))return false;                                  // Evia+Sporades: closed cluster
  const sameGroup=ga===gb&&ga!=='Other';                            // 'Other' is not a real group
  return sameGroup||haversine(ISL[a],ISL[b])<=130;
}}
function nearTrip(k){{if(!state.trip.length)return true;return state.trip.every(t=>pairOK(t.k,k));}}
function flightFare(k){{const nm=haversine(GATES.Piraeus,ISL[k])/1.852;return Math.min(120,Math.max(55,Math.round(55+0.15*nm)));}}
const eur=n=>'€'+Math.round(n).toLocaleString(LANG==='el'?'el-GR':'en-GB');
const rnd=n=>n<100?Math.round(n/5)*5:Math.round(n/10)*10;
const mid=f=>(f[0]+f[1])/2;
// ---- exact dates (optional): per-island check-in/out derived from nights ----
const MKEYS=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'];
const isoD=d=>{{const p=n=>String(n).padStart(2,'0');return d.getFullYear()+'-'+p(d.getMonth()+1)+'-'+p(d.getDate());}};
const seas=(tbl,mk)=>tbl[mk]!==undefined?tbl[mk]:Math.min.apply(null,Object.values(tbl)); // off-season months price like the cheapest listed month
function tripStart(){{if(!state.date)return null;const d=new Date(state.date+'T12:00:00');return isNaN(d)?null:d;}}
function legDates(i){{const d0=tripStart();if(d0===null||!state.trip[i])return null;let off=0;for(let j=0;j<i;j++)off+=state.trip[j].n;
  const a=new Date(d0);a.setDate(a.getDate()+off);const b=new Date(a);b.setDate(b.getDate()+state.trip[i].n);return[a,b];}}
function monthAt(i){{const ld=legDates(i);return ld?MKEYS[ld[0].getMonth()]:state.month;}}
const fmtD=d=>d.toLocaleDateString(LANG==='el'?'el-GR':'en-GB',{{day:'numeric',month:'short'}});
function bookUrl(i){{const t=state.trip[i];let u='https://www.booking.com/searchresults.html?ss='+encodeURIComponent(ISL[t.k].n+', Greece')+'&group_adults='+state.pax+'&no_rooms=1&group_children=0';
  const ld=legDates(i);if(ld)u+='&checkin='+isoD(ld[0])+'&checkout='+isoD(ld[1]);return u;}}
// ---- smart swaps: on-island spend (rooms+food+vehicle) for a candidate at a stop ----
function stayCost(k,i,v){{const isl=ISL[k],n=state.trip[i].n,mk=monthAt(i);
  const rn=isl.room[state.tier]*seas(CFG.season_room,mk);
  const mult=(!state.own&&!v&&isl.cn>=4&&isl.car)?CFG.carless_central_premium:1;
  let c=rn*n*mult + mealDay(k)*state.pax*n;
  if(!state.own&&v&&isl.car){{c+=isl.car*seas(CFG.season_car,mk)*(v==='m'?(CFG.moto_factor||0.55):1)*n;
    c+=(v==='m'?Math.round(CFG.fuel_per_day*0.4):CFG.fuel_per_day)*n;}}
  return c;}}
function fitsExcept(i,k){{return state.trip.every((t,j)=>j===i||pairOK(t.k,k));}}

// ---------------- state ----------------
let state={{step:1,month:'jun',date:null,pax:2,tier:'mid',nonEU:false,fly:false,own:false,trip:[]}};
// URL params: ?i=milos:4:c:b,ios:3&m=aug&pax=2&tier=mid
(function(){{
  const q=new URLSearchParams(location.search);
  try{{const saved=localStorage.getItem('tc-state');if(saved&&!q.get('i')){{state=JSON.parse(saved);}}}}catch(e){{}}
  if(q.get('i')){{
    const trip=q.get('i').split(',').map(s=>{{const p=s.split(':');
      return ISL[p[0]]?{{k:p[0],n:Math.min(14,Math.max(1,parseInt(p[1])||3)),v:p.includes('c')?'c':(p.includes('m')?'m':''),b:p.includes('b')}}:null;}}).filter(Boolean);
    if(trip.length){{state.trip=trip;state.step=6;}}
  }}
  if(q.get('m')&&CFG.season_room[q.get('m')])state.month=q.get('m');
  if(q.get('pax'))state.pax=Math.min(8,Math.max(1,parseInt(q.get('pax'))||2));
  if(['budget','mid','comfort'].includes(q.get('tier')))state.tier=q.get('tier');
  if(state.date&&!/^\d{{4}}-\d{{2}}-\d{{2}}$/.test(state.date))state.date=null;
  if(/^\d{{4}}-\d{{2}}-\d{{2}}$/.test(q.get('d')||''))state.date=q.get('d');
  {{const ts=tripStart();if(!ts||ts<new Date(Date.now()-864e5))state.date=null;
   else{{const mk=MKEYS[ts.getMonth()];if(CFG.season_room[mk])state.month=mk;}}}}
  if(!CFG.season_room[state.month])state.month='jun';
  state.trip=(state.trip||[]).filter(t=>ISL[t.k]);
  if(q.get('fly')==='1')state.fly=true;
  if(q.get('veh')==='own'){{state.own=true;state.fly=false;}}
  state.fly=!!state.fly;state.own=!!state.own;if(state.own)state.fly=false;
  state.trip.forEach(t=>{{if(t.v===undefined)t.v=t.c?'c':'';delete t.c;}});
}})();
function sync(){{
  try{{localStorage.setItem('tc-state',JSON.stringify(state));}}catch(e){{}}
  const i=state.trip.map(t=>t.k+':'+t.n+(t.v?':'+t.v:'')+(t.b?':b':'')).join(',');
  history.replaceState(null,'','?i='+i+'&m='+state.month+'&pax='+state.pax+'&tier='+state.tier+(state.fly?'&fly=1':'')+(state.own?'&veh=own':'')+(state.date?'&d='+state.date:''));
}}

// per-tier room price for an island in the selected month
function roomNight(k,i){{return ISL[k].room[state.tier]*seas(CFG.season_room,i===undefined?state.month:monthAt(i));}}
function mealDay(k){{const m=ISL[k].meal;return state.tier==='budget'?m*CFG.meal_budget:state.tier==='comfort'?m*CFG.meal_comfort:m;}}

// ---------------- render ----------------
function render(){{
  document.getElementById('tc-pax').textContent=state.pax;
  if(typeof syncSteps==='function')syncSteps();
  const _di=document.getElementById('tc-date');if(_di&&_di.value!==(state.date||''))_di.value=state.date||'';
  document.querySelectorAll('#tc-months .tc-chip').forEach(c=>c.classList.toggle('on',c.dataset.m===state.month));
  document.querySelectorAll('#tc-tiers .tc-chip').forEach(c=>c.classList.toggle('on',c.dataset.t===state.tier));
  document.getElementById('tc-noneu').classList.toggle('on',state.nonEU);
  const allV=v=>state.trip.every(t=>!ISL[t.k].car||t.v===v)&&state.trip.some(t=>ISL[t.k].car);
  document.querySelectorAll('#tc-arr .tc-chip').forEach(c=>c.classList.toggle('on',(c.dataset.arr==='fly')===state.fly));
  document.querySelectorAll('#tc-veh .tc-chip').forEach(c=>{{const v=c.dataset.veh;
    c.classList.toggle('on', v==='own'?state.own : (!state.own&&(v==='car'?allV('c'):v==='moto'?allV('m'):allV(''))));}});

  const sR=CFG.season_room[state.month],sC=CFG.season_car[state.month];
  let h='';
  if(!state.trip.length){{
    document.getElementById('tc-route').innerHTML=`<div class="tc-leg" style="padding:18px 4px;font-size:14px">${{T.empty_trip}}</div>`;
    document.getElementById('tc-quick').innerHTML=['santorini','milos','naxos']
      .map(k=>`<button class="tc-addbtn" data-add="${{k}}">+ ${{iname(k)}}</button>`).join(' ');
    document.getElementById('tc-summary').innerHTML=`<h2>${{T.estimate}}</h2><div class="tc-ss">${{T.empty_trip}}</div>`;
    sync();return;
  }}
  const first=state.trip[0].k,last=state.trip[state.trip.length-1].k;
  const flyIn=state.fly&&!state.own&&ISL[first].air,flyOut=state.fly&&!state.own&&ISL[last].air;
  const flyChip=document.querySelector('#tc-arr [data-arr="fly"]');
  if(flyChip)flyChip.style.opacity=(state.own||!(ISL[first].air||ISL[last].air))?'0.45':'1';
  if(flyIn){{
    h+=`<div class="tc-leg"><span class="l">✈</span> ${{GATES.Piraeus[LANG].replace(/\s*\(.*\)/,'')}} (ATH) — ${{T.departure}}<span class="fp">€${{rnd(flightFare(first))}} pp</span></div>`;
  }}else{{
    const dep=legInfo('M',first);
    h+=`<div class="tc-leg"><span class="l">🛳</span> ${{dep.label||''}} — ${{T.departure}} ${{(dep.fly&&!state.own)?'<span class="hint">'+T.fly_hint+'</span>':''}}<span class="fp">€${{rnd(mid(dep.f))}} pp</span></div>`;
  }}
  state.trip.forEach((t,i)=>{{
    const isl=ISL[t.k],rn=roomNight(t.k,i),ld=legDates(i);
    const guide=(LANG==='el'?'/el':'')+'/island/'+t.k+'/';
    h+=`<div class="tc-card">
      ${{isl.img?`<img src="${{isl.img}}" alt="${{iname(t.k)}}" loading="lazy">`:''}}
      <div class="tc-cb">
        <div class="tc-cn">${{iname(t.k)}}<a href="${{guide}}">${{T.guide}}</a></div>
        <div class="tc-cs">${{T.rooms_per_night}} ${{eur(rnd(rn))}}${{T.per_night}} · ${{ld?fmtD(ld[0])+' – '+fmtD(ld[1]):T.months[state.month]}} · <a href="${{bookUrl(i)}}" target="_blank" rel="noopener sponsored" style="color:#076880;font-weight:700;text-decoration:none">${{T.book_room}}</a></div>
        <div class="tc-cc">
          <span class="tc-n"><button data-a="n-" data-i="${{i}}">−</button> ${{t.n}} ${{t.n===1?T.night:T.nights}} <button data-a="n+" data-i="${{i}}">+</button></span>
          ${{(isl.car&&!state.own)?`<span class="tc-seg"><button class="${{!t.v?'on':''}}" data-a="veh" data-v="" data-i="${{i}}" title="${{T.veh_none}}">🚶</button><button class="${{t.v==='m'?'on':''}}" data-a="veh" data-v="m" data-i="${{i}}" title="${{T.veh_moto}}">🛵</button><button class="${{t.v==='c'?'on':''}}" data-a="veh" data-v="c" data-i="${{i}}" title="${{T.veh_car}}">🚗</button></span>`:''}}
          ${{isl.boat?`<span class="tc-sw ${{t.b?'on':''}}" data-a="boat" data-i="${{i}}"><span class="s"></span> ${{T.boat_day}} <small>€${{isl.boat.pp}} pp</small></span>`:''}}
        </div>
        ${{(!state.own&&!t.v&&isl.cn>=4&&isl.car)?`<div class="tc-warn">${{T.carless_note.replace('{{n}}',iname(t.k)).replace('{{p}}',Math.round((CFG.carless_central_premium-1)*100))}}</div>`:''}}
      </div>
      <button class="tc-x" data-a="rm" data-i="${{i}}" title="${{T.remove}}">✕</button>
    </div>`;
    const next=state.trip[i+1];
    if(next){{const li=legInfo(t.k,next.k);
      h+=`<div class="tc-leg"><span class="l">⛴</span> ${{T.ferry_to}} ${{iname(next.k)}}${{li.label?' <small>('+li.label+')</small>':''}} ${{(li.fly&&!state.own)?'<span class="hint">'+T.fly_hint+'</span>':''}}<span class="fp">€${{rnd(mid(li.f))}} pp</span></div>`;}}
  }});
  if(flyOut){{
    h+=`<div class="tc-leg"><span class="l">✈</span> ${{T.back_to}} ${{GATES.Piraeus[LANG].replace(/\s*\(.*\)/,'')}} (ATH)<span class="fp">€${{rnd(flightFare(last))}} pp</span></div>`;
  }}else{{
    const ret=legInfo(last,'M');
    h+=`<div class="tc-leg"><span class="l">🛳</span> ${{T.back_to}} ${{ret.label||''}}<span class="fp">€${{rnd(mid(ret.f))}} pp</span></div>`;
  }}
  document.getElementById('tc-route').innerHTML=h;
  renderSwaps();

  // quick-add buttons
  const inTrip=k=>state.trip.some(t=>t.k===k);
  const quickKeys=state.trip.length
    ?Object.keys(ISL).filter(k=>!inTrip(k)&&nearTrip(k))
      .sort((a,b)=>Math.min(...state.trip.map(t=>haversine(ISL[t.k],ISL[a])))-Math.min(...state.trip.map(t=>haversine(ISL[t.k],ISL[b])))).slice(0,3)
    :['santorini','milos','naxos'];
  document.getElementById('tc-quick').innerHTML=quickKeys
    .map(k=>`<button class="tc-addbtn" data-add="${{k}}">+ ${{iname(k)}}</button>`).join(' ');

  // ---------------- totals (single typical figures) ----------------
  const nightsTotal=state.trip.reduce((a,t)=>a+t.n,0);
  let tot=0,li='';
  const line=(ic,lbl,small,amt,book,url)=>`<div class="tc-li"><span>${{ic}}</span><span class="lbl">${{lbl}}<small>${{small}}</small></span><span class="amt">${{eur(rnd(amt))}}</span>${{book?`<a class="bk" href="${{url}}" target="_blank" rel="noopener sponsored">${{book}}</a>`:''}}</div>`;
  // ferries
  let fsum=0;const legs=[...(flyIn?[]:[['M',first]]),...state.trip.slice(0,-1).map((t,i)=>[t.k,state.trip[i+1].k]),...(flyOut?[]:[[last,'M']])];
  legs.forEach(([a,b])=>{{fsum+=mid(legInfo(a,b).f)*state.pax;}});
  if(legs.length){{
    const portOf=k=>{{const g=gateOf(k);return g?g[LANG]:T.ionian_gate_s;}};
    const ports=[...new Set(legs.filter(([a,b])=>a==='M'||b==='M').map(([a,b])=>portOf(a==='M'?b:a)))];
    const portsTxt=ports.length?`${{T.from_port}} ${{ports.join(' & ')}} · `:'';
    li+=line('⛴',T.li_ferries,`${{portsTxt}}${{legs.length}} ${{T.li_legs}} × ${{state.pax}} ${{T.li_pax}}`,fsum,T.book_ferry,'https://www.ferryhopper.com/'+(LANG==='el'?'el/':'en/'));tot+=fsum;}}
  if(flyIn||flyOut){{const fl=((flyIn?flightFare(first):0)+(flyOut?flightFare(last):0))*state.pax;
    li+=line('✈',T.li_flights,`${{(flyIn?1:0)+(flyOut?1:0)}} × ${{state.pax}} ${{T.li_pax}}`,fl,null);tot+=fl;}}
  // rooms
  let rsum=0;
  state.trip.forEach((t,i)=>{{const rn=roomNight(t.k,i);
    const mult=(!state.own&&!t.v&&ISL[t.k].cn>=4&&ISL[t.k].car)?CFG.carless_central_premium:1;
    rsum+=rn*t.n*mult;}});
  li+=line('🛏',`${{T.li_rooms}} — ${{nightsTotal}} ${{T.nights}}`,state.trip.map(t=>`${{iname(t.k)}} ${{t.n}}${{(!state.own&&!t.v&&ISL[t.k].cn>=4&&ISL[t.k].car)?' '+T.central:''}}`).join(' · '),rsum,state.trip.length===1?T.book_room:null,state.trip.length===1?bookUrl(0):null);
  tot+=rsum;
  // car + fuel
  if(state.own){{
    // Your own car rides every ferry leg. Vehicle fee ≈ 2.3× the passenger fare,
    // clamped to real-world car-deck pricing (short hop ≥ €25, long haul ≤ €130).
    const carLegs=[['M',first],...state.trip.slice(0,-1).map((t,i)=>[t.k,state.trip[i+1].k]),[last,'M']];
    const carFee=f=>Math.min(130,Math.max(25,mid(f)*2.3));
    const cfSum=carLegs.reduce((a,[x,y])=>a+carFee(legInfo(x,y).f),0);
    li+=line('🚙',T.li_carferry,`${{T.carferry_s}} ${{carLegs.length}} ${{T.li_legs}}`,cfSum,null);tot+=cfSum;
    const fuel=nightsTotal*CFG.fuel_per_day;
    li+=line('⛽',T.li_fuel,`€${{CFG.fuel_per_day}}/${{LANG==='el'?'μέρα':'day'}} × ${{nightsTotal}} ${{T.days}}`,fuel,null);tot+=fuel;
  }}else{{
  let csum=0,cd=0,fuelSum=0;
  state.trip.forEach((t,i)=>{{if(t.v&&ISL[t.k].car){{csum+=ISL[t.k].car*seas(CFG.season_car,monthAt(i))*(t.v==='m'?(CFG.moto_factor||0.55):1)*t.n;cd+=t.n;
    fuelSum+=(t.v==='m'?Math.round(CFG.fuel_per_day*0.4):CFG.fuel_per_day)*t.n;}}}});
  if(cd){{li+=line('🚗',`${{T.li_vehicle}} — ${{cd}} ${{T.days}}`,state.trip.filter(t=>t.v&&ISL[t.k].car).map(t=>iname(t.k)+' '+(t.v==='m'?'🛵':'🚗')).join(' · '),csum,T.book_car,'https://www.discovercars.com/?a_aid=antaran2');tot+=csum;
    li+=line('⛽',T.li_fuel,`🚗 €${{CFG.fuel_per_day}} · 🛵 €${{Math.round(CFG.fuel_per_day*0.4)}} /${{LANG==='el'?'μέρα':'day'}}`,fuelSum,null);tot+=fuelSum;}}
  }}
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
    const esim=state.pax*18;li+=line('📶',T.li_esim,`${{state.pax}}× ${{T.esim_s}}`,esim,T.book_esim,'https://yesim.tpx.lt/Sax2vWmP');tot+=esim;
    const ins=state.pax*(nightsTotal+1)*3;li+=line('🛡',T.li_insurance,`${{state.pax}}× ${{nightsTotal+1}} ${{T.ins_days}}`,ins,null);tot+=ins;}}

  const _ts=tripStart();let whenTxt=T.months[state.month];
  if(_ts){{const _e=new Date(_ts);_e.setDate(_e.getDate()+nightsTotal);whenTxt=fmtD(_ts)+' – '+fmtD(_e);}}
  document.getElementById('tc-summary').innerHTML=`
    <h2>${{T.estimate}}</h2>
    <div class="tc-ss">${{state.pax}} ${{T.li_pax}} · ${{nightsTotal}} ${{T.nights}} · ${{whenTxt}} · ${{({{budget:T.tier_budget,mid:T.tier_mid,comfort:T.tier_comfort}})[state.tier]}}</div>
    ${{li}}
    <div class="tc-tot"><span class="t1">${{state.fly?T.total_fly:T.total}}</span><span class="amt">${{eur(rnd(tot))}}</span></div>
    <div class="tc-pp">${{eur(rnd(tot/state.pax))}} ${{T.pp}}</div>
    <div class="tc-ctas">
      <a class="tc-cta f" href="https://www.ferryhopper.com/${{LANG==='el'?'el/':'en/'}}" target="_blank" rel="noopener sponsored">${{T.cta_ferry}}</a>
      <a class="tc-cta c" href="https://www.discovercars.com/?a_aid=antaran2" target="_blank" rel="noopener sponsored">${{T.cta_car}}</a>
    </div>
    <div class="tc-assume">${{T.assume.replace('{{month}}',T.months[state.month])}}</div>
    <div class="tc-honest">${{T.honest}}</div>`;
  sync();
}}

function renderSwaps(){{
  const box=document.getElementById('tc-swaps');if(!box)return;
  if(!state.trip.length){{box.innerHTML='';return;}}
  const inTrip=k=>state.trip.some(t=>t.k===k);
  const byStop={{}};
  state.trip.forEach((cur,i)=>{{
    if(i===0)return; // first island is the user's anchor choice — never suggest swapping it
    const v0=cur.v,curStay=stayCost(cur.k,i,v0),curTot=ISL[cur.k].tot,curB=ISL[cur.k].b;
    let save=null,up=null;
    Object.keys(ISL).forEach(k=>{{
      if(inTrip(k)||!fitsExcept(i,k))return;
      const v=(v0&&ISL[k].car)?v0:'';
      const dM=Math.round(stayCost(k,i,v)-curStay),dT=+(ISL[k].tot-curTot).toFixed(1),dB=+(ISL[k].b-curB).toFixed(1);
      if(dM<=-60&&dT>=-0.4){{if(!save||dM<save.dM)save={{i,k,dM,dT,dB,kind:'save',score:-dM}};}}
      if(dT>=0.2&&dM<=150){{if(!up||dT>up.dT||(dT===up.dT&&dM<up.dM))up={{i,k,dM,dT,dB,kind:'up',score:dT*250-Math.max(0,dM)}};}}
    }});
    const best=[save,up].filter(Boolean).sort((a,b)=>b.score-a.score)[0];
    if(best)byStop[i]=best;
  }});
  const sug=Object.values(byStop).sort((a,b)=>b.score-a.score).slice(0,3);
  if(!sug.length){{box.innerHTML='';return;}}
  const chips=sug.map(s=>{{
    const money=s.dM<0
      ?`<b style="color:#2E7D32">${{T.swap_save}} ${{eur(Math.abs(s.dM))}}</b>`
      :`<b style="color:#B26A00">+${{eur(s.dM)}}</b>`;
    const parts=[money];
    if(Math.abs(s.dT)>=0.1)parts.push(`⭐ ${{T.swap_overall}} ${{s.dT>0?'+':''}}${{s.dT.toFixed(1)}}`);
    if(Math.abs(s.dB)>=0.3)parts.push(`🏖 ${{T.swap_beach}} ${{s.dB>0?'+':''}}${{s.dB.toFixed(1)}}`);
    return `<div class="tc-swap">
      <span class="tc-swap-t"><b>${{iname(s.k)}}</b> <small>${{T.swap_instead}} ${{iname(state.trip[s.i].k)}}</small></span>
      <span class="tc-swap-d">${{parts.join(' · ')}}</span>
      <button class="tc-swap-b" data-swap="${{s.i}}:${{s.k}}">${{T.swap_apply}} ⇄</button>
    </div>`;
  }}).join('');
  box.innerHTML=`<div class="tc-ctrl tc-swaps-box">
    <h3 style="margin-bottom:2px">${{T.swaps_title}}</h3>
    <div style="font-size:12.5px;color:var(--ink-4,#A0ADB8);margin-bottom:10px">${{T.swaps_sub}}</div>
    ${{chips}}</div>`;
}}

// ---------------- events ----------------
document.getElementById('tc-months').addEventListener('click',e=>{{const c=e.target.closest('.tc-chip');if(c){{state.month=c.dataset.m;state.date=null;openStep(4);render();}}}});
document.getElementById('tc-date').addEventListener('change',e=>{{const v=e.target.value;
  state.date=/^\d{{4}}-\d{{2}}-\d{{2}}$/.test(v)?v:null;
  if(state.date)openStep(4);
  const ts=tripStart();if(ts){{const mk=MKEYS[ts.getMonth()];if(CFG.season_room[mk])state.month=mk;}}
  render();}});
document.getElementById('tc-tiers').addEventListener('click',e=>{{const c=e.target.closest('.tc-chip');if(c){{state.tier=c.dataset.t;render();}}}});
document.getElementById('tc-noneu').addEventListener('click',()=>{{state.nonEU=!state.nonEU;render();}});
document.getElementById('tc-arr').addEventListener('click',e=>{{const c=e.target.closest('.tc-chip');if(!c)return;
  if(c.dataset.arr==='fly'){{if(state.own)return;state.fly=true;}}else state.fly=false;render();}});
document.getElementById('tc-veh').addEventListener('click',e=>{{const c=e.target.closest('.tc-chip');if(!c)return;
  const v=c.dataset.veh;
  if(v==='own'){{state.own=!state.own;if(state.own)state.fly=false;}}
  else{{state.own=false;state.trip.forEach(t=>{{if(ISL[t.k].car)t.v=(v==='car'?'c':v==='moto'?'m':'');}});}}
  render();}});
document.getElementById('tc-pax-minus').addEventListener('click',()=>{{state.pax=Math.max(1,state.pax-1);render();}});
document.getElementById('tc-pax-plus').addEventListener('click',()=>{{state.pax=Math.min(8,state.pax+1);render();}});
document.getElementById('tc-route').addEventListener('click',e=>{{
  const el=e.target.closest('[data-a]');if(!el)return;const i=+el.dataset.i,t=state.trip[i];
  if(el.dataset.a==='n-')t.n=Math.max(1,t.n-1);
  else if(el.dataset.a==='n+')t.n=Math.min(14,t.n+1);
  else if(el.dataset.a==='veh')t.v=el.dataset.v;
  else if(el.dataset.a==='boat')t.b=!t.b;
  else if(el.dataset.a==='rm')state.trip.splice(i,1);
  render();}});
document.getElementById('tc-quick').addEventListener('click',e=>{{const b=e.target.closest('[data-add]');
  if(b&&!state.trip.some(t=>t.k===b.dataset.add)){{state.trip.push({{k:b.dataset.add,n:3,v:'',b:false}});render();}}}});
document.getElementById('tc-swaps').addEventListener('click',e=>{{const b=e.target.closest('[data-swap]');if(!b)return;
  const [i,k]=b.dataset.swap.split(':');const s=state.trip[+i];if(!s||state.trip.some(x=>x.k===k))return;
  s.k=k;if(!ISL[k].car)s.v='';render();}});

// island search autocomplete
const sIn=document.getElementById('tc-search'),sUl=document.getElementById('tc-sug');
function norm(s){{return s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');}}
function distTo(k){{return state.trip.length?Math.min(...state.trip.map(t=>haversine(ISL[t.k],ISL[k]))):0;}}
function renderSug(){{
  const q=norm(sIn.value.trim());
  const pool=Object.keys(ISL).filter(k=>!state.trip.some(t=>t.k===k));
  const raw=q?pool.filter(k=>norm(ISL[k].n).includes(q)||norm(ISL[k].nel).includes(q)):pool;
  let hits=raw.filter(nearTrip);
  hits=q
    ?hits.sort((a,b)=>((norm(iname(a)).startsWith(q)?0:1)-(norm(iname(b)).startsWith(q)?0:1))||distTo(a)-distTo(b))
    :hits.sort((a,b)=>distTo(a)-distTo(b)||iname(a).localeCompare(iname(b), LANG));
  let html=hits.map(k=>`<div data-k="${{k}}">${{iname(k)}} <small style="color:var(--ink-4,#A0ADB8)">${{ISL[k].g}}</small></div>`).join('');
  if(raw.length&&!hits.length)html=`<div style="cursor:default;color:var(--ink-4,#A0ADB8);font-weight:600;font-size:12px">${{T.add_far}}</div>`;
  sUl.innerHTML=html;
  sUl.style.display=html?'block':'none';
}}
sIn.addEventListener('input',renderSug);
sIn.addEventListener('focus',renderSug);
sUl.addEventListener('click',e=>{{const d=e.target.closest('[data-k]');if(!d)return;
  state.trip.push({{k:d.dataset.k,n:3,v:'',b:false}});sIn.value='';sUl.style.display='none';render();}});
document.addEventListener('click',e=>{{if(!e.target.closest('.tc-add'))sUl.style.display='none';}});

// ---------------- six-step flow ----------------
// Each answer opens the next question. Steps never re-hide once opened, so
// going back to change something is always possible.
function openStep(n){{
  if(n>state.step)state.step=Math.min(6,n);
  syncSteps();
}}
function syncSteps(){{
  if(!state.trip.length&&state.step>4)state.step=4;
  if(state.trip.length&&state.step<6)state.step=6;
  const mc=document.getElementById('tc-months');
  if(mc&&!state.date&&state.step>1)mc.hidden=false;
  document.querySelectorAll('.tc-step-c').forEach(el=>{{
    el.hidden = (+el.dataset.step) > state.step;
  }});
  const aw=document.getElementById('tc-arrwrap');
  if(aw)aw.hidden=!state.trip.length;
  const isl=document.getElementById('tc-island');
  if(isl&&document.activeElement!==isl)isl.value=state.trip[0]?iname(state.trip[0].k):'';
  const note=document.getElementById('tc-flynote');
  if(note){{
    const f=state.trip[0],l=state.trip[state.trip.length-1];
    const noAir=!state.trip.length||(!ISL[f.k].air&&!ISL[l.k].air);
    note.hidden=!(noAir&&!state.own);
  }}
}}
document.getElementById('tc-unsure').addEventListener('click',()=>{{
  document.getElementById('tc-months').hidden=false;
  document.getElementById('tc-date').value='';state.date=null;openStep(4);render();}});

// island picker — sets or replaces the first stop
const iIn=document.getElementById('tc-island'),iUl=document.getElementById('tc-isug');
function renderISug(){{
  const q=iIn.value.trim().toLowerCase();
  const keys=Object.keys(ISL).filter(k=>iname(k).toLowerCase().includes(q)).slice(0,8);
  iUl.innerHTML=keys.map(k=>`<div data-k="${{k}}">${{iname(k)}}</div>`).join('');
  iUl.style.display=keys.length?'block':'none';
}}
iIn.addEventListener('input',renderISug);
iIn.addEventListener('focus',()=>{{iIn.select();renderISug();}});
iUl.addEventListener('click',e=>{{const d=e.target.closest('[data-k]');if(!d)return;
  const k=d.dataset.k;
  // Default nights come from the island's own suggested stay.
  const n=state.trip[0]?state.trip[0].n:(ISL[k].days||3);
  state.trip[0]={{k:k,n:n,v:'',b:false}};
  iUl.style.display='none';iIn.blur();openStep(5);render();}});
document.addEventListener('click',e=>{{if(!e.target.closest('#tc-island,#tc-isug'))iUl.style.display='none';}});

syncSteps();
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
