#!/usr/bin/env python3
"""Festival pages, built from festivals.json (the master list).

Produces, EN + EL:
  /festivals/                  hub: highlights per month, island directory, "happening soon"
  /festivals/<month>/          every festival in that month, grouped by day, filterable
  /festivals/<island>/         every festival on that island (islands with >= 3), chronological
  /festivals/ics/<island>.ics  calendar bundle per island
  /festivals/ics/<island>/<slug>.ics   one .ics per festival with an exact date
  /festivals-index.json        {island: count} for the SPA's "all N festivals" link
Also patches sitemap.xml (BEGIN/END FESTIVAL block) and writes Event JSON-LD.

Dates: festivals.json carries structured dates (see tools/festival_schema.md);
tools/feasts.py resolves them for SEASON_YEAR — the year of the next 15 August —
so the whole section rolls over to the coming season automatically.

Run AFTER prerender.py (which regenerates sitemap.xml) and after
build_festival_extras.py (Ikaria article, shared head/nav helpers).
"""
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from feasts import resolve, human_when, MONTHS_EN, MONTHS_EL_NOM, MONTHS_EL_GEN  # noqa: E402
from build_festival_extras import (SITE_URL, esc, page_head, header_nav, FOOTER, MONTHS,  # noqa: E402
                                   slugify)

TODAY = date.today()
# The season we are selling: this year's until 15 August, then next year's.
SEASON_YEAR = TODAY.year if (TODAY.month, TODAY.day) <= (8, 15) else TODAY.year + 1

MONTH_SLUG = {i + 1: m[0] for i, m in enumerate(MONTHS)}
MONTH_ACC_EL = {i + 1: m[3] for i, m in enumerate(MONTHS)}   # "τον Αύγουστο"

TYPES = {
    'panigiri':  ('Panigiri', 'Πανηγύρι'),
    'religious': ('Religious', 'Θρησκευτική'),
    'food':      ('Food & harvest', 'Γαστρονομία'),
    'music':     ('Music', 'Μουσική'),
    'cultural':  ('Arts & culture', 'Πολιτισμός'),
    'carnival':  ('Carnival', 'Αποκριές'),
    'sport':     ('Sport', 'Αθλητική'),
    'other':     ('Other', 'Άλλο'),
}


GEN_EL = {}   # island -> Greek genitive without article ('Μήλου'), from islands/*.json name_genitive_el
_MASC = {'poros', 'kalamos', 'agios-efstratios'}


def gen_with_article(key, name_el):
    """'της Μήλου' / 'του Πόρου' / 'των Κυθήρων' — article inferred from the name."""
    g = GEN_EL.get(key)
    if not g:
        return ''
    if g.endswith('ων'):
        art = 'των'
    elif key in _MASC or name_el.endswith(('ο', 'ι')):
        art = 'του'
    else:
        art = 'της'
    return f'{art} {g}'


def L(lang, en, el):
    return el if lang == 'el' else en


# --------------------------------------------------------------------------- data
def load():
    fests = json.loads((ROOT / 'festivals.json').read_text(encoding='utf-8'))
    names, heroes = {}, {}
    for p in sorted((ROOT / 'islands').glob('*.json')):
        d = json.loads(p.read_text(encoding='utf-8'))
        names[d['key']] = (d.get('name') or d['key'].title(), d.get('name_el') or d.get('name') or d['key'])
        heroes[d['key']] = d.get('hero_photo') or ''
        GEN_EL[d['key']] = d.get('name_genitive_el') or ''
    flat = []
    for isl, lst in fests.items():
        for i, e in enumerate(lst):
            r = resolve(e.get('date'), SEASON_YEAR, e.get('eve'), e.get('duration_days'))
            f = dict(e)
            f['island'] = isl
            f['start'], f['end'], f['months'], f['exact'] = r['start'], r['end'], r['months'], r['exact']
            f['slug'] = slugify(e.get('village', '') + '-' + e.get('name', '')) or f'festival-{i}'
            f['when_en'] = human_when(e.get('date'), SEASON_YEAR, e.get('eve'), e.get('duration_days'), 'en',
                                      e.get('when') or e.get('date', {}).get('approx'))
            f['when_el'] = human_when(e.get('date'), SEASON_YEAR, e.get('eve'), e.get('duration_days'), 'el',
                                      e.get('when_el') or e.get('when') or e.get('date', {}).get('approx'))
            # sort: exact dates by day, approx at the start of their first month
            f['sort'] = (f['start'].toordinal() if f['start'] else date(SEASON_YEAR, f['months'][0], 1).toordinal() - 0.5)
            flat.append(f)
    # unique slugs per island
    seen = {}
    for f in flat:
        k = (f['island'], f['slug'])
        if k in seen:
            seen[k] += 1
            f['slug'] = f"{f['slug']}-{seen[k]}"
        else:
            seen[k] = 1
    flat.sort(key=lambda f: (f['sort'], f['island'], f['name']))
    return flat, names, heroes


# --------------------------------------------------------------------------- pieces
def gcal_link(f, lang, names):
    if not f['start']:
        return ''
    s = f['start'].strftime('%Y%m%d')
    e = (f['end'] + timedelta(days=1)).strftime('%Y%m%d')
    name = f['name_el'] if lang == 'el' and f.get('name_el') else f['name']
    iname = names[f['island']][1 if lang == 'el' else 0]
    loc = ', '.join(x for x in (f.get('village_el') if lang == 'el' else f.get('village'), iname, 'Greece') if x)
    details = f"{SITE_URL}{'/el' if lang == 'el' else ''}/festivals/{f['island']}/"
    return ('https://calendar.google.com/calendar/render?action=TEMPLATE&text=' + quote(name)
            + f'&dates={s}/{e}&location=' + quote(loc) + '&details=' + quote(details))


def type_badge(f, lang):
    t = f.get('type') or 'other'
    lab = TYPES.get(t, TYPES['other'])[1 if lang == 'el' else 0]
    return f'<span class="fv-type fv-type-{esc(t)}">{esc(lab)}</span>'


