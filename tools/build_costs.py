#!/usr/bin/env python3
"""Build costs.json from costs.csv (the human-editable cost table).

Workflow: edit costs.csv in Excel/Numbers (keep it CSV), run the deploy —
this script runs before prerender and regenerates costs.json, which the
trip-cost page fetches at runtime.

costs.csv columns (per island, July single values):
  island, afford, room budget, room mid, room comfort, meal pp/day,
  car €/day (— for car-free), boat day name (blank = none), boat €pp, notes

Formulas (ranges, season surge, meal tiers, premiums) live in META below —
change once, all 88 islands follow. Season surge applies to rooms AND cars.
"""
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def load_rules():
    """Read cost-rules.csv → META dict. Season rows use the month columns;
    scalar rows use the 'value' column."""
    months = ['apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct']
    meta = {'baseline': 'July; single typical values per island in costs.csv. '
                        'All multipliers come from cost-rules.csv.'}
    with open(ROOT / 'cost-rules.csv', newline='', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            rule = row['rule'].strip()
            if not rule:
                continue
            if rule.startswith('season_'):
                meta[rule] = {m: float(row[m]) for m in months if row.get(m, '').strip()}
            else:
                meta[rule] = float(row['value'])
    # sanity: July must be the 1.0 baseline
    for k in ('season_room', 'season_car'):
        if abs(meta.get(k, {}).get('jul', 1.0) - 1.0) > 1e-9:
            print(f'  ! warning: {k} July is not 1.00 — island values are July baselines')
    return meta


def num(v):
    v = str(v).strip().replace('€', '')
    if v in ('', '—', '-'):
        return None
    return float(v) if '.' in v else int(v)

def main():
    src = ROOT / 'costs.csv'
    out = ROOT / 'costs.json'
    islands = {}
    errors = []
    with open(src, newline='', encoding='utf-8-sig') as f:
        for i, row in enumerate(csv.DictReader(f), start=2):
            cols = list(row.values())
            key = cols[0].strip()
            if not key:
                continue
            try:
                entry = {
                    'room': {'budget': num(cols[2]), 'mid': num(cols[3]), 'comfort': num(cols[4])},
                    'meal_pp_mid': num(cols[5]),
                    'car_day': num(cols[6]),
                }
                if None in entry['room'].values() or entry['meal_pp_mid'] is None:
                    errors.append(f'line {i} ({key}): missing room/meal value')
                boat_name = cols[7].strip()
                if boat_name:
                    entry['boat'] = {'name': boat_name, 'pp': num(cols[8]) or 55}
                islands[key] = entry
            except Exception as e:
                errors.append(f'line {i} ({key}): {e}')
    if errors:
        print('costs.csv problems:')
        for e in errors:
            print('  ✗', e)
        sys.exit(1)
    # sanity: every island JSON should have a costs row
    missing = [p.stem for p in (ROOT / 'islands').glob('*.json') if p.stem not in islands]
    if missing:
        print(f'  ! islands without cost rows: {", ".join(sorted(missing))}')
    from datetime import date
    json.dump({'_meta': dict(load_rules(), updated=str(date.today())), 'islands': islands},
              open(out, 'w'), ensure_ascii=False, indent=1)
    print(f'✓ costs.json built: {len(islands)} islands ({len([i for i in islands.values() if "boat" in i])} boat days, {len([i for i in islands.values() if i["car_day"] is None])} car-free)')

if __name__ == '__main__':
    main()
