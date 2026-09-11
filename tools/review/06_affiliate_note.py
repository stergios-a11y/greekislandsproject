#!/usr/bin/env python3
"""Review fix 5 — disclose the affiliate relationship at the moment of the click,
not only on /privacy/.

A small note is attached to every booking-CTA cluster:
  .detail-actionbar   island pages
  .cta-affiliate      compare pages, ferries page, sticky mobile bar
  .planner-btn-group  route planner / international ferries
  .tc-ctas            trip-cost result

Static clusters get the markup from the generators (so crawlers and the no-JS
fallback see it); SPA-rendered ones get it from attachAffiliateNotes(), which
skips any cluster that already has a note, so the two never double up.

Wording note: of the three partners only DiscoverCars currently carries a live
affiliate id (Booking.com is on a placeholder AID, Ferryhopper links are plain).
Every cluster contains the car link, so "affiliate links" is true of every
cluster as a whole, and stays true when the other two are switched on.

Idempotent.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
NOTE_EN = 'Affiliate links — they support this guide and cost you nothing.'
NOTE_EL = 'Affiliate σύνδεσμοι — στηρίζουν αυτόν τον οδηγό χωρίς κόστος για εσένα.'

def note_html(lang):
    href = '/privacy/#affiliate' if lang == 'en' else '/el/privacy/#affiliate'
    txt = NOTE_EN if lang == 'en' else NOTE_EL
    return (f'<p class="aff-note"><a href="{href}">{txt}</a></p>')

JS = """
/* Affiliate disclosure at the point of action. Server-rendered clusters already
   carry a .aff-note; this only fills in the ones the SPA builds. */
