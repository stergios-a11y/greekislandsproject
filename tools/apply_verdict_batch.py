#!/usr/bin/env python3
"""Splice upgraded verdicts + FAQs into vs_verdicts.json / vs_faqs.json. Usage: apply.py batch.json"""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
b=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
vp,fp=ROOT/'vs_verdicts.json',ROOT/'vs_faqs.json'
v=json.loads(vp.read_text(encoding='utf-8')); f=json.loads(fp.read_text(encoding='utf-8'))
for k,x in b.items():
    assert k in v, k
    v[k]={'en':x['verdict']['en'],'el':x['verdict']['el']}
    f[k]={'en':x['faqs']['en'],'el':x['faqs']['el']}
vp.write_text(json.dumps(v,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
fp.write_text(json.dumps(f,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
print('applied',list(b),'| verdicts',len(v),'faqs',len(f))
