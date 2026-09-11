#!/usr/bin/env python3
"""Replace intro / intro_el in islands/*.json.
Usage: python3 tools/review/apply_intros.py tools/review/intros_batch2.json"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
b = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
for k, v in b.items():
    p = ROOT / 'islands' / f'{k}.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    old, old_el = len((d.get('intro') or '').split()), len((d.get('intro_el') or '').split())
    d['intro'] = v['intro']; d['intro_el'] = v['intro_el']
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'{k:12} EN {old:3d} -> {len(v["intro"].split()):3d}   EL {old_el:3d} -> {len(v["intro_el"].split()):3d}')