def card(f, names, lang, show_island=True, heading='h3'):
    is_el = lang == 'el'
    name = f.get('name_el') if is_el and f.get('name_el') else f['name']
    desc = f.get('desc_el') if is_el and f.get('desc_el') else f.get('desc', '')
    when = f['when_el'] if is_el else f['when_en']
    village = f.get('village_el') if is_el and f.get('village_el') else f.get('village', '')
    iname = names[f['island']][1 if is_el else 0]
    p = '/el' if is_el else ''
    island_line = ''
    if show_island:
        island_line = f'<a class="fv-island" href="{p}/festivals/{f["island"]}/">{esc(iname)}</a>'
    if village and village.lower() in name.lower():
        village = ''   # already in the name ("Panigiri of Agia Marina, Triovasalos")
    village_html = f'<span class="fv-village">{esc(village)}</span>' if village else ''
    date_attrs = ''
    if f['start']:
        date_attrs = f' data-start="{f["start"].isoformat()}" data-end="{f["end"].isoformat()}"'
        if SEASON_YEAR != TODAY.year and 'fixed' in (f.get('date') or {}):
            rn = resolve(f['date'], TODAY.year, f.get('eve'), f.get('duration_days'))
            if rn['start']:
                date_attrs += f' data-start-now="{rn["start"].isoformat()}" data-end-now="{rn["end"].isoformat()}"'
    actions = []
    if f['start']:
        actions.append(f'<a class="fv-act" href="/festivals/ics/{f["island"]}/{f["slug"]}.ics" download>'
                       f'{L(lang, "＋ Calendar (.ics)", "＋ Ημερολόγιο (.ics)")}</a>')
        actions.append(f'<a class="fv-act" href="{esc(gcal_link(f, lang, names))}" target="_blank" rel="noopener">Google</a>')
    if f.get('source'):
        actions.append(f'<a class="fv-act fv-src" href="{esc(f["source"])}" target="_blank" rel="noopener nofollow">'
                       f'{L(lang, "source", "πηγή")}</a>')
    unverified = ''
    if f.get('confidence') == 'medium':
        unverified = f'<span class="fv-check" title="{esc(L(lang, "Reported for recent years; confirm locally before travelling", "Από πρόσφατες χρονιές — επιβεβαίωσε τοπικά πριν ταξιδέψεις"))}">{L(lang, "confirm locally", "επιβεβαίωσε τοπικά")}</span>'
    photo = ''
    if f.get('photo'):
        photo = f'<img class="fv-photo" src="{esc(f["photo"])}" alt="{esc(name)}" loading="lazy">'
    return (f'<article class="fv-card" id="{esc(f["slug"])}" data-island="{f["island"]}" data-type="{esc(f.get("type") or "other")}"'
            f' data-months="{",".join(str(m) for m in f["months"])}"{date_attrs}>'
            f'{photo}<div class="fv-body">'
            f'<div class="fv-top">{island_line}{type_badge(f, lang)}{unverified}</div>'
            f'<{heading} class="fv-name">{esc(name)}</{heading}>'
            f'<p class="fv-when">{esc(when)}{(" · " + village_html) if village_html else ""}</p>'
            f'<p class="fv-desc">{esc(desc)}</p>'
            f'<div class="fv-actions">{"".join(actions)}</div>'
            f'</div></article>')


def event_jsonld(fs, names, lang, heroes):
    events = []
    for f in fs:
        if not f['start']:
            continue
        is_el = lang == 'el'
        iname = names[f['island']][1 if is_el else 0]
        name = f.get('name_el') if is_el and f.get('name_el') else f['name']
        desc = re.sub(r'<[^>]+>', '', f.get('desc_el') if is_el and f.get('desc_el') else f.get('desc', ''))
        village = f.get('village_el') if is_el and f.get('village_el') else f.get('village', '')
        ev = {
            '@context': 'https://schema.org', '@type': 'Event', 'name': name,
            'startDate': f['start'].isoformat(), 'endDate': f['end'].isoformat(),
            'eventStatus': 'https://schema.org/EventScheduled',
            'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode',
            'location': {'@type': 'Place', 'name': f'{village + ", " if village else ""}{iname}, Greece',
                         'address': {'@type': 'PostalAddress', 'addressLocality': village or iname,
                                     'addressRegion': iname, 'addressCountry': 'GR'}},
            'description': desc[:200],
            'url': f"{SITE_URL}{'/el' if is_el else ''}/festivals/{f['island']}/#{f['slug']}",
        }
        img = f.get('photo') or heroes.get(f['island'])
        if img:
            ev['image'] = img
        events.append(ev)
    if not events:
        return ''
    return '<script type="application/ld+json">' + json.dumps(events, ensure_ascii=False, separators=(',', ':')) + '</script>\n'


def breadcrumb_jsonld(lang, crumbs):
    items = [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE_URL + u} for i, (n, u) in enumerate(crumbs)]
    return ('<script type="application/ld+json">' + json.dumps(
        {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items},
        ensure_ascii=False, separators=(',', ':')) + '</script>\n')


