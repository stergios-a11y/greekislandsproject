#!/usr/bin/env python3
"""Five new compare pages: every Small Cyclades pair except donousa/schoinoussa,
which already exists. Opinionated — each one states which island wins and for
whom, rather than hedging.

Scores in play: koufonisia 4.0 (beach 5.0, night 4.0, access 3.0, afford 3.0),
schoinoussa 3.4 (4.5/2.5/2.5/3.8), donousa 3.4 (4.5/2.5/2.2/3.8),
iraklia 3.2 (4.2/1.5/2.0/4.3).
"""
import json

V = {}


def cols(a_name, b_name, a_items, b_items, el=False):
    h = 'Διάλεξε' if el else 'Choose'
    suffix = 'αν…' if el else 'if…'
    li = lambda xs: ''.join(f'<li>{x}</li>' for x in xs)
    return (f'\n<div class="compare-verdict-cols">\n<div class="compare-verdict-col">\n'
            f'<h4>{h} {a_name} {suffix}</h4>\n<ul>\n{li(a_items)}\n</ul>\n</div>\n'
            f'<div class="compare-verdict-col">\n<h4>{h} {b_name} {suffix}</h4>\n<ul>\n{li(b_items)}\n</ul>\n</div>\n</div>\n')


# ===================================================== koufonisia vs schoinoussa
V['koufonisia__schoinoussa'] = {'en': (
"<p><strong>The short answer:</strong> Koufonisia, on the numbers and on the water — 4.0 overall against 3.4, and a rare 5.0 for beaches. Pori, Italida and the Pisina rock pool are genuinely among the best swimming in the Cyclades, not just among the best in this little archipelago. But that is exactly the problem: Koufonisia is the Small Cyclades island that got discovered. In August it has boat traffic, a bar scene and rooms that sold out in February. Schoinoussa is what Koufonisia felt like fifteen years ago, and it has better food than an island of 227 people has any right to. Go to Koufonisia for the water. Go to Schoinoussa for the dinner and the quiet.</p>"
+ cols('Koufonisia', 'Schoinoussa',
 ["The beaches are the point of the trip. Pori is a vast sandy bay, Italida and Fanos are close to perfect, and the Pisina — a natural rock pool you jump into — is the single most photographed thing in the Small Cyclades.",
  "You want somewhere flat and walkable. Pano Koufonisi is 4 km² and almost level; you can reach every beach on foot or by bike, and plenty of people never rent anything.",
  "You want a bit of life after dinner. It scores 4.0 for nightlife, which for this archipelago is enormous — a handful of proper bars in the Chora and a young summer crowd.",
  "You want the day trip to Kato Koufonisi, the uninhabited island across the channel, with Nero and Detis beaches and nobody on them.",
  "You are going in June or September and can therefore have the beaches without the crowd."],
 ["You want the food. Half a dozen tavernas in the Chora punch far above the island's size — Deli is in the Greek Gastronomy Guide and the fava is worth the ferry on its own.",
  "You want quiet in August, when Koufonisia does not have any. Schoinoussa gets Greek families, not a scene.",
  "You like the idea of the driest place in Greece — it is nicknamed the Island of the Sun and gets less rain than anywhere else in the country.",
  "You want every beach within a 35-minute walk of one village, on gentle terrain, with a natural harbour at Mersini that doubles as a swimming bay.",
  "You are travelling with children and want easy, shallow, sheltered water — Almyros in particular."])
+ """
<h4>The beaches, honestly</h4>
<p>Koufonisia wins and it is not close. It scores 5.0 to Schoinoussa's 4.5, and the gap is real rather than a rounding artefact: Pori is a genuine set-piece beach, a wide sweep of pale sand at the north end of the island, and the run of coves along the east coast — Finikas, Fanos, Italida, Platia Pounta — gives you four or five distinct swims within an hour's walk. The Pisina, a deep rock pool in the low cliffs, is the kind of thing people plan a trip around.</p>
<p>Schoinoussa's beaches are excellent and would be the headline on almost any other island. Tsigouri is five minutes from the port, Psili Ammos is the long sandy one in the north, and Almyros is the shallowest and most sheltered water in the group. What Schoinoussa lacks is a Pori — a beach that makes you stop walking and stare. What it has instead is that every single beach is easy to reach, which for a family or a week of doing very little matters more than a set-piece.</p>

<h4>What each island is actually like</h4>
<p>Koufonisia is busy in a way that surprises people who came expecting a Lesser Cyclades hermitage. The Chora has bars that stay open, a fishing fleet that still works, boats coming and going all day in high season. It is a lovely island with a genuine local life, but in the first three weeks of August it is closer in feel to a small Paros than to its neighbours. The flatness is a real gift — everything is bikeable — and the fact that Kato Koufonisi sits empty ten minutes away by caique means you always have an escape.</p>
<p>Schoinoussa is a single low hill with one village on top and a port beneath it. Nothing much happens, on purpose. The pleasure of the place is the walk down to a beach in the morning, the walk back up in the evening, and then a dinner that is startlingly good for somewhere this small. The Chora at night is a handful of lit tables and not much else, which is either exactly what you came for or a problem.</p>

<h4>Logistics and cost</h4>
<p>Both sit on the Express Skopelitis line that threads the Small Cyclades out of Naxos, and both are also reachable direct from Piraeus on the larger ferries (6–9 hours). Koufonisia has the better connections of the two — it is the busiest stop on the chain, so more boats call and more days work. Schoinoussa is a shorter hop from Naxos but sees fewer sailings.</p>
<p>Koufonisia is the more expensive island, and the difference is not trivial in August: it scores 3.0 for affordability against Schoinoussa's 3.8, which in practice means rooms costing meaningfully more and booking months earlier. Out of season the gap narrows to almost nothing.</p>

<h4>The honest verdict</h4>
<p>If you are only going to visit one Small Cyclades island in your life, go to Koufonisia — the beaches are better than Schoinoussa's, and being told to avoid somewhere because it is popular is usually bad advice. But go in June or September. In August, Koufonisia is a victim of its own photographs and Schoinoussa is the better holiday: cheaper, emptier, and with the best food in the archipelago by a distance. The real answer, if you have five days, is both — they are ninety minutes apart on the same boat, and doing the pair costs less than a long weekend on Mykonos.</p>
"""),
'el': (
"<p><strong>Η σύντομη απάντηση:</strong> Τα Κουφονήσια, στα νούμερα και στο νερό — 4.0 συνολικά έναντι 3.4, και ένα σπάνιο 5.0 στις παραλίες. Το Πόρι, η Ιταλίδα και η Πισίνα είναι από τα καλύτερα μπάνια των Κυκλάδων, όχι μόνο του μικρού αυτού συμπλέγματος. Αυτό όμως είναι και το πρόβλημα: τα Κουφονήσια είναι το νησί των Μικρών Κυκλάδων που ανακαλύφθηκε. Τον Αύγουστο έχει σκάφη, μπαρ και δωμάτια που κλείστηκαν τον Φεβρουάριο. Η Σχοινούσα είναι ό,τι ήταν τα Κουφονήσια δεκαπέντε χρόνια πριν, και έχει καλύτερο φαγητό από όσο δικαιούται ένα νησί 227 κατοίκων. Κουφονήσια για το νερό. Σχοινούσα για το δείπνο και την ησυχία.</p>"
+ cols('τα Κουφονήσια', 'τη Σχοινούσα',
 ["Οι παραλίες είναι ο λόγος του ταξιδιού. Το Πόρι είναι ένας απέραντος αμμώδης κόλπος, η Ιταλίδα και ο Φανός σχεδόν ιδανικές, και η Πισίνα — φυσική πέτρινη πισίνα όπου βουτάς — το πιο φωτογραφημένο σημείο των Μικρών Κυκλάδων.",
  "Θέλεις κάτι επίπεδο και περπατήσιμο. Το Πάνω Κουφονήσι είναι 4 τ.χλμ. και σχεδόν εντελώς επίπεδο· φτάνεις σε κάθε παραλία με τα πόδια ή με ποδήλατο.",
  "Θέλεις λίγη ζωή μετά το φαγητό. Βαθμολογείται 4.0 στη νυχτερινή ζωή, τεράστιο για το σύμπλεγμα — μερικά κανονικά μπαρ στη Χώρα και νεανικός κόσμος.",
  "Θέλεις την εκδρομή στο Κάτω Κουφονήσι, το ακατοίκητο νησί απέναντι, με το Νερό και τον Δέτη άδεια.",
  "Πηγαίνεις Ιούνιο ή Σεπτέμβριο, οπότε έχεις τις παραλίες χωρίς τον κόσμο."],
 ["Θέλεις το φαγητό. Μισή ντουζίνα ταβέρνες στη Χώρα ξεπερνούν κατά πολύ το μέγεθος του νησιού — το Deli είναι στον Greek Gastronomy Guide και η φάβα αξίζει το πλοίο από μόνη της.",
  "Θέλεις ησυχία τον Αύγουστο, που τα Κουφονήσια δεν έχουν. Η Σχοινούσα έχει ελληνικές οικογένειες, όχι σκηνή.",
  "Σου αρέσει η ιδέα του πιο ξηρού τόπου της Ελλάδας — το λένε Νησί του Ήλιου και δέχεται λιγότερη βροχή από οπουδήποτε αλλού.",
  "Θέλεις κάθε παραλία σε 35 λεπτά με τα πόδια από ένα χωριό, σε ήπιο έδαφος, με το φυσικό λιμάνι της Μερσίνης να λειτουργεί και ως παραλία.",
  "Ταξιδεύεις με παιδιά και θέλεις ρηχά, απάνεμα νερά — ιδίως τον Αλμυρό."], el=True)
+ """
<h4>Οι παραλίες, ειλικρινά</h4>
<p>Τα Κουφονήσια κερδίζουν και δεν είναι κοντά. 5.0 έναντι 4.5, και η διαφορά είναι πραγματική: το Πόρι είναι μια κανονική «μεγάλη» παραλία στον βορρά, και η σειρά των όρμων στην ανατολική ακτή — Φοίνικας, Φανός, Ιταλίδα, Πλάτια Πούντα — σου δίνει τέσσερα-πέντε διαφορετικά μπάνια μέσα σε μία ώρα περπάτημα. Η Πισίνα είναι από τα πράγματα για τα οποία οργανώνεις ταξίδι.</p>
<p>Οι παραλίες της Σχοινούσας είναι εξαιρετικές και σε οποιοδήποτε άλλο νησί θα ήταν ο τίτλος. Το Τσιγκούρι είναι πέντε λεπτά από το λιμάνι, η Ψιλή Άμμος η μακριά αμμουδιά στον βορρά, και ο Αλμυρός τα πιο ρηχά και απάνεμα νερά του συμπλέγματος. Αυτό που λείπει στη Σχοινούσα είναι ένα Πόρι. Αυτό που έχει είναι ότι κάθε παραλία φτάνεται εύκολα — που για οικογένεια ή για μια εβδομάδα χαλάρωσης μετράει περισσότερο.</p>

<h4>Πώς είναι πραγματικά κάθε νησί</h4>
<p>Τα Κουφονήσια είναι πιο πολυσύχναστα από όσο περιμένει κάποιος που ήρθε για ερημιά. Η Χώρα έχει μπαρ που μένουν ανοιχτά, ψαράδικο στόλο που δουλεύει, σκάφη να μπαινοβγαίνουν όλη μέρα. Υπέροχο νησί με αληθινή ζωή, αλλά το πρώτο δεκαπενθήμερο του Αυγούστου μοιάζει πιο κοντά σε μια μικρή Πάρο παρά στους γείτονές του. Το επίπεδο έδαφος είναι δώρο, και το Κάτω Κουφονήσι δέκα λεπτά μακριά σου δίνει πάντα διαφυγή.</p>
<p>Η Σχοινούσα είναι ένας χαμηλός λόφος με ένα χωριό στην κορυφή και ένα λιμάνι κάτω. Δεν συμβαίνει τίποτα, σκόπιμα. Η χαρά είναι η κατάβαση σε μια παραλία το πρωί, η ανάβαση το απόγευμα, και μετά ένα δείπνο εντυπωσιακά καλό για τόσο μικρό μέρος. Η Χώρα το βράδυ είναι λίγα φωτισμένα τραπέζια — που είναι είτε αυτό που ήρθες να βρεις είτε πρόβλημα.</p>

<h4>Πρόσβαση και κόστος</h4>
<p>Και τα δύο είναι στη γραμμή του Express Skopelitis από τη Νάξο, και τα δύο έχουν και απευθείας πλοία από Πειραιά (6–9 ώρες). Τα Κουφονήσια έχουν καλύτερες συνδέσεις — είναι η πιο πολυσύχναστη στάση της γραμμής. Η Σχοινούσα είναι πιο σύντομο πέρασμα από τη Νάξο αλλά με λιγότερα δρομολόγια.</p>
<p>Τα Κουφονήσια είναι ακριβότερα, και τον Αύγουστο η διαφορά δεν είναι μικρή: 3.0 στην προσιτότητα έναντι 3.8 της Σχοινούσας, που σημαίνει αισθητά ακριβότερα δωμάτια και κρατήσεις μήνες πριν. Εκτός σεζόν η διαφορά σχεδόν εξαφανίζεται.</p>

<h4>Η ειλικρινής ετυμηγορία</h4>
<p>Αν πρόκειται να δεις ένα μόνο νησί των Μικρών Κυκλάδων στη ζωή σου, πήγαινε στα Κουφονήσια — οι παραλίες είναι καλύτερες, και το να αποφεύγεις κάτι επειδή είναι δημοφιλές είναι συνήθως κακή συμβουλή. Αλλά πήγαινε Ιούνιο ή Σεπτέμβριο. Τον Αύγουστο τα Κουφονήσια είναι θύμα των φωτογραφιών τους και η Σχοινούσα είναι οι καλύτερες διακοπές: φθηνότερη, πιο άδεια, με το καλύτερο φαγητό του συμπλέγματος. Η πραγματική απάντηση, αν έχεις πέντε μέρες, είναι και τα δύο — απέχουν ενενήντα λεπτά με το ίδιο καράβι.</p>
""")}

