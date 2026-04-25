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
  'hero.sub': { en: '76 islands scored across beaches, culture, nightlife, access and price. Click any circle to explore.', el: '76 νησιά βαθμολογημένα σε παραλίες, πολιτισμό, νυχτερινή ζωή, πρόσβαση και τιμή. Πάτα οποιοδήποτε σημείο για εξερεύνηση.' },
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
  'help.step4.title': { en: 'Save &amp; compare', el: 'Αποθήκευση &amp; σύγκριση' },
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
  'dim.car.hint': { en: 'Car reliance: 1=useless, 2=e-scooter works, 5=essential', el: 'Χρησιμότητα οχήματος: 1=περιττή, 2=e-scooter αρκεί, 5=απαραίτητη' },
  'car.none': { en: 'Useless', el: 'Άχρηστο' },
  'car.helpful': { en: 'E-scooter', el: 'Πατίνι' },
  'car.useful': { en: 'Useful', el: 'Χρήσιμο' },
  'car.recommended': { en: 'Very useful', el: 'Πολύ χρήσιμο' },
  'car.essential': { en: 'Essential', el: 'Απαραίτητο' },

  // Detail page buttons
  'detail.back': { en: '← Back to Map', el: '← Χάρτης' },
  'detail.compare': { en: '＋ Compare', el: '＋ Σύγκριση' },
  'detail.save': { en: '☆ Save', el: '☆ Λίστα' },
  'detail.saved': { en: '★ Saved', el: '★ Στη λίστα' },
  'detail.copylink': { en: '🔗 Copy link', el: '🔗 Αντιγραφή' },
  'detail.print': { en: '🖨 Print', el: '🖨 Εκτύπωση' },
  'detail.bookferry': { en: '🚢 Book ferry tickets', el: '🚢 Κράτηση' },
  'detail.copied': { en: '✓ Copied!', el: '✓ Αντιγράφτηκε!' },

  // Generic fallback (ghost islands / failed JSON fetch)
  'fallback.summary': { en: 'Blueprint Summary', el: 'Σύνοψη Aegean Blueprint' },
  'fallback.scores': { en: 'scores <strong>{SCORE}/5</strong> overall.', el: 'βαθμολογείται συνολικά με <strong>{SCORE}/5</strong>.' },
  'fallback.beach': { en: ' Outstanding beaches.', el: ' Εξαιρετικές παραλίες.' },
  'fallback.hist': { en: ' Exceptional culture and history.', el: ' Εξαιρετικός πολιτισμός και ιστορία.' },
  'fallback.night': { en: ' Among the best nightlife in Greece.', el: ' Από τις καλύτερες νυχτερινές διασκεδάσεις στην Ελλάδα.' },
  'fallback.afford_high': { en: ' Very affordable.', el: ' Πολύ οικονομικό.' },
  'fallback.afford_low': { en: ' One of the most expensive islands — budget accordingly.', el: ' Από τα πιο ακριβά νησιά — προγραμμάτισε τον προϋπολογισμό σου.' },
  'fallback.access_high': { en: ' Excellent connections from Athens.', el: ' Εξαιρετικές συνδέσεις από Αθήνα.' },
  'fallback.access_low': { en: ' Remote and harder to reach — but worth the effort.', el: ' Απομακρυσμένο και δύσκολο στην πρόσβαση — αλλά αξίζει τον κόπο.' },
  'fallback.coming_soon': { en: 'Full itinerary and beach guide coming soon.', el: 'Πλήρες πρόγραμμα και οδηγός παραλιών σύντομα.' },
  'fallback.compare_link': { en: 'Compare with another island →', el: 'Σύγκριση με άλλο νησί →' },
  'fallback.loading': { en: 'Loading {NAME} guide…', el: 'Φόρτωση οδηγού για {NAME}…' },

  // Local & Seasonal section
  'local.section_title': { en: 'Local & Seasonal', el: 'Τοπικά & Εποχιακά' },
  'local.specialties': { en: 'Local Specialties', el: 'Τοπικά Προϊόντα' },
  'local.crafts': { en: 'Crafts & Souvenirs', el: 'Χειροτεχνία & Αναμνηστικά' },
  'local.festivals': { en: 'Festivals & Events', el: 'Πανηγύρια & Εκδηλώσεις' },

  // Detail sidebar
  'detail.ratings': { en: 'Blueprint Ratings', el: 'Βαθμολογίες' },
  'detail.keystats': { en: 'Key Stats', el: 'Βασικά Στοιχεία' },
  'sidebar.beach': { en: 'Beach Quality', el: 'Ποιότητα Παραλιών' },
  'sidebar.culture': { en: 'Culture &amp; History', el: 'Πολιτισμός &amp; Ιστορία' },
  'sidebar.night': { en: 'Night Life', el: 'Νυχτερινή ζωή' },
  'sidebar.access': { en: 'Access Ease', el: 'Ευκολία Πρόσβασης' },
  'sidebar.afford': { en: 'Price Level', el: 'Κόστος' },
  'sidebar.car': { en: 'Car reliance', el: 'Χρησιμότητα οχήματος' },
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

  // Section 1 — Why this site exists
  'mission.why.title': { en: 'Why this site exists', el: 'Γιατί υπάρχει αυτή η σελίδα' },
  'mission.why.p1': { en: 'There are 76 islands on Aegean Blueprint. Most guides try to cover all of them, and end up saying nothing useful about any. AI-generated lists read like they were written by someone who has never tasted a tomato.', el: 'Στο Aegean Blueprint υπάρχουν 76 νησιά. Οι περισσότεροι οδηγοί τα καλύπτουν όλα — και καταλήγουν να μη λένε τίποτα χρήσιμο για κανένα. Οι λίστες από AI διαβάζονται σαν να τις έγραψε άνθρωπος που δεν έχει δοκιμάσει ποτέ ντομάτα.' },
  'mission.why.quote': { en: "This site is for people who don't want choices. They want the gist, without the fluff.", el: 'Αυτή η σελίδα είναι για ανθρώπους που δεν θέλουν επιλογές. Θέλουν την ουσία, χωρίς περιττά.' },
  'mission.why.p2': { en: 'Each island page gives you one opinionated recommendation: where to stay, what to do for 2 to 5 days, where to swim, where to eat. Not ten options. One. The one I would pick.', el: 'Κάθε σελίδα νησιού σού δίνει μία πρόταση με άποψη: πού να μείνεις, τι να κάνεις σε 2 έως 5 μέρες, πού να κολυμπήσεις, πού να φας. Όχι δέκα επιλογές. Μία. Αυτή που θα διάλεγα ο ίδιος.' },

  // Section 2 — Built by one person
  'mission.author.title': { en: 'Built by one person', el: 'Φτιαγμένο από έναν άνθρωπο' },
  'mission.author.role': { en: 'Founder · Athens', el: 'Δημιουργός · Αθήνα' },
  'mission.author.role2': { en: 'Founder · Athens', el: 'Δημιουργός · Αθήνα' },
  'mission.author.bio': { en: 'Greek, based in Athens. 50+ islands visited over 20+ years. Not a travel influencer, not a sponsored blog. One person writing what he actually thinks.', el: 'Έλληνας, ζω στην Αθήνα. 50+ νησιά σε 20+ χρόνια. Δεν είμαι influencer, ούτε blog με χορηγίες. Ένας άνθρωπος που γράφει αυτό που πραγματικά πιστεύει.' },
  'mission.author.note': { en: 'The alternative is what everyone else does: aggregate TripAdvisor reviews, run them through an SEO mill, translate the output, and call it a "guide." The writing reads fine. The advice is worthless.', el: 'Η εναλλακτική είναι αυτό που κάνουν όλοι: κριτικές από TripAdvisor, πέρασμα από SEO μηχανή, μετάφραση σε όλες τις γλώσσες, και το λένε «οδηγό». Το κείμενο διαβάζεται μια χαρά. Η συμβουλή έχει μικρή χρησιμότητα.' },

  // Section 3 — The one-recommendation principle
  'mission.principle.title': { en: 'The one-recommendation principle', el: 'Η αρχή της μίας πρότασης' },
  'mission.principle.intro': { en: 'For each island, this site picks exactly one of each:', el: 'Για κάθε νησί, η σελίδα διαλέγει ακριβώς ένα από τα παρακάτω:' },
  'mission.principle.hotel.label': { en: 'One hotel', el: 'Ένα ξενοδοχείο' },
  'mission.principle.hotel.text': { en: 'With a budget alternative if the top pick is too expensive. Linked to Booking.com so you can check availability in one click.', el: 'Με μια οικονομικότερη εναλλακτική αν η πρώτη επιλογή είναι ακριβή. Σύνδεσμος στο Booking.com για να δεις τη διαθεσιμότητα με ένα κλικ.' },
  'mission.principle.route.label': { en: 'One itinerary', el: 'Ένα δρομολόγιο' },
  'mission.principle.route.text': { en: '2 to 5 days depending on the island, mapped with driving distances. Beaches, villages, archaeological sites, places to eat. No "optional side-trips."', el: '2 έως 5 μέρες ανάλογα με το νησί, χαρτογραφημένο με αποστάσεις. Παραλίες, χωριά, αρχαιολογικοί χώροι, εστιατόρια. Χωρίς «προαιρετικές εκδρομές».' },
  'mission.principle.dinner.label': { en: 'One dinner spot per night', el: 'Ένα εστιατόριο ανά βράδυ' },
  'mission.principle.dinner.text': { en: "Named, linked, often with a phone number to book ahead. Where I'd take a friend who had one night on the island.", el: 'Με όνομα, σύνδεσμο, συχνά και τηλέφωνο για κράτηση. Εκεί που θα πήγαινα έναν φίλο που έχει μόνο μία βραδιά στο νησί.' },
  'mission.principle.kicker': { en: 'Pick an island. Pack a bag. Go.', el: 'Διάλεξε ένα νησί. Φτιάξε βαλίτσα. Φύγε.' },

  // Section 4 — How we score
  'mission.scoring.title': { en: 'How we score', el: 'Πώς βαθμολογούμε' },
  'mission.scoring.lead': { en: 'Every island gets rated 1 to 5 on five dimensions, plus an overall number. None of these are computed by an algorithm or scraped from elsewhere — they\'re my own informed judgment, based on having been to most of them or talking to people who live on the rest.', el: 'Κάθε νησί παίρνει βαθμολογία 1 έως 5 σε πέντε διαστάσεις, συν έναν συνολικό αριθμό. Κανένα από αυτά δεν υπολογίζεται με αλγόριθμο και κανένα δεν είναι παρμένο από αλλού — είναι η δική μου κρίση, με βάση το ότι έχω πάει στα περισσότερα ή ότι μιλάω με ανθρώπους που ζουν στα υπόλοιπα.' },
  'mission.scoring.honest': { en: "If you want to know why Milos is 4.6 and Tinos is 3.9, the short answer is: I think so, for the reasons below. The longer answer is: disagree with me — I'd rather have that conversation than pretend there's a formula.", el: 'Αν θες να ξέρεις γιατί η Μήλος είναι 4.6 και η Τήνος 3.9, η σύντομη απάντηση είναι: έτσι το κρίνω, για τους παρακάτω λόγους. Η μακριά απάντηση: διαφώνησε μαζί μου — καλύτερα αυτή η συζήτηση, παρά μια ψεύτικη για φόρμουλες.' },

  // Sources
  'mission.sources.title': { en: 'Where the information comes from', el: 'Από πού έρχονται οι πληροφορίες' },
  'mission.sources.visited.t': { en: 'Personal visits.', el: 'Προσωπικές επισκέψεις.' },
  'mission.sources.visited.d': { en: ' 50+ of the 76 islands, most more than once.', el: ' 50+ από τα 76 νησιά, τα περισσότερα παραπάνω από μία φορές.' },
  'mission.sources.local.t': { en: 'Local contacts.', el: 'Ντόπιες γνωριμίες.' },
  'mission.sources.local.d': { en: ' Friends and family who live or summer on specific islands. Kalymnos, Ikaria, Lemnos, Skyros — when I call someone who lives there, their answer beats any guidebook.', el: ' Φίλοι και συγγενείς που ζουν ή παραθερίζουν σε συγκεκριμένα νησιά. Κάλυμνος, Ικαρία, Λήμνος, Σκύρος — όταν παίρνω τηλέφωνο σε κάποιον που ζει εκεί, η απάντησή του κερδίζει κάθε οδηγό.' },
  'mission.sources.official.t': { en: 'Official data.', el: 'Επίσημες πηγές.' },
  'mission.sources.official.d': { en: ' Ferry schedules from operators directly. Opening hours from the actual restaurant or museum. Wikipedia for historical facts. Not from SEO-farm aggregators.', el: ' Δρομολόγια απευθείας από τους μεταφορείς. Ωράρια από τα ίδια τα εστιατόρια και τα μουσεία. Wikipedia για ιστορικά στοιχεία. Όχι από SEO-farm συλλογείς.' },
  'mission.sources.feedback.t': { en: 'Reader corrections.', el: 'Διορθώσεις αναγνωστών.' },
  'mission.sources.feedback.d': { en: ' When someone emails to say a restaurant closed, the page updates. The Feedback button is the loop.', el: ' Όταν μου γράφει κάποιος ότι έκλεισε ένα εστιατόριο, η σελίδα ενημερώνεται. Το κουμπί Σχόλια είναι ο κύκλος.' },

  // Rubric
  'mission.rubric.title': { en: 'The rubric', el: 'Η κλίμακα' },
  'mission.rubric.intro': { en: "Five dimensions. Each scored 1 to 5. Here's what those numbers actually mean.", el: 'Πέντε διαστάσεις. Κάθε μία βαθμολογείται 1 έως 5. Να τι σημαίνουν πραγματικά αυτοί οι αριθμοί.' },

  'mission.rubric.beach.name': { en: 'Beach', el: 'Παραλία' },
  'mission.rubric.beach.desc': { en: 'How good the swimming is.', el: 'Πόσο καλό είναι το μπάνιο.' },
  'mission.rubric.beach.5': { en: "You'd pick the island because of the water. Milos, Elafonisos, Lefkada.", el: 'Θα διάλεγες το νησί για τα νερά του. Μήλος, Ελαφόνησος, Λευκάδα.' },
  'mission.rubric.beach.3': { en: "Good beaches exist but they're not the reason to come.", el: 'Καλές παραλίες υπάρχουν αλλά δεν είναι ο λόγος να έρθεις.' },
  'mission.rubric.beach.1': { en: 'Swim at the hotel pool instead.', el: 'Κολύμπα καλύτερα στην πισίνα του ξενοδοχείου.' },

  'mission.rubric.hist.name': { en: 'Culture', el: 'Πολιτισμός' },
  'mission.rubric.hist.desc': { en: 'Archaeology, museums, churches, old towns, living tradition.', el: 'Αρχαιολογία, μουσεία, εκκλησίες, παλιές πόλεις, ζωντανή παράδοση.' },
  'mission.rubric.hist.5': { en: 'Serious depth. Delos, Rhodes Old Town, Patmos.', el: 'Σοβαρό βάθος. Δήλος, Παλιά Πόλη Ρόδου, Πάτμος.' },
  'mission.rubric.hist.3': { en: 'One or two good sites, worth a half-day.', el: 'Ένα-δύο καλά σημεία, αξίζουν μισή μέρα.' },
  'mission.rubric.hist.1': { en: 'The island\'s story is "we have a beach."', el: 'Η ιστορία του νησιού είναι «έχουμε παραλία».' },

  'mission.rubric.night.name': { en: 'Nightlife', el: 'Νυχτερινή ζωή' },
  'mission.rubric.night.desc': { en: 'From beach clubs to late dinners.', el: 'Από beach clubs μέχρι αργά δείπνα.' },
  'mission.rubric.night.5': { en: 'Party-destination level. Mykonos, Ios.', el: 'Επίπεδο party-προορισμού. Μύκονος, Ίος.' },
  'mission.rubric.night.3': { en: 'Good food, a few bars, things happen after midnight.', el: 'Καλό φαγητό, λίγα μπαρ, κάτι γίνεται μετά τα μεσάνυχτα.' },
  'mission.rubric.night.1': { en: 'Dinner ends at 10pm and the village sleeps.', el: 'Το δείπνο τελειώνει στις 10 και το χωριό κοιμάται.' },

  'mission.rubric.access.name': { en: 'Access', el: 'Πρόσβαση' },
  'mission.rubric.access.desc': { en: 'How hard to reach from Athens, and onward.', el: 'Πόσο δύσκολο να φτάσεις από την Αθήνα, και παραπέρα.' },
  'mission.rubric.access.5': { en: 'Airport plus fast ferries. Santorini, Rhodes, Corfu.', el: 'Αεροδρόμιο και γρήγορα πλοία. Σαντορίνη, Ρόδος, Κέρκυρα.' },
  'mission.rubric.access.3': { en: 'One reliable ferry a day in summer.', el: 'Ένα αξιόπιστο πλοίο τη μέρα το καλοκαίρι.' },
  'mission.rubric.access.1': { en: 'You need to really want to go.', el: 'Πρέπει πραγματικά να το θες.' },

  'mission.rubric.afford.name': { en: 'Affordability', el: 'Οικονομικά' },
  'mission.rubric.afford.desc': { en: 'Week for two in August: hotel + food + getting around.', el: 'Εβδομάδα για δύο τον Αύγουστο: ξενοδοχείο + φαγητό + μετακινήσεις.' },
  'mission.rubric.afford.5': { en: 'Genuinely cheap. Ikaria, Samothrace, Lemnos.', el: 'Γνήσια φθηνά. Ικαρία, Σαμοθράκη, Λήμνος.' },
  'mission.rubric.afford.3': { en: 'Normal Greek-island pricing.', el: 'Κανονικές τιμές ελληνικού νησιού.' },
  'mission.rubric.afford.1': { en: 'Mykonos/Santorini territory. Dinner alone can clear €200.', el: 'Επίπεδο Μυκόνου/Σαντορίνης. Μόνο το δείπνο ξεπερνά τα 200€.' },

  // Overall
  'mission.overall.title': { en: 'The overall number', el: 'Ο συνολικός αριθμός' },
  'mission.overall.p1': { en: 'The overall number leans most on Beach and Culture — that\'s what most people come for — but it\'s not a formula. A quiet, affordable island with one great beach and one real ruin can outscore a famous one that doesn\'t offer anything unique. <strong>Milos is {milos.total}, Tinos is {tinos.total}.</strong> I set numbers by judgment, then check them by ranking islands against each other in my head.', el: 'Ο συνολικός αριθμός γέρνει περισσότερο προς την Παραλία και τον Πολιτισμό — γι\' αυτά έρχεται ο περισσότερος κόσμος εδώ — αλλά δεν είναι φόρμουλα. Ένα ήσυχο, οικονομικό νησί με μία πραγματικά ωραία παραλία και ένα αληθινό μνημείο μπορεί να βγει μπροστά από ένα διάσημο που δεν προσφέρει κάτι μοναδικό. <strong>Η Μήλος είναι {milos.total}, η Τήνος {tinos.total}.</strong> Βάζω τους αριθμούς με την κρίση μου, και τους ξαναβλέπω συγκρίνοντας τα νησιά μεταξύ τους στο μυαλό μου.' },
  'mission.overall.p3': { en: 'Use the five underlying numbers if your trip has a specific goal. The overall is for sorting the table when you don\'t yet know what you want.', el: 'Χρησιμοποίησε τις πέντε επιμέρους διαστάσεις αν το ταξίδι σου έχει συγκεκριμένο στόχο. Τη συνολική βαθμολογία όταν ταξινομείς τον πίνακα και δεν έχεις ακόμα αποφασίσει τι ψάχνεις.' },

  // Updates
  'mission.updates.title': { en: 'How often this changes', el: 'Πόσο συχνά αλλάζει' },
  'mission.updates.p1': { en: "Restaurants close. Ferry operators swap routes. A hotel changes hands and quality drops. Scores themselves rarely shift — an island's personality doesn't change in a season — but the specifics on a page do.", el: 'Τα εστιατόρια κλείνουν. Οι ακτοπλοϊκές αλλάζουν γραμμές. Ένα ξενοδοχείο αλλάζει χέρια και η ποιότητα πέφτει. Οι ίδιες οι βαθμολογίες σπάνια αλλάζουν — ο χαρακτήρας ενός νησιού δεν αλλάζει σε μια σεζόν — αλλά οι λεπτομέρειες στη σελίδα αλλάζουν.' },
  'mission.updates.p2': { en: 'When I get reader feedback or visit an island again, the page updates. When a restaurant I recommended closes, the link comes down within a week. The goal is not to be an encyclopedia — it\'s to be the most current opinionated recommendation you can trust for the next 6 months.', el: 'Όταν παίρνω σχόλια από αναγνώστες ή επισκέπτομαι ξανά ένα νησί, η σελίδα ενημερώνεται. Όταν κλείνει ένα εστιατόριο που πρότεινα, ο σύνδεσμος κατεβαίνει μέσα σε μια εβδομάδα. Στόχος δεν είναι να γίνουμε εγκυκλοπαίδεια — αλλά η πιο ενημερωμένη πρόταση με άποψη που μπορείς να εμπιστευτείς για τους επόμενους 6 μήνες.' },

  // Limits
  'mission.limits.title': { en: "What the scores can't capture", el: 'Τι δεν μπορούν να δείξουν οι βαθμολογίες' },
  'mission.limits.lead': { en: "Five numbers can't describe an island. A few things they miss:", el: 'Πέντε αριθμοί δεν περιγράφουν ένα νησί. Κάποια πράγματα που χάνουν:' },
  'mission.limits.season': { en: "Season. Ios in July is a 5 for nightlife; Ios in April is a 1. The score reflects the peak.", el: 'Εποχή. Η Ίος τον Ιούλιο είναι 5 στη νυχτερινή ζωή· τον Απρίλιο είναι 1. Ο αριθμός δείχνει την κορύφωση.' },
  'mission.limits.taste': { en: "Personal taste. If you hate parties, Mykonos's high Nightlife score is a warning, not a selling point.", el: 'Προσωπικό γούστο. Αν μισείς τα πάρτι, η ψηλή βαθμολογία Νυχτερινής Ζωής της Μυκόνου είναι προειδοποίηση, όχι πλεονέκτημα.' },
  'mission.limits.crowds': { en: "Crowds. Santorini scores well across the board but feels different when six cruise ships dock the same day. The pages mention this; the numbers don't reflect it.", el: 'Τουριστικός συνωστισμός. Η Σαντορίνη βαθμολογείται καλά παντού, αλλά έχει άλλη αίσθηση όταν δένουν έξι κρουαζιερόπλοια την ίδια μέρα. Οι σελίδες το αναφέρουν, οι αριθμοί όχι.' },
  'mission.limits.drift': { en: "Drift. A \"must-eat\" restaurant can coast for years on reviews after the original chef leaves. I try to catch these but I'm one person.", el: 'Μετατόπιση. Ένα «must-eat» εστιατόριο μπορεί να εξακολουθεί να συστήνεται χρόνια μετά την αποχώρηση του αρχικού σεφ. Προσπαθώ να τα πιάνω αλλά είμαι ένας άνθρωπος.' },

  // Disagree
  'mission.disagree.title': { en: 'Think I got one wrong?', el: 'Πιστεύεις πως έκανα λάθος;' },
  'mission.disagree.text': { en: 'Hit the <strong>💬 Feedback</strong> button at the bottom right of any page and pick <em>"Suggest a rating correction."</em> Explain what you\'d change and why. If you make a good case, I\'ll update the number. The five dimensions and the reasoning stay in the open.', el: 'Πάτα το κουμπί <strong>💬 Σχόλια</strong> κάτω δεξιά σε οποιαδήποτε σελίδα και διάλεξε <em>«Πρόταση διόρθωσης βαθμολογίας»</em>. Εξήγησε τι θα άλλαζες και γιατί. Αν έχεις καλό επιχείρημα, θα ενημερώσω τον αριθμό. Οι πέντε διαστάσεις και η λογική παραμένουν δημόσιες.' },

  'scoring.howlink': { en: 'how we score', el: 'πώς βαθμολογούμε' },
  'feedback.topic.suggestion': { en: '💡 Suggestion or feature idea', el: '💡 Πρόταση ή ιδέα' },
  'feedback.topic.error': { en: '🐛 Error or correction', el: '🐛 Λάθος ή διόρθωση' },
  'feedback.topic.rating': { en: '⭐ Suggest a rating correction', el: '⭐ Πρόταση διόρθωσης βαθμολογίας' },
  'feedback.topic.missing-island': { en: '🏝 Island we should add', el: '🏝 Νησί που πρέπει να προσθέσουμε' },
  'feedback.topic.missing-restaurant': { en: '🍴 Restaurant or beach to add', el: '🍴 Εστιατόριο ή παραλία να προσθέσουμε' },
  'feedback.topic.other': { en: '💬 Something else', el: '💬 Κάτι άλλο' },
  'feedback.message.placeholder': { en: "Tell us what's on your mind...", el: 'Πες μας τι σκέφτεσαι...' },
  'feedback.email.placeholder': { en: 'you@example.com', el: 'you@example.com' },

  // Accessibility: aria-label / title / alt attributes
  'a11y.search_islands': { en: 'Search islands', el: 'Αναζήτηση νησιών' },
  'a11y.filter_group': { en: 'Filter by island group', el: 'Φιλτράρισμα ανά νησιωτικό σύμπλεγμα' },
  'a11y.rank_map_by': { en: 'Rank map by', el: 'Ταξινόμηση χάρτη κατά' },
  'a11y.radar_compare': { en: 'Radar chart comparing two islands', el: 'Διάγραμμα ράνταρ που συγκρίνει δύο νησιά' },
  'a11y.switch_language': { en: 'Switch language', el: 'Αλλαγή γλώσσας' },
  'a11y.toggle_dark': { en: 'Toggle dark mode', el: 'Εναλλαγή σκοτεινής λειτουργίας' },
  'a11y.car_scale': { en: '1 = car useless, 5 = car essential', el: '1 = το αυτοκίνητο περιττό, 5 = το αυτοκίνητο απαραίτητο' },
  'a11y.has_airport': { en: 'Commercial airport on the island', el: 'Εμπορικό αεροδρόμιο στο νησί' },
  'a11y.how_to_use': { en: 'How to use this site', el: 'Πώς να χρησιμοποιήσετε αυτόν τον ιστότοπο' },
  'a11y.send_feedback': { en: 'Send feedback', el: 'Αποστολή σχολίων' },
  'a11y.logo_alt': { en: 'Aegean Blueprint logo', el: 'Λογότυπο Aegean Blueprint' },

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

