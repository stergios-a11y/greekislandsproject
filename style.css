'use strict';

const VERSION = 'v3.1';

const ISLANDS_DATA = {
  "athens":       { name:"Athens (Piraeus)", lat:37.983, lng:23.727, beach:2.0, hist:5.0, night:5.0, access:5.0, afford:3.0, total:3.8, area:39,    pop:664000,  island_group:"Saronic" },
  "paros":        { name:"Paros",            lat:37.085, lng:25.148, beach:5.0, hist:3.8, night:5.0, access:4.5, afford:2.2, total:4.1, area:196,   pop:13700,   island_group:"Cyclades" },
  "chania":       { name:"Crete (Chania)",   lat:35.512, lng:24.018, beach:5.0, hist:4.7, night:4.0, access:4.5, afford:3.4, total:4.9, area:2376,  pop:108000,  island_group:"Crete" },
  "heraklion":    { name:"Crete (Heraklion)",lat:35.338, lng:25.131, beach:3.5, hist:5.0, night:4.7, access:5.0, afford:3.5, total:4.3, area:2641,  pop:173000,  island_group:"Crete" },
  "rethymno":     { name:"Crete (Rethymno)", lat:35.367, lng:24.475, beach:3.8, hist:4.5, night:3.8, access:3.5, afford:3.7, total:4.0, area:1496,  pop:34300,   island_group:"Crete" },
  "lasithi":      { name:"Crete (Lasithi)",  lat:35.188, lng:25.715, beach:4.0, hist:3.5, night:3.4, access:3.2, afford:3.2, total:4.0, area:1823,  pop:76000,   island_group:"Crete" },
  "santorini":    { name:"Santorini",        lat:36.393, lng:25.461, beach:3.2, hist:5.0, night:4.2, access:4.7, afford:1.0, total:4.8, area:76,    pop:15500,   island_group:"Cyclades" },
  "milos":        { name:"Milos",            lat:36.732, lng:24.429, beach:5.0, hist:3.5, night:3.0, access:3.2, afford:2.8, total:4.7, area:151,   pop:4900,    island_group:"Cyclades" },
  "rhodes":       { name:"Rhodes",           lat:36.170, lng:27.910, beach:4.2, hist:5.0, night:4.1, access:4.8, afford:3.5, total:4.4, area:1400,  pop:115000,  island_group:"Dodecanese" },
  "naxos":        { name:"Naxos",            lat:37.105, lng:25.376, beach:4.8, hist:4.4, night:3.5, access:3.8, afford:4.0, total:4.5, area:429,   pop:18900,   island_group:"Cyclades" },
  "mykonos":      { name:"Mykonos",          lat:37.446, lng:25.328, beach:4.3, hist:3.0, night:5.0, access:4.8, afford:0.5, total:4.3, area:85,    pop:10100,   island_group:"Cyclades" },
  "corfu":        { name:"Corfu",            lat:39.624, lng:19.921, beach:3.9, hist:4.8, night:4.2, access:4.7, afford:3.2, total:4.2, area:593,   pop:102000,  island_group:"Ionian" },
  "zakynthos":    { name:"Zakynthos",        lat:37.787, lng:20.899, beach:4.8, hist:2.5, night:4.5, access:3.7, afford:3.5, total:4.1, area:405,   pop:40700,   island_group:"Ionian" },
  "kefalonia":    { name:"Kefalonia",        lat:38.175, lng:20.569, beach:4.7, hist:3.2, night:3.2, access:3.5, afford:3.8, total:4.1, area:773,   pop:35800,   island_group:"Ionian" },
  "hydra":        { name:"Hydra",            lat:37.350, lng:23.466, beach:2.2, hist:4.2, night:3.8, access:4.2, afford:1.8, total:4.1, area:52,    pop:2700,    island_group:"Saronic" },
  "folegandros":  { name:"Folegandros",      lat:36.630, lng:24.900, beach:3.9, hist:3.8, night:3.5, access:2.8, afford:2.2, total:4.0, area:32,    pop:765,     island_group:"Cyclades" },
  "koufonisia":   { name:"Koufonisia",       lat:36.930, lng:25.600, beach:5.0, hist:2.0, night:4.0, access:3.0, afford:3.0, total:4.0, area:26,    pop:399,     island_group:"Cyclades" },
  "euboea":       { name:"Euboea",           lat:38.5,   lng:24.0,   beach:3.8, hist:4.0, night:3.0, access:4.9, afford:4.8, total:3.8, area:3684,  pop:210000,  island_group:"Other" },
  "lesvos":       { name:"Lesvos",           lat:39.21,  lng:26.21,  beach:4.0, hist:4.7, night:3.0, access:3.5, afford:4.6, total:4.0, area:1633,  pop:83000,   island_group:"NE Aegean" },
  "chios":        { name:"Chios",            lat:38.368, lng:26.135, beach:3.2, hist:4.7, night:2.5, access:3.2, afford:4.5, total:3.6, area:842,   pop:51000,   island_group:"NE Aegean" },
  "kos":          { name:"Kos",              lat:36.891, lng:27.287, beach:4.0, hist:4.2, night:4.0, access:4.6, afford:3.8, total:3.7, area:287,   pop:33300,   island_group:"Dodecanese" },
  "samos":        { name:"Samos",            lat:37.757, lng:26.702, beach:3.5, hist:4.6, night:3.0, access:3.5, afford:4.2, total:3.3, area:477,   pop:32900,   island_group:"NE Aegean" },
  "lefkada":      { name:"Lefkada",          lat:38.706, lng:20.648, beach:4.9, hist:2.5, night:3.2, access:4.5, afford:4.0, total:3.9, area:335,   pop:22600,   island_group:"Ionian" },
  "syros":        { name:"Syros",            lat:37.444, lng:24.942, beach:2.8, hist:4.3, night:3.5, access:4.5, afford:3.5, total:3.8, area:84,    pop:21500,   island_group:"Cyclades" },
  "lemnos":       { name:"Lemnos",           lat:39.916, lng:25.166, beach:4.3, hist:3.5, night:2.2, access:3.0, afford:4.4, total:3.5, area:476,   pop:16900,   island_group:"NE Aegean" },
  "kalymnos":     { name:"Kalymnos",         lat:36.983, lng:26.983, beach:3.5, hist:4.0, night:3.0, access:3.2, afford:4.2, total:3.5, area:110,   pop:16179,   island_group:"Dodecanese" },
  "thasos":       { name:"Thasos",           lat:40.666, lng:24.666, beach:4.2, hist:3.2, night:3.0, access:3.2, afford:4.1, total:3.7, area:379,   pop:13700,   island_group:"Other" },
  "aegina":       { name:"Aegina",           lat:37.750, lng:23.500, beach:2.5, hist:4.2, night:3.2, access:5.0, afford:3.5, total:3.4, area:87,    pop:13000,   island_group:"Saronic" },
  "tinos":        { name:"Tinos",            lat:37.583, lng:25.166, beach:3.5, hist:4.0, night:3.0, access:4.2, afford:3.2, total:3.7, area:194,   pop:8600,    island_group:"Cyclades" },
  "andros":       { name:"Andros",           lat:37.830, lng:24.930, beach:3.8, hist:4.0, night:2.8, access:4.0, afford:3.2, total:3.7, area:380,   pop:9200,    island_group:"Cyclades" },
  "ikaria":       { name:"Ikaria",           lat:37.600, lng:26.166, beach:4.0, hist:3.0, night:4.5, access:2.5, afford:4.5, total:3.8, area:255,   pop:8400,    island_group:"NE Aegean" },
  "leros":        { name:"Leros",            lat:37.150, lng:26.850, beach:3.2, hist:4.0, night:3.0, access:3.2, afford:4.2, total:3.3, area:53,    pop:7900,    island_group:"Dodecanese" },
  "karpathos":    { name:"Karpathos",        lat:35.583, lng:27.133, beach:4.4, hist:4.0, night:2.2, access:2.0, afford:3.8, total:3.8, area:300,   pop:6200,    island_group:"Dodecanese" },
  "skiathos":     { name:"Skiathos",         lat:39.163, lng:23.490, beach:4.6, hist:2.0, night:4.7, access:4.5, afford:3.0, total:3.9, area:49,    pop:6088,    island_group:"Sporades" },
  "skopelos":     { name:"Skopelos",         lat:39.121, lng:23.726, beach:4.2, hist:3.2, night:2.5, access:2.5, afford:3.8, total:3.6, area:96,    pop:4960,    island_group:"Sporades" },
  "kythira":      { name:"Kythira",          lat:36.250, lng:23.000, beach:4.2, hist:4.5, night:2.5, access:2.5, afford:3.8, total:3.7, area:279,   pop:3973,    island_group:"Other" },
  "patmos":       { name:"Patmos",           lat:37.322, lng:26.545, beach:3.0, hist:4.8, night:2.8, access:2.2, afford:2.5, total:3.6, area:34,    pop:3047,    island_group:"Dodecanese" },
  "poros":        { name:"Poros",            lat:37.510, lng:23.470, beach:3.0, hist:4.2, night:3.5, access:4.8, afford:3.2, total:3.5, area:23,    pop:3993,    island_group:"Saronic" },
  "alonnisos":    { name:"Alonnisos",        lat:39.216, lng:23.916, beach:4.4, hist:3.0, night:2.5, access:2.5, afford:4.0, total:3.8, area:64,    pop:2750,    island_group:"Sporades" },
  "skyros":       { name:"Skyros",           lat:38.866, lng:24.533, beach:4.0, hist:3.8, night:2.8, access:2.5, afford:4.2, total:3.4, area:209,   pop:2994,    island_group:"Sporades" },
  "ithaca":       { name:"Ithaca",           lat:38.366, lng:20.716, beach:3.8, hist:4.9, night:2.5, access:2.5, afford:3.5, total:3.8, area:96,    pop:3231,    island_group:"Ionian" },
  "sifnos":       { name:"Sifnos",           lat:36.966, lng:24.716, beach:3.8, hist:4.0, night:3.2, access:3.5, afford:3.5, total:3.9, area:73,    pop:2625,    island_group:"Cyclades" },
  "symi":         { name:"Symi",             lat:36.583, lng:27.833, beach:3.0, hist:4.8, night:3.5, access:3.5, afford:2.5, total:3.8, area:58,    pop:2590,    island_group:"Dodecanese" },
  "paxos":        { name:"Paxos",            lat:39.200, lng:20.150, beach:4.2, hist:3.0, night:3.5, access:2.8, afford:2.5, total:4.0, area:19,    pop:2300,    island_group:"Ionian" },
  "kea":          { name:"Kea (Tzia)",       lat:37.616, lng:24.333, beach:3.8, hist:3.8, night:3.0, access:4.5, afford:3.0, total:3.5, area:131,   pop:2455,    island_group:"Cyclades" },
  "ios":          { name:"Ios",              lat:36.723, lng:25.281, beach:4.6, hist:2.5, night:5.0, access:3.2, afford:3.5, total:3.9, area:109,   pop:2024,    island_group:"Cyclades" },
  "amorgos":      { name:"Amorgos",          lat:36.833, lng:25.900, beach:4.0, hist:3.8, night:3.5, access:2.5, afford:3.5, total:4.0, area:126,   pop:1973,    island_group:"Cyclades" },
  "kythnos":      { name:"Kythnos",          lat:37.383, lng:24.416, beach:4.2, hist:3.2, night:3.0, access:3.5, afford:3.8, total:3.5, area:100,   pop:1456,    island_group:"Cyclades" },
  "astypalaia":   { name:"Astypalaia",       lat:36.550, lng:26.350, beach:4.0, hist:4.2, night:3.0, access:2.5, afford:3.8, total:3.8, area:97,    pop:1334,    island_group:"Dodecanese" },
  "antiparos":    { name:"Antiparos",        lat:37.000, lng:25.080, beach:4.5, hist:3.0, night:4.0, access:3.5, afford:2.8, total:4.0, area:35,    pop:1211,    island_group:"Cyclades" },
  "serifos":      { name:"Serifos",          lat:37.150, lng:24.483, beach:4.5, hist:3.2, night:3.0, access:3.5, afford:3.8, total:3.9, area:75,    pop:1420,    island_group:"Cyclades" },
  "agistri":      { name:"Agistri",          lat:37.700, lng:23.350, beach:3.5, hist:2.5, night:3.5, access:4.5, afford:4.0, total:3.2, area:13,    pop:1142,    island_group:"Saronic" },
  "nisyros":      { name:"Nisyros",          lat:36.583, lng:27.166, beach:3.0, hist:5.0, night:2.5, access:2.8, afford:4.0, total:3.8, area:41,    pop:1008,    island_group:"Dodecanese" },
  "kimolos":      { name:"Kimolos",          lat:36.800, lng:24.570, beach:4.5, hist:3.2, night:2.5, access:3.0, afford:3.8, total:3.7, area:36,    pop:910,     island_group:"Cyclades" },
  "kastellorizo": { name:"Kastellorizo",     lat:36.140, lng:29.580, beach:2.0, hist:5.0, night:2.8, access:1.2, afford:3.5, total:4.0, area:12,    pop:492,     island_group:"Dodecanese" },
  "sikinos":      { name:"Sikinos",          lat:36.683, lng:25.116, beach:3.5, hist:4.2, night:2.2, access:2.5, afford:4.0, total:3.4, area:42,    pop:273,     island_group:"Cyclades" },
  "anafi":        { name:"Anafi",            lat:36.366, lng:25.766, beach:4.5, hist:3.2, night:2.5, access:2.0, afford:4.2, total:3.9, area:38,    pop:271,     island_group:"Cyclades" },
  "elafonisos":   { name:"Elafonisos",       lat:36.480, lng:22.980, beach:5.0, hist:2.0, night:2.5, access:2.5, afford:3.8, total:4.0, area:19,    pop:1041,    island_group:"Other" },
  "samothrace":   { name:"Samothrace",       lat:40.466, lng:25.533, beach:3.0, hist:4.1, night:2.5, access:1.8, afford:4.5, total:3.2, area:178,   pop:2859,    island_group:"Other" },
  "fournoi":      { name:"Fournoi",          lat:37.580, lng:26.500, beach:3.8, hist:3.0, night:1.8, access:2.0, afford:4.5, total:3.2, area:45,    pop:1459,    island_group:"Other" },
  "spetses":      { name:"Spetses",          lat:37.260, lng:23.130, beach:2.8, hist:4.2, night:4.2, access:4.2, afford:2.0, total:3.7, area:22,    pop:4027,    island_group:"Saronic" },
  "tilos":        { name:"Tilos",            lat:36.416, lng:27.366, beach:3.8, hist:3.5, night:2.0, access:2.2, afford:4.2, total:3.5, area:61,    pop:780,     island_group:"Dodecanese" },
  "leipsoi":      { name:"Leipsoi",          lat:37.300, lng:26.750, beach:4.0, hist:3.0, night:2.0, access:2.5, afford:4.5, total:3.4, area:16,    pop:790,     island_group:"Dodecanese" },
  "halki":        { name:"Halki",            lat:36.220, lng:27.610, beach:3.8, hist:4.0, night:2.0, access:2.5, afford:4.0, total:3.6, area:28,    pop:478,     island_group:"Dodecanese" },
  "meganisi":     { name:"Meganisi",         lat:38.660, lng:20.780, beach:4.0, hist:2.5, night:2.8, access:3.2, afford:3.2, total:3.5, area:22,    pop:1041,    island_group:"Ionian" },
  "ammouliani":   { name:"Ammouliani",       lat:40.332, lng:23.916, beach:4.5, hist:2.0, night:3.0, access:3.0, afford:4.0, total:3.5, area:4,     pop:547,     island_group:"Other" },
  "salamis":      { name:"Salamis",          lat:37.933, lng:23.500, beach:2.0, hist:3.5, night:3.0, access:5.0, afford:4.5, total:2.8, area:95,    pop:39283,   island_group:"Saronic" },
  "therasia":     { name:"Therasia",         lat:36.433, lng:25.350, beach:3.0, hist:3.5, night:1.5, access:3.0, afford:3.5, total:3.1, area:9,     pop:319,     island_group:"Cyclades" },
  "schoinoussa":  { name:"Schoinoussa",      lat:36.866, lng:25.516, beach:4.5, hist:2.0, night:2.5, access:2.5, afford:3.8, total:3.4, area:8,     pop:227,     island_group:"Cyclades" },
  "donousa":      { name:"Donousa",          lat:37.100, lng:25.800, beach:4.5, hist:2.0, night:2.5, access:2.2, afford:3.8, total:3.4, area:13,    pop:167,     island_group:"Cyclades" },
  "kasos":        { name:"Kasos",            lat:35.383, lng:26.916, beach:3.2, hist:3.8, night:1.5, access:1.5, afford:4.5, total:2.8, area:66,    pop:1084,    island_group:"Dodecanese" },
  "agathonisi":   { name:"Agathonisi",       lat:37.466, lng:26.966, beach:3.5, hist:2.0, night:1.5, access:1.8, afford:4.5, total:3.0, area:13,    pop:185,     island_group:"Dodecanese" },
  "gavdos":       { name:"Gavdos",           lat:34.840, lng:24.080, beach:4.8, hist:2.0, night:2.5, access:1.0, afford:4.5, total:2.5, area:33,    pop:152,     island_group:"Crete" }
};

