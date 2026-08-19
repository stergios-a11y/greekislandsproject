#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ^ explicit declaration: this file contains Greek titles and descriptions, and
#   some interpreters refuse non-ASCII source without it (PEP 263).
"""Generate static, SEO-indexable comparison pages at /compare/<a>-vs-<b>/.

Each page is:
  - The same SPA shell as index.html (header, nav, footer, fonts, CSS)
  - The same #view-compare skeleton — radar chart, cards, etc. all render
    identically to /#compare when the SPA hydrates
  - A unique <title> + <meta description> + canonical URL per pair
  - The editorial verdict from vs_verdicts.json baked into the HTML so
    Google crawls it without executing JavaScript
  - The FAQ from vs_faqs.json (where present) baked into the HTML AND
    serialized as FAQPage JSON-LD in <head> for rich-snippet eligibility
  - An inline boot hint window.__INITIAL_COMPARE_PAIR so the SPA pre-fills
    the dropdowns on first paint, no flash of the default pair

The earlier teardown (commit 02e1f3b4) was driven by the OLD static pages
looking visually different from the SPA. This rebuild guarantees identical
appearance by reusing the same shell — only the URL changes.

Reads:  vs_verdicts.json, vs_faqs.json, island metadata in script.js
Writes: compare/<slug>/index.html, el/compare/<slug>/index.html
"""
import hashlib
import json
import re
from pathlib import Path

def _resolve_root():
    candidates = []
    try:
        candidates.append(Path(__file__).resolve().parent.parent)
    except NameError:
        pass
    candidates.append(Path.cwd())
    cwd = Path.cwd()
    for _ in range(4):
        candidates.append(cwd)
        cwd = cwd.parent
    for c in candidates:
        if (c / 'vs_verdicts.json').is_file() and (c / 'script.js').is_file():
            return c
    raise SystemExit(
        "Could not find project root. Run from inside the project, e.g. "
        "`cd ~/greekislandsproject && python3 tools/build_compare_pages.py`."
    )

ROOT = _resolve_root()
SITE_URL = 'https://aegeanblueprint.com'
ASSET_V = 100

# style.css has its own version; using ASSET_V here meant compare pages asked
# for a different ?v= of the same stylesheet than every other page.
def _style_v():
    try:
        return int(re.search(r'style\.css\?v=(\d+)', (ROOT / 'index.html').read_text(encoding='utf-8')).group(1))
    except Exception:
        return ASSET_V


STYLE_V = _style_v()

from datetime import date as _date
YEAR = _date.today().year
TITLE_OVERRIDES = {('chania', 'rethymno'): ('Chania vs Rethymno {y}: Chania Wins on Beaches — Honest Pick', 'Χανιά ή Ρέθυμνο {y}: Τα Χανιά Κερδίζουν στις Παραλίες'), ('corfu', 'zakynthos'): ('Corfu vs Zakynthos {y}: Old Town or Better Beaches?', 'Κέρκυρα ή Ζάκυνθος {y}: Παλιά Πόλη ή Καλύτερες Παραλίες;'), ('mykonos', 'paros'): ('Mykonos vs Paros {y}: Same Nightlife, Half the Price', 'Μύκονος ή Πάρος {y}: Ίδια Νυχτερινή Ζωή, Μισή Τιμή'), ('kos', 'rhodes'): ('Kos vs Rhodes {y}: Rhodes for History, Kos for Easy', 'Κως ή Ρόδος {y}: Ρόδος για Ιστορία, Κως για Ευκολία'), ('corfu', 'rhodes'): ('Corfu vs Rhodes {y}: Two Old Towns, One Clear Winner', 'Κέρκυρα ή Ρόδος {y}: Δύο Παλιές Πόλεις, Ένας Νικητής'), ('kefalonia', 'zakynthos'): ('Kefalonia vs Zakynthos {y}: Quiet Coves or Party Coast?', 'Κεφαλονιά ή Ζάκυνθος {y}: Ήσυχοι Όρμοι ή Πάρτι;'), ('naxos', 'paros'): ('Naxos vs Paros {y}: Which Cyclade Actually Suits You?', 'Νάξος ή Πάρος {y}: Ποια Κυκλάδα σού Ταιριάζει Πραγματικά;'), ('ios', 'santorini'): ('Ios vs Santorini {y}: Caldera Views or Cheaper Nights?', 'Ίος ή Σαντορίνη {y}: Καλντέρα ή Φθηνότερες Νύχτες;'), ('milos', 'naxos'): ('Milos vs Naxos {y}: Strange Coastline or All-Rounder?', 'Μήλος ή Νάξος {y}: Παράξενη Ακτή ή Ολοκληρωμένο Νησί;')}
DESC_OVERRIDES = {('chania', 'rethymno'): ("Chania scores 4.8 to Rethymno's 3.8 — better beaches, better old town, more to do. But Rethymno is cheaper and quieter. Which one fits your trip, honestly.", 'Τα Χανιά βαθμολογούνται 4.8 έναντι 3.8 του Ρεθύμνου — καλύτερες παραλίες, καλύτερη παλιά πόλη. Το Ρέθυμνο όμως είναι φθηνότερο και πιο ήσυχο. Ειλικρινής σύγκριση.'), ('corfu', 'zakynthos'): ('Zakynthos has the better beaches (4.8 vs 3.9); Corfu has the far better old town (4.8 vs 2.5). Scored side by side on beaches, nightlife, access and price.', 'Η Ζάκυνθος έχει καλύτερες παραλίες (4.8 έναντι 3.9)· η Κέρκυρα πολύ καλύτερη παλιά πόλη (4.8 έναντι 2.5). Αναλυτική σύγκριση με βαθμολογίες.'), ('mykonos', 'paros'): ("Both score 5.0 for nightlife and Paros beats Mykonos on beaches — at a fraction of the cost. When Mykonos is still worth it, and when it isn't.", 'Και τα δύο 5.0 στη νυχτερινή ζωή, και η Πάρος κερδίζει στις παραλίες — με πολύ μικρότερο κόστος. Πότε αξίζει η Μύκονος και πότε όχι.'), ('kos', 'rhodes'): ('Rhodes wins overall (4.4 vs 3.7) on history and old town; Kos is flatter, cheaper and easier to get around by bike. Scored on beaches, nightlife and price.', 'Η Ρόδος κερδίζει συνολικά (4.4 έναντι 3.7) σε ιστορία και παλιά πόλη· η Κως είναι πιο επίπεδη, φθηνότερη και ευκολότερη με ποδήλατο. Με βαθμολογίες.'), ('corfu', 'rhodes'): ('Two UNESCO old towns compared: Rhodes edges it overall (4.4 vs 4.2) with the stronger medieval core, Corfu is greener with better food. Scored side by side.', 'Δύο παλιές πόλεις UNESCO: η Ρόδος υπερτερεί οριακά (4.4 έναντι 4.2) με ισχυρότερο μεσαιωνικό πυρήνα, η Κέρκυρα είναι πιο πράσινη με καλύτερο φαγητό.'), ('kefalonia', 'zakynthos'): ('Dead level overall at 4.1 each — Zakynthos for nightlife and Navagio, Kefalonia for quiet coves and mountains. The honest split, scored.', 'Ισοπαλία στο 4.1 — Ζάκυνθος για νυχτερινή ζωή και Ναυάγιο, Κεφαλονιά για ήσυχους όρμους και βουνά. Η ειλικρινής διαφορά, με βαθμολογίες.')}

# --- Saronic day-trip set + the three Evia regions -------------------------
# The default template would produce "Evia (Central) vs Evia (North)", which
# reads badly and wastes the title. All six get a verdict-led title instead.
TITLE_OVERRIDES.update({
    ('agistri', 'salamis'): (
        "Agistri vs Salamina {y}: Only One Is Worth Swimming In",
        'Αγκίστρι ή Σαλαμίνα {y}: Μόνο στο Ένα Αξίζει το Μπάνιο'),
    ('aegina', 'salamis'): (
        "Aegina vs Salamina {y}: Closest Isn't Best",
        'Αίγινα ή Σαλαμίνα {y}: Το Πιο Κοντινό Δεν Είναι Καλύτερο'),
    ('agistri', 'poros'): (
        'Agistri vs Poros {y}: Better Swimming or Better Town?',
        'Αγκίστρι ή Πόρος {y}: Καλύτερο Μπάνιο ή Καλύτερη Πόλη;'),
    ('evia-central', 'evia-north'): (
        'Central vs North Evia {y}: No Ferry or No Bills?',
        'Κεντρική ή Βόρεια Εύβοια {y}: Χωρίς Πλοίο ή Χωρίς Έξοδα;'),
    ('evia-north', 'evia-south'): (
        'North vs South Evia {y}: South Wins on Beaches',
        'Βόρεια ή Νότια Εύβοια {y}: Ο Νότος Κερδίζει στις Παραλίες'),
    ('evia-central', 'evia-south'): (
        'Central vs South Evia {y}: Ancient Sites or Best Beaches?',
        'Κεντρική ή Νότια Εύβοια {y}: Αρχαία ή Καλύτερες Παραλίες;'),
})
DESC_OVERRIDES.update({
    ('agistri', 'salamis'): (
        "Agistri scores 3.4 to Salamina's 2.8, and the gap is water: 3.5 for beaches "
        'against 2.0. Salamina has the 480 BC battle and a 15-minute ferry. Honest pick.',
        'Το Αγκίστρι βαθμολογείται 3.4 έναντι 2.8 της Σαλαμίνας, και η διαφορά είναι το νερό: '
        '3.5 στις παραλίες έναντι 2.0. Η Σαλαμίνα έχει τη ναυμαχία και 15 λεπτά πλοίο.'),
    ('aegina', 'salamis'): (
        'Aegina wins 3.3 to 2.8 on the Temple of Aphaia, Perdika fish tavernas and easier '
        'ferries. Salamina is closer and cheaper. Neither is a beach island — 2.5 vs 2.0.',
        'Η Αίγινα κερδίζει 3.3 έναντι 2.8 με τον Ναό της Αφαίας, τις ψαροταβέρνες της Πέρδικας '
        'και ευκολότερα πλοία. Η Σαλαμίνα είναι πιο κοντά και φθηνότερη. Καμία για παραλίες.'),
    ('agistri', 'poros'): (
        "Poros edges it 3.5 to 3.4 on town and culture (4.2 vs 2.5); Agistri wins beaches "
        '(3.5 vs 3.0), price and needs no car at all. Swim on Agistri, stay on Poros.',
        'Ο Πόρος υπερτερεί 3.5 έναντι 3.4 σε πόλη και πολιτισμό (4.2 έναντι 2.5)· το Αγκίστρι '
        'κερδίζει σε παραλίες (3.5 έναντι 3.0), τιμή, και δεν θέλει καθόλου αυτοκίνητο.'),
    ('evia-central', 'evia-north'): (
        'Central Evia scores 3.9 to 3.6: no ferry at all via the Chalkida bridge, plus ancient '
        'Eretria and Mt Dirfys. North Evia is cheapest on the island (4.8) with thermal springs.',
        'Η Κεντρική Εύβοια βαθμολογείται 3.9 έναντι 3.6: χωρίς πλοίο μέσω της Χαλκίδας, με την '
        'αρχαία Ερέτρια και τη Δίρφη. Η Βόρεια είναι η φθηνότερη (4.8) με ιαματικές πηγές.'),
    ('evia-north', 'evia-south'): (
        'South Evia wins 3.9 to 3.6 on the best beaches on the island (4.6 vs 3.8) and the '
        'Dimosari gorge. North Evia is cheaper (4.8) with the Edipsos thermal springs.',
        'Η Νότια Εύβοια κερδίζει 3.9 έναντι 3.6 με τις καλύτερες παραλίες του νησιού (4.6 έναντι '
        '3.8) και το φαράγγι του Δημοσάρη. Η Βόρεια είναι φθηνότερη (4.8) με τα Λουτρά Αιδηψού.'),
    ('evia-central', 'evia-south'): (
        'A real tie at 3.9 each. Central wins culture (4.5 vs 3.5) and needs no ferry; South '
        'wins beaches decisively (4.6 vs 3.5) plus Mt Ochi and Karystos. Scored side by side.',
        'Πραγματική ισοπαλία στο 3.9. Η Κεντρική κερδίζει στον πολιτισμό (4.5 έναντι 3.5) και δεν '
        'θέλει πλοίο· η Νότια κερδίζει καθαρά στις παραλίες (4.6 έναντι 3.5), με Όχη και Κάρυστο.'),
})