# ===================================================== iraklia vs koufonisia
V['iraklia__koufonisia'] = {'en': (
"<p><strong>The short answer:</strong> These are the two ends of the same ferry line and they could not be less alike. Koufonisia scores 4.0 with a perfect 5.0 for beaches and 4.0 for nightlife; Iraklia scores 3.2, with 1.5 for nightlife — the lowest figure we give any island with a hotel on it. Iraklia has 140 residents, one road, a very good cave and almost nothing else. If you want the famous Cycladic swimming, take Koufonisia. If your actual goal is to be somewhere where nothing can possibly be asked of you, Iraklia is the more honest choice, and it is the cheapest island in the archipelago.</p>"
+ cols('Koufonisia', 'Iraklia',
 ["You want the beaches this archipelago is famous for — Pori, Italida, Fanos, and the Pisina rock pool.",
  "You want to be able to eat and drink somewhere after dark without it being an event.",
  "You want good ferry connections; Koufonisia is the busiest stop on the Small Cyclades line.",
  "You want the Kato Koufonisi day trip across the channel.",
  "You are travelling with someone who would find Iraklia boring, and would be right."],
 ["You want the emptiest inhabited island in the group — 140 people, and in the shoulder season you will meet most of them.",
  "You want the Cave of Agios Ioannis, a large stalactite cave up the mountain, which is genuinely worth the walk and is the one real 'sight' in the Small Cyclades.",
  "You want the cheapest island here by a clear margin — it scores 4.3 for affordability against Koufonisia's 3.0.",
  "You are happy with one very good beach (Livadi) rather than six.",
  "You want to see what the Cyclades were like before anyone came, which on Iraklia is not a marketing line."])
+ """
<h4>Beaches: 5.0 against 4.2</h4>
<p>Koufonisia is one of only a handful of islands we score 5.0 for beaches, and it earns it through variety as much as quality — Pori's big sandy bay in the north, then Finikas, Fanos, Italida and Platia Pounta strung along the east coast, then the Pisina rock pool, then the empty beaches of Kato Koufonisi across the water. You can swim somewhere different every day for a week.</p>
<p>Iraklia has Livadi, and Livadi is lovely — a broad sandy bay a twenty-minute walk from the port at Agios Georgios, shallow and usually almost empty. After that the options thin out fast: Alimia is a beautiful cove but needs a boat, Papas is small and rocky. One excellent beach and a couple of alternatives is the honest summary. If beaches are the reason you are going to the Small Cyclades, that matters.</p>

<h4>The cave, and why it counts</h4>
<p>Iraklia has the one thing none of its neighbours can offer: the Cave of Agios Ioannis, a serious stalactite cave an hour and a half up the mountain from Panagia village, with a chapel at the mouth and a feast day on 28 August that draws the whole island. It is a proper expedition — take a torch, take water — and it gives a day on Iraklia a shape that a day on the other Lesser Cyclades does not have. Koufonisia, for all its water, has no equivalent; its cultural score is 2.0 and that is generous.</p>

<h4>Money</h4>
<p>Iraklia is the cheapest island in this comparison set and one of the cheapest in the Cyclades — 4.3 for affordability against Koufonisia's 3.0. In August that gap is stark: Koufonisia rooms are booked months ahead at prices that would embarrass Naxos, while Iraklia stays quietly affordable because demand never arrives. A week for two on Iraklia can be done for well under €600 including ferries.</p>

<h4>The honest verdict</h4>
<p>Koufonisia is the better island and Iraklia is the better idea, and which of those sentences matters more is entirely about you. Almost everyone should choose Koufonisia: the swimming is exceptional, the logistics are easier, and there is enough life to keep two people happy for four days. Choose Iraklia only if you know, from experience rather than aspiration, that you are the kind of traveller who is happy with one beach, one taverna and a long walk to a cave — because on Iraklia there is no fallback if you are wrong about that. The obvious move for anyone with a week is Koufonisia first, Iraklia second, in that order, so that the quiet feels earned rather than imposed.</p>
"""),
'el': (
"<p><strong>Η σύντομη απάντηση:</strong> Είναι τα δύο άκρα της ίδιας ακτοπλοϊκής γραμμής και δεν θα μπορούσαν να διαφέρουν περισσότερο. Τα Κουφονήσια βαθμολογούνται 4.0 με άριστα 5.0 στις παραλίες και 4.0 στη νυχτερινή ζωή· η Ηρακλειά 3.2, με 1.5 στη νυχτερινή ζωή — το χαμηλότερο νούμερο που δίνουμε σε νησί που έχει ξενοδοχείο. Η Ηρακλειά έχει 140 κατοίκους, έναν δρόμο, ένα πολύ καλό σπήλαιο και σχεδόν τίποτα άλλο. Για το διάσημο κυκλαδίτικο μπάνιο, Κουφονήσια. Αν ο πραγματικός στόχος είναι να μην μπορεί να σου ζητηθεί τίποτα, η Ηρακλειά είναι η πιο ειλικρινής επιλογή — και το φθηνότερο νησί του συμπλέγματος.</p>"
+ cols('τα Κουφονήσια', 'την Ηρακλειά',
 ["Θέλεις τις παραλίες για τις οποίες φημίζεται το σύμπλεγμα — Πόρι, Ιταλίδα, Φανός, Πισίνα.",
  "Θέλεις να μπορείς να φας και να πιεις κάπου αφού σκοτεινιάσει χωρίς να είναι γεγονός.",
  "Θέλεις καλές συνδέσεις· τα Κουφονήσια είναι η πιο πολυσύχναστη στάση της γραμμής.",
  "Θέλεις την εκδρομή στο Κάτω Κουφονήσι.",
  "Ταξιδεύεις με κάποιον που θα έβρισκε την Ηρακλειά βαρετή — και θα είχε δίκιο."],
 ["Θέλεις το πιο άδειο κατοικημένο νησί της ομάδας — 140 κάτοικοι, και εκτός αιχμής θα γνωρίσεις τους περισσότερους.",
  "Θέλεις το Σπήλαιο του Αγίου Ιωάννη, μεγάλο σπήλαιο με σταλακτίτες, που αξίζει πραγματικά την ανάβαση και είναι το μόνο κανονικό «αξιοθέατο» των Μικρών Κυκλάδων.",
  "Θέλεις το φθηνότερο νησί εδώ με σαφή διαφορά — 4.3 στην προσιτότητα έναντι 3.0 των Κουφονησίων.",
  "Σου αρκεί μία πολύ καλή παραλία (Λιβάδι) αντί για έξι.",
  "Θέλεις να δεις πώς ήταν οι Κυκλάδες πριν έρθει κανείς — που στην Ηρακλειά δεν είναι διαφημιστική φράση."], el=True)
+ """
<h4>Παραλίες: 5.0 έναντι 4.2</h4>
<p>Τα Κουφονήσια είναι από τα λίγα νησιά που βαθμολογούμε 5.0 στις παραλίες, και το κερδίζουν με ποικιλία όσο και με ποιότητα — το Πόρι στον βορρά, μετά Φοίνικας, Φανός, Ιταλίδα και Πλάτια Πούντα στην ανατολική ακτή, μετά η Πισίνα, μετά οι άδειες παραλίες του Κάτω Κουφονησίου. Μπορείς να κολυμπάς αλλού κάθε μέρα για μια εβδομάδα.</p>
<p>Η Ηρακλειά έχει το Λιβάδι, και το Λιβάδι είναι υπέροχο — πλατιά αμμουδιά είκοσι λεπτά από το λιμάνι του Αγίου Γεωργίου, ρηχή και συνήθως σχεδόν άδεια. Μετά οι επιλογές λιγοστεύουν γρήγορα: η Αλιμιά είναι όμορφη αλλά θέλει βάρκα, ο Πάπας μικρός και βραχώδης. Μία εξαιρετική παραλία και δύο εναλλακτικές είναι η ειλικρινής περιγραφή.</p>

<h4>Το σπήλαιο, και γιατί μετράει</h4>
<p>Η Ηρακλειά έχει το ένα πράγμα που δεν έχει κανένας γείτονάς της: το Σπήλαιο του Αγίου Ιωάννη, σοβαρό σπήλαιο με σταλακτίτες μιάμιση ώρα ανηφόρα από την Παναγιά, με εκκλησάκι στο στόμιο και πανηγύρι στις 28 Αυγούστου. Είναι κανονική εξόρμηση — φακός, νερό — και δίνει στη μέρα ένα σχήμα που δεν έχει η μέρα στα άλλα μικρά νησιά. Τα Κουφονήσια, με όλο το νερό τους, δεν έχουν αντίστοιχο· η πολιτιστική τους βαθμολογία είναι 2.0 και είναι γενναιόδωρη.</p>

<h4>Χρήματα</h4>
<p>Η Ηρακλειά είναι το φθηνότερο νησί της σύγκρισης και από τα φθηνότερα των Κυκλάδων — 4.3 έναντι 3.0. Τον Αύγουστο η διαφορά είναι κραυγαλέα: τα δωμάτια στα Κουφονήσια κλείνονται μήνες πριν σε τιμές που θα ντρόπιαζαν τη Νάξο, ενώ η Ηρακλειά μένει ήσυχα προσιτή γιατί η ζήτηση δεν φτάνει ποτέ. Μια εβδομάδα για δύο στην Ηρακλειά γίνεται κάτω από 600€ με τα πλοία.</p>

<h4>Η ειλικρινής ετυμηγορία</h4>
<p>Τα Κουφονήσια είναι το καλύτερο νησί και η Ηρακλειά η καλύτερη ιδέα, και ποια από τις δύο προτάσεις μετράει περισσότερο εξαρτάται απόλυτα από σένα. Σχεδόν όλοι πρέπει να διαλέξουν Κουφονήσια: το μπάνιο είναι εξαιρετικό, η πρόσβαση ευκολότερη, και υπάρχει αρκετή ζωή για τέσσερις μέρες. Διάλεξε Ηρακλειά μόνο αν ξέρεις, από εμπειρία και όχι από φιλοδοξία, ότι είσαι ταξιδιώτης που ευχαριστείται με μία παραλία, μία ταβέρνα και μια μακριά ανάβαση σε σπήλαιο — γιατί στην Ηρακλειά δεν υπάρχει εναλλακτική αν κάνεις λάθος. Η προφανής κίνηση για μια εβδομάδα: πρώτα Κουφονήσια, μετά Ηρακλειά, με αυτή τη σειρά.</p>
""")}