CSS = '''<style>
.fv-page{max-width:1060px;margin:0 auto;padding:26px 22px 60px}
.fv-page h1{font-family:var(--serif,Georgia),serif;font-size:34px;line-height:1.15;margin:0 0 8px;text-wrap:balance}
.fv-lede{color:var(--ink-2,#2E3D50);font-size:16px;line-height:1.6;max-width:760px;margin:0 0 18px}
.fv-stats{display:flex;flex-wrap:wrap;gap:8px 18px;font-size:13px;color:var(--ink-3,#637080);margin:0 0 22px}
.fv-stats b{color:var(--ink,#1A2332);font-size:15px}
.fv-strip{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 22px}
.fv-strip a{font-size:13px;font-weight:700;color:var(--aegean-dark,#076880);text-decoration:none;background:var(--aegean-pale,#E8F7FB);border-radius:999px;padding:6px 12px;white-space:nowrap}
.fv-strip a.on{background:var(--aegean,#0B8FAC);color:#fff}
.fv-strip a small{font-weight:600;opacity:.75;margin-left:3px}
.fv-controls{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 20px;position:sticky;top:0;z-index:5;background:var(--marble,#FFFBF5);padding:10px 0;border-bottom:1px solid var(--border,#EAE4DC)}
.fv-controls select,.fv-controls input{font:inherit;font-size:14px;padding:8px 12px;border:1px solid var(--border-2,#D8CEC2);border-radius:10px;background:var(--white,#fff);color:inherit}
.fv-controls input{flex:1;min-width:150px}
.fv-chips{display:flex;flex-wrap:wrap;gap:6px}
.fv-chip{cursor:pointer;font-size:12.5px;font-weight:700;border:1px solid var(--border-2,#D8CEC2);background:var(--white,#fff);color:var(--ink-2,#2E3D50);border-radius:999px;padding:5px 11px}
.fv-chip.on{background:var(--ink,#1A2332);color:var(--white,#fff);border-color:var(--ink,#1A2332)}
.fv-clear{cursor:pointer;border:none;background:none;color:var(--aegean-dark,#076880);font-weight:700;font-size:13px;padding:8px}
.fv-count{font-size:13px;color:var(--ink-3,#637080);margin-left:auto}
.fv-section{margin:0 0 36px}
.fv-section>h2{font-family:var(--serif,Georgia),serif;font-size:24px;margin:0 0 4px;padding-bottom:6px;border-bottom:2px solid var(--aegean,#0B8FAC);display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.fv-section>h2 small{font-size:14px;font-weight:600;color:var(--ink-3,#637080)}
.fv-section>h2 a.fv-more{margin-left:auto;font-size:13.5px;color:var(--aegean-dark,#076880);text-decoration:none;font-weight:700}
.fv-day{font-size:13px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;color:var(--ink-3,#637080);margin:18px 0 8px}
.fv-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}
.fv-card{display:flex;flex-direction:column;background:var(--white,#fff);border:1px solid var(--border,#EAE4DC);border-radius:12px;overflow:hidden}
.fv-card.is-hidden,.fv-section.is-hidden,.fv-day.is-hidden{display:none!important}
.fv-photo{width:100%;height:150px;object-fit:cover}
.fv-body{padding:14px 16px 12px;display:flex;flex-direction:column;gap:4px;flex:1}
.fv-top{display:flex;gap:8px;align-items:center;flex-wrap:wrap;font-size:11.5px}
.fv-island{font-weight:800;color:var(--aegean-dark,#076880);text-decoration:none;text-transform:uppercase;letter-spacing:.05em}
.fv-type{font-weight:700;border-radius:999px;padding:2px 8px;background:var(--ink-5,#E4E8ED);color:var(--ink-2,#2E3D50)}
.fv-type-panigiri{background:var(--terra-pale,#FDEDE7);color:#B4432F}
.fv-type-religious{background:var(--aegean-pale,#E8F7FB);color:var(--aegean-dark,#076880)}
.fv-type-food{background:var(--olive-pale,#E8F6F1);color:#2F7A4E}
.fv-type-carnival{background:#F3E8FA;color:#6B3FA0}
.fv-type-music,.fv-type-cultural{background:#FFF3D6;color:#8A5A00}
.fv-check{font-weight:700;color:var(--ink-3,#637080);border-bottom:1px dotted currentColor;cursor:help}
.fv-name{font-family:var(--serif,Georgia),serif;font-size:18px;line-height:1.25;margin:2px 0 0}
.fv-when{font-size:13.5px;font-weight:800;color:#C6421F;margin:0}
.fv-village{font-weight:600;color:var(--ink-3,#637080)}
.fv-desc{font-size:14px;line-height:1.55;color:var(--ink-2,#2E3D50);margin:2px 0 0}
.fv-actions{display:flex;flex-wrap:wrap;gap:6px 12px;margin-top:auto;padding-top:10px;font-size:12.5px}
.fv-act{font-weight:700;color:var(--aegean-dark,#076880);text-decoration:none}
.fv-src{color:var(--ink-3,#637080);font-weight:600}
.fv-soon{margin:0 0 34px}
.fv-tag{display:inline-block;font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.05em;color:#fff;background:var(--aegean,#0B8FAC);border-radius:999px;padding:2px 9px}
.fv-tag.next{background:var(--ink-3,#637080)}
.fv-dir{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:8px}
.fv-dir a{display:flex;justify-content:space-between;gap:8px;padding:10px 12px;border:1px solid var(--border,#EAE4DC);border-radius:10px;background:var(--white,#fff);text-decoration:none;color:var(--ink,#1A2332);font-weight:700;font-size:14px}
.fv-dir a span{color:var(--ink-3,#637080);font-weight:600}
.fv-note{font-size:13.5px;color:var(--ink-3,#637080);line-height:1.55;max-width:760px;margin:26px 0 0;padding-top:14px;border-top:1px dashed var(--border-2,#D8CEC2)}
.fv-cta{display:inline-block;font-size:13px;font-weight:800;color:var(--aegean-dark,#076880);text-decoration:none;background:var(--aegean-pale,#E8F7FB);border-radius:999px;padding:7px 14px;margin:0 8px 8px 0}
.fv-noresults{display:none;padding:24px;text-align:center;color:var(--ink-3,#637080)}
.fv-cal{width:100%;border-collapse:collapse;font-size:14px;margin:0 0 24px}
.fv-cal td{padding:8px 10px 8px 0;border-bottom:1px dashed var(--border-2,#D8CEC2);vertical-align:top}
.fv-cal td:first-child{white-space:nowrap;font-weight:800;color:#C6421F;width:150px}
.fv-cal a{color:inherit;text-decoration:none;font-weight:700}
@media(max-width:700px){.fv-controls{position:static}}
@media(max-width:600px){.fv-page{padding:18px 14px 44px}.fv-page h1{font-size:27px}.fv-grid{grid-template-columns:1fr}.fv-cal td:first-child{width:110px}}
html.dark .fv-type-panigiri{background:#3A2320;color:#E8877A}
html.dark .fv-type-food{background:#1D3327;color:#7CC496}
html.dark .fv-type-carnival{background:#2A1F3A;color:#C9A6F0}
html.dark .fv-type-music,html.dark .fv-type-cultural{background:#372F16;color:#D9BB4A}
html.dark .fv-when,html.dark .fv-cal td:first-child{color:#F07050}
</style>'''