const ISLANDS = Object.entries(ISLANDS_DATA).map(([key, data]) => ({ key, ...data }));

let mapInstance = null;
let mapMarkers = {};
let miniMapInstance = null;
let itineraryMapInstance = null;
let currentMapMode = 'overall';
let currentGroupFilter = 'all';
let compareSelection = [null, null];
let radarChartInstance = null;
let sortState = { col: 'total', asc: false };

const SCORE_DIMS = ['beach', 'hist', 'night', 'access', 'afford'];
const DIM_LABELS = ['Beach', 'Culture', 'Nightlife', 'Access', 'Price'];
const SCORE_COLORS = {
  beach:  '#1B4F8A',
  hist:   '#5A7A3A',
  night:  '#C0522A',
  access: '#C4962A',
  afford: '#7B5EA7',
};

/* ---- Lesvos 6-day itinerary data ---- */
const LESVOS_DAYS = [
  {
    day: 1,
    title: 'Mytilene & the South',
    color: '#1B4F8A',
    stops: [
      { name: 'Mytilene Town',        lat: 39.107, lng: 26.554, desc: 'Arrive, settle in. Walk the waterfront, visit the Byzantine castle.' },
      { name: 'Mytilene Castle',      lat: 39.112, lng: 26.561, desc: 'Medieval fortress with panoramic harbour views.' },
      { name: 'Varia',                lat: 39.083, lng: 26.553, desc: 'Museum of Theophilos & Tériade — two exceptional art museums.' },
      { name: 'Agios Isidoros Beach', lat: 39.033, lng: 26.481, desc: 'Relaxed sandy beach south of the capital. Evening swim.' },
    ],
  },
  {
    day: 2,
    title: 'Plomari & Ouzo Country',
    color: '#C0522A',
    stops: [
      { name: 'Mytilene',             lat: 39.107, lng: 26.554, desc: 'Depart after breakfast.' },
      { name: 'Agiasos',              lat: 39.072, lng: 26.388, desc: 'Charming mountain village with cobbled lanes and a lively carnival tradition.' },
      { name: 'Plomari',              lat: 38.977, lng: 26.371, desc: 'Ouzo capital of Greece. Tour a distillery (Barbayiannis or Varvagiannis).' },
      { name: 'Melinda Beach',        lat: 38.969, lng: 26.337, desc: 'Secluded pebble cove west of Plomari. Swim & lunch.' },
      { name: 'Vatera Beach',         lat: 38.949, lng: 26.193, desc: '8 km of uninterrupted sand — one of the finest beaches in the Aegean.' },
    ],
  },
  {
    day: 3,
    title: 'Sigri & Petrified Forest',
    color: '#5A7A3A',
    stops: [
      { name: 'Vatera',               lat: 38.949, lng: 26.193, desc: 'Depart west.' },
      { name: 'Petrified Forest',     lat: 39.193, lng: 25.934, desc: 'UNESCO-listed petrified forest — 20 million year old trees turned to stone.' },
      { name: 'Sigri',                lat: 39.208, lng: 25.855, desc: 'Westernmost village. Tiny harbour, Natural History Museum of the Lesvos Petrified Forest.' },
      { name: 'Faneromeni Beach',     lat: 39.218, lng: 25.887, desc: 'Wild, windy beach near Sigri — dramatic cliffs and turquoise water.' },
      { name: 'Skala Eresou',         lat: 39.170, lng: 25.965, desc: 'Birthplace of Sappho. Laid-back beach village, stay the night.' },
    ],
  },
  {
    day: 4,
    title: 'Kalloni & the Gulf',
    color: '#C4962A',
    stops: [
      { name: 'Skala Eresou',         lat: 39.170, lng: 25.965, desc: 'Morning coffee on the beach.' },
      { name: 'Kalloni',              lat: 39.212, lng: 26.202, desc: 'Main inland town. Kalloni Gulf is famous for sardines — try them grilled at the port.' },
      { name: 'Skala Kalloni',        lat: 39.178, lng: 26.211, desc: 'Fishing port on the Gulf of Kalloni, a world-class birdwatching site.' },
      { name: 'Parakila',             lat: 39.242, lng: 26.274, desc: 'Quiet village on the northern shore of the gulf.' },
      { name: 'Molyvos (Mithymna)',   lat: 39.372, lng: 26.164, desc: 'Most photogenic village in Lesvos — castle above a stone-cobbled harbour. Stay here.' },
    ],
  },
  {
    day: 5,
    title: 'Molyvos, Petra & the North',
    color: '#7B5EA7',
    stops: [
      { name: 'Molyvos Castle',       lat: 39.376, lng: 26.166, desc: 'Morning walk up to the Byzantine castle. Views over Turkey.' },
      { name: 'Eftalou Hot Springs',  lat: 39.388, lng: 26.187, desc: 'Ottoman-era thermal baths right on the beach. Perfect start to the day.' },
      { name: 'Petra',                lat: 39.327, lng: 26.152, desc: 'Village dominated by a huge rock with a chapel on top — climb for the view.' },
      { name: 'Anaxos Beach',         lat: 39.310, lng: 26.135, desc: 'Long sandy beach with views of Molyvos. Afternoon swim.' },
      { name: 'Lepetymnos Forest',    lat: 39.329, lng: 26.198, desc: 'Pine forest hike with views of both coasts of the island.' },
    ],
  },
  {
    day: 6,
    title: 'Eastern Lesvos & Departure',
    color: '#C0522A',
    stops: [
      { name: 'Mandamados',           lat: 39.308, lng: 26.334, desc: 'Famous for its black icon of Archangel Michael and local pottery.' },
      { name: 'Tsonia Beach',         lat: 39.316, lng: 26.415, desc: 'Remote northern beach accessible by dirt road — pristine and empty.' },
      { name: 'Thermi',               lat: 39.164, lng: 26.611, desc: 'Spa village with natural thermal springs 12 km north of Mytilene.' },
      { name: 'Mytilene Town',        lat: 39.107, lng: 26.554, desc: 'Return to Mytilene. Final lunch at the harbour, depart.' },
    ],
  },
];

