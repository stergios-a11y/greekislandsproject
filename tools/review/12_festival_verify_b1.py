#!/usr/bin/env python3
"""Festival second-source pass, batch 1 — the 20 islands whose festival pages get
the most search impressions. 57 entries that had neither high confidence nor a
second source.

Result: 39 confirmed against an independent source, 13 corrected, 5 unconfirmable.

Where a correction changes a date, the description is rewritten with it — a fixed
date and prose that still names the old one is how a page ends up contradicting
itself.

Two corrections were checked again by hand because they were large:
  sifnos[10]   The monastery of Panagia tou Vounou is dedicated to the Eisodia of
               the Theotokos (21 November), not the Annunciation — terrabook's
               monastery page states the dedication, so the entry was eight
               months out and the Lenten-menu detail belonged to the wrong fast.
  naxos[13]    naxospress (the original source) has Apollonas keeping Agios
               Ioannis Theologos on 26 September; mynaxos and naxos.travelfind
               both have Agios Ioannis Prodromos on 29 August. Two independent
               sources against one, and the saint's-day arithmetic agrees, so the
               entry moves.

The 5 unconfirmable entries are marked second_source_searched so a later pass
does not repeat the work.
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if not (ROOT / 'festivals.json').exists():
    ROOT = Path(__file__).resolve().parent / 'repo'
MERGED = Path(__file__).resolve().parent / 'merged.json'
if not MERGED.exists():
    MERGED = ROOT / 'tools' / 'review' / 'festival_verify_b1.json'

# ---- prose that has to move with a corrected date -------------------------
PROSE = {
 ('heraklion', 0): dict(
   desc="Wine festival in the village of Daphnes, the heart of Heraklion's wine country — roughly ten nights from late June into early July, not August. Tastings of local Liatiko, Vidiano and Mandilari, with music in the village square. The dates shift by a few days each year; the municipality publishes the programme in June.",
   desc_el="Γιορτή κρασιού στο χωριό Δαφνές, στην καρδιά του οινικού Ηρακλείου — περίπου δέκα βράδια από τα τέλη Ιουνίου στις αρχές Ιουλίου, όχι τον Αύγουστο. Γευσιγνωσίες τοπικών Λιάτικου, Βιδιανού και Μανδηλαριάς, με μουσική στην πλατεία. Οι ημερομηνίες μετακινούνται λίγες μέρες κάθε χρόνο· ο δήμος βγάζει το πρόγραμμα τον Ιούνιο.",
   when="Late June to early July", when_el="Τέλη Ιουνίου – αρχές Ιουλίου"),
 ('heraklion', 10): dict(
   desc="For the Nativity of the Virgin the Messara village of Agios Thomas walks out to the 14th-century chapel of Panagia Kardiotissa by the river for vespers on the evening of 7 September, followed by a glenti; it is the last big panigiri of the Heraklion season. The chapel is a short walk from the village; bring a torch for the way back.",
   desc_el="Για το Γενέσιο της Θεοτόκου ο Άγιος Θωμάς της Μεσαράς βγαίνει στο εκκλησάκι της Παναγίας Καρδιώτισσας του 14ου αιώνα, δίπλα στο ποτάμι, για εσπερινό το βράδυ της 7ης Σεπτεμβρίου και γλέντι μετά· είναι το τελευταίο μεγάλο πανηγύρι της σεζόν στο Ηράκλειο. Το ξωκλήσι είναι λίγα λεπτά περπάτημα από το χωριό· πάρε φακό για την επιστροφή."),
 ('kea', 0): dict(
   desc="A municipal food night, held on a Saturday in early May, that turns Ioulida into a tasting walk: stations at the Piazza, the main uphill street, Skaki and the square, where local producers and tavernas hand out samples of Kea specialities — paspalas, loza, thyme honey, the local cheeses — with a chef's menu inspired by Kea recipes, a sweets workshop by the women's association and dance groups to finish. Free; Ioulida is car-free, so park at the entrance and walk.",
   desc_el="Γαστρονομική βραδιά του Δήμου, ένα Σάββατο στις αρχές Μαΐου, που κάνει την Ιουλίδα περίπατο γεύσεων: σταθμοί στην Πιάτσα, στον κεντρικό ανηφορικό δρόμο, στο Σκάκι και στην πλατεία, όπου παραγωγοί και ταβέρνες μοιράζουν δείγματα από τζιώτικες σπεσιαλιτέ — πασπαλάς, λόζα, θυμαρίσιο μέλι, ντόπια τυριά — με μενού σεφ εμπνευσμένο από κείες συνταγές, εργαστήρι γλυκών από τον Σύλλογο Γυναικών και χορευτικά στο τέλος. Δωρεάν· η Ιουλίδα είναι πεζόδρομος, πάρκαρε στην είσοδο και περπάτα.",
   when="A Saturday in early May", when_el="Ένα Σάββατο στις αρχές Μαΐου"),
 ('sifnos', 10): dict(
   desc="The hilltop monastery of Panagia tou Vounou, with the best view over Platys Gialos bay, is dedicated to the Eisodia — the Presentation of the Virgin — and celebrates with vespers and a fasting panigiri on the evening of 20 November: revithada and salt cod rather than lamb, since it falls in the Nativity fast, plus the violin-laouto takimi. Out of season the island is quiet and this is a genuinely local night; it is on the Apollonia–Platys Gialos road, so easy to reach by car.",
   desc_el="Το μοναστήρι της Παναγιάς του Βουνού, με την καλύτερη θέα στον κόλπο του Πλατύ Γιαλού, είναι αφιερωμένο στα Εισόδια της Θεοτόκου και γιορτάζει με εσπερινό και νηστίσιμο πανηγύρι το βράδυ της 20ής Νοεμβρίου — ρεβιθάδα και μπακαλιάρο αντί για αρνί, αφού πέφτει στη σαρακοστή των Χριστουγέννων, με το τακίμι βιολί–λαούτο. Εκτός σεζόν το νησί είναι ήσυχο και η βραδιά καθαρά ντόπια· είναι πάνω στον δρόμο Απολλωνίας–Πλατύ Γιαλού, εύκολα με αυτοκίνητο.",
   when="20–21 November", when_el="20–21 Νοεμβρίου"),
 ('naxos', 13): dict(
   name="Panigiri of Agios Ioannis Prodromos, Apollonas",
   name_el="Πανηγύρι Αγίου Ιωάννη Προδρόμου, Απόλλωνας",
   desc="The fishing village of Apollonas at the northern tip keeps the Beheading of the Forerunner — vespers on the evening of 28 August, liturgy on the 29th — with grilled meat and seafood, local wine, music and dancing by the harbour. One of the last panigiria of the Naxos season, with the August crowds gone and the water still warm.",
   desc_el="Ο ψαράδικος Απόλλωνας στη βόρεια άκρη γιορτάζει την Αποτομή του Προδρόμου — εσπερινός το βράδυ της 28ης Αυγούστου, λειτουργία στις 29 — με ψητά και θαλασσινά, ντόπιο κρασί, μουσική και χορό στο λιμάνι. Από τα τελευταία πανηγύρια της ναξιώτικης σεζόν, με τον αυγουστιάτικο κόσμο να έχει φύγει και τη θάλασσα ακόμα ζεστή.",
   when="28–29 August", when_el="28–29 Αυγούστου"),
 ('astypalaia', 1): dict(
   desc="The island's patron, the monk Anthimos who brought the Portaitissa icon, is honoured on 4 September with a liturgy and procession through Chora. A quiet, local occasion at the end of the season.",
   desc_el="Ο πολιούχος του νησιού, ο μοναχός Άνθιμος που έφερε την εικόνα της Πορταΐτισσας, τιμάται στις 4 Σεπτεμβρίου με λειτουργία και λιτανεία στη Χώρα. Ήσυχη, ντόπια γιορτή στο τέλος της σεζόν."),
 ('samos', 0): dict(
   desc="The Heraion half of the Municipality of East Samos's Iraia–Pythagoreia festival: concerts, theatre and commemorations of Hera, ancient patroness of Samos, staged at and around the sanctuary. The programme runs across August, with some events into September and October; the municipality publishes it in July.",
   desc_el="Το σκέλος «Ηραία» του φεστιβάλ Ηραία–Πυθαγόρεια του Δήμου Ανατολικής Σάμου: συναυλίες, θέατρο και εκδηλώσεις για την Ήρα, αρχαία προστάτιδα της Σάμου, στο Ηραίο και γύρω από αυτό. Το πρόγραμμα απλώνεται σε όλον τον Αύγουστο, με εκδηλώσεις και τον Σεπτέμβριο–Οκτώβριο· ο δήμος το ανακοινώνει τον Ιούλιο.",
   when="Throughout August", when_el="Σε όλον τον Αύγουστο"),
 ('lemnos', 0): dict(
   desc="Patron saint of Lemnos. Great vespers and the procession of the icon on the evening of 6 September at the church of Agios Sozon at Fysini, liturgy on the 7th, and a panigiri that runs three days — the biggest on the island.",
   desc_el="Προστάτης άγιος της Λήμνου. Μέγας εσπερινός και λιτανεία της εικόνας το βράδυ της 6ης Σεπτεμβρίου στον Άγιο Σώζοντα στη Φυσίνη, λειτουργία στις 7, και πανηγύρι που κρατά τρεις μέρες — το μεγαλύτερο του νησιού.",
   when="6–8 September", when_el="6–8 Σεπτεμβρίου"),
 ('milos', 0): dict(
   desc="Folk Saint John's Eve tradition still alive on Milos: at sunset on 23 June, unmarried girls collect water from a well in silence and leave tokens in it overnight; the tokens are drawn on the 24th, the saint's day, to predict their future husbands. Bonfires are jumped on the eve. Smaller and more intimate than the better-known Cretan version.",
   desc_el="Λαϊκή παράδοση της παραμονής του Αγίου Ιωάννη ζωντανή στη Μήλο: το σούρουπο της 23ης Ιουνίου, ανύπαντρες κοπέλες παίρνουν νερό από πηγάδι σιωπηλά και αφήνουν μέσα σημάδια όλη νύχτα· τα βγάζουν στις 24, την ημέρα του άγιου, για να μαντέψουν τον μέλλοντα σύζυγο. Οι φωτιές πηδιούνται την παραμονή. Πιο οικείο από την κρητική εκδοχή.",
   when="23 June (eve) and 24 June", when_el="23 Ιουνίου (παραμονή) και 24 Ιουνίου"),
 ('santorini', 0): dict(
   desc="Classical music and arts festival hosted at the 17th-century Megaron Gyzi mansion in Fira — about eleven days in early-to-mid August (3–13 August in 2026). Chamber concerts, recitals, exhibitions. The quiet, refined antithesis to Santorini's mass-tourism reputation. Limited tickets — book ahead.",
   desc_el="Φεστιβάλ κλασικής μουσικής και τεχνών στο αρχοντικό του Μεγάρου Γκύζη του 17ου αιώνα στα Φηρά — περίπου έντεκα μέρες στις αρχές με μέσα Αυγούστου (3–13 Αυγούστου το 2026). Συναυλίες δωματίου, ρεσιτάλ, εκθέσεις. Η ήσυχη, εκλεπτυσμένη αντίθεση στη μαζική φήμη της Σαντορίνης. Περιορισμένα εισιτήρια.",
   when="Early-to-mid August", when_el="Αρχές–μέσα Αυγούστου"),
 ('kos', 0): dict(
   desc="Annual cultural festival named after the island's most famous son, running from July through September with Hippocratic Week in mid-October. Open-air concerts, theatre, the symbolic re-reading of the Hippocratic Oath at the Asklepieion archaeological site. The main draws are the dance performances and ancient drama productions in atmospheric settings.",
   desc_el="Ετήσιο πολιτιστικό φεστιβάλ που τιμά τον πιο διάσημο γιο του νησιού, από τον Ιούλιο έως τον Σεπτέμβριο, με την Ιπποκράτεια Εβδομάδα στα μέσα Οκτωβρίου. Υπαίθριες συναυλίες, θέατρο, συμβολική απαγγελία του Όρκου του Ιπποκράτη στο Ασκληπιείο. Κυρίαρχες οι παραστάσεις χορού και αρχαίου δράματος.",
   when="July through September, with Hippocratic Week in mid-October",
   when_el="Ιούλιος–Σεπτέμβριος, με την Ιπποκράτεια Εβδομάδα στα μέσα Οκτωβρίου"),
 ('mykonos', 0): dict(
   desc="Major international LGBTQ+ summer festival drawing 30,000+ visitors — six days in late August, on dates that move every year (20–25 August in 2026). Pool parties, beach events, headline DJs at Cavo Paradiso and other venues. Mykonos has been a leading gay summer destination since the 1970s; XLSIOR is the most concentrated week of it. Expect rooms to be impossible.",
   desc_el="Μεγάλο διεθνές ΛΟΑΤΚΙ+ καλοκαιρινό φεστιβάλ με 30.000+ επισκέπτες — έξι μέρες στα τέλη Αυγούστου, σε ημερομηνίες που αλλάζουν κάθε χρόνο (20–25 Αυγούστου το 2026). Πάρτι σε πισίνες, παραλιακές εκδηλώσεις, διεθνείς DJ σε Cavo Paradiso και αλλού. Η Μύκονος είναι κορυφαίος γκέι προορισμός από τη δεκαετία του 1970· το XLSIOR είναι η πιο πυκνή εβδομάδα του. Βρες δωμάτιο από πολύ νωρίς — αλλιώς δεν υπάρχει.",
   when="Late August (20–25 August in 2026)", when_el="Τέλη Αυγούστου (20–25 Αυγούστου το 2026)"),
}
# fixes the agents described in prose but did not put in a `fix` object
EXTRA_FIX = {
 ('naxos', 13):      {'date': {'fixed': '08-29'}},
 ('astypalaia', 1):  {'date': {'fixed': '09-04'}},
}

def main():
    data = json.loads((ROOT / 'festivals.json').read_text(encoding='utf-8'))
    verd = json.loads(MERGED.read_text(encoding='utf-8'))
    n_conf = n_corr = n_unc = 0
    for isl, items in verd.items():
        for it in items:
            f = data[isl][it['i']]
            v = it['verdict']
            if v == 'unconfirmable':
                f['second_source_searched'] = True
                n_unc += 1
                continue
            if it.get('source2'):
                f['source2'] = it['source2']
            if it.get('confidence'):
                f['confidence'] = it['confidence']
            if v == 'confirmed':
                n_conf += 1
                continue
            fix = dict(it.get('fix') or {})
            fix.update(EXTRA_FIX.get((isl, it['i']), {}))
            fix.update(PROSE.get((isl, it['i']), {}))
            if not fix:
                print(f'  !! {isl}[{it["i"]}] corrected with nothing to apply', file=sys.stderr)
                return 1
            for k, val in fix.items():
                f[k] = val
            print(f'  {isl:11}[{it["i"]}] {", ".join(sorted(fix))}')
            n_corr += 1
    (ROOT / 'festivals.json').write_text(
        json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'\n{n_conf} confirmed, {n_corr} corrected, {n_unc} marked searched')
    return 0

sys.exit(main())
