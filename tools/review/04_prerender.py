#!/usr/bin/env python3
"""Review fixes 2 + 3, crawler side.

The SPA renders the "why this score" line and the visited badge from the island
JSON, but the prerendered #seo-fallback is what Google reads and what a no-JS
visitor sees. This teaches tools/prerender.py to emit both there too, and adds
the empty #blueprint-why slot to the prerendered sidebar shell so hydration has
somewhere to write. Idempotent.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
P = ROOT / 'tools' / 'prerender.py'

WHY_BLOCK = '''
    # "Why this score" — the one sentence that turns the ring into a decision.
    # Written by tools/review/gen_why_score.py, folded into the island JSON by
    # tools/review/02_render.py.
    _why = (data.get('why_score') or {}).get('el' if lang == 'el' else 'en')
    if _why:
        rating_text = rating_text + f'\\n<p class="seo-why">{esc(_why)}</p>'
'''

VISITED_BLOCK = '''
    # Provenance. Only islands that declare provenance.visited say anything —
    # silence must never read as "not visited".
    _vis = (data.get('provenance') or {}).get('visited')
    if _vis:
        _mEN = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December']
        _mEL = ['Ιανουάριο', 'Φεβρουάριο', 'Μάρτιο', 'Απρίλιο', 'Μάιο', 'Ιούνιο',
                'Ιούλιο', 'Αύγουστο', 'Σεπτέμβριο', 'Οκτώβριο', 'Νοέμβριο', 'Δεκέμβριο']
        _parts = str(_vis).split('-')
        _yr = _parts[0]
        _when = _yr
        if len(_parts) > 1 and _parts[1].isdigit() and 1 <= int(_parts[1]) <= 12:
            _mi = int(_parts[1]) - 1
            _when = f'{(_mEL if lang == "el" else _mEN)[_mi]} {_yr}'
        _lbl = 'Το έχω επισκεφθεί' if lang == 'el' else 'Visited by the author'
        last_updated_html = (
            f'<p class="seo-visited">{_lbl} · <strong>{esc(_when)}</strong></p>\\n    '
            + last_updated_html
        )
'''

CSS_LINE = ('  .seo-why {{ margin: 6px 0 0; font-size: .95em; color: var(--ink-2, #5a6472); '
            'border-left: 3px solid var(--aegean, #0B8FAC); padding-left: 9px; }}\n'
            '  .seo-visited {{ margin: 6px 0 0; font-size: .85em; font-weight: 600; '
            'color: var(--olive, #6b7f4b); }}\n')

def main():
    s = P.read_text(encoding='utf-8')
    if 'seo-why' in s:
        print('prerender: already patched'); return 0

    a1 = "        _cp = cluster_prose(key, meta, lang)\n        if _cp:\n            rating_text = rating_text + '\\n' + _cp\n"
    if s.count(a1) != 1:
        print(f'  !! rating_text anchor: {s.count(a1)} matches', file=sys.stderr); return 1
    s = s.replace(a1, a1 + WHY_BLOCK)

    a2 = "    else:\n        last_updated_html = ''\n"
    if s.count(a2) != 1:
        print(f'  !! last_updated anchor: {s.count(a2)} matches', file=sys.stderr); return 1
    s = s.replace(a2, a2 + VISITED_BLOCK)

    a3 = '  .seo-intro p {{ font-size: var(--text-sub, 18px); }}\n'
    if s.count(a3) != 1:
        print(f'  !! css anchor: {s.count(a3)} matches', file=sys.stderr); return 1
    s = s.replace(a3, a3 + CSS_LINE)

    # empty slot in the prerendered sidebar shell, mirroring index.html
    a4 = ('          <a href="#how-we-score" onclick="navMission(event)" class="how-we-score-link" '
          'data-i18n="scoring.howlink">')
    if s.count(a4) != 1:
        print(f'  !! sidebar anchor: {s.count(a4)} matches', file=sys.stderr); return 1
    s = s.replace(a4, '          <p class="blueprint-why" id="blueprint-why" hidden></p>\n' + a4)

    P.write_text(s, encoding='utf-8')
    print('prerender: patched')
    return 0

sys.exit(main())
