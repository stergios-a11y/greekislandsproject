#!/usr/bin/env python3
"""Build the whole site for one market — the one command to run after any change.

    python3 tools/build.py                 # greece (default)
    MARKET=croatia python3 tools/build.py  # another market pack

Order: validate → prerender (island pages, homepage blocks, sitemap, market-data.js,
theme sync) → optional page families, each only if the market enables the feature in
markets/<market>/market.json "features" (missing = on). Stops at the first failure.
"""
import os
import subprocess
import sys
import time
from pathlib import Path

import market as M

TOOLS = Path(__file__).resolve().parent

# (feature or None for always, script) — order matters: later steps patch the sitemap
STEPS = [
    (None, 'validate'),
    (None, 'prerender'),
    ('itineraries', 'build_itineraries'),
    ('compare', 'build_compare_pages'),
    ('festivals', 'build_festival_extras'),
    ('festivals', 'build_festivals'),
    ('match', 'build_match_page'),
    ('collections', 'build_collections'),
    ('trip_cost', 'build_costs'),
    ('trip_cost', 'build_trip_cost'),
]


def main():
    t0 = time.time()
    print(f'━━ Building market "{M.MARKET}" ━━')
    for feat, script in STEPS:
        if feat and not M.feature(feat):
            print(f'· {script}: skipped (feature "{feat}" off)')
            continue
        t = time.time()
        r = subprocess.run([sys.executable, str(TOOLS / f'{script}.py')], cwd=M.ROOT, env=os.environ)
        if r.returncode:
            print(f'✗ {script} failed (exit {r.returncode}) — build stopped')
            return r.returncode
        print(f'  ({script}: {time.time() - t:.1f}s)')
    print(f'━━ Done in {time.time() - t0:.0f}s ━━')
    return 0


if __name__ == '__main__':
    sys.exit(main())