FILTER_JS = r'''<script>
(function(){
  var q=function(s,r){return (r||document).querySelector(s)},qa=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
  var cards=qa('.fv-card'),islSel=q('#fv-island'),typeChips=qa('.fv-chip'),search=q('#fv-q'),clearBtn=q('#fv-clear'),countEl=q('#fv-count'),noRes=q('#fv-noresults');
  var type='';
  function apply(){
    var isl=islSel?islSel.value:'',s=(search?search.value:'').trim().toLowerCase(),n=0;
    cards.forEach(function(c){
      var ok=(!isl||c.getAttribute('data-island')===isl)&&(!type||c.getAttribute('data-type')===type)&&(!s||c.textContent.toLowerCase().indexOf(s)>-1);
      c.classList.toggle('is-hidden',!ok);if(ok)n++;
    });
    qa('.fv-day').forEach(function(d){var el=d.nextElementSibling;d.classList.toggle('is-hidden',!el||!qa('.fv-card:not(.is-hidden)',el).length)});
    qa('.fv-section[data-auto]').forEach(function(sec){sec.classList.toggle('is-hidden',!qa('.fv-card:not(.is-hidden)',sec).length)});
    if(countEl)countEl.textContent=n;
    if(noRes)noRes.style.display=n?'none':'block';
  }
  if(islSel)islSel.addEventListener('change',apply);
  if(search)search.addEventListener('input',apply);
  typeChips.forEach(function(ch){ch.addEventListener('click',function(){var v=ch.getAttribute('data-type');type=(type===v)?'':v;typeChips.forEach(function(x){x.classList.toggle('on',x.getAttribute('data-type')===type)});apply();})});
  if(clearBtn)clearBtn.addEventListener('click',function(){if(islSel)islSel.value='';if(search)search.value='';type='';typeChips.forEach(function(x){x.classList.remove('on')});apply();});
  // Happening now & soon: real dates, 21-day window, plus a "next up" tail.
  var soon=q('#fv-soon'),soonGrid=q('#fv-soon-grid');
  if(soon&&soonGrid){
    var now=new Date();now.setHours(0,0,0,0);var lim=new Date(now.getTime()+21*864e5);var list=[];
    cards.forEach(function(c){[['data-start','data-end'],['data-start-now','data-end-now']].forEach(function(k){var s=c.getAttribute(k[0]),e=c.getAttribute(k[1]);if(!s)return;var sd=new Date(s+'T00:00:00'),ed=new Date(e+'T00:00:00');if(ed>=now&&sd<=lim)list.push([sd,c]);});});
    list.sort(function(a,b){return a[0]-b[0]});
    list.slice(0,9).forEach(function(p){var cl=p[1].cloneNode(true);cl.classList.remove('is-hidden');cl.removeAttribute('id');var t=document.createElement('span');t.className='fv-tag'+(p[0]<=now?'':' next');t.textContent=p[0]<=now?soon.getAttribute('data-now'):soon.getAttribute('data-next');cl.querySelector('.fv-top').appendChild(t);soonGrid.appendChild(cl);});
    if(soonGrid.children.length)soon.hidden=false;
  }
  var h=location.hash&&document.getElementById(location.hash.slice(1));if(h)h.style.outline='2px solid var(--aegean,#0B8FAC)';
})();
</script>'''


def controls(lang, fs, names, with_island=True):
    is_el = lang == 'el'
    islands = sorted({f['island'] for f in fs}, key=lambda k: names[k][1 if is_el else 0])
    types = [t for t in TYPES if any((f.get('type') or 'other') == t for f in fs)]
    sel = ''
    if with_island and len(islands) > 1:
        opts = ''.join(f'<option value="{k}">{esc(names[k][1 if is_el else 0])}</option>' for k in islands)
        sel = (f'<select id="fv-island" aria-label="{L(lang, "Island", "Νησί")}"><option value="">'
               f'{L(lang, "Island: all", "Νησί: όλα")}</option>{opts}</select>')
    chips = ''.join(f'<button type="button" class="fv-chip" data-type="{t}">{esc(TYPES[t][1 if is_el else 0])}</button>' for t in types)
    return (f'<div class="fv-controls">{sel}'
            f'<input id="fv-q" type="search" placeholder="{L(lang, "Search a village or saint…", "Ψάξε χωριό ή άγιο…")}">'
            f'<div class="fv-chips">{chips}</div>'
            f'<button type="button" class="fv-clear" id="fv-clear">{L(lang, "Clear", "Καθαρισμός")}</button>'
            f'<span class="fv-count"><span id="fv-count">{len(fs)}</span> {L(lang, "shown", "εμφανίζονται")}</span></div>'
            f'<p class="fv-noresults" id="fv-noresults">{L(lang, "Nothing matches these filters.", "Τίποτα δεν ταιριάζει με τα φίλτρα.")}</p>')


def soon_block(lang):
    return (f'<section class="fv-section fv-soon" id="fv-soon" hidden data-now="{L(lang, "Now", "Τώρα")}" data-next="{L(lang, "Next up", "Έρχεται")}">'
            f'<h2>{L(lang, "Happening now &amp; soon", "Τώρα &amp; προσεχώς")}</h2><div class="fv-grid" id="fv-soon-grid"></div></section>')


def month_strip(lang, counts, active=None, hub=False):
    p = '/el/festivals/' if lang == 'el' else '/festivals/'
    out = []
    for m in range(1, 13):
        n = counts.get(m, 0)
        if not n:
            continue
        lab = MONTHS_EL_NOM[m - 1] if lang == 'el' else MONTHS_EN[m - 1]
        cls = ' class="on"' if active == m else ''
        out.append(f'<a{cls} href="{p}{MONTH_SLUG[m]}/">{lab}<small>{n}</small></a>')
    if not hub:
        out.append(f'<a href="{p}">{L(lang, "All festivals →", "Όλες οι γιορτές →")}</a>')
    return '<nav class="fv-strip" aria-label="months">' + ''.join(out) + '</nav>'


