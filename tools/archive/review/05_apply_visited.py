#!/usr/bin/env python3
"""Fold tools/review/visited.json into islands/<key>.json as provenance.visited.

Only non-null entries are written. Clearing an entry back to null removes the
field again, so the file stays the single source of truth. Run the build chain
afterwards (prerender at minimum) to refresh the crawler-visible badge.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
src = json.loads((ROOT / 'tools/review/visited.json').read_text(encoding='utf-8'))
vis = src.get('visited', src)

bad = [k for k, v in vis.items() if v and not re.fullmatch(r'\d{4}(-(0[1-9]|1[0-2]))?', str(v))]
if bad:
    print('  !! bad date format (want YYYY or YYYY-MM):', ', '.join(bad), file=sys.stderr)
    sys.exit(1)

added = removed = 0
for p in sorted((ROOT / 'islands').glob('*.json')):
    d = json.loads(p.read_text(encoding='utf-8'))
    k = d.get('key')
    want = vis.get(k)
    have = (d.get('provenance') or {}).get('visited')
    if want == have:
        continue
    prov = d.get('provenance') or {}
    if want:
        prov['visited'] = want; added += 1
    else:
        prov.pop('visited', None); removed += 1
    if prov:
        d['provenance'] = prov
    else:
        d.pop('provenance', None)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

print(f'provenance: {added} set, {removed} cleared, '
      f'{sum(1 for v in vis.values() if v)} islands marked visited')
