#!/usr/bin/env python3
"""Build one standalone itinerary page per island.

  /island/<key>/itinerary/          (EN)
  /el/island/<key>/programma/       (EL)

Why: 'milos itinerary 4 days', 'corfu itinerary 5 days', 'naxos itinerary
4 days' sit at positions 4-8 in Search Console and land on the island page,
where the plan is the fourth section down. This page answers that query in
its own title, first sentence and heading structure. Nothing new is written:
days, stops, times, photos, drives, overnight bases and eat & drink all come
from islands/<key>.json. The lede and the three planning questions are
generated from the data, with hand overrides in tools/itinerary_overrides.json.

The island page keeps its itinerary section (linked from here as 'Full
guide'); beaches, when-to-visit and getting-there stay there too, so the two
URLs do not compete. Runs AFTER prerender.py (needs ISLAND_META and the
cost hints) and updates sitemap.xml idempotently.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))

import prerender as PR                                                   # noqa: E402
from build_festival_extras import (SITE_URL, page_head, header_nav,      # noqa: E402
                                   FOOTER, esc)
from build_compare_pages import fit_description                          # noqa: E402

YEAR = date.today().year
TODAY = date.today().isoformat()
OVERRIDES = {}
_ov = ROOT / 'tools' / 'itinerary_overrides.json'
if _ov.exists():
    OVERRIDES = json.loads(_ov.read_text(encoding='utf-8'))

# CARTO tiles, same key script.js uses (kept in one place there).
_js = (ROOT / 'script.js').read_text(encoding='utf-8')
_m = re.search(r"const CARTO_KEY = '([^']*)'", _js)
CARTO_KEY = _m.group(1) if _m else ''
TILE = 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png' + (f'?key={CARTO_KEY}' if CARTO_KEY else '')

MONTH_ABBR_EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
MONTH_ABBR_EL = ['Ιαν', 'Φεβ', 'Μάρ', 'Απρ', 'Μάι', 'Ιούν', 'Ιούλ', 'Αύγ', 'Σεπ', 'Οκτ', 'Νοέ', 'Δεκ']
CAR_EN = ['', 'No car needed', 'Car helpful', 'Car useful', 'Car recommended', 'Car essential']
CAR_EL = ['', 'Χωρίς αυτοκίνητο', 'Αυτοκίνητο βοηθά', 'Αυτοκίνητο χρήσιμο', 'Αυτοκίνητο συνιστάται', 'Αυτοκίνητο απαραίτητο']
DAY_COLORS = ['#0B8FAC', '#E8522A', '#3D8B6F', '#B08A55', '#7B5EA7', '#C6421F', '#1C7FA0']


def L(lang, en, el):
    return el if lang == 'el' else en


def pick(o, f, lang):
    return PR.pick(o, f, lang) or ''


def beach_id(key, name):
    return re.sub(r'[^a-z0-9]', '_', f'{key}_{name}', flags=re.I).lower()


def thumb(url, w=256, h=172):
    if not url or 'cloudinary.com' not in url or '/upload/' not in url:
        return url
    return url.replace('/upload/', f'/upload/w_{w},h_{h},c_fill,g_auto,q_auto,f_auto/', 1)


def el_at(data):
    """«στη Μήλο», «στην Αμμουλιανή», «στον Πόρο», «στους Παξούς»."""
    name = data.get('name_accusative_el') or data.get('name_el') or data['name']
    g = data.get('gender_el') or 'f'
    art = {'m': 'στον', 'n': 'στο', 'plm': 'στους', 'plf': 'στις', 'pln': 'στα'}.get(g)
    if art:
        return f'{art} {name}'
    import unicodedata
    first = unicodedata.normalize('NFD', name)[:1].lower()
    return ('στην ' if first in 'αεηιουωκπτξψ' else 'στη ') + name


def el_gen(data):
    """«της Μήλου», «του Πόρου», «των Παξών»."""
    gen = data.get('name_genitive_el') or data.get('name_el') or data['name']
    g = data.get('gender_el') or 'f'
    art = {'m': 'του', 'n': 'του', 'plm': 'των', 'plf': 'των', 'pln': 'των'}.get(g, 'της')
    return f'{art} {gen}'


def best_months(data, lang):
    ms = (data.get('when_to_visit') or {}).get('months') or []
    best = [i for i, m in enumerate(ms) if m.get('tag') == 'perfect'] or [i for i, m in enumerate(ms) if m.get('tag') == 'great']
    if not best:
        return ''
    ab = MONTH_ABBR_EL if lang == 'el' else MONTH_ABBR_EN
    # collapse runs: [4,5,8] -> "May–Jun, Sep"
    runs, start, prev = [], best[0], best[0]
    for i in best[1:] + [None]:
        if i is not None and i == prev + 1:
            prev = i
            continue
        runs.append(ab[start] if start == prev else f'{ab[start]}–{ab[prev]}')
        if i is not None:
            start = prev = i
    return ', '.join(runs)


def bases(days, lang):
    seen = []
    for d in days:
        o = pick(d, 'overnight', lang)
        if o and o not in seen:
            seen.append(o)
    return seen


def beach_stops(data):
    """Stops that are beaches in this island's beach list -> (stop name, beach id)."""
    names = {(b.get('name') or '').lower(): b for b in (data.get('beaches') or []) if b.get('name')}
    out, seen = [], set()
    for d in (data.get('itinerary') or {}).get('days') or []:
        for s in d.get('stops') or []:
            sn = (s.get('name') or '').lower()
            hit = None
            for bn, b in names.items():
                core = bn.replace(' beach', '').replace(' bay', '')
                if core and (core in sn):
                    hit = b
                    break
            if hit and hit['name'] not in seen:
                seen.add(hit['name'])
                out.append(hit)
    return out


