#!/usr/bin/env python3
"""Movable-feast engine + date resolution for festivals.json.

Every festival carries a structured `date`:
    {"fixed": "MM-DD"}                      fixed saint's day / fixed event
    {"movable": "easter", "offset": N}      N days from Orthodox Easter Sunday
    {"approx": "mid-September", "months": [9]}   no exact date

resolve(date, year, eve=False, duration_days=1) -> dict with
    start (date | None), end (date | None), months [ints], exact (bool)

Orthodox Easter uses the Meeus Julian algorithm, converted to Gregorian
(valid 1900-2099: Julian-Gregorian offset = 13 days).
"""
from datetime import date, timedelta

MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
             'August', 'September', 'October', 'November', 'December']
# Genitive, as used after a day number: "15 Αυγούστου"
MONTHS_EL_GEN = ['Ιανουαρίου', 'Φεβρουαρίου', 'Μαρτίου', 'Απριλίου', 'Μαΐου', 'Ιουνίου',
                 'Ιουλίου', 'Αυγούστου', 'Σεπτεμβρίου', 'Οκτωβρίου', 'Νοεμβρίου', 'Δεκεμβρίου']
MONTHS_EL_NOM = ['Ιανουάριος', 'Φεβρουάριος', 'Μάρτιος', 'Απρίλιος', 'Μάιος', 'Ιούνιος',
                 'Ιούλιος', 'Αύγουστος', 'Σεπτέμβριος', 'Οκτώβριος', 'Νοέμβριος', 'Δεκέμβριος']

# Named offsets from Easter Sunday, so data can say {"movable": "pentecost"}.
MOVABLE_OFFSETS = {
    'easter': 0,
    'clean_monday': -48,
    'cheese_sunday': -49,       # last Sunday of Apokries
    'lazarus_saturday': -8,
    'palm_sunday': -7,
    'holy_thursday': -3,
    'good_friday': -2,
    'holy_saturday': -1,
    'easter_monday': 1,
    'bright_friday': 5,         # Zoodochos Pigi
    'thomas_sunday': 7,
    'ascension': 39,
    'pentecost': 49,
    'agiou_pnevmatos': 50,      # Whit Monday / Holy Spirit
    'all_saints': 56,
}


def orthodox_easter(year):
    """Orthodox Easter Sunday as a Gregorian date (Meeus Julian algorithm)."""
    a = year % 4
    b = year % 7
    c = year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    month = (d + e + 114) // 31
    day = (d + e + 114) % 31 + 1
    julian = date(year, month, day)
    return julian + timedelta(days=13)   # Julian -> Gregorian, 1900-2099


def resolve(d, year, eve=False, duration_days=1):
    """Resolve a structured date for a given year."""
    duration_days = max(1, int(duration_days or 1))
    if not isinstance(d, dict):
        return {'start': None, 'end': None, 'months': [], 'exact': False}
    if 'fixed' in d:
        mm, dd = d['fixed'].split('-')
        try:
            start = date(year, int(mm), int(dd))
        except ValueError:
            return {'start': None, 'end': None, 'months': [int(mm)], 'exact': False}
    elif 'movable' in d:
        base = orthodox_easter(year)
        off = d.get('offset')
        if off is None:
            off = MOVABLE_OFFSETS.get(d['movable'], 0)
        start = base + timedelta(days=int(off))
    else:
        months = [int(m) for m in (d.get('months') or [])]
        return {'start': None, 'end': None, 'months': months, 'exact': False}
    # A panigiri whose party is on the eve starts the day before the saint's day.
    first = start - timedelta(days=1) if eve else start
    end = first + timedelta(days=duration_days - 1)
    if eve and end < start:
        end = start
    months = sorted({first.month, end.month})
    return {'start': first, 'end': end, 'months': months, 'exact': True}


def human_when(d, year, eve=False, duration_days=1, lang='en', approx_text=None):
    """Readable date string for a resolved festival, e.g. '16-17 July (eve on the 16th)'."""
    r = resolve(d, year, eve, duration_days)
    if not r['exact']:
        return approx_text or ''
    s, e = r['start'], r['end']
    if lang == 'el':
        mon = MONTHS_EL_GEN
        if s == e:
            core = f'{s.day} {mon[s.month - 1]}'
        elif s.month == e.month:
            core = f'{s.day}–{e.day} {mon[s.month - 1]}'
        else:
            core = f'{s.day} {mon[s.month - 1]} – {e.day} {mon[e.month - 1]}'
        return core
    mon = MONTHS_EN
    if s == e:
        core = f'{s.day} {mon[s.month - 1]}'
    elif s.month == e.month:
        core = f'{s.day}–{e.day} {mon[s.month - 1]}'
    else:
        core = f'{s.day} {mon[s.month - 1]} – {e.day} {mon[e.month - 1]}'
    return core


if __name__ == '__main__':
    for y in (2026, 2027, 2028):
        print(y, orthodox_easter(y))
    print(human_when({'fixed': '07-17'}, 2027, eve=True))
    print(human_when({'movable': 'easter', 'offset': 50}, 2027, lang='el'))