# ===================================================== iraklia vs schoinoussa
V['iraklia__schoinoussa'] = {'en': (
"<p><strong>The short answer:</strong> Schoinoussa, for almost everyone. It scores 3.4 against Iraklia's 3.2, but the interesting gap is not the total — it is that Schoinoussa has better beaches (4.5 to 4.2), far better food, and enough infrastructure that a week there is comfortable rather than a test of character. Iraklia's case rests on two things: it is cheaper (4.3 to 3.8, the best value in the archipelago) and it is emptier, with 140 residents against 227. Both are quiet. Only one of them has dinner.</p>"
+ cols('Schoinoussa', 'Iraklia',
 ["You want to eat well. This is the whole argument. Half a dozen tavernas in the Chora, one of them in the Greek Gastronomy Guide, on an island of 227 people.",
  "You want several easy beaches rather than one good one — Tsigouri, Almyros, Psili Ammos and Kato Nisi are all within a 35-minute walk.",
  "You want the slightly better ferry position; Schoinoussa sits mid-chain and hops easily to Koufonisia, Iraklia and Naxos.",
  "You are with family and want shallow, sheltered swimming and a village with a shop and a doctor.",
  "You like the idea of the driest island in Greece — the Island of the Sun."],
 ["You want the emptiest option, full stop. 140 people, one road, and a genuine sense that the season has not really reached here.",
  "You want the Cave of Agios Ioannis — the one substantial sight in the Small Cyclades, an hour and a half uphill from Panagia.",
  "You want the cheapest week available in the Cyclades. Iraklia is the best value island in this whole group.",
  "You are content with Livadi, which is a lovely broad sandy bay, and not bothered that the alternatives are thin.",
  "You are coming for one or two nights as a stop on a longer Small Cyclades chain, rather than as a destination."])
+ """
<h4>Why the food difference is the real story</h4>
<p>It sounds like a small thing and it is not. On islands this size, the evening is the day's event, and Schoinoussa's Chora delivers a genuinely good one — Deli with the best view on the island and a fava worth remembering, Harama for grilled octopus, and several more besides. The fact that an island of 227 people supports this is the single most surprising thing about the Small Cyclades.</p>
<p>Iraklia has a handful of simple tavernas at Agios Georgios and in Panagia, and they are fine — fresh, cheap, unfussy. But if you are staying five nights, you will eat the same meal several times, and that is worth knowing in advance rather than discovering on night three.</p>

<h4>Beaches</h4>
<p>Schoinoussa wins on both quality and count. Tsigouri is a five-minute walk from the port and is wide, sandy and shallow; Almyros is the most sheltered water in the group and the safest for small children; Psili Ammos is the long sandy one in the north; Kato Nisi, also called Panagia, is the sunset beach on the west coast. Four proper beaches, all walkable from one village.</p>
<p>Iraklia has Livadi and it is a genuinely fine beach — broad, sandy, shallow, and usually near-empty even in August, which is a rare combination. Beyond it, Alimia needs a boat and Papas is small. If your holiday is essentially 'walk to a beach, swim, walk back', Iraklia does that perfectly well with one beach. If you want variety, it does not.</p>

<h4>The honest verdict</h4>
<p>Choose Schoinoussa unless you have a specific reason not to. It is better on beaches, dramatically better on food, marginally better connected, and it costs very little more. Iraklia is the right answer in exactly two situations: you are hopping the whole chain and want a night at the quiet end, or emptiness and cost are your two governing criteria and you genuinely do not mind eating the same dinner four times. There is also a third, better answer — do both. They are adjacent stops on the Express Skopelitis, twenty minutes apart, and two nights on Iraklia followed by three on Schoinoussa is the most complete version of the Small Cyclades that a week allows.</p>
"""),
'el': (
"<p><strong>Η σύντομη απάντηση:</strong> Η Σχοινούσα, για σχεδόν όλους. Βαθμολογείται 3.4 έναντι 3.2 της Ηρακλειάς, αλλά το ενδιαφέρον δεν είναι το σύνολο — είναι ότι η Σχοινούσα έχει καλύτερες παραλίες (4.5 έναντι 4.2), πολύ καλύτερο φαγητό, και αρκετές υποδομές ώστε μια εβδομάδα να είναι άνετη και όχι δοκιμασία χαρακτήρα. Τα επιχειρήματα της Ηρακλειάς είναι δύο: είναι φθηνότερη (4.3 έναντι 3.8, η καλύτερη σχέση αξίας του συμπλέγματος) και πιο άδεια, με 140 κατοίκους έναντι 227. Και οι δύο είναι ήσυχες. Μόνο η μία έχει δείπνο.</p>"
+ cols('τη Σχοινούσα', 'την Ηρακλειά',
 ["Θέλεις να φας καλά. Αυτό είναι όλο το επιχείρημα. Μισή ντουζίνα ταβέρνες στη Χώρα, μία στον Greek Gastronomy Guide, σε νησί 227 κατοίκων.",
  "Θέλεις πολλές εύκολες παραλίες αντί για μία καλή — Τσιγκούρι, Αλμυρός, Ψιλή Άμμος και Κάτω Νησί, όλες σε 35 λεπτά με τα πόδια.",
  "Θέλεις ελαφρώς καλύτερη ακτοπλοϊκή θέση· η Σχοινούσα είναι στο μέσο της γραμμής και πηδάει εύκολα σε Κουφονήσια, Ηρακλειά και Νάξο.",
  "Είσαι με οικογένεια και θέλεις ρηχά, απάνεμα νερά και χωριό με μαγαζί και γιατρό.",
  "Σου αρέσει η ιδέα του πιο ξηρού νησιού της Ελλάδας — του Νησιού του Ήλιου."],
 ["Θέλεις την πιο άδεια επιλογή, τελεία. 140 κάτοικοι, ένας δρόμος, και η αίσθηση ότι η σεζόν δεν έφτασε ποτέ εδώ.",
  "Θέλεις το Σπήλαιο του Αγίου Ιωάννη — το μόνο ουσιαστικό αξιοθέατο των Μικρών Κυκλάδων, μιάμιση ώρα ανηφόρα από την Παναγιά.",
  "Θέλεις τη φθηνότερη εβδομάδα στις Κυκλάδες. Η Ηρακλειά είναι η καλύτερη αξία της ομάδας.",
  "Σου αρκεί το Λιβάδι, μια υπέροχη πλατιά αμμουδιά, και δεν σε πειράζει ότι οι εναλλακτικές είναι λίγες.",
  "Έρχεσαι για μία-δύο νύχτες ως στάση σε μια μεγαλύτερη διαδρομή, όχι ως προορισμό."], el=True)
+ """
<h4>Γιατί η διαφορά στο φαγητό είναι η ουσία</h4>
<p>Ακούγεται μικρό και δεν είναι. Σε νησιά αυτού του μεγέθους το βράδυ είναι το γεγονός της ημέρας, και η Χώρα της Σχοινούσας το παραδίδει πραγματικά καλά — το Deli με την ομορφότερη θέα και μια φάβα που θυμάσαι, η Χάραμα για χταπόδι σχάρας, και άλλες ακόμη. Το ότι ένα νησί 227 κατοίκων συντηρεί αυτό είναι το πιο εκπληκτικό στοιχείο των Μικρών Κυκλάδων.</p>
<p>Η Ηρακλειά έχει μερικές απλές ταβέρνες στον Άγιο Γεώργιο και στην Παναγιά, και είναι καλές — φρέσκες, φθηνές, χωρίς επιτήδευση. Αν όμως μείνεις πέντε νύχτες, θα φας το ίδιο γεύμα αρκετές φορές, και καλύτερα να το ξέρεις πριν παρά να το ανακαλύψεις την τρίτη βραδιά.</p>

<h4>Παραλίες</h4>
<p>Η Σχοινούσα κερδίζει σε ποιότητα και σε πλήθος. Το Τσιγκούρι είναι πέντε λεπτά από το λιμάνι, πλατύ, αμμώδες και ρηχό· ο Αλμυρός τα πιο απάνεμα νερά της ομάδας και το ασφαλέστερο για μικρά παιδιά· η Ψιλή Άμμος η μακριά αμμουδιά του βορρά· το Κάτω Νησί (Παναγιά) η παραλία του ηλιοβασιλέματος στα δυτικά. Τέσσερις κανονικές παραλίες, όλες με τα πόδια από ένα χωριό.</p>
<p>Η Ηρακλειά έχει το Λιβάδι και είναι πραγματικά καλή παραλία — πλατιά, αμμώδης, ρηχή, και συνήθως σχεδόν άδεια ακόμη και τον Αύγουστο, σπάνιος συνδυασμός. Παραπέρα, η Αλιμιά θέλει βάρκα και ο Πάπας είναι μικρός. Αν οι διακοπές σου είναι «περπάτα σε μια παραλία, κολύμπα, γύρνα», η Ηρακλειά τα κάνει μια χαρά με μία παραλία. Αν θέλεις ποικιλία, όχι.</p>

<h4>Η ειλικρινής ετυμηγορία</h4>
<p>Διάλεξε Σχοινούσα εκτός αν έχεις συγκεκριμένο λόγο να μην το κάνεις. Καλύτερη στις παραλίες, δραματικά καλύτερη στο φαγητό, οριακά καλύτερα συνδεδεμένη, και κοστίζει ελάχιστα περισσότερο. Η Ηρακλειά είναι η σωστή απάντηση σε δύο ακριβώς περιπτώσεις: κάνεις όλη τη γραμμή και θέλεις μια νύχτα στο ήσυχο άκρο, ή η ερημιά και το κόστος είναι τα δύο κριτήρια που σε ορίζουν και πραγματικά δεν σε πειράζει να φας το ίδιο δείπνο τέσσερις φορές. Υπάρχει και τρίτη, καλύτερη απάντηση — και τα δύο. Είναι γειτονικές στάσεις του Express Skopelitis, είκοσι λεπτά μακριά, και δύο νύχτες Ηρακλειά και τρεις Σχοινούσα είναι η πληρέστερη εκδοχή των Μικρών Κυκλάδων που επιτρέπει μια εβδομάδα.</p>
""")}

