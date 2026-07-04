#!/usr/bin/env python3
"""
Generate Open Graph images (1200x630) for every island in islands/.

Each image shows:
  - "Aegean Blueprint" branding (top-left)
  - Island name (centered, large, Nunito Bold)
  - Italic subtitle (single line, ellipsised if too long)
  - Score badge + island group pill (centered, below subtitle)
  - Aegean colour palette matching the site

Output: og/{key}.jpg (or .png) — committed to the repo and served at
        https://aegeanblueprint.com/og/{key}.jpg

Usage:
  python3 tools/og.py             # regenerate all 78
  python3 tools/og.py naxos       # regenerate just naxos
  python3 tools/og.py naxos andros# regenerate a few

After this runs, the prerenderer (separate change) will reference these
files in the og:image meta tag instead of the generic /logo.png.

Font handling:
  Tries Nunito (the site's display face) first. Falls back to Avenir Next /
  Helvetica Neue / DejaVu Sans / Pillow default in that order. If none of
  the brand fonts are found, prints a warning so you know to install Nunito
  for visual consistency. To install Nunito on Mac:
    brew install --cask font-nunito
  or download from https://fonts.google.com/specimen/Nunito and double-click
  the TTFs to install via Font Book.
"""

import json
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ----------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ISLANDS_DIR = ROOT / 'islands'
OUT_DIR = ROOT / 'og'
OUT_DIR.mkdir(exist_ok=True)

# ----------------------------------------------------------------------
# Brand
# ----------------------------------------------------------------------
W, H = 1200, 630

AEGEAN = (11, 143, 172)        # #0B8FAC
AEGEAN_PALE = (232, 247, 251)  # #E8F7FB
AEGEAN_LIGHT = (200, 238, 245) # #C8EEF5
AEGEAN_DARK = (7, 104, 128)    # #076880
INK_1 = (26, 35, 50)           # #1A2332
INK_2 = (51, 51, 51)
INK_3 = (85, 85, 85)
WHITE = (255, 255, 255)

# ----------------------------------------------------------------------
# Font lookup — tries the site's display face first, then platform fallbacks
# ----------------------------------------------------------------------
FONT_CANDIDATES_BOLD = [
    # Site brand
    'Nunito-Bold.ttf',
    'Nunito-Black.ttf',
    # Mac system fonts (likely on owner's machine)
    '/Library/Fonts/Nunito-Bold.ttf',
    '/System/Library/Fonts/Avenir Next.ttc',
    '/System/Library/Fonts/HelveticaNeue.ttc',
    '/Library/Fonts/Arial Bold.ttf',
    # Linux fallbacks
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf',
]

FONT_CANDIDATES_REGULAR = [
    'Nunito-Regular.ttf',
    '/Library/Fonts/Nunito-Regular.ttf',
    '/System/Library/Fonts/Avenir Next.ttc',
    '/System/Library/Fonts/HelveticaNeue.ttc',
    '/Library/Fonts/Arial.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
]

FONT_CANDIDATES_ITALIC = [
    'Nunito-Italic.ttf',
    '/Library/Fonts/Nunito-Italic.ttf',
    '/System/Library/Fonts/Avenir Next.ttc',
    '/System/Library/Fonts/HelveticaNeue.ttc',
    '/Library/Fonts/Arial Italic.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf',
]

_warned = {'nunito': False}

def _find_font(candidates):
    for c in candidates:
        if Path(c).exists():
            return c
        # also check ~/Library/Fonts on Mac
        user_p = Path.home() / 'Library' / 'Fonts' / c
        if user_p.exists():
            return str(user_p)
    return None

def load_font(size, weight='bold'):
    pool = {
        'bold': FONT_CANDIDATES_BOLD,
        'regular': FONT_CANDIDATES_REGULAR,
        'italic': FONT_CANDIDATES_ITALIC,
    }[weight]
    p = _find_font(pool)
    if p is None:
        return ImageFont.load_default()
    if 'nunito' not in p.lower() and not _warned['nunito']:
        print('  ! Nunito not installed — falling back to', p)
        print('    Install Nunito for brand consistency: brew install --cask font-nunito')
        _warned['nunito'] = True
    try:
        return ImageFont.truetype(p, size)
    except (OSError, IOError):
        return ImageFont.load_default()

