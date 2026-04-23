/* ============================================================
   I18N — Greek/English translations for UI and island summaries
   Default language: 'en' (English). Greek users at /el/ get 'el'.
============================================================ */

// Detect language from URL path or localStorage
function detectLanguage() {
  if (window.location.pathname.startsWith('/el/') || window.location.pathname === '/el') {
    return 'el';
  }
  // Allow ?lang=el override (helpful for testing without /el/ folder)
  const params = new URLSearchParams(window.location.search);
  if (params.get('lang') === 'el') return 'el';
  return 'en';
}

const CURRENT_LANG = detectLanguage();

// UI translations
const UI_TEXT = {
  // Nav
  'nav.map': { en: 'Map', el: 'Χάρτης' },
  'nav.data': { en: 'Islands Data', el: 'Στοιχεία Νησιών' },
  'nav.compare': { en: 'Compare', el: 'Σύγκριση' },
  'nav.hopping': { en: 'Island Hopping', el: 'Νησοπορία' },
  'nav.match': { en: 'Match Me', el: 'Βρες το Νησί σου' },
  'nav.shortlist': { en: '⭐ My Shortlist', el: '⭐ Η Λίστα μου' },
  'nav.mission': { en: 'Mission', el: 'Στόχος' },

  // Hero / homepage
  'hero.title': { en: 'Find your perfect Greek island', el: 'Βρες το ιδανικό σου ελληνικό νησί' },
  'hero.sub': { en: '83 islands scored across beaches, culture, nightlife, access and price. Click any circle to explore.', el: '83 νησιά βαθμολογημένα σε παραλίες, πολιτισμό, νυχτερινή ζωή, πρόσβαση και τιμή. Πάτα οποιοδήποτε σημείο για εξερεύνηση.' },
  'hero.tagline': { en: 'The Greek Island Decision Engine', el: 'Ο οδηγός για το Ελληνικό νησί που σας ταιριάζει' },
  'hero.dismiss': { en: 'Got it', el: 'Έγινε' },
  'hero.stat.islands': { en: 'Islands', el: 'Νησιά' },
  'hero.stat.dimensions': { en: 'Score dimensions', el: 'Διαστάσεις' },
  'hero.stat.guides': { en: 'Full guides', el: 'Πλήρεις οδηγοί' },
  'hero.stat.minutes': { en: 'Minutes', el: 'Λεπτά' },

  // Help modal
  'help.btn': { en: 'How to', el: 'Οδηγίες' },
  'help.step1.title': { en: 'Explore the map', el: 'Εξερεύνησε τον χάρτη' },
  'help.step1.desc': { en: "Click any circle to open the island's full guide. Bigger circles = higher overall rating.", el: 'Πάτα σε οποιοδήποτε κυκλάκι για τον πλήρη οδηγό του νησιού. Μεγαλύτερο κυκλάκι = υψηλότερη βαθμολογία.' },
  'help.step2.title': { en: 'Filter and rank', el: 'Φιλτράρισμα και ταξινόμηση' },
  'help.step2.desc': { en: 'Use the dropdowns to filter by island group or rank by what matters to you — beaches, culture, nightlife.', el: 'Χρησιμοποίησε τα φίλτρα για να διαλέξεις νησιωτικό σύμπλεγμα ή να ταξινομήσεις κατά παραλίες, πολιτισμό, νυχτερινή ζωή.' },
  'help.step3.title': { en: 'Take the quiz', el: 'Κάνε το quiz' },
  'help.step3.desc': { en: "Not sure where to go? Answer 5 quick questions and we'll match you to your top islands.", el: 'Δεν είσαι σίγουρος; Απάντησε σε 5 γρήγορες ερωτήσεις και θα σου προτείνουμε τα κορυφαία νησιά.' },
  'help.step4.title': { en: 'Save & compare', el: 'Αποθήκευση & σύγκριση' },
  'help.step4.desc': { en: 'Star islands to your shortlist, or put two side-by-side with Compare.', el: 'Αποθήκευσε νησιά στη λίστα σου, ή σύγκρινε δύο δίπλα-δίπλα.' },
  'help.close': { en: 'Got it — let me explore', el: 'Έγινε — ας εξερευνήσω' },

  // Search/filter
  'search.placeholder': { en: '🔍  Search islands…', el: '🔍  Αναζήτηση νησιών…' },
  'filter.allgroups': { en: 'All islands', el: 'Όλα τα νησιά' },
  'filter.withairport': { en: '✈ With airport', el: '✈ Με αεροδρόμιο' },
  'filter.withoutairport': { en: 'Without airport', el: 'Χωρίς αεροδρόμιο' },
  'data.col.airport': { en: '✈ Airport ↕', el: '✈ Αεροδρόμιο ↕' },
  'tooltip.hasairport': { en: 'Airport', el: 'Αεροδρόμιο' },
  'filter.rankby': { en: 'Rank map by', el: 'Ταξινόμηση κατά' },
  'filter.overall': { en: '🏠 Overall', el: '🏠 Συνολικά' },
  'filter.beach': { en: '🏖️ Beaches', el: '🏖️ Παραλίες' },
  'filter.culture': { en: '🏛️ Culture', el: '🏛️ Πολιτισμός' },
  'filter.night': { en: '🍷 Nightlife', el: '🍷 Νυχτερινή ζωή' },
  'filter.access': { en: '🚢 Access', el: '🚢 Πρόσβαση' },
  'filter.afford': { en: '💸 Price', el: '💸 Τιμή' },
  'filter.car': { en: '🚗 Car reliance', el: '🚗 Χρησιμότητα οχήματος' },
  // Dimension labels (for radar chart, bars, columns)
  'dim.beach': { en: 'Beach', el: 'Παραλία' },
  'dim.culture': { en: 'Culture', el: 'Πολιτισμός' },
  'dim.night': { en: 'Nightlife', el: 'Νυχτερινή ζωή' },
  'dim.access': { en: 'Access', el: 'Πρόσβαση' },
  'dim.afford': { en: 'Affordability', el: 'Προσιτή τιμή' },
  'dim.car': { en: 'Car reliance', el: 'Χρησιμότητα οχήματος' },
  'dim.car.hint': { en: 'Car reliance: 1=useless, 2=moped/scooter, 5=essential', el: 'Χρησιμότητα οχήματος: 1=άχρηστη, 2=μηχανάκι, 5=απαραίτητη' },
  'car.none': { en: 'Useless', el: 'Άχρηστο' },
  'car.helpful': { en: 'Moped', el: 'Μηχανάκι' },
  'car.useful': { en: 'Useful', el: 'Χρήσιμο' },
  'car.recommended': { en: 'Very useful', el: 'Πολύ χρήσιμο' },
  'car.essential': { en: 'Essential', el: 'Απαραίτητο' },

  // Detail page buttons
  'detail.back': { en: '← Back to Map', el: '← Πίσω στον Χάρτη' },
  'detail.compare': { en: '＋ Compare', el: '＋ Σύγκριση' },
  'detail.save': { en: '☆ Save', el: '☆ Αποθήκευση' },
  'detail.saved': { en: '★ Saved', el: '★ Αποθηκεύτηκε' },
  'detail.copylink': { en: '🔗 Copy link', el: '🔗 Αντιγραφή' },
  'detail.print': { en: '🖨 Print', el: '🖨 Εκτύπωση' },
  'detail.bookferry': { en: '🚢 Book ferry tickets', el: '🚢 Κράτηση πλοίου' },
  'detail.copied': { en: '✓ Copied!', el: '✓ Αντιγράφτηκε!' },

  // Detail sidebar
  'detail.ratings': { en: 'Blueprint Ratings', el: 'Βαθμολογίες' },
  'detail.keystats': { en: 'Key Stats', el: 'Βασικά Στοιχεία' },
  'sidebar.beach': { en: 'Beach Quality', el: 'Ποιότητα Παραλιών' },
  'sidebar.culture': { en: 'Culture & History', el: 'Πολιτισμός & Ιστορία' },
  'sidebar.night': { en: 'Night Life', el: 'Νυχτερινή ζωή' },
  'sidebar.access': { en: 'Access Ease', el: 'Ευκολία Πρόσβασης' },
  'sidebar.afford': { en: 'Price Level', el: 'Κόστος' },
  'sidebar.car': { en: '🚗 Car reliance', el: '🚗 Χρησιμότητα οχήματος' },
  'tooltip.overall': { en: 'Overall', el: 'Συνολικά' },
  'tooltip.recommended': { en: 'recommended', el: 'συνιστώμενες' },
  'tooltip.click': { en: 'Click to explore →', el: 'Πάτα για εξερεύνηση →' },
  'detail.area': { en: 'Land Area:', el: 'Έκταση:' },
  'detail.population': { en: 'Population:', el: 'Πληθυσμός:' },
  'detail.group': { en: 'Group:', el: 'Ομάδα:' },
  'detail.suggestedstay': { en: 'Suggested stay:', el: 'Συνιστώμενη παραμονή:' },
  'detail.beaches': { en: 'Top Beaches', el: 'Καλύτερες Παραλίες' },
  'detail.itinerary': { en: 'Itinerary', el: 'Πρόγραμμα' },
  'detail.alldays': { en: 'All days', el: 'Όλες οι μέρες' },
  'detail.day': { en: 'Day', el: 'Ημέρα' },
  'common.km': { en: 'km', el: 'χλμ' },
  'common.mindrive': { en: 'min drive', el: 'λεπτά οδήγηση' },
  'common.sleep': { en: 'Sleep', el: 'Διανυκτέρευση' },
  'detail.editorial': { en: 'Editorial', el: 'Εκδοτική' },
  'detail.yourrating': { en: 'Your rating', el: 'Η βαθμολογία σου' },
  'detail.spec.type': { en: 'Type', el: 'Τύπος' },
  'detail.spec.length': { en: 'Length', el: 'Μήκος' },
  'detail.spec.depth': { en: 'Depth', el: 'Βάθος' },
  'detail.spec.wind': { en: 'Wind protection', el: 'Προστασία από αέρα' },
  'detail.spec.facilities': { en: 'Facilities', el: 'Υποδομές' },
  'detail.beaches.title': { en: 'Top Beaches of', el: 'Κορυφαίες Παραλίες της' },
  'detail.beaches.sub': { en: 'Ranked by overall quality — with details on sand type, depth, wind exposure and facilities.', el: 'Κατάταξη με βάση τη συνολική ποιότητα — με λεπτομέρειες για τον τύπο άμμου, το βάθος, την έκθεση στον άνεμο και τις υποδομές.' },
  'detail.yourrating': { en: 'Your rating', el: 'Η βαθμολογία σου' },
  'detail.editorial': { en: 'Editorial', el: 'Επιμελητής' },

  // Footer
  'footer.copyright': { en: '© 2026 Stergios Gousios · Aegean Blueprint', el: '© 2026 Στέργιος Γούσιος · Aegean Blueprint' },

  // Data table page
  'data.title': { en: 'Islands Database', el: 'Βάση Νησιών' },
  'data.search': { en: 'Filter islands…', el: 'Φιλτράρισμα νησιών…' },
  'data.col.island': { en: 'Island ↕', el: 'Νησί ↕' },
  'data.col.group': { en: 'Group ↕', el: 'Ομάδα ↕' },
  'data.col.rating': { en: 'Rating ↕', el: 'Βαθμός ↕' },
  'data.col.beach': { en: 'Beach ↕', el: 'Παραλίες ↕' },
  'data.col.culture': { en: 'Culture ↕', el: 'Πολιτισμός ↕' },
  'data.col.night': { en: 'Night ↕', el: 'Νύχτα ↕' },
  'data.col.access': { en: 'Access ↕', el: 'Πρόσβαση ↕' },
  'data.col.afford': { en: 'Affordability ↕', el: 'Τιμή ↕' },
  'data.col.car': { en: '🚗 Car reliance ↕', el: '🚗 Χρησιμότητα οχήματος ↕' },
  'data.col.days': { en: 'Days ↕', el: 'Μέρες ↕' },
  'data.col.area': { en: 'Area (km²) ↕', el: 'Έκταση (km²) ↕' },
  'data.col.pop': { en: 'Population ↕', el: 'Πληθυσμός ↕' },
  'data.col.scores': { en: 'Scores', el: 'Βαθμολογίες' },
  'data.showdims': { en: '📊 Detailed scores', el: '📊 Αναλυτικές βαθμολογίες' },
  'data.hidedims': { en: '📊 Hide scores', el: '📊 Απόκρυψη βαθμολογιών' },
  'data.hinttext': { en: 'See the 5 dimensions we rate each island on — beaches, culture, nightlife, access, price.', el: 'Δες τις 5 διαστάσεις που βαθμολογούμε σε κάθε νησί — παραλίες, πολιτισμός, νυχτερινή ζωή, πρόσβαση, τιμή.' },

  // Compare page
  'compare.title': { en: 'Compare Islands', el: 'Σύγκριση Νησιών' },
  'compare.intro': { en: 'Select two islands to compare side-by-side.', el: 'Επίλεξε δύο νησιά για σύγκριση.' },
  'compare.optionA': { en: '— Island A —', el: '— Νησί Α —' },
  'compare.optionB': { en: '— Island B —', el: '— Νησί Β —' },
  'compare.vs': { en: 'vs', el: 'εναντίον' },
  'compare.clear': { en: 'Clear', el: 'Καθαρισμός' },
  'compare.placeholder': { en: 'Select two islands above to start comparing.', el: 'Επίλεξε δύο νησιά παραπάνω για να αρχίσει η σύγκριση.' },

  // Hopping page
  'hopping.title': { en: '🚢 Island Hopping', el: '🚢 Νησοπορία' },
  'hopping.intro': { en: 'The most iconic Greek ferry routes — the backbone of any island-hopping trip. Hover over a line for details, click a port to open its island page.', el: 'Οι πιο εμβληματικές διαδρομές πλοίων στην Ελλάδα. Πέρνα τον κέρσορα πάνω από μια γραμμή για λεπτομέρειες, πάτα σε ένα λιμάνι για να ανοίξεις τη σελίδα του νησιού.' },
  'hopping.legend.high': { en: 'High frequency (multiple daily)', el: 'Πολλά δρομολόγια (πολλά ημερησίως)' },
  'hopping.legend.med': { en: 'Medium (1-2 per day)', el: 'Μέτρια (1-2 ημερησίως)' },
  'hopping.legend.low': { en: 'About 1/day (Skopelitis route, 6/week)', el: 'Περίπου 1/ημέρα (Σκοπελίτης, 6 φορές/εβδομάδα)' },
  'hopping.itineraries': { en: 'Suggested Itineraries', el: 'Προτεινόμενες Διαδρομές' },
  'hopping.itin.intro': { en: 'Eight curated multi-island routes — from the classic Cyclades circuit to the quiet Small Cyclades escape. Each uses real ferry connections and shows approximate nights per stop.', el: 'Δέκα επιλεγμένες διαδρομές πολλαπλών νησιών — από την κλασική διαδρομή των Κυκλάδων μέχρι την ήσυχη απόδραση στις Μικρές Κυκλάδες. Όλες χρησιμοποιούν πραγματικές συνδέσεις πλοίων.' },
  'hopping.night': { en: 'night', el: 'βράδυ' },
  'hopping.nights': { en: 'nights', el: 'βράδια' },
  'hopping.visit': { en: 'Visit:', el: 'Επισκέψου:' },

  // Match Me / Quiz
  'match.title': { en: 'Match Me', el: 'Βρες το Νησί σου' },
  'match.intro': { en: "Answer 4 quick questions and we'll recommend your top islands.", el: 'Απάντησε σε 4 γρήγορες ερωτήσεις και θα σου προτείνουμε τα κορυφαία νησιά για εσένα.' },
  'match.results.title': { en: 'Your top islands', el: 'Τα κορυφαία σου νησιά' },
  'match.results.sub': { en: 'Matched on your preferences — click any to explore', el: 'Με βάση τις προτιμήσεις σου — πάτα οποιοδήποτε για εξερεύνηση' },
  'match.retake': { en: 'Retake quiz', el: 'Επανάληψη' },
  'quiz.back': { en: 'Back', el: 'Πίσω' },
  'quiz.next': { en: 'Next →', el: 'Επόμενο →' },
  'quiz.find': { en: 'Find my islands →', el: 'Βρες τα νησιά μου →' },
  'quiz.why.top': { en: 'Top', el: 'Κορυφαία' },
  'quiz.why.strong': { en: 'Strong', el: 'Ισχυρή' },
  'quiz.why.affordable': { en: 'Very affordable', el: 'Πολύ προσιτό' },
  'quiz.why.lowcrowds': { en: 'Low crowds', el: 'Λίγος κόσμος' },
  'quiz.why.easy': { en: 'Easy to reach', el: 'Εύκολη πρόσβαση' },
  'quiz.why.overall': { en: 'Overall score', el: 'Συνολική βαθμολογία' },

  // Shortlist dimensions (in card)
  'shortlist.dim.beach': { en: 'Beach', el: 'Παραλία' },
  'shortlist.dim.culture': { en: 'Culture', el: 'Πολιτισμός' },
  'shortlist.dim.night': { en: 'Night', el: 'Νυχτερινή' },

  // Mission page
  'mission.title': { en: 'Mission', el: 'Στόχος' },
  'mission.tagline': { en: 'For travellers who want to live the holiday, not plan it.', el: 'Για ταξιδιώτες που θέλουν να ζήσουν τις διακοπές, όχι να τις σχεδιάσουν.' },
  'mission.lead1': { en: "This site is for people who don't want choices. They want the gist, without the fluff.", el: 'Αυτή η σελίδα είναι για ανθρώπους που δεν θέλουν επιλογές. Θέλουν την ουσία, χωρίς περιττά.' },
  'mission.lead2': { en: 'Greece has 83 inhabited islands and countless guides, blogs and listicles trying to cover them all. It\'s overwhelming, and most of it is shallow.', el: 'Η Ελλάδα έχει 83 κατοικημένα νησιά και αμέτρητους οδηγούς, blogs και λίστες που προσπαθούν να τα καλύψουν όλα. Είναι κουραστικό, και οι περισσότεροι είναι επιφανειακοί.' },
  'mission.lead3.before': { en: '', el: '' },
  'mission.lead3.bold': { en: 'Aegean Blueprint is made by locals who have actually travelled to the islands on the site', el: 'Το Aegean Blueprint φτιάχτηκε από ντόπιους που έχουν ταξιδέψει πραγματικά στα νησιά της σελίδας' },
  'mission.lead3.after': { en: ' — not curated from search rankings, and not stitched together by AI. Each island page gives you one clear, opinionated recommendation: what to see, where to swim, how long to stay. That\'s it.', el: ' — όχι από αποτελέσματα αναζήτησης, ούτε ραμμένο από AI. Κάθε σελίδα νησιού δίνει μία ξεκάθαρη πρόταση: τι να δεις, πού να κολυμπήσεις, πόσο να μείνεις. Τίποτα παραπάνω.' },
  'mission.point.label': { en: 'The point', el: 'Η ουσία' },
  'mission.point.text': { en: 'Pick an island. Pack a bag. Go.', el: 'Διάλεξε ένα νησί. Φτιάξε βαλίτσα. Φύγε.' },
  'mission.kicker': { en: "Planning a trip shouldn't take longer than the trip itself.", el: 'Ο σχεδιασμός ενός ταξιδιού δεν πρέπει να διαρκεί περισσότερο από το ίδιο το ταξίδι.' },
  'mission.author.role': { en: 'Founder · Athens', el: 'Δημιουργός · Αθήνα' },

  // Detail page (back button is already defined above)

  // Feedback
  'feedback.btn': { en: '💬 Feedback', el: '💬 Σχόλια' },
  'feedback.title': { en: 'Got feedback?', el: 'Θες να μας πεις κάτι;' },
  'feedback.intro': { en: 'Spotted an error? Have a suggestion? Want to recommend an island, beach, or restaurant we should add? Tell us — we read everything.', el: 'Είδες κάποιο λάθος; Έχεις πρόταση; Θέλεις να μας πεις για κάποιο νησί, παραλία ή εστιατόριο; Διαβάζουμε τα πάντα.' },
  'feedback.topic': { en: "What's this about?", el: 'Σχετικά με;' },
  'feedback.message': { en: 'Your message', el: 'Το μήνυμά σου' },
  'feedback.email': { en: 'Your email (optional — only if you want a reply)', el: 'Το email σου (προαιρετικά)' },
  'feedback.submit': { en: 'Send via email', el: 'Αποστολή με email' },
  'feedback.note': { en: 'This will open your email app with the message ready to send.', el: 'Θα ανοίξει η εφαρμογή email σου με το μήνυμα έτοιμο.' },

  // Shortlist
  'shortlist.title': { en: '⭐ My Shortlist', el: '⭐ Η Λίστα μου' },
  'shortlist.intro': { en: 'Your saved islands — stored in this browser.', el: 'Τα αποθηκευμένα σου νησιά — αποθηκευμένα σε αυτή τη συσκευή.' },
  'shortlist.empty': { en: 'No islands saved yet.', el: 'Δεν έχεις αποθηκεύσει νησιά ακόμα.' },
  'shortlist.howto': { en: 'Click the ☆ Save button on any island page to add it here.', el: 'Πάτα το ☆ Αποθήκευση σε οποιοδήποτε νησί για να το προσθέσεις εδώ.' },
  'shortlist.remove': { en: '✕ Remove', el: '✕ Αφαίρεση' },
  'shortlist.clearall': { en: 'Clear all', el: 'Καθαρισμός όλων' },

  // Common
  'common.days': { en: 'days', el: 'μέρες' },
  'common.day': { en: 'day', el: 'μέρα' },
  'common.km': { en: 'km', el: 'χλμ' },
  'common.min': { en: 'min', el: 'λεπτά' },
  'common.hr': { en: 'hr', el: 'ώρα' },
  'common.hrs': { en: 'hrs', el: 'ώρες' },
  'common.overnight': { en: 'Overnight', el: 'Διανυκτέρευση' },
  'common.driving': { en: 'driving', el: 'οδήγηση' },
};

