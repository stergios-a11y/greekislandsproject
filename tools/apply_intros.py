#!/usr/bin/env python3
"""Replace intro / intro_el in islands/*.json. Usage: apply_intros.py intros.json"""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
b=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
for k,v in b.items():
    p=ROOT/'islands'/f'{k}.json'; d=json.loads(p.read_text(encoding='utf-8'))
    old=len((d.get('intro') or '').split())
    d['intro']=v['intro']; d['intro_el']=v['intro_el']
    p.write_text(json.dumps(d,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
    print(f'{k}: {old} -> {len(v["intro"].split())} words')