function scoreToColor(s) {
  if (s >= 4.5) return '#2E7D32';
  if (s >= 3.8) return '#1B4F8A';
  if (s >= 3.0) return '#C4962A';
  return '#C0522A';
}
function haversineApprox(a, b) {
  const dlat = a.lat - b.lat, dlng = a.lng - b.lng;
  return Math.sqrt(dlat * dlat + dlng * dlng);
}
function fmt(n, decimals = 1) { return Number(n).toFixed(decimals); }
function fmtNum(n) { return Number(n).toLocaleString(); }

/* ============================================================
   URL ROUTING
   Maps:  /                   → home (map)
          /#map                → home
          /#data               → data
          /#compare            → compare
          /#hopping            → hopping
          /#match              → match
          /#mission            → mission
          /#island/lesvos      → island detail page
          /#island/naxos       → island detail page (generic)
============================================================ */
const VIEW_HASH_MAP = {
  '':          'home',
  'map':       'home',
  'data':      'data',
  'compare':   'compare',
  'hopping':   'hopping',
  'match':     'match',
  'mission':   'mission',
};

function parseHash() {
  const hash = window.location.hash.replace('#', '').trim();
  if (!hash) return { view: 'home', param: null };
  if (hash.startsWith('island/')) {
    return { view: 'island', param: hash.replace('island/', '') };
  }
  return { view: VIEW_HASH_MAP[hash] || 'home', param: null };
}

