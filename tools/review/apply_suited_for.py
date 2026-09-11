#!/usr/bin/env python3
"""Fold a suited_for batch into islands/*.json.

Usage: python3 tools/review/apply_suited_for.py tools/review/suited_for_batch.json

Refuses to overwrite an island that already has a suited_for block — the 15
hand-written ones are the reference set and must not be clobbered. Pass
--overwrite only if you mean it.
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OVER = '--overwrite' in sys.argv
src = [a for a in sys.argv[1:] if not a.startswith('--')][0]
batch = json.loads(Path(src).read_text(encoding='utf-8'))

added = skipped = 0
bad = []
for k, v in sorted(batch.items()):
    p = ROOT / 'islands' / f'{k}.json'
    if not p.exists():
        bad.append(f'{k}: no islands/{k}.json'); continue
    if len(v.get('good', [])) != len(v.get('good_el', [])) or \
       len(v.get('skip', [])) != len(v.get('skip_el', [])):
        bad.append(f'{k}: EN/EL array lengths differ'); continue
    d = json.loads(p.read_text(encoding='utf-8'))
    if d.get('suited_for') and not OVER:
        skipped += 1; continue
    d['suited_for'] = {'good': v['good'], 'good_el': v['good_el'],
                       'skip': v['skip'], 'skip_el': v['skip_el']}
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    added += 1

if bad:
    for b in bad: print('  !!', b, file=sys.stderr)
    sys.exit(1)
total = sum(1 for p in (ROOT / 'islands').glob('*.json')
            if json.loads(p.read_text(encoding='utf-8')).get('suited_for'))
print(f'suited_for: {added} written, {skipped} already present — {total} of 88 islands now have one')
