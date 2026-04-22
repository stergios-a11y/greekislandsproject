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
  'nav.mission': { en: 'Why This Exists', el: 'Γιατί Υπάρχει' },

  // Hero / homepage
  'hero.title': { en: 'Aegean Blueprint', el: 'Aegean Blueprint' },
  'hero.tagline': { en: 'The Greek Island Decision Engine', el: 'Ο οδηγός για το Ελληνικό νησί που σας ταιριάζει' },
  'hero.dismiss': { en: 'Got it', el: 'Έγινε' },
  'hero.stat.islands': { en: 'Islands', el: 'Νησιά' },
  'hero.stat.dimensions': { en: 'Dimensions', el: 'Διαστάσεις' },
  'hero.stat.minutes': { en: 'Minutes', el: 'Λεπτά' },

  // Search/filter
  'search.placeholder': { en: 'Search islands...', el: 'Αναζήτηση νησιών...' },
  'filter.allgroups': { en: 'All groups', el: 'Όλες οι ομάδες' },
  'filter.rankby': { en: 'Rank map by', el: 'Ταξινόμηση κατά' },
  'filter.overall': { en: 'Overall', el: 'Συνολικά' },
  'filter.beach': { en: 'Beaches', el: 'Παραλίες' },
  'filter.culture': { en: 'Culture', el: 'Πολιτισμός' },
  'filter.night': { en: 'Nightlife', el: 'Νυχτερινή ζωή' },
  'filter.access': { en: 'Access', el: 'Πρόσβαση' },
  'filter.afford': { en: 'Affordability', el: 'Προσιτή τιμή' },

  // Detail page buttons
  'detail.back': { en: '← Back to Map', el: '← Πίσω στον Χάρτη' },
  'detail.compare': { en: '＋ Compare', el: '＋ Σύγκριση' },
  'detail.save': { en: '☆ Save', el: '☆ Αποθήκευση' },
  'detail.saved': { en: '★ Saved', el: '★ Αποθηκεύτηκε' },
  'detail.copylink': { en: '🔗 Copy link', el: '🔗 Αντιγραφή' },
  'detail.print': { en: '🖨 Print / PDF', el: '🖨 Εκτύπωση / PDF' },
  'detail.bookferry': { en: '🚢 Book ferry tickets', el: '🚢 Κράτηση πλοίου' },
  'detail.copied': { en: '✓ Copied!', el: '✓ Αντιγράφτηκε!' },

  // Detail sidebar
  'detail.ratings': { en: 'Blueprint Ratings', el: 'Βαθμολογίες' },
  'detail.keystats': { en: 'Key Stats', el: 'Βασικά Στοιχεία' },
  'detail.area': { en: 'Land Area:', el: 'Έκταση:' },
  'detail.population': { en: 'Population:', el: 'Πληθυσμός:' },
  'detail.group': { en: 'Group:', el: 'Ομάδα:' },
  'detail.suggestedstay': { en: 'Suggested stay:', el: 'Συνιστώμενη παραμονή:' },
  'detail.beaches': { en: 'Top Beaches', el: 'Καλύτερες Παραλίες' },
  'detail.itinerary': { en: 'Itinerary', el: 'Πρόγραμμα' },
  'detail.alldays': { en: 'All days', el: 'Όλες οι μέρες' },
  'detail.day': { en: 'Day', el: 'Ημέρα' },
  'detail.yourrating': { en: 'Your rating', el: 'Η βαθμολογία σου' },
  'detail.editorial': { en: 'Editorial', el: 'Επιμελητής' },

  // Footer
  'footer.copyright': { en: '© 2026 Stergios Gousios · Aegean Blueprint', el: '© 2026 Στέργιος Γούσιος · Aegean Blueprint' },

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
window.islandName = islandName;
window.groupName = groupName;
window.CURRENT_LANG = CURRENT_LANG;
window.applyStaticTranslations = applyStaticTranslations;