function navigateTo(view, param) {
  let hash = '';
  if (view === 'home') hash = '#map';
  else if (view === 'island') hash = `#island/${param}`;
  else hash = `#${view}`;
  if (window.location.hash !== hash) {
    history.pushState({ view, param }, '', hash);
  }
  showView(view, param);
}

function showView(view, param) {
  const homeControls = document.getElementById('home-controls');
  const allViews = ['home', 'data', 'compare', 'hopping', 'match', 'mission', 'detail'];
  allViews.forEach(v => {
    const el = document.getElementById(`view-${v}`);
    if (el) el.style.display = 'none';
  });
  const nav = document.getElementById('main-nav');
  if (nav) nav.querySelectorAll('a').forEach(a => a.classList.remove('active'));

  if (view === 'island') {
    const el = document.getElementById('view-detail');
    if (el) el.style.display = '';
    homeControls.style.display = 'none';
    if (param) renderIslandPage(param);
    return;
  }

  const target = document.getElementById(`view-${view}`);
  if (target) target.style.display = '';
  homeControls.style.display = (view === 'home') ? '' : 'none';

  const navLink = document.getElementById(`nav-${view}`);
  if (navLink) navLink.classList.add('active');
  if (nav && nav.classList.contains('open')) nav.classList.remove('open');
  if (view === 'home' && mapInstance) setTimeout(() => mapInstance.invalidateSize(), 100);
  if (view === 'hopping') setTimeout(renderHopping, 50);
  if (view === 'match') setupQuizIfNeeded();
}

/* Alias for backward compat */
function handleNav(view, param) { navigateTo(view, param); }
window._openDetail = (key) => navigateTo('island', key);
window._addCmpNav = function(key) { addToCompare(key); navigateTo('compare'); };

document.addEventListener('DOMContentLoaded', () => {
  // Hard fallback: always dismiss loading after 3s no matter what
  const hardFallback = setTimeout(dismissLoading, 3000);

  try { setupNav(); } catch(e) { console.warn('setupNav', e); }
  try { setupDarkMode(); } catch(e) { console.warn('setupDarkMode', e); }
  try { setupVibeChips(); } catch(e) { console.warn('setupVibeChips', e); }
  try { setupGroupFilter(); } catch(e) { console.warn('setupGroupFilter', e); }
  try { setupMap(); } catch(e) { console.warn('setupMap', e); }
  try { setupTable(); } catch(e) { console.warn('setupTable', e); }
  try { setupCompare(); } catch(e) { console.warn('setupCompare', e); }

  const vd = document.getElementById('version-display');
  if (vd) vd.textContent = `Aegean Blueprint ${VERSION}`;

  clearTimeout(hardFallback);
  dismissLoading();

  try {
    const { view, param } = parseHash();
    showView(view, param);
  } catch(e) {
    console.warn('showView on init', e);
    showView('home', null);
  }
});

window.addEventListener('popstate', () => {
  try {
    const { view, param } = parseHash();
    showView(view, param);
  } catch(e) { showView('home', null); }
});

