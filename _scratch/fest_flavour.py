#!/usr/bin/env python3
"""Festivals hub with more panigiri and less spreadsheet (Oct 2026): night hero with string lights and
flags, island picker inside it; the year as 12 bars; islands grouped by sea; a short 'what to expect'
panel that covers saint's-day panigiria and the festivals with no saint (wine, ouzo, music...); cards
get a tear-off date tab and an icon per kind. Patches tools/build_festivals.py."""
from pathlib import Path
import sys
R = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
P = R / 'tools/build_festivals.py'
s = P.read_text(encoding='utf-8')
def sub(a, b):
    global s
    if b in s: print('  already'); return
    assert s.count(a) == 1, a[:80]; s = s.replace(a, b); print('  ok')

# icons per kind + month tabs
sub("""GEN_EL = {}   # island""", """TYPE_ICON = {'panigiri': '💃', 'religious': '⛪', 'food': '🍷', 'music': '🎻', 'cultural': '🎭',
             'carnival': '🎉', 'sport': '🏃', 'other': '✨'}
MON_TAB_EN = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
MON_TAB_EL = ['ΙΑΝ', 'ΦΕΒ', 'ΜΑΡ', 'ΑΠΡ', 'ΜΑΪ', 'ΙΟΥΝ', 'ΙΟΥΛ', 'ΑΥΓ', 'ΣΕΠ', 'ΟΚΤ', 'ΝΟΕ', 'ΔΕΚ']
MON_SHORT_EL = ['Ιαν', 'Φεβ', 'Μαρ', 'Απρ', 'Μάι', 'Ιούν', 'Ιούλ', 'Αύγ', 'Σεπ', 'Οκτ', 'Νοέ', 'Δεκ']
GROUPS = [('Cyclades', 'Κυκλάδες'), ('Dodecanese', 'Δωδεκάνησα'), ('Ionian', 'Ιόνιο'), ('NE Aegean', 'Βορειοανατολικό Αιγαίο'),
          ('Saronic', 'Σαρωνικός'), ('Sporades', 'Σποράδες'), ('Crete', 'Κρήτη'), ('Evia', 'Εύβοια'), ('Other', 'Άλλα νησιά')]
FLAG_COLORS = ['#1f5fa8', '#f2c230', '#d9452b', '#ffffff', '#2a9d6f']


def _sag(t, y0, sag):
    return (1 - t) ** 2 * y0 + 2 * (1 - t) * t * (y0 + 2 * sag) + t * t * y0


def bunting_svg(w=1200, n=30, sag=16, y0=4, size=13, cls='fv-bunt'):
    h = y0 + sag + size * 1.4 + 4
    out = [f'<svg class="{cls}" viewBox="0 0 {w} {h:.0f}" preserveAspectRatio="xMidYMin slice" aria-hidden="true">',
           f'<path d="M0,{y0} Q{w / 2},{y0 + 2 * sag} {w},{y0}" fill="none" stroke="#8a7a62" stroke-width="1.2"/>']
    for i in range(n):
        t = (i + .5) / n; x = t * w; y = _sag(t, y0, sag)
        out.append(f'<path d="M{x - size * .55:.1f},{y:.1f}L{x + size * .55:.1f},{y:.1f}L{x:.1f},{y + size * 1.25:.1f}Z" fill="{FLAG_COLORS[i % 5]}" stroke="rgba(0,0,0,.15)" stroke-width=".5"/>')
    return ''.join(out) + '</svg>'


def lights_svg(w=1200, n=24, sag=24, y0=8):
    out = [f'<svg class="fv-lights" viewBox="0 0 {w} {y0 + sag + 18}" preserveAspectRatio="xMidYMin slice" aria-hidden="true">',
           f'<path d="M0,{y0} Q{w / 2},{y0 + 2 * sag} {w},{y0}" fill="none" stroke="rgba(255,255,255,.28)" stroke-width="1"/>']
    for i in range(n):
        t = (i + .5) / n; x = t * w; y = _sag(t, y0, sag) + 4
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="#ffd27a" opacity=".2"/><circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="#ffe7a8"/>')
    return ''.join(out) + '</svg>'


GEN_EL = {}   # island""")

# icon in the type badge
sub("""    return f'<span class="fv-type fv-type-{esc(t)}">{esc(lab)}</span>'""",
    """    return f'<span class="fv-type fv-type-{esc(t)}"><span aria-hidden="true">{TYPE_ICON.get(t, "✨")}</span> {esc(lab)}</span>'""")