# ------------------------------------------------------------------ text
def lede_text(key, data, meta, lang, days, base_list):
    ov = (OVERRIDES.get(key) or {}).get('lede_el' if lang == 'el' else 'lede')
    if ov:
        return ov
    n = len(days)
    name = data.get('name_el') if lang == 'el' else data['name']
    cn = int(round(meta.get('car_need') or 3))
    if lang == 'el':
        base = f' Βάση: {" και ".join(base_list[:2])}.' if base_list else ''
        car = (' Το πρόγραμμα προϋποθέτει αυτοκίνητο από την πρώτη μέρα.' if cn >= 4
               else ' Γίνεται χωρίς αυτοκίνητο.' if cn <= 2 else '')
        return (f'{n} {"μέρα" if n == 1 else "μέρες"} {el_at(data)}, μέρα με τη μέρα: τι βλέπεις, με τι σειρά, πόσο οδηγείς '
                f'και πού κοιμάσαι.{base}{car}')
    base = f' Base: {" and ".join(base_list[:2])}.' if base_list else ''
    car = (' It assumes a hire car from day one.' if cn >= 4 else ' It works without a car.' if cn <= 2 else '')
    return (f'{name} in {n} {"day" if n == 1 else "days"}, day by day: what to see, in what order, how far you drive '
            f'and where you sleep.{base}{car}')


def faq_items(key, data, meta, lang, days, base_list):
    ov = (OVERRIDES.get(key) or {}).get('faq_el' if lang == 'el' else 'faq')
    if ov:
        return ov
    n = len(days)
    name = data.get('name_el') if lang == 'el' else data['name']
    cn = int(round(meta.get('car_need') or 3))
    out = []
    if lang == 'el':
        out.append((f'Φτάνουν {n} μέρες {el_at(data)};',
                    f'Ναι, για πρώτη επίσκεψη. Το πρόγραμμα καλύπτει τα βασικά με ρυθμό που αφήνει χρόνο για θάλασσα. '
                    f'Με μία μέρα παραπάνω, πρόσθεσε μια ήσυχη μέρα σε παραλία χωρίς μετακινήσεις.'))
        out.append((f'Χρειάζομαι αυτοκίνητο {el_at(data)};',
                    ('Ναι. Οι παραλίες και τα χωριά είναι απλωμένα και το λεωφορείο δεν φτάνει παντού· κλείσε από πριν τον Ιούλιο και τον Αύγουστο.' if cn >= 4
                     else 'Βοηθά για μία-δύο μέρες, αλλά το βασικό πρόγραμμα βγαίνει με λεωφορείο, ταξί και βάρκες.' if cn == 3
                     else 'Όχι. Το πρόγραμμα γίνεται με τα πόδια, βάρκες και το τοπικό λεωφορείο.')))
        out.append((f'Πού να μείνω {el_at(data)};',
                    (f'Το πρόγραμμα κοιμάται σε {"·".join([" "]).join(base_list)}.' if len(base_list) == 1 else
                     f'Το πρόγραμμα κοιμάται σε {", ".join(base_list[:-1])} και {base_list[-1]}, για να μη διασχίζεις το νησί κάθε πρωί.' if base_list
                     else 'Διάλεξε βάση κοντά στο λιμάνι για την πρώτη και την τελευταία νύχτα.')))
    else:
        out.append((f'Is {n} {"day" if n == 1 else "days"} enough for {name}?',
                    f'Yes, for a first visit. The plan covers the essentials at a pace that leaves time in the water. '
                    f'With one more day, add a slow beach day with no driving.'))
        out.append((f'Do I need a car on {name}?',
                    ('Yes. The beaches and villages are spread out and the bus does not reach the ones that matter; book ahead for July and August.' if cn >= 4
                     else 'It helps for a day or two, but the core of this plan works with the bus, taxis and boats.' if cn == 3
                     else 'No. This plan works on foot, by boat and with the local bus.')))
        out.append((f'Where should I stay on {name}?',
                    (f'The plan sleeps in {base_list[0]}.' if len(base_list) == 1 else
                     f'The plan sleeps in {", ".join(base_list[:-1])} and {base_list[-1]}, so you are not crossing the island every morning.' if base_list
                     else 'Pick a base near the port for the first and last night.')))
    return [{'q': q, 'a': a} for q, a in out]


