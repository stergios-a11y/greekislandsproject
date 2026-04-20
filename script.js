/* ==========================================================
   Aegean Blueprint — script.js  v2.0
   Upgrades included:
   #1  AI-powered Match Me recommender (quiz + scoring)
   #2  Island comparison with Chart.js radar chart
   #3  Auto-generated Island Hopping pairs (proximity + complementarity)
   #4  Island Group filter chips
   #5  Duplicate koufonisia_main removed from runtime
   #6  All event listeners moved here (no inline onclick in HTML)
   #8  Loading overlay dismissed after data ready
   #9  Mobile-responsive table (card view < 600px handled via CSS)
   ========================================================== */

'use strict';

/* ----------------------------------------------------------
   DATA
---------------------------------------------------------- */
const VERSION = 'v2.0';

// NOTE: koufonisia_main duplicate (#5) is simply not loaded here.
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

// Convert to array with key attached
const ISLANDS = Object.entries(ISLANDS_DATA).map(([key, data]) => ({ key, ...data }));

/* ----------------------------------------------------------
   STATE
---------------------------------------------------------- */
let mapInstance = null;
let mapMarkers = {};
let miniMapInstance = null;
let currentMapMode = 'overall';
let currentGroupFilter = 'all';
let compareSelection = [null, null]; // [keyA, keyB]
let radarChartInstance = null;
let sortState = { col: 'total', asc: false };

const SCORE_DIMS = ['beach', 'hist', 'night', 'access', 'afford'];
const DIM_LABELS = ['Beach', 'Culture', 'Nightlife', 'Access', 'Price'];

const SCORE_COLORS = {
  beach:  '#378ADD',
  hist:   '#1D9E75',
  night:  '#D4537E',
  access: '#BA7517',
  afford: '#7F77DD',
};

/* ----------------------------------------------------------
   UTILITIES
---------------------------------------------------------- */
function scoreToColor(s) {
  if (s >= 4.5) return '#4a9e2f';
  if (s >= 3.8) return '#378ADD';
  if (s >= 3.0) return '#BA7517';
  return '#D85A30';
}

function haversineApprox(a, b) {
  // Fast Euclidean approx sufficient for ferry-proximity (degrees)
  const dlat = a.lat - b.lat;
  const dlng = a.lng - b.lng;
  return Math.sqrt(dlat * dlat + dlng * dlng);
}

function fmt(n, decimals = 1) {
  return Number(n).toFixed(decimals);
}

function fmtNum(n) {
  return Number(n).toLocaleString();
}

/* ----------------------------------------------------------
   INIT
---------------------------------------------------------- */
document.addEventListener('DOMContentLoaded', () => {
  setupNav();
  setupDarkMode();
  setupVibeChips();
  setupGroupFilter();
  setupMap();
  setupTable();
  setupCompare();
  setupHopping();
  setupQuiz();
  document.getElementById('version-display').textContent = `Aegean Blueprint ${VERSION}`;
  dismissLoading();
});

function dismissLoading() {
  const overlay = document.getElementById('loading-overlay');
  if (overlay) {
    setTimeout(() => overlay.classList.add('hidden'), 400);
  }
}

/* ----------------------------------------------------------
   NAVIGATION  (upgrade #6 — no inline onclick)
---------------------------------------------------------- */
const NAV_VIEWS = {
  'nav-home':    'home',
  'nav-map':     'home',
  'nav-data':    'data',
  'nav-compare': 'compare',
  'nav-hopping': 'hopping',
  'nav-match':   'match',
  'nav-mission': 'mission',
};

