#!/usr/bin/env python3
"""Collection pages — island groupings a single-island page can't rank for.

Two pages, EN + EL:

  /quiet-islands/   "Greek islands where nothing happens" — the whole corpus
                    ranked on a transparent quiet score. Mainstream Greek travel
                    titles publish this list constantly as assertion; this site
                    can rank it, which is the only real differentiator.

  /diapontia/       Othonoi, Erikousa and Mathraki as one trip. Travellers reach
                    the Diapontia as a group, never individually, so no single
                    island page can answer the query.

Reuses head/header/footer helpers from build_festival_extras.
Patches sitemap.xml — run LAST in the build chain, alongside build_match_page.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_festival_extras import (  # noqa: E402
    ROOT, SITE_URL, esc, page_head, header_nav, FOOTER, patch_sitemap,
)

YEAR = date.today().year

CSS = '''<style>
.cx-page{max-width:1000px;margin:0 auto;padding:26px 22px 40px}
.cx-page h1{font-family:var(--font-display,Georgia,serif);font-size:31px;margin:0 0 10px}
.cx-intro{font-size:16.5px;line-height:1.65;color:var(--ink-2,#3C4A57);margin:0 0 22px;max-width:70ch}
.cx-page h2{font-family:var(--font-display,Georgia,serif);font-size:21px;margin:32px 0 12px}
.cx-note{font-size:13.5px;color:var(--ink-3,#637080);background:var(--sand,#FAF6EF);
  border-radius:12px;padding:12px 15px;margin:0 0 22px;line-height:1.6}
.cx-list{list-style:none;margin:0;padding:0}
.cx-row{display:flex;align-items:flex-start;gap:14px;padding:14px 4px;
  border-bottom:1px solid var(--line,#E4E9ED)}
.cx-row:last-child{border-bottom:0}
.cx-rank{flex:none;width:26px;font-weight:800;font-size:15px;color:var(--ink-4,#A0ADB8);text-align:right;padding-top:2px}
.cx-body{flex:1 1 auto;min-width:0}
.cx-name{font-weight:800;font-size:16px;margin:0 0 3px}
.cx-name a{color:var(--ink-1,#1A2332);text-decoration:none}
.cx-name a:hover{color:var(--aegean-dark,#076880)}
.cx-why{font-size:14px;color:var(--ink-3,#637080);line-height:1.55;margin:0}
.cx-facts{display:flex;flex-wrap:wrap;gap:6px;margin-top:7px}
.cx-fact{font-size:12px;font-weight:700;background:var(--sand,#FAF6EF);
  border-radius:20px;padding:3px 10px;color:var(--ink-2,#3C4A57)}
.cx-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin:0 0 6px}
.cx-card{border:1px solid var(--line,#E4E9ED);border-radius:14px;overflow:hidden;background:var(--white,#fff)}
.cx-card img{width:100%;height:150px;object-fit:cover;display:block}
.cx-card-b{padding:13px 15px 15px}
.cx-card h3{margin:0 0 5px;font-size:17px}
.cx-card h3 a{color:var(--ink-1,#1A2332);text-decoration:none}
.cx-card p{margin:0;font-size:13.5px;line-height:1.55;color:var(--ink-3,#637080)}
.cx-page ol.cx-steps{padding-left:20px;line-height:1.7;font-size:15px;max-width:70ch}
.cr-island{margin:26px 0 0}
.cr-island h3{font-size:17px;margin:0 0 8px}
.cr-island h3 a{color:var(--ink-1,#1A2332);text-decoration:none}
.cr-island h3 small{font-weight:600;font-size:12.5px;color:var(--ink-4,#A0ADB8)}
.cr-list{list-style:none;margin:0;padding:0;font-size:13.5px;line-height:1.7;color:var(--ink-3,#637080)}
.cr-list li{padding:2px 0;border-bottom:1px solid var(--line,#EFF3F6)}
.cr-list li:last-child{border-bottom:0}
.cr-subj{font-weight:700;color:var(--ink-2,#3C4A57)}
.cr-list a{color:#076880;text-decoration:none}
.cx-facts{display:flex;flex-wrap:wrap;gap:6px}
</style>'''


def load_meta():
    """Island stats parsed from script.js's ISLANDS_DATA."""
    js = (ROOT / 'script.js').read_text(encoding='utf-8')
    start = js.index('const ISLANDS_DATA =')
    end = js.index('\n};', start) + 3
    block = js[start:end]
    out = {}
    for m in re.finditer(r'"([a-z-]+)":\s*\{([^}]+)\}', block):
        key, body = m.group(1), m.group(2)

        def num(name):
            mm = re.search(name + r':\s*([\d.]+)', body)
            return float(mm.group(1)) if mm else None

        nm = re.search(r'name:"([^"]+)"', body)
        grp = re.search(r'island_group:"([^"]+)"', body)
        out[key] = {
            'name': nm.group(1) if nm else key.title(),
            'group': grp.group(1) if grp else '',
            'night': num('night') or 0, 'pop': num('pop') or 0,
            'beach': num('beach') or 0, 'total': num('total') or 0,
            'car_need': num('car_need') or 0, 'access': num('access') or 0,
            'area': num('area') or 0, 'days': int(num('days') or 3),
            'hiking': 'hiking:true' in body.replace(' ', ''),
        }
    return out