function dismissLoading() {
  const overlay = document.getElementById('loading-overlay');
  if (overlay) {
    overlay.classList.add('hidden');
    // Also force-remove after transition in case classList doesn't trigger CSS
    setTimeout(() => { if (overlay) overlay.style.display = 'none'; }, 600);
  }
}

function setupNav() {
  const navMap = {
    'nav-home':    'home',
    'nav-map':     'home',
    'nav-data':    'data',
    'nav-compare': 'compare',
    'nav-hopping': 'hopping',
    'nav-match':   'match',
    'nav-mission': 'mission',
  };
  Object.entries(navMap).forEach(([btnId, view]) => {
    const el = document.getElementById(btnId);
    if (el) el.addEventListener('click', (e) => { e.preventDefault(); navigateTo(view); });
  });
  const menuToggle = document.getElementById('menu-toggle-btn');
  if (menuToggle) menuToggle.addEventListener('click', toggleMenu);
  const detailBack = document.getElementById('detail-back-btn');
  if (detailBack) detailBack.addEventListener('click', () => navigateTo('home'));
  const detailCmpBtn = document.getElementById('detail-compare-btn');
  if (detailCmpBtn) {
    detailCmpBtn.addEventListener('click', () => {
      const key = detailCmpBtn.dataset.islandKey;
      if (key) addToCompare(key);
      navigateTo('compare');
    });
  }
}

function toggleMenu() {
  const nav = document.getElementById('main-nav');
  if (nav) nav.classList.toggle('open');
}

function setupDarkMode() {
  const btn = document.getElementById('dark-mode-btn');
  const root = document.documentElement;
  if (localStorage.getItem('darkMode') === 'true') {
    root.classList.add('dark');
    btn.textContent = '☀';
  }
  btn.addEventListener('click', () => {
    const isDark = root.classList.toggle('dark');
    btn.textContent = isDark ? '☀' : '☾';
    localStorage.setItem('darkMode', isDark);
    if (radarChartInstance) renderRadarChart();
  });
}

function setupMap() {
  const GREECE_BOUNDS = L.latLngBounds(L.latLng(33.8, 18.5), L.latLng(42.2, 30.2));
  mapInstance = L.map('main-map', {
    zoomControl: true, minZoom: 5, maxZoom: 14,
    maxBounds: GREECE_BOUNDS, maxBoundsViscosity: 0.85,
  });
  mapInstance.fitBounds(GREECE_BOUNDS);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors', maxZoom: 14,
  }).addTo(mapInstance);
  renderMapMarkers();
  const searchInput = document.getElementById('islandSearch');
  if (searchInput) searchInput.addEventListener('input', filterIslands);
}

function getDisplayScore(island) {
  const modeMap = { overall:'total', beach:'beach', hist:'hist', night:'night', access:'access', afford:'afford' };
  return island[modeMap[currentMapMode] || 'total'];
}

function makeMarkerIcon(score) {
  const color = scoreToColor(score);
  const size = Math.round(28 + score * 4);
  return L.divIcon({
    className: 'custom-marker',
    html: `<div style="background:${color};width:${size}px;height:${size}px;border-radius:50%;border:2.5px solid #fff;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#fff;box-shadow:0 2px 6px rgba(0,0,0,.3);">${fmt(score)}</div>`,
    iconSize: [size, size], iconAnchor: [size / 2, size / 2],
  });
}

function renderMapMarkers() {
  Object.values(mapMarkers).forEach(m => mapInstance.removeLayer(m));
  mapMarkers = {};
  const searchTerm = (document.getElementById('islandSearch')?.value || '').toLowerCase();
  ISLANDS.forEach(island => {
    if (searchTerm && !island.name.toLowerCase().includes(searchTerm)) return;
    if (currentGroupFilter !== 'all' && island.island_group !== currentGroupFilter) return;
    const score = getDisplayScore(island);
    const marker = L.marker([island.lat, island.lng], { icon: makeMarkerIcon(score) })
      .addTo(mapInstance)
      .bindPopup(`<div style="min-width:160px;font-family:sans-serif"><strong style="font-size:14px">${island.name}</strong><br><small style="color:#888;text-transform:uppercase;letter-spacing:.5px">${island.island_group}</small><div style="margin-top:8px;font-size:13px">Overall: <strong style="color:${scoreToColor(island.total)}">${fmt(island.total)}</strong></div><div style="font-size:12px;color:#666;margin-top:2px">Beach ${fmt(island.beach)} · Culture ${fmt(island.hist)} · Night ${fmt(island.night)}</div><button onclick="window._openDetail('${island.key}')" style="margin-top:10px;padding:6px 12px;width:100%;cursor:pointer;background:#1B4F8A;color:#fff;border:none;border-radius:6px;font-size:12px;font-weight:600">View details</button></div>`);
    marker.on('click', () => navigateTo('island', island.key));
    mapMarkers[island.key] = marker;
  });
}

function filterIslands() { renderMapMarkers(); }
function updateMapMode(mode) { currentMapMode = mode; renderMapMarkers(); }

function setupVibeChips() {
  const container = document.getElementById('vibe-filters');
  if (!container) return;
  container.querySelectorAll('.vibe-chip').forEach(btn => {
    btn.addEventListener('click', () => {
      container.querySelectorAll('.vibe-chip').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      updateMapMode(btn.dataset.mode);
    });
  });
}

function setupGroupFilter() {
  const row = document.getElementById('group-filter-row');
  if (!row) return;
  const groups = ['all', ...new Set(ISLANDS.map(i => i.island_group))].sort((a, b) => {
    if (a === 'all') return -1; if (b === 'all') return 1; return a.localeCompare(b);
  });
  groups.forEach(group => {
    const btn = document.createElement('button');
    btn.className = 'group-chip' + (group === 'all' ? ' active' : '');
    btn.textContent = group === 'all' ? 'All Groups' : group;
    btn.dataset.group = group;
    btn.addEventListener('click', () => {
      row.querySelectorAll('.group-chip').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentGroupFilter = group;
      renderMapMarkers();
    });
    row.appendChild(btn);
  });
}

