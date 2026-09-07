#!/usr/bin/env python3
"""Splice FAQ-only batches into vs_faqs.json. Usage: apply_faqs.py faqs.json"""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
b=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
fp=ROOT/'vs_faqs.json'; v=json.loads((ROOT/'vs_verdicts.json').read_text(encoding='utf-8'))
f=json.loads(fp.read_text(encoding='utf-8'))
for k,x in b.items():
    assert k in v, k
    assert len(x['en'])==5 and len(x['el'])==5, k
    f[k]={'en':x['en'],'el':x['el']}
fp.write_text(json.dumps(f,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
print('applied',len(b),'pairs | vs_faqs.json now',len(f),'of',len(v))
