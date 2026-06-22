"""
v2: viewbox-constrained audit of coordinates in islands/*.json against OpenStreetMap Nominatim.
Flags coordinates that are >2km from the geocoder's best match.

Usage:
    python3 audit-coordinates.py                  # audit all islands
    python3 audit-coordinates.py therasia evia    # audit specific islands

Output: writes audit-results.json with a list of suspect coordinates.
Does NOT modify any JSON file. Review the results before fixing anything.

Honest limitations:
- Nominatim's data is incomplete for small beaches, abandoned villages,
  and obscure ruins. "Not found" doesn't mean the coord is wrong.
- Place names with multiple possible matches (e.g. "Agios Nikolaos" exists
  on many islands) get resolved by adding the island name to the query.
- Rate limit: 1 query/sec per Nominatim's policy. Audit of 79 islands
  with ~10 stops each = ~800 queries = ~14 minutes total.
- The tool reports DISCREPANCIES, it doesn't decide who's right. You verify
  the flagged ones manually before fixing.
"""

import json
import time
import math
import urllib.request
import urllib.parse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ISLANDS_DIR = ROOT / 'islands'
RESULTS_PATH = ROOT / 'audit-results.json'
USER_AGENT = 'aegeanblueprint-audit/1.0 (https://aegeanblueprint.com)'

# Names that frequently appear and don't need geocoding (generic verbs/descriptions)
SKIP_NAMES = {
    'arrival', 'departure', 'drive', 'return', 'lunch', 'dinner', 'breakfast',
    'walk', 'hike', 'ferry', 'boat', 'sunset', 'swim',
}

def haversine_km(lat1, lng1, lat2, lng2):
    """Distance between two lat/lng points in km."""
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lng2 - lng1)
    a = math.sin(dp/2)**2 + math.cos(p1) * math.cos(p2) * math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def clean_query_name(name):
    """Strip prefixes like 'Lunch — ', 'Drive to ', 'Hike ' that confuse geocoder."""
    n = name
    for prefix in ['Lunch — ', 'Lunch -', 'Dinner — ', 'Dinner -', 'Breakfast — ', 'Breakfast -',
                   'Drive to ', 'Drive — ', 'Drive to the ', 'Walk ', 'Hike ', 'Hike to ',
                   'Hike up ', 'Ferry to ', 'Boat to ', 'Sunset at ', 'Swim at ', 'Visit ',
                   'Return ', 'Departure — ', 'Arrival — ', 'Drive back to ']:
        if n.startswith(prefix):
            n = n[len(prefix):]
            break
    # Remove parenthetical clarifications: "Castello Rosso (Bourtzi)" → "Castello Rosso"
    if '(' in n:
        n = n.split('(')[0].strip()
    # Remove em-dash clarifications: "Lunch — Cavo D'Oro" if prefix didn't match
    if ' — ' in n:
        parts = n.split(' — ')
        # Use the longer, more place-name-like half
        n = max(parts, key=len).strip()
    return n.strip()

def should_geocode(name, stop_type):
    """Filter out names that won't usefully geocode."""
    cleaned = clean_query_name(name).lower()
    if not cleaned or len(cleaned) < 3:
        return False
    # Skip purely descriptive entries
    if stop_type in ('arrival', 'departure'):
        return False
    # Skip if the cleaned name is just a generic verb
    if cleaned in SKIP_NAMES:
        return False
    return True

def geocode(query, viewbox=None):
    """Query Nominatim. Returns (lat, lng) or None.

    If viewbox is given as (south, west, north, east), restricts results to
    that bounding box via Nominatim's `viewbox` + `bounded=1` parameters.
    This is a HARD geometric filter — places outside the box are never
    returned, even if the lexical match would otherwise be perfect.
    Without this, Nominatim returns the most "important" globally-popular
    match for the place name, ignoring the island-name hint in the query.
    """
    params = {
        'q': query, 'format': 'json', 'limit': 1, 'countrycodes': 'gr',
    }
    if viewbox is not None:
        south, west, north, east = viewbox
        # Nominatim's viewbox format: lon1,lat1,lon2,lat2 (west,north,east,south)
        params['viewbox'] = f'{west},{north},{east},{south}'
        params['bounded'] = 1
    url = 'https://nominatim.openstreetmap.org/search?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        if data:
            return (float(data[0]['lat']), float(data[0]['lon']))
    except Exception as e:
        print(f'  [error] geocode "{query}": {e}', file=sys.stderr)
    return None