def greek_names():
    out = {}
    for f in sorted((ROOT / 'islands').glob('*.json')):
        d = json.loads(f.read_text(encoding='utf-8'))
        out[d['key']] = d.get('name_el') or d.get('name') or d['key']
    return out


def hero_photos():
    p = ROOT / 'hero-photos.json'
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}


def thumb(url):
    if not url:
        return ''
    if 'res.cloudinary.com' in url:
        return re.sub(r'/upload/(?:[^/]*/)?v(\d+)/',
                      r'/upload/w_520,h_300,c_fill,g_auto,q_auto,f_auto/v\1/', url)
    return url


# ---------------------------------------------------------------- quiet score

def quiet_score(m):
    """How little happens here, 0-10.

    Deliberately simple and stated on the page: quiet is mostly the absence of
    nightlife and the absence of people, with a bonus for islands small enough
    to cross on foot. Access is NOT part of it — hard to reach is a different
    claim from quiet, and conflating them would just rank the ferry timetable.
    """
    import math
    night = max(0.0, 5.0 - m['night']) / 5.0            # 0-1, quiet evenings
    pop = max(0.0, 4.0 - math.log10(max(m['pop'], 1))) / 4.0   # 0-1, few people
    walk = max(0.0, 3.0 - m['car_need']) / 3.0          # 0-1, no car needed
    return round((night * 4.2 + pop * 4.2 + walk * 1.6), 2)


def quiet_line(m, lang):
    """One honest sentence, built from that island's own numbers."""
    pop = int(m['pop'])
    if lang == 'el':
        bits = []
        bits.append(f'{pop:,}'.replace(',', '.') + ' κάτοικοι' if pop >= 1000 else f'{pop} κάτοικοι')
        bits.append('νυχτερινή ζωή %.1f/5' % m['night'])
        if m['car_need'] <= 1.5:
            bits.append('δεν χρειάζεσαι αυτοκίνητο')
        if m['beach'] >= 4.0:
            bits.append('παραλίες %.1f/5' % m['beach'])
        return ' · '.join(bits)
    bits = [f'{pop:,} residents' if pop >= 1000 else f'{pop} residents',
            'nightlife %.1f/5' % m['night']]
    if m['car_need'] <= 1.5:
        bits.append('no car needed')
    if m['beach'] >= 4.0:
        bits.append('beaches %.1f/5' % m['beach'])
    return ' · '.join(bits)


