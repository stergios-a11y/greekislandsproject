#!/usr/bin/env python3
"""Review fix 1/4 — make /privacy/ describe the site that actually exists.

Corrections (EN + EL):
  a. "no contact form"      -> the feedback form exists; it composes a mailto, no server
  b. "GitHub Pages"         -> Cloudflare Pages (actual host)
  c. "OpenStreetMap/Leaflet -> CARTO basemaps (OSM data) + Esri fallback
  d. hotel-booking example  -> ferries, car hire, accommodation (the live partners)
  e. consent banner         -> named as Google's certified CMP, + a manage-preferences link
  f. last-updated date bump
Idempotent: re-running changes nothing.
"""
import re, sys, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TODAY_EN = datetime.date.today().strftime('%-d %B %Y')
EL_MONTHS = ['Ιανουαρίου','Φεβρουαρίου','Μαρτίου','Απριλίου','Μαΐου','Ιουνίου',
             'Ιουλίου','Αυγούστου','Σεπτεμβρίου','Οκτωβρίου','Νοεμβρίου','Δεκεμβρίου']
_t = datetime.date.today()
TODAY_EL = f'{_t.day} {EL_MONTHS[_t.month-1]} {_t.year}'

MANAGE_EN = ('<p id="cookie-prefs-wrap" hidden>Ads and their consent choices are handled by Google\'s '
             'certified consent platform. <a href="#" id="cookie-prefs-link">Manage your cookie '
             'preferences</a>.</p>')
MANAGE_EL = ('<p id="cookie-prefs-wrap" hidden>Οι διαφημίσεις και οι επιλογές συγκατάθεσης διαχειρίζονται '
             'από την πιστοποιημένη πλατφόρμα συγκατάθεσης της Google. <a href="#" id="cookie-prefs-link">'
             'Διαχείριση προτιμήσεων cookies</a>.</p>')

# Shows the link only when Google's CMP is actually present on the page, so we never
# advertise a control that does nothing.
SCRIPT = """<script>
(function () {
  var wrap = document.getElementById('cookie-prefs-wrap');
  var link = document.getElementById('cookie-prefs-link');
  if (!wrap || !link) return;
  function open(e) {
    if (e) e.preventDefault();
    if (window.googlefc && window.googlefc.showRevocationMessage) {
      window.googlefc.showRevocationMessage();
    } else if (window.__tcfapi) {
      window.__tcfapi('displayConsentUi', 2, function () {});
    }
  }
  function check(tries) {
    if (window.googlefc || window.__tcfapi) { wrap.hidden = false; link.addEventListener('click', open); return; }
    if (tries > 0) setTimeout(function () { check(tries - 1); }, 400);
  }
  check(10);
})();
</script>"""

