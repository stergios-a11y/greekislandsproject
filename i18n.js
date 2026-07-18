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
  'nav.festivals': { en: 'Festivals', el: 'Γιορτές' },
  'nav.ferries': { en: 'Ferries', el: 'Πλοία' },
  'nav.hopping': { en: 'Ferries & Hopping', el: 'Πλοία & Νησοπορία' },
  'nav.tripcost': { en: 'Budget', el: 'Μπάτζετ' },
  'nav.international': { en: 'International', el: 'Διεθνώς' },
  'nav.match': { en: 'Match Me', el: 'Βρες το Νησί σου' },
  'nav.shortlist': { en: '⭐ My Shortlist', el: '⭐ Η Λίστα μου' },
  'nav.mission': { en: 'Mission', el: 'Στόχος' },
  'nav.privacy': { en: 'Privacy', el: 'Απόρρητο' },

  // Hero / homepage
  'hero.title': { en: 'Find your perfect Greek island', el: 'Βρες το ιδανικό σου ελληνικό νησί' },
  'hero.sub': { en: '88 islands scored across beaches, culture, nightlife, access and affordability. Click any circle to explore.', el: '88 νησιά βαθμολογημένα σε παραλίες, πολιτισμό, νυχτερινή ζωή, πρόσβαση και προσιτή τιμή. Πάτα οποιοδήποτε σημείο για εξερεύνηση.' },
  'hero.tagline': { en: 'The Greek Island Decision Engine', el: 'Ο οδηγός για το Ελληνικό νησί που σας ταιριάζει' },
  'hero.dismiss': { en: 'Got it', el: 'Έγινε' },
  'hero.stat.islands': { en: 'Islands', el: 'Νησιά' },
  'hero.stat.dimensions': { en: 'Score dimensions', el: 'Διαστάσεις' },
  'hero.stat.guides': { en: 'Full guides', el: 'Πλήρεις οδηγοί' },
  'hero.stat.minutes': { en: 'Minutes', el: 'Λεπτά' },

  // Homepage content section (below the map)
  'home.scroll_hint': { en: 'About this site', el: 'Σχετικά με τη σελίδα' },
  'home.back_to_map': { en: 'Back to the map', el: 'Πίσω στον χάρτη' },
  'home.about.title': { en: 'A Greek islands travel guide with opinions', el: 'Ένας οδηγός για τα ελληνικά νησιά, με άποψη' },
  'home.about.p1': { en: "Most island guides list 30 beaches and call it a recommendation. This one picks the one you should actually go to, and tells you why the other 29 didn't make it. The same goes for the where-to-stay, the where-to-eat, the day plan, the side trip.", el: 'Οι περισσότεροι οδηγοί νησιών γράφουν 30 παραλίες και το λένε πρόταση. Εδώ διαλέγω αυτή που πραγματικά αξίζει, και εξηγώ γιατί δεν πέρασαν οι άλλες 29. Το ίδιο ισχύει για το πού θα μείνεις, πού θα φας, το πλάνο της ημέρας, την παρέκβαση.' },
  'home.about.p2': { en: "No sponsorships, no affiliate hotel chains in disguise. Each island gets an honest score across beaches, history, nightlife, access and price — not a marketing brochure, not an algorithm, just one person's take, cross-checked with friends and family who actually live on each island.", el: 'Χωρίς χορηγίες, χωρίς συγκαλυμμένες affiliate πλατφόρμες κρατήσεων. Κάθε νησί παίρνει μια ειλικρινή βαθμολογία σε παραλίες, ιστορία, νυχτερινή ζωή, πρόσβαση και τιμές — όχι διαφημιστικό φυλλάδιο, όχι αλγόριθμος, η κρίση ενός ανθρώπου, διασταυρωμένη με φίλους και συγγενείς που ζουν στα νησιά.' },
  'home.about.p3': { en: "The map above is the entry point. Click any circle to open that island's full guide. Use the dropdowns to filter by region or rank by what matters to you.", el: 'Ο χάρτης παραπάνω είναι το σημείο εκκίνησης. Πάτα οποιοδήποτε κυκλάκι για να ανοίξεις τον πλήρη οδηγό του νησιού. Χρησιμοποίησε τα μενού για να φιλτράρεις ανά περιοχή ή να ταξινομήσεις με το κριτήριο που σε ενδιαφέρει.' },
  'home.featured.title': { en: 'Featured islands', el: 'Επιλεγμένα νησιά' },
  'home.featured.sub': { en: 'A few starting points across different moods. Click for the full guide.', el: 'Λίγες αφετηρίες για διαφορετικές διαθέσεις. Πάτα για τον πλήρη οδηγό.' },
  'home.how.title': { en: 'How this site works', el: 'Πώς λειτουργεί η σελίδα' },
  'home.how.one.title': { en: 'One recommendation, not ten', el: 'Μία πρόταση, όχι δέκα' },
  'home.how.one.text': { en: "Every page gives a single pick for dinner, a single pick for the best beach, a single 2-to-5-day plan. A friend who knows the place doesn't list every option — they tell you the one to go to.", el: 'Κάθε σελίδα δίνει μία επιλογή για δείπνο, μία για την καλύτερη παραλία, ένα πλάνο 2 έως 5 ημερών. Ένας φίλος που γνωρίζει το μέρος δεν σου λέει όλες τις επιλογές — σου λέει αυτή που πρέπει.' },
  'home.how.scores.title': { en: 'Honest scores', el: 'Ειλικρινείς βαθμολογίες' },
  'home.how.scores.text': { en: "Beaches, history, nightlife, access, price. A 5/5 in beaches means world-class. A 2/5 in nightlife means there's a bar and that's it. The overall number is a judgment call, not a formula — no weighting, no claims of objectivity. Read the <a href=\"#mission\">full rubric →</a>", el: 'Παραλίες, ιστορία, νυχτερινή ζωή, πρόσβαση, τιμές. Το 5/5 στις παραλίες σημαίνει παγκόσμιας κλάσης. Το 2/5 στη νυχτερινή ζωή σημαίνει υπάρχει ένα μπαρ και τελείωσε. Ο συνολικός αριθμός είναι θέμα κρίσης, όχι φόρμουλα — χωρίς ζυγίσματα, χωρίς ισχυρισμούς αντικειμενικότητας. Διάβασε το <a href="#mission">πλήρες κριτήριο →</a>' },
  'home.how.scores.link': { en: 'full rubric →', el: 'πλήρες κριτήριο →' },
  'home.how.updates.title': { en: 'Real updates', el: 'Πραγματικές ενημερώσεις' },
  'home.how.updates.text': { en: 'When a restaurant closes, the link comes down within a week. When someone writes in to say a beach has changed, the page changes. The feedback button is below the map.', el: 'Όταν κλείνει ένα εστιατόριο, ο σύνδεσμος κατεβαίνει μέσα σε μια εβδομάδα. Όταν κάποιος γράφει ότι μια παραλία έχει αλλάξει, η σελίδα αλλάζει. Το κουμπί σχολίων βρίσκεται κάτω από τον χάρτη.' },
  'home.how.nofunnel.title': { en: 'No signup walls', el: 'Χωρίς τοίχους εγγραφής' },
  'home.how.nofunnel.text': { en: "No newsletter wall, no \"click to continue\", no email required to see a page. This is a static site you can read. The feedback button is the one place to write back.", el: 'Χωρίς newsletter wall, χωρίς "πάτα εδώ για συνέχεια", χωρίς email για να δεις σελίδα. Είναι ένα στατικό site που μπορείς να διαβάσεις. Το κουμπί σχολίων είναι το μοναδικό σημείο επικοινωνίας.' },

  // Help modal
  'help.btn': { en: 'How to', el: 'Οδηγίες' },
  'help.step1.title': { en: 'Explore the map', el: 'Εξερεύνησε τον χάρτη' },
  'help.step1.desc': { en: "Click any circle to open the island's full guide.", el: 'Πάτα σε οποιοδήποτε κυκλάκι για τον πλήρη οδηγό του νησιού.' },
  'help.step2.title': { en: 'Filter and rank', el: 'Φιλτράρισμα και ταξινόμηση' },
  'help.step2.desc': { en: 'Use the dropdowns to filter by island group or rank by what matters to you — beaches, culture, nightlife.', el: 'Χρησιμοποίησε τα φίλτρα για να διαλέξεις νησιωτικό σύμπλεγμα ή να ταξινομήσεις κατά παραλίες, πολιτισμό, νυχτερινή ζωή.' },
  'help.step3.title': { en: 'Take the quiz', el: 'Κάνε το quiz' },
  'help.step3.desc': { en: "Not sure where to go? Answer 7 quick questions and we'll match you to your top islands.", el: 'Δεν είσαι σίγουρος; Απάντησε σε 7 γρήγορες ερωτήσεις και θα σου προτείνουμε τα κορυφαία νησιά.' },
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
  'filter.afford': { en: '💸 Affordability', el: '💸 Προσιτή τιμή' },
  'filter.car': { en: '🚗 Car reliance', el: '🚗 Χρησιμότητα οχήματος' },
  // Dimension labels (for radar chart, bars, columns)
  'dim.beach': { en: 'Beach', el: 'Παραλία' },
  'dim.culture': { en: 'Culture', el: 'Πολιτισμός' },
  'dim.night': { en: 'Nightlife', el: 'Νυχτερινή ζωή' },
  'dim.access': { en: 'Access', el: 'Πρόσβαση' },
  'dim.afford': { en: 'Affordability', el: 'Προσιτή τιμή' },
  'dim.car': { en: 'Car reliance', el: 'Χρησιμότητα οχήματος' },
  'dim.car.hint': { en: 'Car reliance: 1 = not needed, 3 = useful, 5 = essential', el: 'Χρησιμότητα οχήματος: 1 = δεν χρειάζεται, 3 = χρήσιμο, 5 = απαραίτητο' },
  'car.none': { en: 'Not needed', el: 'Δεν χρειάζεται' },
  'car.helpful': { en: 'Optional', el: 'Προαιρετικό' },
  'car.useful': { en: 'Useful', el: 'Χρήσιμο' },
  'car.recommended': { en: 'Recommended', el: 'Συνιστάται' },
  'car.essential': { en: 'Essential', el: 'Απαραίτητο' },

  // Detail page buttons
  'detail.back': { en: '← Back to Map', el: '← Χάρτης' },
  'detail.compare': { en: '＋ Compare', el: '＋ Σύγκριση' },
  'detail.save': { en: '☆ Save', el: '☆ Λίστα' },
  'detail.saved': { en: '★ Saved', el: '★ Στη λίστα' },
  'detail.copylink': { en: '🔗 Copy link', el: '🔗 Αντιγραφή' },
  'detail.print': { en: '🖨 Print', el: '🖨 Εκτύπωση' },
  'detail.bookferry': { en: '🚢 Book ferry tickets', el: '🚢 Κράτηση' },
  'detail.rentcar': { en: '🚗 Rent a car', el: '🚗 Ενοικίαση αυτοκινήτου' },
  'detail.tripcost': { en: '💶 Cost for {d} days', el: '💶 Κόστος για {d} μέρες' },
  'similar.title': { en: 'Islands like this one', el: 'Παρόμοια νησιά' },
  'similar.intro': { en: 'Based on character, vibe, and ferry-region.', el: 'Βάσει χαρακτήρα και περιοχής.' },
  'group.cyclades':  { en: 'Cyclades',     el: 'Κυκλάδες' },
  'group.dodecanese':{ en: 'Dodecanese',   el: 'Δωδεκάνησα' },
  'group.saronic':   { en: 'Saronic',      el: 'Σαρωνικός' },
  'group.sporades':  { en: 'Sporades',     el: 'Σποράδες' },
  'group.ionian':    { en: 'Ionian',       el: 'Ιόνιο' },
  'group.neaegean':  { en: 'NE Aegean',    el: 'Β.Α. Αιγαίο' },
  'group.crete':     { en: 'Crete',        el: 'Κρήτη' },
  'group.evia':      { en: 'Evia',         el: 'Εύβοια' },
  'group.other':     { en: 'Other',        el: 'Άλλα' },
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
  'wtv.title': { en: 'When to Visit', el: 'Πότε να Πας' },

  // Detail sidebar
  'detail.ratings': { en: 'Blueprint Ratings', el: 'Βαθμολογίες' },
  'detail.keystats': { en: 'Key Stats', el: 'Βασικά Στοιχεία' },
  'sidebar.beach': { en: 'Beach Quality', el: 'Ποιότητα Παραλιών' },
  'sidebar.culture': { en: 'Culture &amp; History', el: 'Πολιτισμός &amp; Ιστορία' },
  'sidebar.night': { en: 'Night Life', el: 'Νυχτερινή ζωή' },
  'sidebar.access': { en: 'Access Ease', el: 'Ευκολία Πρόσβασης' },
  'sidebar.afford': { en: 'Affordability', el: 'Προσιτή τιμή' },
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
  'common.book_hotel': { en: 'Book', el: 'Κράτηση' },
  'common.booking_aria': { en: 'Search this hotel on Booking.com', el: 'Αναζήτηση ξενοδοχείου στο Booking.com' },
  'map.layer.map': { en: 'Map', el: 'Χάρτης' },
  'map.layer.satellite': { en: 'Satellite', el: 'Δορυφόρος' },
  'getting_there.title': { en: 'Getting there', el: 'Πώς θα φτάσεις' },
  'getting_there.tip': { en: 'Tip', el: 'Συμβουλή' },
  'detail.editorial': { en: 'Editorial', el: 'Βαθμολογία' },
  'detail.spec.type': { en: 'Type', el: 'Τύπος' },
  'detail.spec.length': { en: 'Length', el: 'Μήκος' },
  'detail.spec.depth': { en: 'Depth', el: 'Βάθος' },
  'detail.spec.wind': { en: 'Wind protection', el: 'Προστασία από αέρα' },
  'detail.spec.facilities': { en: 'Facilities', el: 'Υποδομές' },
  'detail.beaches.title': { en: 'Top Beaches of', el: 'Κορυφαίες Παραλίες' },
  'detail.beaches.sub': { en: 'Ranked by overall quality — with details on sand type, depth, wind exposure and facilities.', el: 'Κατάταξη με βάση τη συνολική ποιότητα — με λεπτομέρειες για τον τύπο άμμου, το βάθος, την έκθεση στον άνεμο και τις υποδομές.' },

  // Footer
  'footer.copyright': { en: '© 2026 Aegean Blueprint', el: '© 2026 Aegean Blueprint' },
  'footer.privacy':   { en: 'Privacy', el: 'Απόρρητο' },
  'hopping.crosslink_intl': { en: 'Continuing beyond Greece? See the ', el: 'Συνεχίζεις εκτός Ελλάδας; Δες τις ' },
  'hopping.crosslink_intl_label': { en: 'international ferry routes from Greek islands', el: 'διεθνείς ακτοπλοϊκές συνδέσεις από τα νησιά' },

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
  'data.hinttext': { en: 'See the 5 dimensions we rate each island on — beaches, culture, nightlife, access, affordability.', el: 'Δες τις 5 διαστάσεις που βαθμολογούμε σε κάθε νησί — παραλίες, πολιτισμός, νυχτερινή ζωή, πρόσβαση, προσιτή τιμή.' },

  // Compare page
  'compare.title': { en: 'Compare Islands', el: 'Σύγκριση Νησιών' },
  'compare.intro': { en: 'Select two islands to compare side-by-side.', el: 'Επίλεξε δύο νησιά για σύγκριση.' },
  'compare.optionA': { en: '— Island A —', el: '— Νησί Α —' },
  'compare.optionB': { en: '— Island B —', el: '— Νησί Β —' },
  'compare.vs': { en: 'vs', el: 'εναντίον' },
  'compare.clear': { en: 'Clear', el: 'Καθαρισμός' },
  'compare.placeholder': { en: 'Select two islands above to start comparing.', el: 'Επίλεξε δύο νησιά παραπάνω για να αρχίσει η σύγκριση.' },
  'compare.wtv_title':    { en: 'When to visit — overlap', el: 'Πότε να επισκεφτείς — επικάλυψη' },
  'months.short': { en: 'Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec', el: 'Ιαν,Φεβ,Μαρ,Απρ,Μάι,Ιουν,Ιουλ,Αυγ,Σεπ,Οκτ,Νοε,Δεκ' },
  'wtv.tag.avoid':   { en: 'Avoid',   el: 'Αποφύγετε' },
  'wtv.tag.ok':      { en: 'OK',      el: 'ΟΚ' },
  'wtv.tag.great':   { en: 'Great',   el: 'Καλό' },
  'wtv.tag.perfect': { en: 'Best',    el: 'Άριστο' },
  'compare.extra_title':  { en: 'Character & practicalities', el: 'Χαρακτήρας & πρακτικά' },
  'compare.best_for':     { en: 'Best for', el: 'Ιδανικό για' },
  'compare.wtv_both_perfect': { en: 'Both at their best in {months}', el: 'Και τα δύο άριστα: {months}' },
  'compare.wtv_both_good':    { en: 'Both great or better in {months}', el: 'Και τα δύο καλά: {months}' },
  'compare.wtv_no_overlap':   { en: 'No month where both are great — pick one over the other', el: 'Δεν υπάρχει μήνας που και τα δύο είναι καλά' },
  'wtv.perfect': { en: 'Best',    el: 'Άριστο' },
  'wtv.great':   { en: 'Great',   el: 'Καλό' },
  'wtv.ok':      { en: 'OK',      el: 'ΟΚ' },
  'wtv.avoid':   { en: 'Avoid',   el: 'Αποφύγετε' },
  'wtv.limited': { en: 'Limited service', el: 'Περιορισμένη λειτουργία' },

  // Hopping page
  'hopping.title': { en: '🚢 Island Hopping', el: '🚢 Νησοπορία' },
  'hopping.maptitle': { en: 'Ferry network map', el: 'Χάρτης δικτύου πλοίων' },
  'hopping.show':     { en: 'Show', el: 'Εμφάνιση' },
  'hopping.book.label': { en: 'Book ferries', el: 'Κράτηση πλοίων' },
  'hopping.focus.one':   { en: 'connection shown', el: 'σύνδεση' },
  'hopping.focus.many':  { en: 'connections shown', el: 'συνδέσεις' },
  'hopping.focus.guide': { en: 'View island guide', el: 'Δες τον οδηγό' },
  'hopping.focus.clear': { en: 'Show all routes', el: 'Όλες οι διαδρομές' },
  'planner.title':       { en: 'Plan a route', el: 'Σχεδίασε διαδρομή' },
  'planner.intro':       { en: "Pick where you're starting and where you want to go. We'll find the fastest direct or 1-transfer route based on real ferry connections.", el: 'Διάλεξε από πού ξεκινάς και πού θες να πας. Θα βρούμε την πιο γρήγορη απευθείας διαδρομή ή με μία ανταπόκριση, βάσει πραγματικών συνδέσεων.' },
  'planner.from':        { en: 'From', el: 'Από' },
  'planner.to':          { en: 'To', el: 'Προς' },
  'planner.choose':      { en: 'choose', el: 'επίλεξε' },
  'planner.pickfromfirst':{ en: 'pick a starting point first', el: 'διάλεξε πρώτα σημείο εκκίνησης' },
  'planner.find':        { en: 'Find route', el: 'Βρες διαδρομή' },
  'planner.mainland':    { en: 'Mainland ports', el: 'Λιμάνια στεριάς' },
  'planner.islands':     { en: 'Islands', el: 'Νησιά' },
  'planner.pickboth':    { en: 'Pick both a starting point and a destination.', el: 'Διάλεξε σημείο εκκίνησης και προορισμό.' },
  'planner.samepoint':   { en: 'Pick two different ports.', el: 'Διάλεξε δύο διαφορετικά σημεία.' },
  'planner.noroute':     { en: 'No ferry route in our database — these may be served by an indirect route via a major hub like Piraeus or Rhodes.', el: 'Δεν υπάρχει διαδρομή στη βάση μας — μάλλον χρειάζεται μέσω μεγάλου κόμβου όπως ο Πειραιάς ή η Ρόδος.' },
  'planner.direct':      { en: 'Direct', el: 'Απευθείας' },
  'planner.onetransfer': { en: '1 transfer', el: '1 ανταπόκριση' },
  'planner.transfers':   { en: 'transfers', el: 'ανταποκρίσεις' },
  'planner.totaltime':   { en: 'Total time', el: 'Συνολικός χρόνος' },
  'planner.routetype':   { en: 'Route', el: 'Διαδρομή' },
  'planner.totalprice':  { en: 'Approx. price', el: 'Περ. τιμή' },
  'planner.book':        { en: 'Book this trip on Ferryhopper', el: 'Κράτηση στο Ferryhopper' },
  'planner.disclaimer':  { en: 'Durations and prices are approximate; check operator schedules close to your travel date.', el: 'Οι διάρκειες και οι τιμές είναι ενδεικτικές. Ελέγξτε τα δρομολόγια κοντά στην ημερομηνία ταξιδιού.' },
  'planner.freq.high':   { en: 'Multiple daily', el: 'Πολλά ημερησίως' },
  'planner.freq.med':    { en: 'Daily / near-daily', el: 'Καθημερινά' },
  'planner.freq.low':    { en: 'Few per week', el: 'Λίγα/εβδομάδα' },
  'planner.freq.seasonal':{ en: 'Summer only', el: 'Μόνο καλοκαίρι' },
  'hopping.intro': { en: 'The most iconic Greek ferry routes — the backbone of any island-hopping trip. Hover over a line for details, click a port to open its island page.', el: 'Οι πιο εμβληματικές διαδρομές πλοίων στην Ελλάδα. Πέρνα τον κέρσορα πάνω από μια γραμμή για λεπτομέρειες, πάτα σε ένα λιμάνι για να ανοίξεις τη σελίδα του νησιού.' },
  'hopping.crosslink': { en: 'Looking for ferries from mainland Athens to the islands? See our ', el: 'Ψάχνεις πλοία από την ηπειρωτική Ελλάδα προς τα νησιά; Δες τον ' },
  'hopping.crosslink_label': { en: 'complete ferries guide', el: 'πλήρη οδηγό πλοίων' },
  'hopping.legend.high': { en: 'Multiple daily', el: 'Πολλά ημερησίως' },
  'hopping.legend.med': { en: 'Daily / near-daily', el: 'Καθημερινά' },
  'hopping.legend.low': { en: 'Few per week', el: 'Λίγα/εβδομάδα' },
  'hopping.itineraries': { en: 'Suggested Itineraries', el: 'Προτεινόμενες Διαδρομές' },
  'hopping.itin.intro': { en: 'Eight curated multi-island routes — from the classic Cyclades circuit to the quiet Small Cyclades escape. Each uses real ferry connections and shows approximate nights per stop.', el: 'Δέκα επιλεγμένες διαδρομές πολλαπλών νησιών — από την κλασική διαδρομή των Κυκλάδων μέχρι την ήσυχη απόδραση στις Μικρές Κυκλάδες. Όλες χρησιμοποιούν πραγματικές συνδέσεις πλοίων.' },
  'hopping.night': { en: 'night', el: 'βράδυ' },
  'hopping.nights': { en: 'nights', el: 'βράδια' },
  'hopping.visit': { en: 'Visit:', el: 'Επισκέψου:' },
  'hopping.pricetrip': { en: '💶 What does this trip cost? →', el: '💶 Πόσο κοστίζει αυτό το ταξίδι; →' },

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
  'filter.vibes': { en: 'Filters', el: 'Φίλτρα' },
  'vibe.goodnow':     { en: 'Good now', el: 'Καλή εποχή τώρα' },
  'vibe.idealnow':    { en: 'Ideal now', el: 'Ιδανικά τώρα' },
  'vibe.caroptional': { en: 'Car optional', el: 'Αυτοκίνητο προαιρετικό' },
  'vibe.hint':        { en: 'Tap one or more to narrow the map', el: 'Πάτα ένα ή περισσότερα για φιλτράρισμα' },
  'vibe.carfree':  { en: 'Car-free', el: 'Χωρίς αυτοκίνητο' },
  'vibe.remote':   { en: 'Off the radar', el: 'Μακριά από κόσμο' },
  'vibe.budget':   { en: 'Budget-friendly', el: 'Οικονομικό' },
  'vibe.nightlife':{ en: 'Nightlife', el: 'Νυχτερινή ζωή' },
  'vibe.tiny':     { en: 'Under 2,000 people', el: 'Κάτω από 2.000 κατ.' },
  'vibe.drama':    { en: 'Dramatic landscape', el: 'Εντυπωσιακό τοπίο' },
  'vibe.hiking':   { en: 'Serious hiking', el: 'Σοβαρή πεζοπορία' },
  'vibe.springs':  { en: 'Hot springs', el: 'Ιαματικά λουτρά' },
  'vibe.chora':    { en: 'Medieval chora', el: 'Μεσαιωνική χώρα' },
  'vibe.sailing':  { en: 'Sailing hub', el: 'Κόμβος ιστιοπλοΐας' },
  'vibe.airport':  { en: 'Has airport', el: 'Με αεροδρόμιο' },
  'vibe.clear':    { en: 'Clear filters', el: 'Καθαρισμός' },
  'a11y.vibe_filters': { en: 'Toggle vibe filters', el: 'Φίλτρα νησιών' },
  'match.title': { en: 'Match Me', el: 'Βρες το Νησί σου' },
  'match.intro': { en: "Answer 7 quick questions and we'll match you to your ideal islands.", el: 'Απάντησε σε 7 γρήγορες ερωτήσεις και θα σε ταιριάξουμε με τα ιδανικά νησιά για εσένα.' },
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
  'quiz.why.season': { en: 'Perfect season fit', el: 'Ιδανική εποχή' },
  'quiz.why.transport.car': { en: 'Reachable by car', el: 'Προσβάσιμο με αυτοκίνητο' },
  'quiz.why.transport.fly': { en: 'Has airport', el: 'Έχει αεροδρόμιο' },
  'quiz.why.transport.short': { en: 'Short ferry hop', el: 'Κοντινό πλοίο' },

  // Shortlist dimensions (in card)
  'shortlist.dim.beach': { en: 'Beach', el: 'Παραλία' },
  'shortlist.dim.culture': { en: 'Culture', el: 'Πολιτισμός' },
  'shortlist.dim.night': { en: 'Night', el: 'Νυχτερινή' },

  // Mission page
  'mission.title': { en: 'Mission', el: 'Στόχος' },
  'mission.tagline': { en: 'For travellers who want to live the holiday, not plan it.', el: 'Για ταξιδιώτες που θέλουν να ζήσουν τις διακοπές, όχι να τις σχεδιάσουν.' },

  // Section 1 — Why this site exists
  'mission.why.title': { en: 'Why this site exists', el: 'Γιατί υπάρχει αυτή η σελίδα' },
  'mission.why.p1': { en: 'There are 88 islands on Aegean Blueprint. Most guides try to cover all of them, and end up saying nothing useful about any. AI-generated lists read like they were written by someone who has never tasted a tomato.', el: 'Στο Aegean Blueprint υπάρχουν 88 νησιά. Οι περισσότεροι οδηγοί τα καλύπτουν όλα — και καταλήγουν να μη λένε τίποτα χρήσιμο για κανένα. Οι λίστες από AI διαβάζονται σαν να τις έγραψε άνθρωπος που δεν έχει δοκιμάσει ποτέ ντομάτα.' },
  'mission.why.quote': { en: "This site is for people who don't want choices. They want the gist, without the fluff.", el: 'Αυτή η σελίδα είναι για ανθρώπους που δεν θέλουν επιλογές. Θέλουν την ουσία, χωρίς περιττά.' },
  'mission.why.p2': { en: 'Each island page gives you one opinionated recommendation: where to stay, what to do for 2 to 5 days, where to swim, where to eat. Not ten options. One. The one I would pick.', el: 'Κάθε σελίδα νησιού δίνει μία πρόταση με άποψη: πού να μείνεις, τι να κάνεις σε 2 έως 5 μέρες, πού να κολυμπήσεις, πού να φας. Όχι δέκα επιλογές. Μία. Αυτή που θα διάλεγα.' },

  // Section 2 — Built by one person
  'mission.author.title': { en: 'Built by one person', el: 'Φτιαγμένο από έναν άνθρωπο, για ταξιδιώτες' },
  'mission.author.role': { en: 'Founder · Athens', el: 'Δημιουργός · Αθήνα' },
  'mission.author.role2': { en: 'Founder · Athens', el: 'Δημιουργός · Αθήνα' },
  'mission.author.bio': { en: 'Greek, based in Athens. 50+ islands visited over 20+ years. Not a travel influencer, not a sponsored blog. One person writing what he actually thinks.', el: 'Έλληνας, ζω στην Αθήνα. Έχω επισκεφθεί 50+ νησιά σε διάστημα 20+ ετών — κάποια πολλές φορές, κάποια μία και αξέχαστη. Δεν είμαι influencer, δεν δέχομαι χορηγίες. Γράφω αυτά που πραγματικά πιστεύω, με την ίδια γλώσσα που θα μιλούσα σε έναν φίλο.' },
  'mission.author.note': { en: 'The alternative is what everyone else does: aggregate TripAdvisor reviews, run them through an SEO mill, translate the output, and call it a "guide." The writing reads fine. The advice is worthless.', el: 'Η εναλλακτική είναι αυτό που κάνουν όλοι: κριτικές από TripAdvisor, πέρασμα από SEO μηχανή, μετάφραση σε όλες τις γλώσσες, και το λένε «οδηγό». Το κείμενο διαβάζεται μια χαρά. Η συμβουλή έχει μικρή χρησιμότητα.' },
  'mission.author.also.before': { en: "If you're driving in Greece, Stergios also built ", el: 'Αν οδηγείς στην Ελλάδα, ο Στέργιος έχει φτιάξει επίσης το ' },
  'mission.author.also.after':  { en: ' — a Greek motorway toll and route calculator that shows you how much time you\'d lose to save €1 of tolls.', el: ' — υπολογιστή διοδίων και διαδρομών που δείχνει πόσο χρόνο θα χάσεις για να γλιτώσεις €1 από τα διόδια.' },

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
  'mission.scoring.title': { en: 'How we score', el: 'Πώς βαθμολογώ' },
  'mission.scoring.lead': { en: 'Every island gets rated 1 to 5 on five dimensions, plus an overall number and one practical fact (how much you need a car). None of these are computed by an algorithm or scraped from elsewhere — they\'re my own informed judgment, based on having been to most of them or talking to people who live on the rest.', el: 'Κάθε νησί παίρνει βαθμολογία 1 έως 5 σε πέντε διαστάσεις, μαζί με έναν συνολικό αριθμό και ένα πρακτικό στοιχείο (πόσο χρειάζεται αυτοκίνητο). Καμία βαθμολογία δεν προκύπτει από αλγόριθμο και καμία δεν είναι αντιγραμμένη από αλλού — είναι η δική μου κρίση, βασισμένη σε όσα έχω δει ο ίδιος ή σε όσα μου λένε άνθρωποι που ζουν εκεί.' },
  'mission.scoring.honest': { en: "If you want to know why Milos is 4.7 and Tinos is 3.7, the short answer is: I think so, for the reasons below. The longer answer is: disagree with me — I'd rather have that conversation than pretend there's a formula.", el: 'Αν θες να ξέρεις γιατί η Μήλος έχει 4.7 και η Τήνος 3.7, η σύντομη απάντηση είναι: έτσι το κρίνω, για τους λόγους που εξηγώ παρακάτω. Η πιο μακριά απάντηση: διαφώνησε. Προτιμώ αυτή τη συζήτηση από το να προσποιούμαι ότι υπάρχει φόρμουλα.' },

  // Sources
  'mission.sources.title': { en: 'Where the information comes from', el: 'Από πού έρχονται οι πληροφορίες' },
  'mission.sources.visited.t': { en: 'Personal visits.', el: 'Προσωπικές επισκέψεις.' },
  'mission.sources.visited.d': { en: ' 50+ of the 88 islands, most more than once.', el: ' 50+ από τα 88 νησιά, τα περισσότερα παραπάνω από μία φορές.' },
  'mission.sources.local.t': { en: 'Local contacts.', el: 'Ντόπιες γνωριμίες.' },
  'mission.sources.local.d': { en: ' Friends and family who live or summer on specific islands. Kalymnos, Ikaria, Lemnos, Skyros — when I call someone who lives there, their answer beats any guidebook.', el: ' Φίλοι και συγγενείς που ζουν ή παραθερίζουν σε συγκεκριμένα νησιά. Κάλυμνος, Ικαρία, Λήμνος, Σκύρος — όταν παίρνω τηλέφωνο σε κάποιον που ζει εκεί, η απάντησή του μετράει περισσότερο από κάθε οδηγό.' },
  'mission.sources.official.t': { en: 'Official data.', el: 'Επίσημες πηγές.' },
  'mission.sources.official.d': { en: ' Ferry schedules from operators directly. Opening hours from the actual restaurant or museum. Wikipedia for historical facts. Not from SEO-farm aggregators.', el: ' Δρομολόγια απευθείας από τις ακτοπλοϊκές. Ωράρια από τα ίδια τα εστιατόρια και τα μουσεία. Wikipedia για ιστορικά στοιχεία. Όχι από SEO-farm συλλογείς.' },
  'mission.sources.feedback.t': { en: 'Reader corrections.', el: 'Διορθώσεις αναγνωστών.' },
  'mission.sources.feedback.d': { en: ' When someone emails to say a restaurant closed, the page updates. The Feedback button is the loop.', el: ' Όταν κάποιος γράφει ότι έκλεισε ένα εστιατόριο, η σελίδα ενημερώνεται. Το κουμπί Σχόλια κλείνει τον κύκλο.' },

  // Rubric
  'mission.rubric.title': { en: 'The rubric', el: 'Η κλίμακα' },
  'mission.rubric.intro': { en: "Five rated dimensions, each scored 1 to 5, plus a sixth number for car reliance — a fact, not a quality score. Here's what those numbers actually mean.", el: 'Πέντε βαθμολογημένες διαστάσεις, κάθε μία από 1 έως 5, συν έναν έκτο αριθμό για την εξάρτηση από αυτοκίνητο — στοιχείο πληροφορίας, όχι ποιότητας. Να τι σημαίνουν πραγματικά αυτοί οι αριθμοί.' },

  'mission.rubric.beach.name': { en: 'Beach', el: 'Παραλία' },
  'mission.rubric.beach.desc': { en: 'How good the swimming is.', el: 'Πόσο καλό είναι το μπάνιο.' },
  'mission.rubric.beach.5': { en: "You'd pick the island because of the water. Milos, Elafonisos, Lefkada.", el: 'Θα διάλεγες το νησί για τα νερά του. Μήλος, Ελαφόνησος, Λευκάδα.' },
  'mission.rubric.beach.3': { en: "Good beaches exist but they're not the reason to come.", el: 'Καλές παραλίες υπάρχουν αλλά δεν είναι ο λόγος να έρθεις.' },
  'mission.rubric.beach.1': { en: 'Swim at the hotel pool instead.', el: 'Κολύμπα καλύτερα στην πισίνα του ξενοδοχείου.' },

  'mission.rubric.hist.name': { en: 'Culture', el: 'Πολιτισμός' },
  'mission.rubric.hist.desc': { en: 'Archaeology, museums, churches, old towns, living tradition.', el: 'Αρχαιολογία, μουσεία, εκκλησίες, παλιές πόλεις, ζωντανή παράδοση.' },
  'mission.rubric.hist.5': { en: 'Serious depth. Delos, Rhodes Old Town, Patmos.', el: 'Σοβαρό βάθος. Δήλος, Παλιά Πόλη Ρόδου, Πάτμος.' },
  'mission.rubric.hist.3': { en: 'One or two good sites, worth a half-day.', el: 'Ένα-δύο καλά σημεία, αξίζουν μισή μέρα.' },
  'mission.rubric.hist.1': { en: 'The island\'s story is "we have a beach."', el: 'Όλη η ιστορία του νησιού είναι «έχουμε παραλία».' },

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

  'mission.rubric.car.name': { en: 'Car reliance', el: 'Εξάρτηση από αυτοκίνητο' },
  'mission.rubric.car.desc': { en: 'Practical fact, not a quality score. How much a car shapes the trip.', el: 'Πρακτικό στοιχείο, όχι βαθμολογία ποιότητας. Πόσο διαμορφώνει το ταξίδι το αυτοκίνητο.' },
  'mission.rubric.car.5': { en: 'Essential. The island only opens up if you drive. Crete, Naxos, Lefkada.', el: 'Απαραίτητο. Το νησί ανοίγεται μόνο με αυτοκίνητο. Κρήτη, Νάξος, Λευκάδα.' },
  'mission.rubric.car.3': { en: 'Useful but not required. Buses cover the basics; a car opens up beaches.', el: 'Χρήσιμο αλλά όχι απαραίτητο. Τα λεωφορεία καλύπτουν τα βασικά· το αυτοκίνητο ανοίγει παραλίες.' },
  'mission.rubric.car.1': { en: 'Not needed. You walk or take the local bus. Hydra, Koufonisia.', el: 'Δεν χρειάζεται. Πάς με τα πόδια ή με το τοπικό λεωφορείο. Ύδρα, Κουφονήσια.' },

  // Overall
  'mission.overall.title': { en: 'The overall number', el: 'Ο συνολικός αριθμός' },
  'mission.overall.p1': { en: 'The overall number leans most on Beach and Culture — that\'s what most people come for — but it\'s not a formula. A quiet, affordable island with one great beach and one real ruin can outscore a famous one that doesn\'t offer anything unique. <strong>Milos is 4.7, Tinos is 3.7.</strong> I set numbers by judgment, then check them by ranking islands against each other in my head.', el: 'Ο συνολικός αριθμός γέρνει περισσότερο προς την Παραλία και τον Πολιτισμό — γι\' αυτά έρχεται ο περισσότερος κόσμος εδώ — αλλά δεν είναι φόρμουλα. Ένα ήσυχο, οικονομικό νησί με μία πραγματικά ωραία παραλία και ένα αληθινό μνημείο μπορεί να βγει μπροστά από ένα διάσημο που δεν προσφέρει κάτι μοναδικό. <strong>Η Μήλος είναι 4.7, η Τήνος 3.7.</strong> Βάζω τους αριθμούς με την κρίση μου, και τους ξαναβλέπω συγκρίνοντας τα νησιά μεταξύ τους στο μυαλό μου.' },
  'mission.overall.p3': { en: 'Use the five underlying numbers if your trip has a specific goal. The overall is for sorting the table when you don\'t yet know what you want.', el: 'Χρησιμοποίησε τις πέντε επιμέρους διαστάσεις όταν το ταξίδι σου έχει συγκεκριμένο στόχο. Δες τον συνολικό αριθμό όταν ταξινομείς τον πίνακα και δεν έχεις ακόμα αποφασίσει τι θέλεις.' },

  // Updates
  'mission.updates.title': { en: 'How often this changes', el: 'Πόσο συχνά αλλάζει' },
  'mission.updates.p1': { en: "Restaurants close. Ferry operators swap routes. A hotel changes hands and quality drops. Scores themselves rarely shift — an island's personality doesn't change in a season — but the specifics on a page do.", el: 'Τα εστιατόρια κλείνουν. Οι ακτοπλοϊκές αλλάζουν γραμμές. Ένα ξενοδοχείο αλλάζει χέρια και η ποιότητα πέφτει. Οι ίδιες οι βαθμολογίες σπάνια αλλάζουν — ο χαρακτήρας ενός νησιού δεν αλλάζει σε μια σεζόν — αλλά οι λεπτομέρειες στη σελίδα αλλάζουν.' },
  'mission.updates.p2': { en: 'When I get reader feedback or visit an island again, the page updates. When a restaurant I recommended closes, the link comes down within a week. The goal is not to be an encyclopedia — it\'s to be the most current opinionated recommendation you can trust for the next 6 months.', el: 'Όταν λαμβάνω σχόλια από αναγνώστες ή επισκέπτομαι ξανά ένα νησί, η σελίδα ενημερώνεται. Όταν κλείνει ένα εστιατόριο που έχω προτείνει, ο σύνδεσμος κατεβαίνει μέσα σε μια εβδομάδα.' },

  // Limits
  'mission.limits.title': { en: "What the scores can't capture", el: 'Τι δεν μπορούν να δείξουν οι βαθμολογίες' },
  'mission.limits.lead': { en: "Five numbers can't describe an island. A few things they miss:", el: 'Πέντε αριθμοί δεν περιγράφουν ένα νησί. Κάποια πράγματα που χάνουν:' },
  'mission.limits.season': { en: "Season. Ios in July is a 5 for nightlife; Ios in April is a 1. The score reflects the peak.", el: 'Εποχή. Η Ίος τον Ιούλιο είναι 5 στη νυχτερινή ζωή· τον Απρίλιο είναι 1. Ο αριθμός δείχνει την κορύφωση.' },
  'mission.limits.taste': { en: "Personal taste. If you hate parties, Mykonos's high Nightlife score is a warning, not a selling point.", el: 'Προσωπικό γούστο. Αν μισείς τα πάρτι, η ψηλή βαθμολογία Νυχτερινής Ζωής της Μυκόνου είναι προειδοποίηση, όχι πλεονέκτημα.' },
  'mission.limits.crowds': { en: "Crowds. Santorini scores well across the board but feels different when six cruise ships dock the same day. The pages mention this; the numbers don't reflect it.", el: 'Τουριστικός συνωστισμός. Η Σαντορίνη βαθμολογείται καλά παντού, αλλά έχει εντελώς άλλη αίσθηση όταν δένουν έξι κρουαζιερόπλοια την ίδια μέρα. Οι σελίδες το αναφέρουν· οι αριθμοί δεν μπορούν.' },
  'mission.limits.drift': { en: "Drift. A \"must-eat\" restaurant can coast for years on reviews after the original chef leaves. I try to catch these but I'm one person.", el: 'Μετατόπιση. Ένα «must-eat» εστιατόριο μπορεί να εξακολουθεί να συστήνεται χρόνια μετά την αποχώρηση του αρχικού σεφ. Προσπαθώ να τα πιάνω εγκαίρως — εδώ βοηθάνε πολύ τα σχόλια σου.' },

  // Disagree
  'mission.disagree.title': { en: 'Think I got one wrong?', el: 'Πιστεύεις πως κάτι λείπει ή είναι λάθος;' },
  'mission.disagree.text': { en: 'Hit the <strong>💬 Feedback</strong> button at the bottom right of any page and pick <em>"Suggest a rating correction."</em> Explain what you\'d change and why. If you make a good case, I\'ll update the number. The five dimensions and the reasoning stay in the open.', el: 'Πάτα το κουμπί <strong>💬 Σχόλια</strong> κάτω δεξιά σε οποιαδήποτε σελίδα και διάλεξε <em>«Πρόταση διόρθωσης βαθμολογίας»</em>. Εξήγησε τι θα άλλαζες και γιατί. Αν έχω παραλείψει ένα σημαντικό σημείο ή έχω βαθμολογήσει λάθος, η σελίδα διορθώνεται. Έχει συμβεί ήδη αρκετές φορές.' },

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
  'a11y.car_scale': { en: '1 = not needed, 5 = essential', el: '1 = δεν χρειάζεται, 5 = απαραίτητο' },
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
  'kythira': 'Κύθηρα', 'antikythera': 'Αντικύθηρα', 'elafonisos': 'Ελαφόνησος',
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
  'evia-north': 'Εύβοια (Βόρεια)',
  'evia-central': 'Εύβοια (Κεντρική)',
  'evia-south': 'Εύβοια (Νότια)',
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
  'arki': 'Αρκιοί',
  'othonoi': 'Οθωνοί',
  'mathraki': 'Μαθράκι',
  'pserimos': 'Ψέριμος',
  'telendos': 'Τέλενδος',
  'erikousa': 'Ερείκουσα',
  'kastos': 'Καστός',
  'kalamos': 'Κάλαμος',
  'thymaina': 'Θύμαινα',
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

