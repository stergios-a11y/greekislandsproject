#!/usr/bin/env python3
"""Seed why_score.json — one sentence per island explaining its overall score
from the five component scores that produced it.

Strengths and weaknesses are chosen by each island's PERCENTILE within a
dimension, not by a flat cutoff: beach scores skew high across the Aegean
(median 3.9) and nightlife skews low (median 2.9), so a flat "4.0 = good"
rule calls half the islands beach destinations and almost none of them
lively. The wording band is then picked from the absolute value.

Seeds only islands not already present; --force rewrites all. The JSON is
meant to be hand-edited afterwards — edits survive re-runs.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FORCE = '--force' in sys.argv
DIMS = ['beach', 'hist', 'night', 'access', 'afford']

def load_islands():
    s = (ROOT / 'script.js').read_text(encoding='utf-8')
    blk = re.search(r'const ISLANDS_DATA = \{(.*?)\n\};', s, re.S).group(1)
    rows = {}
    for m in re.finditer(r'"([a-z0-9-]+)":\s*\{([^}]*)\}', blk):
        d = {}
        for f in re.finditer(r'(\w+):\s*("([^"]*)"|[\d.]+|true|false)', m.group(2)):
            v = f.group(2)
            d[f.group(1)] = f.group(3) if f.group(3) is not None else (
                True if v == 'true' else False if v == 'false' else float(v))
        rows[m.group(1)] = d
    return rows

# Noun phrases, so two of them join with "and" and still read as English.
STRENGTH = {
 'beach':  [(4.8, 'some of the best beaches in Greece',   'από τις καλύτερες παραλίες της Ελλάδας'),
            (4.4, 'outstanding beaches',                  'εξαιρετικές παραλίες'),
            (4.0, 'very good beaches',                    'πολύ καλές παραλίες'),
            (0.0, 'decent beaches',                       'αξιοπρεπείς παραλίες')],
 'hist':   [(4.8, 'an extraordinary depth of history',    'εξαιρετικό ιστορικό βάθος'),
            (4.3, 'exceptional history and architecture', 'σπουδαία ιστορία και αρχιτεκτονική'),
            (3.8, 'real history and character',           'πραγματική ιστορία και χαρακτήρα'),
            (0.0, 'more to see than most of its size',    'περισσότερα να δεις απ᾽ όσα περιμένεις')],
 'night':  [(4.8, 'the loudest nightlife in the Aegean',  'την πιο έντονη νυχτερινή ζωή του Αιγαίου'),
            (4.2, 'serious nightlife',                    'σοβαρή νυχτερινή ζωή'),
            (3.6, 'a real night scene',                   'αληθινή νυχτερινή ζωή'),
            (0.0, 'more going on at night than its neighbours', 'πιο ζωντανές νύχτες από τα γειτονικά')],
 'access': [(4.6, 'very easy access',                     'πολύ εύκολη πρόσβαση'),
            (4.0, 'easy access',                          'εύκολη πρόσβαση'),
            (0.0, 'straightforward access',               'βολική πρόσβαση')],
 'afford': [(4.4, 'genuinely low prices',                 'πραγματικά χαμηλές τιμές'),
            (3.9, 'good value',                           'καλή σχέση τιμής-αξίας'),
            (0.0, 'fair prices',                          'λογικές τιμές')],
}
# Clauses, joined after "but".
WEAKNESS = {
 'beach':  [(2.3, 'the beaches are not the reason to come', 'οι παραλίες δεν είναι ο λόγος που έρχεσαι'),
            (3.0, 'the beaches are ordinary',               'οι παραλίες είναι μέτριες'),
            (9.9, 'the beaches are the weakest thing about it', 'οι παραλίες είναι το πιο αδύναμο σημείο του')],
 'hist':   [(1.8, 'there is very little to see beyond the landscape', 'ελάχιστα πράγματα να δεις πέρα από το τοπίο'),
            (2.6, 'the sights are thin',                    'τα αξιοθέατα είναι λίγα'),
            (9.9, 'it is light on things to visit',         'έχει λίγα πράγματα να επισκεφτείς')],
 'night':  [(1.5, 'there is no nightlife at all',           'δεν υπάρχει καθόλου νυχτερινή ζωή'),
            (2.4, 'it is very quiet after dinner',          'είναι πολύ ήσυχο μετά το δείπνο'),
            (9.9, 'the evenings are low-key',               'τα βράδια είναι ήσυχα')],
 'access': [(1.8, 'it is genuinely hard to reach',          'είναι πραγματικά δύσκολο να φτάσεις'),
            (2.8, 'getting there is awkward',               'η πρόσβαση είναι δύσκολη'),
            (9.9, 'the connections are limited',            'οι συνδέσεις είναι περιορισμένες')],
 'afford': [(1.5, 'it is expensive',                        'είναι ακριβό'),
            (2.8, 'it is pricey in season',                 'είναι ακριβό στη σεζόν'),
            (9.9, 'it is not one of the cheap islands',     'δεν είναι από τα φθηνά νησιά')],
}

STRENGTH_FLOOR = 3.6      # below this, a high percentile is still not a selling point
WEAKNESS_CEIL  = 3.2      # above this, a low percentile is still not a fault

FLAG_ORDER = ['drama', 'chora', 'hiking', 'springs', 'sailing']
FLAGS = {
 'drama':   ('a genuinely dramatic landscape', 'πραγματικά δραματικό τοπίο'),
 'chora':   ('one of the finest choras in the Aegean', 'μία από τις ωραιότερες χώρες του Αιγαίου'),
 'hiking':  ('serious walking country', 'σοβαρές διαδρομές πεζοπορίας'),
 'springs': ('hot springs', 'ιαματικές πηγές'),
 'sailing': ('some of the best sailing water in Greece', 'από τα καλύτερα νερά της Ελλάδας για ιστιοπλοΐα'),
}

def band(table, val, asc=False):
    for thr, en, el in table:
        if (val <= thr) if asc else (val >= thr):
            return en, el
    return table[-1][1], table[-1][2]

def pctile(sorted_vals, v):
    n = len(sorted_vals)
    below = sum(1 for x in sorted_vals if x < v)
    equal = sum(1 for x in sorted_vals if x == v)
    return (below + equal / 2.0) / n

def join(items, lang):
    if not items: return ''
    if len(items) == 1: return items[0]
    a = ' and ' if lang == 'en' else ' και '
    if len(items) == 2: return items[0] + a + items[1]
    return ', '.join(items[:-1]) + a + items[-1]

def build(r, dist):
    total = r['total']
    ranked = sorted(DIMS, key=lambda d: -pctile(dist[d], r[d]))
    # Percentile says "good FOR a Greek island"; the absolute floor/ceiling stops
    # a merely median score being sold as a strength (or a fault).
    strong = [d for d in ranked
              if pctile(dist[d], r[d]) >= 0.66 and r[d] >= STRENGTH_FLOOR][:2]
    weak = [d for d in reversed(ranked)
            if pctile(dist[d], r[d]) <= 0.35 and r[d] <= WEAKNESS_CEIL][:2]
    weak = [d for d in weak if d not in strong]

    s_en = [band(STRENGTH[d], r[d])[0] for d in strong]
    s_el = [band(STRENGTH[d], r[d])[1] for d in strong]
    w_en = [band(WEAKNESS[d], r[d], asc=True)[0] for d in weak]
    w_el = [band(WEAKNESS[d], r[d], asc=True)[1] for d in weak]

    # The five numbers miss what several islands are actually for. The character
    # flags carry it, so they top up (or stand in for) a thin strength clause.
    for f in FLAG_ORDER:
        if len(s_en) >= 2: break
        if r.get(f):
            s_en.append(FLAGS[f][0]); s_el.append(FLAGS[f][1])

    # Fall back to the island's own best dimension before car-freeness, so no
    # island is introduced by what it doesn't need.
    if not s_en:
        best = ranked[0]
        s_en = [band(STRENGTH[best], r[best])[0]]
        s_el = [band(STRENGTH[best], r[best])[1]]

    car = r.get('car_need', 0)
    if car >= 4.5:
        w_en.append('you cannot do it without a car'); w_el.append('δεν γίνεται χωρίς αυτοκίνητο')
    elif car <= 1.0 and len(s_en) < 3:
        s_en.append('nothing you need a car for'); s_el.append('τίποτα που να θέλει αυτοκίνητο')

    se, sl = join(s_en[:3], 'en'), join(s_el[:3], 'el')
    we, wl = join(w_en[:2], 'en'), join(w_el[:2], 'el')
    n = f'{total:.1f}'
    if se and we:
        return {'en': f'Why {n}: {se} — but {we}.',
                'el': f'Γιατί {n}: {sl} — αλλά {wl}.'}
    if se and total >= 4.2:
        return {'en': f'Why {n}: {se}, and no real weak spot.',
                'el': f'Γιατί {n}: {sl}, και κανένα πραγματικό αδύνατο σημείο.'}
    if se:
        return {'en': f'Why {n}: {se}, and nothing that actively lets it down.',
                'el': f'Γιατί {n}: {sl}, και τίποτα που να το ρίχνει.'}
    return {'en': f'Why {n}: solid across the board, outstanding in nothing.',
            'el': f'Γιατί {n}: σταθερό παντού, κορυφαίο πουθενά.'}

def main():
    rows = load_islands()
    dist = {d: sorted(r[d] for r in rows.values()) for d in DIMS}
    p = ROOT / 'why_score.json'
    cur = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
    added = 0
    for k, r in sorted(rows.items()):
        if k in cur and not FORCE:
            continue
        cur[k] = build(r, dist); added += 1
    p.write_text(json.dumps(cur, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
    print(f'why_score.json: {len(cur)} islands ({added} written)')

main()