/* ============================================================
   ISLAND DETAIL / ITINERARY PAGE
============================================================ */
function renderIslandPage(key) {
  const island = ISLANDS_DATA[key];
  if (!island) return;

  document.getElementById('island-name').textContent = island.name;
  document.getElementById('island-meta-info').textContent = `${island.island_group} · ${fmtNum(island.area)} km² · Pop. ${fmtNum(island.pop)}`;

  const compareBtn = document.getElementById('detail-compare-btn');
  if (compareBtn) {
    compareBtn.dataset.islandKey = key;
    compareBtn.textContent = compareSelection.includes(key) ? '✓ In Compare' : '＋ Compare';
  }

  SCORE_DIMS.forEach(dim => {
    const bar = document.getElementById(`star-${dim}`);
    const val = document.getElementById(`val-${dim}`);
    if (bar) { bar.style.width = `${(island[dim] / 5) * 100}%`; bar.style.background = SCORE_COLORS[dim]; }
    if (val) val.textContent = fmt(island[dim]);
  });
  document.getElementById('stat-area').textContent = `${fmtNum(island.area)} km²`;
  document.getElementById('stat-pop').textContent = fmtNum(island.pop);
  document.getElementById('stat-group').textContent = island.island_group;

  const guide = document.getElementById('island-guide');
  if (!guide) return;

  if (key === 'lesvos') {
    guide.innerHTML = buildLesvosItinerary();
    setTimeout(() => initItineraryMap(), 80);
  } else {
    // Generic mini-map + summary for other islands
    const miniMapEl = document.getElementById('island-mini-map');
    if (miniMapEl) {
      if (miniMapInstance) { miniMapInstance.remove(); miniMapInstance = null; }
      miniMapEl.style.height = '220px';
      setTimeout(() => {
        miniMapInstance = L.map(miniMapEl, { zoomControl: false, attributionControl: false }).setView([island.lat, island.lng], 9);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(miniMapInstance);
        L.marker([island.lat, island.lng]).addTo(miniMapInstance).bindPopup(island.name).openPopup();
      }, 50);
    }
    guide.innerHTML = `<div class="island-guide-box"><h3>Blueprint Summary</h3><p>${island.name} scores <strong>${fmt(island.total)}/5</strong> overall.${island.beach >= 4.5 ? ' Outstanding beaches.' : ''}${island.hist >= 4.5 ? ' Exceptional culture and history.' : ''}${island.night >= 4.5 ? ' Among the best nightlife in Greece.' : ''}${island.afford >= 4.2 ? ' Very affordable.' : ''}${island.afford <= 1.5 ? ' One of the most expensive islands — budget accordingly.' : ''}${island.access >= 4.5 ? ' Excellent connections from Athens.' : ''}${island.access <= 2.0 ? ' Remote and harder to reach — but worth the effort.' : ''}</p><p style="margin-top:10px"><a href="#" onclick="window._addCmpNav('${key}')">Compare with another island →</a></p></div>`;
  }
}

function buildLesvosItinerary() {
  const legendItems = LESVOS_DAYS.map(d =>
    `<span class="itin-legend-item"><span class="itin-legend-dot" style="background:${d.color}"></span>Day ${d.day}: ${d.title}</span>`
  ).join('');

  const dayCards = LESVOS_DAYS.map(d => {
    const stops = d.stops.map((s, i) =>
      `<div class="itin-stop">
        <div class="itin-stop-num" style="background:${d.color}">${i + 1}</div>
        <div class="itin-stop-content">
          <div class="itin-stop-name">${s.name}</div>
          <div class="itin-stop-desc">${s.desc}</div>
        </div>
      </div>`
    ).join('');
    return `<div class="itin-day-card">
      <div class="itin-day-header" style="border-left:4px solid ${d.color}">
        <span class="itin-day-label" style="color:${d.color}">Day ${d.day}</span>
        <span class="itin-day-title">${d.title}</span>
      </div>
      <div class="itin-stops">${stops}</div>
    </div>`;
  }).join('');

  return `
    <div class="itin-wrapper">
      <div class="itin-hero">
        <h2 class="itin-title">6-Day Lesvos Itinerary</h2>
        <p class="itin-subtitle">A complete circuit of the island — from the Aegean's ouzo capital to the birthplace of Sappho, medieval castles to petrified forests.</p>
      </div>
      <div class="itin-map-wrap">
        <div id="itin-map"></div>
        <div class="itin-legend">${legendItems}</div>
      </div>
      <div class="itin-days">${dayCards}</div>
    </div>`;
}

function initItineraryMap() {
  const mapEl = document.getElementById('itin-map');
  if (!mapEl) return;
  if (itineraryMapInstance) { itineraryMapInstance.remove(); itineraryMapInstance = null; }

  itineraryMapInstance = L.map(mapEl, { zoomControl: true, attributionControl: true });
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors', maxZoom: 14,
  }).addTo(itineraryMapInstance);

  const allCoords = LESVOS_DAYS.flatMap(d => d.stops.map(s => [s.lat, s.lng]));
  const bounds = L.latLngBounds(allCoords);
  itineraryMapInstance.fitBounds(bounds, { padding: [30, 30] });

  LESVOS_DAYS.forEach(day => {
    const coords = day.stops.map(s => [s.lat, s.lng]);

    // Draw route polyline for this day
    L.polyline(coords, {
      color: day.color,
      weight: 4,
      opacity: 0.85,
      dashArray: null,
    }).addTo(itineraryMapInstance);

    // Draw stop markers
    day.stops.forEach((stop, i) => {
      const icon = L.divIcon({
        className: 'custom-marker',
        html: `<div style="background:${day.color};width:28px;height:28px;border-radius:50%;border:2.5px solid #fff;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#fff;box-shadow:0 2px 6px rgba(0,0,0,.35);">${i + 1}</div>`,
        iconSize: [28, 28], iconAnchor: [14, 14],
      });
      L.marker([stop.lat, stop.lng], { icon })
        .addTo(itineraryMapInstance)
        .bindPopup(`<div style="min-width:180px;font-family:sans-serif"><div style="font-size:11px;font-weight:700;color:${day.color};text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px">Day ${day.day} · Stop ${i + 1}</div><strong style="font-size:14px">${stop.name}</strong><p style="font-size:12px;color:#555;margin:6px 0 0;line-height:1.5">${stop.desc}</p></div>`);
    });
  });
}

/* ============================================================
   DATA TABLE
============================================================ */
function setupTable() {
  const searchInput = document.getElementById('tableSearchInput');
  if (searchInput) searchInput.addEventListener('input', renderTable);
  const thead = document.querySelector('#islands-table thead');
  if (thead) {
    thead.querySelectorAll('th[data-col]').forEach(th => {
      th.addEventListener('click', () => {
        const col = th.dataset.col;
        if (sortState.col === col) sortState.asc = !sortState.asc;
        else { sortState.col = col; sortState.asc = false; }
        renderTable();
      });
    });
  }
  renderTable();
}

function renderTable() {
  const query = (document.getElementById('tableSearchInput')?.value || '').toLowerCase();
  let list = ISLANDS.filter(i => !query || i.name.toLowerCase().includes(query) || i.island_group.toLowerCase().includes(query));
  const col = sortState.col, asc = sortState.asc;
  list.sort((a, b) => {
    const av = a[col], bv = b[col];
    if (typeof av === 'string') return asc ? av.localeCompare(bv) : bv.localeCompare(av);
    return asc ? av - bv : bv - av;
  });
  const countLabel = document.getElementById('table-count-label');
  if (countLabel) countLabel.textContent = `${list.length} islands`;
  const tbody = document.getElementById('islands-table-body');
  if (!tbody) return;
  tbody.innerHTML = list.map(i => `<tr data-key="${i.key}" class="table-row-clickable"><td data-label="Island" style="font-weight:600">${i.name}</td><td data-label="Group"><span class="group-tag">${i.island_group}</span></td><td data-label="Total" style="color:${scoreToColor(i.total)};font-weight:600">${fmt(i.total)}</td><td data-label="Beach">${fmt(i.beach)}</td><td data-label="Culture">${fmt(i.hist)}</td><td data-label="Night">${fmt(i.night)}</td><td data-label="Access">${fmt(i.access)}</td><td data-label="Price">${fmt(i.afford)}</td><td data-label="Area" class="text-right">${fmtNum(i.area)}</td><td data-label="Pop" class="text-right">${fmtNum(i.pop)}</td></tr>`).join('');
  tbody.querySelectorAll('.table-row-clickable').forEach(row => {
    row.addEventListener('click', () => navigateTo('island', row.dataset.key));
  });
}

