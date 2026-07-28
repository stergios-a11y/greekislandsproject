#!/usr/bin/env python3
"""Festival long-tail pages: 12 month hubs (EN+EL) + the Ikaria panigiria article.

Month hubs live at /festivals/<month>/ and /el/festivals/<month>/ — lean landing
pages for "greek island festivals in august" / "πανηγύρια Αύγουστος" queries.
The main /festivals/ page remains the full calendar (hubs link back to it).

The Ikaria page is the one festival subject deep enough to earn a standalone
article: /festivals/ikaria-panigiria/ (+ EL).

Patches sitemap.xml with the new URLs, so run AFTER prerender.py and
build_compare_pages.py (both regenerate/patch the sitemap).
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = 'https://aegeanblueprint.com'
STYLE_V = 43   # keep in sync with index.html
YEAR = date.today().year

TP_SCRIPT = '<script async data-cfasync="false" data-noptimize="1" data-no-defer="1" src="https://emrldtp.com/NTUxOTU3.js?t=551957"></script>'

MONTHS = [
    ('january', 'January', 'Ιανουάριος', 'τον Ιανουάριο'),
    ('february', 'February', 'Φεβρουάριος', 'τον Φεβρουάριο'),
    ('march', 'March', 'Μάρτιος', 'τον Μάρτιο'),
    ('april', 'April', 'Απρίλιος', 'τον Απρίλιο'),
    ('may', 'May', 'Μάιος', 'τον Μάιο'),
    ('june', 'June', 'Ιούνιος', 'τον Ιούνιο'),
    ('july', 'July', 'Ιούλιος', 'τον Ιούλιο'),
    ('august', 'August', 'Αύγουστος', 'τον Αύγουστο'),
    ('september', 'September', 'Σεπτέμβριος', 'τον Σεπτέμβριο'),
    ('october', 'October', 'Οκτώβριος', 'τον Οκτώβριο'),
    ('november', 'November', 'Νοέμβριος', 'τον Νοέμβριο'),
    ('december', 'December', 'Δεκέμβριος', 'τον Δεκέμβριο'),
]

_MONTH_NAMES = {m[1].lower(): i + 1 for i, m in enumerate(MONTHS)}
_MONTH_NAMES.update({'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'jun': 6, 'jul': 7,
                     'aug': 8, 'sep': 9, 'sept': 9, 'oct': 10, 'nov': 11, 'dec': 12})


def esc(s):
    return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def when_to_months(when):
    s = (when or '').lower()
    months = set()
    for name, num in _MONTH_NAMES.items():
        if re.search(r'\b' + name + r'\b', s):
            months.add(num)
    m = re.search(r'(\w+)\s+through\s+(?:early\s+|mid-)?(\w+)', s)
    if m:
        a, b = _MONTH_NAMES.get(m.group(1)), _MONTH_NAMES.get(m.group(2))
        if a and b:
            months.update(range(a, b + 1) if a <= b else list(range(a, 13)) + list(range(1, b + 1)))
    if not months:
        if 'easter' in s or 'holy' in s or 'pentecost' in s or 'whitsun' in s:
            months.update([4, 5])
        if 'pre-lent' in s or 'apokries' in s or 'carnival' in s:
            months.update([2, 3])
    return sorted(months)


def slugify(s):
    s = re.sub(r'[^a-z0-9]+', '-', (s or '').lower())
    return s.strip('-')[:60]


def collect():
    fests = []
    names = {}
    for f in sorted((ROOT / 'islands').glob('*.json')):
        d = json.loads(f.read_text(encoding='utf-8'))
        names[d['key']] = (d.get('name') or d['key'].title(), d.get('name_el') or d.get('name') or d['key'])
        for x in (d.get('festivals') or []):
            if isinstance(x, dict):
                fests.append(dict(x, island=d['key'], months=when_to_months(x.get('when', ''))))
    return fests, names


def page_head(title, desc, path_en, path_el, lang):
    url = SITE_URL + (path_el if lang == 'el' else path_en)
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#0B8FAC">
<meta name="author" content="Stergios Gousios">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{SITE_URL}{path_en}">
<link rel="alternate" hreflang="el" href="{SITE_URL}{path_el}">
<link rel="alternate" hreflang="x-default" href="{SITE_URL}{path_en}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<link rel="icon" href="/logo-hero.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css?v={STYLE_V}">
{TP_SCRIPT}
</head>'''


def header_nav(lang, toggle_href, active='festivals'):
    p = '/el/' if lang == 'el' else '/'
    L = (lambda en, el: el if lang == 'el' else en)
    return f'''<body>
<header>
  <div class="header-content">
    <a class="logo-wrapper" href="{p}" style="text-decoration: none;">
      <img src="/logo-hero.svg" id="site-logo" alt="Aegean Blueprint logo">
      <span id="brand-text"><span class="brand-word">Aegean</span> <span class="brand-word">Blueprint</span></span>
    </a>
    <div class="menu-toggle" id="menu-toggle-btn"><span></span><span></span><span></span></div>
    <nav class="top-nav" id="main-nav">
      <a href="{p}#compare">{L('Compare', 'Σύγκριση')}</a>
      <a href="{p}#match"{' class="active"' if active == 'match' else ''}>{L('Match Me', 'Βρες το Νησί σου')}</a>
      <a href="{p}trip-cost/">{L('Budget', 'Μπάτζετ')}</a>
      <a href="{p}#hopping">{L('Ferries &amp; Hopping', 'Πλοία &amp; Νησοπορία')}</a>
      <a href="{p}festivals/"{' class="active"' if active == 'festivals' else ''}>{L('Festivals', 'Γιορτές')}</a>
      <a href="{p}#data">{L('Islands Data', 'Στοιχεία Νησιών')}</a>
      <a href="{p}#mission">{L('Mission', 'Στόχος')}</a>
      <a href="{p}#shortlist">{L('⭐ My Shortlist', '⭐ Η Λίστα μου')}</a>
    </nav>
    <a class="lang-toggle-static" href="{toggle_href}" style="background: none; border: 1px solid rgba(255,255,255,0.4); color: #fff; padding: 4px 10px; border-radius: 4px; text-decoration: none; font-size: 13px; white-space: nowrap;"><span style="margin-right: 4px;">🌐</span>{'EN' if lang == 'el' else 'EL'}</a>
  </div>
</header>
<script>document.getElementById("menu-toggle-btn").addEventListener("click",function(){{var n=document.getElementById("main-nav");n.classList.toggle("open");this.classList.toggle("open");}});</script>'''


FOOTER = '''<footer class="seo-footer" style="max-width:1000px;margin:0 auto;padding:24px 22px;font-size:13px;color:#637080">
  <p>© 2026 Aegean Blueprint · <a href="{lang_link}" style="color:#076880;text-decoration:none">{lang_label}</a> · <a href="{privacy}" style="color:#076880;text-decoration:none">{privacy_label}</a></p>
</footer>
</body>
</html>'''

BUDGET_MONTH = {4: 'apr', 5: 'may', 6: 'jun', 7: 'jul', 8: 'aug', 9: 'sep', 10: 'oct'}


def fest_entry(f, names, lang, mnum):
    is_el = lang == 'el'
    name = f.get('name_el') if is_el and f.get('name_el') else f.get('name', '')
    when = f.get('when_el') if is_el and f.get('when_el') else f.get('when', '')
    desc = f.get('desc_el') if is_el and f.get('desc_el') else f.get('desc', '')
    iname = names[f['island']][1 if is_el else 0]
    ipath = f"{'/el' if is_el else ''}/island/{f['island']}/"
    slug = slugify(f.get('name', ''))
    budget = ''
    if mnum in BUDGET_MONTH:
        bhref = f"{'/el' if is_el else ''}/trip-cost/?i={f['island']}%3A3&m={BUDGET_MONTH[mnum]}"
        blabel = 'Πόσο κοστίζει αυτό το ταξίδι; →' if is_el else 'What would this trip cost? →'
        budget = f'<a class="fx-budget" href="{bhref}">💶 {blabel}</a>'
    return f'''  <article class="fest-card" id="{slug}">
    <div class="fest-text">
      <a class="fest-island" href="{ipath}">{esc(iname)}</a>
      <h2 class="fest-name">{esc(name)}</h2>
      <p class="fest-when">{esc(when)}</p>
      <p class="fest-desc">{esc(desc)}</p>
      {budget}
    </div>
  </article>'''


EXTRA_CSS = '''<style>
.fx-page{max-width:1000px;margin:0 auto;padding:26px 22px 50px}
.fx-page h1{font-family:'Alegreya',serif;font-size:32px;margin-bottom:8px}
.fx-intro{color:#637080;font-size:15px;line-height:1.65;max-width:760px;margin-bottom:8px}
.fx-months{margin:16px 0 26px;font-size:13.5px;font-weight:700;line-height:2.1}
.fx-months a{color:#076880;text-decoration:none;background:rgba(200,238,245,.45);border-radius:999px;padding:5px 12px;margin-right:6px;white-space:nowrap}
.fx-months a.on{background:#0B8FAC;color:#fff}
.fest-card{background:#fff;border-radius:14px;box-shadow:0 4px 18px rgba(26,35,50,.09);padding:18px 20px;margin-bottom:14px}
.fest-island{font-size:12px;font-weight:800;color:#076880;text-decoration:none;text-transform:uppercase;letter-spacing:.05em}
.fest-name{font-family:'Alegreya',serif;font-size:21px;margin:4px 0 2px}
.fest-when{font-weight:800;font-size:13.5px;color:#C6421F;margin:0 0 6px}
.fest-desc{font-size:14.5px;line-height:1.6;color:#2E3D50;margin:0}
.fx-budget{display:inline-block;margin-top:10px;font-size:12.5px;font-weight:800;color:#076880;text-decoration:none;background:rgba(232,247,251,.9);border-radius:999px;padding:6px 13px}
.fx-back{display:inline-block;margin-top:22px;font-weight:800;font-size:14px;color:#076880;text-decoration:none}
.fx-art p{font-size:15.5px;line-height:1.75;color:#2E3D50;max-width:760px;margin:0 0 16px}
.fx-art h2{font-family:'Alegreya',serif;font-size:23px;margin:28px 0 10px}
.fx-art ul{max-width:760px;margin:0 0 16px 20px;font-size:15px;line-height:1.7;color:#2E3D50}
.fx-cal{max-width:760px;border-collapse:collapse;margin:0 0 16px;font-size:14.5px}
.fx-cal td{padding:9px 14px 9px 0;border-bottom:1px dashed rgba(26,35,50,.15);vertical-align:top}
.fx-cal td:first-child{font-weight:800;white-space:nowrap;color:#C6421F}
</style>'''


def month_links(active_slug, lang, counts):
    p = '/el/festivals/' if lang == 'el' else '/festivals/'
    out = []
    for slug, en, el, _acc in MONTHS:
        n = counts.get(slug, 0)
        if not n:
            continue
        label = (el if lang == 'el' else en)
        cls = ' class="on"' if slug == active_slug else ''
        out.append(f'<a{cls} href="{p}{slug}/">{label} ({n})</a>')
    back = 'Πλήρες ημερολόγιο →' if lang == 'el' else 'Full calendar →'
    out.append(f'<a href="{"/el/festivals/" if lang == "el" else "/festivals/"}">{back}</a>')
    return '<nav class="fx-months">' + ' '.join(out) + '</nav>'


def build_month_hubs(fests, names):
    by_month = {}
    for f in fests:
        for m in f['months']:
            by_month.setdefault(m, []).append(f)
    counts = {MONTHS[m - 1][0]: len(v) for m, v in by_month.items()}
    made = []
    for mnum, flist in sorted(by_month.items()):
        slug, en, el, el_acc = MONTHS[mnum - 1]
        flist = sorted(flist, key=lambda f: f.get('when', ''))
        for lang in ('en', 'el'):
            is_el = lang == 'el'
            path_en, path_el = f'/festivals/{slug}/', f'/el/festivals/{slug}/'
            n = len(flist)
            if is_el:
                title = f'Πανηγύρια & γιορτές στα νησιά {el_acc} {YEAR} — {n} εκδηλώσεις | Aegean Blueprint'
                desc = f'Όλα τα πανηγύρια και οι γιορτές στα ελληνικά νησιά {el_acc}: ημερομηνίες, νησί και τι να περιμένεις. {n} εκδηλώσεις, ενημερωμένες για το {YEAR}.'
                h1 = f'Πανηγύρια & γιορτές {el_acc}'
                intro = f'{n} γιορτές και πανηγύρια στα νησιά {el_acc} — με ημερομηνίες και σύνδεσμο για τον πλήρη οδηγό κάθε νησιού. Οι κινητές γιορτές είναι υπολογισμένες για φέτος.'
            else:
                title = f'Greek Island Festivals in {en} {YEAR} — {n} events & dates | Aegean Blueprint'
                desc = f'Every island festival and panigiri in {en}: dates, which island, and what to expect. {n} events across the Greek islands, updated for {YEAR}.'
                h1 = f'Greek island festivals in {en}'
                intro = f'{n} festivals and panigiria across the islands in {en} — with dates and a link to each island’s full guide. Movable feasts are pinned to this year’s dates.'
            entries = '\n'.join(fest_entry(f, names, lang, mnum) for f in flist)
            html = (page_head(title, desc, path_en, path_el, lang)
                    + header_nav(lang, (path_en if is_el else path_el))
                    + EXTRA_CSS
                    + f'<main class="fx-page">\n<h1>{esc(h1)}</h1>\n<p class="fx-intro">{esc(intro)}</p>\n'
                    + month_links(slug, lang, counts)
                    + entries
                    + f'\n<a class="fx-back" href="{"/el/festivals/" if is_el else "/festivals/"}">&larr; {"Πλήρες ημερολόγιο γιορτών" if is_el else "Full festival calendar"}</a>\n</main>\n'
                    + FOOTER.format(
                        lang_link=(path_en if is_el else path_el),
                        lang_label=('English' if is_el else 'Ελληνικά'),
                        privacy=('/el/privacy/' if is_el else '/privacy/'),
                        privacy_label=('Απόρρητο' if is_el else 'Privacy')))
            out = ROOT / (path_el if is_el else path_en).strip('/')
            out.mkdir(parents=True, exist_ok=True)
            (out / 'index.html').write_text(html, encoding='utf-8')
        made.append((path_en, path_el))
    return made


# ------------------------------------------------------------------ Ikaria

IKARIA_EN = f'''
<p>Every Greek island has panigiria — the saint’s-day feasts that villages have thrown for centuries. Ikaria is where the tradition never became a show for visitors. An Ikarian panigiri is a village fundraiser, a family reunion, an all-night dance and a political statement about how life should be lived, all at once. There is no stage and no ticket. You sit where there is space, you eat what everyone eats, and at some point between midnight and sunrise you understand why this island is famous for forgetting to die.</p>
<h2>How an Ikarian panigiri works</h2>
<p>The mechanics matter, because they are the point. The feast is organised by the village itself, and everything you pay goes to the village: the school, the road, the water system, the clinic. You pay when the plate of food arrives — goat in tomato sauce, usually, with potatoes, soufiko if you are lucky, bread, and wine from the barrel — and the price is deliberately honest. The tables are long and communal; you will share yours with strangers, and by the second carafe they will not be strangers.</p>
<p>The music is live — violin and laouto, sometimes for twelve hours without a real break — and it builds toward the Ikariotikos, the island’s circling dance. It starts slow and gets faster, and the circle grows all night. Nobody minds a foreigner joining the outer ring; they mind a foreigner filming it instead of dancing it.</p>
<h2>The etiquette, briefly</h2>
<ul>
<li>Come late. Nothing worth seeing happens before 10pm; the peak is 2–4am.</li>
<li>Bring cash — you pay for the plate and the wine, and it funds the village.</li>
<li>Join the outer circle of the dance; follow the steps of the person to your right.</li>
<li>Don’t reserve, don’t rush, don’t expect a menu. There is one dish and it is correct.</li>
<li>Forget driving back early. Sleep is a September problem.</li>
</ul>
<h2>The calendar that matters</h2>
<p>Panigiria follow the saints’ days, so the dates are fixed — what varies is which village throws the biggest party each year. These are the reliable pillars of the season:</p>
<table class="fx-cal">
<tr><td>15 July</td><td><strong>Agios Kirykos</strong> — the capital’s feast for its patron saints, the warm-up for the big run.</td></tr>
<tr><td>17 July</td><td><strong>Agia Marina</strong> — celebrated in several villages, the season finding its rhythm.</td></tr>
<tr><td>20 July</td><td><strong>Profitis Ilias</strong> — always on hilltops: chapels on summits, dancing under open sky.</td></tr>
<tr><td>26–27 July</td><td><strong>Agia Paraskevi &amp; Agios Panteleimonas</strong> — one of the busiest stretches, several villages at once.</td></tr>
<tr><td>6 August</td><td><strong>Christos Raches (Transfiguration)</strong> — one of the island’s two giants; the mountain village fills with thousands and the dancing routinely ends at 7am.</td></tr>
<tr><td>15 August</td><td><strong>Langada (Dormition)</strong> — the most famous panigiri in Greece, in a near-abandoned mountain village above Agios Dimitrios. People come from across the island and the diaspora. If you attend one panigiri in your life, this is the one.</td></tr>
</ul></table>
<p>Smaller feasts continue into September, and there are winter ones for the committed. The saint’s day is fixed by the church calendar; villages occasionally shift the party to the nearest weekend — the kafeneio in any village will know, and asking is part of the experience.</p>
<p><em>Full disclosure: Ikaria is still on my own list — this guide is built from research and Ikarians’ own accounts, the way this site handles the few islands I haven’t reached yet. It will be rewritten, probably at length, the week I finally dance at Langada. If you’ve been and I got something wrong, the feedback button exists for exactly this.</em></p>
<h2>Planning around a panigiri</h2>
<p>Rooms near Christos Raches and Langada are effectively gone for 5–6 and 14–15 August; book months ahead or stay in Armenistis or Evdilos and accept the mountain drive. A car is essential — the great panigiria are in mountain villages, and taxis stop existing after midnight. Ferries fill around 15 August in both directions.</p>
'''

IKARIA_EL = f'''
<p>Κάθε ελληνικό νησί έχει πανηγύρια — τις γιορτές των αγίων που στήνουν τα χωριά εδώ και αιώνες. Η Ικαρία είναι το μέρος όπου η παράδοση δεν έγινε ποτέ θέαμα για τουρίστες. Το ικαριώτικο πανηγύρι είναι έρανος του χωριού, οικογενειακή επανένωση, ολονύχτιος χορός και δήλωση για το πώς πρέπει να ζει κανείς — όλα μαζί. Δεν υπάρχει σκηνή, δεν υπάρχει εισιτήριο. Κάθεσαι όπου υπάρχει χώρος, τρως ό,τι τρώνε όλοι, και κάπου ανάμεσα στα μεσάνυχτα και την ανατολή καταλαβαίνεις γιατί το νησί φημίζεται ότι ξεχνά να πεθάνει.</p>
<h2>Πώς λειτουργεί το ικαριώτικο πανηγύρι</h2>
<p>Η μηχανική έχει σημασία, γιατί είναι η ουσία. Τη γιορτή τη διοργανώνει το ίδιο το χωριό, και ό,τι πληρώσεις πάει στο χωριό: στο σχολείο, στον δρόμο, στο νερό, στο αγροτικό ιατρείο. Πληρώνεις όταν έρθει το πιάτο — κατσίκι κοκκινιστό συνήθως, με πατάτες, σουφικό αν είσαι τυχερός, ψωμί και κρασί από το βαρέλι — και η τιμή είναι σκόπιμα τίμια. Τα τραπέζια είναι μακριά και κοινά· θα το μοιραστείς με αγνώστους, και στη δεύτερη καράφα δεν θα είναι πια άγνωστοι.</p>
<p>Η μουσική είναι ζωντανή — βιολί και λαούτο, καμιά φορά δώδεκα ώρες χωρίς πραγματικό διάλειμμα — και χτίζει προς τον Ικαριώτικο. Ξεκινά αργά και γίνεται όλο και πιο γρήγορος, και ο κύκλος μεγαλώνει όλη νύχτα. Κανείς δεν ενοχλείται αν ένας ξένος μπει στον εξωτερικό κύκλο· ενοχλούνται αν τον τραβάει βίντεο αντί να τον χορεύει.</p>
<h2>Η εθιμοτυπία, σύντομα</h2>
<ul>
<li>Έλα αργά. Τίποτα αξιόλογο δεν συμβαίνει πριν τις 10 το βράδυ· η κορύφωση είναι 2–4 τα ξημερώματα.</li>
<li>Φέρε μετρητά — πληρώνεις το πιάτο και το κρασί, και τα έσοδα χρηματοδοτούν το χωριό.</li>
<li>Μπες στον εξωτερικό κύκλο του χορού· ακολούθησε τα βήματα του διπλανού σου.</li>
<li>Μην κάνεις κράτηση, μη βιάζεσαι, μην περιμένεις μενού. Υπάρχει ένα πιάτο και είναι το σωστό.</li>
<li>Ξέχνα την πρωινή επιστροφή. Ο ύπνος είναι πρόβλημα του Σεπτεμβρίου.</li>
</ul>
<h2>Το ημερολόγιο που μετράει</h2>
<p>Τα πανηγύρια ακολουθούν τις γιορτές των αγίων, άρα οι ημερομηνίες είναι σταθερές — αυτό που αλλάζει είναι ποιο χωριό στήνει το μεγαλύτερο γλέντι κάθε χρονιά. Οι σταθεροί πυλώνες της σεζόν:</p>
<table class="fx-cal">
<tr><td>15 Ιουλίου</td><td><strong>Άγιος Κήρυκος</strong> — η γιορτή της πρωτεύουσας για τους πολιούχους της, το προοίμιο της μεγάλης σειράς.</td></tr>
<tr><td>17 Ιουλίου</td><td><strong>Αγία Μαρίνα</strong> — γιορτάζεται σε αρκετά χωριά, η σεζόν βρίσκει ρυθμό.</td></tr>
<tr><td>20 Ιουλίου</td><td><strong>Προφήτης Ηλίας</strong> — πάντα σε κορυφές: ξωκλήσια σε υψώματα, χορός κάτω από ανοιχτό ουρανό.</td></tr>
<tr><td>26–27 Ιουλίου</td><td><strong>Αγία Παρασκευή &amp; Άγιος Παντελεήμονας</strong> — από τις πιο γεμάτες νύχτες, πολλά χωριά ταυτόχρονα.</td></tr>
<tr><td>6 Αυγούστου</td><td><strong>Χριστός Ραχών (Μεταμόρφωση)</strong> — ένας από τους δύο γίγαντες του νησιού· το ορεινό χωριό γεμίζει με χιλιάδες κόσμο και ο χορός τελειώνει συχνά στις 7 το πρωί.</td></tr>
<tr><td>15 Αυγούστου</td><td><strong>Λαγκάδα (Κοίμηση)</strong> — το πιο διάσημο πανηγύρι της Ελλάδας, σε ένα σχεδόν εγκαταλελειμμένο ορεινό χωριό πάνω από τον Άγιο Δημήτριο. Έρχεται κόσμος από όλο το νησί και τη διασπορά. Αν πας σε ένα πανηγύρι στη ζωή σου, είναι αυτό.</td></tr>
</table>
<p>Μικρότερες γιορτές συνεχίζουν τον Σεπτέμβριο, και υπάρχουν και χειμωνιάτικες για τους πιστούς του είδους. Η μέρα του αγίου είναι σταθερή από το εορτολόγιο· τα χωριά καμιά φορά μεταφέρουν το γλέντι στο κοντινότερο σαββατοκύριακο — το καφενείο κάθε χωριού ξέρει, και το να ρωτήσεις είναι μέρος της εμπειρίας.</p>
<p><em>Με ειλικρίνεια: η Ικαρία είναι ακόμη στη δική μου λίστα — αυτός ο οδηγός στηρίζεται σε έρευνα και στις αφηγήσεις των ίδιων των Ικαριωτών, όπως κάνει αυτό το site για τα λίγα νησιά που δεν έχω προλάβει ακόμη. Θα ξαναγραφτεί, μάλλον εκτενώς, τη βδομάδα που θα χορέψω επιτέλους στη Λαγκάδα. Αν έχεις πάει και κάτι δεν στέκει, το κουμπί feedback υπάρχει ακριβώς γι' αυτό.</em></p>
<h2>Οργάνωση γύρω από ένα πανηγύρι</h2>
<p>Δωμάτια κοντά στον Χριστό Ραχών και τη Λαγκάδα ουσιαστικά δεν υπάρχουν για 5–6 και 14–15 Αυγούστου· κλείσε μήνες πριν, ή μείνε σε Αρμενιστή ή Εύδηλο και δέξου την ορεινή διαδρομή. Το αυτοκίνητο είναι απαραίτητο — τα μεγάλα πανηγύρια γίνονται σε ορεινά χωριά και τα ταξί παύουν να υπάρχουν μετά τα μεσάνυχτα. Τα πλοία γεμίζουν γύρω στον Δεκαπενταύγουστο και προς τις δύο κατευθύνσεις.</p>
'''


def build_ikaria():
    for lang in ('en', 'el'):
        is_el = lang == 'el'
        path_en, path_el = '/festivals/ikaria-panigiria/', '/el/festivals/ikaria-panigiria/'
        if is_el:
            title = f'Πανηγύρια Ικαρίας {YEAR} — ημερομηνίες, χωριά & πώς να πας | Aegean Blueprint'
            desc = f'Τα πανηγύρια της Ικαρίας: πώς λειτουργούν, η εθιμοτυπία, και το ημερολόγιο {YEAR} — Χριστός Ραχών 6 Αυγούστου, Λαγκάδα 15 Αυγούστου, και όλη η καλοκαιρινή σειρά.'
            h1 = 'Τα πανηγύρια της Ικαρίας'
            body = IKARIA_EL
            cta = f'<a class="fx-budget" style="font-size:14px;padding:9px 18px" href="/el/trip-cost/?i=ikaria%3A4&m=aug">💶 Πόσο κοστίζει μια εβδομάδα πανηγυριών; →</a> <a class="fx-budget" style="font-size:14px;padding:9px 18px" href="/el/island/ikaria/">🏝 Ο πλήρης οδηγός της Ικαρίας →</a>'
        else:
            title = f'Ikaria Panigiria {YEAR} — dates, villages & how to join | Aegean Blueprint'
            desc = f'Ikaria’s all-night village feasts explained: how a panigiri works, the etiquette, and the {YEAR} calendar — Christos Raches on 6 August, the legendary Langada on 15 August.'
            h1 = 'The panigiria of Ikaria'
            body = IKARIA_EN
            cta = f'<a class="fx-budget" style="font-size:14px;padding:9px 18px" href="/trip-cost/?i=ikaria%3A4&m=aug">💶 What would a panigiri week cost? →</a> <a class="fx-budget" style="font-size:14px;padding:9px 18px" href="/island/ikaria/">🏝 Full Ikaria guide →</a>'
        html = (page_head(title, desc, path_en, path_el, lang)
                + header_nav(lang, (path_en if is_el else path_el))
                + EXTRA_CSS
                + f'<main class="fx-page fx-art">\n<h1>{esc(h1)}</h1>\n'
                + body
                + f'<p style="margin-top:22px">{cta}</p>\n'
                + f'<a class="fx-back" href="{"/el/festivals/" if is_el else "/festivals/"}">&larr; {"Όλες οι γιορτές των νησιών" if is_el else "All island festivals"}</a>\n</main>\n'
                + FOOTER.format(
                    lang_link=(path_en if is_el else path_el),
                    lang_label=('English' if is_el else 'Ελληνικά'),
                    privacy=('/el/privacy/' if is_el else '/privacy/'),
                    privacy_label=('Απόρρητο' if is_el else 'Privacy')))
        out = ROOT / (path_el if is_el else path_en).strip('/')
        out.mkdir(parents=True, exist_ok=True)
        (out / 'index.html').write_text(html, encoding='utf-8')
    return [('/festivals/ikaria-panigiria/', '/el/festivals/ikaria-panigiria/')]


def patch_sitemap(pairs):
    sm_path = ROOT / 'sitemap.xml'
    sm = sm_path.read_text(encoding='utf-8')
    today = date.today().isoformat()
    blocks = []
    for en, el in pairs:
        if SITE_URL + en in sm:
            continue
        for path, other in ((en, el), (el, en)):
            blocks.append(
                f'  <url>\n    <loc>{SITE_URL}{path}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>0.6</priority>\n'
                f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE_URL}{en}"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="el" href="{SITE_URL}{el}"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE_URL}{en}"/>\n  </url>')
    if blocks:
        sm = sm.replace('</urlset>', '\n'.join(blocks) + '\n</urlset>')
        sm_path.write_text(sm, encoding='utf-8')
    return len(blocks)


def main():
    fests, names = collect()
    pairs = build_month_hubs(fests, names)
    pairs += build_ikaria()
    n = patch_sitemap(pairs)
    print(f'✓ Festival extras: {len(pairs)} page pairs ({len(pairs) * 2} pages), {n} sitemap entries added')


if __name__ == '__main__':
    sys.exit(main())
