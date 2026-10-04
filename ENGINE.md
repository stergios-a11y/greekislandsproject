# Engine & markets

One engine, many island/destination guides. A **market** (e.g. `greece`) is a folder of
data, theme and a few templates; the engine builds a complete static site from it.

## Build

    python3 tools/build.py                      # validate → build every page → smoke test
    MARKET=croatia python3 tools/build.py       # another market
    python3 tools/smoke.py --browser            # optional: real-browser check of every page type

`build.py` stops at the first failure. Don't push a build that ends in ✗.
Browser mode needs Playwright once: `pip3 install playwright && python3 -m playwright install chromium`.

## Where things live

| Path | What |
|---|---|
| `markets/<m>/market.json` | languages, brand (name, URL, author, analytics, colours, logo), menus, UI strings, **features** on/off |
| `markets/<m>/destinations.json` | one entry per destination: name, lat/lng, scores 0–5, days, group, flags |
| `markets/<m>/clusters.json`, `home.json` | map clusters; homepage picks |
| `markets/<m>/theme.css` | palette + fonts (light and dark) — the only CSS a market writes |
| `markets/<m>/ferries.json` | ferry graph, ports, map lines, booking slugs, international routes, itineraries (feature `ferries`) |
| `markets/<m>/festivals.json` | festival master list (feature `festivals`) |
| `markets/<m>/costs.csv`, `cost-rules.csv` | trip-cost inputs (feature `trip_cost`) |
| `markets/<m>/templates/` | market-only template overrides (ads, affiliate buttons) |
| `islands/<key>.json` | the guide per destination: intro, itinerary days/stops, beaches, when to visit |
| `templates/` | engine page markup (`{{placeholders}}`) |
| `tools/` | engine: `build.py`, `validate.py`, `smoke.py`, `market.py`, `shell.py`, `prerender.py`, `build_*.py` |
| `tools/content/` | content import helpers (batches, photos, coordinate audit) |
| `tools/archive/` | finished one-offs, reference only |
| `market-data.js` | **generated** browser copy of the market data — never edit |

## New market checklist

1. `markets/<m>/market.json` — copy Greece's, change languages, brand, menus, strings; switch off features you don't have.
2. `destinations.json`, `clusters.json`, `home.json` — your destinations.
3. `theme.css` — your palette and fonts (every token Greece defines).
4. `islands/<key>.json` for each destination (same schema as Greece).
5. Optional: `ferries.json`, `festivals.json`, cost CSVs, `templates/partials/*` overrides.
6. `MARKET=<m> python3 tools/validate.py` until 0 errors, then build and smoke test.

Still Greece-specific inside the engine (to generalise during the pilot): `index.html` /
`el/index.html` (hand-kept SPA shells), parts of the copy inside `script.js`, `i18n.js` and
`prerender.py`, and the quiz questions. Each market is meant to be its own repo/site (copy the
engine, add one market folder): `islands/` and the generated pages sit at the root, so two
markets don't share one checkout.