# --- Dodecanese + NE Aegean decisions --------------------------------------
TITLE_OVERRIDES.update({
    ('karpathos', 'kos'): (
        'Karpathos vs Kos {y}: Wild Beaches or Easy Flights?',
        'Κάρπαθος ή Κως {y}: Άγριες Παραλίες ή Εύκολες Πτήσεις;'),
    ('chios', 'samos'): (
        'Chios vs Samos {y}: Mastic Villages or Ancient Engineering?',
        'Χίος ή Σάμος {y}: Μαστιχοχώρια ή Αρχαία Μηχανική;'),
})
DESC_OVERRIDES.update({
    ('karpathos', 'kos'): (
        "Karpathos wins on beaches (4.4 vs 4.0) and emptiness; Kos wins on access 4.6 to 2.0 "
        '— direct flights, flat cycling, the Asklepion. The honest Dodecanese decision.',
        'Η Κάρπαθος κερδίζει στις παραλίες (4.4 έναντι 4.0) και στην ερημιά· η Κως στην πρόσβαση '
        '4.6 έναντι 2.0 — απευθείας πτήσεις, ποδήλατο, Ασκληπιείο. Ειλικρινής σύγκριση.'),
    ('chios', 'samos'): (
        'Chios edges it 3.6 to 3.3 on the mastic villages and Nea Moni (culture 4.7); Samos is '
        'greener with better beaches, the Eupalinos Tunnel and Ephesus an hour away.',
        'Η Χίος υπερτερεί 3.6 έναντι 3.3 με τα Μαστιχοχώρια και τη Νέα Μονή (πολιτισμός 4.7)· η '
        'Σάμος είναι πιο πράσινη με καλύτερες παραλίες, το Ευπαλίνειο και την Έφεσο μία ώρα μακριά.'),
})

# --- NE Aegean + the four missing Sporades pairs ---------------------------
TITLE_OVERRIDES.update({
    ('lemnos', 'lesvos'): (
        'Lemnos vs Lesvos {y}: Better Beaches or More Island?',
        'Λήμνος ή Λέσβος {y}: Καλύτερες Παραλίες ή Πιο Πολύ Νησί;'),
    ('alonnisos', 'skiathos'): (
        'Alonnisos vs Skiathos {y}: Monk Seals or Party Beaches?',
        'Αλόννησος ή Σκιάθος {y}: Φώκιες ή Παραλίες με Πάρτι;'),
    ('skiathos', 'skyros'): (
        'Skiathos vs Skyros {y}: Not Actually the Same Trip',
        'Σκιάθος ή Σκύρος {y}: Δεν Είναι το Ίδιο Ταξίδι'),
    ('skopelos', 'skyros'): (
        'Skopelos vs Skyros {y}: Pine Forest or Cycladic Chora?',
        'Σκόπελος ή Σκύρος {y}: Πευκοδάσος ή Κυκλαδίτικη Χώρα;'),
    ('alonnisos', 'skyros'): (
        'Alonnisos vs Skyros {y}: Marine Park or Living Folklore?',
        'Αλόννησος ή Σκύρος {y}: Θαλάσσιο Πάρκο ή Ζωντανή Παράδοση;'),
})
DESC_OVERRIDES.update({
    ('lemnos', 'lesvos'): (
        "Lesvos scores 4.0 to Lemnos's 3.7 on culture (4.7 vs 3.5) — but Lemnos has better "
        'beaches (4.3 vs 4.0) and fits three days where Lesvos needs six. Scored side by side.',
        'Η Λέσβος βαθμολογείται 4.0 έναντι 3.7 στον πολιτισμό (4.7 έναντι 3.5) — αλλά η Λήμνος έχει '
        'καλύτερες παραλίες (4.3 έναντι 4.0) και χωράει σε τρεις μέρες όπου η Λέσβος θέλει έξι.'),
    ('alonnisos', 'skiathos'): (
        'Nearly level at 3.9 vs 3.8 with almost the same beach score — so it comes down to crowds '
        'and cost. Skiathos flies direct; Alonnisos has the marine park and is cheaper.',
        'Σχεδόν ισοπαλία 3.9 έναντι 3.8 με σχεδόν ίδια βαθμολογία παραλιών — κρίνεται στον κόσμο και '
        'το κόστος. Η Σκιάθος έχει απευθείας πτήσεις· η Αλόννησος το θαλάσσιο πάρκο και φθηνότερα.'),
    ('skiathos', 'skyros'): (
        'Both are Sporades but not on the same ferry network — Skiathos from Volos, Skyros from '
        'Kymi. Skiathos wins beaches 4.6 to 4.0; Skyros wins culture 3.8 to 2.0.',
        'Και οι δύο Σποράδες αλλά όχι στο ίδιο δίκτυο πλοίων — Σκιάθος από Βόλο, Σκύρος από Κύμη. '
        'Η Σκιάθος κερδίζει στις παραλίες 4.6 έναντι 4.0· η Σκύρος στον πολιτισμό 3.8 έναντι 2.0.'),
    ('skopelos', 'skyros'): (
        'Skopelos edges it 3.6 to 3.4 on pine forest and beaches (4.2 vs 4.0); Skyros is cheaper '
        'with stronger culture (3.8 vs 3.2) and a chora that looks Cycladic. Not combinable.',
        'Η Σκόπελος υπερτερεί 3.6 έναντι 3.4 με πευκοδάσος και παραλίες (4.2 έναντι 4.0)· η Σκύρος '
        'είναι φθηνότερη με ισχυρότερο πολιτισμό (3.8 έναντι 3.2) και κυκλαδίτικη χώρα.'),
    ('alonnisos', 'skyros'): (
        'The two quietest Sporades. Alonnisos wins 3.8 to 3.4 on beaches and the marine park; '
        'Skyros on culture (3.8 vs 3.0), price and the goat-mask carnival.',
        'Οι δύο ησυχότερες Σποράδες. Η Αλόννησος κερδίζει 3.8 έναντι 3.4 σε παραλίες και θαλάσσιο '
        'πάρκο· η Σκύρος στον πολιτισμό (3.8 έναντι 3.0), στην τιμή και στο καρναβάλι.'),
})

# --- enrichment batch 1: highest-traffic thin verdicts, now long-form --------
TITLE_OVERRIDES.update({
    ('kefalonia', 'lefkada'): (
        'Kefalonia vs Lefkada {y}: The Closest Call in the Ionian',
        'Κεφαλονιά ή Λευκάδα {y}: Η Πιο Δύσκολη Επιλογή στο Ιόνιο'),
    ('corfu', 'lefkada'): (
        'Corfu vs Lefkada {y}: Old Town or the Beach Wall?',
        'Κέρκυρα ή Λευκάδα {y}: Παλιά Πόλη ή Τείχος Παραλιών;'),
    ('milos', 'sifnos'): (
        'Milos vs Sifnos {y}: Landscape or Dinner?',
        'Μήλος ή Σίφνος {y}: Τοπίο ή Δείπνο;'),
})
DESC_OVERRIDES.update({
    ('kefalonia', 'lefkada'): (
        "Kefalonia takes it 4.1 to 4.0, but Lefkada has the better beaches (4.9 vs 4.7) and a "
        'bridge instead of a ferry. Scale and culture against concentration and price.',
        'Η Κεφαλονιά κερδίζει 4.1 έναντι 4.0, αλλά η Λευκάδα έχει καλύτερες παραλίες (4.9 έναντι 4.7) '
        'και γεφύρι αντί για πλοίο. Κλίμακα και πολιτισμός έναντι συγκέντρωσης και τιμής.'),
    ('corfu', 'lefkada'): (
        'Corfu wins 4.2 to 4.0 on its UNESCO Old Town (culture 4.8 vs 2.5); Lefkada wins beaches '
        '4.9 to 3.9 and costs less. Two opposite ideas of an Ionian holiday, scored.',
        'Η Κέρκυρα κερδίζει 4.2 έναντι 4.0 με την Παλιά Πόλη UNESCO (πολιτισμός 4.8 έναντι 2.5)· η '
        'Λευκάδα στις παραλίες 4.9 έναντι 3.9 και κοστίζει λιγότερο. Δύο αντίθετες ιδέες διακοπών.'),
    ('milos', 'sifnos'): (
        "Milos wins 4.7 to 3.9 on a perfect 5.0 beach score — Sarakiniko, Kleftiko, 70 beaches. "
        'Sifnos wins on food, walking and price (3.5 vs 2.8). Not a close call, but not a wrong one.',
        'Η Μήλος κερδίζει 4.7 έναντι 3.9 με άριστα 5.0 στις παραλίες — Σαρακήνικο, Κλέφτικο, 70 '
        'παραλίες. Η Σίφνος κερδίζει σε φαγητό, περπάτημα και τιμή (3.5 έναντι 2.8).'),
})

# --- enrichment batch 2 -----------------------------------------------------
# chania/heraklion also FIXES a factually wrong generic title: the template was
# emitting "Crete (Chania) vs Crete (Heraklion): Which Greek Island Should You
# Visit?" — they are two ends of the same island.
TITLE_OVERRIDES.update({
    ('chania', 'heraklion'): (
        'Chania vs Heraklion {y}: Same Island, Opposite Trips',
        'Χανιά ή Ηράκλειο {y}: Ίδιο Νησί, Αντίθετα Ταξίδια'),
    ('antiparos', 'paros'): (
        'Antiparos vs Paros {y}: Seven Minutes, Two Different Islands',
        'Αντίπαρος ή Πάρος {y}: Επτά Λεπτά, Δύο Άλλα Νησιά'),
    ('folegandros', 'milos'): (
        'Folegandros vs Milos {y}: Stillness or Spectacle?',
        'Φολέγανδρος ή Μήλος {y}: Ησυχία ή Θέαμα;'),
})
DESC_OVERRIDES.update({
    ('chania', 'heraklion'): (
        'Two ends of Crete, not two islands. Chania scores 4.8 — the highest here — on beaches '
        '5.0 vs 3.5; Heraklion holds the only perfect 5.0 culture score, for Knossos and the museum.',
        'Δύο άκρα της Κρήτης, όχι δύο νησιά. Τα Χανιά βαθμολογούνται 4.8 — το υψηλότερο εδώ — με '
        'παραλίες 5.0 έναντι 3.5· το Ηράκλειο κρατά το μόνο άριστο 5.0 στον πολιτισμό.'),
    ('antiparos', 'paros'): (
        'Seven minutes apart, 4.1 vs 4.0, and completely different in scale. Paros has perfect 5.0 '
        'beaches and nightlife; Antiparos is one Chora and two days. Neither is the cheap one.',
        'Επτά λεπτά μακριά, 4.1 έναντι 4.0, και τελείως διαφορετικής κλίμακας. Η Πάρος έχει άριστα '
        '5.0 σε παραλίες και νυχτερινή ζωή· η Αντίπαρος μια Χώρα και δύο μέρες.'),
    ('folegandros', 'milos'): (
        "Milos wins 4.7 to 4.0 on a perfect 5.0 beach score — Sarakiniko, Kleftiko, 70 beaches. "
        'Folegandros has the better chora and the stillness, but costs the same as Paros.',
        'Η Μήλος κερδίζει 4.7 έναντι 4.0 με άριστα 5.0 στις παραλίες — Σαρακήνικο, Κλέφτικο, 70 '
        'παραλίες. Η Φολέγανδρος έχει καλύτερη χώρα και ησυχία, αλλά κοστίζει όσο η Πάρος.'),
})