def note(lang):
    return ('<p class="fv-note">' + L(lang,
        f'Dates are resolved for {SEASON_YEAR}: fixed saint\'s days as they fall, movable feasts computed from Orthodox Easter '
        f'({SEASON_YEAR}: {resolve({"movable": "easter"}, SEASON_YEAR)["start"].strftime("%-d %B")}). Panigiria are usually held on the eve '
        'of the saint\'s day, and a village occasionally shifts one to the nearest weekend — where an entry says "confirm locally", '
        'the date comes from recent years\' announcements rather than an official calendar. If you know better, the feedback button exists for exactly this.',
        f'Οι ημερομηνίες είναι υπολογισμένες για το {SEASON_YEAR}: οι σταθερές γιορτές όπως πέφτουν, οι κινητές από το ορθόδοξο Πάσχα '
        f'({SEASON_YEAR}: {resolve({"movable": "easter"}, SEASON_YEAR)["start"].day} {["Απριλίου","Μαΐου"][resolve({"movable": "easter"}, SEASON_YEAR)["start"].month-4]}). '
        'Τα πανηγύρια γίνονται συνήθως την παραμονή, και πού και πού ένα χωριό το μεταφέρει στο κοντινό Σαββατοκύριακο — όπου γράφει «επιβεβαίωσε τοπικά», '
        'η ημερομηνία προέρχεται από ανακοινώσεις προηγούμενων χρόνων και όχι από επίσημο ημερολόγιο. Αν ξέρεις καλύτερα, το κουμπί feedback υπάρχει ακριβώς γι\' αυτό.')
        + '</p>')


def write(path_rel, html):
    out = ROOT / path_rel.strip('/') / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8')


def footer(lang, en_path, el_path):
    is_el = lang == 'el'
    return (FOOTER.replace('{lang_link}', en_path if is_el else el_path)
            .replace('{lang_label}', 'English' if is_el else 'Ελληνικά')
            .replace('{privacy}', '/el/privacy/' if is_el else '/privacy/')
            .replace('{privacy_label}', 'Απόρρητο' if is_el else 'Privacy')
            .replace('{credits}', '/el/credits/' if is_el else '/credits/')
            .replace('{credits_label}', 'Πηγές φωτογραφιών' if is_el else 'Photo credits'))


# --------------------------------------------------------------------------- pages
def build_hub(flat, names, heroes):
    pairs = [('/festivals/', '/el/festivals/')]
    counts = {}
    for f in flat:
        counts[f['months'][0]] = counts.get(f['months'][0], 0) + 1
    per_island = {}
    for f in flat:
        per_island.setdefault(f['island'], []).append(f)
    exact = sum(1 for f in flat if f['exact'])
    for lang in ('en', 'el'):
        is_el = lang == 'el'
        n = len(flat)
        if is_el:
            title = f'Πανηγύρια Νησιών {SEASON_YEAR}: {n} Γιορτές ανά Χωριό & Ημερομηνία'
            desc = (f'{n} πανηγύρια και γιορτές σε {len(per_island)} ελληνικά νησιά για το {SEASON_YEAR}, με χωριό, ημερομηνία και τι γίνεται. '
                    'Ανά μήνα, ανά νησί, με προσθήκη στο ημερολόγιό σου.')
            h1 = f'Πανηγύρια & γιορτές στα νησιά, {SEASON_YEAR}'
            lede = (f'{n} πανηγύρια, λιτανείες, γιορτές κρασιού και φεστιβάλ σε {len(per_island)} νησιά — με το χωριό και την ημερομηνία, '
                    'όχι «κάπου τον Αύγουστο». Διάλεξε μήνα ή νησί, φιλτράρισε ανά είδος, και βάλε όσα θέλεις στο ημερολόγιό σου.')
        else:
            title = f'Greek Island Festivals {SEASON_YEAR}: {n} Panigiria by Village & Date'
            desc = (f'{n} panigiria and festivals on {len(per_island)} Greek islands for {SEASON_YEAR} — village, date and what actually happens. '
                    'By month, by island, with add-to-calendar.')
            h1 = f'Greek island festivals &amp; panigiria, {SEASON_YEAR}'
            lede = (f'{n} village feasts, processions, wine festivals and summer festivals across {len(per_island)} islands — with the village and the date, '
                    'not "sometime in August". Pick a month or an island, filter by kind, and put the ones you want in your calendar.')
        p = '/el' if is_el else ''
        # highlights per month: verified first, then high confidence, cap 8
        sections = []
        for m in range(1, 13):
            mf = [f for f in flat if f['months'][0] == m]
            if not mf:
                continue
            ranked = sorted(mf, key=lambda f: (not f.get('verified'), f.get('confidence') != 'high', f['sort']))
            pick = sorted(ranked[:8], key=lambda f: f['sort'])
            lab = MONTHS_EL_NOM[m - 1] if is_el else MONTHS_EN[m - 1]
            more = (f'<a class="fv-more" href="{p}/festivals/{MONTH_SLUG[m]}/">'
                    + L(lang, f'All {len(mf)} in {lab} →', f'Όλες οι {len(mf)} {MONTH_ACC_EL[m]} →') + '</a>') if len(mf) > len(pick) else ''
            sections.append(f'<section class="fv-section" id="m{m}" data-auto><h2>{lab} <small>{len(mf)}</small>{more}</h2>'
                            f'<div class="fv-grid">{"".join(card(f, names, lang) for f in pick)}</div></section>')
        # island directory
        dir_items = []
        for k in sorted(per_island, key=lambda k: names[k][1 if is_el else 0]):
            cnt = len(per_island[k])
            nm = esc(names[k][1 if is_el else 0])
            dir_items.append(f'<a href="{p}/festivals/{k}/">{nm}<span>{cnt}</span></a>')
        directory = (f'<section class="fv-section" id="islands"><h2>{L(lang, "By island", "Ανά νησί")} <small>{len(per_island)}</small></h2>'
                     f'<div class="fv-dir">{"".join(dir_items)}</div></section>')
        ikaria = (f'<a class="fv-cta" href="{p}/festivals/ikaria-panigiria/">{L(lang, "The panigiria of Ikaria — the long read →", "Τα πανηγύρια της Ικαρίας — το μεγάλο άρθρο →")}</a>'
                  f'<a class="fv-cta" href="{p}/festivals/august/">{L(lang, "August: " + str(counts.get(8, 0)) + " feasts →", "Αύγουστος: " + str(counts.get(8, 0)) + " πανηγύρια →")}</a>')
        stats = (f'<div class="fv-stats"><span><b>{n}</b> {L(lang, "festivals", "γιορτές")}</span><span><b>{len(per_island)}</b> {L(lang, "islands", "νησιά")}</span>'
                 f'<span><b>{exact}</b> {L(lang, "with exact dates", "με ακριβή ημερομηνία")}</span><span><b>{sum(1 for f in flat if (f.get("type") or "") == "panigiri")}</b> {L(lang, "village panigiria", "πανηγύρια χωριών")}</span></div>')
        body = (f'<main class="fv-page"><h1>{h1}</h1><p class="fv-lede">{lede}</p>{stats}{ikaria}'
                + month_strip(lang, counts, hub=True)
                + soon_block(lang)
                + controls(lang, flat, names)
                + ''.join(sections) + directory + note(lang) + '</main>')
        top = [f for f in flat if f.get('verified') and f['exact']]
        html = (page_head(title, desc, '/festivals/', '/el/festivals/', lang)
                .replace('</head>', CSS + breadcrumb_jsonld(lang, [(L(lang, 'Home', 'Αρχική'), p + '/'), (L(lang, 'Festivals', 'Γιορτές'), p + '/festivals/')])
                         + event_jsonld(top, names, lang, heroes) + '</head>')
                + header_nav(lang, '/festivals/' if is_el else '/el/festivals/')
                + body + FILTER_JS + footer(lang, '/festivals/', '/el/festivals/'))
        write(f'{p}/festivals/', html)
    return pairs


