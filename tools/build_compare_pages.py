#!/usr/bin/env python3
"""Generate static, SEO-indexable comparison pages at /compare/<a>-vs-<b>/.

Each page is:
  - The same SPA shell as index.html (header, nav, footer, fonts, CSS)
  - The same #view-compare skeleton — radar chart, cards, etc. all render
    identically to /#compare when the SPA hydrates
  - A unique <title> + <meta description> + canonical URL per pair
  - The editorial verdict from vs_verdicts.json baked into the HTML so
    Google crawls it without executing JavaScript
  - The FAQ from vs_faqs.json (where present) baked into the HTML AND
    serialized as FAQPage JSON-LD in <head> for rich-snippet eligibility
  - An inline boot hint window.__INITIAL_COMPARE_PAIR so the SPA pre-fills
    the dropdowns on first paint, no flash of the default pair

The earlier teardown (commit 02e1f3b4) was driven by the OLD static pages
looking visually different from the SPA. This rebuild guarantees identical
appearance by reusing the same shell — only the URL changes.

Reads:  vs_verdicts.json, vs_faqs.json, island metadata in script.js
Writes: compare/<slug>/index.html, el/compare/<slug>/index.html
"""
import json
import re
from pathlib import Path

def _resolve_root():
    candidates = []
    try:
        candidates.append(Path(__file__).resolve().parent.parent)
    except NameError:
        pass
    candidates.append(Path.cwd())
    cwd = Path.cwd()
    for _ in range(4):
        candidates.append(cwd)
        cwd = cwd.parent
    for c in candidates:
        if (c / 'vs_verdicts.json').is_file() and (c / 'script.js').is_file():
            return c
    raise SystemExit(
        "Could not find project root. Run from inside the project, e.g. "
        "`cd ~/greekislandsproject && python3 tools/build_compare_pages.py`."
    )

ROOT = _resolve_root()
SITE_URL = 'https://aegeanblueprint.com'
ASSET_V = 47

VERDICTS = json.loads((ROOT / 'vs_verdicts.json').read_text(encoding='utf-8'))
FAQS_PATH = ROOT / 'vs_faqs.json'
FAQS = json.loads(FAQS_PATH.read_text(encoding='utf-8')) if FAQS_PATH.exists() else {}

def load_island_meta():
    js = (ROOT / 'script.js').read_text(encoding='utf-8')
    meta = {}
    for m in re.finditer(
        r'^\s*"([a-z-]+)"\s*:\s*\{\s*name\s*:\s*"([^"]+)"[^}]*island_group\s*:\s*"([^"]+)"',
        js, re.MULTILINE
    ):
        meta[m.group(1)] = {'name': m.group(2), 'group': m.group(3)}
    return meta

def load_island_names_el():
    js = (ROOT / 'i18n.js').read_text(encoding='utf-8')
    m = re.search(r'const\s+ISLAND_NAMES_EL\s*=\s*\{(.*?)\};', js, re.DOTALL)
    if not m:
        return {}
    out = {}
    for ml in re.finditer(r"'([a-z-]+)'\s*:\s*'([^']+)'", m.group(1)):
        out[ml.group(1)] = ml.group(2)
    return out

META = load_island_meta()
NAMES_EL = load_island_names_el()

def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;')
                  .replace('>', '&gt;').replace('"', '&quot;'))

def parse_pair_key(pk):
    return tuple(pk.split('__', 1))

def slug_for_pair(a, b):
    a, b = sorted([a, b])
    return f'{a}-vs-{b}'

def render_faq_jsonld(faqs):
    if not faqs:
        return ''
    schema = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {'@type': 'Question', 'name': item['q'],
             'acceptedAnswer': {'@type': 'Answer', 'text': item['a']}}
            for item in faqs
        ]
    }
    return ('<script type="application/ld+json">'
            + json.dumps(schema, ensure_ascii=False, separators=(',', ':'))
            + '</script>')

def render_faq_html(faqs, lang):
    if not faqs:
        return ''
    items = []
    for item in faqs:
        items.append(
            f'<details><summary>{esc(item["q"])}</summary>'
            f'<p>{esc(item["a"])}</p></details>'
        )
    heading = 'Common questions' if lang == 'en' else 'Συχνές ερωτήσεις'
    return (f'<div class="compare-faq">'
            f'<h3 class="compare-faq-heading">{heading}</h3>'
            f'{"".join(items)}</div>')