# --- title/description pass: off the generic template ------------------------
# 26 of these had full long-form verdicts but were still emitting
# "X vs Y: Which Greek Island Should You Visit?"; 4 more were rendering the
# awkward "Crete (Heraklion) vs ...". Each title now states the page's verdict.
TITLE_OVERRIDES.update({
    ('corfu', 'kefalonia'): (
        'Corfu vs Kefalonia {y}: Culture or Coastline?',
        'Κέρκυρα ή Κεφαλονιά {y}: Πολιτισμός ή Ακτογραμμή;'),
    ('hydra', 'spetses'): (
        'Hydra vs Spetses {y}: No Cars or More Beach?',
        'Ύδρα ή Σπέτσες {y}: Χωρίς Αυτοκίνητα ή Πιο Παραλία;'),
    ('aegina', 'hydra'): (
        'Aegina vs Hydra {y}: Working Island or Film Set?',
        'Αίγινα ή Ύδρα {y}: Ζωντανό Νησί ή Σκηνικό;'),
    ('ios', 'paros'): (
        'Ios vs Paros {y}: Party Island or All-Rounder?',
        'Ίος ή Πάρος {y}: Νησί για Πάρτι ή Ολοκληρωμένο;'),
    ('paros', 'sifnos'): (
        'Paros vs Sifnos {y}: Beaches and Bars or Dinner?',
        'Πάρος ή Σίφνος {y}: Παραλίες και Μπαρ ή Δείπνο;'),
    ('kea', 'kythnos'): (
        'Kea vs Kythnos {y}: Closer to Athens or Better Beaches?',
        'Κέα ή Κύθνος {y}: Πιο Κοντά στην Αθήνα ή Καλύτερες Παραλίες;'),
    ('aegina', 'agistri'): (
        'Aegina vs Agistri {y}: Temple and Town or Just Swimming?',
        'Αίγινα ή Αγκίστρι {y}: Ναός και Πόλη ή Μόνο Μπάνιο;'),
    ('mykonos', 'rhodes'): (
        'Mykonos vs Rhodes {y}: Nightlife or a Medieval City?',
        'Μύκονος ή Ρόδος {y}: Νυχτερινή Ζωή ή Μεσαιωνική Πόλη;'),
    ('milos', 'santorini'): (
        'Milos vs Santorini {y}: Beaches or the View?',
        'Μήλος ή Σαντορίνη {y}: Παραλίες ή η Θέα;'),
    ('ios', 'mykonos'): (
        'Ios vs Mykonos {y}: Same 5.0 Nightlife, Far Less Money',
        'Ίος ή Μύκονος {y}: Ίδια Νυχτερινή Ζωή, Πολύ Λιγότερα Λεφτά'),
    ('chania', 'corfu'): (
        'Chania vs Corfu {y}: The Beaches Decide It',
        'Χανιά ή Κέρκυρα {y}: Οι Παραλίες Κρίνουν'),
    ('paros', 'santorini'): (
        'Paros vs Santorini {y}: Beaches or the Caldera?',
        'Πάρος ή Σαντορίνη {y}: Παραλίες ή Καλντέρα;'),
    ('rhodes', 'santorini'): (
        'Rhodes vs Santorini {y}: A Week or Three Nights?',
        'Ρόδος ή Σαντορίνη {y}: Μια Εβδομάδα ή Τρεις Νύχτες;'),
    ('chania', 'santorini'): (
        'Chania vs Santorini {y}: Both 4.8, Nothing Alike',
        'Χανιά ή Σαντορίνη {y}: Και τα Δύο 4.8, Τίποτα Κοινό'),
    ('amorgos', 'astypalaia'): (
        'Amorgos vs Astypalaia {y}: Cliffs or Castle?',
        'Αμοργός ή Αστυπάλαια {y}: Βράχια ή Κάστρο;'),
    ('donousa', 'schoinoussa'): (
        'Donousa vs Schoinoussa {y}: Sisters, Not Rivals',
        'Δονούσα ή Σχοινούσα {y}: Αδελφές, Όχι Αντίπαλες'),
    ('mykonos', 'santorini'): (
        'Mykonos vs Santorini {y}: Beaches or the Postcard?',
        'Μύκονος ή Σαντορίνη {y}: Παραλίες ή Καρτ Ποστάλ;'),
    ('chios', 'lesvos'): (
        'Chios vs Lesvos {y}: Mastic Villages or Sheer Scale?',
        'Χίος ή Λέσβος {y}: Μαστιχοχώρια ή Καθαρή Κλίμακα;'),
    ('folegandros', 'santorini'): (
        'Folegandros vs Santorini {y}: Same Cliffs, No Crowds',
        'Φολέγανδρος ή Σαντορίνη {y}: Ίδιοι Βράχοι, Χωρίς Κόσμο'),
    ('samothrace', 'thasos'): (
        'Samothrace vs Thasos {y}: Wild or Easy?',
        'Σαμοθράκη ή Θάσος {y}: Άγρια ή Εύκολη;'),
    ('naxos', 'santorini'): (
        'Naxos vs Santorini {y}: Better Beaches, Far Cheaper',
        'Νάξος ή Σαντορίνη {y}: Καλύτερες Παραλίες, Πολύ Φθηνότερα'),
    ('koufonisia', 'schoinoussa'): (
        'Koufonisia vs Schoinoussa {y}: A Perfect 5.0 for Beaches',
        'Κουφονήσια ή Σχοινούσα {y}: Άριστα 5.0 στις Παραλίες'),
    ('iraklia', 'schoinoussa'): (
        'Iraklia vs Schoinoussa {y}: The Quietest Two, Compared',
        'Ηρακλειά ή Σχοινούσα {y}: Οι Δύο Πιο Ήσυχες, Συγκριτικά'),
    ('iraklia', 'koufonisia'): (
        'Iraklia vs Koufonisia {y}: Same Ferry, Opposite Islands',
        'Ηρακλειά ή Κουφονήσια {y}: Ίδιο Πλοίο, Αντίθετα Νησιά'),
    ('donousa', 'koufonisia'): (
        'Donousa vs Koufonisia {y}: Isolation or Quality?',
        'Δονούσα ή Κουφονήσια {y}: Απομόνωση ή Ποιότητα;'),
    ('donousa', 'iraklia'): (
        'Donousa vs Iraklia {y}: The Two Hardest to Reach',
        'Δονούσα ή Ηρακλειά {y}: Οι Δύο Πιο Δύσκολες στην Πρόσβαση'),
    ('heraklion', 'rhodes'): (
        'Heraklion vs Rhodes {y}: Two Perfect 5.0s for History',
        'Ηράκλειο ή Ρόδος {y}: Δύο Άριστα 5.0 στην Ιστορία'),
    ('chania', 'rhodes'): (
        'Chania vs Rhodes {y}: Beaches or the Old Town?',
        'Χανιά ή Ρόδος {y}: Παραλίες ή Παλιά Πόλη;'),
    ('corfu', 'heraklion'): (
        'Corfu vs Heraklion {y}: Venetian Town or Knossos?',
        'Κέρκυρα ή Ηράκλειο {y}: Βενετσιάνικη Πόλη ή Κνωσός;'),
    ('heraklion', 'santorini'): (
        'Heraklion vs Santorini {y}: Knossos or the Caldera?',
        'Ηράκλειο ή Σαντορίνη {y}: Κνωσός ή Καλντέρα;'),
})
DESC_OVERRIDES.update({
    ('corfu', 'kefalonia'): (
        'Corfu takes it 4.2 to 4.1 on its UNESCO Old Town (culture 4.8 vs 3.2); Kefalonia has the better beaches (4.7 vs 3.9) and Myrtos. Scored side by side on price, access and nightlife.',
        'Η Κέρκυρα κερδίζει 4.2 έναντι 4.1 με την Παλιά Πόλη UNESCO (πολιτισμός 4.8 έναντι 3.2)· η Κεφαλονιά έχει καλύτερες παραλίες (4.7 έναντι 3.9) και τον Μύρτο. Αναλυτική σύγκριση.'),
    ('hydra', 'spetses'): (
        "Hydra wins 4.0 to 3.7 on atmosphere and the total absence of cars, but it's the most expensive island here at 1.8. Spetses has better beaches (2.8 vs 2.2) and suits a longer stay.",
        'Η Ύδρα κερδίζει 4.0 έναντι 3.7 στην ατμόσφαιρα και στην παντελή απουσία αυτοκινήτων, αλλά είναι το ακριβότερο νησί εδώ με 1.8. Οι Σπέτσες έχουν καλύτερες παραλίες και θέλουν χρόνο.'),
    ('aegina', 'hydra'): (
        'Hydra scores 4.0 to Aegina’s 3.3 but costs nearly twice as much (1.8 vs 3.5) and has worse beaches. Aegina is a working island of 13,000 with the Temple of Aphaia. Honest comparison.',
        'Η Ύδρα βαθμολογείται 4.0 έναντι 3.3 της Αίγινας αλλά κοστίζει σχεδόν διπλά (1.8 έναντι 3.5) και έχει χειρότερες παραλίες. Η Αίγινα είναι ζωντανό νησί 13.000 κατοίκων με τον Ναό της Αφαίας.'),
    ('ios', 'paros'): (
        'Both score a perfect 5.0 for nightlife. Paros wins overall 4.1 to 3.9 on beaches, ferries and variety; Ios is cheaper (3.5 vs 2.2) and more singular. When each one is the right call.',
        'Και τα δύο έχουν άριστα 5.0 στη νυχτερινή ζωή. Η Πάρος κερδίζει 4.1 έναντι 3.9 σε παραλίες, πλοία και ποικιλία· η Ίος είναι φθηνότερη (3.5 έναντι 2.2) και πιο μονοδιάστατη.'),
    ('paros', 'sifnos'): (
        'Paros wins 4.1 to 3.9 with perfect 5.0 scores for beaches and nightlife; Sifnos has the best food in the Cyclades, 100 km of marked paths, and costs less (3.5 vs 2.2).',
        'Η Πάρος κερδίζει 4.1 έναντι 3.9 με άριστα 5.0 σε παραλίες και νυχτερινή ζωή· η Σίφνος έχει το καλύτερο φαγητό των Κυκλάδων, 100 χλμ. μονοπάτια, και κοστίζει λιγότερο (3.5 έναντι 2.2).'),
    ('kea', 'kythnos'): (
        'Dead level at 3.5 each. Kea is closer to Athens (access 4.5 vs 3.5) with the ancient sites; Kythnos has better beaches (4.2 vs 3.8), hot springs and lower prices. The honest split.',
        'Ισοπαλία στο 3.5. Η Κέα είναι πιο κοντά στην Αθήνα (πρόσβαση 4.5 έναντι 3.5) με τους αρχαίους χώρους· η Κύθνος έχει καλύτερες παραλίες (4.2 έναντι 3.8), ιαματικές πηγές και χαμηλότερες τιμές.'),
    ('aegina', 'agistri'): (
        'Agistri edges it 3.4 to 3.3 on beaches (3.5 vs 2.5) and needs no car at all. Aegina has the Temple of Aphaia, Perdika’s fish tavernas and the easiest ferries in Greece.',
        'Το Αγκίστρι υπερτερεί 3.4 έναντι 3.3 στις παραλίες (3.5 έναντι 2.5) και δεν θέλει καθόλου αυτοκίνητο. Η Αίγινα έχει τον Ναό της Αφαίας, την Πέρδικα και τα ευκολότερα πλοία της Ελλάδας.'),
    ('mykonos', 'rhodes'): (
        'Rhodes edges it 4.4 to 4.3 and costs a fraction as much — affordability 3.5 against Mykonos’s 1.0, the lowest we score. Mykonos has 5.0 nightlife; Rhodes has a 5.0 for history.',
        'Η Ρόδος υπερτερεί 4.4 έναντι 4.3 και κοστίζει πολύ λιγότερο — προσιτότητα 3.5 έναντι 1.0 της Μυκόνου, η χαμηλότερη που δίνουμε. Η Μύκονος έχει 5.0 νυχτερινή ζωή· η Ρόδος 5.0 στην ιστορία.'),
    ('milos', 'santorini'): (
        'Santorini wins 4.8 to 4.7 on the caldera and a perfect 5.0 for culture; Milos has the only perfect 5.0 beach score on this site against Santorini’s 3.2. Going for beaches? Milos.',
        'Η Σαντορίνη κερδίζει 4.8 έναντι 4.7 με την καλντέρα και άριστα 5.0 στον πολιτισμό· η Μήλος έχει τη μόνη άριστη βαθμολογία 5.0 παραλιών εδώ έναντι 3.2. Για παραλίες; Μήλος.'),
    ('ios', 'mykonos'): (
        'Both score a perfect 5.0 for nightlife, but Ios rates 3.5 for affordability against Mykonos’s 1.0 — the lowest on this site. Ios also has better beaches (4.6 vs 4.3).',
        'Και τα δύο άριστα 5.0 στη νυχτερινή ζωή, αλλά η Ίος βαθμολογείται 3.5 στην προσιτότητα έναντι 1.0 της Μυκόνου — η χαμηλότερη εδώ. Η Ίος έχει και καλύτερες παραλίες (4.6 έναντι 4.3).'),
    ('chania', 'corfu'): (
        'Chania scores 4.8 — the highest on this site — to Corfu’s 4.2, on beaches 5.0 against 3.9. Corfu wins culture by a hair (4.8 vs 4.7). Two Venetian towns, one clear swimmer.',
        'Τα Χανιά βαθμολογούνται 4.8 — το υψηλότερο εδώ — έναντι 4.2 της Κέρκυρας, με παραλίες 5.0 έναντι 3.9. Η Κέρκυρα κερδίζει οριακά στον πολιτισμό (4.8 έναντι 4.7).'),
    ('paros', 'santorini'): (
        'Santorini wins 4.8 to 4.1 on the caldera and culture 5.0, but Paros has perfect 5.0 beaches against Santorini’s 3.2 and costs less. Three nights there or a week here.',
        'Η Σαντορίνη κερδίζει 4.8 έναντι 4.1 με την καλντέρα και πολιτισμό 5.0, αλλά η Πάρος έχει άριστα 5.0 παραλίες έναντι 3.2 και κοστίζει λιγότερο. Τρεις νύχτες εκεί ή μια εβδομάδα εδώ.'),
    ('rhodes', 'santorini'): (
        'Both hold a perfect 5.0 for culture. Santorini takes it 4.8 to 4.4 on the caldera; Rhodes has far better beaches (4.2 vs 3.2), costs much less (3.5 vs 1.0) and fills a week.',
        'Και τα δύο κρατούν άριστα 5.0 στον πολιτισμό. Η Σαντορίνη κερδίζει 4.8 έναντι 4.4 με την καλντέρα· η Ρόδος έχει πολύ καλύτερες παραλίες (4.2 έναντι 3.2) και κοστίζει πολύ λιγότερο.'),
    ('chania', 'santorini'): (
        'A genuine tie at 4.8 each, and they could not be less alike: Chania has perfect 5.0 beaches against Santorini’s 3.2; Santorini has 5.0 culture and the caldera. Scored side by side.',
        'Πραγματική ισοπαλία στο 4.8, και δεν θα μπορούσαν να διαφέρουν περισσότερο: τα Χανιά έχουν άριστα 5.0 παραλίες έναντι 3.2· η Σαντορίνη 5.0 πολιτισμό και την καλντέρα.'),
    ('amorgos', 'astypalaia'): (
        'Amorgos wins 4.0 to 3.8 on the Hozoviotissa monastery and its cliffs; Astypalaia has the better castle and culture (4.2 vs 3.8). Identical 4.0 beaches and 2.5 access.',
        'Η Αμοργός κερδίζει 4.0 έναντι 3.8 με τη Χοζοβιώτισσα και τα βράχια της· η Αστυπάλαια έχει καλύτερο κάστρο και πολιτισμό (4.2 έναντι 3.8). Ίδιες παραλίες 4.0 και πρόσβαση 2.5.'),
    ('donousa', 'schoinoussa'): (
        'These two score identically — 3.4 each, 4.5 beaches each — so this is not a rivalry. What actually differs is isolation, ferries and what there is to do after swimming.',
        'Αυτά τα δύο βαθμολογούνται ίδια — 3.4 έκαστο, 4.5 στις παραλίες — οπότε δεν είναι αντιπαλότητα. Διαφέρουν στην απομόνωση, στα πλοία και στο τι κάνεις μετά το μπάνιο.'),
    ('mykonos', 'santorini'): (
        'Santorini wins 4.8 to 4.3 on culture 5.0 and the caldera; Mykonos has much better beaches (4.3 vs 3.2) and 5.0 nightlife. Both score 1.0 for affordability — the lowest we give.',
        'Η Σαντορίνη κερδίζει 4.8 έναντι 4.3 με πολιτισμό 5.0 και την καλντέρα· η Μύκονος έχει πολύ καλύτερες παραλίες (4.3 έναντι 3.2) και 5.0 νυχτερινή ζωή. Και τα δύο 1.0 στην προσιτότητα.'),
    ('chios', 'lesvos'): (
        'Both score 4.7 for culture. Lesvos wins overall 4.0 to 3.6 on sheer scale, beaches and the petrified forest; Chios has the mastic villages and Nea Moni, and is slightly cheaper.',
        'Και τα δύο 4.7 στον πολιτισμό. Η Λέσβος κερδίζει 4.0 έναντι 3.6 στην κλίμακα, τις παραλίες και το απολιθωμένο δάσος· η Χίος έχει τα Μαστιχοχώρια και τη Νέα Μονή, και είναι λίγο φθηνότερη.'),
    ('folegandros', 'santorini'): (
        'Santorini wins 4.8 to 4.0 on the caldera and culture 5.0. Folegandros has a cliff-edge chora nearly as dramatic, 765 residents and no crowds — but the same 2.2-vs-1.0 price bracket.',
        'Η Σαντορίνη κερδίζει 4.8 έναντι 4.0 με την καλντέρα και πολιτισμό 5.0. Η Φολέγανδρος έχει χώρα σε βράχο σχεδόν εξίσου εντυπωσιακή, 765 κατοίκους και μηδέν κόσμο.'),
    ('samothrace', 'thasos'): (
        'Thasos wins 3.7 to 3.2 on beaches (4.2 vs 3.0) and access — Samothrace scores 1.8, the hardest to reach here. Samothrace has Mt Saos, the waterfalls and the Sanctuary of the Gods.',
        'Η Θάσος κερδίζει 3.7 έναντι 3.2 στις παραλίες (4.2 έναντι 3.0) και στην πρόσβαση — η Σαμοθράκη βαθμολογείται 1.8, η δυσκολότερη εδώ. Η Σαμοθράκη έχει τον Σάο, τις βάθρες και το Ιερό.'),
    ('naxos', 'santorini'): (
        'Santorini wins 4.8 to 4.5, but Naxos has far better beaches (4.8 vs 3.2) and rates 4.0 for affordability against Santorini’s 1.0. A real island against a three-night view.',
        'Η Σαντορίνη κερδίζει 4.8 έναντι 4.5, αλλά η Νάξος έχει πολύ καλύτερες παραλίες (4.8 έναντι 3.2) και βαθμολογείται 4.0 στην προσιτότητα έναντι 1.0. Πραγματικό νησί έναντι τριήμερης θέας.'),
    ('koufonisia', 'schoinoussa'): (
        'Koufonisia wins 4.0 to 3.4 with a perfect 5.0 for beaches — Pori, Italida and the Pisina rock pool. Schoinoussa is quieter and cheaper. Both are Small Cyclades, one ferry apart.',
        'Τα Κουφονήσια κερδίζουν 4.0 έναντι 3.4 με άριστα 5.0 στις παραλίες — Πορί, Ιταλίδα και η Πισίνα. Η Σχοινούσα είναι ησυχότερη και φθηνότερη. Και τα δύο Μικρές Κυκλάδες, ένα πλοίο μακριά.'),
    ('iraklia', 'schoinoussa'): (
        'Schoinoussa edges it 3.4 to 3.2 on beaches and ferries; Iraklia is the cheaper and emptier of the two, with the lowest nightlife score in the archipelago at 1.5.',
        'Η Σχοινούσα υπερτερεί 3.4 έναντι 3.2 στις παραλίες και στα πλοία· η Ηρακλειά είναι η φθηνότερη και πιο άδεια, με τη χαμηλότερη νυχτερινή ζωή του αρχιπελάγους στο 1.5.'),
    ('iraklia', 'koufonisia'): (
        'Two ends of the same ferry line and nothing alike: Koufonisia scores 4.0 with perfect 5.0 beaches and 4.0 nightlife; Iraklia scores 3.2 with 1.5 nightlife and near-total quiet.',
        'Δύο άκρα της ίδιας γραμμής και τίποτα κοινό: τα Κουφονήσια βαθμολογούνται 4.0 με άριστα 5.0 παραλίες και 4.0 νυχτερινή ζωή· η Ηρακλειά 3.2 με 1.5 και σχεδόν απόλυτη ησυχία.'),
    ('donousa', 'koufonisia'): (
        'Koufonisia wins 4.0 to 3.4 on quality — a perfect 5.0 for beaches against 4.5 — while Donousa wins on isolation, with access 2.2 and almost no one there. Scored side by side.',
        'Τα Κουφονήσια κερδίζουν 4.0 έναντι 3.4 στην ποιότητα — άριστα 5.0 στις παραλίες έναντι 4.5 — ενώ η Δονούσα κερδίζει στην απομόνωση, με πρόσβαση 2.2 και σχεδόν κανέναν εκεί.'),
    ('donousa', 'iraklia'): (
        'The two hardest Small Cyclades to reach — access 2.2 and 2.0, the lowest in the archipelago. Donousa edges it 3.4 to 3.2 on beaches; Iraklia is cheaper and quieter still.',
        'Οι δύο δυσκολότερες Μικρές Κυκλάδες — πρόσβαση 2.2 και 2.0, οι χαμηλότερες του αρχιπελάγους. Η Δονούσα υπερτερεί 3.4 έναντι 3.2 στις παραλίες· η Ηρακλειά είναι φθηνότερη και ησυχότερη.'),
    ('heraklion', 'rhodes'): (
        'Both hold a perfect 5.0 for culture — Knossos and the museum against the medieval Old Town. Rhodes wins overall 4.4 to 4.2 on much better beaches (4.2 vs 3.5).',
        'Και τα δύο κρατούν άριστα 5.0 στον πολιτισμό — η Κνωσός και το μουσείο έναντι της μεσαιωνικής Παλιάς Πόλης. Η Ρόδος κερδίζει 4.4 έναντι 4.2 με πολύ καλύτερες παραλίες (4.2 έναντι 3.5).'),
    ('chania', 'rhodes'): (
        'Chania scores 4.8 — the highest here — to Rhodes’s 4.4, on perfect 5.0 beaches against 4.2. Rhodes answers with a 5.0 for culture and the best medieval town in Greece.',
        'Τα Χανιά βαθμολογούνται 4.8 — το υψηλότερο εδώ — έναντι 4.4 της Ρόδου, με άριστα 5.0 παραλίες έναντι 4.2. Η Ρόδος απαντά με 5.0 στον πολιτισμό και την καλύτερη μεσαιωνική πόλη της Ελλάδας.'),
    ('corfu', 'heraklion'): (
        'A dead tie at 4.2 each. Heraklion holds the only perfect 5.0 culture score on this site, for Knossos and the museum; Corfu has the better Old Town to stay in, plus beaches and food.',
        'Ισοπαλία στο 4.2. Το Ηράκλειο κρατά τη μόνη άριστη βαθμολογία 5.0 πολιτισμού εδώ, για την Κνωσό και το μουσείο· η Κέρκυρα έχει καλύτερη Παλιά Πόλη για διαμονή, παραλίες και φαγητό.'),
    ('heraklion', 'santorini'): (
        'Both hold a perfect 5.0 for culture — Knossos against the caldera. Santorini wins overall 4.8 to 4.2; Heraklion costs far less (3.5 vs 1.0) and has the better museum.',
        'Και τα δύο άριστα 5.0 στον πολιτισμό — η Κνωσός έναντι της καλντέρας. Η Σαντορίνη κερδίζει 4.8 έναντι 4.2· το Ηράκλειο κοστίζει πολύ λιγότερο (3.5 έναντι 1.0) και έχει καλύτερο μουσείο.'),
})