function setupNav() {
  Object.entries(NAV_VIEWS).forEach(([btnId, view]) => {
    const el = document.getElementById(btnId);
    if (el) el.addEventListener('click', (e) => { e.preventDefault(); handleNav(view); });
  });

  const menuToggle = document.getElementById('menu-toggle-btn');
  if (menuToggle) {
    menuToggle.addEventListener('click', toggleMenu);
  }

  const detailBack = document.getElementById('detail-back-btn');
  if (detailBack) detailBack.addEventListener('click', () => handleNav('home'));

  const detailCmpBtn = document.getElementById('detail-compare-btn');
  if (detailCmpBtn) {
    detailCmpBtn.addEventListener('click', () => {
      const key = detailCmpBtn.dataset.islandKey;
      if (key) addToCompare(key);
      handleNav('compare');
    });
  }
}

function handleNav(view) {
  const homeControls = document.getElementById('home-controls');
  const views = ['home', 'data', 'compare', 'hopping', 'match', 'mission', 'detail'];
  views.forEach(v => {
    const el = document.getElementById(`view-${v}`);
    if (el) el.style.display = 'none';
  });

  const nav = document.getElementById('main-nav');
  if (nav) nav.querySelectorAll('a').forEach(a => a.classList.remove('active'));

  const target = document.getElementById(`view-${view}`);
  if (target) target.style.display = '';

  homeControls.style.display = (view === 'home') ? '' : 'none';

  const navLink = document.getElementById(`nav-${view}`);
  if (navLink) navLink.classList.add('active');

  if (nav && nav.classList.contains('open')) nav.classList.remove('open');

  // Invalidate map size when returning to map
  if (view === 'home' && mapInstance) {
    setTimeout(() => mapInstance.invalidateSize(), 100);
  }
}

function toggleMenu() {
  const nav = document.getElementById('main-nav');
  if (nav) nav.classList.toggle('open');
}

/* ----------------------------------------------------------
   DARK MODE  (upgrade #10)
---------------------------------------------------------- */
function setupDarkMode() {
  const btn = document.getElementById('dark-mode-btn');
  const root = document.documentElement;

  // Respect saved preference
  if (localStorage.getItem('darkMode') === 'true') {
    root.classList.add('dark');
    btn.textContent = '☀';
  }

  btn.addEventListener('click', () => {
    const isDark = root.classList.toggle('dark');
    btn.textContent = isDark ? '☀' : '☾';
    localStorage.setItem('darkMode', isDark);
    // Redraw radar chart if visible
    if (radarChartInstance) renderRadarChart();
  });
}

/* ----------------------------------------------------------
   MAP  (Leaflet)
---------------------------------------------------------- */
function setupMap() {
  mapInstance = L.map('main-map', { zoomControl: true }).setView([37.8, 24.5], 6);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 18,
  }).addTo(mapInstance);

  renderMapMarkers();

  const searchInput = document.getElementById('islandSearch');
  if (searchInput) searchInput.addEventListener('input', filterIslands);
}

function getDisplayScore(island) {
  const modeMap = {
    overall: 'total',
    beach:   'beach',
    hist:    'hist',
    night:   'night',
    access:  'access',
    afford:  'afford',
  };
  return island[modeMap[currentMapMode] || 'total'];
}

function makeMarkerIcon(score) {
  const color = scoreToColor(score);
  const size = Math.round(28 + score * 4);
  return L.divIcon({
    className: 'custom-marker',
    html: `<div style="
      background:${color};
      width:${size}px;height:${size}px;
      border-radius:50%;
      border:2px solid #fff;
      display:flex;align-items:center;justify-content:center;
      font-size:11px;font-weight:700;color:#fff;
      box-shadow:0 1px 4px rgba(0,0,0,.35);
    ">${fmt(score)}</div>`,
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
  });
}