# ----------------------------------------------------------------------
# Drawing helpers
# ----------------------------------------------------------------------
def draw_gradient_bg(draw, top, bottom):
    """Vertical linear gradient top -> bottom."""
    for y in range(H):
        t = y / (H - 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

def draw_dotted_line(draw, x1, y, x2, color, dot=3, gap=8):
    x = x1
    while x < x2:
        draw.ellipse([x, y - dot//2, x + dot, y + dot//2 + dot], fill=color)
        x += dot + gap

def text_bbox(draw, text, font):
    """Wrapper that returns (w, h) tuple."""
    l, t, r, b = draw.textbbox((0, 0), text, font=font)
    return r - l, b - t

def truncate_to_width(draw, text, font, max_w):
    """Truncate with ellipsis if text exceeds max_w pixels."""
    w, _ = text_bbox(draw, text, font)
    if w <= max_w:
        return text
    while text and text_bbox(draw, text + '…', font)[0] > max_w:
        text = text[:-1]
    return text.rstrip() + '…'

def fit_text_size(draw, text, weight, max_w, max_size, min_size=40):
    """Find the largest font size at which `text` fits in max_w."""
    size = max_size
    while size > min_size:
        font = load_font(size, weight)
        if text_bbox(draw, text, font)[0] <= max_w:
            return font, size
        size -= 4
    return load_font(min_size, weight), min_size

# ----------------------------------------------------------------------
# Score badge — small rounded bar like the site's beach rating row
# ----------------------------------------------------------------------
def draw_pill(draw, x, y, label, font, fill, fg, padding=18, radius=20):
    """Draw a rounded pill with text. Returns (right_x, bottom_y)."""
    tw, th = text_bbox(draw, label, font)
    w = tw + padding * 2
    h = th + 14
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill)
    # Pillow's textbbox top can differ; small visual offset for vertical centering
    draw.text((x + padding, y + 4), label, font=font, fill=fg)
    return x + w, y + h

def _star_points(cx, cy, r):
    """5-point star polygon points (drawn, not a font glyph — Nunito lacks ★)."""
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    return pts

def draw_score_pill(draw, x, y, score, font, fill, fg, padding=18, radius=20):
    """Rounded score pill with a drawn star + number. Returns (right_x, bottom_y)."""
    label = f'{score:.1f}'
    tw, th = text_bbox(draw, label, font)
    star_r = 13
    star_gap = 10
    w = padding + star_r * 2 + star_gap + tw + padding
    h = th + 14
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill)
    draw.polygon(_star_points(x + padding + star_r, y + h / 2, star_r), fill=fg)
    draw.text((x + padding + star_r * 2 + star_gap, y + 4), label, font=font, fill=fg)
    return x + w, y + h

# ----------------------------------------------------------------------
# Render one OG image
# ----------------------------------------------------------------------
def get_island_meta(key):
    """Read script.js to get score + group + name fallback for the island."""
    # Cache ISLANDS_DATA parse on first call
    if not hasattr(get_island_meta, '_cache'):
        import re
        text = (ROOT / 'script.js').read_text()
        m = re.search(r'const ISLANDS_DATA\s*=\s*\{([\s\S]*?)\};', text)
        if not m:
            get_island_meta._cache = {}
        else:
            cache = {}
            entry_re = re.compile(
                r'"([a-z0-9-]+)"\s*:\s*\{\s*name\s*:\s*"([^"]+)"[^}]*?total\s*:\s*([\d.]+)[^}]*?island_group\s*:\s*"([^"]+)"'
            )
            for m2 in entry_re.finditer(m.group(1)):
                cache[m2.group(1)] = {
                    'name': m2.group(2),
                    'total': float(m2.group(3)),
                    'group': m2.group(4),
                }
            get_island_meta._cache = cache
    return get_island_meta._cache.get(key, {})

# ----------------------------------------------------------------------
# Photo-forward card: hero image background + scrim + overlaid text
# ----------------------------------------------------------------------
def _hero_url(data):
    for day in (data.get('itinerary') or {}).get('days') or []:
        for s in day.get('stops') or []:
            if s.get('photo'):
                return s['photo']
    for b in data.get('beaches') or []:
        if b.get('photo'):
            return b['photo']
    return None

def _bump_size(url):
    """Ask the CDN for a card-sized image so it isn't upscaled/soft."""
    if 'res.cloudinary.com' in url:
        import re
        return re.sub(r'/upload/(?:[^/]*/)?v(\d+)/',
                      '/upload/w_1200,h_630,c_fill,q_auto,f_jpg/v\\1/', url)
    if '/thumb/' in url:
        import re
        return re.sub(r'/\d+px-', '/1200px-', url)
    return url

def _download_img(url):
    import urllib.request
    from io import BytesIO
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh)'})
    raw = urllib.request.urlopen(req, timeout=25).read()
    return Image.open(BytesIO(raw)).convert('RGB')