# --- Crete regional bases + the last uncovered Saronic pair -----------------
# "where do I base myself in Crete" is the real planning question for the
# largest Greek island; the generic template would have said "Which Greek
# Island Should You Visit?" about four regions of the same one.
TITLE_OVERRIDES.update({
    ('heraklion', 'rethymno'): (
        'Heraklion vs Rethymno {y}: Land in One, Sleep in the Other',
        'Ηράκλειο ή Ρέθυμνο {y}: Προσγειώνεσαι στο Ένα, Μένεις στο Άλλο'),
    ('chania', 'lasithi'): (
        'Chania vs Lasithi {y}: Opposite Ends of Crete',
        'Χανιά ή Λασίθι {y}: Τα Δύο Άκρα της Κρήτης'),
    ('heraklion', 'lasithi'): (
        'Heraklion vs Lasithi {y}: Knossos or the Better Coast?',
        'Ηράκλειο ή Λασίθι {y}: Κνωσός ή Καλύτερη Ακτή;'),
    ('lasithi', 'rethymno'): (
        'Lasithi vs Rethymno {y}: Palm Beaches or a Venetian Town?',
        'Λασίθι ή Ρέθυμνο {y}: Φοινικόδασος ή Βενετσιάνικη Πόλη;'),
    ('agistri', 'hydra'): (
        'Agistri vs Hydra {y}: Both Car-Free, Nothing Else Alike',
        'Αγκίστρι ή Ύδρα {y}: Και τα Δύο Χωρίς Αυτοκίνητα'),
})
DESC_OVERRIDES.update({
    ('heraklion', 'rethymno'): (
        'Heraklion wins 4.2 to 3.8 on the only perfect 5.0 culture score and the airport; Rethymno '
        'has the better-preserved old town, better beaches and lower prices. Land in one, stay in the other.',
        'Το Ηράκλειο κερδίζει 4.2 έναντι 3.8 με τη μόνη άριστη βαθμολογία 5.0 πολιτισμού και το '
        'αεροδρόμιο· το Ρέθυμνο έχει καλύτερα διατηρημένη παλιά πόλη, καλύτερες παραλίες, φθηνότερα.'),
    ('chania', 'lasithi'): (
        'Chania scores 4.8 — the highest here — to Lasithi’s 4.0, on beaches 5.0 vs 4.0. But they are '
        'four hours apart: this is two different holidays, not two bases for one trip.',
        'Τα Χανιά βαθμολογούνται 4.8 — το υψηλότερο εδώ — έναντι 4.0 του Λασιθίου, με παραλίες 5.0 '
        'έναντι 4.0. Απέχουν όμως τέσσερις ώρες: δύο διαφορετικές διακοπές, όχι δύο βάσεις.'),
    ('heraklion', 'lasithi'): (
        'Heraklion edges it 4.2 to 4.0 on Knossos and a 5.0 for access; Lasithi has better beaches '
        '(4.0 vs 3.5), Vai and Spinalonga. An hour apart — the easiest Crete pair to combine.',
        'Το Ηράκλειο υπερτερεί 4.2 έναντι 4.0 με την Κνωσό και 5.0 στην πρόσβαση· το Λασίθι έχει '
        'καλύτερες παραλίες (4.0 έναντι 3.5), το Βάι και τη Σπιναλόγκα. Μία ώρα μακριά.'),
    ('lasithi', 'rethymno'): (
        'Lasithi edges it 4.0 to 3.8 on beaches and its own airport; Rethymno has the best-preserved '
        'old town in Crete (culture 4.5 vs 3.5) and costs less. The quieter two Crete bases, compared.',
        'Το Λασίθι υπερτερεί 4.0 έναντι 3.8 σε παραλίες και δικό του αεροδρόμιο· το Ρέθυμνο έχει την '
        'καλύτερα διατηρημένη παλιά πόλη της Κρήτης (πολιτισμός 4.5 έναντι 3.5) και κοστίζει λιγότερο.'),
    ('agistri', 'hydra'): (
        'Both score 1.0 for car reliance, and diverge from there. Hydra wins 4.0 to 3.4 on the harbour '
        'and culture; Agistri has far better beaches (3.5 vs 2.2) at less than half the price.',
        'Και τα δύο 1.0 στην ανάγκη οχήματος, και μετά αποκλίνουν. Η Ύδρα κερδίζει 4.0 έναντι 3.4 με '
        'το λιμάνι και τον πολιτισμό· το Αγκίστρι έχει πολύ καλύτερες παραλίες με το μισό κόστος.'),
})

