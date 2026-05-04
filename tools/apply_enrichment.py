#!/usr/bin/env python3
"""
Aegean Blueprint — apply enrichment edits.

Reads a proposed_edits.json file with one entry per (island, location)
giving a wiki URL to add. Walks each island's JSON, matches stops/beaches
by name, applies the wiki field if it's currently null/missing.

Usage:
  python3 tools/apply_enrichment.py proposed_edits.json [--dry-run]

Edit format:
  {
    "santorini": [
      {"target": "stop:Vlychada Beach (swim)", "wiki": "https://...", "source": "wikipedia|maps"},
      {"target": "beach:Vlychada Beach", "wiki": "https://..."},
      ...
    ]
  }
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ISLANDS = ROOT / 'islands'

def main():
    if len(sys.argv) < 2:
        print("usage: apply_enrichment.py proposed_edits.json [--dry-run]", file=sys.stderr)
        sys.exit(1)
    edits_path = sys.argv[1]
    dry_run = '--dry-run' in sys.argv

    with open(edits_path) as f:
        edits = json.load(f)

    total_applied, total_skipped, total_missed = 0, 0, 0
    for key, items in edits.items():
        if key.startswith('_'):
            continue  # Metadata key like _README — not an island
        path = ISLANDS / f'{key}.json'
        with open(path) as f:
            d = json.load(f)
        applied, skipped, missed = 0, 0, 0
        for item in items:
            kind, _, name = item['target'].partition(':')
            wiki = item['wiki']
            found = False
            if kind == 'stop':
                for day in d.get('itinerary', {}).get('days', []):
                    for s in day.get('stops', []):
                        if s.get('name') == name:
                            found = True
                            if s.get('wiki'):
                                skipped += 1
                            else:
                                s['wiki'] = wiki
                                applied += 1
                            break
                    if found:
                        break
            elif kind == 'beach':
                for b in d.get('beaches', []):
                    if b.get('name') == name:
                        found = True
                        if b.get('wiki'):
                            skipped += 1
                        else:
                            b['wiki'] = wiki
                            applied += 1
                        break
            if not found:
                missed += 1
                print(f"  [miss] {key} {item['target']!r} not found", file=sys.stderr)

        if not dry_run:
            with open(path, 'w') as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
                f.write('\n')

        total_applied += applied
        total_skipped += skipped
        total_missed += missed
        print(f"  {key}: +{applied} applied, ={skipped} already-set, ?{missed} not-found")

    action = "would apply" if dry_run else "applied"
    print(f"\nTotal: {action} {total_applied} edits, {total_skipped} already-set, {total_missed} not-found")
    if dry_run:
        print("(dry run — no files written)")

if __name__ == '__main__':
    main()