# ===================================================== donousa vs koufonisia
V['donousa__koufonisia'] = {'en': (
"<p><strong>The short answer:</strong> Koufonisia on quality, Donousa on isolation, and the gap is wider than the scores suggest — 4.0 against 3.4, with Koufonisia taking beaches 5.0 to 4.5 and nightlife 4.0 to 2.5. What Donousa has that Koufonisia has entirely lost is remoteness: it sits at the far end of the chain toward Amorgos, sees the fewest boats of any Small Cyclades island (access 2.2, the worst here), and still carries the backpacker culture it acquired in the 1970s. Koufonisia is where the Small Cyclades went mainstream. Donousa is where they did not.</p>"
+ cols('Koufonisia', 'Donousa',
 ["You want the best swimming in the archipelago — Pori, Italida, Fanos and the Pisina rock pool, all within walking distance of one another.",
  "You want somewhere flat enough to cycle and small enough to need nothing else.",
  "You want a bar to go to. Nightlife 4.0 against Donousa's 2.5 is the largest single gap between these two islands.",
  "You want reliable ferries — Koufonisia is the busiest stop on the line and the easiest to build a trip around.",
  "You want the Kato Koufonisi day trip."],
 ["You want the hardest of these islands to reach, and you consider that a feature. Access 2.2 is the lowest score in the group.",
  "You want to hike. Donousa has the best marked trail network in the Small Cyclades — Kalotaritissa, Mersini, the walk to the Fokospilia cave.",
  "You want Kedros: a long dune-backed beach three kilometres from the port, with a free-camping tradition and a reputation that goes back fifty years.",
  "You want the alternative crowd rather than the summer crowd — solo travellers, returnees, people reading actual books.",
  "You are prepared for genuinely limited infrastructure: few rooms, fewer tavernas, a shop with gaps on the shelves."])
+ """
<h4>How different they really are</h4>
<p>More different than any other pair in this archipelago. Koufonisia in August has day boats, a bar strip, and rooms that were gone by spring; Donousa in August has a beach with tents on it and a taverna where the owner remembers you from last year. They are ninety minutes apart on the same ferry and they belong to different decades.</p>
<p>The physical islands differ too. Koufonisia is flat, 4 km², and effectively one loop of beaches. Donousa is 13 km² of hill and cliff with a single village (Stavros) and real walking — up to Mersini, across to Kalotaritissa, out to the sea cave. If you like a landscape you have to earn, Donousa has one and Koufonisia does not.</p>

<h4>Beaches</h4>
<p>Koufonisia takes this decisively. Pori alone would win it, and then there is the whole east-coast run and the rock pool. Nothing on Donousa matches Italida for colour or Pori for scale.</p>
<p>But Kedros deserves its reputation. It is a long, sandy, dune-backed bay that feels far from anywhere, and the swimming is excellent. Livadi and Mersini are quieter alternatives, and there are coves along the coast you can only reach on foot. Four good beaches against Koufonisia's eight or nine, and none with a beach bar.</p>

<h4>The honest verdict</h4>
<p>Koufonisia is the better island by most measures anyone would use, and for a first trip to the Small Cyclades it is the obvious answer. Donousa is for a specific person: someone who has already done a Cycladic island or two, wants to be genuinely out of reach, is happy walking for their swimming, and treats the shortage of restaurants as part of the appeal rather than a compromise. If that is not you, Donousa will feel like Koufonisia with the good parts removed. If it is you, Koufonisia will feel like a place that used to be what you came for. Both are true; pick the one that describes you.</p>
"""),
'el': (
"<p><strong>Η σύντομη απάντηση:</strong> Κουφονήσια στην ποιότητα, Δονούσα στην απομόνωση, και η διαφορά είναι μεγαλύτερη από όσο δείχνουν οι βαθμοί — 4.0 έναντι 3.4, με τα Κουφονήσια να παίρνουν τις παραλίες 5.0 έναντι 4.5 και τη νυχτερινή ζωή 4.0 έναντι 2.5. Αυτό που έχει η Δονούσα και έχουν χάσει εντελώς τα Κουφονήσια είναι η απομόνωση: βρίσκεται στο άκρο της γραμμής προς Αμοργό, βλέπει τα λιγότερα πλοία από κάθε νησί των Μικρών Κυκλάδων (πρόσβαση 2.2, η χειρότερη εδώ), και κρατά ακόμη την κουλτούρα των backpackers που απέκτησε στη δεκαετία του '70. Τα Κουφονήσια είναι εκεί όπου οι Μικρές Κυκλάδες έγιναν mainstream. Η Δονούσα εκεί όπου δεν έγιναν.</p>"
+ cols('τα Κουφονήσια', 'τη Δονούσα',
 ["Θέλεις το καλύτερο μπάνιο του συμπλέγματος — Πόρι, Ιταλίδα, Φανός και Πισίνα, όλα σε απόσταση περπατήματος μεταξύ τους.",
  "Θέλεις κάτι αρκετά επίπεδο για ποδήλατο και αρκετά μικρό για να μη χρειάζεσαι τίποτα άλλο.",
  "Θέλεις ένα μπαρ να πας. Το 4.0 έναντι 2.5 στη νυχτερινή ζωή είναι η μεγαλύτερη διαφορά των δύο νησιών.",
  "Θέλεις αξιόπιστα πλοία — τα Κουφονήσια είναι η πιο πολυσύχναστη στάση της γραμμής.",
  "Θέλεις την εκδρομή στο Κάτω Κουφονήσι."],
 ["Θέλεις το δυσκολότερο νησί εδώ στην πρόσβαση, και το θεωρείς πλεονέκτημα. Το 2.2 είναι η χαμηλότερη βαθμολογία της ομάδας.",
  "Θέλεις πεζοπορία. Η Δονούσα έχει το καλύτερο δίκτυο σημαδεμένων μονοπατιών των Μικρών Κυκλάδων — Καλοταρίτισσα, Μερσίνη, η διαδρομή στο σπήλαιο Φωκόσπηλια.",
  "Θέλεις τον Κέδρο: μακριά αμμουδιά με αμμόλοφους τρία χιλιόμετρα από το λιμάνι, με παράδοση ελεύθερου κάμπινγκ πενήντα ετών.",
  "Θέλεις τον εναλλακτικό κόσμο και όχι τον κόσμο του καλοκαιριού — μοναχικοί ταξιδιώτες, επαναλαμβανόμενοι επισκέπτες, άνθρωποι που διαβάζουν όντως βιβλία.",
  "Είσαι έτοιμος για πραγματικά περιορισμένες υποδομές: λίγα δωμάτια, λιγότερες ταβέρνες, μαγαζί με κενά στα ράφια."], el=True)
+ """
<h4>Πόσο διαφέρουν πραγματικά</h4>
<p>Περισσότερο από κάθε άλλο ζευγάρι του συμπλέγματος. Τα Κουζονήσια τον Αύγουστο έχουν ημερόπλοια, σειρά μπαρ και δωμάτια που εξαφανίστηκαν την άνοιξη· η Δονούσα τον Αύγουστο έχει μια παραλία με σκηνές και μια ταβέρνα όπου ο ιδιοκτήτης σε θυμάται από πέρσι. Απέχουν ενενήντα λεπτά με το ίδιο καράβι και ανήκουν σε διαφορετικές δεκαετίες.</p>
<p>Διαφέρουν και φυσικά. Τα Κουφονήσια είναι επίπεδα, 4 τ.χλμ., πρακτικά ένας κύκλος παραλιών. Η Δονούσα είναι 13 τ.χλμ. λόφου και βράχου με ένα χωριό (Σταυρός) και κανονικό περπάτημα — πάνω στη Μερσίνη, απέναντι στην Καλοταρίτισσα, ως τη θαλάσσια σπηλιά. Αν σου αρέσει τοπίο που πρέπει να κερδίσεις, η Δονούσα έχει, τα Κουφονήσια όχι.</p>

<h4>Παραλίες</h4>
<p>Τα Κουφονήσια κερδίζουν καθαρά. Μόνο το Πόρι θα αρκούσε, και μετά υπάρχει όλη η ανατολική ακτή και η Πισίνα. Τίποτα στη Δονούσα δεν φτάνει την Ιταλίδα στο χρώμα ή το Πόρι στην έκταση.</p>
<p>Ο Κέδρος όμως αξίζει τη φήμη του. Μακριά αμμουδιά με αμμόλοφους που μοιάζει μακριά από τα πάντα, και το μπάνιο εξαιρετικό. Το Λιβάδι και η Μερσίνη είναι πιο ήσυχες εναλλακτικές, και υπάρχουν όρμοι που φτάνεις μόνο με τα πόδια. Τέσσερις καλές παραλίες έναντι οκτώ-εννέα, και καμία με beach bar.</p>

<h4>Η ειλικρινής ετυμηγορία</h4>
<p>Τα Κουφονήσια είναι το καλύτερο νησί με τα περισσότερα κριτήρια που θα χρησιμοποιούσε κανείς, και για πρώτο ταξίδι στις Μικρές Κυκλάδες είναι η προφανής απάντηση. Η Δονούσα είναι για συγκεκριμένο άνθρωπο: κάποιον που έχει κάνει ήδη ένα-δύο κυκλαδίτικα νησιά, θέλει να είναι πραγματικά απρόσιτος, χαίρεται να περπατά για το μπάνιο του, και θεωρεί την έλλειψη εστιατορίων μέρος της γοητείας και όχι συμβιβασμό. Αν δεν είσαι αυτός, η Δονούσα θα σου φανεί σαν Κουφονήσια χωρίς τα καλά. Αν είσαι, τα Κουφονήσια θα σου φανούν σαν μέρος που κάποτε ήταν αυτό που ήρθες να βρεις. Και τα δύο αληθεύουν· διάλεξε αυτό που σε περιγράφει.</p>
""")}

