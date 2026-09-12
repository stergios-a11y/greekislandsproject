#!/usr/bin/env python3
"""Festival second-source pass, batch 2 — the remaining 119 entries on 47 islands.

71 confirmed against an independent source, 16 corrected, 32 unconfirmable.
The unconfirmable share is much higher than batch 1 because these are the
low-traffic islands: Arki, Telendos, Psara, Othonoi and the smaller Evia
villages simply have very little dated web presence.

As in batch 1, a corrected date takes its description with it.

Two of the corrections land on entries this project changed only yesterday:
  folegandros[0]  I had made the Kera procession Easter Monday + 7 days. It
                  starts on Easter Sunday itself and runs three days.
  skyros[0]       My 2-day Apokries window ended before Clean Monday, which is
                  when the Geros dances in the square. Three days.
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if not (ROOT / 'festivals.json').exists():
    ROOT = Path(__file__).resolve().parent / 'repo'
MERGED = Path(__file__).resolve().parent / 'merged2.json'
if not MERGED.exists():
    MERGED = ROOT / 'tools' / 'review' / 'festival_verify_b2.json'

PROSE = {
 ('ammouliani', 0): dict(
   desc="Ammouliani was settled in 1925 by refugees from the island of Marmara, who brought the cult of their 14th-century icon of Panagia Stylarini (the original is in Koutloumousiou on Athos, the copy in the island's church). The feast is kept on the first Saturday-Sunday on or after the Exaltation of the Cross on 14 September (14-15 September 2024, 16-17 September 2023) with a great vespers, a procession down to the harbour and an episcopal liturgy with the Metropolitan of Ierissos. The season is winding down, so rooms are easy and the fish tavernas are still open.",
   desc_el="Η Αμμουλιανή κατοικήθηκε το 1925 από πρόσφυγες του νησιού Μαρμαρά, που έφεραν τη λατρεία της εικόνας της Παναγίας Στυλαρινής του 14ου αιώνα (η αυθεντική είναι στην Κουτλουμουσίου στον Άθω, το αντίγραφο στον ναό του νησιού). Η γιορτή γίνεται το πρώτο Σάββατο-Κυριακή από τις 14 Σεπτεμβρίου και μετά, στην Ύψωση του Σταυρού (14-15 Σεπτεμβρίου 2024, 16-17 Σεπτεμβρίου 2023), με μέγα εσπερινό, λιτανεία ως το λιμάνι και αρχιερατική λειτουργία με τον Μητροπολίτη Ιερισσού. Η σεζόν τελειώνει, οπότε δωμάτια βρίσκεις εύκολα και οι ψαροταβέρνες είναι ακόμα ανοιχτές.",
   when="First Saturday-Sunday on or after 14 September",
   when_el="Το πρώτο Σάββατο-Κυριακή από τις 14 Σεπτεμβρίου"),
 ('skyros', 0): dict(
   desc="Among the most distinctive carnivals in Greece — the 'Yeros' figure dressed in goat skins and bells dances through the village. The peak is the last Apokries Saturday and Sunday plus Clean Monday, when the Geros dances in the square all day. Pre-Christian roots, deeply Skyrian.",
   desc_el="Από τις πιο ξεχωριστές απόκριες της Ελλάδας — η μορφή του «Γέρου» ντυμένου με κατσικίσιες προβιές και κουδούνια χορεύει στους δρόμους του χωριού. Κορυφώνεται το τελευταίο Σάββατο-Κυριακή της Αποκριάς και την Καθαρά Δευτέρα, όταν ο Γέρος χορεύει στην πλατεία όλη μέρα. Προχριστιανικές ρίζες, βαθιά σκυριανές.",
   when="Apokries Saturday to Clean Monday", when_el="Από το Σάββατο της Αποκριάς ως την Καθαρά Δευτέρα"),
 ('kalymnos', 2): dict(
   desc="Not the 15 August panigiri, despite the name: on the Dormition the liturgy is in the Arginonta parish church, and the mountain chapel of Panagia Galatiani gets its own night about a week later, when the icon is carried back up the valley with a procession, vespers and a glendi in the chapel courtyard (21-22 August in 2026). An easier option than the climb to Kyra Psili and popular with the climbing crowd staying in Masouri, ten minutes away by scooter.",
   desc_el="Δεν είναι το πανηγύρι της 15ης Αυγούστου, παρά το όνομα: τον Δεκαπενταύγουστο η λειτουργία γίνεται στον ενοριακό ναό της Αργινώντας, και το ξωκλήσι της Παναγίας της Γαλατιανής στο βουνό έχει τη δική του βραδιά περίπου μια βδομάδα μετά, όταν η εικόνα ανεβαίνει πίσω στην κοιλάδα με λιτανεία, εσπερινό και γλέντι στην αυλή του ξωκλησιού (21-22 Αυγούστου το 2026). Πιο εύκολο από την ανάβαση στην Κυρά Ψηλή και αγαπημένο των αναρριχητών που μένουν Μασούρι, δέκα λεπτά με μηχανάκι.",
   when="Late August, about a week after the Dormition",
   when_el="Τέλη Αυγούστου, περίπου μια βδομάδα μετά τον Δεκαπενταύγουστο"),
 ('syros', 0): dict(
   name="Klidonas bonfires, Kaminia", name_el="Κλήδονας, Καμίνια",
   desc="The village of Kaminia revives the Klidonas on the night of 23-24 June: the May wreaths are burned, kids jump the fire, and the local cultural association serves meze and wine with live music. Small and local, and a short drive from Ermoupoli.",
   desc_el="Τα Καμίνια αναβιώνουν τον Κλήδονα τη νύχτα 23-24 Ιουνίου: καίγονται οι μάηδες, τα παιδιά πηδούν τη φωτιά και ο πολιτιστικός σύλλογος κερνά μεζέ και κρασί με ζωντανή μουσική. Μικρό και τοπικό, λίγα λεπτά με αυτοκίνητο από την Ερμούπολη."),
 ('andros', 3): dict(
   desc="The port of Gavrio spreads the Gavriotika across a month, from late July into late August: sports tournaments, a chess competition, folk evenings and, on the closing night, a big kakavia (fishermen's soup) cooked on the waterfront and served free with music and dancing. The programme is announced by the Filoproodos Omilos 'To Gavrio' each summer. Handy if you are arriving or leaving by ferry.",
   desc_el="Το Γαύριο απλώνει τα Γαυριώτικα σε έναν μήνα, από τα τέλη Ιουλίου ως τα τέλη Αυγούστου: αθλητικά τουρνουά, σκάκι, λαϊκές βραδιές και την τελευταία νύχτα μεγάλη κακαβιά που βράζει στην προκυμαία και μοιράζεται δωρεάν με μουσική και χορό. Το πρόγραμμα το βγάζει κάθε καλοκαίρι ο Φιλοπρόοδος Όμιλος «Το Γαύριο». Βολεύει αν φτάνεις ή φεύγεις με πλοίο.",
   when="Late July to late August", when_el="Τέλη Ιουλίου – τέλη Αυγούστου"),
 ('andros', 9): dict(
   desc="The beach hamlet of Vitali on the north-east coast holds one of the last panigiria of the Andros summer for Agia Sofia on 17 September, with a liturgy at the chapel and food, wine and music by the sea. Reached by a long dirt road from Vourkoti or Ano Agios Petros; go with a car you do not mind scratching.",
   desc_el="Το Βιτάλι, ο μικρός οικισμός στην παραλία της βορειοανατολικής ακτής, κάνει ένα από τα τελευταία πανηγύρια του ανδριώτικου καλοκαιριού για την Αγία Σοφία στις 17 Σεπτεμβρίου, με λειτουργία στο ξωκλήσι και φαγητό, κρασί και μουσική δίπλα στη θάλασσα. Φτάνεις από μεγάλο χωματόδρομο από Βουρκωτή ή Άνω Άγιο Πέτρο, πήγαινε με αυτοκίνητο που δεν σε νοιάζει να γρατζουνιστεί.",
   when="17 September", when_el="17 Σεπτεμβρίου"),
 ('halki', 3): dict(
   desc="Two evenings of mandolin music, the instrument of old Halki, on the steps of Agios Nikolaos and on the harbour (22-23 July in 2026), with Cretan and Dodecanese players. Informal; bring a chair or grab a taverna table on the front.",
   desc_el="Δύο βραδιές μαντολίνου, του οργάνου της παλιάς Χάλκης, στα σκαλιά του Αγίου Νικολάου και στο λιμάνι (22-23 Ιουλίου το 2026), με κρητικούς και δωδεκανήσιους παίχτες. Χαλαρό· πάρε καρέκλα ή πιάσε τραπέζι σε ταβέρνα της παραλίας.",
   when="22-23 July, 2 nights", when_el="22-23 Ιουλίου, 2 βραδιές"),
 ('lasithi', 0): dict(
   desc="Eastern Crete's big summer festival, named after the 17th-century Sitia-born poet Vitsentzos Kornaros, author of 'Erotokritos'. Concerts, dance, theatre and exhibitions from early June to the end of August, in and around the Venetian Kazarma fortress, plus village panigiria with raki, Cretan bands and communal tables. One of the most honest cultural experiences on the island.",
   desc_el="Το μεγάλο καλοκαιρινό φεστιβάλ της ανατολικής Κρήτης, στο όνομα του Σητειακού ποιητή Βιτσέντζου Κορνάρου, του δημιουργού του «Ερωτόκριτου». Συναυλίες, χορός, θέατρο και εκθέσεις από τις αρχές Ιουνίου ως το τέλος Αυγούστου, στο βενετσιάνικο φρούριο Καζάρμα και γύρω από αυτό, μαζί με πανηγύρια στα χωριά με ρακή, κρητικές κομπανίες και κοινά τραπέζια. Μια από τις πιο αυθεντικές πολιτιστικές εμπειρίες του νησιού.",
   when="Early June to the end of August", when_el="Αρχές Ιουνίου – τέλη Αυγούστου"),
 ('spetses', 0): dict(
   desc="The single most spectacular naval festival in Greece. Reenacts the 1822 Battle of Spetses — a wooden replica of the Ottoman flagship is set ablaze in the harbour, with fireworks. The burning is on the Saturday of that week; 8 September itself carries the festal liturgy of Panagia Armata, and the surrounding programme runs from late August to mid-September. Hundreds of thousands attend; book accommodation months ahead.",
   desc_el="Το πιο εντυπωσιακό ναυτικό φεστιβάλ στην Ελλάδα. Αναπαράσταση της Ναυμαχίας των Σπετσών (1822) — ξύλινο αντίγραφο της οθωμανικής ναυαρχίδας πυρπολείται στο λιμάνι, με πυροτεχνήματα. Η πυρπόληση γίνεται το Σάββατο εκείνης της εβδομάδας· στις 8 Σεπτεμβρίου είναι η λειτουργία της Παναγίας Αρμάτας, και το γύρω πρόγραμμα τρέχει από τα τέλη Αυγούστου ως τα μέσα Σεπτεμβρίου. Εκατοντάδες χιλιάδες έρχονται· κράτηση μήνες πριν.",
   when="Saturday of the week of 8 September",
   when_el="Το Σάββατο της εβδομάδας της 8ης Σεπτεμβρίου"),
 ('schoinoussa', 1): dict(
   desc="Panagia Akathi in Chora is the island's church, and its panigiri falls not in summer but on the Saturday of the Akathist in Great Lent, when the icon is carried through Chora. It is the one night of the year the whole of Schinoussa, plus visitors from Iraklia and Koufonisi, sits down together: patatato and other local dishes served free after the liturgy, wine, and violin-and-laouto dancing until late. Book a room well ahead; the island has few.",
   desc_el="Η Παναγία η Ακαθή στη Χώρα είναι η εκκλησία του νησιού, και το πανηγύρι της δεν πέφτει το καλοκαίρι αλλά το Σάββατο του Ακαθίστου στη Μεγάλη Σαρακοστή, όταν η εικόνα περιφέρεται στη Χώρα. Είναι η μία νύχτα του χρόνου που όλη η Σχοινούσα, μαζί με κόσμο από Ηρακλειά και Κουφονήσι, κάθεται στο ίδιο τραπέζι: πατατάτο και άλλα ντόπια φαγητά δωρεάν μετά τη λειτουργία, κρασί και χορός με βιολί και λαούτο ως αργά. Κλείσε δωμάτιο πολύ νωρίς, το νησί έχει λίγα.",
   when="Saturday of the Akathist, Great Lent", when_el="Σάββατο του Ακαθίστου, Μεγάλη Σαρακοστή"),
 ('schoinoussa', 2): dict(
   name="Panigiri of Agios Nikolaos, Pharos", name_el="Πανηγύρι Αγίου Νικολάου, Φάρος",
   desc="The lighthouse chapel at Pharos, reached by caique from Mersini, celebrates the sailors' saint on 6 December with a liturgy and a communal meal for the islanders who winter on Schinoussa. Worth knowing only if you are there in December.",
   desc_el="Το ξωκλήσι στον Φάρο, όπου φτάνεις με καΐκι από τη Μερσίνη, γιορτάζει τον Άγιο Νικόλαο στις 6 Δεκεμβρίου με λειτουργία και κοινό τραπέζι για όσους ξεχειμωνιάζουν στη Σχοινούσα. Χρήσιμο μόνο αν βρεθείς εκεί τον Δεκέμβρη."),
 ('evia-central', 1): dict(
   desc="Kymi's dried figs are a PDO product and the village of Vitala above the town celebrates them with an evening festival on 16 August, at 9 pm: fig sweets and fig-based dishes, live music and dancing, 5 EUR entry and food and drink deliberately held at old prices. Fits neatly with the Oxylithos stifado the day before.",
   desc_el="Τα ξερά σύκα Κύμης είναι προϊόν ΠΟΠ και τα Βίταλα, πάνω από την πόλη, τα γιορτάζουν με βραδινή γιορτή στις 16 Αυγούστου, στις 9 μ.μ.: γλυκά και φαγητά με σύκο, ζωντανή μουσική και χορός, είσοδος 5 ευρώ και φαγητό-ποτό επίτηδες σε παλιές τιμές. Δένει με το στιφάδο του Οξυλίθου την προηγούμενη μέρα.",
   when="16 August", when_el="16 Αυγούστου"),
 ('folegandros', 0): dict(
   desc="The icon of the Panagia is brought down from the Kastro church on Easter Sunday and carried from house to house across the island over the following three days — a procession unique to Folegandros, with locals hosting the icon overnight in turn.",
   desc_el="Η εικόνα της Παναγίας κατεβαίνει από την εκκλησία του Κάστρου την Κυριακή του Πάσχα και περιφέρεται από σπίτι σε σπίτι σε όλο το νησί τις επόμενες τρεις μέρες — λιτανεία μοναδική στη Φολέγανδρο, με τους ντόπιους να φιλοξενούν την εικόνα με τη σειρά.",
   when="Easter Sunday to Bright Tuesday", when_el="Από την Κυριακή του Πάσχα ως τη Τρίτη της Διακαινησίμου"),
 ('folegandros', 4): dict(
   desc="A harbour evening in Karavostasi built around kakavia, the fishermen's soup: the local boats' catch is cooked in big pots on the quay and served free with wine, with island music afterwards. Held on 23 August; arrive early with a plate and a spoon of your own if you can, and eat standing — there are few tables.",
   desc_el="Βραδιά στο λιμάνι του Καραβοστασιού γύρω από την κακαβιά, τη σούπα των ψαράδων: η ψαριά των καϊκιών μαγειρεύεται σε μεγάλα καζάνια στην προβλήτα και μοιράζεται δωρεάν με κρασί, με νησιώτικη μουσική μετά. Γίνεται 23 Αυγούστου· έλα νωρίς, αν μπορείς με δικό σου πιάτο και κουτάλι, και φάε όρθιος — τραπέζια υπάρχουν λίγα."),
 ('lesvos', 0): dict(
   desc="In Agia Paraskevi village, an ancient and unusual ritual: a bull is paraded, blessed, then ritually slaughtered and shared communally. The festival runs Friday to Monday and the dates are announced each year by the village's farming association, usually in late June or early July. Pre-Christian roots, controversial in modern times, but among Greece's most extraordinary surviving folk traditions.",
   desc_el="Στο χωριό Αγία Παρασκευή, αρχαία και ασυνήθιστη τελετή: ένας ταύρος περιφέρεται, ευλογείται, μετά θυσιάζεται και μοιράζεται κοινοτικά. Το πανηγύρι κρατά από Παρασκευή ως Δευτέρα και οι ημερομηνίες ανακοινώνονται κάθε χρόνο από τον αγροτικό σύλλογο του χωριού, συνήθως τέλη Ιουνίου ή αρχές Ιουλίου. Προχριστιανικές ρίζες, αμφιλεγόμενη στην εποχή μας, αλλά από τις πιο ξεχωριστές επιβιώνουσες λαϊκές παραδόσεις της Ελλάδας.",
   when="Friday to Monday, late June or early July (announced annually)",
   when_el="Παρασκευή ως Δευτέρα, τέλη Ιουνίου ή αρχές Ιουλίου (ανακοινώνεται κάθε χρόνο)"),
}

def main():
    data = json.loads((ROOT / 'festivals.json').read_text(encoding='utf-8'))
    verd = json.loads(MERGED.read_text(encoding='utf-8'))
    nc = nk = nu = 0
    for isl, items in verd.items():
        for it in items:
            f = data[isl][it['i']]
            v = it['verdict']
            if v == 'unconfirmable':
                f['second_source_searched'] = True; nu += 1; continue
            if it.get('source2'): f['source2'] = it['source2']
            if it.get('confidence'): f['confidence'] = it['confidence']
            if v == 'confirmed':
                nc += 1; continue
            fix = dict(it.get('fix') or {})
            fix.update(PROSE.get((isl, it['i']), {}))
            if not fix:
                print(f'  !! {isl}[{it["i"]}] corrected with nothing to apply', file=sys.stderr); return 1
            for k, val in fix.items(): f[k] = val
            print(f'  {isl:13}[{it["i"]}] {", ".join(sorted(fix))}')
            nk += 1
    (ROOT / 'festivals.json').write_text(
        json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'\n{nc} confirmed, {nk} corrected, {nu} marked searched')
    return 0

sys.exit(main())