// Greek names of islands (only for those we have)
const ISLAND_NAMES_EL = {
  'lefkada': 'Λευκάδα', 'meganisi': 'Μεγανήσι', 'ithaca': 'Ιθάκη',
  'kefalonia': 'Κεφαλονιά', 'zakynthos': 'Ζάκυνθος', 'corfu': 'Κέρκυρα',
  'kythira': 'Κύθηρα', 'elafonisos': 'Ελαφόνησος',
  'santorini': 'Σαντορίνη', 'mykonos': 'Μύκονος', 'naxos': 'Νάξος',
  'paros': 'Πάρος', 'milos': 'Μήλος', 'sifnos': 'Σίφνος',
  'folegandros': 'Φολέγανδρος', 'ios': 'Ίος', 'amorgos': 'Αμοργός',
  'iraklia': 'Ηρακλειά',
  'rhodes': 'Ρόδος', 'kos': 'Κως', 'patmos': 'Πάτμος',
  'kalymnos': 'Κάλυμνος', 'karpathos': 'Κάρπαθος', 'symi': 'Σύμη',
  'chania': 'Χανιά', 'heraklion': 'Ηράκλειο', 'rethymno': 'Ρέθυμνο',
  'lasithi': 'Λασίθι',
  'lesvos': 'Λέσβος', 'samos': 'Σάμος', 'chios': 'Χίος',
  'ikaria': 'Ικαρία', 'lemnos': 'Λήμνος',
  'agios-efstratios': 'Άγιος Ευστράτιος', 'psara': 'Ψαρά', 'oinousses': 'Οινούσσες',
  'skiathos': 'Σκιάθος', 'skopelos': 'Σκόπελος', 'alonnisos': 'Αλόννησος',
  'hydra': 'Ύδρα', 'spetses': 'Σπέτσες', 'aegina': 'Αίγινα',
  'poros': 'Πόρος', 'salamis': 'Σαλαμίνα',
  'agathonisi': 'Αγαθονήσι',
  'agistri': 'Αγκίστρι',
  'ammouliani': 'Αμμουλιανή',
  'anafi': 'Ανάφη',
  'andros': 'Άνδρος',
  'antiparos': 'Αντίπαρος',
  'astypalaia': 'Αστυπάλαια',
  'donousa': 'Δονούσα',
  'euboea': 'Εύβοια',
  'fournoi': 'Φούρνοι',
  'gavdos': 'Γαύδος',
  'halki': 'Χάλκη',
  'kasos': 'Κάσος',
  'kastellorizo': 'Καστελλόριζο',
  'kea': 'Κέα (Τζια)',
  'kimolos': 'Κίμωλος',
  'koufonisia': 'Κουφονήσια',
  'kythnos': 'Κύθνος',
  'leipsoi': 'Λειψοί',
  'leros': 'Λέρος',
  'nisyros': 'Νίσυρος',
  'paxos': 'Παξοί',
  'samothrace': 'Σαμοθράκη',
  'schoinoussa': 'Σχοινούσα',
  'serifos': 'Σέριφος',
  'sikinos': 'Σίκινος',
  'skyros': 'Σκύρος',
  'syros': 'Σύρος',
  'thasos': 'Θάσος',
  'therasia': 'Θηρασιά',
  'tilos': 'Τήλος',
  'tinos': 'Τήνος',
};