def render_page(pair_key, lang):
    a, b = parse_pair_key(pair_key)
    if a not in META or b not in META:
        raise ValueError(f"Unknown island in pair {pair_key}: {a} / {b}")

    slug = slug_for_pair(a, b)

    if lang == 'el':
        name_a = NAMES_EL.get(a, META[a]['name'])
        name_b = NAMES_EL.get(b, META[b]['name'])
    else:
        name_a = META[a]['name']
        name_b = META[b]['name']

    verdict_entry = VERDICTS.get(pair_key, {})
    verdict_html = verdict_entry.get('el' if lang == 'el' else 'en', '') or ''
    faq_entry = FAQS.get(pair_key, {})
    faqs = faq_entry.get('el' if lang == 'el' else 'en', []) or []

    if lang == 'en':
        page_title = f'{name_a} vs {name_b}: Which Greek Island Should You Visit? | Aegean Blueprint'
        page_desc = (f'{name_a} vs {name_b} — side-by-side comparison of beaches, '
                     f'culture, nightlife, access, and price. Practical recommendations '
                     f'for choosing the right island for your trip.')
        h1_text = f'{name_a} vs {name_b}'
        subtitle = 'Side-by-side comparison — beaches, culture, atmosphere, and the practical question of which one suits your trip.'
        verdict_heading = 'Our verdict'
        og_locale = 'en_US'
    else:
        page_title = f'{name_a} ή {name_b}: Ποιο ελληνικό νησί να διαλέξεις; | Aegean Blueprint'
        page_desc = (f'{name_a} ή {name_b} — αναλυτική σύγκριση παραλιών, πολιτισμού, '
                     f'νυχτερινής ζωής, πρόσβασης και τιμών. Πρακτικές συμβουλές για '
                     f'να επιλέξεις το σωστό νησί για το ταξίδι σου.')
        h1_text = f'{name_a} ή {name_b}'
        subtitle = 'Λεπτομερής σύγκριση — παραλίες, πολιτισμός, ατμόσφαιρα, και η πρακτική επιλογή του νησιού που ταιριάζει στο ταξίδι σου.'
        verdict_heading = 'Η ετυμηγορία μας'
        og_locale = 'el_GR'

    en_url = f'{SITE_URL}/compare/{slug}/'
    el_url = f'{SITE_URL}/el/compare/{slug}/'
    canonical = el_url if lang == 'el' else en_url

    faq_jsonld = render_faq_jsonld(faqs)

    if verdict_html or faqs:
        prerendered_verdict = (
            f'<h3 class="compare-verdict-heading">{esc(verdict_heading)}</h3>'
            f'{verdict_html}'
            f'{render_faq_html(faqs, lang)}'
        )
        verdict_display = ''
    else:
        prerendered_verdict = ''
        verdict_display = 'display:none;'

    init_pair = json.dumps([a, b])

    if lang == 'el':
        nav_items = [
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
            ('/el/privacy/', 'Απόρρητο', 'nav-privacy'),
        ]
        home_url = '/el/'
        privacy_link = '<a href="/el/privacy/" data-i18n="footer.privacy">Απόρρητο</a>'
    else:
        nav_items = [
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
            ('/privacy/', 'Privacy', 'nav-privacy'),
        ]
        home_url = '/'
        privacy_link = '<a href="/privacy/" data-i18n="footer.privacy">Privacy</a>'

    nav_html = '\n        '.join(
        f'<a href="{esc(href)}" id="{nav_id}">{esc(label)}</a>'
        for href, label, nav_id in nav_items
    )

    page_css = '''
  #view-compare > h2[data-i18n="compare.title"],
  #view-compare > p.compare-intro {
    display: none;
  }
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
    line-height: 1.5;
  }
  @media (max-width: 600px) {
    .vs-page-h1 { font-size: 26px; }
    .vs-page-sub { font-size: 15px; }
  }
'''

    og_image = f'{SITE_URL}/og-image.png'

    html = f'''<!DOCTYPE html>
<html lang="{'el' if lang == 'el' else 'en'}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(page_title)}</title>
<meta name="description" content="{esc(page_desc)}">
<meta name="theme-color" content="#0B8FAC">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="el" href="{el_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
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
<link rel="stylesheet" href="/style.css?v={ASSET_V}">
<style>{page_css}</style>
{faq_jsonld}
</head>
<body>

<div id="loading-overlay" style="display:none;">
  <div class="loading-inner">
    <img src="/logo.svg" alt="Aegean Blueprint logo" id="loading-logo">
    <div class="loading-spinner"></div>
    <p>Loading…</p>
  </div>
</div>

<header>
  <div class="header-content">
    <a href="{home_url}" class="logo-wrapper" id="nav-home">
      <img src="/logo-hero.svg" id="site-logo" alt="Aegean Blueprint logo">
      <span id="brand-text"><span class="brand-word">Aegean</span> <span class="brand-word">Blueprint</span></span>
    </a>
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
  <h2 data-i18n="compare.title">Compare Islands</h2>
  <p class="compare-intro" data-i18n="compare.intro">Select two islands to compare side-by-side.</p>
  <div class="compare-selectors">
    <select id="compare-select-a"><option value="" data-i18n="compare.optionA">— Island A —</option></select>
    <span class="vs-label" data-i18n="compare.vs">vs</span>
    <select id="compare-select-b"><option value="" data-i18n="compare.optionB">— Island B —</option></select>
  </div>
  <div id="compare-container">
    <div id="compare-placeholder" class="compare-placeholder" style="display:none;" data-i18n="compare.placeholder">Select two islands above to start comparing.</div>
    <div id="compare-content">
      <div class="compare-radar-wrap">
        <canvas id="compare-radar-chart" role="img" aria-label="Radar chart comparing two islands"></canvas>
      </div>
      <div class="compare-cards" id="compare-cards"></div>
      <div id="compare-verdict" class="compare-verdict" style="{verdict_display}">{prerendered_verdict}</div>
      <div class="compare-section-label" data-i18n="compare.wtv_title">When to visit — overlap</div>
      <div id="compare-wtv" class="compare-wtv"></div>
      <div class="compare-section-label" data-i18n="compare.extra_title">Character &amp; practicalities</div>
      <div id="compare-extra" class="compare-extra"></div>
    </div>
  </div>
</main>

<footer id="site-footer">
  <div class="footer-line">
    <span class="footer-copy" data-i18n="footer.copyright">© 2026 Aegean Blueprint</span> · {privacy_link}<span class="footer-updated" id="footer-updated"></span>
  </div>
</footer>

<script>
window.__INITIAL_COMPARE_PAIR = {init_pair};
</script>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script src="/i18n.js?v=31"></script>
<script src="/script.js?v={ASSET_V}"></script>
</body>
</html>
'''
    return html