# ------------------------------------------------------------------ page
def render(key, data, meta, lang):
    it = data.get('itinerary') or {}
    days = it.get('days') or []
    if not days:
        return None
    n = len(days)
    name = data.get('name_el') if lang == 'el' else data['name']
    en_path = f'/island/{key}/itinerary/'
    el_path = f'/el/island/{key}/programma/'
    guide = f'/el/island/{key}/' if lang == 'el' else f'/island/{key}/'
    is_el = lang == 'el'

    if is_el:
        title = (f'{name}: Πρόγραμμα μιας Ημέρας ({YEAR})' if n == 1
                 else f'{name}: Πρόγραμμα {n} Ημερών, Μέρα με τη Μέρα ({YEAR})')
        h1 = f'{name} σε μία Μέρα' if n == 1 else f'{name} σε {n} Μέρες'
    else:
        title = (f'{name} in a Day: The Itinerary ({YEAR})' if n == 1
                 else f'{name} Itinerary: {n} Days, Day by Day ({YEAR})')
        h1 = f'{name} in a Day' if n == 1 else f'{name} in {n} Days'
    sub = pick(it, 'subtitle', lang)
    desc = fit_description((sub + ' ' if sub else '') + L(lang,
        'Day-by-day plan with times, drives, where to sleep and the beaches on the way.',
        'Πρόγραμμα μέρα με τη μέρα, με ώρες, διαδρομές, πού κοιμάσαι και τις παραλίες στον δρόμο.'))

    base_list = bases(days, lang)
    hero_url, hero_credit = PR.find_hero_image(data)
    cn = int(round(meta.get('car_need') or 3))
    pills = (data.get('getting_there') or {}).get('pills_el' if is_el else 'pills') or []
    months = best_months(data, lang)
    beaches = data.get('beaches') or []
    bstops = beach_stops(data)
    hint = PR.cost_hint(key, meta)
    cost_href = f"{'/el' if is_el else ''}/trip-cost/?i={key}%3A{n}"
    cost_label = (f"💶 ≈ €{PR._fmt_eur(hint['total'], lang)} {L(lang, 'for 2', 'για 2')} →" if hint
                  else L(lang, f'💶 Cost for {n} days', f'💶 Κόστος για {n} μέρες'))
    total_km = sum(int(d.get('km') or 0) for d in days)

    chips = [f'🗓 {n} {L(lang, "day" if n == 1 else "days", "μέρα" if n == 1 else "μέρες")}' + (f' · {n - 1} {L(lang, "night" if n == 2 else "nights", "νύχτα" if n == 2 else "νύχτες")}' if n > 1 else '')]
    if cn:
        chips.append('🚗 ' + (CAR_EL if is_el else CAR_EN)[min(5, max(1, cn))])
    if base_list:
        chips.append(f'🛏 {L(lang, "Base", "Βάση")}: {" · ".join(base_list[:2])}')
    chips += pills[:2]
    if months:
        chips.append(f'📅 {L(lang, "Best", "Καλύτερα")} {months}')
    chips_html = ''.join(f'<span class="it-chip">{esc(c)}</span>' for c in chips)
    if beaches:
        chips_html += f'<a class="it-chip it-chip-go" href="{guide}#sec-beaches">🏖 {len(beaches)} {L(lang, "beaches, ranked", "παραλίες, με κατάταξη")} →</a>'

    # sticky bar
    bar = ''.join(f'<a href="#day-{d["day"]}">{L(lang, "Day", "Μέρα")} {d["day"]}</a>' for d in days)
    bar += f'<span class="it-sp"></span>'
    if beaches:
        bar += f'<a class="it-link" href="{guide}#sec-beaches">🏖 {L(lang, "Beaches", "Παραλίες")}</a>'
    bar += f'<a class="it-link" href="{guide}">📖 {L(lang, "Full guide", "Πλήρης οδηγός")}</a>'
    bar += f'<a class="it-cta" href="{cost_href}">{esc(cost_label)}</a>'

    # beaches-on-this-plan strip
    strip = ''
    if bstops:
        links = ' · '.join(f'<a href="{guide}#{beach_id(key, b["name"])}">{esc(pick(b, "name", lang))}</a>' for b in bstops)
        strip = (f'<div class="it-bstrip"><b>🏖 {L(lang, "Beaches on this plan", "Παραλίες σε αυτό το πρόγραμμα")}:</b> {links} '
                 f'<span>— {L(lang, "each links to its card with the wind rule and today’s conditions.", "κάθε μία οδηγεί στην κάρτα της, με τον κανόνα ανέμου και τις σημερινές συνθήκες.")} '
                 f'<a href="{guide}#sec-beaches">{L(lang, f"All {len(beaches)}, ranked", f"Και οι {len(beaches)}, με κατάταξη")} →</a></span></div>')

    # days
    bnames = {(b.get('name') or '').lower().replace(' beach', '').replace(' bay', ''): b for b in beaches if b.get('name')}
    day_html = []
    for i, d in enumerate(days):
        color = d.get('color') or DAY_COLORS[i % len(DAY_COLORS)]
        km, mins = d.get('km'), d.get('drive_mins')
        meta_bits = []
        if km:
            meta_bits.append(f'{km} km' + (f' · {mins} min' if mins else ''))
        ov = pick(d, 'overnight', lang)
        sleep = f'<span class="it-sleep">🌙 {L(lang, "Sleep", "Ύπνος")}: {esc(ov)}</span>' if ov else ''
        stops = []
        for s in d.get('stops') or []:
            sname = pick(s, 'name', lang)
            sn = (s.get('name') or '').lower()
            b = next((bb for core, bb in bnames.items() if core and core in sn), None)
            chip = (f' <a class="it-bchip" href="{guide}#{beach_id(key, b["name"])}">🏖 {L(lang, "beach card · wind &amp; conditions", "κάρτα παραλίας · άνεμος &amp; συνθήκες")} →</a>' if b else '')
            link = f'<a href="{esc(s["wiki"])}" target="_blank" rel="noopener">{esc(sname)}</a>' if s.get('wiki') else esc(sname)
            photo = (f'<img src="{esc(thumb(s["photo"]))}" alt="{esc(sname)}" loading="lazy" width="128" height="86">' if s.get('photo') else '<span class="it-nophoto"></span>')
            stops.append(f'<div class="it-stop"><div class="it-t">{esc(s.get("time") or "")}</div>'
                         f'<div><h3>{link}{chip}</h3><p>{PR.safe_html(pick(s, "desc", lang))}</p></div>{photo}</div>')
        food = ''
        _food = d.get('food') or []
        for f in (_food if isinstance(_food, list) else [_food]):
            if not isinstance(f, dict):
                continue
            meal = pick(f, 'meal', lang); area = pick(f, 'area', lang)
            food += f'<div class="it-food"><b>🍽 {esc(meal)}{" · " + esc(area) if area else ""}</b> {PR.safe_html(pick(f, "desc", lang))}</div>'
        nl = pick(d, 'nightlife', lang)
        if nl:
            food += f'<div class="it-food"><b>🌙 {L(lang, "Evening", "Βράδυ")}</b> {PR.safe_html(nl)}</div>'
        day_html.append(
            f'<section class="it-day" id="day-{d["day"]}" style="--c:{esc(color)}">'
            f'<div class="it-dh"><span class="it-n">{L(lang, "DAY", "ΜΕΡΑ")} {d["day"]}</span><h2>{esc(pick(d, "title", lang))}</h2>'
            f'<span class="it-meta">{" · ".join(meta_bits)}{" " if meta_bits and sleep else ""}{sleep}</span></div>'
            + ''.join(stops) + (f'<div class="it-foodwrap">{food}</div>' if food else '') + '</section>')

    faqs = faq_items(key, data, meta, lang, days, base_list)
    faq_html = ''.join(f'<details{" open" if i == 0 else ""}><summary>{esc(f["q"])}</summary><p>{PR.safe_html(f["a"])}</p></details>' for i, f in enumerate(faqs))

    # sidebar links
    side_links = [(f'{guide}#sec-beaches', L(lang, f'Top beaches of {name}', f'Παραλίες {el_gen(data)}')) if beaches else None,
                  (f'{guide}#sec-when', L(lang, 'Best time to visit', 'Πότε να πας')),
                  (f'{guide}#sec-getting', L(lang, 'Getting there', 'Πώς πας')),
                  (guide, L(lang, f'Full {name} guide', f'Πλήρης οδηγός {el_gen(data)}'))]
    side_links = ''.join(f'<a href="{h}">{esc(t)} →</a>' for h, t in side_links if h)

    # map data
    pts = [{'d': d['day'], 'c': d.get('color') or DAY_COLORS[i % len(DAY_COLORS)],
            'p': [[s['lat'], s['lng'], pick(s, 'name', lang)] for s in d.get('stops') or [] if s.get('lat') and s.get('lng')]}
           for i, d in enumerate(days)]

    lede = lede_text(key, data, meta, lang, days, base_list)

    # JSON-LD
    canonical = SITE_URL + (el_path if is_el else en_path)
    trip = {"@context": "https://schema.org", "@type": "TouristTrip", "name": h1, "description": desc, "url": canonical,
            "inLanguage": "el" if is_el else "en",
            "touristType": ["Beach lovers", "Island hoppers"],
            "itinerary": {"@type": "ItemList", "numberOfItems": sum(len(d.get('stops') or []) for d in days),
                          "itemListElement": [{"@type": "ListItem", "position": pos + 1,
                                               "item": {"@type": "TouristAttraction", "name": pick(s, 'name', lang),
                                                        **({"geo": {"@type": "GeoCoordinates", "latitude": s['lat'], "longitude": s['lng']}} if s.get('lat') else {})}}
                                              for pos, s in enumerate([s for d in days for s in (d.get('stops') or [])])]},
            "isPartOf": {"@type": "TouristDestination", "name": name, "url": SITE_URL + guide}}
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": f['q'], "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', f['a'])}} for f in faqs]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": L(lang, 'Home', 'Αρχική'), "item": SITE_URL + ('/el/' if is_el else '/')},
        {"@type": "ListItem", "position": 2, "name": name, "item": SITE_URL + guide},
        {"@type": "ListItem", "position": 3, "name": h1, "item": canonical}]}
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (trip, faq_ld, crumbs))

    head = page_head(title, desc, en_path, el_path, lang)
    head = head.replace(f'<meta property="og:image" content="{SITE_URL}/og-image.png">', f'<meta property="og:image" content="{esc(hero_url or SITE_URL + "/og-image.png")}">', 1)
    head = head.replace('</head>', ld + CSS + '</head>')
    body = header_nav(lang, el_path if not is_el else en_path, active='')

    footer = (FOOTER.replace('{lang_link}', en_path if is_el else el_path)
              .replace('{lang_label}', 'English' if is_el else 'Ελληνικά')
              .replace('{privacy}', '/el/privacy/' if is_el else '/privacy/')
              .replace('{privacy_label}', 'Απόρρητο' if is_el else 'Privacy')
              .replace('{credits}', '/el/credits/' if is_el else '/credits/')
              .replace('{credits_label}', 'Πηγές φωτογραφιών' if is_el else 'Photo credits'))

    main = f'''
<main class="it-page">
<div class="it-crumb"><a href="{'/el/' if is_el else '/'}">{L(lang, 'Home', 'Αρχική')}</a> › <a href="{guide}">{esc(name)}</a> › <b>{esc(h1)}</b></div>
<div class="it-hero"{f' style="background-image:url({esc(hero_url)})"' if hero_url else ''}><div class="it-scrim"></div><div class="it-hbody">
  <div class="it-eyebrow">{esc((PR.GROUP_NAMES_EL.get(meta.get('group'), meta.get('group')) if is_el else meta.get('group')) or '')} · {L(lang, 'Day-by-day plan', 'Πρόγραμμα μέρα με τη μέρα')}</div>
  <h1>{esc(h1)}</h1>
  {f'<p class="it-sub">{esc(sub)}</p>' if sub else ''}
  <div class="it-facts">{chips_html}</div>
</div></div>
<nav class="it-bar" id="it-bar">{bar}</nav>
<div class="it-grid"><div>
<p class="it-lede">{PR.safe_html(lede)}</p>
{strip}
{''.join(day_html)}
<section class="it-faq"><h2>{L(lang, 'Planning questions', 'Πρακτικές ερωτήσεις')}</h2>{faq_html}</section>
<p class="it-back"><a href="{guide}">← {L(lang, f'Back to the full {name} guide', f'Πίσω στον πλήρη οδηγό {el_gen(data)}')}</a></p>
</div>
<aside class="it-side">
  <div class="it-card"><h4>{L(lang, 'Route map', 'Χάρτης διαδρομής')}</h4><div id="it-map" class="it-map"></div><small>{n} {L(lang, 'days', 'μέρες')}{f' · ~{total_km} km' if total_km else ''}</small></div>
  <div class="it-card it-btns"><a class="it-btn f" href="https://www.ferryhopper.com/{'el/' if is_el else 'en/'}" target="_blank" rel="noopener sponsored">🚢 {L(lang, 'Book ferry tickets', 'Κράτηση πλοίου')}</a><a class="it-btn c" href="https://www.discovercars.com/?a_aid=antaran2" target="_blank" rel="noopener sponsored">🚗 {L(lang, 'Rent a car', 'Ενοικίαση αυτοκινήτου')}</a><a class="it-btn k" href="javascript:window.print()">🖨 {L(lang, 'Print this plan', 'Εκτύπωση')}</a>
  <p class="aff-note"><a href="{'/el/privacy/#affiliate' if is_el else '/privacy/#affiliate'}">{L(lang, 'Affiliate links — they support this guide and cost you nothing.', 'Affiliate σύνδεσμοι — στηρίζουν αυτόν τον οδηγό χωρίς κόστος για εσένα.')}</a></p></div>
  <div class="it-card"><h4>{L(lang, f'From the {name} guide', f'Από τον οδηγό {el_gen(data)}')}</h4><div class="it-links">{side_links}</div></div>
</aside></div>
</main>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
(function(){{
  var D={json.dumps(pts, ensure_ascii=False)};
  var el=document.getElementById('it-map'); if(!el||!window.L) return;
  var map=L.map(el,{{scrollWheelZoom:false,attributionControl:false}});
  L.tileLayer({json.dumps(TILE)},{{subdomains:'abcd',maxZoom:18}}).addTo(map);
  var all=[];
  D.forEach(function(d){{var ll=d.p.map(function(p){{return [p[0],p[1]];}}); all=all.concat(ll);
    if(ll.length>1) L.polyline(ll,{{color:d.c,weight:3,opacity:.85,dashArray:'6 5'}}).addTo(map);
    d.p.forEach(function(p,i){{L.circleMarker([p[0],p[1]],{{radius:6,color:'#fff',weight:2,fillColor:d.c,fillOpacity:1}}).addTo(map).bindTooltip('D'+d.d+'.'+(i+1)+' '+p[2]);}});}});
  if(all.length) map.fitBounds(all,{{padding:[18,18]}});
  var bar=document.getElementById('it-bar'), links=[].slice.call(bar.querySelectorAll('a[href^="#day-"]'));
  var secs=links.map(function(a){{return document.querySelector(a.getAttribute('href'));}});
  function mark(){{var y=window.scrollY+140, cur=0; secs.forEach(function(s,i){{if(s&&s.offsetTop<=y) cur=i;}}); links.forEach(function(a,i){{a.classList.toggle('on',i===cur);}});}}
  window.addEventListener('scroll',mark,{{passive:true}}); mark();
}})();
</script>
'''
    return head + body + main + footer + '</body></html>'


