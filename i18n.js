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
  'nav.international': { en: 'International', el: 'Διεθνώς' },
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
  'tooltip.suggesteddays': { en: 'Suggested stay', el: 'Προτεινόμενη διαμονή' },
  'common.yes': { en: 'Yes', el: 'Ναι' },
  'compare.pop': { en: 'Pop', el: 'Πληθ' },
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
  'dim.car.hint': { en: 'Car reliance: 1=useless, 2=e-scooter works, 5=essential', el: 'Χρησιμότητα οχήματος: 1=άχρηστη, 2=πατίνι αρκεί, 5=απαραίτητη' },
  'car.none': { en: 'Useless', el: 'Άχρηστο' },
  'car.helpful': { en: 'E-scooter', el: 'Πατίνι' },
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
  'detail.beach': { en: 'Beach', el: 'Παραλία' },
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

  // International Escapes page
  'international.title': { en: '🌍 International Escapes', el: '🌍 Διεθνείς Αποδράσεις' },
  'international.intro': { en: "Greek islands are closer to foreign shores than you think. From Corfu, Albania is 30 minutes away. From the east Aegean, Turkey is a short ferry across. Here are the proven international ferry connections from Greek islands — a different kind of island-hopping.", el: 'Τα ελληνικά νησιά είναι πιο κοντά σε ξένες ακτές απ\'όσο νομίζεις. Από την Κέρκυρα, η Αλβανία απέχει 30 λεπτά. Από το Ανατολικό Αιγαίο, η Τουρκία είναι σύντομη διαδρομή. Εδώ είναι οι αξιόπιστες διεθνείς συνδέσεις πλοίων από ελληνικά νησιά — ένα διαφορετικό είδος νησοπορίας.' },
  'international.legend.daily': { en: 'Daily (multiple crossings per day)', el: 'Καθημερινά (πολλά δρομολόγια)' },
  'international.legend.frequent': { en: 'Frequent in summer (4-7/week)', el: 'Συχνά το καλοκαίρι (4-7/εβδ)' },
  'international.legend.seasonal': { en: 'Seasonal / limited', el: 'Εποχιακό / περιορισμένο' },
  'international.routes.title': { en: 'All Routes', el: 'Όλες οι Διαδρομές' },
  'international.country.albania': { en: 'Albania', el: 'Αλβανία' },
  'international.country.turkey': { en: 'Turkey', el: 'Τουρκία' },
  'international.destination.worth': { en: 'worth the trip?', el: 'αξίζει το ταξίδι;' },
  'international.schedule.btn': { en: 'See schedules', el: 'Δες δρομολόγια' },
  'international.prebook': { en: '💡 <strong>No need to pre-book.</strong> For all routes below, you can buy your ferry ticket on the spot at the port on the same day. Summer is busier — arrive 60–90 min before departure to secure your seat.', el: '💡 <strong>Δεν χρειάζεται προκράτηση.</strong> Για όλες τις παρακάτω διαδρομές, μπορείς να αγοράσεις το εισιτήριο επί τόπου στο λιμάνι την ίδια μέρα. Το καλοκαίρι έχει κίνηση — έλα 60–90 λεπτά πριν την αναχώρηση για να εξασφαλίσεις θέση.' },

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
  'mission.scoring.title': { en: 'How we score', el: 'Πώς βαθμολογούμε' },
  'mission.scoring.lead': { en: 'Every island on this site gets rated 1–5 on five dimensions. These numbers aren\'t an algorithm. They\'re one person\'s judgment — Stergios\'s — based on having actually been to these islands, read everything written about the rest, and thought carefully about what each one is actually good for.', el: 'Κάθε νησί στη σελίδα βαθμολογείται από 1 έως 5 σε πέντε διαστάσεις. Αυτοί οι αριθμοί δεν είναι αλγόριθμος. Είναι η κρίση ενός ανθρώπου — του Στέργιου — που έχει ταξιδέψει στα νησιά αυτά, έχει διαβάσει όσα έχουν γραφτεί για τα υπόλοιπα, και έχει σκεφτεί προσεκτικά για τι είναι πραγματικά καλό το καθένα.' },
  'mission.scoring.honest': { en: 'We think that\'s more useful than a "proprietary weighted index" stitched from TripAdvisor stars and hotel counts. But it\'s not objective, and we won\'t pretend it is. If you want to know why Milos is a 4.6 and Tinos is a 3.9, the short answer is: Stergios thinks so, for the reasons below. The longer answer is: disagree with us — we\'d rather have that conversation than a fake one about formulas.', el: 'Πιστεύουμε ότι αυτό είναι πιο χρήσιμο από έναν «ιδιόκτητο σταθμισμένο δείκτη» ραμμένο από αστεράκια TripAdvisor και αριθμούς ξενοδοχείων. Αλλά δεν είναι αντικειμενικό, και δεν θα το παραστήσουμε. Αν θέλεις να ξέρεις γιατί η Μήλος είναι 4.6 και η Τήνος 3.9, η σύντομη απάντηση είναι: έτσι το κρίνει ο Στέργιος, για τους λόγους που ακολουθούν. Η μακριά απάντηση είναι: διαφώνησε μαζί μας — καλύτερα αυτή η συζήτηση, παρά μια ψεύτικη για φόρμουλες.' },
  'mission.scoring.dims.title': { en: 'The five dimensions', el: 'Οι πέντε διαστάσεις' },
  'mission.scoring.beach.term': { en: '🏖 Beach', el: '🏖 Παραλία' },
  'mission.scoring.beach.def': { en: 'How good the swimming is. A 5 means you\'d pick this island <em>because</em> of the water — Milos, Elafonisos, Lefkada. A 3 means good beaches exist but they\'re not the reason to come. A 1 means swim at your hotel pool instead.', el: 'Πόσο καλό είναι το μπάνιο. Το 5 σημαίνει ότι θα διάλεγες το νησί <em>για</em> τα νερά του — Μήλος, Ελαφόνησος, Λευκάδα. Το 3 σημαίνει καλές παραλίες υπάρχουν αλλά δεν είναι ο λόγος να έρθεις. Το 1 σημαίνει κολύμπα καλύτερα στην πισίνα του ξενοδοχείου.' },
  'mission.scoring.hist.term': { en: '🏛 Culture', el: '🏛 Πολιτισμός' },
  'mission.scoring.hist.def': { en: 'Archaeology, museums, churches, old towns, living tradition. A 5 rewards depth, not just tourist-brochure ruins — Delos, Rhodes Old Town, Patmos. A 3 means one or two good sites. A 1 means the island\'s story is "we have a beach."', el: 'Αρχαιολογία, μουσεία, εκκλησίες, παλιές πόλεις, ζωντανή παράδοση. Το 5 ανταμείβει το βάθος, όχι απλά ερείπια τουριστικού φυλλαδίου — Δήλος, Παλιά Πόλη Ρόδου, Πάτμος. Το 3 σημαίνει ένα-δύο καλά σημεία. Το 1 σημαίνει η ιστορία του νησιού είναι «έχουμε παραλία».' },
  'mission.scoring.night.term': { en: '🌃 Nightlife', el: '🌃 Νυχτερινή ζωή' },
  'mission.scoring.night.def': { en: 'From beach clubs to dinner-and-a-walk. A 5 is party-destination-level (Mykonos, Ios). A 3 means you can find good food and a few bars. A 1 means dinner ends at 10pm and the village sleeps.', el: 'Από beach clubs μέχρι φαγητό-και-βόλτα. Το 5 είναι επίπεδο party-προορισμού (Μύκονος, Ίος). Το 3 σημαίνει βρίσκεις καλό φαγητό και λίγα μπαρ. Το 1 σημαίνει το δείπνο τελειώνει στις 10 και το χωριό κοιμάται.' },
  'mission.scoring.access.term': { en: '🚢 Access', el: '🚢 Πρόσβαση' },
  'mission.scoring.access.def': { en: 'How hard it is to get there from Athens, and how far it is to the next island. A 5 has an airport and fast ferries (Santorini, Rhodes, Corfu). A 3 means one reliable ferry a day in summer. A 1 means you need to really want to go.', el: 'Πόσο δύσκολο είναι να φτάσεις από την Αθήνα, και πόσο μακριά από το επόμενο νησί. Το 5 έχει αεροδρόμιο και γρήγορα πλοία (Σαντορίνη, Ρόδος, Κέρκυρα). Το 3 σημαίνει ένα αξιόπιστο πλοίο τη μέρα το καλοκαίρι. Το 1 σημαίνει πρέπει πραγματικά να το θες.' },
  'mission.scoring.afford.term': { en: '💶 Affordability', el: '💶 Οικονομικά' },
  'mission.scoring.afford.def': { en: 'What a week costs for two people in August, hotel + food + getting around. A 5 is genuinely cheap (Ikaria, Samothrace). A 3 is normal Greek-island pricing. A 1 is Mykonos/Santorini territory where dinner alone can clear €200.', el: 'Πόσο κοστίζει μία εβδομάδα για δύο τον Αύγουστο, ξενοδοχείο + φαγητό + μετακινήσεις. Το 5 είναι γνήσια φθηνά (Ικαρία, Σαμοθράκη). Το 3 είναι κανονικές τιμές ελληνικού νησιού. Το 1 είναι επίπεδο Μυκόνου/Σαντορίνης όπου μόνο το δείπνο ξεπερνά τα 200€.' },
  'mission.scoring.overall.title': { en: 'The overall number', el: 'Ο συνολικός αριθμός' },
  'mission.scoring.overall.text': { en: 'The overall rating is a weighted mix of the five, tilted toward Beach and Culture because that\'s what most people come to the Greek islands for. It\'s still a judgment call, not a calculation — the weights themselves are a choice, and someone whose holiday is all about nightlife would weight it differently. Use the five underlying numbers. The single number is for sorting the table.', el: 'Η συνολική βαθμολογία είναι ένας σταθμισμένος μέσος όρος των πέντε, με έμφαση στην Παραλία και τον Πολιτισμό, γιατί γι\'αυτά έρχονται οι περισσότεροι στα ελληνικά νησιά. Παραμένει κρίση, όχι υπολογισμός — τα ίδια τα βάρη είναι επιλογή, και κάποιος με διακοπές εξ ολοκλήρου για νυχτερινή ζωή θα τα ζύγιζε αλλιώς. Χρησιμοποίησε τις πέντε επιμέρους διαστάσεις. Ο ένας αριθμός είναι για να ταξινομείς τον πίνακα.' },
  'mission.scoring.disagree.title': { en: 'Think we got one wrong?', el: 'Πιστεύεις πως κάναμε λάθος;' },
  'mission.scoring.disagree.text': { en: 'Tell us. Hit the <strong>💬 Feedback</strong> button at the bottom right of any page and pick "Suggest a rating correction." Explain what you\'d change and why. We read everything — and if you make a good case, we\'ll update the number. The five dimensions and the rationale stay in the open.', el: 'Πες μας. Πάτα το κουμπί <strong>💬 Σχόλια</strong> κάτω δεξιά σε οποιαδήποτε σελίδα και διάλεξε «Πρόταση διόρθωσης βαθμολογίας». Εξήγησε τι θα άλλαζες και γιατί. Διαβάζουμε τα πάντα — και αν έχεις καλό επιχείρημα, θα ενημερώσουμε τον αριθμό. Οι πέντε διαστάσεις και η λογική παραμένουν δημόσιες.' },
  'scoring.howlink': { en: 'how we score', el: 'πώς βαθμολογούμε' },
  'feedback.topic.rating': { en: '⭐ Suggest a rating correction', el: '⭐ Πρόταση διόρθωσης βαθμολογίας' },

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
