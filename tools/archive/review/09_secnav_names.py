#!/usr/bin/env python3
"""section_view reported raw DOM ids, so the analytics names were inconsistent.

Two sections already carry an id of their own — itin-days-container and local
(the latter added for the /#local anchor) — and buildSectionNav only assigns the
canonical sec-* id to elements that have none. section_view therefore reported
'itin-days-container' and 'local' alongside 'overview', 'when', 'beaches'. Since
the whole point of the event is comparing where beaches sit against the
itinerary, the names need to be stable. Report the canonical key instead.

Idempotent.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
P = ROOT / 'script.js'
s = P.read_text(encoding='utf-8')
if 'SECNAV_NAME' in s:
    print('secnav names: already applied'); sys.exit(0)

def one(old, where):
    if s.count(old) != 1:
        print(f'  !! {where}: {s.count(old)} matches', file=sys.stderr); sys.exit(1)

old = '  const marks = present.map(s => s.el);'
new = ("""  const marks = present.map(s => s.el);
  // Two sections keep an id of their own (itin-days-container, local), so the
  // DOM id is not a stable analytics name. Report the canonical key instead.
  const SECNAV_NAME = new Map(present.map(s => [s.el, s.id.replace(/^sec-/, '')]));""")
one(old, 'marks'); s = s.replace(old, new)

old = ("      track('section_view', { section: current.id.replace(/^sec-/, ''), "
       "island: currentIslandKey || '', order: _seenSections.size });")
new = ("      track('section_view', { section: SECNAV_NAME.get(current) || current.id, "
       "island: currentIslandKey || '', order: _seenSections.size });")
one(old, 'section_view call'); s = s.replace(old, new)

P.write_text(s, encoding='utf-8')
print('secnav names: applied')
