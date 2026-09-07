#!/usr/bin/env python3
"""Append researched beaches to islands/<key>.json. Usage: apply_beaches.py new_beaches.json"""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
b=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
for isl,new in b.items():
    p=ROOT/'islands'/f'{isl}.json'; d=json.loads(p.read_text(encoding='utf-8'))
    have={x['name'] for x in d['beaches']}
    added=[x for x in new if x['name'] not in have]
    d['beaches'].extend(added)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
    print(f'{isl}: +{len(added)} -> {len(d["beaches"])} beaches')
