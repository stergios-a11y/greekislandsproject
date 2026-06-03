#!/usr/bin/env python3
"""Generate static comparison pages at /compare/<a>-vs-<b>/ that load the
SPA shell (header, nav, footer, dark-mode toggle, language switcher) and
the same #view-compare skeleton used by the in-app /#compare route.

The SPA's parseHash() detects the /compare/<a>-vs-<b>/ path, pre-selects
those two islands, and calls renderCompareView() — so the user lands on
a fully rendered comparison page with the radar chart + colored bars +
editorial verdict, identical in look to what they'd see by manually
picking those islands in the in-app comparator.

Crawlable SEO content (H1, prose verdict from vs_verdicts.json, FAQ JSON-LD
where present) is also written directly into the HTML so Google indexes it
without needing to execute JavaScript.

Runs after prerender.py — they're independent.

Inputs:
  - vs_verdicts.json    : { 'a__b': {en: '<p>...</p>', el: '<p>...</p>'} }
  - vs_faqs.json (opt)  : { 'a__b': {en: [{q,a}, ...], el: [...]} }
  - script.js island metadata (for friendly names)

Outputs:
  - compare/<slug>/index.html (EN)
  - el/compare/<slug>/index.html (EL)
"""
import json
import re
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = 'https://aegeanblueprint.com'

# --------------------------------------------------------------------
# Load island metadata from script.js
# --------------------------------------------------------------------
def load_island_meta():
    """Parse the ISLANDS_DATA-like object out of script.js. We only need
    name and island_group per key."""
    js = (ROOT / 'script.js').read_text(encoding='utf-8')
    # Match lines like:  "milos": { name:"Milos", ... island_group:"Cyclades" ...},
    meta = {}
    # Find the start of the metadata block (avoid matching other braces). Each
    # island entry is on a single line of the form:  "key": { ... },
    line_re = re.compile(r'^\s*"([a-z-]+)":\s*\{[^}]*name:\s*"([^"]+)"[^}]*island_group:\s*"([^"]+)"',
                          re.MULTILINE)
    for m in line_re.finditer(js):
        key, name, group = m.group(1), m.group(2), m.group(3)
        meta[key] = {'name': name, 'group': group}
    return meta

# Greek island names — read from i18n.js ISLAND_NAMES_EL
def load_island_names_el():
    """Pull the Greek-name lookup from i18n.js. Format: { key: 'Greek Name' }."""
    js = (ROOT / 'i18n.js').read_text(encoding='utf-8')
    # The map is declared as `const ISLAND_NAMES_EL = { ... };` — extract its body.
    m = re.search(r'const\s+ISLAND_NAMES_EL\s*=\s*\{(.*?)\};', js, re.DOTALL)
    if not m:
        return {}
    body = m.group(1)
    names = {}
    for line in re.finditer(r'\'([a-z-]+)\'\s*:\s*\'([^\']+)\'', body):
        names[line.group(1)] = line.group(2)
    return names

META = load_island_meta()
NAMES_EL = load_island_names_el()

# --------------------------------------------------------------------
# Editorial content
# --------------------------------------------------------------------
def load_verdicts():
    p = ROOT / 'vs_verdicts.json'
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding='utf-8'))

def load_faqs():
    """Optional vs_faqs.json — same key shape as verdicts.
    Each value is {en: [{q,a},...], el: [...]}."""
    p = ROOT / 'vs_faqs.json'
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding='utf-8'))

VERDICTS = load_verdicts()
FAQS = load_faqs()

# --------------------------------------------------------------------
# Slug helpers
# --------------------------------------------------------------------
def parse_slug(slug):
    """'milos-vs-santorini' -> ('milos', 'santorini')"""
    return tuple(slug.split('-vs-', 1))

def pair_key(a, b):
    """Sorted pair key matching vs_verdicts.json convention."""
    return '__'.join(sorted([a, b]))

# --------------------------------------------------------------------
# HTML escaping
# --------------------------------------------------------------------
def esc(s):
    return (str(s).replace('&', '&amp;')
                  .replace('<', '&lt;')
                  .replace('>', '&gt;')
                  .replace('"', '&quot;'))

