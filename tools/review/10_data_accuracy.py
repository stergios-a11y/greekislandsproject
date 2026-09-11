#!/usr/bin/env python3
"""Data-accuracy pass — internal contradictions and unsupported claims.

Rule used for numbers: ISLANDS_DATA in script.js is the single source of truth
for area and population; prose must not contradict it. Where ISLANDS_DATA was
itself wrong against the census, the score is corrected too (noted below).

Sourced corrections:
  kasos       has a public airport (KSJ), Olympic Air to Karpathos, Rhodes and
              Sitia — the guide said "No airport" and sent readers to Karpathos.
  elafonisos  the Pounta crossing is ~10 min (the guide said 10 in one place and
              5 in another; Ferryhopper says ~10).
  kythnos     "99 beaches" appears nowhere; every Greek source says 92.
  rhodes      keeps the widely cited "300 days of sunshine", drops the
              unsupported "sunniest place in the country".
  tilos       2021 census is 746, not 780; prose said "roughly 500".
  lemnos      477.6 km², so the intro's 477 was right and the score was not.
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

TEXT = {
 # --- area: prose contradicted the island's own score -----------------------
 'kefalonia': [('(786 km²)', '(773 km²)'), ('(786 χλμ²)', '(773 χλμ²)')],
 'kythira':   [('(281 km²)', '(279 km²)'), ('(281 χλμ²)', '(279 χλμ²)')],
 'samos':     [('(478 km²)', '(477 km²)'), ('(478 χλμ²)', '(477 χλμ²)')],
 'milos':     [('small (160 km²)', 'small (151 km²)'), ('μικρή (160 χλμ²)', 'μικρή (151 χλμ²)')],
 'leros':     [('Leros is 54 km²', 'Leros is 53 km²'), ('Η Λέρος είναι 54 τ.χλμ.', 'Η Λέρος είναι 53 τ.χλμ.')],
 'leipsoi':   [('one main 17 km² inhabited island', 'one main 16 km² inhabited island'),
               ('ένα κύριο κατοικημένο νησί 17 τ.χλμ.', 'ένα κύριο κατοικημένο νησί 16 τ.χλμ.')],
 # --- population: prose contradicted the island's own score -----------------
 'ammouliani': [('The 600 year-round residents', 'The 547 year-round residents'),
                ('Οι 600 μόνιμοι κάτοικοι', 'Οι 547 μόνιμοι κάτοικοι')],
 'gavdos':     [('The 142 year-round residents', 'The 152 year-round residents'),
                ('Οι 142 μόνιμοι κάτοικοι', 'Οι 152 μόνιμοι κάτοικοι')],
 'halki':      [('30 km of coastline, around 300 residents', '30 km of coastline, around 480 residents'),
                ('30 χλμ ακτογραμμή, περίπου 300 κάτοικοι', '30 χλμ ακτογραμμή, περίπου 480 κάτοικοι'),
                ('Tiny island, around 300 residents.', 'Tiny island, around 480 residents.'),
                ('Μικρό νησί, ~300 κάτοικοι.', 'Μικρό νησί, ~480 κάτοικοι.')],
 'kimolos':    [("90% of the island's 800 residents", "90% of the island's 910 residents"),
                ('το 90% των 800 κατοίκων του νησιού', 'το 90% των 910 κατοίκων του νησιού')],
 'therasia':   [('About 250 year-round residents', 'About 320 year-round residents'),
                ('Περίπου 250 μόνιμοι κάτοικοι', 'Περίπου 320 μόνιμοι κάτοικοι'),
                ('the same strait, about 250 year-round residents', 'the same strait, about 320 year-round residents'),
                ('ίδιο στενό, γύρω στους 250 μόνιμους κατοίκους', 'ίδιο στενό, γύρω στους 320 μόνιμους κατοίκους')],
 'kasos':      [('The island has 1000 residents', 'The island has about 1,080 residents'),
                ('Το νησί έχει 1000 κατοίκους', 'Το νησί έχει περίπου 1.080 κατοίκους'),
                ('— 1,000 residents, five villages', '— about 1,080 residents, five villages'),
                ('— 1.000 κάτοικοι, πέντε χωριά', '— περίπου 1.080 κάτοικοι, πέντε χωριά'),
  # the airport it does have
                ('No airport. Tiny port on the Karpathos line — direct from Piraeus 17–22h, or via Karpathos and Crete. Population under 1,000.',
                 'Small airport (KSJ) with Olympic Air flights from Karpathos, Rhodes and Sitia. By sea, a tiny port on the Karpathos line — direct from Piraeus 17–22h, or via Karpathos and Crete.'),
                ('Χωρίς αεροδρόμιο. Μικρό λιμάνι στη γραμμή Καρπάθου — απευθείας από Πειραιά 17–22 ώρες, ή μέσω Καρπάθου και Κρήτης. Πληθυσμός κάτω από 1.000.',
                 'Μικρό αεροδρόμιο (KSJ) με πτήσεις της Olympic Air από Κάρπαθο, Ρόδο και Σητεία. Από θάλασσα, μικρό λιμάνι στη γραμμή Καρπάθου — απευθείας από Πειραιά 17–22 ώρες, ή μέσω Καρπάθου και Κρήτης.'),
                ('Most travellers fly to Karpathos and ferry over — the direct boat is brutal.',
                 'Fly in if you can — the direct boat from Piraeus is brutal, and the Karpathos hop is short.'),
                ('Οι περισσότεροι πετάνε στην Κάρπαθο και πάνε με πλοίο — το απευθείας είναι σκληρό.',
                 'Πέτα αν μπορείς — το απευθείας πλοίο από τον Πειραιά είναι σκληρό, και η πτήση από Κάρπαθο σύντομη.')],
 # --- tilos: area to match its score, population to the 2021 census ---------
 'tilos':      [('Tilos is 63 km²', 'Tilos is 61 km²'),
                ('Η Τήλος είναι 63 τ.χλμ.', 'Η Τήλος είναι 61 τ.χλμ.'),
                ('with roughly 500 year-round residents', 'with around 750 year-round residents'),
                ('με περίπου 500 μόνιμους κατοίκους', 'με περίπου 750 μόνιμους κατοίκους'),
                ("500 of the island's residents live here.", "Most of the island's residents live here."),
                ('500 από τους κατοίκους του νησιού ζουν εδώ.', 'Εδώ ζουν οι περισσότεροι κάτοικοι του νησιού.')],
 # --- sourced corrections ---------------------------------------------------
 'elafonisos': [('Ferry from Pounta on the mainland — 5 minutes across the strait.',
                 'Ferry from Pounta on the mainland — about 10 minutes across the strait.'),
                ('Πλοίο από την Πούντα στην ηπειρωτική χώρα — 5 λεπτά για να διασχίσεις το στενό.',
                 'Πλοίο από την Πούντα στην ηπειρωτική χώρα — περίπου 10 λεπτά για να διασχίσεις το στενό.')],
 'kythnos':    [('The draw: 99 beaches,', 'The draw: 92 beaches,'),
                ('Η έλξη: 99 παραλίες,', 'Η έλξη: 92 παραλίες,')],
 'rhodes':     [('More than 300 days of sunshine a year make it the sunniest place in the country.',
                 'More than 300 days of sunshine a year, and one of the longest seasons in Greece.'),
                ('Πάνω από 300 μέρες λιακάδας τον χρόνο την κάνουν το πιο ηλιόλουστο μέρος της χώρας.',
                 'Πάνω από 300 μέρες λιακάδας τον χρόνο, και από τις μεγαλύτερες σεζόν στην Ελλάδα.')],
 # --- prose rounding that contradicted the island's own sidebar figure ------
 'anafi':      [('around 300 year-round residents', 'around 270 year-round residents'),
                ('περίπου 300 μόνιμοι κάτοικοι', 'περίπου 270 μόνιμοι κάτοικοι')],
 'donousa':    [('with about 200 year-round residents', 'with about 170 year-round residents'),
                ('με περίπου 200 μόνιμους κατοίκους', 'με περίπου 170 μόνιμους κατοίκους')],
}

# ISLANDS_DATA corrections (the score itself was wrong)
SCORES = [('tilos',  'pop',  '780',  '746'),   # 2021 census
          ('lemnos', 'area', '476',  '477')]   # 477.6 km²

def main():
    changed = miss = 0
    for key, pairs in TEXT.items():
        p = ROOT / 'islands' / f'{key}.json'
        s = p.read_text(encoding='utf-8')
        orig = s
        for old, new in pairs:
            if new in s:
                continue
            n = s.count(old)
            if n != 1:
                print(f'  !! {key}: {n} matches for {old[:60]!r}', file=sys.stderr); miss += 1; continue
            s = s.replace(old, new); changed += 1
            print(f'  {key:12} {old[:58]}  ->  {new[:58]}')
        if s != orig:
            json.loads(s)
            p.write_text(s, encoding='utf-8')

    js = ROOT / 'script.js'
    t = js.read_text(encoding='utf-8')
    for key, field, old, new in SCORES:
        import re
        m = re.search(r'"' + key + r'":\s*\{[^}]*\}', t)
        if not m:
            print(f'  !! script.js: no ISLANDS_DATA row for {key}', file=sys.stderr); miss += 1; continue
        row = m.group(0)
        oldf, newf = f'{field}:{old}', f'{field}:{new}'
        if newf in row.replace(' ', ''):
            continue
        import re as _re
        row2 = _re.sub(r'\b' + field + r':\s*' + old + r'\b', f'{field}:{new}', row)
        if row2 == row:
            print(f'  !! script.js: {key}.{field}={old} not found', file=sys.stderr); miss += 1; continue
        t = t[:m.start()] + row2 + t[m.end():]
        changed += 1
        print(f'  {key:12} ISLANDS_DATA {field} {old} -> {new}')
    js.write_text(t, encoding='utf-8')

    print(f'\n{changed} corrections applied, {miss} not found')
    return 1 if miss else 0

sys.exit(main())