def update_sitemap(slugs):
    """Add per-pair URLs to sitemap.xml. Idempotent — replaces the block on re-runs."""
    sitemap_path = ROOT / 'sitemap.xml'
    if not sitemap_path.exists():
        return 0
    xml = sitemap_path.read_text(encoding='utf-8')

    START = '<!-- BEGIN AUTO-GENERATED COMPARE PAGES -->'
    END = '<!-- END AUTO-GENERATED COMPARE PAGES -->'
    today = '2026-06-06'

    entries = []
    for slug in sorted(slugs):
        for path in (f'/compare/{slug}/', f'/el/compare/{slug}/'):
            entries.append(
                f'<url><loc>{SITE_URL}{path}</loc>'
                f'<lastmod>{today}</lastmod>'
                f'<changefreq>monthly</changefreq>'
                f'<priority>0.6</priority></url>'
            )
    block = START + '\n  ' + '\n  '.join(entries) + '\n  ' + END

    if START in xml and END in xml:
        new_xml = re.sub(
            re.escape(START) + r'.*?' + re.escape(END),
            block, xml, count=1, flags=re.DOTALL
        )
    else:
        new_xml = xml.replace('</urlset>', '  ' + block + '\n</urlset>')

    sitemap_path.write_text(new_xml, encoding='utf-8')
    return len(entries)


def cleanup_leftover_dirs(current_slugs):
    """Remove compare/<slug>/ and el/compare/<slug>/ dirs that exist on disk
    but aren't in the current generation set. Protects against stale pages
    from earlier builds lingering and competing in search results.

    Only deletes dirs matching the *-vs-* pattern (paranoia — we never want
    to nuke anything outside the comparison-page namespace)."""
    current = set(current_slugs)
    removed = 0
    for parent in ('compare', 'el/compare'):
        dir_path = ROOT / parent
        if not dir_path.exists():
            continue
        for entry in dir_path.iterdir():
            if not entry.is_dir():
                continue
            name = entry.name
            # Safety guard: only touch dirs that look like comparison slugs
            if '-vs-' not in name:
                continue
            if name in current:
                continue
            # Leftover — remove it
            import shutil
            shutil.rmtree(entry)
            removed += 1
    return removed


def main():
    pair_keys = sorted(VERDICTS.keys())
    valid_pairs = []
    skipped = []
    for pk in pair_keys:
        a, b = parse_pair_key(pk)
        if a in META and b in META:
            valid_pairs.append(pk)
        else:
            skipped.append(pk)

    print(f"Generating static compare pages for {len(valid_pairs)} pairs ({len(skipped)} skipped)")

    slugs = []
    for pk in valid_pairs:
        a, b = parse_pair_key(pk)
        slug = slug_for_pair(a, b)
        slugs.append(slug)

        en_path = ROOT / 'compare' / slug / 'index.html'
        en_path.parent.mkdir(parents=True, exist_ok=True)
        en_path.write_text(render_page(pk, 'en'), encoding='utf-8')

        el_path = ROOT / 'el' / 'compare' / slug / 'index.html'
        el_path.parent.mkdir(parents=True, exist_ok=True)
        el_path.write_text(render_page(pk, 'el'), encoding='utf-8')

    print(f"✓ Wrote {len(valid_pairs) * 2} HTML files ({len(valid_pairs)} EN + {len(valid_pairs)} EL)")

    if skipped:
        print(f"⚠ Skipped pairs with unknown islands:")
        for pk in skipped:
            print(f"   - {pk}")

    removed = cleanup_leftover_dirs(slugs)
    if removed:
        print(f"✓ Cleaned up {removed} leftover comparison dirs (stale from earlier builds)")

    added = update_sitemap(slugs)
    if added:
        print(f"✓ Sitemap updated ({added} URL entries)")

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