# --------------------------------------------------------------------
# Page rendering
# --------------------------------------------------------------------
def render_faq_jsonld(faqs):
    """Build FAQPage JSON-LD from a [{q, a}, ...] list."""
    if not faqs:
        return ''
    schema = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {
                '@type': 'Question',
                'name': item['q'],
                'acceptedAnswer': {'@type': 'Answer', 'text': item['a']}
            }
            for item in faqs
        ]
    }
    payload = json.dumps(schema, ensure_ascii=False, separators=(',', ':'))
    return f'<script type="application/ld+json">{payload}</script>'

def render_faq_html(faqs, lang):
    """Visible <details>/<summary> accordion for the FAQ block."""
    if not faqs:
        return ''
    items = []
    for item in faqs:
        q = esc(item['q'])
        a = esc(item['a'])
        items.append(f'<details><summary>{q}</summary><p>{a}</p></details>')
    heading = 'Common questions' if lang == 'en' else 'Συχνές ερωτήσεις'
    return (
        f'<div class="compare-faq">'
        f'<h3 class="compare-faq-heading">{heading}</h3>'
        f'{"".join(items)}'
        f'</div>'
    )

def render_page(slug, lang):
    """Render one comparison page (EN or EL).
    slug like 'milos-vs-santorini'; the function returns the full HTML string."""
    a, b = parse_slug(slug)
    if a not in META or b not in META:
        raise ValueError(f"Unknown island key in slug '{slug}': missing {a!r} or {b!r}")

    # Localized friendly names — used for the H1, OG title, etc.
    if lang == 'el':
        name_a = NAMES_EL.get(a, META[a]['name'])
        name_b = NAMES_EL.get(b, META[b]['name'])
    else:
        name_a = META[a]['name']
        name_b = META[b]['name']

    # Verdict prose (from vs_verdicts.json). May be empty.
    pkey = pair_key(a, b)
    verdict_entry = VERDICTS.get(pkey, {})
    verdict_html = verdict_entry.get('el' if lang == 'el' else 'en', '') or ''

    # FAQs (from vs_faqs.json, optional). May be empty.
    faq_entry = FAQS.get(pkey, {})
    faqs = faq_entry.get('el' if lang == 'el' else 'en', []) or []

    # ------------- meta block -------------
    if lang == 'en':
        page_title = f'{name_a} vs {name_b}: Which Greek Island Should You Choose? | Aegean Blueprint'
        page_desc = (f'{name_a} vs {name_b}: side-by-side comparison of beaches, nightlife, '
                     f'culture, access, and price. Find the right island for your trip.')
        h1_text = f'{name_a} vs {name_b}: Which Should You Visit?'
        subtitle = (f'Side-by-side comparison of two Greek islands — scores, character, when to visit.')
        verdict_heading = 'Our verdict'
        wtv_heading = 'When to visit — overlap'
        extra_heading = 'Character & practicalities'
    else:
        page_title = f'{name_a} ή {name_b}: Ποιο ελληνικό νησί να διαλέξεις; | Aegean Blueprint'
        page_desc = (f'{name_a} ή {name_b}: αναλυτική σύγκριση παραλιών, νυχτερινής ζωής, '
                     f'πολιτισμού, πρόσβασης και τιμών. Βρες το σωστό νησί για το ταξίδι σου.')
        h1_text = f'{name_a} ή {name_b};'
        subtitle = 'Λεπτομερής σύγκριση δύο ελληνικών νησιών — βαθμολογίες, χαρακτηριστικά, ποια εποχή να πας.'
        verdict_heading = 'Η ετυμηγορία μας'
        wtv_heading = 'Πότε να πας — επικάλυψη'
        extra_heading = 'Χαρακτήρας & πρακτικά'

    # Canonical + hreflang
    base = f'{SITE_URL}/compare/{slug}/'
    el_base = f'{SITE_URL}/el/compare/{slug}/'
    canonical = el_base if lang == 'el' else base

    # OG image — site default
    og_image = f'{SITE_URL}/og-image.png'

    # ------------- FAQ schema in head -------------
    faq_jsonld = render_faq_jsonld(faqs)

    # ------------- pre-rendered verdict block (visible to Google without JS) -------------
    # Wrap the verdict HTML so that when the SPA boots, renderCompareVerdict()
    # can overwrite #compare-verdict with its own rendering — but until that
    # happens (e.g. JS disabled, slow-loading bots), the prose is right there.
    if verdict_html or faqs:
        prerendered_verdict = (
            f'<h3 class="compare-verdict-heading">{verdict_heading}</h3>'
            f'{verdict_html}'
            f'{render_faq_html(faqs, lang)}'
        )
        verdict_div_style = ''   # visible by default
    else:
        prerendered_verdict = ''
        verdict_div_style = 'display:none;'

    # ------------- the H1 (above the SPA's auto-rendered <h2> Compare Islands) -------------
    # The SPA's #view-compare starts with <h2 data-i18n="compare.title">Compare Islands</h2>.
    # We don't want two competing headings, so we render a single <h1> at the top of the
    # main section and HIDE the SPA's stock heading + intro line with inline CSS for this page.

    # ------------- shell -------------
    asset_v = 47  # bump together with script.js version
    # JSON-encoded pair for the inline boot hint (window.__INITIAL_COMPARE_PAIR)
    init_pair_json = json.dumps([a, b])
    if lang == 'en':
        lang_attr = 'en'
        og_locale = 'en_US'
        alt_lang = 'el'
        alt_url = el_base
        privacy_url = '/privacy/'
        # The brand bits: text labels in headers, footer etc. Most labels are
        # data-i18n driven and will be replaced by applyStaticTranslations()
        # after script.js boots, so we use English placeholders here.
    else:
        lang_attr = 'el'
        og_locale = 'el_GR'
        alt_lang = 'en'
        alt_url = base

    # The static-page-specific CSS:
    # - Hide the SPA's "Compare Islands" stock <h2> and intro so the page doesn't
    #   have two competing titles
    # - Add small breathing room around the H1
    # - Style the FAQ accordion + verdict heading consistently
    extra_css = '''
  .vs-page-h1 {
    font-family: var(--display, Georgia, serif);
    font-size: 32px;
    margin: 0 0 6px;
    color: var(--ink-1, #222);
  }
  .vs-page-sub {
    font-size: 16px;
    color: var(--ink-2, #555);
    margin: 0 0 24px;
  }
  .compare-faq {
    margin-top: 18px;
  }
  .compare-faq-heading {
    font-family: var(--display, Georgia, serif);
    font-size: 20px;
    margin: 0 0 12px;
    color: var(--ink-1, #222);
  }
  .compare-faq details {
    background: var(--white, #fff);
    border: 1px solid var(--border, #e5e1d8);
    border-radius: 8px;
    padding: 0;
    margin-bottom: 8px;
  }
  .compare-faq details summary {
    cursor: pointer;
    padding: 12px 16px;
    font-weight: 600;
    font-size: 15px;
    color: var(--ink-1, #222);
    list-style: none;
  }
  .compare-faq details summary::-webkit-details-marker { display: none; }
  .compare-faq details summary::after {
    content: '+';
    float: right;
    color: var(--aegean, #0B8FAC);
    font-weight: 700;
  }
  .compare-faq details[open] summary::after { content: '−'; }
  .compare-faq details p {
    padding: 0 16px 14px;
    margin: 0;
    font-size: 15px;
    line-height: 1.6;
    color: var(--ink-1, #333);
  }
  html.dark .compare-faq details {
    background: #2a2a2a;
    border-color: #444;
  }
'''

    # Read the shared header markup from index.html so we don't duplicate it.
    # Just copy the <header> + <body opening>...<header> closing</header> chunk.
    # Simpler: hand-build the header here. The compare-page header doesn't need
    # the home-controls / vibe-panel / help-modal etc.
    nav_links_en = [
        ('/', 'Map', 'nav-map'),
        ('/#data', 'Islands Data', 'nav-data'),
        ('/#compare', 'Compare', 'nav-compare'),
        ('/festivals/', 'Festivals', 'nav-festivals'),
        ('/ferries/', 'Ferries', 'nav-ferries'),
        ('/#hopping', 'Island Hopping', 'nav-hopping'),
        ('/#international', 'International', 'nav-international'),
        ('/#match', 'Match Me', 'nav-match'),
        ('/#shortlist', '⭐ My Shortlist', 'nav-shortlist'),
        ('/#mission', 'Mission', 'nav-mission'),
    ]
    nav_links_el = [
        ('/el/', 'Χάρτης', 'nav-map'),
        ('/el/#data', 'Στοιχεία Νησιών', 'nav-data'),
        ('/el/#compare', 'Σύγκριση', 'nav-compare'),
        ('/el/festivals/', 'Γιορτές', 'nav-festivals'),
        ('/el/ferries/', 'Πλοία', 'nav-ferries'),
        ('/el/#hopping', 'Νησοπορία', 'nav-hopping'),
        ('/el/#international', 'Διεθνώς', 'nav-international'),
        ('/el/#match', 'Ταίριαξέ με', 'nav-match'),
        ('/el/#shortlist', '⭐ Λίστα μου', 'nav-shortlist'),
        ('/el/#mission', 'Στόχος', 'nav-mission'),
    ]
    nav_items = nav_links_el if lang == 'el' else nav_links_en
    nav_html = '\n        '.join(
        f'<a href="{href}" id="{nav_id}">{esc(label)}</a>'
        for href, label, nav_id in nav_items
    )
    if lang == 'el':
        nav_html += '\n        <a href="/el/privacy/" class="nav-utility" id="nav-privacy">Απόρρητο</a>'
        footer_privacy = '<a href="/el/privacy/" data-i18n="footer.privacy">Απόρρητο</a>'
        site_logo_text = 'Aegean Blueprint'
    else:
        nav_html += '\n        <a href="/privacy/" class="nav-utility" id="nav-privacy">Privacy</a>'
        footer_privacy = '<a href="/privacy/" data-i18n="footer.privacy">Privacy</a>'
        site_logo_text = 'Aegean Blueprint'

    # ------------- ASSEMBLE -------------
    html = f'''<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(page_title)}</title>
<meta name="description" content="{esc(page_desc)}">
<meta name="theme-color" content="#0B8FAC">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{base}">
<link rel="alternate" hreflang="el" href="{el_base}">
<link rel="alternate" hreflang="x-default" href="{base}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(page_title)}">
<meta property="og:description" content="{esc(page_desc)}">
<meta property="og:image" content="{og_image}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{og_locale}">
<meta property="og:site_name" content="Aegean Blueprint">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(page_title)}">
<meta name="twitter:description" content="{esc(page_desc)}">
<meta name="twitter:image" content="{og_image}">
<script>if(localStorage.getItem("darkMode")==="true"){{document.documentElement.classList.add("dark");}}</script>
<link rel="stylesheet" href="/style.css">
<style>
{extra_css}
</style>
{faq_jsonld}
</head>
<body>

<header>
  <div class="header-content">
    <div class="logo-wrapper" id="nav-home">
      <img src="/logo-hero.svg" id="site-logo" alt="Aegean Blueprint logo">
      <span id="brand-text"><span class="brand-word">Aegean</span> <span class="brand-word">Blueprint</span></span>
    </div>
    <div class="menu-toggle" id="menu-toggle-btn"><span></span><span></span><span></span></div>
    <nav class="top-nav" id="main-nav">
        {nav_html}
    </nav>
    <div class="lang-dropdown" id="lang-dropdown">
      <button class="lang-toggle" id="lang-toggle-btn" aria-label="Switch language" aria-haspopup="true" aria-expanded="false">
        <span class="lang-globe">🌐</span>
        <span class="lang-current" id="lang-current">{'EL' if lang == 'el' else 'EN'}</span>
        <span class="lang-caret">▾</span>
      </button>
      <div class="lang-menu" id="lang-menu" role="menu">
        <a href="#" class="lang-option" data-lang="en" role="menuitem"><span class="lang-option-flag">🇬🇧</span> English</a>
        <a href="#" class="lang-option" data-lang="el" role="menuitem"><span class="lang-option-flag">🇬🇷</span> Ελληνικά</a>
      </div>
    </div>
    <button class="dark-mode-toggle" id="dark-mode-btn" aria-label="Toggle dark mode">☾</button>
  </div>
</header>

<main id="view-compare" class="view-section content-page">
  <h1 class="vs-page-h1">{esc(h1_text)}</h1>
  <p class="vs-page-sub">{esc(subtitle)}</p>
  <div class="compare-selectors">
    <select id="compare-select-a"><option value="" data-i18n="compare.optionA">— Island A —</option></select>
    <span class="vs-label" data-i18n="compare.vs">vs</span>
    <select id="compare-select-b"><option value="" data-i18n="compare.optionB">— Island B —</option></select>
  </div>
  <div id="compare-container">
    <div id="compare-placeholder" class="compare-placeholder" data-i18n="compare.placeholder">Select two islands above to start comparing.</div>
    <div id="compare-content" style="display:none;">
      <div class="compare-radar-wrap">
        <canvas id="compare-radar-chart" role="img" aria-label="Radar chart comparing two islands"></canvas>
      </div>
      <div class="compare-cards" id="compare-cards"></div>
      <div id="compare-verdict" class="compare-verdict" style="{verdict_div_style}">{prerendered_verdict}</div>
      <div class="compare-section-label" data-i18n="compare.wtv_title">{esc(wtv_heading)}</div>
      <div id="compare-wtv" class="compare-wtv"></div>
      <div class="compare-section-label" data-i18n="compare.extra_title">{esc(extra_heading)}</div>
      <div id="compare-extra" class="compare-extra"></div>
    </div>
  </div>
</main>

<footer id="site-footer">
  <div class="footer-line">
    <span class="footer-copy" data-i18n="footer.copyright">© 2026 Aegean Blueprint</span> · {footer_privacy}<span class="footer-updated" id="footer-updated"></span>
  </div>
</footer>

<script>
// Tell the SPA which pair to render before it boots, so the first paint
// shows the right chart and no flash of the default mykonos/santorini view.
window.__INITIAL_COMPARE_PAIR = {init_pair_json};
</script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script src="/i18n.js?v={asset_v}"></script>
<script src="/script.js?v={asset_v}"></script>
</body>
</html>
'''
    return html


