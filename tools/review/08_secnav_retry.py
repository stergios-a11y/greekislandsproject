#!/usr/bin/env python3
"""Fourth bug, uncovered once the TDZ throw stopped hiding it.

With the ReferenceError gone, buildSectionNav() runs — but on a cold load it
still produces nothing. It is called ~60ms after the guide HTML is injected,
and it only counts a section as real when its box is taller than 24px. At that
moment the itinerary and beach sections are still unlaid-out image grids with
zero height, so fewer than three sections qualify and the function returns
without building the bar. Called by hand ten seconds later on the same page it
builds all seven chips.

So: retry instead of racing layout. Each bail-out schedules another attempt
(12 x 150ms ~ 1.8s), success cancels the chain, and a one-shot window.load
handler covers the case where images settle later than that.

Idempotent.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
P = ROOT / 'script.js'
s = P.read_text(encoding='utf-8')

if '_secnavRetry' in s:
    print('secnav retry: already applied'); sys.exit(0)

def one(old, where):
    if s.count(old) != 1:
        print(f'  !! {where}: {s.count(old)} matches', file=sys.stderr); sys.exit(1)

HELPER = """/* buildSectionNav measures section heights, so it can only run once the island
   HTML has actually been laid out. Rather than guess a delay, every bail-out
   schedules another attempt and the first success cancels the chain. */
let _secnavRetry = 0;
let _secnavTimer = 0;
function secnavRetryReset() {
  _secnavRetry = 0;
  if (_secnavTimer) { clearTimeout(_secnavTimer); _secnavTimer = 0; }
}
function secnavRetryLater() {
  if (_secnavTimer) { clearTimeout(_secnavTimer); _secnavTimer = 0; }
  if (_secnavRetry >= 12) return;
  _secnavRetry++;
  _secnavTimer = setTimeout(buildSectionNav, 150);
}

function buildSectionNav() {"""

one('function buildSectionNav() {', 'buildSectionNav declaration')
s = s.replace('function buildSectionNav() {', HELPER)

# bail-outs now retry instead of giving up
one("""  const main = grid && grid.querySelector(':scope > .detail-main');
  if (!grid || !main) return;""", 'grid guard')
s = s.replace("""  const main = grid && grid.querySelector(':scope > .detail-main');
  if (!grid || !main) return;""",
"""  const main = grid && grid.querySelector(':scope > .detail-main');
  if (!grid || !main) { secnavRetryLater(); return; }""")

one('  if (present.length < 3) return;', 'present guard')
s = s.replace('  if (present.length < 3) return;',
"""  // Under three, the sections are probably just not laid out yet — try again
  // shortly rather than leaving the page without its jump list.
  if (present.length < 3) { secnavRetryLater(); return; }
  secnavRetryReset();""")

# fresh island render starts a fresh retry budget
one('      requestAnimationFrame(() => setTimeout(buildSectionNav, 60));', 'render call site')
s = s.replace('      requestAnimationFrame(() => setTimeout(buildSectionNav, 60));',
              '      secnavRetryReset();\n      requestAnimationFrame(() => setTimeout(buildSectionNav, 60));')

# last resort: images that settle after the retry window
one("window.addEventListener('popstate', () => {", 'popstate listener')
s = s.replace("window.addEventListener('popstate', () => {",
"""// Images can finish laying out after the retry window closes; one more go
// once everything has loaded costs nothing and cannot double-build (the
// function removes any existing #secnav first).
window.addEventListener('load', () => {
  if (!document.getElementById('secnav')) {
    secnavRetryReset();
    try { buildSectionNav(); } catch (_) {}
  }
});

window.addEventListener('popstate', () => {""")

P.write_text(s, encoding='utf-8')
print('secnav retry: applied')