# date tab on the card
sub("""    return (f'<article class="fv-card" id="{id_prefix}{esc(f["slug"])}" data-island="{f["island"]}" data-type="{esc(f.get("type") or "other")}"'
            f' data-months="{",".join(str(m) for m in f["months"])}"{date_attrs}>'
            f'{photo}<div class="fv-body">'""",
    """    tab = ''
    if f['start']:
        tab = (f'<div class="fv-tab" aria-hidden="true"><span>{(MON_TAB_EL if is_el else MON_TAB_EN)[f["start"].month - 1]}</span>'
               f'<b>{f["start"].day}</b></div>')
    return (f'<article class="fv-card" id="{id_prefix}{esc(f["slug"])}" data-island="{f["island"]}" data-type="{esc(f.get("type") or "other")}"'
            f' data-months="{",".join(str(m) for m in f["months"])}"{date_attrs}>'
            f'{photo}<div class="fv-body{" has-tab" if tab else ""}">{tab}'""")

# CSS
sub("""@media(max-width:700px){.fv-controls{position:static}}""", """/* panigiri flavour (Oct 2026) */
.fv-hero{position:relative;margin:-26px -22px 30px;padding:0 22px 30px;color:#fff;text-align:center;overflow:hidden;border-radius:0 0 22px 22px;
  background:radial-gradient(ellipse at 50% 125%,rgba(150,70,40,.75) 0%,transparent 55%),linear-gradient(180deg,#10213a 0%,#1d2c4f 55%,#2a1d3a 100%)}
.fv-hero svg{display:block;width:calc(100% + 44px);margin:0 -22px;height:auto}
.fv-hero .fv-bunt{margin-top:-30px}
.fv-hero h1{font:800 12px/1.4 var(--font-ui,sans-serif);letter-spacing:.16em;text-transform:uppercase;color:#ffcf7a;margin:6px 0 6px}
.fv-hero-t{font-family:var(--font-display,Georgia),serif;font-size:40px;font-weight:700;line-height:1.1;margin:0 0 10px;text-wrap:balance}
.fv-hero .fv-lede{color:#e7e2f0;margin:0 auto 16px;max-width:660px}
.fv-hero .fv-stats{justify-content:center;gap:8px;color:#e7e2f0;margin:0 0 18px}
.fv-hero .fv-stats span{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:999px;padding:5px 12px}
.fv-hero .fv-stats b{color:#ffcf7a}
.fv-hero .fv-pick{max-width:600px;margin:0 auto;background:#fff;border:0;border-radius:16px;padding:14px 16px;box-shadow:0 8px 28px rgba(0,0,0,.35);text-align:left;color:var(--ink,#1A2332)}
.fv-hero .fv-pick label{font-size:18px}
.fv-hero .fv-pick button{background:#e8552b}
html.dark .fv-hero .fv-pick{background:#1F2530;color:#E8EDF2}
.fv-bars{display:flex;align-items:flex-end;gap:8px;height:170px;padding:0 2px;border-bottom:2px solid var(--border,#EAE4DC);margin:14px 0 30px}
.fv-bars>*{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;text-decoration:none;color:var(--ink-3,#637080);position:relative}
.fv-bars i{display:block;width:100%;border-radius:8px 8px 3px 3px;background:linear-gradient(180deg,#f3b85b,#e07a3a);transition:filter .15s}
.fv-bars a:hover i{filter:brightness(1.08) saturate(1.2)}
.fv-bars b{font-size:12px;font-weight:700;margin-bottom:3px}
.fv-bars em{position:absolute;bottom:-24px;font-style:normal;font-size:12.5px;font-weight:800;color:var(--ink,#1A2332);padding:0 6px;border-radius:8px}
.fv-bars .pk i{background:linear-gradient(180deg,#ffcf5a,#d9452b)} .fv-bars .pk b{color:#d9452b;font-weight:800}
.fv-bars .now em{background:var(--primary,#0B8FAC);color:#fff}
.fv-section>.fv-bunt{display:block;width:100%;height:auto;max-height:30px;margin:4px 0 0;opacity:.9}
.fv-groups{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:4px 28px}
.fv-group h3{margin:12px 0 6px;font:800 11.5px var(--font-ui,sans-serif);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3,#637080)}
.fv-group div{display:flex;flex-wrap:wrap;gap:6px}
.fv-group a{display:inline-flex;align-items:baseline;gap:5px;background:var(--white,#fff);border:1px solid var(--border,#EAE4DC);border-radius:999px;padding:4px 12px;font-weight:700;color:var(--ink,#1A2332);text-decoration:none}
.fv-group a:hover{border-color:#e07a3a}
.fv-group a small{color:#c46a2c;font-size:11px;font-weight:800}
.fv-what{position:relative;overflow:hidden;background:linear-gradient(135deg,#1d2c4f,#2a1d3a);color:#fff;border-radius:18px;padding:0 26px 22px;margin:0 0 36px}
.fv-what svg{display:block;width:calc(100% + 52px);margin:0 -26px 6px;height:auto}
.fv-what h2{font-family:var(--font-display,Georgia),serif;font-size:22px;margin:0 0 8px;color:#ffcf7a}
.fv-what p{margin:0 0 8px;font-size:15.5px;line-height:1.6;color:#ece7f3;max-width:820px}
.fv-what a{color:#ffcf7a;font-weight:800}
.fv-body.has-tab{display:grid;grid-template-columns:50px minmax(0,1fr);grid-template-rows:auto auto auto 1fr auto;column-gap:12px;row-gap:4px}
.fv-body.has-tab>*:not(.fv-tab){grid-column:2}
.fv-tab{grid-column:1;grid-row:1/span 4;align-self:start;border:1px solid var(--border,#EAE4DC);border-radius:10px;overflow:hidden;text-align:center;background:var(--white,#fff)}
.fv-tab span{display:block;background:#d9452b;color:#fff;font:800 10px/1.6 var(--font-ui,sans-serif);letter-spacing:.06em}
.fv-tab b{display:block;font-family:var(--font-display,Georgia),serif;font-size:24px;line-height:1.3;color:var(--ink,#1A2332)}
html.dark .fv-tab{background:#1F2530;border-color:#2C3542} html.dark .fv-tab b{color:#E8EDF2}
html.dark .fv-group a{background:#1F2530;border-color:#2C3542;color:#E8EDF2}
@media(max-width:600px){.fv-hero{margin:-18px -14px 24px;padding:0 14px 22px}.fv-hero svg{width:calc(100% + 28px);margin:0 -14px}.fv-hero .fv-bunt{margin-top:-22px}
  .fv-hero-t{font-size:29px}.fv-bars{gap:3px;height:130px}.fv-bars b{font-size:10px}.fv-bars em{font-size:10.5px;padding:0 3px}
  .fv-groups{grid-template-columns:1fr}.fv-what{padding:0 18px 18px}.fv-what svg{width:calc(100% + 36px);margin:0 -18px 6px}}
@media(max-width:700px){.fv-controls{position:static}}""")

