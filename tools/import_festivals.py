#!/usr/bin/env python3
"""One-off: build festivals.json (the festival master list) from
  1. the curated `festivals` arrays in islands/*.json (owner-written, verified), and
  2. a researched inventory (research JSON, schema in tools/festival_schema.md).

Researched entries carrying "replaces": "<existing name>" upgrade an existing
entry with a structured date / village / type / source but KEEP the owner's
description and photo (the researched text is kept as desc_research for review).

Usage: python3 tools/import_festivals.py research.json
Re-running is safe: festivals.json is rebuilt from scratch each time.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from feasts import MONTHS_EN  # noqa: E402

_MONTH_NUM = {m.lower(): i + 1 for i, m in enumerate(MONTHS_EN)}
_MONTH_NUM.update({'sept': 9})


def parse_when(when):
    """Best-effort structured date from an owner-written 'when' string."""
    s = (when or '').strip()
    low = s.lower()
    # "D–D Month" range
    m = re.search(r'(\d{1,2})\s*[–\-]\s*(\d{1,2})\s+([a-z]+)', low)
    if m and m.group(3) in _MONTH_NUM:
        mo = _MONTH_NUM[m.group(3)]
        a, b = int(m.group(1)), int(m.group(2))
        return {'fixed': f'{mo:02d}-{a:02d}'}, max(1, b - a + 1)
    # "D Month"
    m = re.search(r'\b(\d{1,2})\s+([a-z]+)', low)
    if m and m.group(2) in _MONTH_NUM:
        return {'fixed': f'{_MONTH_NUM[m.group(2)]:02d}-{int(m.group(1)):02d}'}, 1
    # "Month D"
    m = re.search(r'\b([a-z]+)\s+(\d{1,2})\b', low)
    if m and m.group(1) in _MONTH_NUM:
        return {'fixed': f'{_MONTH_NUM[m.group(1)]:02d}-{int(m.group(2)):02d}'}, 1
    if 'easter monday' in low:
        return {'movable': 'easter', 'offset': 1}, 1
    if 'holy saturday' in low or 'easter saturday' in low:
        return {'movable': 'easter', 'offset': -1}, 1
    if 'good friday' in low:
        return {'movable': 'easter', 'offset': -2}, 1
    if 'pentecost' in low or 'whit' in low or 'holy spirit' in low:
        return {'movable': 'easter', 'offset': 50}, 1
    if 'clean monday' in low:
        return {'movable': 'easter', 'offset': -48}, 1
    if 'easter' in low:
        return {'movable': 'easter', 'offset': 0}, 1
    # approx
    months = set()
    for name, num in _MONTH_NUM.items():
        if re.search(r'\b' + name + r'\b', low):
            months.add(num)
    rng = re.search(r'([a-z]+)\s+(?:through|to|until|-|–)\s+(?:early\s+|mid-|late\s+)?([a-z]+)', low)
    if rng and rng.group(1) in _MONTH_NUM and rng.group(2) in _MONTH_NUM:
        a, b = _MONTH_NUM[rng.group(1)], _MONTH_NUM[rng.group(2)]
        months.update(range(a, b + 1) if a <= b else list(range(a, 13)) + list(range(1, b + 1)))
    if not months and ('apokries' in low or 'carnival' in low or 'pre-lent' in low):
        months.update([2, 3])
    return {'approx': s, 'months': sorted(months)}, 1


def guess_type(name, desc):
    t = (name + ' ' + desc).lower()
    if 'carnival' in t or 'apokries' in t:
        return 'carnival'
    if 'panigiri' in t or 'panigyri' in t or 'feast' in t:
        return 'panigiri'
    if any(w in t for w in ('wine', 'pistachio', 'fish', 'honey', 'harvest', 'sardine', 'mastic', 'cheese', 'gastronom')):
        return 'food'
    if any(w in t for w in ('music', 'jazz', 'concert', 'rebetiko')):
        return 'music'
    if any(w in t for w in ('procession', 'pilgrim', 'litany', 'icon', 'monastery', 'saint', 'agios', 'agia', 'panagia', 'dormition')):
        return 'religious'
    if any(w in t for w in ('regatta', 'race', 'run', 'marathon')):
        return 'sport'
    return 'cultural'


def main(research_path):
    research = json.loads(Path(research_path).read_text(encoding='utf-8'))
    out = {}
    stats = {'existing': 0, 'replaced': 0, 'new': 0}
    for p in sorted((ROOT / 'islands').glob('*.json')):
        d = json.loads(p.read_text(encoding='utf-8'))
        key = d['key']
        entries = []
        existing = [f for f in (d.get('festivals') or []) if isinstance(f, dict)]
        new = research.get(key, [])
        replaced_names = {e['replaces'] for e in new if e.get('replaces')}
        for f in existing:
            if f.get('name') in replaced_names:
                continue
            date, dur = parse_when(f.get('when', ''))
            e = {
                'name': f.get('name', ''), 'name_el': f.get('name_el') or f.get('name', ''),
                'date': date, 'eve': False, 'duration_days': dur,
                'type': guess_type(f.get('name', ''), f.get('desc', '')),
                'when': f.get('when', ''), 'when_el': f.get('when_el') or f.get('when', ''),
                'desc': f.get('desc', ''), 'desc_el': f.get('desc_el') or f.get('desc', ''),
                'verified': True,
            }
            for k in ('photo', 'photo_credit', 'image'):
                if f.get(k):
                    e[k] = f[k]
            entries.append(e); stats['existing'] += 1
        for r in new:
            e = {k: v for k, v in r.items() if k not in ('replaces', 'island')}
            e.setdefault('eve', False); e.setdefault('duration_days', 1)
            e['verified'] = False
            if r.get('replaces'):
                old = next((f for f in existing if f.get('name') == r['replaces']), None)
                if old:
                    e['desc_research'] = e.get('desc', '')
                    e['desc_el_research'] = e.get('desc_el', '')
                    e['desc'] = old.get('desc') or e.get('desc', '')
                    e['desc_el'] = old.get('desc_el') or e.get('desc_el', '')
                    for k in ('photo', 'photo_credit', 'image'):
                        if old.get(k):
                            e[k] = old[k]
                    e['verified'] = True
                    stats['replaced'] += 1
            else:
                stats['new'] += 1
            entries.append(e)
        if entries:
            out[key] = entries
    (ROOT / 'festivals.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    total = sum(len(v) for v in out.values())
    print(f'festivals.json: {total} festivals on {len(out)} islands  ({stats})')


if __name__ == '__main__':
    main(sys.argv[1])