# ===================================================== donousa vs iraklia
V['donousa__iraklia'] = {'en': (
"<p><strong>The short answer:</strong> These are the two hardest Small Cyclades islands to reach — access 2.2 and 2.0, the lowest we score in the archipelago — and choosing between them is a choice between two kinds of nothing. Donousa scores 3.4, Iraklia 3.2. Donousa has the better beach (Kedros), the better walking, and a summer culture of its own. Iraklia has the one real sight in the whole chain, the Cave of Agios Ioannis, and it is cheaper than anywhere else here. If you want a week of swimming and hiking with a few other people around, Donousa. If you want to be almost alone, Iraklia.</p>"
+ cols('Donousa', 'Iraklia',
 ["You want Kedros — a long dune-backed sandy bay, the best single beach on either island, with a free-camping tradition going back to the 1970s.",
  "You want to walk. Donousa has the marked trails: Stavros to Mersini, over to Kalotaritissa, out to the Fokospilia sea cave.",
  "You want a little company. Donousa has a genuine summer scene — small, alternative, returning year after year — where Iraklia has almost none.",
  "You want more beaches to choose from: Kedros, Livadi, Mersini, plus coves reachable only on foot.",
  "You are heading on to Amorgos; Donousa is the natural stepping stone."],
 ["You want the emptiest island in the Small Cyclades. 140 residents against Donousa's 167, and it feels like a bigger difference than that.",
  "You want the Cave of Agios Ioannis, a big stalactite cave ninety minutes above Panagia village, with its feast on 28 August. It is the only proper sight in the archipelago.",
  "You want the cheapest week available — 4.3 for affordability, the best value of any island in this group.",
  "You are happy with Livadi as your beach and do not need alternatives.",
  "You want somewhere that has resisted even the alternative crowd; Iraklia has no scene of any kind."])
+ """
<h4>Two kinds of quiet</h4>
<p>The distinction matters more than the scores. Donousa's quiet is social — a small, self-selecting summer population that comes back every year, camps at Kedros, walks the trails, and knows each other by the second week. There are a few tavernas, a few bars in the loosest sense, and a rhythm to the day.</p>
<p>Iraklia's quiet is closer to absolute. One road, two settlements, 140 people, and outside the first fortnight of August you can spend a day without a conversation you did not start. Nothing is organised for you. That is either the finest thing about it or unbearable, and there is no middle position.</p>

<h4>Beaches and walking</h4>
<p>Donousa is better on both counts, and it is not particularly close. Kedros is a proper beach — long, sandy, backed by dunes, three kilometres from the port — and Livadi and Mersini give you real alternatives. The trail network is the best in the archipelago, marked and maintained, and it turns the island into something you explore rather than sit on.</p>
<p>Iraklia has Livadi, which is genuinely lovely and almost always empty, and then the cave walk, which is the best half-day in the Small Cyclades if you like that sort of thing — steep, hot, and with a real reward at the top. Alimia is beautiful but needs a boat. As a swimming island it is thinner than Donousa; as a walking island it has one outstanding route rather than a network.</p>

<h4>Getting there, and the cost</h4>
<p>Both are awkward, which is the point. Donousa sits at the far northeast of the chain toward Amorgos and sees the fewest sailings of any island here; Iraklia is the first stop out of Naxos but the boats are small and the schedule thin. Either way you are building a trip around the Express Skopelitis and accepting that a missed connection costs you a day.</p>
<p>Iraklia is the cheaper of the two — 4.3 against 3.8 — and it is the best-value island in the Small Cyclades full stop. Neither is expensive. Rooms on both are simple and cost a fraction of Koufonisia's.</p>

<h4>The honest verdict</h4>
<p>Donousa is the better island for a stay, and if you are choosing one of the two for four or five nights it should be Donousa: a better beach, better walking, and just enough of a summer culture that you are not the only person there. Iraklia is the better one or two nights — go for the cave, swim at Livadi, eat whatever the taverna has, and move on down the chain. Choosing Iraklia for a week is a decision you should only make if you have done something similar before and know you enjoyed it. The best version of this comparison is not a choice at all: they are two stops apart, and taking both — Iraklia briefly, Donousa properly — is the most honest way to see the quiet end of the Cyclades.</p>
"""),
'el': (
"<p><strong>Η σύντομη απάντηση:</strong> Είναι τα δύο δυσκολότερα νησιά των Μικρών Κυκλάδων στην πρόσβαση — 2.2 και 2.0, οι χαμηλότερες βαθμολογίες του συμπλέγματος — και η επιλογή ανάμεσά τους είναι επιλογή ανάμεσα σε δύο είδη «τίποτα». Η Δονούσα βαθμολογείται 3.4, η Ηρακλειά 3.2. Η Δονούσα έχει την καλύτερη παραλία (Κέδρος), το καλύτερο περπάτημα και δική της καλοκαιρινή κουλτούρα. Η Ηρακλειά έχει το μόνο πραγματικό αξιοθέατο όλης της γραμμής, το Σπήλαιο του Αγίου Ιωάννη, και είναι φθηνότερη από οπουδήποτε αλλού εδώ. Για μια εβδομάδα μπάνιου και πεζοπορίας με λίγο κόσμο τριγύρω, Δονούσα. Για να είσαι σχεδόν μόνος, Ηρακλειά.</p>"
+ cols('τη Δονούσα', 'την Ηρακλειά',
 ["Θέλεις τον Κέδρο — μακριά αμμουδιά με αμμόλοφους, η καλύτερη παραλία των δύο νησιών, με παράδοση ελεύθερου κάμπινγκ από τη δεκαετία του '70.",
  "Θέλεις να περπατήσεις. Η Δονούσα έχει τα σημαδεμένα μονοπάτια: Σταυρός–Μερσίνη, ως την Καλοταρίτισσα, ως τη θαλάσσια σπηλιά Φωκόσπηλια.",
  "Θέλεις λίγη συντροφιά. Η Δονούσα έχει πραγματική καλοκαιρινή σκηνή — μικρή, εναλλακτική, που επιστρέφει κάθε χρόνο — ενώ η Ηρακλειά σχεδόν καθόλου.",
  "Θέλεις περισσότερες παραλίες: Κέδρος, Λιβάδι, Μερσίνη, και όρμους που φτάνεις μόνο πεζή.",
  "Συνεχίζεις για Αμορφό· η Δονούσα είναι το φυσικό ενδιάμεσο."],
 ["Θέλεις το πιο άδειο νησί των Μικρών Κυκλάδων. 140 κάτοικοι έναντι 167, και μοιάζει μεγαλύτερη διαφορά από όσο ακούγεται.",
  "Θέλεις το Σπήλαιο του Αγίου Ιωάννη, μεγάλο σπήλαιο με σταλακτίτες ενενήντα λεπτά πάνω από την Παναγιά, με πανηγύρι στις 28 Αυγούστου. Το μόνο κανονικό αξιοθέατο του συμπλέγματος.",
  "Θέλεις τη φθηνότερη εβδομάδα — 4.3 στην προσιτότητα, η καλύτερη αξία της ομάδας.",
  "Σου αρκεί το Λιβάδι ως παραλία και δεν χρειάζεσαι εναλλακτικές.",
  "Θέλεις κάπου που αντιστάθηκε ακόμη και στον εναλλακτικό κόσμο· η Ηρακλειά δεν έχει σκηνή κανενός είδους."], el=True)
+ """
<h4>Δύο είδη ησυχίας</h4>
<p>Η διάκριση μετράει περισσότερο από τους βαθμούς. Η ησυχία της Δονούσας είναι κοινωνική — ένας μικρός, αυτοεπιλεγμένος καλοκαιρινός πληθυσμός που επιστρέφει κάθε χρόνο, κατασκηνώνει στον Κέδρο, περπατά τα μονοπάτια και γνωρίζεται μέχρι τη δεύτερη εβδομάδα. Υπάρχουν λίγες ταβέρνες, λίγα μπαρ με την ευρεία έννοια, και ρυθμός στη μέρα.</p>
<p>Η ησυχία της Ηρακλειάς είναι πιο απόλυτη. Ένας δρόμος, δύο οικισμοί, 140 άνθρωποι, και εκτός του πρώτου δεκαπενθημέρου του Αυγούστου μπορείς να περάσεις μέρα χωρίς συζήτηση που δεν ξεκίνησες εσύ. Τίποτα δεν είναι οργανωμένο για σένα. Αυτό είναι είτε το καλύτερό της είτε ανυπόφορο, και δεν υπάρχει ενδιάμεση θέση.</p>

<h4>Παραλίες και περπάτημα</h4>
<p>Η Δονούσα είναι καλύτερη και στα δύο, και όχι οριακά. Ο Κέδρος είναι κανονική παραλία — μακριά, αμμώδης, με αμμόλοφους πίσω, τρία χιλιόμετρα από το λιμάνι — και το Λιβάδι με τη Μερσίνη δίνουν πραγματικές εναλλακτικές. Το δίκτυο μονοπατιών είναι το καλύτερο του συμπλέγματος και μετατρέπει το νησί σε κάτι που εξερευνάς αντί να κάθεσαι πάνω του.</p>
<p>Η Ηρακλειά έχει το Λιβάδι, πραγματικά υπέροχο και σχεδόν πάντα άδειο, και μετά την ανάβαση στο σπήλαιο, που είναι το καλύτερο μισό της μέρας στις Μικρές Κυκλάδες αν σου αρέσουν αυτά — απότομη, ζεστή, με αληθινή ανταμοιβή στην κορυφή. Η Αλιμιά είναι όμορφη αλλά θέλει βάρκα. Ως νησί για μπάνιο είναι φτωχότερη από τη Δονούσα· ως νησί για περπάτημα έχει μία εξαιρετική διαδρομή αντί για δίκτυο.</p>

<h4>Πρόσβαση και κόστος</h4>
<p>Και τα δύο είναι δύσκολα, που είναι το νόημα. Η Δονούσα είναι στο βορειοανατολικό άκρο της γραμμής προς Αμορφό και βλέπει τα λιγότερα δρομολόγια· η Ηρακλειά είναι η πρώτη στάση από τη Νάξο αλλά τα πλοία είναι μικρά και το πρόγραμμα αραιό. Έτσι κι αλλιώς στήνεις το ταξίδι γύρω από το Express Skopelitis και αποδέχεσαι ότι μια χαμένη σύνδεση κοστίζει μια μέρα.</p>
<p>Η Ηρακλειά είναι η φθηνότερη — 4.3 έναντι 3.8 — και η καλύτερη αξία των Μικρών Κυκλάδων συνολικά. Κανένα από τα δύο δεν είναι ακριβό. Τα δωμάτια είναι απλά και κοστίζουν κλάσμα των Κουφονησίων.</p>

<h4>Η ειλικρινής ετυμηγορία</h4>
<p>Η Δονούσα είναι το καλύτερο νησί για διαμονή, και αν διαλέγεις ένα από τα δύο για τέσσερις-πέντε νύχτες, πρέπει να είναι η Δονούσα: καλύτερη παραλία, καλύτερο περπάτημα, και αρκετή καλοκαιρινή κουλτούρα ώστε να μην είσαι ο μόνος. Η Ηρακλειά είναι η καλύτερη μία-δύο νύχτες — πήγαινε για το σπήλαιο, κολύμπα στο Λιβάδι, φάε ό,τι έχει η ταβέρνα, και συνέχισε. Το να διαλέξεις Ηρακλειά για μια εβδομάδα είναι απόφαση που πρέπει να πάρεις μόνο αν έχεις κάνει κάτι παρόμοιο και ξέρεις ότι σου άρεσε. Η καλύτερη εκδοχή αυτής της σύγκρισης δεν είναι επιλογή: απέχουν δύο στάσεις, και το να πάρεις και τα δύο — Ηρακλειά σύντομα, Δονούσα κανονικά — είναι ο πιο ειλικρινής τρόπος να δεις το ήσυχο άκρο των Κυκλάδων.</p>
""")}

# ------------------------------------------------------------------ write
P = 'vs_verdicts.json'
data = json.load(open(P, encoding='utf-8'))
before = len(data)
for k, v in V.items():
    assert k not in data, f'{k} already exists'
    data[k] = v
json.dump(data, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'✓ vs_verdicts.json: {before} → {len(data)} verdicts')
for k in V:
    print(f'   + {k}  EN {len(V[k]["en"]):,} chars · EL {len(V[k]["el"]):,} chars')