def _cover(img, w, h):
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x, y = (nw - w) // 2, (nh - h) // 2
    return img.crop((x, y, x + w, y + h))

def _scrim(photo):
    """Darken for legibility: light base wash + strong bottom + soft top."""
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(H):
        a_top = int(150 * max(0.0, 1 - y / 150.0))
        a_bot = int(210 * max(0.0, (y - (H - 360)) / 360.0)) if y > (H - 360) else 0
        a = min(225, 40 + a_top + a_bot)
        od.line([(0, y), (W, y)], fill=(9, 18, 28, a))
    return Image.alpha_composite(photo.convert('RGBA'), overlay).convert('RGB')

def render_photo_card(key, data, photo):
    img = _scrim(_cover(photo, W, H))
    draw = ImageDraw.Draw(img)
    SOFT = (232, 238, 242)

    draw.rectangle([0, 0, W, 6], fill=AEGEAN)
    draw.text((60, 40), 'AEGEAN BLUEPRINT', font=load_font(30, 'bold'), fill=WHITE)
    draw.text((60, 80), 'Greek Islands · A decision engine', font=load_font(20, 'regular'), fill=SOFT)
    url_font = load_font(20, 'regular')
    uw, _ = text_bbox(draw, 'aegeanblueprint.com', url_font)
    draw.text((W - 60 - uw, 52), 'aegeanblueprint.com', font=url_font, fill=SOFT)

    meta = get_island_meta(key)
    name = data.get('name') or meta.get('name') or key.title()
    subtitle = data.get('subtitle') or ''
    score = meta.get('total')
    group = meta.get('group') or ''

    name_font, _ = fit_text_size(draw, name, 'bold', W - 120, max_size=118, min_size=54)
    nw, nh = text_bbox(draw, name, name_font)
    pill_font = load_font(30, 'bold')
    sub_font = load_font(30, 'italic')

    pills_h = 56
    bottom = H - 56
    pills_y = bottom - pills_h
    if subtitle:
        subtitle = truncate_to_width(draw, subtitle, sub_font, W - 120)
        _, sh = text_bbox(draw, subtitle, sub_font)
        sub_y = pills_y - sh - 30
    else:
        sh, sub_y = 0, pills_y
    name_y = sub_y - nh - (36 if subtitle else 20)

    # soft shadow for the name, then the name
    draw.text((62, name_y + 2), name, font=name_font, fill=(0, 0, 0))
    draw.text((60, name_y), name, font=name_font, fill=WHITE)
    if subtitle:
        draw.text((60, sub_y), subtitle, font=sub_font, fill=SOFT)

    cursor = 60
    if score is not None:
        r, _b = draw_score_pill(draw, cursor, pills_y, score, pill_font, AEGEAN, WHITE, padding=18)
        cursor = r + 16
    if group:
        draw_pill(draw, cursor, pills_y, group, pill_font, WHITE, AEGEAN_DARK, padding=18)

    out_path = OUT_DIR / f'{key}.jpg'
    img.save(out_path, 'JPEG', quality=86, optimize=True, progressive=True)
    return out_path

def render_island(key, data):
    """Photo-forward card when a hero photo is available; else the text card."""
    url = _hero_url(data)
    if url:
        try:
            return render_photo_card(key, data, _download_img(_bump_size(url)))
        except Exception as e:
            print(f'  ! {key}: photo unavailable ({e}) — using text card')
    return render_text_card(key, data)

