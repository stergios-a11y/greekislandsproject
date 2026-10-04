#!/usr/bin/env python3
"""Review fix 4 — stop arguing with the internet on pages that should be selling
the benefit.

The anti-SEO / anti-TripAdvisor framing is good once. It currently runs four
times inside the mission section. This keeps the strongest instance
(mission.why.p1, the stock-photos-of-Oia line) and turns the rest into what the
reader actually gets. It also rewrites the festivals decision card, which was
describing why panigiria matter instead of what the page does.

Nothing outside the mission section and that one card is touched. Idempotent.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

AUTHOR_NOTE_EN = ('This matters because it changes the advice. Someone who has been there tells you '
                  'which beach is unusable in a north wind, which village is shut in May, and which '
                  'ferry connection exists on the timetable but not in practice. That is the part you '
                  'cannot get from reviews.')
AUTHOR_NOTE_EL = ('Αυτό αλλάζει τη συμβουλή. Κάποιος που έχει πάει σου λέει ποια παραλία δεν πατιέται '
                  'με βοριά, ποιο χωριό είναι κλειστό τον Μάιο, και ποια ακτοπλοϊκή σύνδεση υπάρχει '
                  'στο χαρτί αλλά όχι στην πράξη. Αυτό δεν το βρίσκεις στις κριτικές.')

FEST_EN = ("The panigiria and feast days on the island you're going to — the village, the date, and "
           "whether it's worth planning around.")
FEST_EL = ('Τα πανηγύρια και οι γιορτές στο νησί που πας — χωριό, ημερομηνία, και αν αξίζει να το '
           'προγραμματίσεις.')

EDITS = {
 'index.html': [
  # 1. the duplicate jab -> the concrete benefit
  ('This matters because the alternative is what everyone else does: aggregate reviews from '
   'TripAdvisor, run them through an SEO mill, translate the output into every language, and '
   'publish it as a "guide." The writing reads fine. The advice is worthless.',
   AUTHOR_NOTE_EN),
  # 2. trailing jab on the sources list
  (' Wikipedia for historical facts. Not from SEO-farm aggregators.',
   ' Wikipedia for historical facts.'),
  # 3. the scores explanation keeps its point, drops the third TripAdvisor mention
  ("These aren't computed by an algorithm and they aren't scraped from TripAdvisor. They're one "
   "person's informed judgment",
   "These aren't computed by an algorithm and they aren't scraped from anywhere. They're one "
   "person's informed judgment"),
  # 4. festivals card: say what the page does
  ('<p>Every panigiri and feast day across the islands, by date — the deepest-rooted thing an island does.</p>',
   f'<p>{FEST_EN}</p>'),
 ],
 'el/index.html': [
  ('Η εναλλακτική είναι αυτό που κάνουν όλοι: κριτικές από TripAdvisor, πέρασμα από SEO μηχανή, '
   'μετάφραση σε όλες τις γλώσσες, και το λένε «οδηγό». Το κείμενο διαβάζεται μια χαρά. Η συμβουλή '
   'έχει μικρή χρησιμότητα.',
   AUTHOR_NOTE_EL),
  (' Wikipedia για ιστορικά στοιχεία. Όχι από SEO-farm συλλογείς.',
   ' Wikipedia για ιστορικά στοιχεία.'),
  ('<p>Κάθε πανηγύρι και γιορτή στα νησιά, ανά ημερομηνία — το πιο βαθιά ριζωμένο κομμάτι κάθε νησιού.</p>',
   f'<p>{FEST_EL}</p>'),
 ],
 'i18n.js': [
  ('The alternative is what everyone else does: aggregate TripAdvisor reviews, run them through an '
   'SEO mill, translate the output, and call it a "guide." The writing reads fine. The advice is '
   'worthless.',
   AUTHOR_NOTE_EN),
  ('Η εναλλακτική είναι αυτό που κάνουν όλοι: κριτικές από TripAdvisor, πέρασμα από SEO μηχανή, '
   'μετάφραση σε όλες τις γλώσσες, και το λένε «οδηγό». Το κείμενο διαβάζεται μια χαρά. Η συμβουλή '
   'έχει μικρή χρησιμότητα.',
   AUTHOR_NOTE_EL),
  (' Wikipedia for historical facts. Not from SEO-farm aggregators.',
   ' Wikipedia for historical facts.'),
  (' Wikipedia για ιστορικά στοιχεία. Όχι από SEO-farm συλλογείς.',
   ' Wikipedia για ιστορικά στοιχεία.'),
 ],
}

def main():
    changed = []
    for rel, pairs in EDITS.items():
        p = ROOT / rel
        s = p.read_text(encoding='utf-8')
        orig = s
        for old, new in pairs:
            if new in s:
                continue
            if s.count(old) != 1:
                print(f'  !! {rel}: {s.count(old)} matches for {old[:60]}…', file=sys.stderr)
                return 1
            s = s.replace(old, new)
        if s != orig:
            p.write_text(s, encoding='utf-8'); changed.append(rel)
    print('copy:', ', '.join(changed) if changed else 'already applied')
    return 0

sys.exit(main())