# --- "or" phrasing test, Aug 2026 -------------------------------------------
# GSC evidence, restricted to position 4-10 so position isn't doing the work:
#     queries containing " vs "  -> 3,535 impressions, 2.46% CTR
#     queries containing " or "  -> 2,983 impressions, 3.22% CTR
# The Greek titles have always used "ή" (or) and Greek compare pages run 5.52%
# CTR against 1.84% for English. Confounded by competition, but it points the
# same way. Applied to the seven worst-converting English compare pages only,
# so the rest of the corpus stays as a control and the next GSC export can
# actually settle it. URLs and H1s keep "vs" — the pages still rank for both.
TITLE_OVERRIDES.update({
    ('chania', 'rethymno'): (          # 3,282 impr, 0.34% CTR, pos 5.8
        'Chania or Rethymno {y}? Chania Wins on Beaches — Honest Pick',
        'Χανιά ή Ρέθυμνο {y}: Τα Χανιά Κερδίζουν στις Παραλίες'),
    ('corfu', 'kefalonia'): (          # 4,024 impr, 1.29% CTR, pos 4.7
        'Corfu or Kefalonia {y}? Culture vs Coastline, Scored',
        'Κέρκυρα ή Κεφαλονιά {y}: Πολιτισμός ή Ακτογραμμή;'),
    ('corfu', 'rhodes'): (             # 4,188 impr, 1.43% CTR, pos 5.8
        'Corfu or Rhodes {y}? Two Old Towns, One Clear Winner',
        'Κέρκυρα ή Ρόδος {y}: Δύο Παλιές Πόλεις, Ένας Νικητής'),
    ('kos', 'rhodes'): (               # 2,613 impr, 1.22% CTR, pos 5.7
        'Kos or Rhodes {y}? Rhodes for History, Kos for Easy',
        'Κως ή Ρόδος {y}: Ρόδος για Ιστορία, Κως για Ευκολία'),
    ('kefalonia', 'zakynthos'): (      # 1,927 impr, 0.62% CTR, pos 7.1
        'Kefalonia or Zakynthos {y}? Quiet Coves vs Party Coast',
        'Κεφαλονιά ή Ζάκυνθος {y}: Ήσυχοι Όρμοι ή Πάρτι;'),
    ('corfu', 'lefkada'): (            # 1,367 impr, 1.32% CTR, pos 4.3
        'Corfu or Lefkada {y}? Old Town vs the Beach Wall',
        'Κέρκυρα ή Λευκάδα {y}: Παλιά Πόλη ή Τείχος Παραλιών;'),
    ('mykonos', 'paros'): (            #   938 impr, 0.85% CTR, pos 7.0
        'Mykonos or Paros {y}? Same Nightlife, Half the Price',
        'Μύκονος ή Πάρος {y}: Ίδια Νυχτερινή Ζωή, Μισή Τιμή'),
})

def fit_description(text, limit=158, floor=115):
    """Keep a meta description inside Google's snippet budget.

    Aug 2026: 145 of 164 compare descriptions ran 161-191 chars, so the last
    clause was being cut off mid-word in the SERP. These are hand-written, so
    rather than chop them blindly we drop whole trailing sentences — the last
    sentence is usually the generic "Scored side by side on..." tail — and only
    fall back to a clause cut if dropping sentences would gut the description
    below `floor`. Anything already inside the budget is returned untouched.
    """
    text = re.sub(r'\s+', ' ', (text or '')).strip()
    if len(text) <= limit:
        return text
    parts = re.split(r'(?<=[.!?;])\s+', text)
    while len(parts) > 1 and len(' '.join(parts)) > limit:
        candidate = ' '.join(parts[:-1])
        if len(candidate) < floor:
            break
        parts = parts[:-1]
    joined = ' '.join(parts)
    if len(joined) <= limit:
        return joined
    # Single overlong sentence: cut at the last clause boundary that still
    # leaves something substantial, and close it cleanly.
    window = joined[:limit - 1]
    for sep in ('—', ';', ',', ' '):
        idx = window.rfind(sep)
        if idx >= floor:
            return window[:idx].rstrip(' ,;—-·') + '.'
    return window.rstrip(' ,;—-·') + '.'


VERDICTS = json.loads((ROOT / 'vs_verdicts.json').read_text(encoding='utf-8'))
FAQS_PATH = ROOT / 'vs_faqs.json'
FAQS = json.loads(FAQS_PATH.read_text(encoding='utf-8')) if FAQS_PATH.exists() else {}

def load_island_meta():
    js = (ROOT / 'script.js').read_text(encoding='utf-8')
    meta = {}
    for m in re.finditer(
        r'^\s*"([a-z-]+)"\s*:\s*\{\s*name\s*:\s*"([^"]+)"[^}]*island_group\s*:\s*"([^"]+)"',
        js, re.MULTILINE
    ):
        meta[m.group(1)] = {'name': m.group(2), 'group': m.group(3)}
    return meta

def load_island_names_el():
    js = (ROOT / 'i18n.js').read_text(encoding='utf-8')
    m = re.search(r'const\s+ISLAND_NAMES_EL\s*=\s*\{(.*?)\};', js, re.DOTALL)
    if not m:
        return {}
    out = {}
    for ml in re.finditer(r"'([a-z-]+)'\s*:\s*'([^']+)'", m.group(1)):
        out[ml.group(1)] = ml.group(2)
    return out

META = load_island_meta()
NAMES_EL = load_island_names_el()

def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;')
                  .replace('>', '&gt;').replace('"', '&quot;'))

def parse_pair_key(pk):
    return tuple(pk.split('__', 1))

def slug_for_pair(a, b):
    a, b = sorted([a, b])
    return f'{a}-vs-{b}'

def render_faq_jsonld(faqs):
    if not faqs:
        return ''
    schema = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {'@type': 'Question', 'name': item['q'],
             'acceptedAnswer': {'@type': 'Answer', 'text': item['a']}}
            for item in faqs
        ]
    }
    return ('<script type="application/ld+json">'
            + json.dumps(schema, ensure_ascii=False, separators=(',', ':'))
            + '</script>')

# ---------------------------------------------------------------------------
# Related-comparisons widget + hub page helpers (added R2)
# ---------------------------------------------------------------------------

# Manually curated "featured" pairs for the hub page hero — the highest-demand
# comparison queries. Order matters (most-searched first).
FEATURED_PAIR_KEYS = [
    'rhodes__santorini',
    'naxos__santorini',
    'paros__santorini',
    'mykonos__santorini',
    'chania__santorini',
    'mykonos__rhodes',
    'ios__mykonos',
    'corfu__rhodes',
]

def _is_longform(pair_key):
    """A pair is 'long-form' if its EN verdict exceeds 3000 chars."""
    return len((VERDICTS.get(pair_key, {}).get('en') or '')) > 3000

def build_island_to_pairs_index():
    """Returns {island_slug: [pair_key, ...]} for all known pairs."""
    idx = {}
    for pk in VERDICTS.keys():
        try:
            a, b = parse_pair_key(pk)
        except Exception:
            continue
        idx.setdefault(a, []).append(pk)
        idx.setdefault(b, []).append(pk)
    return idx

PAIRS_BY_ISLAND = build_island_to_pairs_index()