def build_quiet(lang, meta, gnames, photos):
    is_el = lang == 'el'
    path_en, path_el = '/quiet-islands/', '/el/quiet-islands/'
    ranked = sorted(meta.items(), key=lambda kv: -quiet_score(kv[1]))[:20]

    if is_el:
        title = f'Ελληνικά νησιά όπου δεν συμβαίνει τίποτα — {YEAR}'
        desc = ('Τα πιο ήσυχα ελληνικά νησιά, με βαθμολογία: λίγοι κάτοικοι, καθόλου νυχτερινή ζωή, '
                'χωρίς αυτοκίνητο. Κατάταξη βάσει δεδομένων, όχι εντυπώσεων.')
        h1 = 'Ελληνικά νησιά όπου δεν συμβαίνει τίποτα'
        intro = ('Κάθε καλοκαίρι δημοσιεύονται λίστες με «ήσυχα νησιά». Σχεδόν ποτέ δεν εξηγούν '
                 'γιατί ένα νησί μπαίνει στη λίστα. Εδώ βαθμολογούμε και τα 88 νησιά και σου '
                 'δείχνουμε τους αριθμούς: πόσοι μένουν εκεί, τι νυχτερινή ζωή υπάρχει, αν '
                 'χρειάζεσαι αυτοκίνητο.')
        note = ('<strong>Πώς υπολογίζεται:</strong> ησυχία = απουσία νυχτερινής ζωής (42%) + '
                'μικρός πληθυσμός (42%) + νησί που το περπατάς (16%). Η δυσκολία πρόσβασης '
                'δεν μετράει — «δυσπρόσιτο» δεν σημαίνει «ήσυχο».')
        h2 = 'Τα 20 πιο ήσυχα'
        foot = 'Δες όλα τα νησιά με βαθμολογίες →'
        foot_href = '/el/#data'
    else:
        title = f'Greek Islands Where Nothing Happens — Ranked, {YEAR}'
        desc = ('The quietest Greek islands, scored: few residents, no nightlife, no car needed. '
                'A ranking from data on all 88 islands, not a list of assertions.')
        h1 = 'Greek islands where nothing happens'
        intro = ('Every summer brings another list of "quiet Greek islands", and almost none of them '
                 'say why an island made the cut. This one scores all 88 and shows you the numbers: '
                 'how many people live there, what the nightlife amounts to, whether you need a car.')
        note = ('<strong>How this is scored:</strong> quiet is the absence of nightlife (42%) plus '
                'the absence of people (42%) plus being small enough to walk (16%). How hard the '
                'island is to reach is deliberately excluded — remote is a different claim from quiet.')
        h2 = 'The 20 quietest'
        foot = 'See every island with full scores →'
        foot_href = '/#data'

    rows = []
    for i, (key, m) in enumerate(ranked, 1):
        nm = gnames.get(key, m['name']) if is_el else m['name']
        href = f'/el/island/{key}/' if is_el else f'/island/{key}/'
        rows.append(
            f'<li class="cx-row"><span class="cx-rank">{i}</span><div class="cx-body">'
            f'<p class="cx-name"><a href="{href}">{esc(nm)}</a></p>'
            f'<p class="cx-why">{esc(quiet_line(m, lang))}</p></div></li>')

    html = (page_head(title, desc, path_en, path_el, lang)
            + header_nav(lang, (path_en if is_el else path_el), active='')
            + CSS
            + f'''<main class="cx-page">
<h1>{esc(h1)}</h1>
<p class="cx-intro">{esc(intro)}</p>
<div class="cx-note">{note}</div>
<h2>{esc(h2)}</h2>
<ol class="cx-list">
{chr(10).join(rows)}
</ol>
<p style="margin-top:22px"><a href="{foot_href}" style="color:#076880;font-weight:800;text-decoration:none">{esc(foot)}</a></p>
</main>
'''
            + FOOTER.format(
                lang_link=(path_en if is_el else path_el),
                lang_label=('English' if is_el else 'Ελληνικά'),
                privacy=('/el/privacy/' if is_el else '/privacy/'),
                privacy_label=('Απόρρητο' if is_el else 'Privacy'),
                credits=('/el/credits/' if is_el else '/credits/'),
                credits_label=('Πηγές φωτογραφιών' if is_el else 'Photo credits')))
    out = ROOT / (path_el if is_el else path_en).strip('/')
    out.mkdir(parents=True, exist_ok=True)
    (out / 'index.html').write_text(html, encoding='utf-8')