function renderMapMarkers() {
  // Remove existing markers
  Object.values(mapMarkers).forEach(m => mapInstance.removeLayer(m));
  mapMarkers = {};

  const searchTerm = (document.getElementById('islandSearch')?.value || '').toLowerCase();

  ISLANDS.forEach(island => {
    if (searchTerm && !island.name.toLowerCase().includes(searchTerm)) return;
    if (currentGroupFilter !== 'all' && island.island_group !== currentGroupFilter) return;

    const score = getDisplayScore(island);
    const marker = L.marker([island.lat, island.lng], { icon: makeMarkerIcon(score) })
      .addTo(mapInstance)
      .bindPopup(`
        <div style="min-width:160px">
          <strong>${island.name}</strong><br>
          <small style="color:#666">${island.island_group}</small><br>
          <div style="margin-top:6px">Overall: <strong>${fmt(island.total)}</strong></div>
          <div>Beach: ${fmt(island.beach)} · Culture: ${fmt(island.hist)}</div>
          <div>Night: ${fmt(island.night)} · Access: ${fmt(island.access)}</div>
          <div>Price: ${fmt(island.afford)}</div>
          <button onclick="window._openDetail('${island.key}')" style="margin-top:8px;padding:4px 10px;width:100%;cursor:pointer;">View Details</button>
        </div>
      `);

    marker.on('click', () => openDetail(island.key));
    mapMarkers[island.key] = marker;
  });
}

// Expose for popup buttons
window._openDetail = openDetail;

function filterIslands() {
  renderMapMarkers();
}

function updateMapMode(mode) {
  currentMapMode = mode;
  renderMapMarkers();
}

/* ----------------------------------------------------------
   VIBE CHIPS  (upgrade #6)
---------------------------------------------------------- */
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