# current month on the bars
sub("""  var pick=q('#fv-pick'),go=q('#fv-pick-go');""", """  var mb=q('.fv-bars [data-m="'+(new Date().getMonth()+1)+'"]');if(mb)mb.classList.add('now');
  var pick=q('#fv-pick'),go=q('#fv-pick-go');""")

# helpers before build_hub
sub("""# --------------------------------------------------------------------------- pages
def build_hub(flat, names, heroes):""", """def year_bars(lang, counts):
    p = '/el/festivals/' if lang == 'el' else '/festivals/'
    mx = max(counts.values()) if counts else 1
    out = []
    for m in range(1, 13):
        n = counts.get(m, 0)
        lab = MON_SHORT_EL[m - 1] if lang == 'el' else MONTHS_EN[m - 1][:3]
        cls = ' class="pk"' if n == mx else ''
        bar = f'<b>{n or ""}</b><i style="height:{max(3, round(n / mx * 120))}px"></i><em>{lab}</em>'
        title = (MONTHS_EL_NOM[m - 1] if lang == 'el' else MONTHS_EN[m - 1]) + f': {n}'
        out.append(f'<a{cls} data-m="{m}" href="{p}{MONTH_SLUG[m]}/" title="{title}">{bar}</a>' if n
                   else f'<span data-m="{m}">{bar}</span>')
    return '<nav class="fv-bars" aria-label="months">' + ''.join(out) + '</nav>'


def island_groups(lang, per_island, names):
    is_el = lang == 'el'
    p = '/el' if is_el else ''
    dest = _market.destinations()
    by = {}
    for k in per_island:
        by.setdefault((dest.get(k) or {}).get('island_group') or 'Other', []).append(k)
    out = []
    for g, g_el in GROUPS + [(x, x) for x in sorted(by) if x not in dict(GROUPS)]:
        ks = sorted(by.get(g, []), key=lambda k: names[k][1 if is_el else 0])
        if not ks:
            continue
        chips = ''.join(f'<a href="{p}/festivals/{k}/" style="font-size:{13 + min(len(per_island[k]), 25) * .2:.1f}px">'
                        f'{esc(names[k][1 if is_el else 0])}<small>{len(per_island[k])}</small></a>' for k in ks)
        out.append(f'<div class="fv-group"><h3>{g_el if is_el else g}</h3><div>{chips}</div></div>')
    return '<div class="fv-groups">' + ''.join(out) + '</div>'


def what_panel(lang):
    p = '/el' if lang == 'el' else ''
    return ('<section class="fv-what">' + lights_svg(n=20, sag=14) + '<h2>' + L(lang, 'What to expect', 'Τι να περιμένεις') + '</h2><p>' + L(lang,
        'Most of these are <b>panigiria</b>: a village keeping its saint\\'s day. Vespers at the church in the evening, then long tables in the square, '
        'goat or fish, local wine, violin and lute until the sun comes up. Nobody checks whether you are from the village; sit down, order, dance when the circle opens.',
        'Τα περισσότερα είναι <b>πανηγύρια</b>: ένα χωριό γιορτάζει τον άγιό του. Εσπερινός στην εκκλησία το βράδυ, μετά μεγάλα τραπέζια στην πλατεία, '
        'κατσίκι ή ψάρι, ντόπιο κρασί, βιολί και λαούτο ως το ξημέρωμα. Κανείς δεν ρωτάει αν είσαι από το χωριό· κάτσε, παράγγειλε, μπες στον χορό όταν ανοίξει ο κύκλος.')
        + '</p><p>' + L(lang,
        'The rest have no saint attached: wine, ouzo, fish and harvest festivals, carnival, music and theatre nights. Same long tables, often bigger crowds. '
        f'For the full picture, read <a href="{p}/festivals/ikaria-panigiria/">the panigiria of Ikaria</a>.',
        'Οι υπόλοιπες γιορτές δεν έχουν άγιο: γιορτές κρασιού, ούζου, ψαριού και σοδειάς, αποκριές, βραδιές μουσικής και θεάτρου. Τα ίδια μεγάλα τραπέζια, συχνά με περισσότερο κόσμο. '
        f'Για όλη την εικόνα, διάβασε <a href="{p}/festivals/ikaria-panigiria/">τα πανηγύρια της Ικαρίας</a>.') + '</p></section>')


# --------------------------------------------------------------------------- pages
def build_hub(flat, names, heroes):""")

