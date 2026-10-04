#!/usr/bin/env python3
"""Page shell — head, header and footer shared by the static page builders.

Markup lives in templates/*.html with {{name}} placeholders (logic stays here, markup there).
A market overrides any template by shipping a file of the same name in
markets/<market>/templates/. Brand and menu come from markets/<market>/market.json.
"""
import re

import market as M

TPL_DIRS = [M.MDIR / 'templates', M.ROOT / 'templates']
_PH = re.compile(r'\{\{\s*(\w+)\s*\}\}')


def template(name):
    for d in TPL_DIRS:
        p = d / name
        if p.exists():
            return p.read_text(encoding='utf-8').rstrip('\n')
    raise FileNotFoundError(f'template {name} not found in {[str(d) for d in TPL_DIRS]}')


def render(name, **kw):
    return _PH.sub(lambda m: str(kw[m.group(1)]), template(name))


def esc(s):
    return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def brand():
    return M.config()['brand']


def label(d, lang):
    """Per-language label dict -> text, falling back to the market's default language."""
    return d.get(lang) or d[M.default_lang()]


def analytics():
    g = brand().get('ga_id')
    return render('partials/analytics.html', ga_id=g) if g else ''


def page_head(title, desc, urls, lang, style_v):
    """urls = {lang: absolute url} for this page in every language it exists in."""
    b = brand()
    return render('page_head.html', lang=lang, title=esc(title), desc=esc(desc), url=urls[lang],
                  hreflang=M.hreflang(urls), theme_color=b['theme_color'], author=b['author'],
                  site_url=b['site_url'], og_image=b['og_image'], logo=b['logo'],
                  analytics=analytics(), style_v=style_v, head_extra=b.get('head_extra', ''))


def brand_html():
    return ' '.join(f'<span class="brand-word">{w}</span>' for w in brand()['brand_words'])


def site_header(lang, toggle_href, active=''):
    b = brand()
    home = M.lang_prefix(lang) + '/'
    links = []
    for item in M.config()['nav']:
        on = ' class="active"' if active and item.get('id') == active else ''
        links.append(render('partials/nav_link.html', href=home + item['href'], active=on,
                            label=label(item['label'], lang)))
    others = [c for c in M.langs() if c != lang]
    toggle = render('partials/lang_toggle_static.html', href=toggle_href, label=others[0].upper()) if others else ''
    return render('site_header.html', home=home, logo=b['logo'], site_name=b['site_name'],
                  brand_html=brand_html(), nav='\n'.join(links), lang_toggle=toggle)


def footer(year):
    """Footer with {privacy}/{credits}/{lang_link}... left for the builder to fill."""
    seg = template('partials/footer_lang.html') if len(M.langs()) > 1 else ''
    return render('footer.html', year=year, site_name=brand()['site_name'], lang_segment=seg)
