# Output schema (one JSON file per island group, path given in your prompt)

{
  "<island-key>": [
    {
      "name": "Panigiri of Agia Marina, Vourkoti",          // EN, specific: saint/event + village
      "name_el": "Πανηγύρι Αγίας Μαρίνας, Βουρκωτή",
      "village": "Vourkoti",                                 // village/town where it happens (EN transliteration)
      "village_el": "Βουρκωτή",
      "date": {"fixed": "07-17"},                            // MM-DD for fixed saint's days / fixed events
              // OR {"movable": "easter", "offset": 50}      // days relative to Orthodox Easter Sunday (Pentecost=+49, Agiou Pnevmatos=+50, Clean Monday=-48, Good Friday=-2, Ascension=+39)
              // OR {"approx": "mid-September, 4 days", "months": [9]}   // only when no fixed date exists
      "eve": true,                                           // true if the main event is the EVE (paramoni) of the saint's day — very common for panigiria
      "duration_days": 1,
      "type": "panigiri",                                    // one of: panigiri (village saint's-day feast with food/music/dance), religious (procession/pilgrimage without feast), music, food (harvest/product festival), carnival, cultural (theatre/arts/summer festival), sport, other
      "desc": "2-3 sentences, EN. What actually happens, why it matters, one practical tip (arrive when, book what, parking). Written for someone deciding whether to plan a trip around it. No marketing fluff.",
      "desc_el": "Same content in Greek. Second-person SINGULAR (Πάτα, Διάλεξε, Βρες — never Πατήστε/Διαλέξτε). Lowercase ethnic/period adjectives (ενετικός, βυζαντινός). Natural Greek, not translated English.",
      "source": "https://…",                                 // the page you got the date/village from (municipality, parish, local news, festival site). REQUIRED.
      "source2": "https://…",                                // optional second source
      "confidence": "high"                                   // high = date+village confirmed by an official or local source for a recent year; medium = widely reported but not officially confirmed; low = single unreliable mention (prefer to omit low)
    }
  ]
}