const AFF_CLUSTERS = ['.detail-actionbar', '.cta-affiliate', '.planner-btn-group', '.tc-ctas'];
function affNoteHtml() {
  const el = (typeof CURRENT_LANG !== 'undefined' && CURRENT_LANG === 'el');
  const href = el ? '/el/privacy/#affiliate' : '/privacy/#affiliate';
  const txt = el
    ? 'Affiliate σύνδεσμοι — στηρίζουν αυτόν τον οδηγό χωρίς κόστος για εσένα.'
    : 'Affiliate links — they support this guide and cost you nothing.';
  return '<a href="' + href + '">' + txt + '</a>';
}
function attachAffiliateNotes() {
  document.querySelectorAll(AFF_CLUSTERS.join(',')).forEach(box => {
    let n = box.querySelector(':scope > .aff-note');
    if (!n) {
      n = document.createElement('p');
      n.className = 'aff-note';
      box.appendChild(n);
    }
    n.innerHTML = affNoteHtml();
  });
}
window.attachAffiliateNotes = attachAffiliateNotes;
"""

CSS = """
/* --- Affiliate disclosure at the point of action (review fix 5) --------- */
.aff-note {
  flex-basis: 100%;
  width: 100%;
  margin: 6px 0 0;
  font-size: .72rem;
  line-height: 1.35;
  color: var(--ink-3, #8a939f);
}
.aff-note a { color: inherit; text-decoration: underline; text-underline-offset: 2px; }
.aff-note a:hover { color: var(--aegean); }
.cta-affiliate .aff-note { text-align: center; margin-top: 4px; }
.tc-ctas .aff-note { text-align: center; }
"""

def bail(msg):
    print('  !!', msg, file=sys.stderr); sys.exit(1)

def sub_once(s, old, new, where):
    if new in s:
        return s
    if s.count(old) < 1:
        bail(f'{where}: anchor not found')
    return s.replace(old, new)

def main():
    # ---- 1. privacy: give the affiliate section a link target ----------------
    for rel, head in (('privacy/index.html', '<h2>Affiliate links</h2>'),
                      ('el/privacy/index.html', '<h2>Affiliate σύνδεσμοι</h2>')):
        p = ROOT / rel
        s = p.read_text(encoding='utf-8')
        if 'id="affiliate"' not in s:
            if s.count(head) != 1:
                bail(f'{rel}: {s.count(head)} matches for the affiliate heading')
            s = s.replace(head, head.replace('<h2>', '<h2 id="affiliate">'))
            p.write_text(s, encoding='utf-8')

    # ---- 2. style.css -------------------------------------------------------
    p = ROOT / 'style.css'
    s = p.read_text(encoding='utf-8')
    if '.aff-note' not in s:
        p.write_text(s.rstrip('\n') + '\n' + CSS, encoding='utf-8')

    # ---- 3. script.js: helper + call sites ----------------------------------
    p = ROOT / 'script.js'
    s = p.read_text(encoding='utf-8')
    if 'attachAffiliateNotes' not in s:
        anchor = 'function scoreVerdict(s) {'
        if s.count(anchor) != 1:
            bail('script.js: cannot place attachAffiliateNotes()')
        s = s.replace(anchor, JS.strip() + '\n\n' + anchor)
        # run it whenever a view is (re)drawn and whenever the language flips
        hook = '      guide.innerHTML = buildIslandPage(data, key);'
        if s.count(hook) != 1:
            bail('script.js: render hook not found')
        s = s.replace(hook, hook + '\n      setTimeout(attachAffiliateNotes, 0);')
        p.write_text(s, encoding='utf-8')

    # ---- 4. static CTA clusters in the generators + hand-written pages ------
    CTA_OPEN = '<div class="cta-affiliate"'
    targets = [
        ('index.html', 'en'), ('el/index.html', 'el'),
        ('ferries/index.html', 'en'),
        ('tools/prerender.py', None), ('tools/build_compare_pages.py', None),
    ]
    for rel, lang in targets:
        p = ROOT / rel
        s = p.read_text(encoding='utf-8')
        orig = s
        # close every cta-affiliate div with the note just before </div>
        def add(m):
            block = m.group(0)
            if 'aff-note' in block:
                return block
            lg = lang
            if lg is None:   # generator: pick by the Greek marker in the block
                lg = 'el' if ('Κράτηση' in block or "is_el else" in block) else 'en'
            if rel.endswith('.py') and 'is_el' in block:
                ins = ("' + ('" + note_html('el').replace("'", "\\'") + "' if is_el else '"
                       + note_html('en').replace("'", "\\'") + "') + '")
                return block[:-len('</div>')] + ins + '</div>'
            return block[:-len('</div>')] + note_html(lg) + '</div>'
        s = re.sub(r'<div class="cta-affiliate".*?</div>', add, s, flags=re.S)
        if s != orig:
            p.write_text(s, encoding='utf-8')

    # ---- 5. prerendered island action bar ----------------------------------
    p = ROOT / 'tools' / 'prerender.py'
    s = p.read_text(encoding='utf-8')
    if 'aff-note' not in s.split('detail-actionbar')[1][:2000]:
        a = ("""        <a class="car-btn" id="detail-car-btn" target="_blank" rel="noopener sponsored" data-i18n="detail.rentcar">{'🚗 Rent a car' if lang == 'en' else '🚗 Ενοικίαση αυτοκινήτου'}</a>""")
        if s.count(a) != 1:
            bail(f'prerender.py: {s.count(a)} matches for the action-bar car button')
        add = ("\n" + '        <p class="aff-note"><a href="{\'/privacy/#affiliate\' if lang == \'en\' else \'/el/privacy/#affiliate\'}">'
               + '{\'' + NOTE_EN + '\' if lang == \'en\' else \'' + NOTE_EL + '\'}</a></p>')
        s = s.replace(a, a + add)
        p.write_text(s, encoding='utf-8')

    # ---- 6. index shells: island action bar + planner groups ---------------
    for rel, lang in (('index.html', 'en'), ('el/index.html', 'el')):
        p = ROOT / rel
        s = p.read_text(encoding='utf-8')
        orig = s
        for cls in ('detail-actionbar', 'planner-btn-group'):
            def add2(m, _c=cls):
                b = m.group(0)
                return b if 'aff-note' in b else b[:-len('</div>')] + note_html(lang) + '</div>'
            s = re.sub(r'<div class="' + cls + r'"[^>]*>.*?</div>\s*</div>',
                       lambda m: m.group(0), s, flags=re.S)  # no-op guard
            s = re.sub(r'<div class="' + cls + r'"[^>]*>(?:(?!</div>).)*?(?:<a\b(?:(?!</div>).)*?)?</div>',
                       add2, s, flags=re.S)
        if s != orig:
            p.write_text(s, encoding='utf-8')

    # ---- 7. trip-cost result CTAs ------------------------------------------
    p = ROOT / 'tools' / 'build_trip_cost.py'
    s = p.read_text(encoding='utf-8')
    if 'aff-note' not in s:
        a = ('      <a class="tc-cta c" href="https://www.discovercars.com/?a_aid=antaran2" '
             'target="_blank" rel="noopener sponsored">${{T.cta_car}}</a>\n    </div>')
        if s.count(a) != 1:
            bail(f'build_trip_cost.py: {s.count(a)} matches for the CTA block')
        s = s.replace(a, a.replace('\n    </div>',
              '\n      <p class="aff-note"><a href="${{LANG===\'el\'?\'/el/privacy/#affiliate\':\'/privacy/#affiliate\'}}">${{T.aff_note}}</a></p>\n    </div>'))
        s = s.replace("'cta_ferry': '🚢 Book ferries', 'cta_car': '🚗 Get the car',",
                      "'cta_ferry': '🚢 Book ferries', 'cta_car': '🚗 Get the car',\n        'aff_note': '" + NOTE_EN + "',")
        s = s.replace("'cta_ferry': '🚢 Κράτηση πλοίων', 'cta_car': '🚗 Κλείσε αυτοκίνητο',",
                      "'cta_ferry': '🚢 Κράτηση πλοίων', 'cta_car': '🚗 Κλείσε αυτοκίνητο',\n        'aff_note': '" + NOTE_EL + "',")
        s = s.replace("        'cta_ferry', 'cta_car',", "        'cta_ferry', 'cta_car', 'aff_note',")
        p.write_text(s, encoding='utf-8')

    print('affiliate note: applied')

main()