def build_months(flat, names, heroes):
    pairs = []
    counts = {}
    for f in flat:
        counts[f['months'][0]] = counts.get(f['months'][0], 0) + 1
    for m in range(1, 13):
        mf = [f for f in flat if m in f['months']]
        if not mf:
            continue
        slug = MONTH_SLUG[m]
        en_path, el_path = f'/festivals/{slug}/', f'/el/festivals/{slug}/'
        pairs.append((en_path, el_path))
        for lang in ('en', 'el'):
            is_el = lang == 'el'
            p = '/el' if is_el else ''
            lab = MONTHS_EL_NOM[m - 1] if is_el else MONTHS_EN[m - 1]
            n = len(mf)
            n_isl = len({f['island'] for f in mf})
            if is_el:
                title = f'Πανηγύρια {MONTHS_EL_GEN[m - 1]} {SEASON_YEAR}: {n} γιορτές σε {n_isl} νησιά'
                desc = f'Όλα τα πανηγύρια και οι γιορτές στα ελληνικά νησιά {MONTH_ACC_EL[m]} {SEASON_YEAR}: ημερομηνία, χωριό, νησί και τι να περιμένεις. {n} καταχωρήσεις, ανά ημέρα.'
                h1 = f'Πανηγύρια &amp; γιορτές {MONTH_ACC_EL[m]} {SEASON_YEAR}'
                lede = f'{n} γιορτές σε {n_isl} νησιά, ανά ημέρα. Οι κινητές γιορτές είναι υπολογισμένες για το {SEASON_YEAR}.'
            else:
                title = f'Greek Island Festivals in {lab} {SEASON_YEAR}: {n} Dates on {n_isl} Islands'
                desc = f'Every panigiri and festival on the Greek islands in {lab} {SEASON_YEAR} — date, village, island and what to expect. {n} entries, day by day.'
                h1 = f'Greek island festivals in {lab} {SEASON_YEAR}'
                lede = f'{n} festivals on {n_isl} islands, day by day. Movable feasts are computed for {SEASON_YEAR}.'
            # group by day
            parts = []
            cur = None
            for f in sorted(mf, key=lambda f: (f['sort'], f['island'])):
                if f['start'] and f['start'].month == m:
                    key = f['start']
                    daylab = (f'{key.day} {lab}' if not is_el else f'{key.day} {MONTHS_EL_GEN[m - 1]}') + ' · ' + (key.strftime('%A') if not is_el else
                             ['Δευτέρα', 'Τρίτη', 'Τετάρτη', 'Πέμπτη', 'Παρασκευή', 'Σάββατο', 'Κυριακή'][key.weekday()])
                elif f['start']:
                    key = 'spill'
                    daylab = L(lang, f'Continues from {MONTHS_EN[f["start"].month - 1]}', f'Συνεχίζεται από {MONTHS_EL_NOM[f["start"].month - 1]}')
                else:
                    key = 'approx'
                    daylab = L(lang, 'Date announced each year', 'Ημερομηνία ανακοινώνεται κάθε χρόνο')
                if key != cur:
                    if cur is not None:
                        parts.append('</div>')
                    parts.append(f'<h2 class="fv-day">{esc(daylab)}</h2><div class="fv-grid">')
                    cur = key
                parts.append(card(f, names, lang))
            if cur is not None:
                parts.append('</div>')
            ics = f'<a class="fv-cta" href="/festivals/ics/month-{slug}.ics" download>{L(lang, "＋ Whole month to calendar", "＋ Όλος ο μήνας στο ημερολόγιο")}</a>'
            body = (f'<main class="fv-page"><h1>{h1}</h1><p class="fv-lede">{lede}</p>'
                    + month_strip(lang, counts, active=m) + ics + controls(lang, mf, names)
                    + ''.join(parts) + note(lang) + '</main>')
            html = (page_head(title, desc, en_path, el_path, lang)
                    .replace('</head>', CSS + breadcrumb_jsonld(lang, [(L(lang, 'Home', 'Αρχική'), p + '/'), (L(lang, 'Festivals', 'Γιορτές'), p + '/festivals/'), (lab, p + en_path)])
                             + event_jsonld(mf, names, lang, heroes) + '</head>')
                    + header_nav(lang, en_path if is_el else el_path)
                    + body + FILTER_JS + footer(lang, en_path, el_path))
            write(f'{p}{en_path}', html)
    return pairs