/* ============================================================
   COMPARE
============================================================ */
function setupCompare() {
  const selA = document.getElementById('compare-select-a');
  const selB = document.getElementById('compare-select-b');
  const clearBtn = document.getElementById('compare-clear-btn');
  if (!selA || !selB) return;
  const sorted = [...ISLANDS].sort((a, b) => a.name.localeCompare(b.name));
  sorted.forEach(i => {
    [selA, selB].forEach(sel => {
      const opt = document.createElement('option');
      opt.value = i.key; opt.textContent = i.name; sel.appendChild(opt);
    });
  });
  selA.addEventListener('change', () => { compareSelection[0] = selA.value || null; renderCompareView(); });
  selB.addEventListener('change', () => { compareSelection[1] = selB.value || null; renderCompareView(); });
  if (clearBtn) clearBtn.addEventListener('click', clearCompare);
}

function addToCompare(key) {
  if (compareSelection.includes(key)) return;
  if (!compareSelection[0]) compareSelection[0] = key;
  else if (!compareSelection[1]) compareSelection[1] = key;
  else compareSelection = [key, compareSelection[1]];
  const selA = document.getElementById('compare-select-a');
  const selB = document.getElementById('compare-select-b');
  if (selA && compareSelection[0]) selA.value = compareSelection[0];
  if (selB && compareSelection[1]) selB.value = compareSelection[1];
}

function clearCompare() {
  compareSelection = [null, null];
  const selA = document.getElementById('compare-select-a');
  const selB = document.getElementById('compare-select-b');
  if (selA) selA.value = ''; if (selB) selB.value = '';
  renderCompareView();
}

function renderCompareView() {
  const iA = compareSelection[0] ? ISLANDS_DATA[compareSelection[0]] : null;
  const iB = compareSelection[1] ? ISLANDS_DATA[compareSelection[1]] : null;
  const placeholder = document.getElementById('compare-placeholder');
  const content = document.getElementById('compare-content');
  if (!iA || !iB) {
    if (placeholder) placeholder.style.display = '';
    if (content) content.style.display = 'none';
    if (radarChartInstance) { radarChartInstance.destroy(); radarChartInstance = null; }
    return;
  }
  if (placeholder) placeholder.style.display = 'none';
  if (content) content.style.display = '';
  renderRadarChart(iA, iB);
  renderCompareCards(iA, iB);
}

function renderRadarChart(iA, iB) {
  if (!iA) { iA = compareSelection[0] ? ISLANDS_DATA[compareSelection[0]] : null; iB = compareSelection[1] ? ISLANDS_DATA[compareSelection[1]] : null; }
  if (!iA || !iB) return;
  const canvas = document.getElementById('compare-radar-chart');
  if (!canvas) return;
  if (radarChartInstance) radarChartInstance.destroy();
  radarChartInstance = new Chart(canvas, {
    type: 'radar',
    data: {
      labels: DIM_LABELS,
      datasets: [
        { label: iA.name, data: SCORE_DIMS.map(d => iA[d]), backgroundColor: 'rgba(27,79,138,0.12)', borderColor: '#1B4F8A', pointBackgroundColor: '#1B4F8A', pointRadius: 4 },
        { label: iB.name, data: SCORE_DIMS.map(d => iB[d]), backgroundColor: 'rgba(196,150,42,0.12)', borderColor: '#C4962A', pointBackgroundColor: '#C4962A', pointRadius: 4 },
      ],
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: { r: { min: 0, max: 5, ticks: { stepSize: 1, font: { size: 10 } }, pointLabels: { font: { size: 12 } } } },
      plugins: { legend: { position: 'bottom', labels: { font: { size: 12 }, boxWidth: 14 } } },
    },
  });
}

function renderCompareCards(iA, iB) {
  const container = document.getElementById('compare-cards');
  if (!container) return;
  const card = (island, other) => {
    const isWinner = island.total > other.total;
    return `<div class="compare-card${isWinner ? ' compare-winner' : ''}">${isWinner ? '<div class="winner-label">Higher overall score</div>' : ''}<h2>${island.name}</h2><div class="compare-meta">${island.island_group} · ${fmtNum(island.area)} km² · Pop. ${fmtNum(island.pop)}</div><div class="compare-total" style="color:${scoreToColor(island.total)}">${fmt(island.total)}<span>/5</span></div><div class="compare-bars">${SCORE_DIMS.map((dim, i) => { const wins = island[dim] >= other[dim]; return `<div class="cmp-bar-row"><span class="cmp-dim-label">${DIM_LABELS[i]}</span><div class="cmp-bar-track"><div class="cmp-bar-fill" style="width:${(island[dim]/5)*100}%;background:${wins ? SCORE_COLORS[dim] : '#bbb'}"></div></div><span class="cmp-dim-val ${wins ? 'wins' : ''}">${fmt(island[dim])}</span></div>`; }).join('')}</div></div>`;
  };
  container.innerHTML = card(iA, iB) + card(iB, iA);
}

/* ============================================================
   HOPPING
============================================================ */
function setupHopping() {}

function renderHopping() {
  const container = document.getElementById('hopping-list');
  if (!container || container.dataset.rendered) return;
  container.dataset.rendered = '1';
  const eligible = ISLANDS.filter(i => i.key !== 'athens' && i.total >= 3.5);
  const pairs = [];
  for (let i = 0; i < eligible.length; i++) {
    for (let j = i + 1; j < eligible.length; j++) {
      const a = eligible[i], b = eligible[j];
      const d = haversineApprox(a, b);
      if (d < 0.3 || d > 2.8) continue;
      const complementarity = Math.abs(a.beach - b.beach) + Math.abs(a.hist - b.hist) + Math.abs(a.night - b.night);
      const avgTotal = (a.total + b.total) / 2;
      pairs.push({ a, b, d, score: avgTotal + complementarity * 0.2, avgTotal });
    }
  }
  pairs.sort((x, y) => y.score - x.score);
  const ferryLabel = d => d < 0.5 ? 'Short ferry (under 45 min)' : d < 1.0 ? 'Medium ferry (~1.5 hrs)' : d < 1.8 ? 'Ferry ~2–3 hrs' : 'Longer ferry (~3–4 hrs)';
  const tags = (a, b) => {
    const t = [];
    if (a.beach >= 4.5 && b.hist >= 4.0) t.push(`${a.name}: beaches · ${b.name}: culture`);
    else if (b.beach >= 4.5 && a.hist >= 4.0) t.push(`${b.name}: beaches · ${a.name}: culture`);
    else if (Math.abs(a.night - b.night) >= 1.5) { const loud = a.night > b.night ? a : b; const quiet = loud === a ? b : a; t.push(`${loud.name}: nightlife · ${quiet.name}: relaxation`); }
    if ((a.afford + b.afford) / 2 >= 3.8) t.push('Budget-friendly combo');
    t.push(a.island_group === b.island_group ? `Both in ${a.island_group}` : `${a.island_group} + ${b.island_group}`);
    return t.slice(0, 3);
  };
  container.innerHTML = pairs.slice(0, 14).map(({ a, b, d, avgTotal }) => `<div class="hopping-pair"><div class="hopping-pair-title">${a.name} + ${b.name}</div><div class="hopping-pair-meta">Combined score: <strong>${fmt(avgTotal)}</strong> &bull; ${ferryLabel(d)}</div><div class="hopping-tags">${tags(a, b).map(tag => `<span class="hopping-tag">${tag}</span>`).join('')}</div></div>`).join('');
}