# ---------------------------------------------------------------- Diapontia

DIAPONTIA = ['othonoi', 'erikousa', 'mathraki']


def build_diapontia(lang, meta, gnames, photos):
    is_el = lang == 'el'
    path_en, path_el = '/diapontia/', '/el/diapontia/'

    if is_el:
        title = f'Διαπόντια Νησιά — Οθωνοί, Ερείκουσα, Μαθράκι ({YEAR})'
        desc = ('Οδηγός για τα τρία Διαπόντια νησιά βορειοδυτικά της Κέρκυρας — πώς πας, '
                'πόσες μέρες χρειάζεσαι, και ποιο ταιριάζει σε ποιον.')
        h1 = 'Τα Διαπόντια Νησιά'
        intro = ('Τρία μικρά νησιά βορειοδυτικά της Κέρκυρας: Οθωνοί, Ερείκουσα, Μαθράκι. '
                 'Σχεδόν κανείς δεν πάει σε ένα μόνο από αυτά — τα φτάνεις μαζί, με το ίδιο '
                 'καραβάκι, και η επιλογή είναι πού θα κοιμηθείς.')
        h2a, h2b = 'Τα τρία νησιά', 'Πώς πας'
        steps = ['Πλοίο από τον Άγιο Στέφανο Αβλιωτών (βορειοδυτική Κέρκυρα) — η πιο συχνή σύνδεση το καλοκαίρι.',
                 'Καθημερινά καραβάκια συνδέουν τα τρία νησιά μεταξύ τους μέσα στη σεζόν.',
                 'Η Ερείκουσα έχει τα περισσότερα καταλύματα· το Μαθράκι τα λιγότερα.',
                 'Εκτός σεζόν τα δρομολόγια αραιώνουν πολύ — έλεγξε πριν κλείσεις.']
        note = ('<strong>Ποιο να διαλέξεις:</strong> Οθωνοί αν θέλεις το μεγαλύτερο και τη σπηλιά '
                'της Καλυψώς· Ερείκουσα αν θέλεις αμμουδιά και ευκολία· Μαθράκι αν θέλεις '
                'πραγματικά να μη συναντήσεις κανέναν.')
    else:
        title = f'The Diapontia Islands — Othonoi, Erikousa, Mathraki ({YEAR})'
        desc = ('A guide to the three Diapontia islands northwest of Corfu — how to reach them, '
                'how many days you need, and which one suits whom.')
        h1 = 'The Diapontia Islands'
        intro = ('Three small islands off the northwest tip of Corfu: Othonoi, Erikousa and Mathraki. '
                 'Almost nobody visits just one — you reach them on the same small boat, and the '
                 'real decision is which one you sleep on.')
        h2a, h2b = 'The three islands', 'Getting there'
        steps = ['Boats run from Agios Stefanos Avlioton on the northwest coast of Corfu — the most frequent summer link.',
                 'In season, local boats also connect the three islands to each other.',
                 'Erikousa has the most rooms; Mathraki the fewest.',
                 'Out of season the service thins dramatically — check before you book anything.']
        note = ('<strong>Which one:</strong> Othonoi for the largest island and the Calypso cave; '
                'Erikousa for a sandy beach and the easiest logistics; Mathraki if the point is '
                'to meet nobody at all.')

    cards = []
    for key in DIAPONTIA:
        m = meta.get(key)
        if not m:
            continue
        nm = gnames.get(key, m['name']) if is_el else m['name']
        href = f'/el/island/{key}/' if is_el else f'/island/{key}/'
        img = thumb((photos.get(key) or {}).get('url', ''))
        line = quiet_line(m, lang)
        cards.append(
            f'<div class="cx-card">'
            + (f'<img src="{img}" alt="{esc(nm)}" loading="lazy">' if img else '')
            + f'<div class="cx-card-b"><h3><a href="{href}">{esc(nm)}</a></h3>'
              f'<p>{esc(line)}</p></div></div>')

    html = (page_head(title, desc, path_en, path_el, lang)
            + header_nav(lang, (path_en if is_el else path_el), active='')
            + CSS
            + f'''<main class="cx-page">
<h1>{esc(h1)}</h1>
<p class="cx-intro">{esc(intro)}</p>
<h2>{esc(h2a)}</h2>
<div class="cx-cards">
{chr(10).join(cards)}
</div>
<div class="cx-note" style="margin-top:18px">{note}</div>
<h2>{esc(h2b)}</h2>
<ol class="cx-steps">
{chr(10).join('<li>' + esc(s) + '</li>' for s in steps)}
</ol>
</main>
'''
            + FOOTER.format(
                lang_link=(path_en if is_el else path_el),
                lang_label=('English' if is_el else 'Ελληνικά'),
                privacy=('/el/privacy/' if is_el else '/privacy/'),
                privacy_label=('Απόρρητο' if is_el else 'Privacy'),
                credits=('/el/credits/' if is_el else '/credits/'),
                credits_label=('Πηγές φωτογραφιών' if is_el else 'Photo credits')))
    out = ROOT / (path_el if is_el else path_en).strip('/')
    out.mkdir(parents=True, exist_ok=True)
    (out / 'index.html').write_text(html, encoding='utf-8')