// Group names in Greek
const GROUP_NAMES_EL = {
  'Cyclades': 'Κυκλάδες',
  'Dodecanese': 'Δωδεκάνησα',
  'Ionian': 'Ιόνιο',
  'Sporades': 'Σποράδες',
  'NE Aegean': 'Β.Α. Αιγαίο',
  'Saronic': 'Σαρωνικός',
  'Crete': 'Κρήτη',
};

// Translation helper functions
function t(key) {
  const entry = UI_TEXT[key];
  if (!entry) return key;
  return entry[CURRENT_LANG] || entry.en || key;
}

// Helper for picking translated content from JSON objects.
// Usage: pickLang(stop, 'name') returns stop.name_el if Greek and exists, otherwise stop.name
function pickLang(obj, field) {
  if (!obj) return '';
  if (CURRENT_LANG === 'el' && obj[field + '_el']) return obj[field + '_el'];
  return obj[field] || '';
}

function islandName(key) {
  if (CURRENT_LANG === 'el' && ISLAND_NAMES_EL[key]) return ISLAND_NAMES_EL[key];
  return ISLANDS_DATA[key] ? ISLANDS_DATA[key].name : key;
}

function groupName(group) {
  if (CURRENT_LANG === 'el' && GROUP_NAMES_EL[group]) return GROUP_NAMES_EL[group];
  return group;
}

// Apply translations to static UI elements on page load
function applyStaticTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    el.textContent = t(key);
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.dataset.i18nPlaceholder;
    el.placeholder = t(key);
  });
  document.documentElement.lang = CURRENT_LANG;
}

// Make available globally
window.t = t;
window.pickLang = pickLang;
window.islandName = islandName;
window.groupName = groupName;
window.CURRENT_LANG = CURRENT_LANG;
window.applyStaticTranslations = applyStaticTranslations;