# hub copy + layout
sub("""            h1 = f'Πανηγύρια & γιορτές στα νησιά, {SEASON_YEAR}'
            lede = (f'{n} πανηγύρια, λιτανείες, γιορτές κρασιού και φεστιβάλ σε {len(per_island)} νησιά — με το χωριό και την ημερομηνία, '
                    'όχι «κάπου τον Αύγουστο». Διάλεξε μήνα ή νησί, φιλτράρισε ανά είδος, και βάλε όσα θέλεις στο ημερολόγιό σου.')""",
    """            h1 = f'Πανηγύρια & γιορτές στα νησιά, {SEASON_YEAR}'
            hero_t = 'Πού χορεύει το νησί απόψε'
            lede = (f'{n} πανηγύρια, λιτανείες και γιορτές κρασιού, ούζου, φαγητού και μουσικής σε {len(per_island)} νησιά — με το χωριό και την ημερομηνία, '
                    'όχι «κάπου τον Αύγουστο».')""")
sub("""            h1 = f'Greek island festivals &amp; panigiria, {SEASON_YEAR}'
            lede = (f'{n} village feasts, processions, wine festivals and summer festivals across {len(per_island)} islands — with the village and the date, '
                    'not "sometime in August". Pick a month or an island, filter by kind, and put the ones you want in your calendar.')""",
    """            h1 = f'Greek island festivals &amp; panigiria, {SEASON_YEAR}'
            hero_t = 'Where the island dances tonight'
            lede = (f'{n} saint\\'s-day panigiria, processions, and wine, ouzo, food and music festivals across {len(per_island)} islands — '
                    'with the village and the date, not "sometime in August".')""")
sub("""        directory = (f'<section class="fv-section" id="islands"><h2>{L(lang, "By island", "Ανά νησί")} <small>{len(per_island)}</small></h2>'
                     f'<div class="fv-dir">{"".join(dir_items)}</div></section>')""",
    """        directory = (f'<section class="fv-section" id="islands"><h2>{L(lang, "By island", "Ανά νησί")} <small>{len(per_island)}</small></h2>'
                     f'{island_groups(lang, per_island, names)}</section>')""")
sub("""        body = (f'<main class="fv-page"><h1>{h1}</h1><p class="fv-lede">{lede}</p>{stats}'
                + picker + directory
                + f'<section class="fv-section" id="bymonth"><h2>{L(lang, "Or browse by month", "Ή ανά μήνα")}</h2>'
                + month_strip(lang, counts, hub=True) + ikaria + '</section>'
                + soon_block(lang)""",
    """        hero = (f'<header class="fv-hero">{lights_svg()}{bunting_svg()}<h1>{h1}</h1><p class="fv-hero-t">{hero_t}</p>'
                f'<p class="fv-lede">{lede}</p>{stats}{picker}</header>')
        body = (f'<main class="fv-page">{hero}'
                + f'<section class="fv-section" id="bymonth"><h2>{L(lang, "The year in festivals", "Η χρονιά σε γιορτές")}</h2>'
                + year_bars(lang, counts) + ikaria + '</section>'
                + directory
                + what_panel(lang)
                + soon_block(lang)""")
P.write_text(s, encoding='utf-8')
print('done')