# ---------------------------------------------------------------- credits

def collect_credits():
    """Every attributed photo on the site, grouped by island.

    Aug 2026: 474 photos carry a CC licence naming a photographer. The inline
    badge on each image is the primary attribution; this page is the durable,
    linkable record — and the honest thing for a site built on other people's
    photographs to have.
    """
    out = []
    for f in sorted((ROOT / 'islands').glob('*.json')):
        d = json.loads(f.read_text(encoding='utf-8'))
        key = d['key']
        items = []

        def take(o, what):
            c = o.get('photo_credit')
            if o.get('photo') and isinstance(c, dict) and (c.get('artist') or c.get('license')):
                items.append({
                    'subject': o.get('name') or what,
                    'artist': (c.get('artist') or '').strip(),
                    'license': (c.get('license') or '').strip(),
                    'license_url': (c.get('license_url') or '').strip(),
                    'page_url': (c.get('page_url') or '').strip(),
                    'source': (c.get('source') or '').strip(),
                })

        for day in (d.get('itinerary') or {}).get('days', []):
            for st in day.get('stops', []):
                take(st, 'stop')
        for b in (d.get('beaches') or []):
            take(b, 'beach')
        if items:
            out.append((key, d.get('name') or key.title(), d.get('name_el') or d.get('name'), items))
    return out


