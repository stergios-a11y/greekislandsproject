#!/usr/bin/env python3
"""
Aegean Blueprint — content enrichment workflow.

For each stop/beach without `wiki` or `photo`, attempt to fill them from:
  1. Wikipedia (EN first, EL fallback) — verify by coord proximity + name match
  2. Google Maps place_id — fallback if no Wikipedia match
  3. Wikimedia Commons — for photos

This script is run by hand (or via Claude tool calls in dev) and emits a
"proposed edits" JSON file rather than mutating the island JSONs directly,
so a human can review before applying.

Usage:
  python3 tools/enrich.py <island_key> [<island_key>...] > /tmp/edits.json
"""
import json, os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ISLANDS = ROOT / 'islands'

# Skip these — they're not real places.
SKIP_NAME = re.compile(
    r'^(lunch|dinner|breakfast|brunch|drinks?|coffee|sunset\s*&|return to|free time|drive to|drive back|ferry|optional|swim)\b'
    r'|—\s*(departure|arrival)$',
    re.I
)

# Common geographic words that don't help disambiguation, plus religious prefixes
# that produce false positives when matching "Agios X" against "Saint X".
COMMON_WORDS = {
    'beach','village','town','island','port','monastery','church','castle',
    'cave','museum','paralia','ano','kato','old','new','departure','arrival',
    'drive','square','main','tomb','ferry','rock','sanctuary','park',
    'geological','agios','saint','agia','holy','st','agioi','memorial',
    'grave','site','archaeological','viewpoint','lighthouse','tower','bay',
    'the','of','and','from'
}

def candidate_names(stop_or_beach):
    """Yield search-suitable names from a stop/beach record."""
    name = stop_or_beach.get('name')
    if not name or SKIP_NAME.search(name):
        return None
    return name

def haversine_km(lat1, lng1, lat2, lng2):
    """Approximate distance in km — good enough for sanity checks."""
    import math
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lng2 - lng1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def collect_targets(island_data, island_name):
    """Return a flat list of target records to enrich.
    Each record has: kind ('stop'|'beach'), island, name, lat, lng, needs_wiki, needs_photo.
    """
    targets = []
    for day in island_data.get('itinerary', {}).get('days', []):
        for stop in day.get('stops', []):
            name = candidate_names(stop)
            if not name: continue
            targets.append({
                'kind': 'stop',
                'island_name': island_name,
                'name': name,
                'lat': stop.get('lat'),
                'lng': stop.get('lng'),
                'type': stop.get('type'),
                'needs_wiki': not stop.get('wiki'),
                'needs_photo': not stop.get('photo'),
                'day': day.get('day'),
            })
    for beach in island_data.get('beaches', []):
        name = beach.get('name')
        if not name: continue
        # Beaches don't have lat/lng on the record itself; they're top-level.
        # Fall back to island center for the coord-sanity check.
        targets.append({
            'kind': 'beach',
            'island_name': island_name,
            'name': name,
            'lat': beach.get('lat'),
            'lng': beach.get('lng'),
            'needs_wiki': not beach.get('wiki'),
            'needs_photo': not beach.get('photo'),
        })
    return targets

if __name__ == '__main__':
    keys = sys.argv[1:]
    if not keys:
        print("usage: enrich.py <island_key>...", file=sys.stderr); sys.exit(1)
    out = {}
    for k in keys:
        path = ISLANDS / f'{k}.json'
        with open(path) as f: d = json.load(f)
        out[k] = collect_targets(d, d.get('name', k))
    print(json.dumps(out, ensure_ascii=False, indent=2))
