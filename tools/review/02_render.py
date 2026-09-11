#!/usr/bin/env python3
"""Review fixes 2 + 3 — wire two new signals into the island page.

 2. Provenance: islands/<key>.json may carry
        "provenance": {"visited": "2025-06"}
    which renders as "Visited by the author · June 2025" beside the
    last-updated stamp. Islands WITHOUT the field render exactly as they do
    today — so this can ship before the visited list is filled in, and no
    island is ever implicitly labelled "not visited".

 3. Why this score: why_score.json is folded into each islands/<key>.json as
    "why_score": {"en": …, "el": …} and rendered under the Blueprint ring, so
    the number becomes a decision instead of an opinion. No extra HTTP request:
    the island JSON is already being fetched.

Idempotent.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
errors = []

# ---------------------------------------------------------------- data ------
def fold_why():
    src = ROOT / 'why_score.json'
    if not src.exists():
        errors.append('why_score.json missing — run tools/review/gen_why_score.py first')
        return 0
    why = json.loads(src.read_text(encoding='utf-8'))
    n = 0
    for p in sorted((ROOT / 'islands').glob('*.json')):
        d = json.loads(p.read_text(encoding='utf-8'))
        k = d.get('key')
        if k not in why:
            continue
        if d.get('why_score') == why[k]:
            continue
        d['why_score'] = why[k]
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        n += 1
    return n

# ---------------------------------------------------------------- script ---
JS_RENDER = """
      // "Why this score" — turns the ring from an opinion into a decision.
      // Source of truth is why_score.json, folded into the island JSON at build
      // time by tools/review/02_render.py, so this costs no extra request.
      const _whyBox = document.getElementById('blueprint-why');
      if (_whyBox) {
        const _wl = (typeof CURRENT_LANG !== 'undefined' && CURRENT_LANG === 'el') ? 'el' : 'en';
        const _wtxt = (data.why_score && data.why_score[_wl]) || '';
        _whyBox.textContent = _wtxt;
        _whyBox.hidden = !_wtxt;
      }
      // Provenance. Only islands that carry provenance.visited say anything —
      // absence must never read as "not visited".
      const _prov = document.getElementById('island-visited');
      if (_prov) _prov.remove();
      const _vis = data.provenance && data.provenance.visited;
      if (_vis) {
        const _vl = (typeof CURRENT_LANG !== 'undefined' && CURRENT_LANG === 'el') ? 'el' : 'en';
        const _stampEl = document.getElementById('island-lastupdated')
                      || document.getElementById('island-meta-info');
        if (_stampEl) {
          const _b = document.createElement('div');
          _b.id = 'island-visited';
          _b.className = 'island-visited';
          _b.innerHTML = '<span class="iv-dot" aria-hidden="true"></span>' + visitedLabel(_vis, _vl);
          _stampEl.parentNode.insertBefore(_b, _stampEl.nextSibling);
        }
      }
"""

JS_HELPER = """
/* Provenance stamp: "2025-06" -> "Visited by the author · June 2025".
   Year-only ("2025") is accepted and renders without a month. */
function visitedLabel(v, lang) {
  const MON_EN = ['January','February','March','April','May','June',
                  'July','August','September','October','November','December'];
  const MON_EL = ['Ιανουάριο','Φεβρουάριο','Μάρτιο','Απρίλιο','Μάιο','Ιούνιο',
                  'Ιούλιο','Αύγουστο','Σεπτέμβριο','Οκτώβριο','Νοέμβριο','Δεκέμβριο'];
  const m = String(v).match(/^(\\d{4})(?:-(\\d{2}))?$/);
  if (!m) return '';
  const year = m[1];
  const mi = m[2] ? parseInt(m[2], 10) - 1 : null;
  const when = (mi != null && mi >= 0 && mi < 12)
    ? (lang === 'el' ? MON_EL[mi] + ' ' + year : MON_EN[mi] + ' ' + year)
    : year;
  return lang === 'el'
    ? 'Το έχω επισκεφθεί · ' + when
    : 'Visited by the author · ' + when;
}
window.visitedLabel = visitedLabel;
"""

def patch_script():
    p = ROOT / 'script.js'
    s = p.read_text(encoding='utf-8')
    if 'blueprint-why' in s:
        return False
    anchor = '      guide.innerHTML = buildIslandPage(data, key);'
    if s.count(anchor) != 1:
        errors.append(f'script.js: {s.count(anchor)} matches for the render anchor'); return False
    s = s.replace(anchor, JS_RENDER.rstrip('\n') + '\n' + anchor)
    fn = 'function scoreVerdict(s) {'
    if s.count(fn) != 1:
        errors.append('script.js: cannot place visitedLabel()'); return False
    s = s.replace(fn, JS_HELPER.strip() + '\n\n' + fn)
    p.write_text(s, encoding='utf-8')
    return True

# ---------------------------------------------------------------- shells ---
# The EN shell links "#how-we-score", the EL one "/el/#how-we-score", so anchor
# on the part they share and walk back to the opening tag.
SHELL_ANCHOR = 'onclick="navMission(event)" class="how-we-score-link"'
def patch_shells():
    done = []
    for rel in ('index.html', 'el/index.html'):
        p = ROOT / rel
        s = p.read_text(encoding='utf-8')
        if 'blueprint-why' in s:
            continue
        if s.count(SHELL_ANCHOR) != 1:
            errors.append(f'{rel}: {s.count(SHELL_ANCHOR)} matches for the how-we-score link'); continue
        i = s.rfind('<a ', 0, s.find(SHELL_ANCHOR))
        if i < 0:
            errors.append(f'{rel}: how-we-score link not found'); continue
        s = s[:i] + '<p class="blueprint-why" id="blueprint-why" hidden></p>\n            ' + s[i:]
        p.write_text(s, encoding='utf-8'); done.append(rel)
    return done

CSS = """
/* --- Why this score + provenance (review fixes 2 & 3) ------------------- */
.blueprint-why {
  margin: 8px 0 10px;
  font-size: .855rem;
  line-height: 1.45;
  color: var(--ink-2);
  border-left: 3px solid var(--aegean);
  padding-left: 9px;
}
.island-visited {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 4px;
  font-size: .78rem;
  font-weight: 600;
  color: var(--olive, #6b7f4b);
}
.island-visited .iv-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--olive, #6b7f4b);
  flex: none;
}
"""

def patch_css():
    p = ROOT / 'style.css'
    s = p.read_text(encoding='utf-8')
    if '.blueprint-why' in s:
        return False
    p.write_text(s.rstrip('\n') + '\n' + CSS, encoding='utf-8')
    return True

def main():
    n = fold_why()
    js = patch_script()
    sh = patch_shells()
    css = patch_css()
    if errors:
        for e in errors: print('  !!', e, file=sys.stderr)
        return 1
    print(f'why_score folded into {n} island JSONs; script.js {"patched" if js else "already ok"}; '
          f'shells {sh or "already ok"}; style.css {"patched" if css else "already ok"}')
    return 0

sys.exit(main())
