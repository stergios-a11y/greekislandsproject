#!/usr/bin/env python3
"""Build /match/ and /el/match/ — the quiz landing page.

Purpose: 'which greek island should I visit' is one of the biggest query
families in the niche, and the quiz (a hash view at /#match) can't rank
because it has no URL. This page is the rankable front door: a real answer
page with the quiz as its CTA, plus honest by-vibe starting points.

Reuses head/header/footer helpers from build_festival_extras.
Patches sitemap.xml — run LAST in the build chain.
"""
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_festival_extras import ROOT, SITE_URL, esc, page_head, header_nav, FOOTER, patch_sitemap  # noqa: E402

YEAR = date.today().year

# By-vibe picks — consistent with the site's own scores.
VIBES = [
    ('🏖', 'Best beaches', 'Οι καλύτερες παραλίες', ['milos', 'elafonisos', 'lefkada', 'koufonisia']),
    ('🤫', 'Peace and quiet', 'Ησυχία και ηρεμία', ['folegandros', 'sikinos', 'anafi', 'kythira']),
    ('👨‍👩‍👧', 'Families', 'Οικογένειες', ['naxos', 'paros', 'skopelos', 'aegina']),
    ('🍷', 'Nightlife', 'Νυχτερινή ζωή', ['mykonos', 'ios', 'paros', 'rhodes']),
    ('🚶', 'No car needed', 'Χωρίς αυτοκίνητο', ['hydra', 'koufonisia', 'symi', 'agistri']),
    ('💸', 'Budget-friendly', 'Οικονομικά', ['ikaria', 'lemnos', 'samothrace', 'thasos']),
    ('🌟', 'First trip to Greece', 'Πρώτο ταξίδι στα νησιά', ['naxos', 'santorini', 'paros', 'milos']),
    ('🏛', 'History and culture', 'Ιστορία και πολιτισμός', ['rhodes', 'patmos', 'corfu', 'chania']),
]

CSS = '''<style>
.mx-page{max-width:1000px;margin:0 auto;padding:26px 22px 50px}
.mx-page h1{font-family:'Alegreya',serif;font-size:32px;margin-bottom:10px}
.mx-intro{color:#2E3D50;font-size:16px;line-height:1.7;max-width:740px;margin-bottom:18px}
.mx-cta{display:inline-block;background:#E8522A;color:#fff;font-family:'Nunito',sans-serif;font-weight:800;font-size:17px;padding:14px 30px;border-radius:14px;text-decoration:none;box-shadow:0 8px 26px rgba(232,82,42,.35)}
.mx-cta small{display:block;font-size:12px;font-weight:700;opacity:.9}
.mx-sub{font-size:13px;color:#637080;margin-top:10px}
.mx-page h2{font-family:'Alegreya',serif;font-size:23px;margin:34px 0 14px}
.mx-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px}
.mx-card{background:#fff;border-radius:14px;box-shadow:0 4px 18px rgba(26,35,50,.09);padding:15px 17px}
.mx-card h3{font-size:15px;font-weight:800;margin:0 0 8px;color:#1A2332}
.mx-card a{display:inline-block;font-size:13.5px;font-weight:700;color:#076880;text-decoration:none;margin:2px 10px 2px 0}
.mx-card a:hover{text-decoration:underline}
.mx-how{max-width:740px;font-size:15px;line-height:1.7;color:#2E3D50}
.mx-how p{margin:0 0 14px}
</style>'''


def island_names():
    names = {}
    for f in sorted((ROOT / 'islands').glob('*.json')):
        d = json.loads(f.read_text(encoding='utf-8'))
        names[d['key']] = (d.get('name') or d['key'].title(), d.get('name_el') or d.get('name') or d['key'])
    return names


