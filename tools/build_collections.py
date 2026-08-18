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
                privacy_label=('Απόρρητο' if is_el else 'Privacy')))
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
                 'Η Ερείκουσα έχει τα περισσότερα καταλύματα· ο Μαθράκι τα λιγότερα.',
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
                privacy_label=('Απόρρητο' if is_el else 'Privacy')))
    out = ROOT / (path_el if is_el else path_en).strip('/')
    out.mkdir(parents=True, exist_ok=True)
    (out / 'index.html').write_text(html, encoding='utf-8')


def main():
    meta = load_meta()
    gnames = greek_names()
    photos = hero_photos()
    for lang in ('en', 'el'):
        build_quiet(lang, meta, gnames, photos)
        build_diapontia(lang, meta, gnames, photos)
    added = patch_sitemap([('/quiet-islands/', '/el/quiet-islands/'),
                           ('/diapontia/', '/el/diapontia/')])
    print(f'✓ Collections built: /quiet-islands/ + /diapontia/ (EN+EL), '
          f'{added} sitemap entries added')
    return 0


if __name__ == '__main__':
    sys.exit(main())
