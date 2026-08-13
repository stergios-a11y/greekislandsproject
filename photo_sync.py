#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""photo_sync.py — drop photos in a folder, get them onto the island page.

Replaces the manual loop of: upload by hand -> copy 15 URLs -> paste them into
chat -> have someone match them to stops by reading the filenames. Filenames
have already had typos twice (κοθφονησια, χρωα); this matches against the real
stop and beach names in islands/*.json instead of trusting the filename.

WHAT IT DOES
  1. Reads every image in a folder.
  2. Checks pixel size BEFORE uploading. The site renders photos at 640x420,
     so anything narrower is rejected — that is how the 386x518 Salamina shot
     should have been caught.
  3. Uploads to Cloudinary with an UNSIGNED preset (no API secret anywhere).
  4. Matches each file to a stop or beach card by name, accent-insensitively,
     in Greek or English.
  5. Writes the URL into islands/<key>.json.

SETUP (once)
  Cloudinary dashboard -> Settings -> Upload -> Upload presets -> Add preset
    Signing mode: Unsigned
    Name it e.g. "aegean_unsigned"
  Then:
    export CLOUDINARY_CLOUD_NAME=dothbs5hs
    export CLOUDINARY_UPLOAD_PRESET=aegean_unsigned

USAGE
    python3 tools/photo_sync.py ~/photos/ikaria              # folder name = island key
    python3 tools/photo_sync.py ~/photos/shots --island ikaria
    python3 tools/photo_sync.py ~/photos/ikaria --dry-run    # match only, no upload
    python3 tools/photo_sync.py ~/photos/ikaria --replace    # also overwrite filled slots

NAMING
  Name files after the place: "seychelles.jpg", "αρμενιστης.jpg", "nas beach.jpg".
  A trailing _2 sends that photo to the BEACH CARD when the same place is also
  an itinerary stop — which is how you stop the same image appearing twice on
  one page (the Agali/Kathisma/Kanakia bug).
"""
import argparse
import json
import mimetypes
import os
import re
import struct
import sys
import unicodedata
import urllib.request
import uuid
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ISLANDS = ROOT / 'islands'
RENDER_W, RENDER_H = 640, 420          # must match content_img_640() in prerender.py

# Words that appear in slot names but carry no identifying information.
STOP_WORDS = {
    'beach', 'stop', 'the', 'and', 'a', 'to', 'in', 'at', 'of', 'or', 'from',
    'day', 'visit', 'walk', 'drive', 'boat', 'village', 'town', 'port',
    'παραλια', 'στη', 'στο', 'στον', 'στην', 'και', 'του', 'της', 'το', 'η', 'ο',
    'χωριο', 'λιμανι', 'μερα',
}


def norm(s):
    """Accent-insensitive, case-insensitive, final-sigma-insensitive."""
    s = unicodedata.normalize('NFD', str(s))
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = unicodedata.normalize('NFC', s).lower().replace('ς', 'σ')
    return re.sub(r'[^0-9a-zα-ω]+', ' ', s).strip()


def tokens(s):
    return {t for t in norm(s).split() if t and t not in STOP_WORDS and len(t) > 2}


def clean_stem(path):
    """'αγκαλη_2_u7q2z3.jpg' -> ('αγκαλη', 2). Strips Cloudinary's random suffix."""
    stem = path.stem
    stem = re.sub(r'_[a-z0-9]{6}$', '', stem)          # cloudinary public-id suffix
    m = re.search(r'[_\-\s](\d)$', stem)
    variant = int(m.group(1)) if m else 1
    if m:
        stem = stem[:m.start()]
    return stem, variant


def image_size(path):
    """(w, h) for JPEG/PNG/WebP using file headers only — no Pillow needed."""
    with open(path, 'rb') as f:
        head = f.read(32)
        if head[:8] == b'\x89PNG\r\n\x1a\n':
            w, h = struct.unpack('>II', head[16:24])
            return w, h
        if head[:2] == b'\xff\xd8':                     # JPEG: walk the segments
            f.seek(2)
            while True:
                b = f.read(1)
                while b and b != b'\xff':
                    b = f.read(1)
                while b == b'\xff':
                    b = f.read(1)
                if not b:
                    break
                marker = b[0]
                if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                    continue
                ln = struct.unpack('>H', f.read(2))[0]
                if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                    f.read(1)
                    h, w = struct.unpack('>HH', f.read(4))
                    return w, h
                f.seek(ln - 2, os.SEEK_CUR)
        if head[:4] == b'RIFF' and head[8:12] == b'WEBP':
            f.seek(12)
            chunk = f.read(8)
            typ = chunk[:4]
            if typ == b'VP8X':
                d = f.read(10)
                w = 1 + int.from_bytes(d[4:7], 'little')
                h = 1 + int.from_bytes(d[7:10], 'little')
                return w, h
            if typ == b'VP8 ':
                d = f.read(10)
                return struct.unpack('<HH', d[6:10])[0] & 0x3FFF, struct.unpack('<HH', d[6:10])[1] & 0x3FFF
            if typ == b'VP8L':
                d = f.read(5)
                bits = int.from_bytes(d[1:5], 'little')
                return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    return None, None


def load_slots(key):
    """Every fillable slot on an island, with the names we can match against."""
    path = ISLANDS / f'{key}.json'
    if not path.exists():
        sys.exit(f'No such island: {path}')
    data = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=OrderedDict)
    it = data.get('itinerary')
    days = it.get('days', []) if isinstance(it, dict) else (it or [])
    slots = []
    for di, day in enumerate(days, 1):
        for s in day.get('stops', []):
            slots.append({'kind': 'stop', 'obj': s, 'where': f'day {di}',
                          'names': [s.get('name', ''), s.get('name_el', '')]})
    for b in (data.get('beaches') or []):
        slots.append({'kind': 'beach', 'obj': b, 'where': 'beach card',
                      'names': [b.get('name', ''), b.get('name_el', '')]})
    return data, path, slots


def akin(a, b, min_prefix=4):
    """Do two words refer to the same thing despite inflection?

    Greek slot names are often genitive while a filename is nominative:
    'αγιος νικολαος' vs 'Παραλία Αγίου Νικολάου'. Exact token equality misses
    every one of those. Comparing on a shared leading stem catches them
    (αγιο|ς / αγιο|υ, νικολα|ος / νικολα|ου) and costs nothing in Latin, where
    it also forgives Karavostasi / Karavostasis.
    """
    if a == b:
        return True
    n = min(len(a), len(b))
    if n < min_prefix:
        return False
    keep = max(min_prefix, n - 3)          # allow up to a 3-letter ending to differ
    return a[:keep] == b[:keep]


def score(file_tokens, slot):
    """Fraction of the filename's words that appear in the slot name."""
    best = 0.0
    for n in slot['names']:
        st = tokens(n)
        if not st or not file_tokens:
            continue
        hit = sum(1 for ft in file_tokens if any(akin(ft, s) for s in st))
        best = max(best, hit / len(file_tokens))
    return best


def upload(path, cloud, preset):
    """Unsigned Cloudinary upload. Multipart built by hand to avoid dependencies."""
    url = f'https://api.cloudinary.com/v1_1/{cloud}/image/upload'
    boundary = uuid.uuid4().hex
    ctype = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
    body = b''
    for field, value in (('upload_preset', preset),):
        body += (f'--{boundary}\r\nContent-Disposition: form-data; name="{field}"\r\n\r\n'
                 f'{value}\r\n').encode()
    body += (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; '
             f'filename="{path.name}"\r\nContent-Type: {ctype}\r\n\r\n').encode()
    body += path.read_bytes() + f'\r\n--{boundary}--\r\n'.encode()
    req = urllib.request.Request(url, data=body, headers={
        'Content-Type': f'multipart/form-data; boundary={boundary}'})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())['secure_url']


def main():
    ap = argparse.ArgumentParser(description='Upload island photos and wire them into the JSON.')
    ap.add_argument('folder')
    ap.add_argument('--island', help='island key (defaults to the folder name)')
    ap.add_argument('--dry-run', action='store_true', help='match only; upload nothing')
    ap.add_argument('--replace', action='store_true', help='overwrite slots that already have a photo')
    ap.add_argument('--min-score', type=float, default=0.5)
    args = ap.parse_args()

    folder = Path(args.folder).expanduser()
    if not folder.is_dir():
        sys.exit(f'Not a folder: {folder}')
    key = args.island or folder.name
    cloud = os.environ.get('CLOUDINARY_CLOUD_NAME')
    preset = os.environ.get('CLOUDINARY_UPLOAD_PRESET')
    if not args.dry_run and not (cloud and preset):
        sys.exit('Set CLOUDINARY_CLOUD_NAME and CLOUDINARY_UPLOAD_PRESET, or use --dry-run.')

    data, path, slots = load_slots(key)
    files = sorted(p for p in folder.iterdir()
                   if p.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp'})
    if not files:
        sys.exit(f'No images in {folder}')

    print(f'{len(files)} images -> {data.get("name", key)}  ({len(slots)} slots)\n')
    taken, plan, skipped = set(), [], []

    for f in files:
        stem, variant = clean_stem(f)
        w, h = image_size(f)
        if w and w < RENDER_W:
            skipped.append((f.name, f'{w}x{h} — narrower than the {RENDER_W}px render width'))
            continue
        if w and h and h < RENDER_H:
            skipped.append((f.name, f'{w}x{h} — shorter than the {RENDER_H}px render height'))
            continue
        ft = tokens(stem)
        # Empty slots outrank filled ones at equal confidence. Without this,
        # "marmari_2" would overwrite the Marmari beach card while the genuinely
        # empty "Drive back to Marmari" stop stayed blank.
        ranked = sorted(((score(ft, s), i, s) for i, s in enumerate(slots)),
                        key=lambda t: (bool(t[2]['obj'].get('photo')), -t[0]))
        # A "_2" file prefers the beach card, so a place that is both a stop and
        # a card does not show the identical image twice.
        pick = None
        for sc, i, s in ranked:
            if sc < args.min_score or i in taken:
                continue
            if variant >= 2 and s['kind'] == 'stop':
                alt = next((j for scj, j, sj in ranked
                            if scj >= args.min_score and sj['kind'] == 'beach' and j not in taken), None)
                if alt is not None:
                    pick = (ranked[[x[1] for x in ranked].index(alt)][0], alt, slots[alt])
                    break
            pick = (sc, i, s)
            break
        if not pick:
            skipped.append((f.name, 'no slot matched — rename it after the place'))
            continue
        sc, i, s = pick
        if s['obj'].get('photo') and not args.replace:
            skipped.append((f.name, f'{s["names"][0]} already has a photo (use --replace)'))
            continue
        taken.add(i)
        # Note the next-best candidate when it is nearly as good — the place name
        # usually matches but the qualifier ("return", "sunset") may not, so a
        # close second is a hint to check this one by eye.
        runner = next((sj['names'][0] for scj, j, sj in ranked
                       if j != i and scj >= sc - 0.001 and scj >= args.min_score), None)
        plan.append((f, s, sc, f'{w}x{h}', runner))

    for f, s, sc, dims, runner in plan:
        amb = f'   ambiguous, also matches: {runner}' if runner else ''
        print(f'  {f.name:<38} -> {s["where"]:<11} {s["names"][0]:<34} '
              f'[{dims}, match {sc:.0%}]{amb}')
    if skipped:
        print('\n  skipped:')
        for n, why in skipped:
            print(f'    {n:<38} {why}')

    if args.dry_run:
        print('\ndry run — nothing uploaded, nothing written.')
        return
    if not plan:
        print('\nnothing to do.')
        return

    print()
    for f, s, sc, dims, runner in plan:
        try:
            s['obj']['photo'] = upload(f, cloud, preset)
            s['obj'].setdefault('photo_credit', None)
            print(f'  uploaded {f.name}')
        except Exception as e:
            print(f'  FAILED   {f.name}: {e}')

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    gaps = sum(1 for s in slots if not s['obj'].get('photo'))
    print(f'\n{path.name} written. Slots still empty: {gaps}')
    print('Now run:  python3 tools/prerender.py && python3 tools/build_compare_pages.py '
          '&& python3 tools/build_festival_extras.py && python3 tools/build_match_page.py')


if __name__ == '__main__':
    main()