def build(lang, names):
    is_el = lang == 'el'
    path_en, path_el = '/match/', '/el/match/'
    if is_el:
        # Brand suffix dropped and the payload tightened: 92 chars meant Google
        # truncated the part that sells the click.
        title = f'Ποιο ελληνικό νησί σού ταιριάζει; Quiz 60 δευτ. ({YEAR})'
        desc = 'Οκτώ γρήγορες ερωτήσεις — παραλίες, κόστος, πόσο χρόνο έχεις — και παίρνεις τα νησιά που σού ταιριάζουν, με βαθμολογίες.'
        h1 = 'Ποιο ελληνικό νησί σού ταιριάζει;'
        intro = ('Υπάρχουν 83 κατοικημένα νησιά και οι περισσότεροι οδηγοί σού λένε «όλα υπέροχα». Εδώ κάθε νησί έχει ειλικρινή βαθμολογία σε παραλίες, πολιτισμό, νυχτερινή ζωή, πρόσβαση και τιμές — '
                 'οπότε το ταίριασμα γίνεται με πραγματικά κριτήρια, όχι με διαφημιστικά.')
        cta_label, cta_small = 'Κάνε το quiz', '~60 δευτερόλεπτα · 3 προτάσεις με βαθμολογία'
        cta_href = '/el/#match'
        or_h2 = 'Ή ξεκίνα από αυτό που ψάχνεις'
        how_h2 = 'Πώς δουλεύει το quiz'
        how = ('<p>Απαντάς σε λίγες γρήγορες ερωτήσεις — τι σημασία έχουν για σένα οι παραλίες, το κόστος, η νυχτερινή ζωή, ο ρυθμός του ταξιδιού — και ο αλγόριθμος συγκρίνει τις απαντήσεις σου με τις βαθμολογίες και των 83 νησιών. '
               'Παίρνεις τα 3 καλύτερα ταιριάσματα, με τους βαθμούς τους, και από εκεί ο πλήρης οδηγός κάθε νησιού: πρόγραμμα ημερών, παραλίες, πού να φας.</p>'
               '<p>Οι βαθμολογίες δεν βγαίνουν από αλγόριθμο ούτε από το TripAdvisor — είναι η κρίση ενός ανθρώπου που έχει πάει στα περισσότερα, εξηγημένη δημόσια στη σελίδα <a href="/el/#mission" style="color:#076880">Στόχος</a>. '
               f'Και όταν διαλέξεις, το <a href="/el/trip-cost/" style="color:#076880">Κόστος</a> σού δείχνει τι θα κοστίσει το ταξίδι — ενημερωμένο για το {YEAR}.</p>')
    else:
        title = f'Which Greek Island Should You Visit? 60-Second Quiz ({YEAR})'
        desc = 'Eight quick questions — beaches, budget, how long you have — and you get the islands that actually fit, scored and ranked.'
        h1 = 'Which Greek island should you visit?'
        intro = ('There are 83 inhabited islands and most guides call all of them wonderful. Here, every island carries an honest score across beaches, culture, nightlife, access and price — '
                 'so the matching runs on real criteria, not marketing copy.')
        cta_label, cta_small = 'Take the quiz', '~60 seconds · 3 scored matches'
        cta_href = '/#match'
        or_h2 = 'Or start from what you want'
        how_h2 = 'How the quiz works'
        how = ('<p>You answer a few quick questions — how much beaches matter, your budget, whether nightlife is a feature or a bug, the pace you travel at — and the matcher compares your answers against the scores of all 83 islands. '
               'You get your 3 best matches with their numbers, and from there each island’s full guide: day plan, beaches, where to eat.</p>'
               '<p>The scores aren’t computed by an algorithm or scraped from TripAdvisor — they’re one person’s informed judgment, explained openly on the <a href="/#mission" style="color:#076880">Mission</a> page. '
               f'And once you’ve picked, the <a href="/trip-cost/" style="color:#076880">Budget planner</a> shows what the trip will actually cost — updated for {YEAR}.</p>')

    cards = ''
    for icon, en_label, el_label, keys in VIBES:
        label = el_label if is_el else en_label
        links = ' '.join(
            f'<a href="{"/el" if is_el else ""}/island/{k}/">{esc(names[k][1 if is_el else 0])}</a>'
            for k in keys if k in names)
        cards += f'<div class="mx-card"><h3>{icon} {esc(label)}</h3>{links}</div>\n'

    html = (page_head(title, desc, path_en, path_el, lang)
            + header_nav(lang, (path_en if is_el else path_el), active='match')
            + CSS
            + f'''<main class="mx-page">
<h1>{esc(h1)}</h1>
<p class="mx-intro">{intro}</p>
<a class="mx-cta" href="{cta_href}">🎯 {esc(cta_label)}<small>{esc(cta_small)}</small></a>
<h2>{esc(or_h2)}</h2>
<div class="mx-grid">
{cards}</div>
<h2>{esc(how_h2)}</h2>
<div class="mx-how">{how}</div>
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


def main():
    names = island_names()
    for lang in ('en', 'el'):
        build(lang, names)
    n = patch_sitemap([('/match/', '/el/match/')])
    print(f'✓ Match landing built: /match/ + /el/match/ ({n} sitemap entries added)')


if __name__ == '__main__':
    sys.exit(main())