/* ============================================================
   QUIZ
============================================================ */
const QUIZ_QUESTIONS = [
  { question: 'What kind of trip are you planning?', options: ['Solo adventure', 'Couple getaway', 'Family vacation', 'Friend group'] },
  { question: 'What matters most to you?', options: ['Beaches & swimming', 'History & culture', 'Nightlife & food', 'Peace & nature'] },
  { question: 'What is your budget level?', options: ['Budget (backpacker)', 'Mid-range', 'Splurge-ready', 'No limit'] },
  { question: 'How do you feel about crowds?', options: ['Love the buzz', 'Some is fine', 'Prefer quiet', 'Must be secluded'] },
];
let quizAnswers = {};
let quizStep = 0;
let quizInitialized = false;

function setupQuizIfNeeded() {
  if (!quizInitialized) { quizInitialized = true; renderQuizStep(); }
}

function renderQuizStep() {
  const container = document.getElementById('quiz-container');
  const results = document.getElementById('quiz-results');
  if (!container) return;
  container.style.display = '';
  if (results) results.style.display = 'none';
  const q = QUIZ_QUESTIONS[quizStep];
  container.innerHTML = `<div class="quiz-progress">${QUIZ_QUESTIONS.map((_, i) => `<div class="quiz-dot ${i < quizStep ? 'done' : i === quizStep ? 'current' : ''}"></div>`).join('')}<span class="quiz-step-label">${quizStep + 1} / ${QUIZ_QUESTIONS.length}</span></div><div class="quiz-card"><div class="quiz-question">${q.question}</div><div class="quiz-options">${q.options.map((opt, i) => `<button class="quiz-option ${quizAnswers[quizStep] === i ? 'selected' : ''}" data-idx="${i}">${opt}</button>`).join('')}</div><div class="quiz-nav">${quizStep > 0 ? `<button class="quiz-back-btn">← Back</button>` : `<span></span>`}<button class="quiz-next-btn ${quizAnswers[quizStep] === undefined ? 'disabled' : ''}" ${quizAnswers[quizStep] === undefined ? 'disabled' : ''}>${quizStep === QUIZ_QUESTIONS.length - 1 ? 'Find my islands →' : 'Next →'}</button></div></div>`;
  container.querySelectorAll('.quiz-option').forEach(btn => {
    btn.addEventListener('click', () => { quizAnswers[quizStep] = parseInt(btn.dataset.idx); renderQuizStep(); });
  });
  const nextBtn = container.querySelector('.quiz-next-btn');
  if (nextBtn) nextBtn.addEventListener('click', () => {
    if (quizAnswers[quizStep] === undefined) return;
    if (quizStep < QUIZ_QUESTIONS.length - 1) { quizStep++; renderQuizStep(); } else { computeQuizResults(); }
  });
  const backBtn = container.querySelector('.quiz-back-btn');
  if (backBtn) backBtn.addEventListener('click', () => { if (quizStep > 0) { quizStep--; renderQuizStep(); } });
}

function computeQuizResults() {
  const priorityDims = ['beach', 'hist', 'night', 'afford'];
  const priority = priorityDims[quizAnswers[1]] || 'total';
  const budgetMod = [2, 0.5, -0.5, -2][quizAnswers[2]] || 0;
  const crowdPref = quizAnswers[3];
  const scored = ISLANDS.filter(i => i.key !== 'athens').map(i => {
    let s = i[priority] * 2.5 + i.total * 1.5;
    if (budgetMod > 0) s += budgetMod * i.afford;
    else if (budgetMod < 0) s += Math.abs(budgetMod) * (5 - i.afford);
    if (crowdPref >= 2) s += crowdPref * Math.max(0, 4 - Math.log10(i.pop + 1)) * 0.5;
    if (quizAnswers[0] === 2) { s += i.access * 0.5; if (i.night > 4) s -= 0.5; }
    return { ...i, matchScore: s };
  }).sort((a, b) => b.matchScore - a.matchScore).slice(0, 6);
  const container = document.getElementById('quiz-container');
  const results = document.getElementById('quiz-results');
  if (!container || !results) return;
  container.style.display = 'none'; results.style.display = '';
  const dimLabel = ['Beach', 'Culture', 'Nightlife', 'Price-friendly'][quizAnswers[1]] || 'Overall';
  const whyText = (island) => {
    const reasons = [];
    if (island[priority] >= 4.5) reasons.push(`Top ${dimLabel.toLowerCase()} score (${fmt(island[priority])})`);
    else if (island[priority] >= 3.8) reasons.push(`Strong ${dimLabel.toLowerCase()} (${fmt(island[priority])})`);
    if (budgetMod > 0 && island.afford >= 4) reasons.push('Very affordable');
    if (crowdPref >= 2 && island.pop < 5000) reasons.push('Low crowds');
    if (island.access >= 4.5) reasons.push('Easy to reach');
    if (!reasons.length) reasons.push(`Overall score ${fmt(island.total)}`);
    return reasons.slice(0, 2).join(' · ');
  };
  results.innerHTML = `<div class="quiz-results-header"><div class="quiz-results-title">Your top islands</div><div class="quiz-results-sub">Matched on your preferences — click any to explore</div></div>${scored.map((island, idx) => `<div class="result-island-card" data-key="${island.key}"><div class="result-rank">${idx + 1}</div><div class="result-info"><div class="result-name">${island.name}</div><div class="result-why">${whyText(island)}</div></div><div class="result-score" style="color:${scoreToColor(island.total)}">${fmt(island.total)}</div></div>`).join('')}<div class="quiz-retake-row"><button class="quiz-retake-btn">Retake quiz</button></div>`;
  results.querySelectorAll('.result-island-card').forEach(card => { card.addEventListener('click', () => navigateTo('island', card.dataset.key)); });
  results.querySelector('.quiz-retake-btn').addEventListener('click', () => { quizAnswers = {}; quizStep = 0; renderQuizStep(); });
}
