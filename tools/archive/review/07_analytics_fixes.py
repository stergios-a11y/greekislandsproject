#!/usr/bin/env python3
"""Three GA4 / island-page bugs found by reading the live analytics (11 Sept).

1. On prerendered island pages the GA snippet lives inside an IIFE, so
   `function gtag(){...}` is scoped to it and never becomes a global.
   gtag('config') still works (the library handles pageviews internally), but
   script.js cannot see gtag, so track() bailed on its first line and
   affiliate_click / outbound_click / section_view had never fired once.
   Fixed by assigning window.gtag instead of declaring a scoped function.

2. buildSectionNav() threw "Cannot access 'track' before initialization" on
   every island page: a later `const track` (the secnav scroll track element)
   put the name in the temporal dead zone for the whole block, so the
   track('section_view', …) call above it threw. The throw happened before the
   bar was rendered, so the jump-to-section bar was missing from all 176 island
   pages. Renamed the local to trackEl.

3. Every prerendered compare-page visit logged a phantom "Compare" pageview at
   /app/compare with ~1s engagement — 1,901 views, 21% of all pageviews.
   gtag('config') already logs the real URL; the boot trackView() was only ever
   meant to cover hash deep links (where the path really is "/"). parseHash now
   reports whether it matched the path, and boot skips the extra pageview then.

Idempotent.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
def bail(m): print('  !!', m, file=sys.stderr); sys.exit(1)
def one(s, old, where):
    if s.count(old) != 1: bail(f'{where}: {s.count(old)} matches')
    return True

done = []

# ---- 1. prerender.py: make gtag a real global -----------------------------
p = ROOT / 'tools' / 'prerender.py'
s = p.read_text(encoding='utf-8')
old = "  function gtag(){{ dataLayer.push(arguments); }}"
new = ("  // Assigned to window, not declared: this snippet runs inside an IIFE, so a\n"
       "  // function declaration would be scoped to it and script.js could never see\n"
       "  // gtag — which is exactly how affiliate_click and section_view went missing.\n"
       "  window.gtag = window.gtag || function(){{ dataLayer.push(arguments); }};")
if new not in s:
    one(s, old, 'prerender.py gtag'); s = s.replace(old, new)
    p.write_text(s, encoding='utf-8'); done.append('prerender.py: gtag global')

# ---- 2 & 3. script.js ------------------------------------------------------
p = ROOT / 'script.js'
s = p.read_text(encoding='utf-8')
orig = s

# 2. TDZ: rename the shadowing local
if "const trackEl = bar.querySelector('.secnav-track');" not in s:
    old = "    const track = bar.querySelector('.secnav-track');"
    new = ("    // Named trackEl, not track: a `const track` here shadows the global\n"
           "    // track() for the WHOLE block, so the section_view call above it threw\n"
           "    // a temporal-dead-zone ReferenceError and took the whole bar down.\n"
           "    const trackEl = bar.querySelector('.secnav-track');")
    one(s, old, 'script.js secnav track'); s = s.replace(old, new)
    for a, b in [("if (chip && track.scrollWidth > track.clientWidth) {",
                  "if (chip && trackEl.scrollWidth > trackEl.clientWidth) {"),
                 ("const c = chip.getBoundingClientRect(), tr = track.getBoundingClientRect();",
                  "const c = chip.getBoundingClientRect(), tr = trackEl.getBoundingClientRect();"),
                 ("        track.scrollTo({ left: Math.max(0, chip.offsetLeft - 16), behavior: 'smooth' });",
                  "        trackEl.scrollTo({ left: Math.max(0, chip.offsetLeft - 16), behavior: 'smooth' });")]:
        one(s, a, f'script.js secnav use {a[:40]}'); s = s.replace(a, b)
    done.append('script.js: secnav TDZ')

# 3. no duplicate pageview for path-routed prerendered pages
if 'fromPath' not in s:
    subs = [
        ("  const pathMatch = path.match(/^\\/island\\/([a-z-]+)$/);\n"
         "  if (pathMatch) return { view: 'island', param: pathMatch[1] };",
         "  const pathMatch = path.match(/^\\/island\\/([a-z-]+)$/);\n"
         "  if (pathMatch) return { view: 'island', param: pathMatch[1], fromPath: true };"),
        ("  if (cmpMatch) return { view: 'compare', param: { pair: [cmpMatch[1], cmpMatch[2]] } };",
         "  if (cmpMatch) return { view: 'compare', param: { pair: [cmpMatch[1], cmpMatch[2]] }, fromPath: true };"),
        ("    const { view, param } = parseHash();\n"
         "    showView(view, param);\n"
         "    // Deep link into a specific view: gtag('config') logged the landing URL as\n"
         "    // \"/\", so send the view itself too. Home needs nothing — already counted.\n"
         "    if (view && view !== 'home') trackView(view, param);",
         "    const { view, param, fromPath } = parseHash();\n"
         "    showView(view, param);\n"
         "    // Hash deep link (/#compare): gtag('config') logged the landing URL as \"/\",\n"
         "    // so send the view itself too. A PATH route (/island/x/, /compare/a-vs-b/) is\n"
         "    // a real URL that gtag('config') already logged — sending it again logged\n"
         "    // every compare visit a second time as a phantom \"/app/compare\" hit with no\n"
         "    // engagement, which became 21% of all pageviews. Home needs nothing either.\n"
         "    if (view && view !== 'home' && !fromPath) trackView(view, param);"),
    ]
    for a, b in subs:
        one(s, a, f'script.js route {a[:40]}'); s = s.replace(a, b)
    done.append('script.js: no duplicate pageview on path routes')

if s != orig:
    p.write_text(s, encoding='utf-8')

print('analytics fixes:', '; '.join(done) if done else 'already applied')