CSS = '''<style>
.it-page{max-width:1060px;margin:0 auto;padding:18px 16px 60px}
.it-crumb{font-size:12.5px;color:var(--ink-3);margin-bottom:10px}.it-crumb a{color:var(--aegean-dark);text-decoration:none}.it-crumb b{color:var(--ink)}
.it-hero{position:relative;border-radius:18px;overflow:hidden;min-height:250px;background:#3a4b5c center/cover;box-shadow:var(--shadow)}
.it-scrim{position:absolute;inset:0;background:linear-gradient(to top,rgba(8,16,26,.86),rgba(8,16,26,.22) 60%,rgba(8,16,26,.05))}
.it-hbody{position:relative;padding:120px 26px 22px;color:#fff}
.it-eyebrow{font-size:11px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:#C8EEF5}
.it-hero h1{font-family:var(--display,var(--serif));font-size:38px;margin:4px 0 6px;line-height:1.1;color:#fff}
.it-sub{font-size:15.5px;color:rgba(255,255,255,.9);margin:0;max-width:60ch}
.it-facts{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.it-chip{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.3);border-radius:999px;padding:5px 11px;font-size:12.5px;font-weight:700;color:#fff;backdrop-filter:blur(3px);text-decoration:none}
.it-chip-go{background:#fff;color:var(--aegean-dark);border-color:#fff}
.it-bar{position:sticky;top:0;z-index:5;background:var(--white);border:1px solid var(--border);border-radius:12px;margin:14px 0 18px;padding:8px 10px;display:flex;gap:6px;align-items:center;overflow-x:auto;box-shadow:var(--shadow-sm);scrollbar-width:none}
.it-bar a{flex:0 0 auto;padding:7px 13px;border-radius:999px;font-size:13.5px;font-weight:700;color:var(--ink-3);text-decoration:none;border:1px solid transparent;white-space:nowrap}
.it-bar a.on{background:var(--aegean-pale);color:var(--aegean-dark);border-color:var(--aegean)}
.it-bar .it-sp{flex:1}.it-bar a.it-link{color:var(--aegean-dark);border-color:var(--aegean-light);background:var(--white)}
.it-bar a.it-cta{background:var(--terracotta);color:#fff;font-weight:800}
.it-grid{display:grid;grid-template-columns:1fr 300px;gap:22px;align-items:start}
@media(max-width:820px){.it-grid{grid-template-columns:1fr}.it-hero h1{font-size:30px}.it-hbody{padding-top:90px}}
.it-lede{font-size:15.5px;line-height:1.65;color:var(--ink-2);margin:0 0 16px}
.it-bstrip{background:var(--olive-pale);border:1px solid #cfe8dd;border-radius:12px;padding:10px 14px;font-size:13.5px;line-height:1.6;margin:0 0 16px;color:var(--ink-2)}
.it-bstrip a{color:var(--aegean-dark);font-weight:700;text-decoration:none}.it-bstrip span{color:var(--ink-3)}
.it-day{background:var(--white);border:1px solid var(--border);border-radius:14px;margin-bottom:16px;overflow:hidden;scroll-margin-top:70px}
.it-dh{display:flex;align-items:center;gap:12px;padding:12px 16px;border-left:4px solid var(--c);background:var(--marble);flex-wrap:wrap}
.it-n{font-family:var(--serif);font-weight:800;color:var(--c);font-size:13px;letter-spacing:.5px}
.it-dh h2{font-family:var(--serif);font-size:18px;margin:0;font-weight:800;color:var(--ink)}
.it-meta{margin-left:auto;font-size:12.5px;color:var(--ink-3);display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.it-sleep{font-size:12px;font-weight:700;color:var(--aegean-dark);background:var(--aegean-pale);border:1px solid var(--aegean-light);border-radius:999px;padding:3px 9px}
.it-stop{display:grid;grid-template-columns:52px 1fr 128px;gap:12px;padding:12px 16px;border-top:1px solid var(--border);align-items:start}
.it-t{font-size:12px;font-weight:800;color:var(--ink-4);padding-top:2px}
.it-stop h3{font-family:var(--serif);font-size:15px;margin:0 0 3px;font-weight:800;color:var(--ink)}
.it-stop h3 a{color:inherit;text-decoration:underline;text-decoration-color:rgba(0,0,0,.18);text-underline-offset:2px}
.it-stop p{margin:0;font-size:13.5px;line-height:1.55;color:var(--ink-3)}
.it-stop img{width:128px;height:86px;object-fit:cover;border-radius:8px;background:var(--marble-2);display:block}
.it-nophoto{width:128px;height:0;display:block}
.it-bchip{display:inline-block;margin-left:6px;font-size:11.5px;font-weight:700;color:var(--olive);background:var(--olive-pale);border:1px solid #cfe8dd;border-radius:999px;padding:2px 8px;text-decoration:none!important;vertical-align:1px}
.it-foodwrap{border-top:1px solid var(--border);padding:10px 16px 12px;background:var(--marble)}
.it-food{font-size:13.5px;line-height:1.6;color:var(--ink-3);margin:4px 0}.it-food b{color:var(--ink-2)}
.it-side{position:sticky;top:64px;display:flex;flex-direction:column;gap:12px}
@media(max-width:820px){.it-side{position:static}}
.it-card{background:var(--white);border:1px solid var(--border);border-radius:14px;padding:14px 16px}
.it-card h4{font-size:11px;letter-spacing:.7px;text-transform:uppercase;color:var(--ink-4);margin:0 0 8px;font-weight:800}
.it-card small{display:block;margin-top:6px;font-size:11.5px;color:var(--ink-3)}
.it-map{height:220px;border-radius:10px;background:#dfeef3}
.it-btns{display:flex;flex-direction:column;gap:8px}
.it-btn{display:block;text-align:center;padding:10px;border-radius:999px;font-weight:800;font-size:13.5px;text-decoration:none;color:#fff}
.it-btn.f{background:var(--terracotta)}.it-btn.c{background:var(--aegean)}.it-btn.k{background:var(--aegean-dark)}
.it-btns .aff-note{margin:4px 0 0;font-size:11px;text-align:center;color:var(--ink-4)}.it-btns .aff-note a{color:inherit}
.it-links a{display:block;font-size:13.5px;color:var(--aegean-dark);text-decoration:none;padding:6px 0;border-top:1px solid var(--border)}.it-links a:first-child{border-top:0}
.it-faq{margin-top:24px}.it-faq h2{font-family:var(--serif);font-size:19px;margin:0 0 10px;color:var(--ink)}
.it-faq details{background:var(--white);border:1px solid var(--border);border-radius:10px;padding:10px 14px;margin-bottom:8px}
.it-faq summary{font-weight:700;cursor:pointer;font-size:14.5px;color:var(--ink)}.it-faq p{margin:8px 0 0;font-size:13.5px;color:var(--ink-3);line-height:1.6}
.it-back{margin-top:18px;font-size:14px}.it-back a{color:var(--aegean-dark);font-weight:700;text-decoration:none}
@media print{.it-bar,.it-side,.it-btns,header,.seo-footer{display:none!important}.it-grid{display:block}.it-day{break-inside:avoid}.it-hero{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
</style>'''


