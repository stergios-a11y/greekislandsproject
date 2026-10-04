#!/usr/bin/env python3
"""Festival date audit — movable feasts that were stored as fixed dates.

Found while starting the second-source pass. Several entries were entered as the
date the feast happens to fall on in the 2027 season and stored as {"fixed": ...},
so the pages are right for 2027 and wrong for every year after it. Since
SEASON_YEAR rolls to 2028 on 16 August 2027, they would go wrong silently.

Two kinds of problem:

A. Six feasts that are Easter-linked by definition — Corfu's Botides is "11am on
   Holy Saturday", Chios's Rouketopolemos is the midnight Easter liturgy, the
   Folegandros icon tours "the week after Easter", Patmos's Niptiras is Holy
   Thursday, and the Skyrian carnival is Apokries. These become movable dates.

B. Eight Agios Georgios panigiria stored at 23 April. In the Orthodox calendar a
   fixed feast that falls before Pascha is kept after it: St George moves to
   Easter Monday (Bright Monday). Easter 2027 is 2 May, so 23 April lands inside
   Holy Week and all eight panigiria actually happen on 3 May 2027 — the site
   would have published the wrong date on eight islands. This adds an
   "if_before_easter" key to the date schema and teaches feasts.py to honour it,
   so the rule applies in every future year rather than being hard-coded.

The Annunciation entries (25 March, on Karpathos, Schoinoussa, Sifnos and Tinos)
are deliberately NOT touched: that feast is celebrated on its date even in Lent.

Idempotent.
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if not (ROOT / 'festivals.json').exists():
    ROOT = Path(__file__).resolve().parent / 'repo'

# ---------------------------------------------------------------- feasts.py --
FEASTS_OLD = """    if 'fixed' in d:
        mm, dd = d['fixed'].split('-')
        try:
            start = date(year, int(mm), int(dd))
        except ValueError:
            return {'start': None, 'end': None, 'months': [int(mm)], 'exact': False}
"""
FEASTS_NEW = """    if 'fixed' in d:
        mm, dd = d['fixed'].split('-')
        try:
            start = date(year, int(mm), int(dd))
        except ValueError:
            return {'start': None, 'end': None, 'months': [int(mm)], 'exact': False}
        # Orthodox transfer rule: a fixed feast that would fall before Pascha is
        # kept after it instead. Agios Georgios (23 April) is the case that shows
        # up in panigiria — it moves to Easter Monday whenever Easter is later.
        _tgt = d.get('if_before_easter')
        if _tgt:
            _easter = orthodox_easter(year)
            if start < _easter:
                start = _easter + timedelta(days=MOVABLE_OFFSETS.get(_tgt, 1))
"""

# ------------------------------------------------------------- A: movables --
# island -> index -> (expected current fixed value, new date dict, note)
MOVABLE = {
 ('chios', 1):       ('05-01', {'movable': 'holy_saturday'},            'midnight Easter liturgy, Vrondados'),
 ('corfu', 0):       ('05-01', {'movable': 'holy_saturday'},            '11am on Holy Saturday'),
 ('folegandros', 0): ('05-03', {'movable': 'easter', 'offset': 1},      'icon tours the week after Easter'),
 ('patmos', 0):      ('04-26', {'movable': 'easter', 'offset': -6},     'Holy Week at the monastery'),
 ('patmos', 1):      ('04-29', {'movable': 'holy_thursday'},            'Niptiras is Holy Thursday'),
 ('skyros', 0):      ('03-13', {'movable': 'easter', 'offset': -50},    'Apokries weekend, Sat + Sun'),
}

# ------------------------------------------------------- B: Agios Georgios --
ST_GEORGE = [('chania', 1), ('iraklia', 0), ('kos', 2), ('koufonisia', 0),
             ('meganisi', 3), ('naxos', 0), ('skiathos', 4), ('skyros', 7)]

def main():
    changed = 0
    # 1. feasts.py
    p = ROOT / 'tools' / 'feasts.py'
    s = p.read_text(encoding='utf-8')
    if 'if_before_easter' not in s:
        if s.count(FEASTS_OLD) != 1:
            print(f'  !! feasts.py: {s.count(FEASTS_OLD)} matches for the fixed-date branch', file=sys.stderr)
            return 1
        s = s.replace(FEASTS_OLD, FEASTS_NEW)
        p.write_text(s, encoding='utf-8')
        print('  feasts.py: if_before_easter support added')
        changed += 1

    # 2. festivals.json
    fp = ROOT / 'festivals.json'
    data = json.loads(fp.read_text(encoding='utf-8'))
    for (isl, i), (expect, new, note) in MOVABLE.items():
        f = data[isl][i]
        if f.get('date') == new:
            continue
        cur = (f.get('date') or {}).get('fixed')
        if cur != expect:
            print(f'  !! {isl}[{i}]: expected fixed={expect}, found {f.get("date")}', file=sys.stderr)
            return 1
        f['date'] = new
        print(f'  {isl:12}[{i}] fixed {expect} -> {new}   ({note})')
        changed += 1
    for isl, i in ST_GEORGE:
        f = data[isl][i]
        dt = f.get('date') or {}
        if dt.get('if_before_easter'):
            continue
        if dt.get('fixed') != '04-23':
            print(f'  !! {isl}[{i}]: expected fixed=04-23, found {dt}', file=sys.stderr)
            return 1
        dt['if_before_easter'] = 'easter_monday'
        print(f'  {isl:12}[{i}] 04-23 + transfer to Easter Monday when 23 April precedes Pascha')
        changed += 1
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'\n{changed} changes')
    return 0

sys.exit(main())