// Turn a beach's raw `facing` value (e.g. 'South — calm water', 'NW',
// 'Northeast-facing') into a full traveler-friendly wind-protection sentence.
// In the Cyclades + most of the Aegean, the dominant summer wind is the
// meltemi (a steady N/NE wind), so a south-facing beach is sheltered, a
// north-facing one is exposed. We render the practical implications.
//
// Lang: 'en' | 'el'. Falls back to returning the raw value if we can't
// classify the direction (e.g. "Various", "Double bay" — rare edge cases
// where the original prose is already clearer than anything we'd generate).
function interpretFacing(rawFacing, lang, islandGroup) {
  if (!rawFacing) return '';
  // Extract the cardinal direction from the start of the string. Data has
  // values like 'South', 'South-facing', 'South — calm water', 'SW', etc.
  // Use a regex separator that requires whitespace around the dash so we
  // don't confuse the dash inside "South-facing" with a separator.
  const head = String(rawFacing)
    .split(/\s+[—–-]\s+/, 1)[0]                                 // drop " — descriptive bit"
    .replace(/[-\s]facing$/i, '')                                // strip a trailing "-facing"
    .trim()
    .toLowerCase();

  // Hybrid/intercardinal directions found in the data map to their nearest
  // canonical 8-point direction so we don't need 16 separate entries.
  const FACING_ALIASES = {
    'south-southwest': 'southwest', 'ssw': 'southwest',
    'west-southwest':  'southwest', 'wsw': 'southwest',
    'south-southeast': 'southeast', 'sse': 'southeast',
    'east-southeast':  'southeast', 'ese': 'southeast',
    'north-northeast': 'northeast', 'nne': 'northeast',
    'east-northeast':  'northeast', 'ene': 'northeast',
    'north-northwest': 'northwest', 'nnw': 'northwest',
    'west-northwest':  'northwest', 'wnw': 'northwest',
  };
  const headNormalized = FACING_ALIASES[head] || head;

  // Mapping: each canonical direction has a full EN+EL sentence describing
  // both what it's sheltered from and what (if anything) it's exposed to.
  const FACING_MAP = {
    'north':     { en: 'North-facing — fully exposed to the meltemi (the dominant summer N/NE wind); often choppy June–September',
                   el: 'Με προσανατολισμό βόρειο — πλήρως εκτεθειμένη στο μελτέμι (τον κυρίαρχο καλοκαιρινό Β/ΒΑ άνεμο)· συχνά αγριεμένη Ιούνιο–Σεπτέμβριο' },
    'n':         { en: 'North-facing — fully exposed to the meltemi (the dominant summer N/NE wind); often choppy June–September',
                   el: 'Με προσανατολισμό βόρειο — πλήρως εκτεθειμένη στο μελτέμι (τον κυρίαρχο καλοκαιρινό Β/ΒΑ άνεμο)· συχνά αγριεμένη Ιούνιο–Σεπτέμβριο' },
    'northeast': { en: 'Northeast-facing — exposed to the meltemi (the dominant summer N/NE wind); often windy on meltemi days',
                   el: 'Με προσανατολισμό βορειοανατολικό — εκτεθειμένη στο μελτέμι (τον κυρίαρχο καλοκαιρινό Β/ΒΑ άνεμο)· συχνά αγριεμένη τις μέρες μελτεμιού' },
    'ne':        { en: 'Northeast-facing — exposed to the meltemi (the dominant summer N/NE wind); often windy on meltemi days',
                   el: 'Με προσανατολισμό βορειοανατολικό — εκτεθειμένη στο μελτέμι (τον κυρίαρχο καλοκαιρινό Β/ΒΑ άνεμο)· συχνά αγριεμένη τις μέρες μελτεμιού' },
    'east':      { en: 'East-facing — mostly sheltered from the meltemi (the summer N/NE wind); can be choppy on the strongest NE days',
                   el: 'Με προσανατολισμό ανατολικό — κυρίως προστατευμένη από το μελτέμι (τον καλοκαιρινό Β/ΒΑ άνεμο)· μπορεί να φουρτουνιάσει τις πιο δυνατές ΒΑ μέρες' },
    'e':         { en: 'East-facing — mostly sheltered from the meltemi (the summer N/NE wind); can be choppy on the strongest NE days',
                   el: 'Με προσανατολισμό ανατολικό — κυρίως προστατευμένη από το μελτέμι (τον καλοκαιρινό Β/ΒΑ άνεμο)· μπορεί να φουρτουνιάσει τις πιο δυνατές ΒΑ μέρες' },
    'southeast': { en: 'Southeast-facing — sheltered from the meltemi (the summer N/NE wind); calm most days, exposed only to rare southern winds',
                   el: 'Με προσανατολισμό νοτιοανατολικό — προστατευμένη από το μελτέμι (τον καλοκαιρινό Β/ΒΑ άνεμο)· ήρεμη τις περισσότερες μέρες, εκτεθειμένη μόνο σε σπάνιους νότιους ανέμους' },
    'se':        { en: 'Southeast-facing — sheltered from the meltemi (the summer N/NE wind); calm most days, exposed only to rare southern winds',
                   el: 'Με προσανατολισμό νοτιοανατολικό — προστατευμένη από το μελτέμι (τον καλοκαιρινό Β/ΒΑ άνεμο)· ήρεμη τις περισσότερες μέρες, εκτεθειμένη μόνο σε σπάνιους νότιους ανέμους' },
    'south':     { en: 'South-facing — sheltered from the meltemi (the summer N/NE wind); calm in summer, exposed only to rare southern winds',
                   el: 'Με προσανατολισμό νότιο — προστατευμένη από το μελτέμι (τον καλοκαιρινό Β/ΒΑ άνεμο)· ήρεμη το καλοκαίρι, εκτεθειμένη μόνο σε σπάνιους νότιους ανέμους' },
    's':         { en: 'South-facing — sheltered from the meltemi (the summer N/NE wind); calm in summer, exposed only to rare southern winds',
                   el: 'Με προσανατολισμό νότιο — προστατευμένη από το μελτέμι (τον καλοκαιρινό Β/ΒΑ άνεμο)· ήρεμη το καλοκαίρι, εκτεθειμένη μόνο σε σπάνιους νότιους ανέμους' },
    'southwest': { en: 'Southwest-facing — sheltered from the meltemi (the summer N/NE wind); calm in summer, exposed only to rare S/SW winds',
                   el: 'Με προσανατολισμό νοτιοδυτικό — προστατευμένη από το μελτέμι (τον καλοκαιρινό Β/ΒΑ άνεμο)· ήρεμη το καλοκαίρι, εκτεθειμένη μόνο σε σπάνιους Ν/ΝΔ ανέμους' },
    'sw':        { en: 'Southwest-facing — sheltered from the meltemi (the summer N/NE wind); calm in summer, exposed only to rare S/SW winds',
                   el: 'Με προσανατολισμό νοτιοδυτικό — προστατευμένη από το μελτέμι (τον καλοκαιρινό Β/ΒΑ άνεμο)· ήρεμη το καλοκαίρι, εκτεθειμένη μόνο σε σπάνιους Ν/ΝΔ ανέμους' },
    'west':      { en: 'West-facing — sheltered from the meltemi (the summer N/NE wind); calm most summer days, sometimes choppy on rare westerly winds',
                   el: 'Με προσανατολισμό δυτικό — προστατευμένη από το μελτέμι (τον καλοκαιρινό Β/ΒΑ άνεμο)· ήρεμη τις περισσότερες καλοκαιρινές μέρες, μερικές φορές φουρτουνιασμένη σε σπάνιους δυτικούς ανέμους' },
    'w':         { en: 'West-facing — sheltered from the meltemi (the summer N/NE wind); calm most summer days, sometimes choppy on rare westerly winds',
                   el: 'Με προσανατολισμό δυτικό — προστατευμένη από το μελτέμι (τον καλοκαιρινό Β/ΒΑ άνεμο)· ήρεμη τις περισσότερες καλοκαιρινές μέρες, μερικές φορές φουρτουνιασμένη σε σπάνιους δυτικούς ανέμους' },
    'northwest': { en: 'Northwest-facing — exposed to the meltemi (the dominant summer N/NE wind); often windy on meltemi days',
                   el: 'Με προσανατολισμό βορειοδυτικό — εκτεθειμένη στο μελτέμι (τον κυρίαρχο καλοκαιρινό Β/ΒΑ άνεμο)· συχνά αγριεμένη τις μέρες μελτεμιού' },
    'nw':        { en: 'Northwest-facing — exposed to the meltemi (the dominant summer N/NE wind); often windy on meltemi days',
                   el: 'Με προσανατολισμό βορειοδυτικό — εκτεθειμένη στο μελτέμι (τον κυρίαρχο καλοκαιρινό Β/ΒΑ άνεμο)· συχνά αγριεμένη τις μέρες μελτεμιού' },
  };


  // Ionian (Eptanisa) islands never see the meltemi — the prevailing summer
  // wind there is the maïstros, a NW afternoon sea breeze (mornings are
  // usually glassy). Same directions, different weather story.
  const FACING_MAP_IONIAN = {
    'north':     { en: "North-facing — open to the Ionian's afternoon maïstros (NW sea breeze); calmest in the morning",
                   el: 'Με προσανατολισμό βόρειο — ανοιχτή στον απογευματινό μαΐστρο (τη ΒΔ θαλάσσια αύρα του Ιονίου)· πιο ήρεμη το πρωί' },
    'northeast': { en: 'Northeast-facing — mostly sheltered from the afternoon maïstros (NW breeze); usually calm',
                   el: 'Με προσανατολισμό βορειοανατολικό — κυρίως προστατευμένη από τον απογευματινό μαΐστρο (ΒΔ αύρα)· συνήθως ήρεμη' },
    'east':      { en: "East-facing — sheltered from the Ionian's afternoon maïstros (NW breeze); typically calm all day",
                   el: 'Με προσανατολισμό ανατολικό — προστατευμένη από τον απογευματινό μαΐστρο του Ιονίου (ΒΔ αύρα)· κατά κανόνα ήρεμη όλη μέρα' },
    'southeast': { en: 'Southeast-facing — well sheltered; calm in summer, exposed only to rare southerlies',
                   el: 'Με προσανατολισμό νοτιοανατολικό — καλά προστατευμένη· ήρεμη το καλοκαίρι, εκτεθειμένη μόνο σε σπάνιους νοτιάδες' },
    'south':     { en: 'South-facing — sheltered from the prevailing NW winds; calm in summer, exposed only to rare southerlies',
                   el: 'Με προσανατολισμό νότιο — προστατευμένη από τους επικρατούντες ΒΔ ανέμους· ήρεμη το καλοκαίρι, εκτεθειμένη μόνο σε σπάνιους νοτιάδες' },
    'southwest': { en: 'Southwest-facing — calm mornings; picks up some of the afternoon maïstros (NW breeze) late in the day',
                   el: 'Με προσανατολισμό νοτιοδυτικό — ήρεμα πρωινά· πιάνει λίγο τον απογευματινό μαΐστρο (ΒΔ αύρα) αργά τη μέρα' },
    'west':      { en: "West-facing — exposed to the afternoon maïstros (the Ionian's NW summer breeze); glassy mornings, waves by late afternoon",
                   el: 'Με προσανατολισμό δυτικό — εκτεθειμένη στον απογευματινό μαΐστρο (τη ΒΔ καλοκαιρινή αύρα του Ιονίου)· λάδι το πρωί, κυματάκι το απόγευμα' },
    'northwest': { en: 'Northwest-facing — head-on to the afternoon maïstros (NW breeze); best swum in the morning',
                   el: 'Με προσανατολισμό βορειοδυτικό — κόντρα στον απογευματινό μαΐστρο (ΒΔ αύρα)· καλύτερη για μπάνιο το πρωί' },
  };
  FACING_MAP_IONIAN['n']=FACING_MAP_IONIAN['north']; FACING_MAP_IONIAN['ne']=FACING_MAP_IONIAN['northeast'];
  FACING_MAP_IONIAN['e']=FACING_MAP_IONIAN['east']; FACING_MAP_IONIAN['se']=FACING_MAP_IONIAN['southeast'];
  FACING_MAP_IONIAN['s']=FACING_MAP_IONIAN['south']; FACING_MAP_IONIAN['sw']=FACING_MAP_IONIAN['southwest'];
  FACING_MAP_IONIAN['w']=FACING_MAP_IONIAN['west']; FACING_MAP_IONIAN['nw']=FACING_MAP_IONIAN['northwest'];

  const activeMap = (islandGroup === 'Ionian') ? FACING_MAP_IONIAN : FACING_MAP;
  const chosen = activeMap[headNormalized];
  if (chosen) return chosen[lang === 'el' ? 'el' : 'en'];
  // Edge cases (e.g. "Various", "Double bay", "All directions") — the original
  // value is usually already a complete prose phrase, so just return it as-is.
  return rawFacing;
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
   ISLANDS_DATA. Example: "Milos is {milos.total}" -> "Milos is 4.7"
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
