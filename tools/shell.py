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


def render(_tpl, **kw):
    return _PH.sub(lambda m: str(kw[m.group(1)]), template(_tpl))


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


def optional(_tpl, **kw):
    """Render a template if this market (or the engine) has it, else ''."""
    try:
        return render(_tpl, **kw)
    except FileNotFoundError:
        return ''


def lang_info(code):
    return next(l for l in M.languages() if l['code'] == code)


def page_head(title, desc, urls, lang, style_v, og_title=None, og_image=None, extra='', close=True):
    """<!DOCTYPE> … <head> contents. urls = {lang: absolute url} for this page in every language.
    close=False leaves </head> to the caller (pages that append their own <style>)."""
    b = brand()
    out = render('page_head.html', lang=lang, title=esc(title), desc=esc(desc), url=urls[lang],
                 hreflang=M.hreflang(urls), theme_color=b['theme_color'], author=b['author'],
                 og_title=esc(og_title if og_title is not None else title),
                 og_image=og_image or b['site_url'] + b['og_image'],
                 og_locale=lang_info(lang).get('og_locale', lang), site_name=b['site_name'],
                 analytics=analytics(), style_v=style_v, extra=extra, head_extra=b.get('head_extra', ''))
    return out + '\n</head>' if close else out


def brand_html():
    return ' '.join(f'<span class="brand-word">{w}</span>' for w in brand()['brand_words'])


def nav_html(lang, active=''):
    home = M.lang_prefix(lang) + '/'
    out = []
    for item in M.config()['nav']:
        out.append(render('partials/nav_link.html', href=home + item['href'],
                          id_attr=f' id="{item["dom_id"]}"' if item.get('dom_id') else '',
                          active=' class="active"' if active and item.get('id') == active else '',
                          label=label(item['label'], lang)))
    return '\n'.join(out)


def site_header(lang, toggle_href, active=''):
    """Header for static pages (no script.js): plain link to the other language."""
    b = brand()
    others = [c for c in M.langs() if c != lang]
    toggle = render('partials/lang_toggle_static.html', href=toggle_href, label=others[0].upper()) if others else ''
    return render('site_header.html', home=M.lang_prefix(lang) + '/', logo=b['logo'], site_name=b['site_name'],
                  brand_html=brand_html(), nav=nav_html(lang, active), lang_toggle=toggle)


def app_header(lang, active=''):
    """Header for pages that run script.js: loading overlay + language dropdown."""
    b = brand()
    dd = ''
    if len(M.langs()) > 1:
        opts = '\n'.join(render('partials/lang_option.html', code=l['code'], flag=l.get('flag', ''), name=l['name'])
                         for l in M.languages())
        dd = render('partials/lang_dropdown.html', current=lang.upper(), options=opts)
    return render('app_header.html', home=M.lang_prefix(lang) + '/', logo=b['logo'],
                  loading_logo=b.get('loading_logo', b['logo']), site_name=b['site_name'],
                  brand_html=brand_html(), nav=nav_html(lang, active), lang_dropdown=dd)


def footer_links(lang):
    home = M.lang_prefix(lang) + '/'
    return ' · '.join(render('partials/footer_link.html', href=home + f['href'], i18n=f.get('i18n', ''),
                             label=label(f['label'], lang)) for f in M.config().get('footer_links', []))


def app_footer(lang, year):
    home = M.lang_prefix(lang) + '/'
    return render('app_footer.html', affiliate_cta=optional('partials/affiliate_cta.html', home=home),
                  year=year, site_name=brand()['site_name'], links=footer_links(lang))


def footer(year, close=True):
    """Footer with {privacy}/{credits}/{lang_link}... left for the builder to fill.
    close=True also ends the document (</body></html>)."""
    seg = template('partials/footer_lang.html') if len(M.langs()) > 1 else ''
    out = render('footer.html', year=year, site_name=brand()['site_name'], lang_segment=seg)
    return out + '\n</body>\n</html>' if close else out


def static_footer(lang, other_href, year):
    """footer() with every slot filled from the market config."""
    home = M.lang_prefix(lang) + '/'
    links = {f['href'].strip('/'): f for f in M.config().get('footer_links', [])}
    others = [c for c in M.langs() if c != lang]
    return footer(year, close=False).format(
        lang_link=other_href, lang_label=lang_info(others[0])['name'] if others else '',
        privacy=home + 'privacy/', privacy_label=label(links['privacy']['label'], lang),
        credits=home + 'credits/', credits_label=label(links['credits']['label'], lang))