EDITS = {
 'privacy/index.html': [
  ("The site has no signup, no login, no comments, and no contact form. You can use the entire site without identifying yourself.",
   "The site has no signup, no login and no comments. There is a feedback form, but it does not send anything to a server: "
   "it assembles the text into a message and hands it to your own email program, which you then choose to send or discard. "
   "Nothing you type into it reaches this site. Apart from emailing me, you can use the entire site without identifying yourself."),
  ("The site is hosted on GitHub Pages, which keeps standard web-server logs",
   "The site is hosted on Cloudflare Pages, which keeps standard web-server logs"),
  ("<li><strong>OpenStreetMap / Leaflet</strong> — provides map tiles when you view the map. OpenStreetMap's <a href=\"https://wiki.osmfoundation.org/wiki/Privacy_Policy\" target=\"_blank\" rel=\"noopener\">privacy policy</a> applies to tile requests.</li>",
   "<li><strong>CARTO</strong> — serves the map tiles (drawn from <a href=\"https://www.openstreetmap.org/copyright\" target=\"_blank\" rel=\"noopener\">OpenStreetMap</a> data) when you open a map. If CARTO is unreachable the map falls back to Esri/ArcGIS tiles. Either provider sees your IP address for the tiles your browser requests.</li>"),
  ("Some pages may contain occasional affiliate links — for example to a hotel booking site. If you click through and make a purchase,",
   "Some pages carry affiliate links — currently ferry tickets (Ferryhopper, Ferryscanner), car hire (DiscoverCars) and accommodation (Booking.com). If you click through and make a booking,"),
  ("EU/UK visitors will see a consent banner before personalized ads are served.",
   "EU/UK visitors are shown Google's certified consent platform before personalized ads are served, and can change that choice at any time using the link below."),
  ("<p>The site does not use any other tracking pixel beyond what's listed above.</p>",
   "<p>The site does not use any other tracking pixel beyond what's listed above.</p>\n" + MANAGE_EN),
  ("<p class=\"updated\">Last updated: 10 May 2026</p>",
   f"<p class=\"updated\">Last updated: {TODAY_EN}</p>"),
 ],
 'el/privacy/index.html': [
  ("Η σελίδα δεν έχει εγγραφή, σύνδεση χρήστη, σχόλια ή φόρμα επικοινωνίας. Μπορείς να χρησιμοποιήσεις όλη τη σελίδα χωρίς να σε ταυτοποιήσει κανείς.",
   "Η σελίδα δεν έχει εγγραφή, σύνδεση χρήστη ή σχόλια. Υπάρχει φόρμα σχολίων, αλλά δεν στέλνει τίποτα σε server: "
   "συνθέτει το κείμενο σε ένα μήνυμα και το παραδίδει στο δικό σου πρόγραμμα email, το οποίο μετά αποφασίζεις αν θα στείλεις. "
   "Τίποτα από όσα γράφεις εκεί δεν φτάνει σε αυτή τη σελίδα. Πέρα από το να μου στείλεις email, μπορείς να χρησιμοποιήσεις όλη τη σελίδα χωρίς να σε ταυτοποιήσει κανείς."),
  ("Η σελίδα φιλοξενείται στο GitHub Pages, που κρατά τυπικά logs",
   "Η σελίδα φιλοξενείται στο Cloudflare Pages, που κρατά τυπικά logs"),
  ("<li><strong>OpenStreetMap / Leaflet</strong> — παρέχει τα tiles του χάρτη όταν ανοίγεις τον χάρτη. Η <a href=\"https://wiki.osmfoundation.org/wiki/Privacy_Policy\" target=\"_blank\" rel=\"noopener\">πολιτική απορρήτου του OpenStreetMap</a> ισχύει για τα αιτήματα tiles.</li>",
   "<li><strong>CARTO</strong> — παρέχει τα tiles του χάρτη (με δεδομένα από το <a href=\"https://www.openstreetmap.org/copyright\" target=\"_blank\" rel=\"noopener\">OpenStreetMap</a>) όταν ανοίγεις έναν χάρτη. Αν η CARTO δεν είναι διαθέσιμη, ο χάρτης γυρίζει σε tiles της Esri/ArcGIS. Και οι δύο πάροχοι βλέπουν την IP σου για τα tiles που ζητά ο browser σου.</li>"),
  ("Ορισμένες σελίδες ίσως περιέχουν περιστασιακούς affiliate συνδέσμους — για παράδειγμα προς πλατφόρμα κρατήσεων ξενοδοχείων. Αν κάνεις κλικ και κάνεις κράτηση,",
   "Ορισμένες σελίδες έχουν affiliate συνδέσμους — αυτή τη στιγμή για ακτοπλοϊκά εισιτήρια (Ferryhopper, Ferryscanner), ενοικίαση αυτοκινήτου (DiscoverCars) και διαμονή (Booking.com). Αν κάνεις κλικ και κάνεις κράτηση,"),
  ("Οι επισκέπτες από ΕΕ/Ηνωμένο Βασίλειο θα βλέπουν banner συγκατάθεσης πριν προβληθεί εξατομικευμένη διαφήμιση.",
   "Στους επισκέπτες από ΕΕ/Ηνωμένο Βασίλειο εμφανίζεται η πιστοποιημένη πλατφόρμα συγκατάθεσης της Google πριν προβληθεί εξατομικευμένη διαφήμιση, και μπορούν να αλλάξουν την επιλογή τους οποτεδήποτε από τον παρακάτω σύνδεσμο."),
 ],
}

def main():
    changed = []
    for rel, pairs in EDITS.items():
        p = ROOT / rel
        src = p.read_text(encoding='utf-8')
        out = src
        for old, new in pairs:
            if new in out:
                continue                      # already applied
            if old not in out:
                print(f'  !! not found in {rel}: {old[:60]}…', file=sys.stderr)
                return 1
            if out.count(old) != 1:
                print(f'  !! {out.count(old)} matches in {rel}: {old[:60]}…', file=sys.stderr)
                return 1
            out = out.replace(old, new)
        if out != src:
            p.write_text(out, encoding='utf-8')
            changed.append(rel)
    # EL: manage-preferences block + date, anchored on whatever the EL wording is
    p = ROOT / 'el/privacy/index.html'
    s = p.read_text(encoding='utf-8')
    if 'cookie-prefs-wrap' not in s:
        m = re.search(r'(<h2>[^<]*[Aa]ffiliate[^<]*</h2>)', s)
        if not m:
            print('  !! EL: no affiliate heading to anchor the cookie block', file=sys.stderr); return 1
        s = s[:m.start()] + MANAGE_EL + '\n\n' + s[m.start():]
    s = re.sub(r'(<p class="updated">[^:]*:\s*)[^<]*(</p>)', r'\g<1>' + TODAY_EL + r'\2', s)
    p.write_text(s, encoding='utf-8'); changed.append('el/privacy/index.html')
    # inject the CMP script into both, once
    for rel in ('privacy/index.html', 'el/privacy/index.html'):
        p = ROOT / rel
        s = p.read_text(encoding='utf-8')
        if 'cookie-prefs-link' in s and "googlefc" not in s:
            s = s.replace('</body>', SCRIPT + '\n</body>')
            p.write_text(s, encoding='utf-8')
    print('privacy: updated', ', '.join(sorted(set(changed))))
    return 0

sys.exit(main())
