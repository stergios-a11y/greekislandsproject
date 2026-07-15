# Next-steps / parked ideas

_Dev notes only — this folder is not deployed to the site._

## Trip Cost Calculator → Decision Engine  _(parked 2026-07-16, ster's idea)_

**The pitch:** turn the site into a decision engine — "build your week, book your
tickets, get your car, see the total." Cost is the last unanswered question before
someone books; right now they leave the site to answer it. This is the moment of
maximum booking intent and finally gives the **Ferryhopper affiliate (still unwired)**
and **Discover Cars** real conversion surface (per-line-item "Book this →" beats a
generic header button). SEO prize: "greek island hopping cost", "how much is a week
in santorini" — real query families nobody answers with actual numbers. Also
programmatic "What a week in X costs" sections per island.

**Guiding principle — ranges, never fake precision.** No live-price APIs, so output
must be a range with visible assumptions, e.g. "€1,240–€1,610 for two, September —
mid-range rooms, one taverna meal/day." Frame it as "an honest estimate, not a quote —
here's where to get the real price" → affiliate click. Keeps the data-honest brand.

**We're closer than it looks — reusable pieces already in the codebase:**
- `ISLANDS_DATA` in `script.js` (~line 44, ~88 islands): each has `afford` (1–5,
  Santorini 1.0 = priciest, cheaper islands ~4–5), suggested `days`, `car_need`,
  `has_airport`, etc. → source for accommodation/car band derivation.
- `FERRY_ROUTES` in `script.js` (~line 3548, ~170 routes): objects
  `{a,b,dur,freq,plo,phi,note}` with real **price ranges** (plo/phi).
- `findFerryRoute(from,to)` returns `{hops:[{to,dur,freq,plo,phi,note}]}` — shortest
  path with per-hop €plo–phi already computed. **Ferry leg of the calculator is
  basically free** — just sum the hops. Ports in `MAINLAND_PORTS` / `ISLANDS_DATA`,
  helpers `allFerryPorts()`, `portDisplayName()`, `reachableFrom()`.
- Ferryhopper deep-link pattern already used: `detail-ferry-btn` →
  `https://www.ferryhopper.com/en/ferries-to/{slug}` (slug map at script.js ~1495).

**New data layer needed:** accommodation/meals/car nightly bands. Approach (matches
how the honest scores work): coarse programmatic bands — budget/mid/comfort ×
low/shoulder/peak season — derived from `afford`, then hand-tune outliers
(Santorini, Mykonos). Meals/day fairly flat; car/day flat-ish.

**Staged rollout:**
1. **v1** — cost model + estimator page. Inputs: pick islands → nights → party size →
   month → car toggle → itemized range + booking CTAs. Reuses route-planner logic.
2. **v2** — trip-builder integration: "Add to trip" on island pages/map, a trip bar
   like the existing shortlist, shareable trip URL (great for couples deciding
   together = free distribution).
3. **v3** — deep links with dates/ports pre-filled into Ferryhopper checkout.

**Open design decisions (deferred by ster on 2026-07-16, "build later"):**
- Placement: new SPA nav view ("Plan & Cost") vs standalone `/cost` page vs extend
  the Island Hopping view (where ferry logic already lives).
- Band-setting: auto-derive from `afford` + tune later, vs draft full band table for
  review before wiring.
- v1 target: full working estimator vs example-trip mock first
  (Athens→Paros→Naxos→back, 7 nights, 2 people, August) to validate output format.

**Honest risk:** 88 islands × seasonal bands is a new dataset that can go stale.
Mitigation: keep bands coarse and derived; layer judgment on top.