def select_related_pairs(pair_key, k=4):
    """For a given pair, return up to k other pair_keys to recommend.

    Strategy: 2 pairs containing island A + 2 containing island B,
    preferring long-form pairs. Dedupe and exclude the current pair.
    """
    try:
        a, b = parse_pair_key(pair_key)
    except Exception:
        return []

    def candidates_for(island):
        return sorted(
            (p for p in PAIRS_BY_ISLAND.get(island, []) if p != pair_key),
            key=lambda p: (not _is_longform(p), p),  # long-form first, then alpha
        )

    a_cands = candidates_for(a)
    b_cands = candidates_for(b)

    out = []
    for i in range(max(len(a_cands), len(b_cands))):
        if i < len(a_cands) and a_cands[i] not in out and len(out) < k:
            out.append(a_cands[i])
        if i < len(b_cands) and b_cands[i] not in out and len(out) < k:
            out.append(b_cands[i])
        if len(out) >= k:
            break
    return out

def render_related_widget(pair_key, lang):
    """Renders a 'Related comparisons' card grid at the bottom of a compare page."""
    related = select_related_pairs(pair_key, k=4)
    if not related:
        return ''
    heading = 'Related comparisons' if lang == 'en' else 'Σχετικές συγκρίσεις'

    cards = []
    for pk in related:
        a, b = parse_pair_key(pk)
        slug = slug_for_pair(a, b)
        if lang == 'el':
            name_a = NAMES_EL.get(a, META[a]['name'])
            name_b = NAMES_EL.get(b, META[b]['name'])
            href = f'/el/compare/{slug}/'
            sep = 'ή'
        else:
            name_a = META[a]['name']
            name_b = META[b]['name']
            href = f'/compare/{slug}/'
            sep = 'vs'
        cards.append(
            f'<a class="compare-related-card" href="{esc(href)}">'
            f'<span class="compare-related-pair">{esc(name_a)} <em>{sep}</em> {esc(name_b)}</span>'
            f'<span class="compare-related-arrow" aria-hidden="true">→</span>'
            f'</a>'
        )
    return (
        f'<div class="compare-related">'
        f'<h3 class="compare-related-heading">{heading}</h3>'
        f'<div class="compare-related-grid">{"".join(cards)}</div>'
        f'</div>'
    )

def render_faq_html(faqs, lang):
    if not faqs:
        return ''
    items = []
    for item in faqs:
        items.append(
            f'<details><summary>{esc(item["q"])}</summary>'
            f'<p>{esc(item["a"])}</p></details>'
        )
    heading = 'Common questions' if lang == 'en' else 'Συχνές ερωτήσεις'
    return (f'<div class="compare-faq">'
            f'<h3 class="compare-faq-heading">{heading}</h3>'
            f'{"".join(items)}</div>')

# --- "or" vs "vs" title experiment ------------------------------------------
# Randomised 50/50 across all English compare pages, assigned by a salted hash
# of the pair key so the split is deterministic and survives rebuilds.
#
# Why randomised rather than "convert everything": the GSC evidence that
# prompted this (queries containing " or " earn 3.22% CTR at positions 4-10
# against 2.46% for " vs ") was collected while EVERY English title said "vs".
# It shows that people who phrase a search with "or" click more — it does NOT
# show that an "or" title causes clicks. Only a controlled split can. And
# because Greek-island search collapses between August and October, a plain
# before/after would be swamped by seasonality; matched groups over the same
# window are the only way to read the result.
#
# Greek titles are excluded — they have always used "ή" and have no control.
OR_TEST_SALT = 'or-vs-title-test-2026-08'
_OR_GROUP = None