// Apply translations to static UI elements on page load.
// Uses innerHTML rather than textContent so translations can include simple
// formatting tags (<strong>, <em>, <br>). All translation strings are
// hard-coded in TRANSLATIONS — no user input ever reaches this path.
function applyStaticTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    el.innerHTML = applyDataTokens(t(key));
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.dataset.i18nPlaceholder;
    el.placeholder = applyDataTokens(t(key));
  });
  document.querySelectorAll('[data-i18n-title]').forEach(el => {
    const key = el.dataset.i18nTitle;
    el.title = applyDataTokens(t(key));
  });
  document.querySelectorAll('[data-i18n-aria-label]').forEach(el => {
    const key = el.dataset.i18nAriaLabel;
    el.setAttribute('aria-label', applyDataTokens(t(key)));
  });
  document.querySelectorAll('[data-i18n-alt]').forEach(el => {
    const key = el.dataset.i18nAlt;
    el.alt = applyDataTokens(t(key));
  });
  document.documentElement.lang = CURRENT_LANG;
}

/* Replace {islandkey.field} tokens in a string by looking up
   ISLANDS_DATA. Example: "Milos is {milos.total}" -> "Milos is 4.6"
   If ISLANDS_DATA isn't loaded yet, leaves tokens as-is. */
function applyDataTokens(text) {
  if (!text || typeof text !== 'string') return text;
  if (text.indexOf('{') === -1) return text;
  if (typeof ISLANDS_DATA === 'undefined') return text;
  return text.replace(/\{([a-z_-]+)\.([a-z_]+)\}/g, (match, key, field) => {
    const island = ISLANDS_DATA[key];
    if (!island) return match;
    const val = island[field];
    if (val === undefined || val === null) return match;
    return typeof val === 'number' ? val.toFixed(1) : String(val);
  });
}

// Make available globally
window.t = t;
window.pickLang = pickLang;
window.islandName = islandName;
window.groupName = groupName;
window.CURRENT_LANG = CURRENT_LANG;
window.applyStaticTranslations = applyStaticTranslations;