/* ----------------------------------------------------------
   GROUP FILTER  (upgrade #4)
---------------------------------------------------------- */
function setupGroupFilter() {
  const row = document.getElementById('group-filter-row');
  if (!row) return;

  const groups = ['all', ...new Set(ISLANDS.map(i => i.island_group))].sort((a, b) => {
    if (a === 'all') return -1;
    if (b === 'all') return 1;
    return a.localeCompare(b);
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

/* ----------------------------------------------------------
   ISLAND DETAIL
---------------------------------------------------------- */
function openDetail(key) {
  const island = ISLANDS_DATA[key];
  if (!island) return;

  handleNav('detail');

  document.getElementById('island-name').textContent = island.name;
  document.getElementById('island-meta-info').textContent = `${island.island_group} · ${fmtNum(island.area)} km² · Pop. ${fmtNum(island.pop)}`;

  const compareBtn = document.getElementById('detail-compare-btn');
  if (compareBtn) {
    compareBtn.dataset.islandKey = key;
    compareBtn.textContent = compareSelection.includes(key) ? '✓ In Compare' : '＋ Compare';
  }

  // Ratings
  SCORE_DIMS.forEach(dim => {
    const bar = document.getElementById(`star-${dim}`);
    const val = document.getElementById(`val-${dim}`);
    if (bar) bar.style.width = `${(island[dim] / 5) * 100}%`;
    if (bar) bar.style.background = SCORE_COLORS[dim];
    if (val) val.textContent = fmt(island[dim]);
  });

  document.getElementById('stat-area').textContent = `${fmtNum(island.area)} km²`;
  document.getElementById('stat-pop').textContent = fmtNum(island.pop);
  document.getElementById('stat-group').textContent = island.island_group;

  // Mini map
  const miniMapEl = document.getElementById('island-mini-map');
  if (miniMapEl) {
    if (miniMapInstance) { miniMapInstance.remove(); miniMapInstance = null; }
    miniMapEl.style.height = '220px';
    setTimeout(() => {
      miniMapInstance = L.map(miniMapEl, { zoomControl: false, attributionControl: false })
        .setView([island.lat, island.lng], 9);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(miniMapInstance);
      L.marker([island.lat, island.lng]).addTo(miniMapInstance)
        .bindPopup(island.name).openPopup();
    }, 50);
  }

  // Guide
  const guide = document.getElementById('island-guide');
  if (guide) {
    guide.innerHTML = `
      <div class="island-guide-box">
        <h3>Blueprint Summary</h3>
        <p>
          ${island.name} scores <strong>${fmt(island.total)}/5</strong> overall.
          ${island.beach >= 4.5 ? 'Outstanding beaches make it a top swimming destination. ' : ''}
          ${island.hist >= 4.5 ? 'Exceptional historical and cultural depth. ' : ''}
          ${island.night >= 4.5 ? 'Among the most vibrant nightlife scenes in Greece. ' : ''}
          ${island.afford >= 4.2 ? 'Very budget-friendly compared to most islands. ' : ''}
          ${island.afford <= 1.5 ? 'One of the most expensive islands — budget accordingly. ' : ''}
          ${island.access >= 4.5 ? 'Excellent connections — easy to reach from Athens. ' : ''}
          ${island.access <= 2.0 ? 'Remote and harder to reach — but that is part of the appeal. ' : ''}
        </p>
        <p style="margin-top:8px">
          <a href="#" onclick="window._addCmpNav('${key}')">Compare with another island →</a>
        </p>
      </div>`;
  }
}

window._addCmpNav = function(key) {
  addToCompare(key);
  handleNav('compare');
};

/* ----------------------------------------------------------
   DATA TABLE  (upgrades #6, #9)
---------------------------------------------------------- */
function setupTable() {
  const searchInput = document.getElementById('tableSearchInput');
  if (searchInput) searchInput.addEventListener('input', renderTable);

  // Sort on th click (upgrade #6 — no inline onclick)
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
  let list = ISLANDS.filter(i =>
    !query || i.name.toLowerCase().includes(query) || i.island_group.toLowerCase().includes(query)
  );

  const col = sortState.col;
  const asc = sortState.asc;
  list.sort((a, b) => {
    const av = a[col], bv = b[col];
    if (typeof av === 'string') return asc ? av.localeCompare(bv) : bv.localeCompare(av);
    return asc ? av - bv : bv - av;
  });

  const countLabel = document.getElementById('table-count-label');
  if (countLabel) countLabel.textContent = `${list.length} islands`;

  const tbody = document.getElementById('islands-table-body');
  if (!tbody) return;

  tbody.innerHTML = list.map(i => `
    <tr data-key="${i.key}" class="table-row-clickable">
      <td data-label="Island" style="font-weight:600">${i.name}</td>
      <td data-label="Group"><span class="group-tag">${i.island_group}</span></td>
      <td data-label="Total" style="color:${scoreToColor(i.total)};font-weight:600">${fmt(i.total)}</td>
      <td data-label="Beach">${fmt(i.beach)}</td>
      <td data-label="Culture">${fmt(i.hist)}</td>
      <td data-label="Night">${fmt(i.night)}</td>
      <td data-label="Access">${fmt(i.access)}</td>
      <td data-label="Price">${fmt(i.afford)}</td>
      <td data-label="Area" class="text-right">${fmtNum(i.area)}</td>
      <td data-label="Pop" class="text-right">${fmtNum(i.pop)}</td>
    </tr>`
  ).join('');

  // Row click → detail
  tbody.querySelectorAll('.table-row-clickable').forEach(row => {
    row.addEventListener('click', () => openDetail(row.dataset.key));
  });
}

/* ----------------------------------------------------------
   COMPARE  (upgrade #2)
---------------------------------------------------------- */
function setupCompare() {
  const selA = document.getElementById('compare-select-a');
  const selB = document.getElementById('compare-select-b');
  const clearBtn = document.getElementById('compare-clear-btn');

  if (!selA || !selB) return;

  // Populate dropdowns
  const sorted = [...ISLANDS].sort((a, b) => a.name.localeCompare(b.name));
  sorted.forEach(i => {
    [selA, selB].forEach(sel => {
      const opt = document.createElement('option');
      opt.value = i.key;
      opt.textContent = i.name;
      sel.appendChild(opt);
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
  else compareSelection = [key, compareSelection[1]]; // replace A

  // Sync dropdowns if rendered
  const selA = document.getElementById('compare-select-a');
  const selB = document.getElementById('compare-select-b');
  if (selA && compareSelection[0]) selA.value = compareSelection[0];
  if (selB && compareSelection[1]) selB.value = compareSelection[1];
}

function clearCompare() {
  compareSelection = [null, null];
  const selA = document.getElementById('compare-select-a');
  const selB = document.getElementById('compare-select-b');
  if (selA) selA.value = '';
  if (selB) selB.value = '';
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
  if (!iA) {
    iA = compareSelection[0] ? ISLANDS_DATA[compareSelection[0]] : null;
    iB = compareSelection[1] ? ISLANDS_DATA[compareSelection[1]] : null;
  }
  if (!iA || !iB) return;

  const canvas = document.getElementById('compare-radar-chart');
  if (!canvas) return;

  if (radarChartInstance) radarChartInstance.destroy();

  radarChartInstance = new Chart(canvas, {
    type: 'radar',
    data: {
      labels: DIM_LABELS,
      datasets: [
        {
          label: iA.name,
          data: SCORE_DIMS.map(d => iA[d]),
          backgroundColor: 'rgba(55,138,221,0.15)',
          borderColor: '#378ADD',
          pointBackgroundColor: '#378ADD',
          pointRadius: 4,
        },
        {
          label: iB.name,
          data: SCORE_DIMS.map(d => iB[d]),
          backgroundColor: 'rgba(29,158,117,0.15)',
          borderColor: '#1D9E75',
          pointBackgroundColor: '#1D9E75',
          pointRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          min: 0, max: 5,
          ticks: { stepSize: 1, font: { size: 10 } },
          pointLabels: { font: { size: 12 } },
        },
      },
      plugins: {
        legend: { position: 'bottom', labels: { font: { size: 12 }, boxWidth: 14 } },
      },
    },
  });
}

function renderCompareCards(iA, iB) {
  const container = document.getElementById('compare-cards');
  if (!container) return;

  const card = (island, other) => {
    const isWinner = island.total > other.total;
    return `
      <div class="compare-card${isWinner ? ' compare-winner' : ''}">
        ${isWinner ? '<div class="winner-label">Higher overall score</div>' : ''}
        <h2>${island.name}</h2>
        <div class="compare-meta">${island.island_group} · ${fmtNum(island.area)} km² · Pop. ${fmtNum(island.pop)}</div>
        <div class="compare-total" style="color:${scoreToColor(island.total)}">${fmt(island.total)}<span>/5</span></div>
        <div class="compare-bars">
          ${SCORE_DIMS.map((dim, i) => {
            const wins = island[dim] >= other[dim];
            return `<div class="cmp-bar-row">
              <span class="cmp-dim-label">${DIM_LABELS[i]}</span>
              <div class="cmp-bar-track">
                <div class="cmp-bar-fill" style="width:${(island[dim]/5)*100}%;background:${wins ? SCORE_COLORS[dim] : '#aaa'}"></div>
              </div>
              <span class="cmp-dim-val ${wins ? 'wins' : ''}">${fmt(island[dim])}</span>
            </div>`;
          }).join('')}
        </div>
      </div>`;
  };

  container.innerHTML = card(iA, iB) + card(iB, iA);
}

/* ----------------------------------------------------------
   ISLAND HOPPING  (upgrade #3 — auto-generated)
---------------------------------------------------------- */
function setupHopping() {
  // Will render on nav
}

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

      // Complementarity: islands that are different from each other in interesting ways are better pairs
      const complementarity =
        Math.abs(a.beach - b.beach) +
        Math.abs(a.hist - b.hist) +
        Math.abs(a.night - b.night);
      const avgTotal = (a.total + b.total) / 2;
      const score = avgTotal + complementarity * 0.2;

      pairs.push({ a, b, d, score, avgTotal, complementarity });
    }
  }

  pairs.sort((x, y) => y.score - x.score);
  const top = pairs.slice(0, 14);

  const ferryLabel = d =>
    d < 0.5 ? 'Short ferry (under 45 min)' :
    d < 1.0 ? 'Medium ferry (~1.5 hrs)' :
    d < 1.8 ? 'Ferry ~2–3 hrs' :
    'Longer ferry (~3–4 hrs)';

  const tags = (a, b) => {
    const t = [];
    if (a.beach >= 4.5 && b.hist >= 4.0) t.push(`${a.name}: beaches · ${b.name}: culture`);
    else if (b.beach >= 4.5 && a.hist >= 4.0) t.push(`${b.name}: beaches · ${a.name}: culture`);
    else if (Math.abs(a.night - b.night) >= 1.5) {
      const loud = a.night > b.night ? a : b;
      const quiet = loud === a ? b : a;
      t.push(`${loud.name}: nightlife · ${quiet.name}: relaxation`);
    }
    if ((a.afford + b.afford) / 2 >= 3.8) t.push('Budget-friendly combo');
    if (a.island_group === b.island_group) t.push(`Both in ${a.island_group}`);
    else t.push(`${a.island_group} + ${b.island_group}`);
    return t.slice(0, 3);
  };

  container.innerHTML = top.map(({ a, b, d, avgTotal }) => `
    <div class="hopping-pair">
      <div class="hopping-pair-title">${a.name} + ${b.name}</div>
      <div class="hopping-pair-meta">
        Combined score: <strong>${fmt(avgTotal)}</strong> &bull; ${ferryLabel(d)}
      </div>
      <div class="hopping-tags">
        ${tags(a, b).map(tag => `<span class="hopping-tag">${tag}</span>`).join('')}
      </div>
    </div>`
  ).join('');
}

// Render hopping when navigated to
const origHandleNav = handleNav;
window.addEventListener('DOMContentLoaded', () => {
  const hoppingLink = document.getElementById('nav-hopping');
  if (hoppingLink) {
    hoppingLink.addEventListener('click', () => setTimeout(renderHopping, 50));
  }
});

/* ----------------------------------------------------------
   MATCH ME QUIZ  (upgrade #1)
---------------------------------------------------------- */
const QUIZ_QUESTIONS = [
  {
    question: 'What kind of trip are you planning?',
    options: ['Solo adventure', 'Couple getaway', 'Family vacation', 'Friend group'],
  },
  {
    question: 'What matters most to you?',
    options: ['Beaches & swimming', 'History & culture', 'Nightlife & food', 'Peace & nature'],
  },
  {
    question: 'What is your budget level?',
    options: ['Budget (backpacker)', 'Mid-range', 'Splurge-ready', 'No limit'],
  },
  {
    question: 'How do you feel about crowds?',
    options: ['Love the buzz', 'Some is fine', 'Prefer quiet', 'Must be secluded'],
  },
];

let quizAnswers = {};
let quizStep = 0;

function setupQuiz() {
  renderQuizStep();
}

function renderQuizStep() {
  const container = document.getElementById('quiz-container');
  const results = document.getElementById('quiz-results');
  if (!container) return;

  container.style.display = '';
  if (results) results.style.display = 'none';

  const q = QUIZ_QUESTIONS[quizStep];

  container.innerHTML = `
    <div class="quiz-progress">
      ${QUIZ_QUESTIONS.map((_, i) => `<div class="quiz-dot ${i < quizStep ? 'done' : i === quizStep ? 'current' : ''}"></div>`).join('')}
      <span class="quiz-step-label">${quizStep + 1} / ${QUIZ_QUESTIONS.length}</span>
    </div>
    <div class="quiz-card">
      <div class="quiz-question">${q.question}</div>
      <div class="quiz-options">
        ${q.options.map((opt, i) => `
          <button class="quiz-option ${quizAnswers[quizStep] === i ? 'selected' : ''}" data-idx="${i}">
            ${opt}
          </button>`).join('')}
      </div>
      <div class="quiz-nav">
        ${quizStep > 0 ? `<button class="quiz-back-btn">← Back</button>` : `<span></span>`}
        <button class="quiz-next-btn ${quizAnswers[quizStep] === undefined ? 'disabled' : ''}" ${quizAnswers[quizStep] === undefined ? 'disabled' : ''}>
          ${quizStep === QUIZ_QUESTIONS.length - 1 ? 'Find my islands →' : 'Next →'}
        </button>
      </div>
    </div>`;

  container.querySelectorAll('.quiz-option').forEach(btn => {
    btn.addEventListener('click', () => {
      quizAnswers[quizStep] = parseInt(btn.dataset.idx);
      renderQuizStep();
    });
  });

  const nextBtn = container.querySelector('.quiz-next-btn');
  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      if (quizAnswers[quizStep] === undefined) return;
      if (quizStep < QUIZ_QUESTIONS.length - 1) {
        quizStep++;
        renderQuizStep();
      } else {
        computeQuizResults();
      }
    });
  }

  const backBtn = container.querySelector('.quiz-back-btn');
  if (backBtn) {
    backBtn.addEventListener('click', () => {
      if (quizStep > 0) { quizStep--; renderQuizStep(); }
    });
  }
}

function computeQuizResults() {
  // Priority dim from Q2: beaches, history, nightlife, peaceful (affordable + low crowd)
  const priorityDims = ['beach', 'hist', 'night', 'afford'];
  const priority = priorityDims[quizAnswers[1]] || 'total';

  // Budget modifier: higher afford score = cheaper island
  const budgetMod = [2, 0.5, -0.5, -2][quizAnswers[2]] || 0;

  // Crowd modifier: low pop for secluded preference
  const crowdPref = quizAnswers[3]; // 0=love buzz, 3=secluded

  const scored = ISLANDS
    .filter(i => i.key !== 'athens')
    .map(i => {
      let s = i[priority] * 2.5 + i.total * 1.5;

      // Budget: reward affordable islands if budget-conscious
      if (budgetMod > 0) s += budgetMod * i.afford;
      else if (budgetMod < 0) s += Math.abs(budgetMod) * (5 - i.afford); // reward luxury

      // Crowd: secluded preference rewards small-pop islands
      if (crowdPref >= 2) {
        const popScore = Math.max(0, 4 - Math.log10(i.pop + 1));
        s += crowdPref * popScore * 0.5;
      }

      // Family preference favours access + no wild nightlife
      if (quizAnswers[0] === 2) {
        s += i.access * 0.5;
        if (i.night > 4) s -= 0.5;
      }

      return { ...i, matchScore: s };
    })
    .sort((a, b) => b.matchScore - a.matchScore)
    .slice(0, 6);

  const container = document.getElementById('quiz-container');
  const results = document.getElementById('quiz-results');
  if (!container || !results) return;

  container.style.display = 'none';
  results.style.display = '';

  const dimLabel = ['Beach', 'Culture', 'Nightlife', 'Price-friendly', 'Overall'][quizAnswers[1]] || 'Overall';

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

  results.innerHTML = `
    <div class="quiz-results-header">
      <div class="quiz-results-title">Your top islands</div>
      <div class="quiz-results-sub">Matched on your preferences — click any to explore</div>
    </div>
    ${scored.map((island, idx) => `
      <div class="result-island-card" data-key="${island.key}">
        <div class="result-rank">${idx + 1}</div>
        <div class="result-info">
          <div class="result-name">${island.name}</div>
          <div class="result-why">${whyText(island)}</div>
        </div>
        <div class="result-score" style="color:${scoreToColor(island.total)}">${fmt(island.total)}</div>
      </div>`).join('')}
    <div class="quiz-retake-row">
      <button class="quiz-retake-btn">Retake quiz</button>
    </div>`;

  results.querySelectorAll('.result-island-card').forEach(card => {
    card.addEventListener('click', () => openDetail(card.dataset.key));
  });

  results.querySelector('.quiz-retake-btn').addEventListener('click', () => {
    quizAnswers = {};
    quizStep = 0;
    renderQuizStep();
  });
}