def _tbl_village(f, is_el):
    v = f.get('village_el') if is_el and f.get('village_el') else f.get('village', '')
    nm = f.get('name_el') if is_el and f.get('name_el') else f['name']
    if not v or v.lower() in nm.lower():
        return ''
    return f' <span class="fv-village">· {esc(v)}</span>'


def build_islands(flat, names, heroes):
    pairs = []
    per = {}
    for f in flat:
        per.setdefault(f['island'], []).append(f)
    for k, fs in per.items():
        # Every island with at least one festival gets a page, so the hub's
        # island directory always leads somewhere. Under 3 entries is thin:
        # noindex,follow and kept out of the sitemap.
        thin = len(fs) < 3
        en_path, el_path = f'/festivals/{k}/', f'/el/festivals/{k}/'
        if not thin:
            pairs.append((en_path, el_path))
        exact = [f for f in fs if f['exact']]
        months = sorted({f['months'][0] for f in fs})
        villages = sorted({f.get('village') for f in fs if f.get('village')})
        for lang in ('en', 'el'):
            is_el = lang == 'el'
            p = '/el' if is_el else ''
            nm = names[k][1 if is_el else 0]
            n = len(fs)
            span = (MONTHS_EL_NOM[months[0] - 1] if is_el else MONTHS_EN[months[0] - 1]) + ('–' + (MONTHS_EL_NOM[months[-1] - 1] if is_el else MONTHS_EN[months[-1] - 1]) if len(months) > 1 else '')
            big = max(fs, key=lambda f: ((f.get('date') or {}).get('fixed') == '08-15', f.get('verified', False),
                                         f.get('type') == 'panigiri', f.get('confidence') == 'high', len(f.get('desc', ''))))
            if is_el:
                gen = GEN_EL.get(k) or ''
                title = (f'Πανηγύρια {gen} {SEASON_YEAR}: {n} {"γιορτή" if n == 1 else "γιορτές"} με ημερομηνίες & χωριά' if gen
                         else f'Πανηγύρια & γιορτές — {nm} {SEASON_YEAR}: {n} με ημερομηνίες & χωριά')
                desc = (f'Όλα τα πανηγύρια και οι γιορτές {gen_with_article(k, nm) or ("στο νησί " + nm)} για το {SEASON_YEAR}: {n} καταχωρήσεις με ημερομηνία, '
                        f'χωριό και τι γίνεται, {span}. Με προσθήκη στο ημερολόγιο.')
                h1 = f'Πανηγύρια &amp; γιορτές: {esc(nm)} {SEASON_YEAR}'
                lede = (f'{n} πανηγύρια και γιορτές, {span}' + (f', σε {len(villages)} χωριά' if len(villages) > 1 else '') +
                        f'. Το μεγάλο: {esc(big.get("name_el") or big["name"])} ({esc(big["when_el"])}). Οι ημερομηνίες είναι υπολογισμένες για το {SEASON_YEAR}.')
            else:
                title = f'{nm} Festivals {SEASON_YEAR}: {n} {"Panigiri" if n == 1 else "Panigiria"} with Dates & Villages'
                desc = f'Every panigiri and festival on {nm} in {SEASON_YEAR}: {n} entries with date, village and what happens, {span}. Add any of them to your calendar.'
                h1 = f'{esc(nm)} festivals &amp; panigiria, {SEASON_YEAR}'
                lede = (f'{n} feasts and festivals, {span}' + (f', across {len(villages)} villages' if len(villages) > 1 else '') +
                        f'. The big one: {esc(big["name"])} ({esc(big["when_en"])}). Dates are computed for {SEASON_YEAR}.')
            # calendar table (exact only), then full cards
            rows = ''.join(f'<tr><td>{esc(f["when_el"] if is_el else f["when_en"])}</td><td><a href="#{f["slug"]}">{esc((f.get("name_el") if is_el and f.get("name_el") else f["name"]))}</a>'
                           + _tbl_village(f, is_el) + '</td></tr>'
                           for f in sorted(exact, key=lambda f: f['sort']))
            table = f'<table class="fv-cal">{rows}</table>' if rows else ''
            ctas = (f'<a class="fv-cta" href="/festivals/ics/{k}.ics" download>{L(lang, "＋ All to calendar (.ics)", "＋ Όλα στο ημερολόγιο (.ics)")}</a>'
                    f'<a class="fv-cta" href="{p}/island/{k}/">{L(lang, "Full " + nm + " guide →", "Ο πλήρης οδηγός →")}</a>'
                    f'<a class="fv-cta" href="{p}/trip-cost/?i={k}%3A4&m=aug">{L(lang, "What would the trip cost? →", "Πόσο κοστίζει το ταξίδι; →")}</a>')
            if k == 'ikaria':
                ctas += f'<a class="fv-cta" href="{p}/festivals/ikaria-panigiria/">{L(lang, "How an Ikarian panigiri works →", "Πώς λειτουργεί ένα ικαριώτικο πανηγύρι →")}</a>'
            cards = ''.join(card(f, names, lang, show_island=False, heading='h2') for f in sorted(fs, key=lambda f: f['sort']))
            body = (f'<main class="fv-page"><h1>{h1}</h1><p class="fv-lede">{lede}</p>{ctas}{table}'
                    + soon_block(lang) + controls(lang, fs, names, with_island=False)
                    + f'<div class="fv-grid">{cards}</div>' + note(lang)
                    + f'<p style="margin-top:18px"><a class="fv-cta" href="{p}/festivals/">{L(lang, "← All island festivals", "← Όλες οι γιορτές των νησιών")}</a></p></main>')
            html = (page_head(title, desc, en_path, el_path, lang)
                    .replace('</head>', ('<meta name="robots" content="noindex,follow">\n' if thin else '')
                             + CSS + breadcrumb_jsonld(lang, [(L(lang, 'Home', 'Αρχική'), p + '/'), (L(lang, 'Festivals', 'Γιορτές'), p + '/festivals/'), (nm, p + en_path)])
                             + event_jsonld(fs, names, lang, heroes) + '</head>')
                    + header_nav(lang, en_path if is_el else el_path)
                    + body + FILTER_JS + footer(lang, en_path, el_path))
            write(f'{p}{en_path}', html)
    return pairs, {k: len(v) for k, v in per.items()}