def _or_group_set():
    """Exactly half the pairs, chosen by hash rank.

    A plain `hash % 2` gave a 31/51 split on 82 pairs — legal for a coin flip
    but a needlessly unbalanced experiment. Ranking every pair by its salted
    hash and taking the lower half guarantees 41/41 while staying entirely
    deterministic.
    """
    global _OR_GROUP
    if _OR_GROUP is None:
        keys = sorted({'__'.join(sorted(parse_pair_key(pk))) for pk in VERDICTS})
        ranked = sorted(keys, key=lambda k: hashlib.md5(
            (OR_TEST_SALT + k).encode('utf-8')).hexdigest())
        _OR_GROUP = set(ranked[:len(ranked) // 2])
    return _OR_GROUP


def in_or_group(a, b):
    return '__'.join(sorted([a, b])) in _or_group_set()


def phrase_pair(title, name_a, name_b, use_or):
    """Swap the leading 'A vs B' / 'A or B' connector only.

    Deliberately anchored to the start of the string: several hooks contain a
    second 'vs' ("Culture vs Coastline, Scored") that must survive untouched.
    """
    want = ' or ' if use_or else ' vs '
    other = ' vs ' if use_or else ' or '

    # Split off the hook at the first ':' or '?'. Hand-written titles routinely
    # carry a second connector in the hook ("Kea vs Kythnos 2026: Closer to
    # Athens or Better Beaches?") and that one must not move.
    m = re.search(r'[:?]', title)
    head, tail = (title[:m.start()], title[m.start():]) if m else (title, '')

    if other in head:
        head = head.replace(other, want, 1)
    elif want not in head:
        # Neither connector in the head — nothing safe to rewrite. Happens if a
        # future override phrases the pair some other way.
        return title

    # "X or Y 2026? hook" reads as a question; "X vs Y 2026: hook" does not.
    if tail:
        tail = ('?' + tail[1:]) if use_or else (':' + tail[1:])
    return head + tail


def render_page(pair_key, lang):
    a, b = parse_pair_key(pair_key)
    if a not in META or b not in META:
        raise ValueError(f"Unknown island in pair {pair_key}: {a} / {b}")

    slug = slug_for_pair(a, b)

    if lang == 'el':
        name_a = NAMES_EL.get(a, META[a]['name'])
        name_b = NAMES_EL.get(b, META[b]['name'])
    else:
        name_a = META[a]['name']
        name_b = META[b]['name']

    verdict_entry = VERDICTS.get(pair_key, {})
    verdict_html = verdict_entry.get('el' if lang == 'el' else 'en', '') or ''
    faq_entry = FAQS.get(pair_key, {})
    faqs = faq_entry.get('el' if lang == 'el' else 'en', []) or []

    if lang == 'en':
        _ov = TITLE_OVERRIDES.get((a, b)) or TITLE_OVERRIDES.get((b, a))
        if _ov:
            # CTR pass Aug 2026: the ' | Aegean Blueprint' suffix cost 19
            # characters on every compare title, pushing the average to 71.6
            # and truncating the hook that earns the click. Google already
            # renders the domain beside the title, so the brand was buying
            # nothing and costing the payload.
            page_title = _ov[0].format(y=YEAR)
        else:
            page_title = f'{name_a} vs {name_b}: An Honest, Scored Comparison'
        # Randomised arm assignment — applies to bespoke and templated titles
        # alike, so the split isn't confounded with which pages I hand-wrote.
        page_title = phrase_pair(page_title, name_a, name_b, in_or_group(a, b))
        _od = DESC_OVERRIDES.get((a, b)) or DESC_OVERRIDES.get((b, a))
        if _od:
            page_desc = _od[0]
        else:
            page_desc = (f'{name_a} vs {name_b} — side-by-side comparison of beaches, '
                         f'culture, nightlife, access, and price. Practical recommendations '
                         f'for choosing the right island for your trip.')
        page_desc = fit_description(page_desc)
        h1_text = f'{name_a} vs {name_b}'
        subtitle = 'Side-by-side comparison — beaches, culture, atmosphere, and the practical question of which one suits your trip.'
        verdict_heading = 'Our verdict'
        og_locale = 'en_US'
    else:
        _ov = TITLE_OVERRIDES.get((a, b)) or TITLE_OVERRIDES.get((b, a))
        if _ov:
            page_title = _ov[1].format(y=YEAR)
        else:
            page_title = f'{name_a} ή {name_b}; Ειλικρινής σύγκριση με βαθμολογίες'
        _od = DESC_OVERRIDES.get((a, b)) or DESC_OVERRIDES.get((b, a))
        if _od:
            page_desc = _od[1]
        else:
            page_desc = (f'{name_a} ή {name_b} — αναλυτική σύγκριση παραλιών, πολιτισμού, '
                         f'νυχτερινής ζωής, πρόσβασης και τιμών. Πρακτικές συμβουλές για '
                         f'να επιλέξεις το σωστό νησί για το ταξίδι σου.')
        page_desc = fit_description(page_desc)
        h1_text = f'{name_a} ή {name_b}'
        subtitle = 'Λεπτομερής σύγκριση — παραλίες, πολιτισμός, ατμόσφαιρα, και η πρακτική επιλογή του νησιού που ταιριάζει στο ταξίδι σου.'
        verdict_heading = 'Η ετυμηγορία μας'
        og_locale = 'el_GR'

    en_url = f'{SITE_URL}/compare/{slug}/'
    el_url = f'{SITE_URL}/el/compare/{slug}/'
    canonical = el_url if lang == 'el' else en_url

    faq_jsonld = render_faq_jsonld(faqs)

    if verdict_html or faqs:
        prerendered_verdict = (
            f'<h3 class="compare-verdict-heading">{esc(verdict_heading)}</h3>'
            f'{verdict_html}'
            f'{render_faq_html(faqs, lang)}'
            f'{render_related_widget(pair_key, lang)}'
        )
        verdict_display = ''
    else:
        prerendered_verdict = ''
        verdict_display = 'display:none;'

    init_pair = json.dumps([a, b])

    if lang == 'el':
        nav_items = [
            ('/el/#compare', 'Σύγκριση', 'nav-compare'),
            ('/el/#match', 'Ταίριαξέ με', 'nav-match'),
            ('/el/trip-cost/', 'Μπάτζετ', 'nav-tripcost'),
            ('/el/#hopping', 'Πλοία & Νησοπορία', 'nav-hopping'),
            ('/el/festivals/', 'Γιορτές', 'nav-festivals'),
            ('/el/#data', 'Στοιχεία Νησιών', 'nav-data'),
            ('/el/#mission', 'Στόχος', 'nav-mission'),
            ('/el/#shortlist', '⭐ Λίστα μου', 'nav-shortlist'),
        ]
        home_url = '/el/'
        privacy_link = '<a href="/el/privacy/" data-i18n="footer.privacy">Απόρρητο</a>'
    else:
        nav_items = [
            ('/#compare', 'Compare', 'nav-compare'),
            ('/#match', 'Match Me', 'nav-match'),
            ('/trip-cost/', 'Budget', 'nav-tripcost'),
            ('/#hopping', 'Ferries & Hopping', 'nav-hopping'),
            ('/festivals/', 'Festivals', 'nav-festivals'),
            ('/#data', 'Islands Data', 'nav-data'),
            ('/#mission', 'Mission', 'nav-mission'),
            ('/#shortlist', '⭐ My Shortlist', 'nav-shortlist'),
        ]
        home_url = '/'
        privacy_link = '<a href="/privacy/" data-i18n="footer.privacy">Privacy</a>'

    nav_html = '\n        '.join(
        f'<a href="{esc(href)}" id="{nav_id}">{esc(label)}</a>'
        for href, label, nav_id in nav_items
    )

    page_css = '''
  #view-compare > h2[data-i18n="compare.title"],
  #view-compare > p.compare-intro {
    display: none;
  }
  .vs-page-h1 {
    font-family: var(--display, Georgia, serif);
    font-size: 32px;
    margin: 0 0 6px;
    color: var(--ink-1, #222);
  }
  .vs-page-sub {
    font-size: 16px;
    color: var(--ink-2, #555);
    margin: 0 0 24px;
    line-height: 1.5;
  }
  @media (max-width: 600px) {
    .vs-page-h1 { font-size: 26px; }
    .vs-page-sub { font-size: 15px; }
  }
  /* Related comparisons widget */
  .compare-related {
    margin-top: 32px;
    padding-top: 24px;
    border-top: 1px solid var(--marble-3, #e0e0e0);
  }
  .compare-related-heading {
    font-family: var(--display, Georgia, serif);
    font-size: var(--text-h3, 20px);
    margin: 0 0 16px;
    color: var(--ink-1, #222);
  }
  .compare-related-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
  .compare-related-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 16px;
    background: var(--marble, #fafafa);
    border: 1px solid var(--marble-3, #e0e0e0);
    border-radius: 8px;
    text-decoration: none;
    color: var(--ink-1, #222);
    transition: background 0.15s, border-color 0.15s;
  }
  .compare-related-card:hover {
    background: var(--marble-2, #f0f0f0);
    border-color: var(--ink-3, #999);
  }
  .compare-related-pair {
    font-size: var(--text-body, 15px);
    line-height: 1.3;
  }
  .compare-related-pair em {
    font-style: normal;
    color: var(--ink-2, #555);
    font-size: var(--text-small, 13px);
    margin: 0 4px;
  }
  .compare-related-arrow {
    color: var(--ink-2, #555);
    margin-left: 12px;
    flex-shrink: 0;
  }
  @media (max-width: 600px) {
    .compare-related-grid { grid-template-columns: 1fr; }
  }
'''

    og_image = f'{SITE_URL}/og-image.png'

    html = f'''<!DOCTYPE html>
<html lang="{'el' if lang == 'el' else 'en'}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script>window.localStorage&&document.documentElement.classList.toggle("dark",localStorage.getItem("darkMode")===null?window.matchMedia("(prefers-color-scheme: dark)").matches:localStorage.getItem("darkMode")==="true")</script>
<title>{esc(page_title)}</title>
<meta name="description" content="{esc(page_desc)}">
<meta name="theme-color" content="#0B8FAC">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="el" href="{el_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(page_title)}">
<meta property="og:description" content="{esc(page_desc)}">
<meta property="og:image" content="{og_image}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{og_locale}">
<meta property="og:site_name" content="Aegean Blueprint">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(page_title)}">
<meta name="twitter:description" content="{esc(page_desc)}">
<meta name="twitter:image" content="{og_image}">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-FMFWLRM2J9"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-FMFWLRM2J9');</script>
<script>if(localStorage.getItem("darkMode")==="true"){{document.documentElement.classList.add("dark");}}</script>
<link rel="stylesheet" href="/style.css?v={STYLE_V}">
<style>{page_css}</style>
{faq_jsonld}
<script async data-cfasync="false" data-noptimize="1" data-no-defer="1" src="https://emrldtp.com/NTUxOTU3.js?t=551957"></script>
</head>
<body>

<div id="loading-overlay" style="display:none;">
  <div class="loading-inner">
    <img src="/logo.svg" alt="Aegean Blueprint logo" id="loading-logo">
    <div class="loading-spinner"></div>
    <p>Loading…</p>
  </div>
</div>

<header>
  <div class="header-content">
    <a href="{home_url}" class="logo-wrapper">
      <img src="/logo-hero.svg" id="site-logo" alt="Aegean Blueprint logo">
      <span id="brand-text"><span class="brand-word">Aegean</span> <span class="brand-word">Blueprint</span></span>
    </a>
    <div class="menu-toggle" id="menu-toggle-btn"><span></span><span></span><span></span></div>
    <nav class="top-nav" id="main-nav">
        {nav_html}
    </nav>
    <div class="lang-dropdown" id="lang-dropdown">
      <button class="lang-toggle" id="lang-toggle-btn" aria-label="Switch language" aria-haspopup="true" aria-expanded="false">
        <span class="lang-globe">🌐</span>
        <span class="lang-current" id="lang-current">{'EL' if lang == 'el' else 'EN'}</span>
        <span class="lang-caret">▾</span>
      </button>
      <div class="lang-menu" id="lang-menu" role="menu">
        <a href="#" class="lang-option" data-lang="en" role="menuitem"><span class="lang-option-flag">🇬🇧</span> English</a>
        <a href="#" class="lang-option" data-lang="el" role="menuitem"><span class="lang-option-flag">🇬🇷</span> Ελληνικά</a>
      </div>
    </div>
    <button class="dark-mode-toggle" id="dark-mode-btn" aria-label="Toggle dark mode">☾</button>
  </div>
</header>

<main id="view-compare" class="view-section content-page">
  <h1 class="vs-page-h1">{esc(h1_text)}</h1>
  <p class="vs-page-sub">{esc(subtitle)}</p>
  <h2 data-i18n="compare.title">Compare Islands</h2>
  <p class="compare-intro" data-i18n="compare.intro">Select two islands to compare side-by-side.</p>
  <div class="compare-selectors">
    <select id="compare-select-a"><option value="" data-i18n="compare.optionA">— Island A —</option></select>
    <span class="vs-label" data-i18n="compare.vs">vs</span>
    <select id="compare-select-b"><option value="" data-i18n="compare.optionB">— Island B —</option></select>
  </div>
  <div id="compare-container">
    <div id="compare-placeholder" class="compare-placeholder" style="display:none;" data-i18n="compare.placeholder">Select two islands above to start comparing.</div>
    <div id="compare-content">
      <div class="compare-radar-wrap">
        <canvas id="compare-radar-chart" role="img" aria-label="Radar chart comparing two islands"></canvas>
      </div>
      <div class="compare-cards" id="compare-cards"></div>
      <div class="compare-section-label" data-i18n="compare.wtv_title">When to visit — overlap</div>
      <div id="compare-wtv" class="compare-wtv"></div>
      <div id="compare-verdict" class="compare-verdict" style="{verdict_display}">{prerendered_verdict}</div>
    </div>
  </div>
</main>

<div class="cta-affiliate"><a class="ferry-btn" href="https://www.ferryhopper.com/" target="_blank" rel="noopener sponsored" data-i18n="detail.bookferry">🚢 Book ferry tickets</a><a class="car-btn" href="https://www.discovercars.com/?a_aid=antaran2" target="_blank" rel="noopener sponsored" data-i18n="detail.rentcar">🚗 Rent a car</a></div>
<footer id="site-footer">
  <div class="footer-line">
    <span class="footer-copy" data-i18n="footer.copyright">© 2026 Aegean Blueprint</span> · {privacy_link}<span class="footer-updated" id="footer-updated"></span>
  </div>
</footer>

<script>
window.__INITIAL_COMPARE_PAIR = {init_pair};
</script>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script src="/i18n.js?v=41"></script>
<script src="/script.js?v={ASSET_V}"></script>
</body>
</html>
'''
    return html


def update_sitemap(slugs):
    """Add per-pair URLs to sitemap.xml. Idempotent — replaces the block on re-runs."""
    sitemap_path = ROOT / 'sitemap.xml'
    if not sitemap_path.exists():
        return 0
    xml = sitemap_path.read_text(encoding='utf-8')

    START = '<!-- BEGIN AUTO-GENERATED COMPARE PAGES -->'
    END = '<!-- END AUTO-GENERATED COMPARE PAGES -->'
    today = '2026-06-06'

    entries = []
    # Hub pages first (higher priority than individual comparisons)
    for path in ('/compare/', '/el/compare/'):
        entries.append(
            f'<url><loc>{SITE_URL}{path}</loc>'
            f'<lastmod>{today}</lastmod>'
            f'<changefreq>weekly</changefreq>'
            f'<priority>0.7</priority></url>'
        )
    for slug in sorted(slugs):
        for path in (f'/compare/{slug}/', f'/el/compare/{slug}/'):
            entries.append(
                f'<url><loc>{SITE_URL}{path}</loc>'
                f'<lastmod>{today}</lastmod>'
                f'<changefreq>monthly</changefreq>'
                f'<priority>0.6</priority></url>'
            )
    block = START + '\n  ' + '\n  '.join(entries) + '\n  ' + END

    if START in xml and END in xml:
        new_xml = re.sub(
            re.escape(START) + r'.*?' + re.escape(END),
            block, xml, count=1, flags=re.DOTALL
        )
    else:
        new_xml = xml.replace('</urlset>', '  ' + block + '\n</urlset>')

    sitemap_path.write_text(new_xml, encoding='utf-8')
    return len(entries)


def render_hub_page(lang, valid_pairs):
    """Render the /compare/ landing page listing all comparison pairs.

    Groups: featured (hand-picked top 8) → by-region (same-group pairs) →
    cross-region. Long-form pairs surfaced first within each region.
    """
    valid_set = set(valid_pairs)

    # Featured: hand-picked, but only include those that actually exist
    featured = [pk for pk in FEATURED_PAIR_KEYS if pk in valid_set]

    # Group same-region pairs by their (shared) island_group, and collect
    # cross-region pairs separately
    by_region = {}  # group name -> list of pair_keys
    cross_region = []  # list of pair_keys
    for pk in valid_pairs:
        a, b = parse_pair_key(pk)
        ga = META[a]['group']
        gb = META[b]['group']
        if ga == gb:
            by_region.setdefault(ga, []).append(pk)
        else:
            cross_region.append(pk)

    # Sort within each section: long-form first, then alpha
    def sort_pairs(pks):
        return sorted(pks, key=lambda p: (not _is_longform(p), p))

    for g in by_region:
        by_region[g] = sort_pairs(by_region[g])
    cross_region = sort_pairs(cross_region)

    # Region display order (most comparisons / highest interest first)
    region_order = ['Cyclades', 'Crete', 'Ionian', 'Dodecanese',
                    'Saronic', 'NE Aegean', 'Sporades', 'Evia', 'Other']

    # Labels per language
    if lang == 'el':
        page_title = 'Συγκρίσεις ελληνικών νησιών | Aegean Blueprint'
        page_desc = ('Όλες οι αναλυτικές συγκρίσεις ελληνικών νησιών — '
                     'παραλίες, κουλτούρα, νυχτερινή ζωή, πρόσβαση, τιμές. '
                     'Επίλεξε το σωστό νησί για το ταξίδι σου.')
        h1_text = 'Συγκρίσεις ελληνικών νησιών'
        subtitle = ('Όλες οι αναλυτικές συγκρίσεις μας — οργανωμένες ανά περιοχή. '
                    'Κάθε σύγκριση εξετάζει παραλίες, ιστορία, φαγητό, κόστος, '
                    'και την πρακτική επιλογή του νησιού που ταιριάζει στο ταξίδι σου.')
        featured_label = 'Δημοφιλείς συγκρίσεις'
        cross_region_label = 'Συγκρίσεις μεταξύ περιοχών'
        region_labels = {
            'Cyclades': 'Κυκλάδες', 'Crete': 'Κρήτη', 'Ionian': 'Ιόνιο',
            'Dodecanese': 'Δωδεκάνησα', 'Saronic': 'Σαρωνικός',
            'NE Aegean': 'ΒΑ Αιγαίο', 'Sporades': 'Σποράδες',
            'Evia': 'Εύβοια', 'Other': 'Άλλα',
        }
        sep = 'ή'
        href_prefix = '/el/compare/'
        canonical = f'{SITE_URL}/el/compare/'
        en_url = f'{SITE_URL}/compare/'
        el_url = canonical
        og_locale = 'el_GR'
    else:
        page_title = 'Greek Island Comparisons | Aegean Blueprint'
        page_desc = ('Side-by-side comparisons of Greek islands — beaches, '
                     'culture, nightlife, access, and price. Pick the right '
                     'island for your trip.')
        h1_text = 'Greek Island Comparisons'
        subtitle = ('All our side-by-side island comparisons, organized by region. '
                    'Each one covers beaches, history, food, cost, and the '
                    'practical question of which island suits your trip.')
        featured_label = 'Featured comparisons'
        cross_region_label = 'Cross-region comparisons'
        region_labels = {
            'Cyclades': 'Cyclades', 'Crete': 'Crete', 'Ionian': 'Ionian',
            'Dodecanese': 'Dodecanese', 'Saronic': 'Saronic',
            'NE Aegean': 'North-East Aegean', 'Sporades': 'Sporades',
            'Evia': 'Evia', 'Other': 'Other',
        }
        sep = 'vs'
        href_prefix = '/compare/'
        canonical = f'{SITE_URL}/compare/'
        en_url = canonical
        el_url = f'{SITE_URL}/el/compare/'
        og_locale = 'en_US'

    def render_card(pk):
        a, b = parse_pair_key(pk)
        slug = slug_for_pair(a, b)
        if lang == 'el':
            name_a = NAMES_EL.get(a, META[a]['name'])
            name_b = NAMES_EL.get(b, META[b]['name'])
        else:
            name_a = META[a]['name']
            name_b = META[b]['name']
        href = f'{href_prefix}{slug}/'
        longform_badge = ''
        if _is_longform(pk):
            tag_label = 'Αναλυτική' if lang == 'el' else 'In-depth'
            longform_badge = f'<span class="hub-card-tag">{tag_label}</span>'
        return (
            f'<a class="hub-card" href="{esc(href)}">'
            f'<span class="hub-card-pair">{esc(name_a)} <em>{sep}</em> {esc(name_b)}</span>'
            f'{longform_badge}'
            f'<span class="hub-card-arrow" aria-hidden="true">→</span>'
            f'</a>'
        )

    def render_section(label, pks, section_id=None):
        if not pks:
            return ''
        id_attr = f' id="{section_id}"' if section_id else ''
        cards = ''.join(render_card(pk) for pk in pks)
        return (
            f'<section class="hub-section"{id_attr}>'
            f'<h2 class="hub-section-heading">{esc(label)} '
            f'<span class="hub-section-count">({len(pks)})</span></h2>'
            f'<div class="hub-grid">{cards}</div>'
            f'</section>'
        )

    # Build all sections
    sections_html = []
    if featured:
        sections_html.append(render_section(featured_label, featured, section_id='featured'))
    for region in region_order:
        if region in by_region:
            sections_html.append(render_section(region_labels[region], by_region[region]))
    if cross_region:
        sections_html.append(render_section(cross_region_label, cross_region))

    # Navigation (same structure as compare pages)
    if lang == 'el':
        nav_items = [
            ('/el/#compare', 'Σύγκριση', 'nav-compare'),
            ('/el/#match', 'Ταίριαξέ με', 'nav-match'),
            ('/el/trip-cost/', 'Μπάτζετ', 'nav-tripcost'),
            ('/el/#hopping', 'Πλοία & Νησοπορία', 'nav-hopping'),
            ('/el/festivals/', 'Γιορτές', 'nav-festivals'),
            ('/el/#data', 'Στοιχεία Νησιών', 'nav-data'),
            ('/el/#mission', 'Στόχος', 'nav-mission'),
            ('/el/#shortlist', '⭐ Λίστα μου', 'nav-shortlist'),
        ]
        privacy_link = '<a href="/el/privacy/" data-i18n="footer.privacy">Απόρρητο</a>'
    else:
        nav_items = [
            ('/#compare', 'Compare', 'nav-compare'),
            ('/#match', 'Match Me', 'nav-match'),
            ('/trip-cost/', 'Budget', 'nav-tripcost'),
            ('/#hopping', 'Ferries & Hopping', 'nav-hopping'),
            ('/festivals/', 'Festivals', 'nav-festivals'),
            ('/#data', 'Islands Data', 'nav-data'),
            ('/#mission', 'Mission', 'nav-mission'),
            ('/#shortlist', '⭐ My Shortlist', 'nav-shortlist'),
        ]
        privacy_link = '<a href="/privacy/" data-i18n="footer.privacy">Privacy</a>'

    nav_html = '\n        '.join(
        f'<a href="{esc(href)}" id="{nav_id}">{esc(label)}</a>'
        for href, label, nav_id in nav_items
    )

    page_css = '''
  main.hub-main { max-width: 960px; margin: 0 auto; padding: 32px 20px 64px; }
  .hub-hero { margin-bottom: 40px; }
  .hub-h1 {
    font-family: var(--display, Georgia, serif);
    font-size: var(--text-hero, 32px);
    margin: 0 0 8px;
    color: var(--ink-1, #222);
    line-height: 1.15;
  }
  .hub-sub {
    font-size: var(--text-body, 16px);
    line-height: 1.55;
    color: var(--ink-2, #555);
    margin: 0;
    max-width: 720px;
  }
  .hub-section { margin-bottom: 36px; }
  .hub-section-heading {
    font-family: var(--display, Georgia, serif);
    font-size: var(--text-h2, 22px);
    margin: 0 0 14px;
    color: var(--ink-1, #222);
    border-bottom: 1px solid var(--marble-3, #e0e0e0);
    padding-bottom: 6px;
  }
  .hub-section-count {
    font-size: var(--text-small, 14px);
    color: var(--ink-3, #888);
    font-weight: normal;
    margin-left: 4px;
  }
  .hub-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 10px;
  }
  .hub-card {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 14px 16px;
    background: var(--marble, #fff);
    border: 1px solid var(--marble-3, #e0e0e0);
    border-radius: 8px;
    text-decoration: none;
    color: var(--ink-1, #222);
    transition: background 0.15s, border-color 0.15s, transform 0.15s;
  }
  .hub-card:hover {
    background: var(--marble-2, #f0f0f0);
    border-color: var(--ink-3, #999);
    transform: translateY(-1px);
  }
  .hub-card-pair {
    font-size: var(--text-body, 15px);
    line-height: 1.3;
    flex: 1;
  }
  .hub-card-pair em {
    font-style: normal;
    color: var(--ink-2, #555);
    font-size: var(--text-small, 13px);
    margin: 0 4px;
  }
  .hub-card-tag {
    color: var(--aegean-dark, #076880);
    background: var(--aegean-light, #C8EEF5);
    flex-shrink: 0;
    font-size: 10.5px;
    font-weight: 800;
    padding: 2px 8px;
    border-radius: 999px;
    letter-spacing: 0.03em;
    text-transform: uppercase;
  }
  .hub-card-arrow {
    color: var(--ink-2, #555);
    flex-shrink: 0;
  }
'''

    og_image = f'{SITE_URL}/og-image.png'

    html = f'''<!DOCTYPE html>
<html lang="{'el' if lang == 'el' else 'en'}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script>window.localStorage&&document.documentElement.classList.toggle("dark",localStorage.getItem("darkMode")===null?window.matchMedia("(prefers-color-scheme: dark)").matches:localStorage.getItem("darkMode")==="true")</script>
<title>{esc(page_title)}</title>
<meta name="description" content="{esc(page_desc)}">
<meta name="theme-color" content="#0B8FAC">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="el" href="{el_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(page_title)}">
<meta property="og:description" content="{esc(page_desc)}">
<meta property="og:image" content="{og_image}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{og_locale}">
<meta property="og:site_name" content="Aegean Blueprint">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-FMFWLRM2J9"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-FMFWLRM2J9');</script>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css?v={STYLE_V}">
<style>{page_css}</style>
<script async data-cfasync="false" data-noptimize="1" data-no-defer="1" src="https://emrldtp.com/NTUxOTU3.js?t=551957"></script>
</head>
<body>
<header>
  <div class="header-content">
    <a class="logo-wrapper" href="{'/el/' if lang == 'el' else '/'}" style="text-decoration: none;">
      <img src="/logo-hero.svg" id="site-logo" alt="Aegean Blueprint logo">
      <span id="brand-text"><span class="brand-word">Aegean</span> <span class="brand-word">Blueprint</span></span>
    </a>
    <div class="menu-toggle" id="menu-toggle-btn"><span></span><span></span><span></span></div>
    <nav class="top-nav" id="main-nav">
        {nav_html}
    </nav>
    <a class="lang-toggle-static" href="{'/compare/' if lang == 'el' else '/el/compare/'}" style="background: none; border: 1px solid rgba(255,255,255,0.4); color: #fff; padding: 4px 10px; border-radius: 4px; text-decoration: none; font-size: 13px; white-space: nowrap;"><span style="margin-right: 4px;">🌐</span>{'EN' if lang == 'el' else 'EL'}</a>
  </div>
</header>

<main class="hub-main">
  <div class="hub-hero">
    <h1 class="hub-h1">{esc(h1_text)}</h1>
    <p class="hub-sub">{esc(subtitle)}</p>
  </div>
  {''.join(sections_html)}
</main>

<div class="cta-affiliate"><a class="ferry-btn" href="https://www.ferryhopper.com/" target="_blank" rel="noopener sponsored" data-i18n="detail.bookferry">🚢 Book ferry tickets</a><a class="car-btn" href="https://www.discovercars.com/?a_aid=antaran2" target="_blank" rel="noopener sponsored" data-i18n="detail.rentcar">🚗 Rent a car</a></div>
<footer id="site-footer">
  <div class="footer-line">
    <span class="footer-copy" data-i18n="footer.copyright">© 2026 Aegean Blueprint</span> · {privacy_link}<span class="footer-updated" id="footer-updated"></span>
  </div>
</footer>

<script src="/i18n.js?v=41"></script>
<script>
  (function() {{
    var btn = document.getElementById("menu-toggle-btn");
    if (btn) btn.addEventListener("click", function() {{ document.getElementById("main-nav").classList.toggle("open"); }});
  }})();
</script>
</body>
</html>
'''
    return html



def cleanup_leftover_dirs(current_slugs):
    """Remove compare/<slug>/ and el/compare/<slug>/ dirs that exist on disk
    but aren't in the current generation set. Protects against stale pages
    from earlier builds lingering and competing in search results.

    Only deletes dirs matching the *-vs-* pattern (paranoia — we never want
    to nuke anything outside the comparison-page namespace)."""
    current = set(current_slugs)
    removed = 0
    for parent in ('compare', 'el/compare'):
        dir_path = ROOT / parent
        if not dir_path.exists():
            continue
        for entry in dir_path.iterdir():
            if not entry.is_dir():
                continue
            name = entry.name
            # Safety guard: only touch dirs that look like comparison slugs
            if '-vs-' not in name:
                continue
            if name in current:
                continue
            # Leftover — remove it
            import shutil
            shutil.rmtree(entry)
            removed += 1
    return removed


def main():
    pair_keys = sorted(VERDICTS.keys())
    valid_pairs = []
    skipped = []
    for pk in pair_keys:
        a, b = parse_pair_key(pk)
        if a in META and b in META:
            valid_pairs.append(pk)
        else:
            skipped.append(pk)

    print(f"Generating static compare pages for {len(valid_pairs)} pairs ({len(skipped)} skipped)")

    slugs = []
    for pk in valid_pairs:
        a, b = parse_pair_key(pk)
        slug = slug_for_pair(a, b)
        slugs.append(slug)

        en_path = ROOT / 'compare' / slug / 'index.html'
        en_path.parent.mkdir(parents=True, exist_ok=True)
        en_path.write_text(render_page(pk, 'en'), encoding='utf-8')

        el_path = ROOT / 'el' / 'compare' / slug / 'index.html'
        el_path.parent.mkdir(parents=True, exist_ok=True)
        el_path.write_text(render_page(pk, 'el'), encoding='utf-8')

    print(f"✓ Wrote {len(valid_pairs) * 2} HTML files ({len(valid_pairs)} EN + {len(valid_pairs)} EL)")

    # Write hub pages (/compare/index.html and /el/compare/index.html)
    en_hub_path = ROOT / 'compare' / 'index.html'
    en_hub_path.parent.mkdir(parents=True, exist_ok=True)
    en_hub_path.write_text(render_hub_page('en', valid_pairs), encoding='utf-8')

    el_hub_path = ROOT / 'el' / 'compare' / 'index.html'
    el_hub_path.parent.mkdir(parents=True, exist_ok=True)
    el_hub_path.write_text(render_hub_page('el', valid_pairs), encoding='utf-8')

    print(f"✓ Wrote 2 hub pages (/compare/ and /el/compare/)")

    if skipped:
        print(f"⚠ Skipped pairs with unknown islands:")
        for pk in skipped:
            print(f"   - {pk}")

    removed = cleanup_leftover_dirs(slugs)
    if removed:
        print(f"✓ Cleaned up {removed} leftover comparison dirs (stale from earlier builds)")

    added = update_sitemap(slugs)
    if added:
        print(f"✓ Sitemap updated ({added} URL entries)")

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