def render_text_card(key, data):
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Background gradient
    draw_gradient_bg(draw, AEGEAN_PALE, WHITE)

    # Subtle top-bar accent
    draw.rectangle([0, 0, W, 6], fill=AEGEAN)

    # Top-left brand
    brand_font = load_font(28, 'bold')
    draw.text((60, 38), 'AEGEAN BLUEPRINT', font=brand_font, fill=AEGEAN_DARK)
    sub_brand = load_font(20, 'regular')
    draw.text((60, 76), 'Greek Islands · A decision engine', font=sub_brand, fill=INK_3)

    # Top-right: site URL
    url_font = load_font(20, 'regular')
    url_text = 'aegeanblueprint.com'
    uw, _ = text_bbox(draw, url_text, url_font)
    draw.text((W - 60 - uw, 50), url_text, font=url_font, fill=INK_3)

    # Island name — centered, sized to fit
    name = data.get('name') or get_island_meta(key).get('name') or key.title()
    name_font, name_size = fit_text_size(draw, name, 'bold', W - 120, max_size=140, min_size=60)
    nw, nh = text_bbox(draw, name, name_font)
    name_y = 220
    draw.text(((W - nw) / 2, name_y), name, font=name_font, fill=INK_1)

    # Subtitle — centred, italic, single line, truncated
    subtitle = data.get('subtitle') or ''
    if subtitle:
        sub_font = load_font(28, 'italic')
        subtitle = truncate_to_width(draw, subtitle, sub_font, W - 160)
        sw, sh = text_bbox(draw, subtitle, sub_font)
        sub_y = name_y + nh + 24
        draw.text(((W - sw) / 2, sub_y), subtitle, font=sub_font, fill=INK_3)
    else:
        sub_y = name_y + nh + 24
        sh = 0

    # Decorative dotted rule under subtitle
    rule_y = sub_y + sh + 36
    rule_w = 200
    draw_dotted_line(draw, (W - rule_w) / 2, rule_y, (W + rule_w) / 2, AEGEAN, dot=4, gap=10)

    # Score badge + group pill (centered, side by side)
    meta = get_island_meta(key)
    score = meta.get('total')
    group = meta.get('group') or ''

    pill_font = load_font(28, 'bold')
    badge_y = rule_y + 36

    # Build the labels first to compute total width and center them
    group_label = group
    pad = 18
    # Score pill uses a drawn star (Nunito has no ★ glyph); measure its width.
    score_str = f'{score:.1f}' if score is not None else ''
    sw, _ = text_bbox(draw, score_str, pill_font) if score_str else (0, 0)
    gw, _ = text_bbox(draw, group_label, pill_font) if group_label else (0, 0)

    score_pill_w = (pad + 26 + 10 + sw + pad) if score_str else 0
    group_pill_w = gw + pad * 2 + 4 if group_label else 0
    gap = 16
    total_w = score_pill_w + (gap if score_str and group_label else 0) + group_pill_w

    cursor = (W - total_w) / 2
    if score_str:
        draw_score_pill(draw, cursor, badge_y, score, pill_font, AEGEAN, WHITE, padding=pad)
        cursor += score_pill_w + gap
    if group_label:
        draw_pill(draw, cursor, badge_y, group_label, pill_font, AEGEAN_LIGHT, AEGEAN_DARK, padding=pad)

    # Save
    out_path = OUT_DIR / f'{key}.jpg'
    img.save(out_path, 'JPEG', quality=88, optimize=True, progressive=True)
    return out_path

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    args = sys.argv[1:]
    keys = args if args else None

    json_files = sorted(ISLANDS_DIR.glob('*.json'))
    if keys:
        json_files = [f for f in json_files if f.stem in keys]
        if not json_files:
            print(f'No matching island JSONs found for: {", ".join(keys)}')
            return

    print(f'Generating OG images for {len(json_files)} island(s) -> {OUT_DIR}/')
    for f in json_files:
        key = f.stem
        try:
            data = json.loads(f.read_text())
        except Exception as e:
            print(f'  ✗ {key}: invalid JSON — {e}')
            continue
        out = render_island(key, data)
        size_kb = out.stat().st_size // 1024
        print(f'  ✓ {key}.jpg  ({size_kb} KB)')

    print(f'\nDone. {len(json_files)} OG images written to {OUT_DIR}/')
    print('Next: deploy and verify at https://aegeanblueprint.com/og/{key}.jpg')

if __name__ == '__main__':
    main()