# --------------------------------------------------------------------------- ics
def _ics_escape(s):
    return (s or '').replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,').replace('\n', '\\n')


def vevent(f, names, year_shift=0):
    if not f['start']:
        return ''
    s = f['start']; e = f['end'] + timedelta(days=1)
    if year_shift:
        r = resolve(f['date'], SEASON_YEAR + year_shift, f.get('eve'), f.get('duration_days'))
        if not r['start']:
            return ''
        s, e = r['start'], r['end'] + timedelta(days=1)
    iname = names[f['island']][0]
    loc = ', '.join(x for x in (f.get('village'), iname, 'Greece') if x)
    desc = re.sub(r'<[^>]+>', '', f.get('desc', '')) + f"\n\n{SITE_URL}/festivals/{f['island']}/#{f['slug']}"
    uid = f"{f['island']}-{f['slug']}-{s.year}@aegeanblueprint.com"
    return ('BEGIN:VEVENT\r\n'
            f'UID:{uid}\r\n'
            f'DTSTAMP:{TODAY.strftime("%Y%m%d")}T000000Z\r\n'
            f'DTSTART;VALUE=DATE:{s.strftime("%Y%m%d")}\r\n'
            f'DTEND;VALUE=DATE:{e.strftime("%Y%m%d")}\r\n'
            f'SUMMARY:{_ics_escape(f["name"])}\r\n'
            f'LOCATION:{_ics_escape(loc)}\r\n'
            f'DESCRIPTION:{_ics_escape(desc)}\r\n'
            f'URL:{SITE_URL}/festivals/{f["island"]}/#{f["slug"]}\r\n'
            'END:VEVENT\r\n')


def ics_file(events_text, name):
    return ('BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Aegean Blueprint//Festivals//EN\r\nCALSCALE:GREGORIAN\r\n'
            f'X-WR-CALNAME:{_ics_escape(name)}\r\n' + events_text + 'END:VCALENDAR\r\n')


def build_ics(flat, names):
    base = ROOT / 'festivals' / 'ics'
    base.mkdir(parents=True, exist_ok=True)
    n = 0
    per, per_month = {}, {}
    for f in flat:
        if not f['start']:
            continue
        per.setdefault(f['island'], []).append(f)
        per_month.setdefault(f['start'].month, []).append(f)
        d = base / f['island']
        d.mkdir(exist_ok=True)
        (d / f"{f['slug']}.ics").write_text(ics_file(vevent(f, names), f['name']), encoding='utf-8')
        n += 1
    for k, fs in per.items():
        # this season + next, so a subscriber's calendar doesn't go blank on 1 September
        body = ''.join(vevent(f, names) + vevent(f, names, 1) for f in fs)
        (base / f'{k}.ics').write_text(ics_file(body, f'{names[k][0]} festivals — Aegean Blueprint'), encoding='utf-8')
    for m, fs in per_month.items():
        body = ''.join(vevent(f, names) for f in fs)
        (base / f'month-{MONTH_SLUG[m]}.ics').write_text(ics_file(body, f'Greek island festivals — {MONTHS_EN[m - 1]} {SEASON_YEAR}'), encoding='utf-8')
    return n


# --------------------------------------------------------------------------- sitemap
def patch_sitemap(pairs):
    sm_path = ROOT / 'sitemap.xml'
    sm = sm_path.read_text(encoding='utf-8')
    START, END = '<!-- BEGIN AUTO-GENERATED FESTIVAL PAGES -->', '<!-- END AUTO-GENERATED FESTIVAL PAGES -->'
    today = TODAY.isoformat()
    blocks = []
    for en, el in pairs:
        if en == '/festivals/':
            continue   # prerender already lists the hub
        pr = '0.7' if en.count('/') == 3 else '0.6'
        for path in (en, el):
            blocks.append(f'  <url><loc>{SITE_URL}{path}</loc><lastmod>{today}</lastmod><priority>{pr}</priority>'
                          f'<xhtml:link rel="alternate" hreflang="en" href="{SITE_URL}{en}"/>'
                          f'<xhtml:link rel="alternate" hreflang="el" href="{SITE_URL}{el}"/>'
                          f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE_URL}{en}"/></url>')
    block = START + '\n' + '\n'.join(blocks) + '\n  ' + END
    # Drop any stale copies of these URLs (older builders appended month hubs at the end).
    ours = {SITE_URL + path for en, el in pairs for path in (en, el) if en != '/festivals/'}
    def _keep(m):
        loc = re.search(r'<loc>(.*?)</loc>', m.group(0))
        return '' if (loc and loc.group(1) in ours) else m.group(0)
    if START in sm:
        head, rest = sm.split(START, 1)
        tail = rest.split(END, 1)[1]
        sm = re.sub(r'\s*<url>.*?</url>', _keep, head, flags=re.DOTALL) + START + rest.split(START, 1)[-1][:0] + END + re.sub(r'\s*<url>.*?</url>', _keep, tail, flags=re.DOTALL)
    else:
        sm = re.sub(r'\s*<url>.*?</url>', _keep, sm, flags=re.DOTALL)
    if START in sm:
        sm = re.sub(re.escape(START) + r'.*?' + re.escape(END), block, sm, count=1, flags=re.DOTALL)
    else:
        sm = sm.replace('</urlset>', '  ' + block + '\n</urlset>')
    sm_path.write_text(sm, encoding='utf-8')
    return len(blocks)


def main():
    flat, names, heroes = load()
    pairs = build_hub(flat, names, heroes)
    pairs += build_months(flat, names, heroes)
    ip, counts = build_islands(flat, names, heroes)
    pairs += ip
    n_ics = build_ics(flat, names)
    (ROOT / 'festivals-index.json').write_text(json.dumps(counts, separators=(',', ':')), encoding='utf-8')
    n_sm = patch_sitemap(pairs)
    print(f'✓ Festivals: {len(flat)} festivals, season {SEASON_YEAR}; {len(pairs)} page pairs, {len(ip)} island pages, {n_ics} .ics, {n_sm} sitemap entries')


if __name__ == '__main__':
    sys.exit(main())