def audit_island(key):
    """Audit one island. Returns list of suspect entries."""
    p = ISLANDS_DIR / f'{key}.json'
    if not p.exists():
        return []
    d = json.loads(p.read_text(encoding='utf-8'))
    suspects = []
    island_name = d.get('name', key)
    items = []  # (kind, day_idx_or_None, idx, name, type, lat, lng)
    for di, day in enumerate(d.get('itinerary', {}).get('days', [])):
        for i, s in enumerate(day.get('stops', [])):
            items.append(('stop', di, i, s.get('name', ''), s.get('type', ''),
                          s.get('lat'), s.get('lng')))
    for i, b in enumerate(d.get('beaches', [])):
        items.append(('beach', None, i, b.get('name', ''), 'beach',
                      b.get('lat'), b.get('lng')))

    for kind, day_idx, idx, name, stop_type, lat, lng in items:
        if lat is None or lng is None:
            continue
        if not should_geocode(name, stop_type):
            continue
        cleaned = clean_query_name(name)
        # Build a viewbox of ±0.4° around the JSON coord (~40km, scales for any
        # island size from tiny to Crete). This is the disambiguator: even if
        # the place name matches another spot globally, Nominatim will only
        # return matches inside this box.
        viewbox = (lat - 0.4, lng - 0.4, lat + 0.4, lng + 0.4)
        # The query keeps the island name as a soft hint (helps tie-break
        # between multiple matches inside the box) but the box does the real
        # filtering. Without the box, Nominatim ignores the island-name hint
        # and returns the globally most-popular match for the place name.
        query = f'{cleaned}, {island_name}, Greece'
        result = geocode(query, viewbox=viewbox)
        time.sleep(1.1)  # Nominatim 1 req/sec policy
        if result is None:
            # Retry without island name in case the place isn't tagged with it
            query2 = f'{cleaned}, Greece'
            result = geocode(query2, viewbox=viewbox)
            time.sleep(1.1)
        if result is None:
            continue  # Not found within 40km — silently skip (probably an obscure beach OSM doesn't have)
        d_km = haversine_km(lat, lng, result[0], result[1])
        # Safety net: even with the viewbox, a malformed result occasionally
        # slips through. If we see >50km, the geocoder picked up something
        # outside the box — don't trust it.
        if d_km > 50.0:
            continue
        if d_km > 2.0:
            suspects.append({
                'island': key,
                'kind': kind,
                'day': day_idx,
                'idx': idx,
                'name': name,
                'json_coord': [lat, lng],
                'osm_coord': [round(result[0], 4), round(result[1], 4)],
                'distance_km': round(d_km, 2),
                'query': query,
            })
            print(f'  ⚠ {key}/{kind}[{idx}] "{name[:40]}": {d_km:.1f}km off — JSON ({lat:.4f},{lng:.4f}) vs OSM ({result[0]:.4f},{result[1]:.4f})')
    return suspects

def write_csv_report(suspects, path):
    """Human-friendly CSV report sorted by distance desc — open in Numbers/Excel to triage."""
    import csv
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['island', 'kind', 'day', 'idx', 'name', 'distance_km',
                    'json_lat', 'json_lng', 'osm_lat', 'osm_lng',
                    'gmaps_link_json', 'gmaps_link_osm'])
        for s in sorted(suspects, key=lambda x: -x['distance_km']):
            jlat, jlng = s['json_coord']
            olat, olng = s['osm_coord']
            w.writerow([
                s['island'], s['kind'], s['day'], s['idx'], s['name'],
                s['distance_km'], jlat, jlng, olat, olng,
                f'https://www.google.com/maps?q={jlat},{jlng}',
                f'https://www.google.com/maps?q={olat},{olng}',
            ])

def main():
    if len(sys.argv) > 1:
        keys = sys.argv[1:]
    else:
        keys = sorted([p.stem for p in ISLANDS_DIR.glob('*.json')])
    est_seconds = len(keys) * 12  # ~10 queries/island × 1.1s each
    print(f'Auditing {len(keys)} islands. ~{len(keys)*10} queries, ~{est_seconds//60}m {est_seconds%60}s estimated.')
    print(f'(Nominatim policy = 1 query/sec. The tool sleeps accordingly.)')
    print()
    all_suspects = []
    for i, key in enumerate(keys, 1):
        print(f'[{i}/{len(keys)}] {key}...')
        s = audit_island(key)
        all_suspects.extend(s)
    print()
    print(f'Done. {len(all_suspects)} suspect coordinates flagged (>2km from OSM).')
    RESULTS_PATH.write_text(json.dumps(all_suspects, ensure_ascii=False, indent=2), encoding='utf-8')
    csv_path = ROOT / 'audit-results.csv'
    write_csv_report(all_suspects, csv_path)
    print(f'  JSON results → {RESULTS_PATH}')
    print(f'  CSV report   → {csv_path}  (open in Numbers/Excel — has Google Maps links for each suspect)')
    print()
    print('NEXT STEP: review the CSV. For each suspect:')
    print('  1. Click the gmaps_link_osm column to see where OSM thinks the place is')
    print('  2. Compare to the gmaps_link_json column to see where the JSON points')
    print('  3. Decide which is right (sometimes OSM is wrong — small beaches especially)')
    print('  4. Share the verified results back to fix in the JSON')

if __name__ == '__main__':
    main()