def build_credits(lang, groups):
    is_el = lang == 'el'
    path_en, path_el = '/credits/', '/el/credits/'
    total = sum(len(i[3]) for i in groups)
    photographers = len({it['artist'] for _, _, _, items in groups for it in items if it['artist']})

    if is_el:
        title = 'Πηγές φωτογραφιών & άδειες χρήσης'
        desc = (f'Κάθε φωτογραφία με άδεια Creative Commons στο Aegean Blueprint — {total} '
                f'φωτογραφίες από {photographers} φωτογράφους, με άδεια και πηγή.')
        h1 = 'Πηγές φωτογραφιών'
        intro = (f'Το μεγαλύτερο μέρος των φωτογραφιών σε αυτόν τον ιστότοπο προέρχεται από '
                 f'φωτογράφους που τις διέθεσαν με άδεια Creative Commons. Εδώ είναι όλες: '
                 f'{total} φωτογραφίες, {photographers} φωτογράφοι. Η αναφορά υπάρχει και '
                 f'πάνω σε κάθε φωτογραφία, με το κουμπάκι «i».')
        lic_h = 'Άδειες που χρησιμοποιούνται'
        note = ('Αν είσαι ο δημιουργός μιας φωτογραφίας και θέλεις διαφορετική αναφορά ή '
                'αφαίρεση, στείλε μήνυμα και θα γίνει αμέσως.')
    else:
        title = 'Photo credits & licences'
        desc = (f'Every Creative Commons photograph on Aegean Blueprint — {total} photos by '
                f'{photographers} photographers, with licence and source for each.')
        h1 = 'Photo credits'
        intro = (f'Most of the photographs on this site were taken by other people and released '
                 f'under Creative Commons licences. Here they all are: {total} photos by '
                 f'{photographers} photographers. The same credit appears on every image itself, '
                 f'behind the small "i" badge.')
        lic_h = 'Licences in use'
        note = ('If you took one of these and would like the credit worded differently, or the '
                'photo removed, get in touch and it will be changed straight away.')

    lic_counts = {}
    for _, _, _, items in groups:
        for it in items:
            lic_counts[it['license'] or '—'] = lic_counts.get(it['license'] or '—', 0) + 1
    lic_rows = ''.join(
        f'<span class="cx-fact">{esc(k)} · {v}</span>'
        for k, v in sorted(lic_counts.items(), key=lambda kv: -kv[1]))

    blocks = []
    for key, name_en, name_el, items in groups:
        nm = (name_el or name_en) if is_el else name_en
        href = f'/el/island/{key}/' if is_el else f'/island/{key}/'
        rows = []
        for it in items:
            who = esc(it['artist']) or ('Άγνωστος' if is_el else 'Unknown')
            lic = esc(it['license'])
            if it['license_url']:
                lic = f'<a href="{esc(it["license_url"])}" target="_blank" rel="noopener nofollow">{lic}</a>'
            src = ''
            if it['page_url']:
                label = it['source'] or 'source'
                src = (f' · <a href="{esc(it["page_url"])}" target="_blank" rel="noopener nofollow">'
                       f'{esc(label)}</a>')
            rows.append(f'<li><span class="cr-subj">{esc(it["subject"])}</span> — {who}'
                        f'{" · " + lic if lic else ""}{src}</li>')
        blocks.append(f'<section class="cr-island"><h3><a href="{href}">{esc(nm)}</a>'
                      f' <small>{len(items)}</small></h3><ul class="cr-list">'
                      + ''.join(rows) + '</ul></section>')

    html = (page_head(title, desc, path_en, path_el, lang)
            + header_nav(lang, (path_en if is_el else path_el), active='')
            + CSS
            + f'''<main class="cx-page">
<h1>{esc(h1)}</h1>
<p class="cx-intro">{esc(intro)}</p>
<h2>{esc(lic_h)}</h2>
<div class="cx-facts">{lic_rows}</div>
<div class="cx-note" style="margin-top:20px">{esc(note)}</div>
{"".join(blocks)}
</main>
'''
            + FOOTER.format(
                lang_link=(path_en if is_el else path_el),
                lang_label=('English' if is_el else 'Ελληνικά'),
                privacy=('/el/privacy/' if is_el else '/privacy/'),
                privacy_label=('Απόρρητο' if is_el else 'Privacy'),
                credits=('/el/credits/' if is_el else '/credits/'),
                credits_label=('Πηγές φωτογραφιών' if is_el else 'Photo credits')))
    out = ROOT / (path_el if is_el else path_en).strip('/')
    out.mkdir(parents=True, exist_ok=True)
    (out / 'index.html').write_text(html, encoding='utf-8')
    return total, photographers

def main():
    meta = load_meta()
    gnames = greek_names()
    photos = hero_photos()
    credits = collect_credits()
    for lang in ('en', 'el'):
        build_quiet(lang, meta, gnames, photos)
        build_diapontia(lang, meta, gnames, photos)
        n_photos, n_people = build_credits(lang, credits)
    added = patch_sitemap([('/quiet-islands/', '/el/quiet-islands/'),
                           ('/diapontia/', '/el/diapontia/'),
                           ('/credits/', '/el/credits/')])
    print(f'✓ Collections built: /quiet-islands/, /diapontia/, /credits/ (EN+EL) — '
          f'{n_photos} photos by {n_people} photographers, {added} sitemap entries added')
    return 0


if __name__ == '__main__':
    sys.exit(main())