def update_sitemap(keys):
    p = ROOT / 'sitemap.xml'
    xml = p.read_text(encoding='utf-8')
    START, END = '<!-- BEGIN AUTO-GENERATED ITINERARY PAGES -->', '<!-- END AUTO-GENERATED ITINERARY PAGES -->'
    rows = []
    for k in sorted(keys):
        en, el = f'/island/{k}/itinerary/', f'/el/island/{k}/programma/'
        for path in (en, el):
            rows.append(f'  <url><loc>{SITE_URL}{path}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority>'
                        f'<xhtml:link rel="alternate" hreflang="en" href="{SITE_URL}{en}"/>'
                        f'<xhtml:link rel="alternate" hreflang="el" href="{SITE_URL}{el}"/>'
                        f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE_URL}{en}"/></url>')
    block = START + '\n' + '\n'.join(rows) + '\n  ' + END
    if START in xml:
        xml = re.sub(re.escape(START) + r'.*?' + re.escape(END), block, xml, count=1, flags=re.DOTALL)
    else:
        xml = xml.replace('</urlset>', '  ' + block + '\n</urlset>')
    p.write_text(xml, encoding='utf-8')
    return len(rows)


def main():
    n = 0
    keys = []
    for jf in sorted((ROOT / 'islands').glob('*.json')):
        key = jf.stem
        if key == 'TEMPLATE' or key not in PR.ISLAND_META:
            continue
        data = json.loads(jf.read_text(encoding='utf-8'))
        meta = PR.ISLAND_META[key]
        for lang, rel in (('en', f'island/{key}/itinerary'), ('el', f'el/island/{key}/programma')):
            html = render(key, data, meta, lang)
            if not html:
                continue
            out = ROOT / rel / 'index.html'
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html, encoding='utf-8')
            n += 1
        keys.append(key)
    rows = update_sitemap(keys)
    print(f'✓ Itinerary pages built: {n} ({len(keys)} islands × 2), sitemap rows {rows}')


if __name__ == '__main__':
    main()