def main():
    # Discover all existing slugs (the directories under /compare/).
    compare_dir = ROOT / 'compare'
    if not compare_dir.exists():
        print("ERROR: /compare directory not found")
        return 1
    slugs = sorted(d.name for d in compare_dir.iterdir()
                   if d.is_dir() and '-vs-' in d.name)
    print(f"Found {len(slugs)} comparison slugs")

    el_dir = ROOT / 'el' / 'compare'
    el_dir.mkdir(parents=True, exist_ok=True)

    ok = 0
    skipped = []
    for slug in slugs:
        a, b = parse_slug(slug)
        if a not in META or b not in META:
            skipped.append((slug, f'missing keys: {a if a not in META else ""} {b if b not in META else ""}'))
            continue
        # EN
        en_path = ROOT / 'compare' / slug / 'index.html'
        en_path.parent.mkdir(parents=True, exist_ok=True)
        en_path.write_text(render_page(slug, 'en'), encoding='utf-8')
        # EL
        el_path = ROOT / 'el' / 'compare' / slug / 'index.html'
        el_path.parent.mkdir(parents=True, exist_ok=True)
        el_path.write_text(render_page(slug, 'el'), encoding='utf-8')
        ok += 1

    print(f"✓ Generated {ok} EN + {ok} EL comparison pages")
    if skipped:
        print(f"⚠ Skipped {len(skipped)}:")
        for s, why in skipped:
            print(f"   - {s}: {why}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
