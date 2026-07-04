'use strict';

const VERSION = 'v4.0';
const BUILD_DATE = '2026-07-04';   // Updated by tools/prerender.py on each deploy

// Booking.com affiliate config.
// Replace BOOKING_AID with your real AID once your booking.com affiliate account
// is approved (apply at https://www.booking.com/affiliate-program/).
// Add island keys to BOOKING_ENABLED_ISLANDS to enable the "Book hotel" button
// on those islands. Leave this list narrow until you've measured click-through
// on a couple of pages.
//
// Safety: the placeholder AID '0000000' is rejected at render time. Even if
// an island is in BOOKING_ENABLED_ISLANDS, the Booking link will not render
// while the AID is still the placeholder — clicks would otherwise go to
// Booking.com with a non-existent affiliate ID and earn no commission.
const BOOKING_AID = '0000000';   // <-- swap when you have your real AID
const BOOKING_PLACEHOLDER_AID = '0000000';
const BOOKING_ENABLED_ISLANDS = new Set([
  // Add island keys here once BOOKING_AID is a real ID.
  // Started with 'santorini' — re-enable when ready.
]);
const BOOKING_READY = (BOOKING_AID && BOOKING_AID !== BOOKING_PLACEHOLDER_AID);

const ISLANDS_DATA = {
  "lefkada":      { name:"Lefkada",          lat:38.706, lng:20.648, beach:4.9, hist:2.5, night:3.2, access:4.5, afford:4.0, car_need:4.0, has_airport:true, total:4.0, area:335,   pop:22600,   days:4, island_group:"Ionian", drama:false, hiking:true, springs:false, chora:false, sailing:true },
  "meganisi":     { name:"Meganisi",         lat:38.643, lng:20.783, beach:4.0, hist:2.5, night:2.8, access:3.2, afford:3.2, car_need:3.0, has_airport:false, total:3.5, area:22,    pop:1041,    days:2, island_group:"Ionian", drama:false, hiking:false, springs:false, chora:false, sailing:true },
  "ithaca":       { name:"Ithaca",           lat:38.41, lng:20.69, beach:3.8, hist:4.9, night:2.5, access:2.5, afford:3.5, car_need:4.0, has_airport:false, total:3.8, area:96,    pop:3231,    days:3, island_group:"Ionian", drama:false, hiking:true, springs:false, chora:false, sailing:true },
  "kefalonia":    { name:"Kefalonia",        lat:38.175, lng:20.569, beach:4.7, hist:3.2, night:3.2, access:3.5, afford:3.8, car_need:5.0, has_airport:true, total:4.1, area:773,   pop:35800,   days:5, island_group:"Ionian", drama:false, hiking:true, springs:false, chora:false, sailing:true },
  "zakynthos":    { name:"Zakynthos",        lat:37.79, lng:20.77, beach:4.8, hist:2.5, night:4.5, access:3.7, afford:3.5, car_need:4.0, has_airport:true, total:4.1, area:405,   pop:40700,   days:4, island_group:"Ionian", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "kythira":      { name:"Kythira",          lat:36.250, lng:23.000, beach:4.2, hist:4.5, night:2.5, access:2.5, afford:3.8, car_need:5.0, has_airport:true, total:3.8, area:279,   pop:3973,    days:4, island_group:"Ionian", drama:false, hiking:true, springs:false, chora:false, sailing:false },
  "antikythera":  { name:"Antikythera",      lat:35.862, lng:23.306, beach:3.5, hist:4.5, night:1.0, access:1.0, afford:3.5, car_need:2.5, has_airport:false, total:3.0, area:20,    pop:40,      days:2, island_group:"Ionian", drama:false, hiking:true, springs:false, chora:false, sailing:false },
  "elafonisos":   { name:"Elafonisos",       lat:36.485, lng:22.99, beach:5.0, hist:2.0, night:2.5, access:2.5, afford:3.8, car_need:1.0, has_airport:false, total:4.0, area:19,    pop:1041,    days:2, island_group:"Other", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "paros":        { name:"Paros",            lat:37.06, lng:25.2, beach:5.0, hist:3.8, night:5.0, access:4.5, afford:2.2, car_need:3.0, has_airport:true, total:4.1, area:196,   pop:13700,   days:3, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:true },
  "chania":       { name:"Crete (Chania)",   lat:35.32, lng:23.9, beach:5.0, hist:4.7, night:4.0, access:4.5, afford:3.4, car_need:5.0, has_airport:true, total:4.8, area:2376,  pop:108000,  days:5, island_group:"Crete", drama:false, hiking:true, springs:false, chora:false, sailing:false },
  "heraklion":    { name:"Crete (Heraklion)",lat:35.15, lng:25.1, beach:3.5, hist:5.0, night:4.7, access:5.0, afford:3.5, car_need:5.0, has_airport:true, total:4.2, area:2641,  pop:173000,  days:5, island_group:"Crete", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "rethymno":     { name:"Crete (Rethymno)", lat:35.25, lng:24.55, beach:3.8, hist:4.5, night:3.8, access:3.5, afford:3.7, car_need:5.0, has_airport:false, total:3.8, area:1496,  pop:34300,   days:4, island_group:"Crete", drama:false, hiking:true, springs:false, chora:false, sailing:false },
  "lasithi":      { name:"Crete (Lasithi)",  lat:35.15, lng:25.9, beach:4.0, hist:3.5, night:3.4, access:3.2, afford:3.2, car_need:5.0, has_airport:true, total:4.0, area:1823,  pop:76000,   days:4, island_group:"Crete", drama:false, hiking:true, springs:false, chora:false, sailing:false },
  "santorini":    { name:"Santorini",        lat:36.393, lng:25.461, beach:3.2, hist:5.0, night:4.2, access:4.7, afford:1.0, car_need:3.0, has_airport:true, total:4.8, area:76,    pop:15500,   days:3, island_group:"Cyclades", drama:true, hiking:false, springs:false, chora:false, sailing:false },
  "milos":        { name:"Milos",            lat:36.74, lng:24.43, beach:5.0, hist:3.5, night:3.0, access:3.2, afford:2.8, car_need:4.0, has_airport:true, total:4.7, area:151,   pop:4900,    days:4, island_group:"Cyclades", drama:true, hiking:false, springs:false, chora:false, sailing:false },
  "rhodes":       { name:"Rhodes",           lat:36.170, lng:27.910, beach:4.2, hist:5.0, night:4.1, access:4.8, afford:3.5, car_need:5.0, has_airport:true, total:4.4, area:1400,  pop:115000,  days:5, island_group:"Dodecanese", drama:false, hiking:false, springs:false, chora:true, sailing:true },
  "naxos":        { name:"Naxos",            lat:37.05, lng:25.49, beach:4.8, hist:4.4, night:3.5, access:3.8, afford:4.0, car_need:4.0, has_airport:true, total:4.5, area:429,   pop:18900,   days:4, island_group:"Cyclades", drama:false, hiking:true, springs:false, chora:true, sailing:true },
  "mykonos":      { name:"Mykonos",          lat:37.45, lng:25.37, beach:4.3, hist:3.0, night:5.0, access:4.8, afford:1.0, car_need:4.0, has_airport:true, total:4.3, area:85,    pop:10100,   days:3, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:true },
  "corfu":        { name:"Corfu",            lat:39.62, lng:19.86, beach:3.9, hist:4.8, night:4.2, access:4.7, afford:3.2, car_need:4.0, has_airport:true, total:4.2, area:593,   pop:102000,  days:5, island_group:"Ionian", drama:false, hiking:false, springs:false, chora:false, sailing:true },


  "hydra":        { name:"Hydra",            lat:37.34, lng:23.48, beach:2.2, hist:4.2, night:3.8, access:4.2, afford:1.8, car_need:1.0, has_airport:false, total:4.0, area:52,    pop:2700,    days:2, island_group:"Saronic", drama:false, hiking:false, springs:false, chora:false, sailing:true },
  "folegandros":  { name:"Folegandros",      lat:36.630, lng:24.900, beach:3.9, hist:3.8, night:3.5, access:2.8, afford:2.2, car_need:3.0, has_airport:false, total:4.0, area:32,    pop:765,     days:3, island_group:"Cyclades", drama:true, hiking:false, springs:false, chora:true, sailing:false },
  "koufonisia":   { name:"Koufonisia",       lat:36.945, lng:25.6, beach:5.0, hist:2.0, night:4.0, access:3.0, afford:3.0, car_need:1.0, has_airport:false, total:4.0, area:26,    pop:399,     days:3, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "evia-north":   { name:"Evia (North)",     lat:38.850, lng:23.200, beach:3.8, hist:3.5, night:2.5, access:4.5, afford:4.8, car_need:5.0, has_airport:false, total:3.6, area:1200,  pop:48000,   days:3, island_group:"Evia", drama:false, hiking:true, springs:true, chora:false, sailing:false },
  "evia-central": { name:"Evia (Central)",   lat:38.500, lng:23.850, beach:3.5, hist:4.5, night:3.5, access:5.0, afford:4.6, car_need:5.0, has_airport:false, total:3.9, area:1700,  pop:120000,  days:3, island_group:"Evia", drama:false, hiking:true, springs:false, chora:false, sailing:false },
  "evia-south":   { name:"Evia (South)",     lat:38.016, lng:24.420, beach:4.2, hist:3.5, night:2.5, access:4.5, afford:4.5, car_need:5.0, has_airport:false, total:3.9, area:780,   pop:42000,   days:3, island_group:"Evia", drama:false, hiking:true, springs:false, chora:false, sailing:false },
  "lesvos":       { name:"Lesvos",           lat:39.21,  lng:26.21,  beach:4.0, hist:4.7, night:3.0, access:3.5, afford:4.6, car_need:5.0, has_airport:true, total:4.0, area:1633,  pop:83000,   days:6, island_group:"NE Aegean", drama:false, hiking:true, springs:true, chora:true, sailing:false },
  "chios":        { name:"Chios",            lat:38.37, lng:25.995, beach:3.2, hist:4.7, night:2.5, access:3.2, afford:4.5, car_need:4.0, has_airport:true, total:3.6, area:842,   pop:51000,   days:4, island_group:"NE Aegean", drama:false, hiking:false, springs:false, chora:true, sailing:false },
  "kos":          { name:"Kos",              lat:36.82, lng:27.1, beach:4.0, hist:4.2, night:4.0, access:4.6, afford:3.8, car_need:4.0, has_airport:true, total:3.7, area:287,   pop:33300,   days:4, island_group:"Dodecanese", drama:false, hiking:false, springs:false, chora:false, sailing:true },
  "samos":        { name:"Samos",            lat:37.74, lng:26.8, beach:3.5, hist:4.6, night:3.0, access:3.5, afford:4.2, car_need:4.0, has_airport:true, total:3.3, area:477,   pop:32900,   days:4, island_group:"NE Aegean", drama:false, hiking:true, springs:false, chora:false, sailing:false },

  "syros":        { name:"Syros",            lat:37.44, lng:24.91, beach:2.8, hist:4.3, night:3.5, access:4.5, afford:3.5, car_need:3.0, has_airport:true, total:3.8, area:84,    pop:21500,   days:2, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "lemnos":       { name:"Lemnos",           lat:39.916, lng:25.166, beach:4.3, hist:3.5, night:2.2, access:3.0, afford:4.4, car_need:4.0, has_airport:true, total:3.7, area:476,   pop:16900,   days:3, island_group:"NE Aegean", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "agios-efstratios": { name:"Agios Efstratios", lat:39.515, lng:25.007, beach:4.5, hist:2.8, night:1.5, access:1.5, afford:4.5, car_need:1.0, has_airport:false, total:3.3, area:43,    pop:270,     days:1, island_group:"NE Aegean", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "psara":        { name:"Psara",            lat:38.55, lng:25.54, beach:3.8, hist:3.5, night:1.5, access:1.5, afford:4.2, car_need:1.0, has_airport:false, total:3.0, area:40,    pop:450,     days:1, island_group:"NE Aegean", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "oinousses":    { name:"Oinousses",        lat:38.520, lng:26.202, beach:3.5, hist:3.2, night:1.8, access:2.0, afford:4.0, car_need:1.0, has_airport:false, total:3.0, area:14,    pop:820,     days:1, island_group:"NE Aegean", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "iraklia":      { name:"Iraklia",          lat:36.84, lng:25.448, beach:4.2, hist:2.5, night:1.5, access:2.0, afford:4.3, car_need:1.0, has_airport:false, total:3.2, area:18,    pop:140,     days:1, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "kalymnos":     { name:"Kalymnos",         lat:36.983, lng:26.983, beach:3.5, hist:4.0, night:3.0, access:3.2, afford:4.2, car_need:4.0, has_airport:true, total:3.5, area:110,   pop:16179,   days:3, island_group:"Dodecanese", drama:false, hiking:true, springs:false, chora:false, sailing:false },
  "thasos":       { name:"Thasos",           lat:40.666, lng:24.666, beach:4.2, hist:3.2, night:3.0, access:3.2, afford:4.1, car_need:4.0, has_airport:false, total:3.7, area:379,   pop:13700,   days:3, island_group:"Other", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "aegina":       { name:"Aegina",           lat:37.750, lng:23.500, beach:2.5, hist:4.2, night:3.2, access:5.0, afford:3.5, car_need:3.0, has_airport:false, total:3.3, area:87,    pop:13000,   days:1, island_group:"Saronic", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "tinos":        { name:"Tinos",            lat:37.583, lng:25.166, beach:3.5, hist:4.0, night:3.0, access:4.2, afford:3.2, car_need:4.0, has_airport:false, total:3.7, area:194,   pop:8600,    days:2, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "andros":       { name:"Andros",           lat:37.830, lng:24.930, beach:3.8, hist:4.0, night:2.8, access:4.0, afford:3.2, car_need:4.0, has_airport:false, total:3.7, area:380,   pop:9200,    days:3, island_group:"Cyclades", drama:false, hiking:true, springs:false, chora:true, sailing:false },
  "ikaria":       { name:"Ikaria",           lat:37.600, lng:26.166, beach:4.0, hist:3.0, night:4.5, access:2.5, afford:4.5, car_need:4.0, has_airport:true, total:3.8, area:255,   pop:8400,    days:4, island_group:"NE Aegean", drama:true, hiking:true, springs:true, chora:false, sailing:false },
  "leros":        { name:"Leros",            lat:37.150, lng:26.850, beach:3.2, hist:4.0, night:3.0, access:3.2, afford:4.2, car_need:3.0, has_airport:true, total:3.3, area:53,    pop:7900,    days:2, island_group:"Dodecanese", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "karpathos":    { name:"Karpathos",        lat:35.583, lng:27.133, beach:4.4, hist:4.0, night:2.2, access:2.0, afford:3.8, car_need:5.0, has_airport:true, total:3.8, area:300,   pop:6200,    days:4, island_group:"Dodecanese", drama:true, hiking:true, springs:false, chora:false, sailing:false },
  "skiathos":     { name:"Skiathos",         lat:39.165, lng:23.47, beach:4.6, hist:2.0, night:4.7, access:4.5, afford:3.0, car_need:3.0, has_airport:true, total:3.9, area:49,    pop:6088,    days:3, island_group:"Sporades", drama:false, hiking:false, springs:false, chora:false, sailing:true },
  "skopelos":     { name:"Skopelos",         lat:39.12, lng:23.7, beach:4.2, hist:3.2, night:2.5, access:2.5, afford:3.8, car_need:4.0, has_airport:false, total:3.6, area:96,    pop:4960,    days:3, island_group:"Sporades", drama:false, hiking:true, springs:false, chora:false, sailing:true },
  "patmos":       { name:"Patmos",           lat:37.322, lng:26.545, beach:3.0, hist:4.8, night:2.8, access:2.2, afford:2.5, car_need:3.0, has_airport:false, total:3.6, area:34,    pop:3047,    days:2, island_group:"Dodecanese", drama:false, hiking:false, springs:false, chora:true, sailing:false },
  "poros":        { name:"Poros",            lat:37.510, lng:23.470, beach:3.0, hist:4.2, night:3.5, access:4.8, afford:3.2, car_need:3.0, has_airport:false, total:3.5, area:23,    pop:3993,    days:1, island_group:"Saronic", drama:false, hiking:false, springs:false, chora:false, sailing:true },
  "alonnisos":    { name:"Alonnisos",        lat:39.216, lng:23.916, beach:4.4, hist:3.0, night:2.5, access:2.5, afford:4.0, car_need:3.0, has_airport:false, total:3.8, area:64,    pop:2750,    days:3, island_group:"Sporades", drama:false, hiking:true, springs:false, chora:false, sailing:true },
  "skyros":       { name:"Skyros",           lat:38.866, lng:24.533, beach:4.0, hist:3.8, night:2.8, access:2.5, afford:4.2, car_need:4.0, has_airport:true, total:3.4, area:209,   pop:2994,    days:3, island_group:"Sporades", drama:true, hiking:false, springs:false, chora:true, sailing:false },

  "sifnos":       { name:"Sifnos",           lat:36.966, lng:24.716, beach:3.8, hist:4.0, night:3.2, access:3.5, afford:3.5, car_need:4.0, has_airport:false, total:3.9, area:73,    pop:2625,    days:3, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:true, sailing:false },
  "symi":         { name:"Symi",             lat:36.583, lng:27.833, beach:3.0, hist:4.8, night:3.5, access:3.5, afford:2.5, car_need:3.0, has_airport:false, total:3.8, area:58,    pop:2590,    days:2, island_group:"Dodecanese", drama:false, hiking:false, springs:false, chora:false, sailing:true },
  "paxos":        { name:"Paxos",            lat:39.200, lng:20.150, beach:4.2, hist:3.0, night:3.5, access:2.8, afford:2.5, car_need:2.0, has_airport:false, total:4.0, area:19,    pop:2300,    days:3, island_group:"Ionian", drama:false, hiking:false, springs:false, chora:false, sailing:true },
  "kea":          { name:"Kea (Tzia)",       lat:37.616, lng:24.333, beach:3.8, hist:3.8, night:3.0, access:4.5, afford:3.0, car_need:4.0, has_airport:false, total:3.5, area:131,   pop:2455,    days:2, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "ios":          { name:"Ios",              lat:36.72, lng:25.33, beach:4.6, hist:2.5, night:5.0, access:3.2, afford:3.5, car_need:3.0, has_airport:false, total:3.9, area:109,   pop:2024,    days:3, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:true, sailing:false },
  "amorgos":      { name:"Amorgos",          lat:36.833, lng:25.900, beach:4.0, hist:3.8, night:3.5, access:2.5, afford:3.5, car_need:4.0, has_airport:false, total:4.0, area:126,   pop:1973,    days:4, island_group:"Cyclades", drama:true, hiking:true, springs:false, chora:true, sailing:false },
  "kythnos":      { name:"Kythnos",          lat:37.4, lng:24.43, beach:4.2, hist:3.2, night:3.0, access:3.5, afford:3.8, car_need:3.0, has_airport:false, total:3.5, area:100,   pop:1456,    days:2, island_group:"Cyclades", drama:false, hiking:false, springs:true, chora:false, sailing:false },
  "astypalaia":   { name:"Astypalaia",       lat:36.55, lng:26.36, beach:4.0, hist:4.2, night:3.0, access:2.5, afford:3.8, car_need:4.0, has_airport:true, total:3.8, area:97,    pop:1334,    days:3, island_group:"Dodecanese", drama:true, hiking:false, springs:false, chora:true, sailing:false },
  "antiparos":    { name:"Antiparos",        lat:37.02, lng:25.086, beach:4.5, hist:3.0, night:4.0, access:3.5, afford:2.8, car_need:3.0, has_airport:false, total:4.0, area:35,    pop:1211,    days:2, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "serifos":      { name:"Serifos",          lat:37.150, lng:24.483, beach:4.5, hist:3.2, night:3.0, access:3.5, afford:3.8, car_need:3.0, has_airport:false, total:3.9, area:75,    pop:1420,    days:2, island_group:"Cyclades", drama:true, hiking:false, springs:false, chora:false, sailing:false },
  "agistri":      { name:"Agistri",          lat:37.700, lng:23.350, beach:3.5, hist:2.5, night:3.5, access:4.5, afford:4.0, car_need:1.0, has_airport:false, total:3.4, area:13,    pop:1142,    days:1, island_group:"Saronic", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "nisyros":      { name:"Nisyros",          lat:36.583, lng:27.166, beach:3.0, hist:5.0, night:2.5, access:2.8, afford:4.0, car_need:3.0, has_airport:false, total:3.8, area:41,    pop:1008,    days:1, island_group:"Dodecanese", drama:true, hiking:false, springs:false, chora:false, sailing:false },
  "kimolos":      { name:"Kimolos",          lat:36.800, lng:24.570, beach:4.5, hist:3.2, night:2.5, access:3.0, afford:3.8, car_need:3.0, has_airport:false, total:3.6, area:36,    pop:910,     days:2, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "kastellorizo": { name:"Kastellorizo",     lat:36.140, lng:29.580, beach:2.0, hist:5.0, night:2.8, access:1.2, afford:3.5, car_need:1.0, has_airport:true, total:4.0, area:12,    pop:492,     days:2, island_group:"Dodecanese", drama:true, hiking:false, springs:false, chora:false, sailing:false },
  "sikinos":      { name:"Sikinos",          lat:36.683, lng:25.116, beach:3.5, hist:4.2, night:2.2, access:2.5, afford:4.0, car_need:3.0, has_airport:false, total:3.4, area:42,    pop:273,     days:2, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:true, sailing:false },
  "anafi":        { name:"Anafi",            lat:36.366, lng:25.766, beach:4.5, hist:3.2, night:2.5, access:2.0, afford:4.2, car_need:3.0, has_airport:false, total:3.9, area:38,    pop:271,     days:2, island_group:"Cyclades", drama:true, hiking:false, springs:false, chora:true, sailing:false },
  "samothrace":   { name:"Samothrace",       lat:40.45, lng:25.535, beach:3.0, hist:4.1, night:2.5, access:1.8, afford:4.5, car_need:3.0, has_airport:false, total:3.2, area:178,   pop:2859,    days:2, island_group:"Other", drama:true, hiking:true, springs:true, chora:false, sailing:false },
  "fournoi":      { name:"Fournoi",          lat:37.580, lng:26.500, beach:3.8, hist:3.0, night:1.8, access:2.0, afford:4.5, car_need:3.0, has_airport:false, total:3.2, area:45,    pop:1459,    days:2, island_group:"NE Aegean", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "spetses":      { name:"Spetses",          lat:37.260, lng:23.130, beach:2.8, hist:3.9, night:4.2, access:3.9, afford:2.0, car_need:3.0, has_airport:false, total:3.7, area:22,    pop:4027,    days:2, island_group:"Saronic", drama:false, hiking:false, springs:false, chora:false, sailing:true },
  "tilos":        { name:"Tilos",            lat:36.44, lng:27.37, beach:3.8, hist:3.5, night:2.0, access:2.2, afford:4.2, car_need:3.0, has_airport:false, total:3.5, area:61,    pop:780,     days:2, island_group:"Dodecanese", drama:false, hiking:true, springs:false, chora:false, sailing:false },
  "leipsoi":      { name:"Leipsoi",          lat:37.300, lng:26.750, beach:4.0, hist:3.0, night:2.0, access:2.5, afford:4.5, car_need:2.0, has_airport:false, total:3.4, area:16,    pop:790,     days:1, island_group:"Dodecanese", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "halki":        { name:"Halki",            lat:36.220, lng:27.610, beach:3.8, hist:4.0, night:2.0, access:2.5, afford:4.0, car_need:3.0, has_airport:false, total:3.6, area:28,    pop:478,     days:2, island_group:"Dodecanese", drama:false, hiking:false, springs:false, chora:true, sailing:false },
  "ammouliani":   { name:"Ammouliani",       lat:40.332, lng:23.916, beach:4.5, hist:2.0, night:3.0, access:3.0, afford:4.0, car_need:2.0, has_airport:false, total:3.5, area:4,     pop:547,     days:2, island_group:"Other", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "salamis":      { name:"Salamis",          lat:37.933, lng:23.500, beach:2.0, hist:3.5, night:3.0, access:4.5, afford:4.5, car_need:3.0, has_airport:false, total:2.8, area:95,    pop:39283,   days:1, island_group:"Saronic", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "therasia":     { name:"Therasia",         lat:36.445, lng:25.335, beach:3.0, hist:3.5, night:1.5, access:3.0, afford:3.5, car_need:1.0, has_airport:false, total:3.1, area:9,     pop:319,     days:1, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "schoinoussa":  { name:"Schoinoussa",      lat:36.87, lng:25.51, beach:4.5, hist:2.0, night:2.5, access:2.5, afford:3.8, car_need:1.0, has_airport:false, total:3.4, area:8,     pop:227,     days:2, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "donousa":      { name:"Donousa",          lat:37.095, lng:25.805, beach:4.5, hist:2.0, night:2.5, access:2.2, afford:3.8, car_need:1.0, has_airport:false, total:3.4, area:13,    pop:167,     days:2, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "kasos":        { name:"Kasos",            lat:35.383, lng:26.916, beach:3.2, hist:3.8, night:1.5, access:1.5, afford:4.5, car_need:3.0, has_airport:true, total:2.8, area:66,    pop:1084,    days:2, island_group:"Dodecanese", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "agathonisi":   { name:"Agathonisi",       lat:37.466, lng:26.966, beach:3.5, hist:2.0, night:1.5, access:1.8, afford:4.5, car_need:2.0, has_airport:false, total:3.0, area:13,    pop:185,     days:1, island_group:"Dodecanese", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "gavdos":       { name:"Gavdos",           lat:34.840, lng:24.080, beach:4.8, hist:2.0, night:2.5, access:1.0, afford:4.5, car_need:1.0, has_airport:false, total:3.0, area:33,    pop:152,     days:3, island_group:"Crete", drama:true, hiking:false, springs:false, chora:false, sailing:false }
};

const ISLANDS = Object.entries(ISLANDS_DATA).map(([key, data]) => ({ key, ...data }));

let mapInstance = null;
let mapMarkers = {};
let miniMapInstance = null;
let itineraryMapInstance = null;
let currentMapMode = 'overall';
let currentGroupFilter = 'all';
// Pre-rendered static comparison pages set window.__INITIAL_COMPARE_PAIR
// in an inline <script> before loading this file, so the SPA can pick up the
// pair immediately and render the right chart on the very first paint — no
// flash of the default mykonos/santorini view. Falls back to those defaults
// when nothing was set (e.g. when the user lands on /#compare).
let compareSelection = (typeof window !== 'undefined'
  && Array.isArray(window.__INITIAL_COMPARE_PAIR)
  && window.__INITIAL_COMPARE_PAIR.length === 2)
  ? [window.__INITIAL_COMPARE_PAIR[0], window.__INITIAL_COMPARE_PAIR[1]]
  : ['mykonos', 'santorini'];
let radarChartInstance = null;
let sortState = { col: 'total', asc: false };
let itinActiveDay = 'all';
let itinRouteLayers = {};
let itinMarkerLayers = {};
let itinBeachMarkers = [];

const SCORE_DIMS = ['beach', 'hist', 'night', 'access', 'afford', 'car_need'];
// For the compare page we exclude car_need from the chart/histogram — it's shown below as a label
const COMPARE_DIMS = ['beach', 'hist', 'night', 'access', 'afford'];

// DIM_LABELS is now a function — gets translated labels at call time
function getDimLabels() {
  return [t('dim.beach'), t('dim.culture'), t('dim.night'), t('dim.access'), t('dim.afford'), t('dim.car')];
}
// Back-compat constant (recomputed on language change)
let DIM_LABELS = ['Beach', 'Culture', 'Nightlife', 'Access', 'Affordability', 'Car needed'];
const SCORE_COLORS = {
  beach: '#1B4F8A', hist: '#5A7A3A', night: '#C0522A', access: '#C4962A', afford: '#7B5EA7', car_need: '#6B7280',
};

function scoreToColor(s) {
  if (s >= 4.5) return '#1B5E20'; // deep green (best)
  if (s >= 3.8) return '#4CAF50'; // green
  if (s >= 3.0) return '#C4962A'; // gold/yellow
  return '#C0522A';               // red/terracotta
}
function haversineApprox(a, b) {
  const dlat = a.lat - b.lat, dlng = a.lng - b.lng;
  return Math.sqrt(dlat * dlat + dlng * dlng);
}
function fmt(n, d = 1) { return Number(n).toFixed(d); }
function fmtNum(n) { return Number(n).toLocaleString(); }

/* ============================================================
   URL ROUTING
============================================================ */
const VIEW_HASH_MAP = {
  '': 'home', 'map': 'home', 'data': 'data', 'compare': 'compare',
  'hopping': 'hopping', 'international': 'international', 'match': 'match', 'mission': 'mission',
};

function parseHash() {
  // First check URL path — supports the pre-rendered SEO pages at /island/{key}/
  const path = window.location.pathname.replace(/^\/el\//, '/').replace(/\/$/, '');
  const pathMatch = path.match(/^\/island\/([a-z-]+)$/);
  if (pathMatch) return { view: 'island', param: pathMatch[1] };

  // Pre-rendered comparison pages at /compare/{a}-vs-{b}/ — the slug carries
  // both island keys; the boot logic uses them to pre-select compareSelection
  // before renderCompareView runs. The 'pair' shape is [keyA, keyB].
  const cmpMatch = path.match(/^\/compare\/([a-z-]+)-vs-([a-z-]+)$/);
  if (cmpMatch) return { view: 'compare', param: { pair: [cmpMatch[1], cmpMatch[2]] } };

  // Fall back to hash routing (the SPA's native navigation)
  const hash = window.location.hash.replace('#', '').trim();
  if (!hash) return { view: 'home', param: null };
  if (hash.startsWith('island/')) return { view: 'island', param: hash.replace('island/', '') };
  return { view: VIEW_HASH_MAP[hash] || 'home', param: null };
}


/* ============================================================
   MAP TILES — switch between light and dark tiles based on theme.
   Both light and dark use CARTO basemaps: Voyager (light) is a clean,
   modern travel-site map with soft teal water that matches our brand
   palette; dark_matter is its visual counterpart. Both are free, no
   API key, and share the same `{s}.basemaps.cartocdn.com` CDN with
   subdomains a/b/c/d.
============================================================ */
// On-brand day-route ramp: distinct but harmonious colors drawn from the site
// palette, used for itinerary day buttons / cards / map routes by day index.
const DAY_COLOR_RAMP = ['#0B8FAC', '#E8522A', '#3D8B6F', '#C98A00', '#7A5FA0', '#076880'];

function getMapTileUrl() {
  const isDark = document.documentElement.classList.contains('dark');
  return isDark
    ? 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png'
    : 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png';
}

function getMapTileAttribution() {
  // Same attribution string for both themes — CARTO requires both
  // OpenStreetMap (source data) and CARTO (style/tiles) to be credited.
  return '© OpenStreetMap contributors © CARTO';
}

// Esri World Imagery — satellite, no API key required, free for non-commercial use
const SATELLITE_TILE_URL = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
const SATELLITE_ATTRIBUTION = 'Tiles © Esri — Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community';
// Esri Reference labels overlay — adds place names + boundaries on top of satellite imagery (= "Hybrid")
const SATELLITE_LABELS_URL = 'https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}';

// Track active map registrations so theme swap and toggle persistence work
const _activeMapEntries = [];

function addThemeAwareTiles(map, options = {}) {
  const isDark = document.documentElement.classList.contains('dark');
  const maxZoom = options.maxZoom || 18;

  // Map (theme-aware) layer. CARTO uses 4 subdomains (a/b/c/d) for both
  // Voyager and dark_matter — keeps tile requests spread across them.
  const mapLayer = L.tileLayer(getMapTileUrl(), {
    attribution: options.attribution || getMapTileAttribution(),
    maxZoom: maxZoom,
    subdomains: 'abcd',
  });

  // Hybrid satellite: Esri imagery + Esri labels/boundaries overlay
  const satImagery = L.tileLayer(SATELLITE_TILE_URL, {
    attribution: SATELLITE_ATTRIBUTION,
    maxZoom: 19,
  });
  const satLabels = L.tileLayer(SATELLITE_LABELS_URL, {
    maxZoom: 19,
    pane: 'overlayPane',  // labels render above the imagery
  });
  const satLayer = L.layerGroup([satImagery, satLabels]);

  const labelMap = (typeof t === 'function') ? t('map.layer.map') : 'Map';
  const labelSat = (typeof t === 'function') ? t('map.layer.satellite') : 'Satellite';

  const baseLayers = {};
  baseLayers[labelMap] = mapLayer;
  baseLayers[labelSat] = satLayer;

  // Always start on Map, regardless of any previous user choice. No persistence.
  mapLayer.addTo(map);

  // Layer control (top-right) — user can toggle in-session, but we don't remember the choice
  let layerControl = null;
  if (!options.hideLayerControl) {
    layerControl = L.control.layers(baseLayers, null, {
      position: options.layerControlPosition || 'topright',
      collapsed: true,
    }).addTo(map);
  }

  _activeMapEntries.push({ map, mapLayer, satLayer, options, labelMap, labelSat, layerControl });
  return mapLayer;
}

function swapAllTiles() {
  // Theme changed — point the existing "map" layer at the new theme's tiles.
  // (Satellite layer is theme-independent, no change needed.)
  const isDark = document.documentElement.classList.contains('dark');
  _activeMapEntries.forEach(entry => {
    entry.mapLayer.options.subdomains = isDark ? 'abcd' : 'abc';
    entry.mapLayer.setUrl(getMapTileUrl());
  });
}


function navigateTo(view, param) {
  const hash = view === 'home' ? '#map' : view === 'island' ? `#island/${param}` : `#${view}`;
  if (window.location.hash !== hash) history.pushState({ view, param }, '', hash);
  showView(view, param);
}

// Navigate to the Mission page and scroll to the How We Score section.
// Used by "how we score" links throughout the site.
function navMission(event) {
  if (event && event.preventDefault) event.preventDefault();
  navigateTo('mission');
  setTimeout(() => {
    const target = document.getElementById('how-we-score');
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 120);
}
window.navMission = navMission;

function showView(view, param) {
  const homeControls = document.getElementById('home-controls');
  ['home','data','compare','hopping','international','match','shortlist','mission','detail'].forEach(v => {
    const el = document.getElementById(`view-${v}`);
    if (el) el.style.display = 'none';
  });
  const nav = document.getElementById('main-nav');
  if (nav) nav.querySelectorAll('a').forEach(a => a.classList.remove('active'));
  // Site-wide affiliate CTA: show on content views, hide on home (map), island detail (has its own buttons) and mission (no-affiliate page).
  const ctaBar = document.getElementById('cta-affiliate');
  if (ctaBar) ctaBar.style.display = (view === 'home' || view === 'island' || view === 'mission' || view === 'hopping' || view === 'international') ? 'none' : '';

  if (view === 'island') {
    const el = document.getElementById('view-detail');
    if (el) el.style.display = '';
    if (homeControls) homeControls.style.display = 'none';
    const helpBtn = document.getElementById('help-btn');
    if (helpBtn) helpBtn.style.display = 'none';
    document.body.classList.remove('home-view-active');
    if (param) renderIslandPage(param);
    return;
  }
  const target = document.getElementById(`view-${view}`);
  if (target) target.style.display = '';
  if (homeControls) homeControls.style.display = (view === 'home') ? '' : 'none';
  const navLink = document.getElementById(`nav-${view}`);
  if (navLink) navLink.classList.add('active');
  // Help button is only relevant on the home/map view
  const helpBtn = document.getElementById('help-btn');
  if (helpBtn) helpBtn.style.display = (view === 'home') ? '' : 'none';
  // Lock body scroll when on home view (map shouldn't be scrollable)
  document.body.classList.toggle('home-view-active', view === 'home');
  if (nav && nav.classList.contains('open')) nav.classList.remove('open');
  if (view === 'home' && mapInstance) setTimeout(() => mapInstance.invalidateSize(), 100);
  if (view === 'hopping') { setTimeout(renderHopping, 50); setTimeout(renderFerryPlanner, 50); }
  if (view === 'international') setTimeout(renderInternational, 50);
  if (view === 'match') setupQuizIfNeeded();
  if (view === 'shortlist') renderShortlist();
  if (view === 'compare') {
    // If a pair was passed via /compare/{a}-vs-{b}/ path, pre-select those
    // islands before the view renders. Validates that both keys exist in the
    // dataset (so a bad URL falls through to the default selection).
    if (param && param.pair && param.pair.length === 2) {
      const [a, b] = param.pair;
      if (ISLANDS_DATA && ISLANDS_DATA[a] && ISLANDS_DATA[b]) {
        compareSelection[0] = a;
        compareSelection[1] = b;
        // Push the dropdowns too — they're the visible source of truth and
        // their change events drive re-render; without this they'd still show
        // the default mykonos/santorini after setupCompare populated them.
        const selA = document.getElementById('compare-select-a');
        const selB = document.getElementById('compare-select-b');
        if (selA) selA.value = a;
        if (selB) selB.value = b;
      }
    }
    setTimeout(renderCompareView, 50);
  }
}

function handleNav(view, param) { navigateTo(view, param); }
window._openDetail = (key) => navigateTo('island', key);
window._addCmpNav = function(key) { addToCompare(key); navigateTo('compare'); };

document.addEventListener('DOMContentLoaded', () => {
  const hardFallback = setTimeout(dismissLoading, 3000);
  if (!localStorage.getItem('heroDismissed')) {
    // First-time visitor: open the help modal automatically
    setTimeout(() => openHelp(), 600);
  }
  try { setupNav(); } catch(e) { console.warn('setupNav', e); }
  try { applyStaticTranslations(); } catch(e) { console.warn('i18n', e); }
  try { renderBuildStamp(); } catch(e) { console.warn('buildStamp', e); }
  try { DIM_LABELS = getDimLabels(); } catch(e) { console.warn('dimLabels', e); }
  try { setupLanguageToggle(); } catch(e) { console.warn('langToggle', e); }
  updateShortlistCount();
  try { setupDarkMode(); } catch(e) { console.warn('setupDarkMode', e); }
  try { setupVibeChips(); } catch(e) { console.warn('setupVibeChips', e); }
  try { setupVibeTags(); } catch(e) { console.warn('setupVibeTags', e); }
  try { setupGroupFilter(); } catch(e) { console.warn('setupGroupFilter', e); }
  try { setupMap(); } catch(e) { console.warn('setupMap', e); }
  try { renderWhatsOnStrip().then(adjustMapHeightToStrip); } catch(e) { console.warn('whatsOn', e); }
  // Featured cards use per-island hero photos from a small manifest. Render once
  // now (fallback initials) and re-render after the manifest loads (with photos).
  try { renderHomeFeatured(); } catch(e) { console.warn('homeFeatured', e); }
  try { loadHeroPhotos().then(() => { try { renderHomeFeatured(); } catch(_) {} }); } catch(e) { console.warn('heroPhotos', e); }
  try { setupTable(); } catch(e) { console.warn('setupTable', e); }
  try { setupCompare(); } catch(e) { console.warn('setupCompare', e); }
  const vd = document.getElementById('version-display');
  if (vd) vd.textContent = `Aegean Blueprint ${VERSION}`;
  clearTimeout(hardFallback);
  dismissLoading();
  try { const { view, param } = parseHash(); showView(view, param); }
  catch(e) { showView('home', null); }
});

window.addEventListener('popstate', () => {
  try { const { view, param } = parseHash(); showView(view, param); }
  catch(e) { showView('home', null); }
});

function printIsland() {
  // Use the browser's native print -> Save as PDF dialog
  // The print stylesheet (in style.css) strips nav, maps, and buttons.
  window.print();
}

window.printIsland = printIsland;

/* ============================================================
   FEEDBACK MODAL — opens email client with prefilled message
============================================================ */
function openFeedback() {
  const modal = document.getElementById('feedback-modal');
  if (modal) {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }
}

function closeFeedback() {
  const modal = document.getElementById('feedback-modal');
  if (modal) {
    modal.style.display = 'none';
    document.body.style.overflow = '';
  }
}

function submitFeedback(event) {
  event.preventDefault();
  const form = event.target;
  const topic = form.topic.value;
  const message = form.message.value;
  const email = form.email.value || '(not provided)';
  const currentUrl = window.location.href;
  
  const topicLabels = {
    'suggestion': 'Suggestion',
    'error': 'Error / correction',
    'rating': 'Rating correction',
    'missing-island': 'Missing island',
    'missing-restaurant': 'Missing restaurant or beach',
    'other': 'Other'
  };
  const topicLabel = topicLabels[topic] || 'Feedback';
  
  const subject = `[Aegean Blueprint] ${topicLabel}`;
  const body = `Topic: ${topicLabel}\n\nMessage:\n${message}\n\nFrom: ${email}\nPage: ${currentUrl}\n\n---\nSent from aegeanblueprint.com`;
  
  const mailtoLink = `mailto:stergiosgousios@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  window.location.href = mailtoLink;
  
  // Close modal after a brief delay
  setTimeout(() => {
    closeFeedback();
    form.reset();
  }, 500);
}

// Close modal when clicking outside the content area
document.addEventListener('click', (e) => {
  const modal = document.getElementById('feedback-modal');
  if (modal && e.target === modal) {
    closeFeedback();
  }
});

// Close on Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const modal = document.getElementById('feedback-modal');
    if (modal && modal.style.display === 'flex') {
      closeFeedback();
    }
  }
});

window.openFeedback = openFeedback;
window.closeFeedback = closeFeedback;
window.submitFeedback = submitFeedback;


function copyIslandLink() {
  const url = 'https://aegeanblueprint.com/' + window.location.hash;
  navigator.clipboard.writeText(url).then(() => {
    const btn = document.getElementById('detail-share-btn');
    if (btn) {
      btn.textContent = '✓ Copied!';
      setTimeout(() => { btn.textContent = '🔗 Copy link'; }, 2000);
    }
  }).catch(() => {
    // Fallback for older browsers
    const el = document.createElement('textarea');
    el.value = url;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    const btn = document.getElementById('detail-share-btn');
    if (btn) {
      btn.textContent = '✓ Copied!';
      setTimeout(() => { btn.textContent = '🔗 Copy link'; }, 2000);
    }
  });
}

function openHelp() {
  const modal = document.getElementById('help-modal');
  if (modal) {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }
}

function closeHelp() {
  const modal = document.getElementById('help-modal');
  if (modal) {
    modal.style.display = 'none';
    document.body.style.overflow = '';
    localStorage.setItem('heroDismissed', '1');
  }
}

// Back-compat
function dismissHero() { closeHelp(); }

window.openHelp = openHelp;
window.closeHelp = closeHelp;

// Close modal on backdrop click
document.addEventListener('click', (e) => {
  const modal = document.getElementById('help-modal');
  if (modal && e.target === modal) closeHelp();
});

// Close modal on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const modal = document.getElementById('help-modal');
    if (modal && modal.style.display === 'flex') closeHelp();
  }
});

function dismissLoading() {
  const overlay = document.getElementById('loading-overlay');
  if (overlay) {
    overlay.classList.add('hidden');
    setTimeout(() => { if (overlay) overlay.style.display = 'none'; }, 600);
  }
}

/* ============================================================
   NAV + DARK MODE
============================================================ */
function renderBuildStamp() {
  const el = document.getElementById('footer-updated');
  if (!el) return;
  // Format date in user's language
  const lang = (typeof CURRENT_LANG !== 'undefined' && CURRENT_LANG === 'el') ? 'el-GR' : 'en-GB';
  const d = new Date(BUILD_DATE);
  const formatted = d.toLocaleDateString(lang, { year: 'numeric', month: 'long', day: 'numeric' });
  const label = (typeof CURRENT_LANG !== 'undefined' && CURRENT_LANG === 'el') ? 'Τελευταία ενημέρωση' : 'Last updated';
  // Include the leading " · " separator inside the textContent so that when
  // the footer is in its empty state (no BUILD_DATE), `:empty` keeps the span
  // hidden and we don't end up with a dangling " · " in the inline footer.
  el.textContent = ` · ${label}: ${formatted}`;
}

function setupNav() {
  const navMap = {
    'nav-home': 'home', 'nav-map': 'home', 'nav-data': 'data',
    'nav-compare': 'compare', 'nav-hopping': 'hopping',
    'nav-international': 'international',
    'nav-match': 'match', 'nav-shortlist': 'shortlist', 'nav-mission': 'mission',
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

function setupLanguageToggle() {
  const btn = document.getElementById('lang-toggle-btn');
  const menu = document.getElementById('lang-menu');
  const currentLabel = document.getElementById('lang-current');
  if (!btn || !menu) return;

  // Set current lang label and mark active option
  const labels = { en: 'EN', el: 'ΕΛ' };
  if (currentLabel) currentLabel.textContent = labels[CURRENT_LANG] || 'EN';
  menu.querySelectorAll('.lang-option').forEach(a => {
    if (a.dataset.lang === CURRENT_LANG) a.classList.add('active');
  });

  // Toggle menu on button click
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    const isOpen = menu.classList.toggle('open');
    btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  });

  // Handle option selection
  menu.querySelectorAll('.lang-option').forEach(a => {
    a.addEventListener('click', (e) => {
      e.preventDefault();
      const targetLang = a.dataset.lang;
      if (targetLang === CURRENT_LANG) {
        menu.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
        return;
      }
      const currentHash = window.location.hash;
      if (targetLang === 'el') {
        window.location.href = '/el/' + currentHash;
      } else {
        window.location.href = '/' + currentHash;
      }
    });
  });

  // Close menu when clicking outside
  document.addEventListener('click', (e) => {
    if (!e.target.closest('#lang-dropdown')) {
      menu.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
    }
  });
}

function setupDarkMode() {
  const btn = document.getElementById('dark-mode-btn');
  const root = document.documentElement;
  // Apply persisted preference even if the toggle button isn't on this page
  // (static island pages don't include the homepage's dark-mode button).
  if (localStorage.getItem('darkMode') === 'true') {
    root.classList.add('dark');
    if (btn) btn.textContent = '☀';
  }
  // No button → nothing to wire up; bail before .addEventListener throws.
  if (!btn) return;
  btn.addEventListener('click', () => {
    const isDark = root.classList.toggle('dark');
    btn.textContent = isDark ? '☀' : '☾';
    localStorage.setItem('darkMode', isDark);
    if (radarChartInstance) renderRadarChart();
    swapAllTiles();
  });
}

/* ============================================================
   MAP
============================================================ */
/* ============================================================
   "Featured islands" homepage grid
   ------------------------------------------------------------
   Renders 6 hand-picked island cards in the homepage content section
   (below the map). Each card has a short tag (mood label) and an
   excerpt drawn from the island's own intro text. The set is curated
   for editorial breadth — different moods, different regions,
   different scores — not algorithmic. Re-curate by editing the
   FEATURED array below.
============================================================ */
const HOMEPAGE_FEATURED = [
  { key: 'folegandros', tagEn: 'Quiet escape',    tagEl: 'Ήσυχη απόδραση' },
  { key: 'milos',       tagEn: 'Beach trip',      tagEl: 'Παραλιακή απόδραση' },
  { key: 'santorini',   tagEn: 'Iconic',          tagEl: 'Εμβληματική' },
  { key: 'hydra',       tagEn: 'No cars',         tagEl: 'Χωρίς αυτοκίνητα' },
  { key: 'symi',        tagEn: 'Off-radar',       tagEl: 'Εκτός ραντάρ' },
  { key: 'naxos',       tagEn: 'Family-friendly', tagEl: 'Φιλικό για οικογένειες' },
];

/* Measure the actual height of the "What's on this month" strip and pass
   it to CSS as --whats-on-strip-height. The default in style.css (~37px)
   is a guess; if the strip ends up taller (long content wrapping to a
   second line) or shorter (font rendering differences, empty strip on
   the off-chance), the map height calc would be off and the "About this
   site" button at the bottom of the map would get clipped or float
   awkwardly. Runs once after the strip is rendered, and again on resize. */
function adjustMapHeightToStrip() {
  const strip = document.getElementById('whats-on-strip');
  if (!strip) return;
  const apply = () => {
    const h = strip.offsetHeight;            // 0 if :empty { display:none } kicked in
    document.documentElement.style.setProperty('--whats-on-strip-height', h + 'px');
    // Force Leaflet to re-measure (otherwise the map tiles don't fill
    // the new bottom space until the next pan/zoom).
    if (typeof mapInstance !== 'undefined' && mapInstance && mapInstance.invalidateSize) {
      mapInstance.invalidateSize();
    }
  };
  apply();
  // Re-measure on window resize — the strip may wrap differently at
  // different widths, changing its height.
  window.addEventListener('resize', apply);
}

/* Smooth-scroll between the map and the homepage content section.
   The map captures mouse-wheel events, so these button-triggered jumps
   are the reliable way to move between the two. */
function scrollToHomeContent() {
  const el = document.getElementById('home-content');
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
function scrollToHomeTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

let HERO_PHOTOS = {};
async function loadHeroPhotos() {
  if (HERO_PHOTOS && Object.keys(HERO_PHOTOS).length) return HERO_PHOTOS;
  try {
    const r = await fetch('/hero-photos.json', { cache: 'default' });
    if (r.ok) HERO_PHOTOS = await r.json();
  } catch (e) { console.warn('hero-photos fetch failed', e); }
  return HERO_PHOTOS;
}

function renderHomeFeatured() {
  const grid = document.getElementById('home-featured-grid');
  if (!grid) return;
  const lang = (typeof CURRENT_LANG !== 'undefined' && CURRENT_LANG === 'el') ? 'el' : 'en';

  const cards = HOMEPAGE_FEATURED.map(item => {
    const meta = (typeof ISLANDS_DATA !== 'undefined') ? ISLANDS_DATA[item.key] : null;
    if (!meta) return '';
    const name = (lang === 'el' && typeof GREEK_NAMES !== 'undefined' && GREEK_NAMES[item.key])
      ? GREEK_NAMES[item.key]
      : meta.name;
    const score = (typeof meta.total === 'number') ? meta.total.toFixed(1) : '';
    const tag = lang === 'el' ? item.tagEl : item.tagEn;
    // Excerpt comes from the per-island JSON's intro field. Since we don't
    // pre-load all 78 JSONs on the homepage, we use a short hardcoded excerpt
    // pulled from each intro's first sentence (curated below for brevity).
    const excerpt = (HOMEPAGE_EXCERPTS[item.key] || {})[lang] || '';
    const href = (lang === 'el' ? '/el/island/' : '/island/') + item.key + '/';
    const hero = HERO_PHOTOS[item.key] || {};
    const grp = (typeof groupName === 'function') ? groupName(meta.island_group) : (meta.island_group || '');
    const photoImg = hero.url
      ? `<img class="hfc-photo" src="${hero.url}" alt="${name}" loading="lazy" onerror="this.closest('.hfc-media').classList.add('hfc-nophoto')">`
      : '';
    return `
      <a class="home-featured-card" href="${href}">
        <div class="hfc-media${hero.url ? '' : ' hfc-nophoto'}" data-initial="${name.charAt(0)}">
          ${photoImg}
          <span class="hfc-scrim"></span>
          <span class="hfc-score">${score}<small>/5</small></span>
          ${grp ? `<span class="hfc-group">${grp}</span>` : ''}
          ${buildPhotoCredit(hero.credit)}
        </div>
        <div class="hfc-body">
          <span class="home-featured-card-name">${name}</span>
          <p class="home-featured-card-excerpt">${excerpt}</p>
          <span class="home-featured-card-tag" data-tag-key="${item.key}" data-tag-label="${tag}"></span>
        </div>
      </a>`;
  }).filter(Boolean).join('');

  grid.innerHTML = cards;
}

/* Excerpts for the featured grid. One sentence per island, EN + EL.
   Drawn from each island's own intro field in islands/*.json — kept
   in sync there. When changing an intro, update here too. */
const HOMEPAGE_EXCERPTS = {
  folegandros: {
    en: 'The Cyclades as they were 30 years ago — 19 square kilometres, 765 people, no airport, three villages.',
    el: 'Οι Κυκλάδες όπως ήταν πριν 30 χρόνια — 19 τετραγωνικά χιλιόμετρα, 765 κάτοικοι, χωρίς αεροδρόμιο, τρία χωριά.'
  },
  milos: {
    en: 'Called the most beautiful island in Greece — volcanic geology, lunar rock at Sarakiniko, white pumice at Kleftiko.',
    el: 'Έχει χαρακτηριστεί το ομορφότερο νησί της Ελλάδας — ηφαιστειακή γεωλογία, σεληνιακοί βράχοι στο Σαρακήνικο, λευκή κίσσηρης στο Κλέφτικο.'
  },
  santorini: {
    en: 'Not primarily a beach island — come for the caldera, the architecture, the wine and the sunsets.',
    el: 'Δεν είναι κυρίως νησί παραλιών — έλα για την καλντέρα, την αρχιτεκτονική, το κρασί και τα ηλιοβασιλέματα.'
  },
  hydra: {
    en: 'Bans all motor vehicles — move on foot, by donkey, or by water taxi. The most peaceful town in the Saronic.',
    el: 'Απαγορεύει τα μηχανοκίνητα οχήματα — με τα πόδια, με γαϊδούρι, ή θαλάσσιο ταξί. Η πιο ήσυχη πόλη στον Σαρωνικό.'
  },
  symi: {
    en: 'The most photographed harbour in Greece — an amphitheatre of ochre, yellow, terracotta and blue mansions.',
    el: 'Το πιο φωτογραφημένο λιμάνι της Ελλάδας — αμφιθέατρο νεοκλασικών αρχοντικών σε ώχρα, κίτρινο, τερακότα και μπλε.'
  },
  naxos: {
    en: 'The largest and most self-sufficient Cycladic island — mountain interior, marble quarries, the finest sandy beaches.',
    el: 'Το μεγαλύτερο και πιο αυτάρκες νησί των Κυκλάδων — ορεινό εσωτερικό, λατομεία μαρμάρου, οι καλύτερες αμμώδεις παραλίες.'
  },
};

/* ============================================================
   "What's on now" home strip
   ------------------------------------------------------------
   Fetches /whats-on.json (built by prerender.py) and renders a small
   strip above the map showing islands tagged "perfect" for the current
   month, plus any festivals happening this month. Refreshes monthly
   automatically — same code, different output in May vs October.
============================================================ */
async function renderWhatsOnStrip() {
  const container = document.getElementById('whats-on-strip');
  if (!container) return;

  let data;
  try {
    const res = await fetch('/whats-on.json', { cache: 'default' });
    if (!res.ok) return;
    data = await res.json();
  } catch (e) {
    console.warn('whats-on fetch failed', e);
    return;
  }

  const month = new Date().getMonth() + 1;   // 1-12
  const lang = (typeof CURRENT_LANG !== 'undefined' && CURRENT_LANG === 'el') ? 'el' : 'en';
  const monthNamesEN = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  const monthNamesEL = ['Ιανουάριο','Φεβρουάριο','Μάρτιο','Απρίλιο','Μάιο','Ιούνιο','Ιούλιο','Αύγουστο','Σεπτέμβριο','Οκτώβριο','Νοέμβριο','Δεκέμβριο'];
  const monthLabel = lang === 'el' ? monthNamesEL[month - 1] : monthNamesEN[month - 1];

  // Find islands tagged "perfect" for this month, then add "great" if too few perfects
  const perfectIslands = [];
  const greatIslands = [];
  Object.keys(data).forEach(key => {
    const entry = data[key];
    if (entry.perfect && entry.perfect.includes(month)) {
      perfectIslands.push(key);
    } else if (entry.great && entry.great.includes(month)) {
      greatIslands.push(key);
    }
  });

  // Pick 6 islands to feature.
  //
  // Strategy depends on how many perfects there are:
  //   - LOTS (>12): peak season — every popular island is "perfect", so showing
  //     top-by-score just surfaces Santorini/Mykonos/Naxos every time. Instead
  //     diversify by island group AND bias toward smaller/less-obvious picks
  //     so the strip gives users something they wouldn't have found themselves.
  //   - SOME (4-12): the sweet spot — show by score, all are genuine.
  //   - FEW (<4): off-season fallback — top up with "great" tagged islands.
  const meta = (typeof ISLANDS_DATA !== 'undefined') ? ISLANDS_DATA : {};
  const byScore = (a, b) => (meta[b]?.total || 0) - (meta[a]?.total || 0);
  const TARGET = 3;   // Slim — fits on one mobile line

  let islandsToShow = [];
  if (perfectIslands.length > 12) {
    // Peak season — diversify by group, prefer smaller islands within group.
    // First sort by population ascending (cap at 8000 — bigger ones are too obvious).
    // Then walk down in group-rotation order so we get one from each group.
    const popOf = k => meta[k]?.pop || 9999;
    const groupOf = k => meta[k]?.island_group || 'Other';
    // Bucket by group
    const groupBuckets = {};
    perfectIslands.forEach(k => {
      const g = groupOf(k);
      if (!groupBuckets[g]) groupBuckets[g] = [];
      groupBuckets[g].push(k);
    });
    // Sort within each bucket: prefer smaller (less obvious) islands. Each
    // island gets a "deserves-spotlight" rank: pop weight + score boost, so
    // a small island with great score outranks an even smaller mediocre one.
    Object.keys(groupBuckets).forEach(g => {
      groupBuckets[g].sort((a, b) => {
        // Lower pop is better; higher score is better. Tie-break on key.
        const popA = Math.log10(popOf(a) + 1);
        const popB = Math.log10(popOf(b) + 1);
        const scoreA = meta[a]?.total || 0;
        const scoreB = meta[b]?.total || 0;
        // "Hidden gem" score: low population and decent rating
        const gemA = -popA * 1.0 + scoreA * 0.4;
        const gemB = -popB * 1.0 + scoreB * 0.4;
        return gemB - gemA;
      });
    });
    // Round-robin across groups, but with a month-based offset so June and
    // September show different picks (both have ~75 perfects but rotate).
    const groupKeys = Object.keys(groupBuckets).sort();   // stable order
    const monthOffset = month;     // 1-12, used as starting bucket index
    let idx = 0;
    while (islandsToShow.length < TARGET) {
      let added = false;
      for (let i = 0; i < groupKeys.length && islandsToShow.length < TARGET; i++) {
        // Stagger which group is picked first based on the month
        const g = groupKeys[(i + monthOffset) % groupKeys.length];
        // Stagger which item within the group based on month too — for groups
        // with multiple candidates, June picks one, September picks the next.
        const itemIdx = (idx + Math.floor(monthOffset / 3)) % Math.max(groupBuckets[g].length, 1);
        if (groupBuckets[g].length > 0 && !islandsToShow.includes(groupBuckets[g][itemIdx])) {
          islandsToShow.push(groupBuckets[g][itemIdx]);
          added = true;
        }
      }
      if (!added) break;
      idx++;
    }
  } else {
    // Normal case — just pick top-scored perfects, fill with greats if too few
    perfectIslands.sort(byScore);
    greatIslands.sort(byScore);
    islandsToShow = perfectIslands.slice(0, TARGET);
    if (islandsToShow.length < 4) {
      const fill = greatIslands.slice(0, TARGET - islandsToShow.length);
      islandsToShow.push(...fill);
    }
  }

  // Count festivals happening this month — the strip just shows a count + link
  // to the full festival calendar page rather than listing them inline.
  let festivalCount = 0;
  Object.keys(data).forEach(key => {
    const entry = data[key];
    if (!entry.festivals) return;
    entry.festivals.forEach(f => {
      if (f.months && f.months.includes(month)) festivalCount++;
    });
  });

  // Nothing to show? Hide the strip entirely.
  if (islandsToShow.length === 0 && festivalCount === 0) {
    container.style.display = 'none';
    return;
  }

  // Build the chip HTML
  const chipsHtml = islandsToShow.map(key => {
    const name = (typeof islandName === 'function') ? islandName(key) : (meta[key]?.name || key);
    return `<a class="whats-on-chip" href="#" onclick="navigateTo('island','${key}');return false;">${name}</a>`;
  }).join('');

  // Festival call-to-action: just a link to the full calendar page, with the count.
  let festivalsHtml = '';
  if (festivalCount > 0) {
    const festPath = lang === 'el' ? '/el/festivals/' : '/festivals/';
    const label = lang === 'el'
      ? `${festivalCount} ${festivalCount === 1 ? 'γιορτή' : 'γιορτές'} αυτόν τον μήνα →`
      : `${festivalCount} ${festivalCount === 1 ? 'festival' : 'festivals'} this month →`;
    festivalsHtml = `<a class="whats-on-festivals-link" href="${festPath}">${label}</a>`;
  }

  // Label depends on the data shape:
  //   - 0 perfects: "Best in <month>" (fallback to greats)
  //   - 1-3 perfects: "Best for <month>" (small handful of recommended)
  //   - 4-12 perfects: "Perfect in <month>" (the genuine sweet spot)
  //   - >12 perfects: "Underrated picks for <month>" (peak season, diversified)
  let perfectLabel;
  if (perfectIslands.length === 0) {
    perfectLabel = lang === 'el' ? `Καλά για ${monthLabel}` : `Best in ${monthLabel}`;
  } else if (perfectIslands.length < 4) {
    perfectLabel = lang === 'el' ? `Ιδανικά τον ${monthLabel}` : `Best for ${monthLabel}`;
  } else if (perfectIslands.length > 12) {
    perfectLabel = lang === 'el' ? `Αξιόλογες επιλογές τον ${monthLabel}` : `Underrated picks for ${monthLabel}`;
  } else {
    perfectLabel = lang === 'el' ? `Ιδανικά τον ${monthLabel}` : `Perfect in ${monthLabel}`;
  }

  container.innerHTML = `
    <div class="whats-on-row">
      <div class="whats-on-perfect">
        <span class="whats-on-label">${perfectLabel}:</span>
        <div class="whats-on-chips">${chipsHtml}</div>
      </div>
      ${festivalsHtml}
    </div>
  `;
  container.style.display = '';
}

// Tiny helpers — escape for HTML attrs and innerHTML use
function escapeAttr(s) {
  return String(s || '').replace(/"/g, '&quot;').replace(/'/g, '&#39;').replace(/</g, '&lt;');
}
function escapeHtml(s) {
  return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function setupMap() {
  const GREECE_BOUNDS = L.latLngBounds(L.latLng(33.8, 18.5), L.latLng(42.2, 30.2));
  mapInstance = L.map('main-map', { zoomControl: true, minZoom: 6, maxZoom: 14, maxBounds: GREECE_BOUNDS, maxBoundsViscosity: 0.85 });
  mapInstance.fitBounds(GREECE_BOUNDS);
  addThemeAwareTiles(mapInstance, { maxZoom: 14 });
  L.control.scale({ imperial: false, position: 'bottomleft' }).addTo(mapInstance);
  renderMapMarkers();
  const searchInput = document.getElementById('islandSearch');
  if (searchInput) searchInput.addEventListener('input', filterIslands);
}

function getDisplayScore(island) {
  const modeMap = { overall:'total', beach:'beach', hist:'hist', night:'night', access:'access', afford:'afford', car_need:'car_need' };
  return island[modeMap[currentMapMode] || 'total'];
}

function makeMarkerIcon(score, dimmed) {
  const color = dimmed ? '#c8c8c8' : scoreToColor(score);
  const size = Math.round(20 + score * 2);
  const textColor = dimmed ? '#999' : '#fff';
  const shadow = dimmed ? 'none' : '0 2px 6px rgba(0,0,0,.3)';
  return L.divIcon({
    className: 'custom-marker',
    html: `<div style="background:${color};width:${size}px;height:${size}px;border-radius:50%;border:2px solid #fff;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:${textColor};box-shadow:${shadow};">${fmt(score)}</div>`,
    iconSize: [size, size], iconAnchor: [size / 2, size / 2],
  });
}

function renderMapMarkers() {
  Object.values(mapMarkers).forEach(m => mapInstance.removeLayer(m));
  mapMarkers = {};
  const searchTerm = (document.getElementById('islandSearch')?.value || '').toLowerCase();
  ISLANDS.forEach(island => {
    if (searchTerm) {
        const enName = island.name.toLowerCase();
        const elName = (typeof ISLAND_NAMES_EL !== 'undefined' && ISLAND_NAMES_EL[island.key]) ? ISLAND_NAMES_EL[island.key].toLowerCase() : '';
        if (!enName.includes(searchTerm) && !elName.includes(searchTerm)) return;
      }
    if (currentGroupFilter === '__airport_yes__') {
      if (!island.has_airport) return;
    } else if (currentGroupFilter === '__airport_no__') {
      if (island.has_airport) return;
    } else if (currentGroupFilter !== 'all' && island.island_group !== currentGroupFilter) {
      return;
    }
    const vibeMatch = islandPassesVibeFilters(island);
    const score = getDisplayScore(island);
    const carWords = ['', t('car.none'), t('car.helpful'), t('car.useful'), t('car.recommended'), t('car.essential')];
    const carLabel = carWords[Math.round(island.car_need || 0)] || '—';
    const marker = L.marker([island.lat, island.lng], { icon: makeMarkerIcon(score, !vibeMatch), opacity: vibeMatch ? 1 : 0.22 })
      .addTo(mapInstance)
      .bindTooltip(`
        <div class="island-tooltip-inner">
          <div class="itt-name">${islandName(island.key)}</div>
          <div class="itt-meta">${groupName(island.island_group)} · ${fmtNum(island.area)} km²</div>
          <div class="itt-overall">${t('tooltip.overall')}: <strong style="color:${scoreToColor(island.total)}">${fmt(island.total)}</strong></div>
          <div class="itt-ratings">
            <div class="itt-rating-row"><span class="itt-rating-label">🏖️ ${t('dim.beach')}</span><span class="itt-rating-bar"><span class="itt-rating-fill itt-fill-beach" style="width:${(island.beach/5)*100}%"></span></span><span class="itt-rating-val">${fmt(island.beach)}</span></div>
            <div class="itt-rating-row"><span class="itt-rating-label">🏛️ ${t('dim.culture')}</span><span class="itt-rating-bar"><span class="itt-rating-fill itt-fill-hist" style="width:${(island.hist/5)*100}%"></span></span><span class="itt-rating-val">${fmt(island.hist)}</span></div>
            <div class="itt-rating-row"><span class="itt-rating-label">🍷 ${t('dim.night')}</span><span class="itt-rating-bar"><span class="itt-rating-fill itt-fill-night" style="width:${(island.night/5)*100}%"></span></span><span class="itt-rating-val">${fmt(island.night)}</span></div>
            <div class="itt-rating-row"><span class="itt-rating-label">🚢 ${t('dim.access')}</span><span class="itt-rating-bar"><span class="itt-rating-fill itt-fill-access" style="width:${(island.access/5)*100}%"></span></span><span class="itt-rating-val">${fmt(island.access)}</span></div>
            <div class="itt-rating-row"><span class="itt-rating-label">💸 ${t('dim.afford')}</span><span class="itt-rating-bar"><span class="itt-rating-fill itt-fill-afford" style="width:${(island.afford/5)*100}%"></span></span><span class="itt-rating-val">${fmt(island.afford)}</span></div>
          </div>
          <div class="itt-car">🚗 ${t('dim.car')}: <strong>${carLabel}</strong></div>
          ${island.has_airport ? `<div class="itt-airport">✈ <strong>${t('tooltip.hasairport')}</strong></div>` : ''}
          ${island.days ? `<div class="itt-days">⏱ ${island.days} ${t('common.days')} ${t('tooltip.recommended')}</div>` : ''}
          <div class="itt-cta">${t('tooltip.click')}</div>
        </div>
      `, { sticky: false, opacity: 1, className: 'island-tooltip' });
    marker.on('click', () => navigateTo('island', island.key));
    mapMarkers[island.key] = marker;
  });
}

// ============================================================
//  VIBE FILTER PANEL
// ============================================================
let activeVibeFilters = new Set();

function toggleVibePanel() {
  const panel = document.getElementById('vibe-panel');
  const btn   = document.getElementById('vibe-filter-btn');
  if (!panel) return;
  const open = panel.style.display === 'none';
  panel.style.display = open ? '' : 'none';
  btn && btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  if (open) updateVibeMatchCount();
}

function toggleVibeTag(filter) {
  if (activeVibeFilters.has(filter)) {
    activeVibeFilters.delete(filter);
  } else {
    activeVibeFilters.add(filter);
  }
  // Update tag button states
  document.querySelectorAll('.vibe-tag').forEach(btn => {
    btn.classList.toggle('active', activeVibeFilters.has(btn.dataset.filter));
  });
  const clearBtn = document.getElementById('vibe-clear-btn');
  if (clearBtn) clearBtn.style.display = activeVibeFilters.size ? '' : 'none';
  // Update badge on filter button
  const countBadge = document.getElementById('vibe-filter-count');
  if (countBadge) {
    countBadge.textContent = activeVibeFilters.size || '';
    countBadge.style.display = activeVibeFilters.size ? '' : 'none';
  }
  updateVibeMatchCount();
  renderMapMarkers();
}

function clearVibeFilters() {
  activeVibeFilters.clear();
  document.querySelectorAll('.vibe-tag').forEach(btn => btn.classList.remove('active'));
  const clearBtn = document.getElementById('vibe-clear-btn');
  if (clearBtn) clearBtn.style.display = 'none';
  const countBadge = document.getElementById('vibe-filter-count');
  if (countBadge) { countBadge.textContent = ''; countBadge.style.display = 'none'; }
  updateVibeMatchCount();
  renderMapMarkers();
}

function updateVibeMatchCount() {
  const el = document.getElementById('vibe-match-count');
  if (!el) return;
  if (!activeVibeFilters.size) { el.textContent = ''; return; }
  const n = ISLANDS.filter(i => islandPassesVibeFilters(i)).length;
  const total = ISLANDS.length;
  el.textContent = `${n} / ${total} islands`;
}

function islandPassesVibeFilters(island) {
  if (!activeVibeFilters.size) return true;
  const mo = new Date().getMonth(); // 0-indexed
  for (const f of activeVibeFilters) {
    switch (f) {
      case 'good_now': {
        const tag = WTV_TAGS[island.key] && WTV_TAGS[island.key][mo];
        if (tag === undefined || tag < 2) return false; // great(2) or perfect(3)
        break;
      }
      case 'ideal_now': {
        const tag = WTV_TAGS[island.key] && WTV_TAGS[island.key][mo];
        if (tag === undefined || tag < 3) return false; // perfect only
        break;
      }
      case 'car_free':     if (!island.car_need || island.car_need > 1.5) return false; break;
      case 'car_optional': if (!island.car_need || island.car_need > 3.0) return false; break;
      case 'remote':     if (!island.access || island.access > 2.5)     return false; break;
      case 'budget':     if (!island.afford  || island.afford  < 4.0)   return false; break;
      case 'nightlife':  if (!island.night   || island.night   < 4.0)   return false; break;
      case 'tiny':       if (!island.pop     || island.pop     > 2000)   return false; break;
      case 'drama':      if (!island.drama)                              return false; break;
      case 'hiking':     if (!island.hiking)                             return false; break;
      case 'springs':    if (!island.springs)                            return false; break;
      case 'chora':      if (!island.chora)                              return false; break;
      case 'sailing':    if (!island.sailing)                            return false; break;
      case 'airport':    if (!island.has_airport)                        return false; break;
    }
  }
  return true;
}

function filterIslands() { renderMapMarkers(); }
function updateMapMode(mode) { currentMapMode = mode; renderMapMarkers(); }

function setupVibeChips() {
  const sel = document.getElementById('vibe-select');
  if (!sel) return;
  sel.addEventListener('change', () => updateMapMode(sel.value));
}

function setupVibeTags() {
  document.querySelectorAll('.vibe-tag').forEach(btn => {
    btn.addEventListener('click', () => toggleVibeTag(btn.dataset.filter));
  });
}

function setupGroupFilter() {
  const sel = document.getElementById('group-select');
  if (!sel) return;
  const groups = [...new Set(ISLANDS.map(i => i.island_group))].sort();
  groups.forEach(group => {
    const opt = document.createElement('option');
    opt.value = group;
    opt.textContent = groupName(group);
    sel.appendChild(opt);
  });
  // Divider + airport options
  const divider = document.createElement('option');
  divider.disabled = true;
  divider.textContent = '──────────';
  sel.appendChild(divider);
  const optAir = document.createElement('option');
  optAir.value = '__airport_yes__';
  optAir.textContent = t('filter.withairport');
  optAir.dataset.i18n = 'filter.withairport';
  sel.appendChild(optAir);
  const optNoAir = document.createElement('option');
  optNoAir.value = '__airport_no__';
  optNoAir.textContent = t('filter.withoutairport');
  optNoAir.dataset.i18n = 'filter.withoutairport';
  sel.appendChild(optNoAir);
  sel.addEventListener('change', () => {
    currentGroupFilter = sel.value;
    renderMapMarkers();
  });
}

/* ============================================================
   ISLAND DETAIL PAGE
   Fetches islands/{key}.json — falls back to generic summary
============================================================ */
let currentIslandKey = '';

async function renderIslandPage(key) {
  currentIslandKey = key;
  setTimeout(updateShortlistButton, 50);
  const island = ISLANDS_DATA[key];
  if (!island) return;

  // Always tear down any stale mini map from a previous island.
  // The generic-fallback path below conditionally creates a Leaflet instance in
  // #island-mini-map, but the JSON-rich path doesn't — and it returns early
  // before the cleanup. Without this, navigating from a JSON-less island to a
  // JSON-rich one would leave the previous map visible at the top of the page.
  if (miniMapInstance) {
    try { miniMapInstance.remove(); } catch(e) {}
    miniMapInstance = null;
  }
  const miniMapElTop = document.getElementById('island-mini-map');
  if (miniMapElTop) {
    miniMapElTop.innerHTML = '';
    miniMapElTop.style.height = '';
    miniMapElTop.style.display = '';
  }

  document.getElementById('island-name').textContent = islandName(key);
  document.getElementById('island-meta-info').textContent = `${island.island_group} · ${fmtNum(island.area)} km² · Pop. ${fmtNum(island.pop)}`;

  const compareBtn = document.getElementById('detail-compare-btn');
  if (compareBtn) {
    compareBtn.dataset.islandKey = key;
    compareBtn.textContent = compareSelection.includes(key) ? '✓ In Compare' : '＋ Compare';
  }

  SCORE_DIMS.forEach(dim => {
    // car_need has a special rendering (pill), handled below — skip the stars loop
    if (dim === 'car_need') return;
    const bar = document.getElementById(`star-${dim}`);
    const val = document.getElementById(`val-${dim}`);
    if (bar) { bar.style.width = `${(island[dim] / 5) * 100}%`; bar.style.background = SCORE_COLORS[dim]; }
    if (val) val.textContent = fmt(island[dim]);
  });
  // Car-need pill in sidebar
  const carVal = document.getElementById('val-car');
  if (carVal) {
    carVal.innerHTML = carNeedHtml(island.car_need);
    const carItem = document.getElementById('rating-item-car');
    if (carItem) carItem.title = t('dim.car.hint');
  }
  document.getElementById('stat-area').textContent = `${fmtNum(island.area)} km²`;
  document.getElementById('stat-pop').textContent = fmtNum(island.pop);
  document.getElementById('stat-group').textContent = groupName(island.island_group);
  const statDays = document.getElementById('stat-days');
  if (statDays) statDays.textContent = island.days ? `${island.days} ${t('common.days')}` : '—';
  
  // Set ferry booking link based on island
  const ferryBtn = document.getElementById('detail-ferry-btn');
  if (ferryBtn) {
    // Map island keys to Ferryhopper URL slugs where they differ
    const ferrySlugMap = {
      'chania': 'chania', 'heraklion': 'heraklion', 'rethymno': 'rethymno',
      'lasithi': 'agios-nikolaos', // Lasithi region -> Agios Nikolaos is closest
      'lefkada': 'lefkada', 'kefalonia': 'kefalonia-sami',
      'zakynthos': 'zakynthos', 'ithaca': 'ithaki',
      'meganisi': 'meganisi', 'kythira': 'kythira', 'elafonisos': 'elafonisos',
      'santorini': 'santorini', 'mykonos': 'mykonos', 'naxos': 'naxos',
      'paros': 'paros', 'milos': 'milos', 'ios': 'ios',
      'sifnos': 'sifnos', 'folegandros': 'folegandros', 'amorgos': 'amorgos',
      'rhodes': 'rhodes', 'corfu': 'corfu',
      'skiathos': 'skiathos', 'skopelos': 'skopelos', 'alonnisos': 'alonnisos',
      'lesvos': 'mytilene', 'samos': 'samos', 'chios': 'chios', 'ikaria': 'ikaria',
      'hydra': 'hydra', 'spetses': 'spetses', 'aegina': 'aegina',
      'poros': 'poros', 'salamis': 'salamina',
      'agios-efstratios': 'agios-efstratios', 'psara': 'psara',
      'oinousses': 'oinousses', 'iraklia': 'iraklia',
      'tinos': 'tinos', 'syros': 'syros', 'andros': 'andros', 'serifos': 'serifos',
      'kythnos': 'kythnos', 'kea': 'kea-tzia', 'paxos': 'paxos',
      'thasos': 'thassos', 'samothrace': 'samothraki', 'skyros': 'skyros'
    };
    const slug = ferrySlugMap[island.key] || island.key;
    ferryBtn.href = `https://www.ferryhopper.com/en/ferries-to/${slug}`;
  }

  // Rent-a-car affiliate (DiscoverCars). Hidden on car-free / fully walkable islands
  // (car_need 1.0 — Hydra and the small islands where renting makes no sense).
  const carBtn = document.getElementById('detail-car-btn');
  if (carBtn) {
    if ((island.car_need || 0) > 1) {
      carBtn.href = 'https://www.discovercars.com/?a_aid=antaran2';
      carBtn.style.display = '';
    } else {
      carBtn.style.display = 'none';
    }
  }

  const guide = document.getElementById('island-guide');
  if (!guide) return;

  // Show loading state
  guide.innerHTML = `<div class="island-guide-box" style="text-align:center;padding:40px;color:var(--ink-3)">${t('fallback.loading').replace('{NAME}', islandName(key))}</div>`;

  // Try to fetch the island's JSON page data
  try {
    const res = await fetch(`/islands/${key}.json`);
    if (res.ok) {
      const data = await res.json();
      // Display "Last updated" from the HTTP Last-Modified response header —
      // GitHub Pages sets this from the underlying git commit time, so it
      // reflects when this island's JSON was actually edited.
      try {
        const lm = res.headers.get('Last-Modified');
        if (lm) {
          const lmDate = new Date(lm);
          if (!isNaN(lmDate.getTime())) {
            const lang = (typeof CURRENT_LANG !== 'undefined' && CURRENT_LANG === 'el') ? 'el' : 'en';
            const label = lang === 'el' ? 'Τελευταία ενημέρωση' : 'Last updated';
            const monthsEl = ['Ιανουαρίου','Φεβρουαρίου','Μαρτίου','Απριλίου','Μαΐου','Ιουνίου',
                              'Ιουλίου','Αυγούστου','Σεπτεμβρίου','Οκτωβρίου','Νοεμβρίου','Δεκεμβρίου'];
            const fmtDate = lang === 'el'
              ? `${lmDate.getDate()} ${monthsEl[lmDate.getMonth()]} ${lmDate.getFullYear()}`
              : lmDate.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
            const isoDate = lmDate.toISOString().split('T')[0];
            // Insert as a sibling of the meta pill if not already present
            const metaPill = document.getElementById('island-meta-info');
            if (metaPill && !document.getElementById('island-lastupdated')) {
              const stamp = document.createElement('div');
              stamp.id = 'island-lastupdated';
              stamp.className = 'island-lastupdated';
              stamp.innerHTML = `<time datetime="${isoDate}">${label}: <strong>${fmtDate}</strong></time>`;
              metaPill.parentNode.insertBefore(stamp, metaPill.nextSibling);
            }
          }
        }
      } catch(e) { /* non-fatal */ }
      guide.innerHTML = buildIslandPage(data, key);
      setTimeout(() => initItineraryMap(data.itinerary.days, data.beaches || []), 80);
      if (data.beaches) setTimeout(() => loadBeachPhotos(data.beaches), 150);
      return;
    }
  } catch(e) {
    // JSON not found — fall through to generic
  }

  // Generic fallback for islands without a JSON file yet
  const miniMapEl = document.getElementById('island-mini-map');
  if (miniMapEl) {
    if (miniMapInstance) { miniMapInstance.remove(); miniMapInstance = null; }
    miniMapEl.style.height = '220px';
    setTimeout(() => {
      miniMapInstance = L.map(miniMapEl, { zoomControl: false, attributionControl: false }).setView([island.lat, island.lng], 9);
      addThemeAwareTiles(miniMapInstance);
      L.marker([island.lat, island.lng]).addTo(miniMapInstance).bindPopup(islandName(island.key)).openPopup();
    }, 50);
  }

  guide.innerHTML = `
    <div class="island-guide-box">
      <h3>${t('fallback.summary')}</h3>
      <p>${islandName(key)} ${t('fallback.scores').replace('{SCORE}', fmt(island.total))}
      ${island.beach >= 4.5 ? t('fallback.beach') : ''}
      ${island.hist >= 4.5 ? t('fallback.hist') : ''}
      ${island.night >= 4.5 ? t('fallback.night') : ''}
      ${island.afford >= 4.2 ? t('fallback.afford_high') : ''}
      ${island.afford <= 1.5 ? t('fallback.afford_low') : ''}
      ${island.access >= 4.5 ? t('fallback.access_high') : ''}
      ${island.access <= 2.0 ? t('fallback.access_low') : ''}
      </p>
      <p style="margin-top:12px;font-size:13px;color:var(--ink-3)">${t('fallback.coming_soon')}</p>
      <p style="margin-top:10px"><a href="#" onclick="window._addCmpNav('${key}')">${t('fallback.compare_link')}</a></p>
    </div>`;
}

/* ============================================================
   ISLAND PAGE BUILDER — works with any island's JSON
============================================================ */
function buildIslandPage(data, key) {
  const itin = data.itinerary;

  // Normalize per-day colors to one on-brand ramp (turquoise → terracotta →
  // olive → amber → plum → deep teal) so day buttons, cards, the route lines
  // and markers all share a harmonious sequence instead of ad-hoc JSON colors.
  (itin.days || []).forEach((d, i) => { d.color = DAY_COLOR_RAMP[i % DAY_COLOR_RAMP.length]; });

  const dayBtns = itin.days.map(d =>
    `<button class="itin-day-btn" data-day="${d.day}" onclick="filterItinDay(${d.day})" style="border-color:${d.color};color:${d.color}"><span>${t("detail.day")} ${d.day}: ${pickLang(d, "title")}</span></button>`
  ).join('');

  const dayCards = itin.days.map(d => {
    const isEl = (typeof CURRENT_LANG !== 'undefined' && CURRENT_LANG === 'el');
    const stopArr = d.stops.map((s, i) => {
      const nameHtml = s.wiki
        ? `<a href="${s.wiki}" target="_blank" rel="noopener" class="itin-stop-link">${pickLang(s, "name")}</a>`
        : pickLang(s, "name");
      const timeHtml = s.time ? `<span class="itin-stop-time">${s.time}</span>` : '';
      const hasPhoto = !!s.photo;
      const photoHtml = hasPhoto
        ? `<div class="itin-stop-photo-wrap">${buildLightboxImg(s.photo, s.name, s.photo_credit, 'itin-stop-photo', 'onerror="this.parentElement.style.display=\'none\'"')}${buildPhotoCredit(s.photo_credit)}</div>`
        : '';
      return `<div class="itin-stop${hasPhoto ? ' has-photo' : ''}">
        <div class="itin-stop-num" style="background:${d.color}">${i + 1}</div>
        <div class="itin-stop-content">
          <div class="itin-stop-text">
            <div class="itin-stop-name-row">${nameHtml}${timeHtml}</div>
            ${s.drive ? `<div class="itin-stop-drive">🚗 ${isEl ? (s.drive_el || s.drive) : s.drive}</div>` : ''}
            <div class="itin-stop-desc">${pickLang(s, "desc")}</div>
          </div>
          ${photoHtml}
        </div>
      </div>`;
    });
    // Meal-timing cues placed in the route at each meal's slot (food itself is in the Eat & Drink panel below)
    const _foods = Array.isArray(d.food) ? d.food : (d.food ? [d.food] : []);
    const _cues = _foods.filter(f => f && (f.meal || f.desc)).map(f => {
      const _meal = ((isEl ? f.meal_el : f.meal) || '').toLowerCase();
      const _area = (isEl ? f.area_el : f.area) || '';
      return { idx: f.after ? d.stops.findIndex(x => x.name === f.after) : -1,
        html: `<div class="itin-meal-cue">🍴 ${isEl ? 'Στάση για' : 'Stop for'} ${_meal}${_area ? ' · ' + _area : ''} — ${isEl ? 'δες «Φαγητό & Ποτό» πιο κάτω' : 'see Eat & Drink below'}</div>` };
    });
    _cues.sort((a, b) => b.idx - a.idx).forEach(c => { if (c.idx >= 0) stopArr.splice(c.idx + 1, 0, c.html); else stopArr.push(c.html); });
    const stops = stopArr.join('');
    const driveInfo = d.km ? `<span class="itin-day-meta">${d.km} ${t('common.km')} · ${d.drive_mins} ${t('common.mindrive')}</span>` : '';
    let overnightHtml = '';
    if (d.overnight) {
      const overnightText = pickLang(d, 'overnight');
      const escAttr = (s) => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');
      // Departure-day detection: if the overnight value is "Departure" / "Αναχώρηση"
      // (or starts with those — handles "Αναχώρηση πρωί" etc), render plainly without
      // the "Sleep:" prefix and without a Booking.com link (you can't sleep there
      // that night — you're leaving). Compare in a case- and accent-insensitive way
      // so "αναχώρηση" / "Αναχώρηση" / "ΑΝΑΧΩΡΗΣΗ" all match.
      const normalised = overnightText.trim().toLowerCase()
        .normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      const isDeparture = normalised.startsWith('departure') ||
                          normalised.startsWith('αναχωρηση') ||  // El after stripping diacritics
                          normalised.startsWith('αναχωρησηs');   // safety net
      if (isDeparture) {
        // Render the bare word, no "Sleep:" prefix, no Booking link.
        const inner = `🌙 ${overnightText}`;
        overnightHtml = `<span class="itin-overnight itin-overnight--departure" style="border-color:${d.color};color:${d.color}">${inner}</span>`;
      } else {
        const inner = `🌙 ${t('common.sleep')}: ${overnightText}`;
        if (BOOKING_READY && BOOKING_ENABLED_ISLANDS.has(currentIslandKey)) {
          // Search-URL strategy — Booking.com matches the hotel name to its inventory.
          // Encoding the hotel name + island keeps the search tight.
          const islandName = ISLANDS_DATA[currentIslandKey] ? ISLANDS_DATA[currentIslandKey].name : '';
          const query = encodeURIComponent(`${overnightText} ${islandName}`);
          const href = `https://www.booking.com/searchresults.html?ss=${query}&aid=${BOOKING_AID}`;
          overnightHtml = `<a href="${href}" target="_blank" rel="noopener sponsored" class="itin-overnight itin-overnight--booking" style="border-color:${d.color};color:${d.color}" aria-label="${escAttr(t('common.booking_aria'))}">${inner} <span class="itin-overnight-cta">→ ${t('common.book_hotel')}</span></a>`;
        } else {
          overnightHtml = `<span class="itin-overnight" style="border-color:${d.color};color:${d.color}">${inner}</span>`;
        }
      }
    }
    // Eat & Drink panel — one row per meal + nightlife, separated from the routed stops.
    let edRows = '';
    _foods.forEach(f => {
      if (!(f && (f.meal || f.desc))) return;
      const meal = (isEl ? f.meal_el : f.meal) || (isEl ? 'Φαγητό' : 'Food');
      const area = (isEl ? f.area_el : f.area) || '';
      const fdesc = (isEl ? f.desc_el : f.desc) || f.desc || '';
      const head = area ? `${meal} · ${area}` : meal;
      edRows += `<div class="ed-row"><span class="ed-icon">🍴</span><div class="ed-text"><div class="ed-head">${head}</div><div class="ed-body">${fdesc}</div></div></div>`;
    });
    const nlText = pickLang(d, 'nightlife');
    if (nlText) {
      const nlTitle = isEl ? 'Νυχτερινή ζωή' : 'Nightlife';
      edRows += `<div class="ed-row"><span class="ed-icon">🍸</span><div class="ed-text"><div class="ed-head">${nlTitle}</div><div class="ed-body">${nlText}</div></div></div>`;
    }
    const eatDrink = edRows ? `<div class="itin-eatdrink"><div class="ed-title">${isEl ? 'Φαγητό & Ποτό' : 'Eat & Drink'}</div>${edRows}</div>` : '';
    return `<div class="itin-day-card" id="itin-day-card-${d.day}">
      <div class="itin-day-header" style="border-left:4px solid ${d.color}">
        <div class="itin-day-header-main">
          <span class="itin-day-label" style="color:${d.color}">${t("detail.day")} ${d.day}</span>
          <span class="itin-day-title">${pickLang(d, "title")}</span>
          ${driveInfo}
        </div>
        ${overnightHtml}
      </div>
      <div class="itin-stops">${stops}</div>
      ${eatDrink}
    </div>`;
  }).join('');

  const beachCards = (data.beaches || []).map((b, i) => {
    const nameHtml = b.wiki
      ? `<a href="${b.wiki}" target="_blank" rel="noopener" class="beach-name-link">${pickLang(b, "name")}</a>`
      : pickLang(b, "name");
    const photoId = `beach-photo-${i}`;
    // Support direct photo URL (Cloudinary, Unsplash etc) OR Wikimedia commons filename
    const photoHtml = b.photo
      ? `<div class="beach-photo-wrap">${buildLightboxImg(b.photo, b.name, b.photo_credit, 'beach-photo', 'onerror="this.parentElement.parentElement.style.display=\'none\'"')}${buildPhotoCredit(b.photo_credit)}</div>`
      : '';
    const beachId = (currentIslandKey + '_' + b.name).replace(/[^a-z0-9]/gi, '_').toLowerCase();
    return `<div class="beach-card">
      ${photoHtml}
      <div class="beach-card-body">
        <div class="beach-rank-name">
          <div class="beach-rank">${i + 1}</div>
          <div class="beach-name-stars">
            <div class="beach-name">${nameHtml}</div>
            <div class="beach-ratings-row">
              <div class="beach-rating-block">
                <span class="beach-rating-label">${t("detail.editorial")}</span>
                <div class="beach-stars">${'\u2605'.repeat(b.rating || 4)}${'\u2606'.repeat(5 - (b.rating || 4))}</div>
              </div>
            </div>
          </div>
        </div>
        <p class="beach-desc">${pickLang(b, "desc")}</p>
        <div class="beach-specs">
          <div class="beach-spec"><span class="beach-spec-label">${t("detail.spec.type")}</span><span class="beach-spec-val">${pickLang(b, "type")}</span></div>
          <div class="beach-spec"><span class="beach-spec-label">${t("detail.spec.length")}</span><span class="beach-spec-val">${pickLang(b, "length")}</span></div>
          <div class="beach-spec"><span class="beach-spec-label">${t("detail.spec.depth")}</span><span class="beach-spec-val">${pickLang(b, "depth")}</span></div>
          <div class="beach-spec"><span class="beach-spec-label">${t("detail.spec.wind")}</span><span class="beach-spec-val">${interpretFacing(pickLang(b, "facing"), CURRENT_LANG)}</span></div>
          <div class="beach-spec beach-spec-full"><span class="beach-spec-label">${t("detail.spec.facilities")}</span><span class="beach-spec-val">${pickLang(b, "facilities")}</span></div>
        </div>
      </div>
    </div>`;
  }).join('');

  const introHtml = data.intro ? `<div class="itin-island-intro"><p>${pickLang(data, 'intro')}</p></div>` : '';

  // Characteristic hero photo: first available itinerary-stop photo, else first beach photo.
  // Mirrors find_hero_image() in prerender.py so the SPA matches the static SEO page.
  let _hp = null, _hc = null, _hn = '';
  for (const _d of itin.days) {
    for (const _s of (_d.stops || [])) { if (_s.photo) { _hp = _s.photo; _hc = _s.photo_credit; _hn = pickLang(_s, 'name'); break; } }
    if (_hp) break;
  }
  if (!_hp && Array.isArray(data.beaches)) {
    for (const _b of data.beaches) { if (_b.photo) { _hp = _b.photo; _hc = _b.photo_credit; _hn = pickLang(_b, 'name'); break; } }
  }
  const heroHtml = _hp
    ? `<figure class="island-hero">${buildLightboxImg(_hp, islandName(key) + (_hn ? ' — ' + _hn : ''), _hc, 'island-hero-img', '')}${buildPhotoCredit(_hc)}</figure>`
    : '';
  const gettingThereHtml = buildGettingThereSection(data);
  // Build the "Top Beaches of X" heading. English: simple concatenation.
  // Greek: use the genitive form + the right article (της/του/των) based on
  // grammatical gender so we say "Παραλίες της Λέσβου" / "του Πόρου" /
  // "των Παξών" (plural).
  let beachHeading;
  if (CURRENT_LANG === 'el') {
    const g = data.gender_el || '';
    let article = 'της';
    if (g === 'm' || g === 'n') article = 'του';
    else if (g.startsWith('pl')) article = 'των';
    const genitive = data.name_genitive_el || data.name_el || islandName(currentIslandKey);
    beachHeading = `${t("detail.beaches.title")} ${article} ${genitive}`;
  } else {
    beachHeading = `${t("detail.beaches.title")} ${islandName(currentIslandKey)}`;
  }
  // When `beaches_intro` is present (islands targeting "best beach in X"),
  // override the heading and render the declarative top-pick prose above the
  // beach list. Mirrors the prerender so SPA-rendered view matches what
  // Google indexed.
  const beachesIntroObj = data.beaches_intro || {};
  const beachesIntroText = (CURRENT_LANG === 'el' ? beachesIntroObj.el : beachesIntroObj.en) || '';
  let beachesIntroHtml = '';
  if (beachesIntroText) {
    const escHtml = (s) => String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
    const paras = beachesIntroText.split(/\n\n+/).map(p => p.trim()).filter(Boolean);
    const htmlParas = paras.map(p => {
      const escaped = escHtml(p);
      return `<p>${escaped.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')}</p>`;
    }).join('');
    beachesIntroHtml = `<div class="itin-beaches-intro">${htmlParas}</div>`;
    // Override the heading to use the target query phrase.
    if (CURRENT_LANG === 'el') {
      beachHeading = `Καλύτερη παραλία — ${data.name_el || islandName(currentIslandKey)}`;
    } else {
      beachHeading = `Best beach in ${islandName(currentIslandKey)}`;
    }
  }
  const beachSection = beachCards ? `
    <div class="itin-beaches-section">
      <div class="itin-beaches-header">
        <h2 class="itin-beaches-title">${beachHeading}</h2>
        <p class="itin-beaches-sub">${t("detail.beaches.sub")}</p>
      </div>
      ${beachesIntroHtml}
      <div class="itin-beaches-list">${beachCards}</div>
    </div>` : '';

  return `
    <div class="itin-wrapper">
      <div class="itin-hero">
        <h2 class="itin-title">${pickLang(itin, "title")}</h2>
        <p class="itin-subtitle">${pickLang(itin, "subtitle")}</p>
      </div>
      ${heroHtml}
      ${introHtml}
      ${buildSuitedForSection(data)}
      ${buildAudienceSections(data)}
      ${gettingThereHtml}
      ${buildWhenToVisitSection(data)}
      <div class="itin-day-filter">
        <button class="itin-day-btn active" data-day="all" onclick="filterItinDay('all')" style="border-color:var(--ink-2);color:var(--ink-1)"><span style="color:inherit">${t("detail.alldays")}</span></button>
        ${dayBtns}
      </div>
      <div class="itin-map-wrap">
        <div id="itin-map"></div>
      </div>
      <div class="itin-days" id="itin-days-container">${dayCards}</div>
      ${beachSection}
      ${buildLocalSection(data)}
      ${buildSimilarIslandsSection(key)}
    </div>`;
}

/* Renders the "Good for / Skip if" orientation block. Two short lists that
   help a reader self-select before reading the full guide. Only renders if
   data.suited_for is present (rolled out to thinner islands first). */
function buildSuitedForSection(data) {
  const sf = data.suited_for;
  if (!sf) return '';
  const lang = (typeof CURRENT_LANG !== 'undefined' && CURRENT_LANG === 'el') ? 'el' : 'en';
  const escHtml = (s) => String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

  const good = (lang === 'el' ? sf.good_el : sf.good) || [];
  const skip = (lang === 'el' ? sf.skip_el : sf.skip) || [];
  if (!good.length && !skip.length) return '';

  const goodTitle = lang === 'el' ? 'Ιδανικό για' : 'Good for';
  const skipTitle = lang === 'el' ? 'Σκέψου αλλιώς αν' : 'Maybe skip if';

  const li = (items) => items.map(x => `<li>${escHtml(x)}</li>`).join('');

  return `
    <div class="itin-suited">
      <div class="itin-suited-col itin-suited-good">
        <h3 class="itin-suited-title">${goodTitle}</h3>
        <ul>${li(good)}</ul>
      </div>
      <div class="itin-suited-col itin-suited-skip">
        <h3 class="itin-suited-title">${skipTitle}</h3>
        <ul>${li(skip)}</ul>
      </div>
    </div>`;
}

/* Renders audience pitches ("Naxos for families", "Milos for hikers", etc.)
   Mirrors the prerender's audience rendering so the SPA-loaded page matches
   what Google indexes. Each entry in data.audience is keyed by audience name
   ('families', 'couples', 'hikers'...) and contains markdown-light prose in
   'en' and 'el'. **Bold** subheaders become <strong>. */
function buildAudienceSections(data) {
  const audience = data.audience;
  if (!audience || typeof audience !== 'object') return '';

  const lang = (typeof CURRENT_LANG !== 'undefined' && CURRENT_LANG === 'el') ? 'el' : 'en';
  const escHtml = (s) => String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

  // Label map — keep in sync with AUDIENCE_LABELS in tools/prerender.py.
  const AUDIENCE_LABELS = {
    families:   ['for families',           'για οικογένειες'],
    couples:    ['for couples',            'για ζευγάρια'],
    hikers:     ['for hikers',             'για πεζοπόρους'],
    solo:       ['for solo travelers',     'για μοναχικούς ταξιδιώτες'],
    foodies:    ['for foodies',            'για καλοφαγάδες'],
    first_time: ['for first-time visitors','για πρώτη επίσκεψη'],
  };

  const name = (lang === 'el' && data.name_el) ? data.name_el : (data.name || '');

  const blocks = [];
  for (const key of Object.keys(audience)) {
    const entry = audience[key] || {};
    const text = (lang === 'el' ? entry.el : entry.en) || '';
    if (!text) continue;
    const labels = AUDIENCE_LABELS[key] || [key, key];
    const suffix = lang === 'el' ? labels[1] : labels[0];
    const heading = `${name} ${suffix}`;

    const paras = text.split(/\n\n+/).map(p => p.trim()).filter(Boolean);
    const htmlParas = paras.map(p => {
      const escaped = escHtml(p);
      return `<p>${escaped.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')}</p>`;
    }).join('');

    blocks.push(
      `<section class="itin-audience" data-audience="${escHtml(key)}">
        <h2 class="itin-audience-title">${escHtml(heading)}</h2>
        ${htmlParas}
      </section>`
    );
  }
  return blocks.join('');
}

function buildGettingThereSection(data) {
  const gt = data.getting_there;
  if (!gt || !gt.pills) return '';

  const lang = (typeof CURRENT_LANG !== 'undefined' && CURRENT_LANG === 'el') ? 'el' : 'en';
  const escHtml = (s) => String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');

  const title = t('getting_there.title');
  const tipLabel = t('getting_there.tip');
  const showMoreLabel = lang === 'el' ? 'Διαβάστε αναλυτικά →' : 'Read full route →';
  const showLessLabel = lang === 'el' ? '← Σύμπτυξη' : '← Show less';

  const pills = (lang === 'el' ? gt.pills_el : gt.pills) || [];
  const summary = (lang === 'el' ? gt.summary_el : gt.summary) || '';
  const tip = lang === 'el' ? gt.tip_el : gt.tip;

  const pillHtml = pills.length
    ? `<div class="itin-gt-pills">${pills.map(p => `<span class="itin-gt-pill">${escHtml(p)}</span>`).join('')}</div>`
    : '';

  // Detailed long-form content (for islands targeting "how to get to X" search
  // queries). When `getting_there.detailed` is present in the JSON, render the
  // SEO-targeted heading + full prose instead of the short summary + toggle.
  // Mirrors the prerender logic so the SPA view matches what Google sees.
  const detailedObj = gt.detailed || {};
  const detailedText = (lang === 'el' ? detailedObj.el : detailedObj.en) || '';
  if (detailedText) {
    // Markdown-light: blank-line-separated paragraphs, **bold** subheaders.
    const paras = detailedText.split(/\n\n+/).map(p => p.trim()).filter(Boolean);
    const htmlParas = paras.map(p => {
      // Escape first, then unescape the **bold** wrappers and replace with <strong>.
      // Doing it in this order means the user-facing text inside the bold can't
      // inject HTML, but the bold marker itself becomes proper markup.
      const escaped = escHtml(p);
      return `<p>${escaped.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')}</p>`;
    }).join('');

    // SEO heading: literal target query in EN; gender-aware accusative in EL.
    const name = (lang === 'el' && data.name_el) ? data.name_el : (data.name || '');
    let heading;
    if (lang === 'en') {
      heading = `How to get to ${name}`;
    } else {
      const acc = data.name_accusative_el || name;
      const gender = (data.gender_el || 'f').toLowerCase();
      const prep = { f: 'στη', m: 'στον', n: 'στο', p: 'στα' }[gender] || 'στη';
      heading = `Πώς να πας ${prep} ${acc}`;
    }

    return `
      <section class="itin-getting-there">
        <h3 class="itin-getting-there-title">${escHtml(heading)}</h3>
        ${pillHtml}
        ${htmlParas}
      </section>`;
  }

  // Split the summary into lead (visible) + rest (collapsed). Accumulate
  // sentences into the lead until we have >= 80 chars, so we don't leave
  // a useless stub like "No airport." as the only visible text.
  let leadHtml = '';
  let restHtml = '';
  if (summary) {
    const tokens = summary.split(/([.!?:](?:\s+|$))/);
    const sentences = [];
    let buf = '';
    for (const tok of tokens) {
      buf += tok;
      if (/^[.!?:](\s+|$)/.test(tok)) { sentences.push(buf); buf = ''; }
    }
    if (buf) sentences.push(buf);
    let lead = '';
    let rest = '';
    for (let i = 0; i < sentences.length; i++) {
      if (lead.length >= 80) {
        rest = sentences.slice(i).join('').trim();
        break;
      }
      lead += sentences[i];
    }
    lead = lead.trimEnd();
    // Merge a trivially short "rest" back into the lead — no toggle needed.
    if (rest && rest.length < 60) {
      lead = (lead + ' ' + rest).trim();
      rest = '';
    }
    if (rest) {
      leadHtml = `<p class="itin-gt-summary itin-gt-lead">${escHtml(lead)}</p>`;
      restHtml = `<p class="itin-gt-summary itin-gt-rest">${escHtml(rest)}</p>`;
    } else {
      leadHtml = `<p class="itin-gt-summary itin-gt-lead">${escHtml(lead)}</p>`;
    }
  }
  const tipHtml = tip ? `<p class="itin-gt-tip"><strong>${escHtml(tipLabel)}:</strong> ${escHtml(tip)}</p>` : '';

  if (!pillHtml && !leadHtml) return '';

  // If there's collapsed content, render a toggle. Otherwise just the lead.
  const hasMore = restHtml || tipHtml;
  const moreBlock = hasMore
    ? `<div class="itin-gt-more" hidden>${restHtml}${tipHtml}</div>
       <button type="button" class="itin-gt-toggle"
               data-show="${escHtml(showMoreLabel)}"
               data-hide="${escHtml(showLessLabel)}"
               aria-expanded="false"
               onclick="toggleGettingThereMore(this)">${escHtml(showMoreLabel)}</button>`
    : '';

  return `
    <section class="itin-getting-there">
      <h3 class="itin-getting-there-title">${escHtml(title)}</h3>
      ${pillHtml}
      ${leadHtml}
      ${moreBlock}
    </section>`;
}

/* Toggle handler for the "Read full route" reveal. Toggles the .itin-gt-more
   block's hidden attribute and swaps the button label. Inline in script.js
   so it's available globally; not exposed via window.* because the onclick
   attribute resolves names from the global scope on click. */
function toggleGettingThereMore(btn) {
  const section = btn.closest('.itin-getting-there');
  if (!section) return;
  const more = section.querySelector('.itin-gt-more');
  if (!more) return;
  const expanded = !more.hasAttribute('hidden');
  if (expanded) {
    more.setAttribute('hidden', '');
    btn.setAttribute('aria-expanded', 'false');
    btn.textContent = btn.dataset.show;
  } else {
    more.removeAttribute('hidden');
    btn.setAttribute('aria-expanded', 'true');
    btn.textContent = btn.dataset.hide;
  }
}

/* ============================================================
   WHEN-TO-VISIT SECTION — 12-month grid + summary paragraph
   Renders only if data.when_to_visit is present.
============================================================ */
/* Photo credit badge — a tiny info dot in the corner that reveals the full
   CC attribution on click. Stops click propagation so it doesn't trigger the
   lightbox underneath. Returns empty string if no credit data present. */
function buildPhotoCredit(credit) {
  if (!credit || typeof credit !== 'object') return '';
  const artist = (credit.artist || '').replace(/"/g, '&quot;');
  const license = (credit.license || '').replace(/"/g, '&quot;');
  if (!artist && !license) return '';
  const pageUrl = credit.page_url || '';
  const text = artist
    ? (license ? `© ${artist} / ${license}` : `© ${artist}`)
    : license;
  const linkedText = pageUrl
    ? `<a href="${pageUrl}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation()">${text}</a>`
    : text;
  return `<button type="button" class="photo-credit-badge" aria-label="Image credit" onclick="event.stopPropagation();this.classList.toggle('open')">i<span class="photo-credit-text">${linkedText}</span></button>`;
}

/* Build an <img> tag that participates in the lightbox. Embeds credit
   metadata as data-* attributes so the lightbox can read them on click
   without traversing the DOM. */
function buildLightboxImg(src, alt, credit, extraClass, extraAttrs) {
  const safeSrc = (src || '').replace(/"/g, '&quot;');
  const safeAlt = (alt || '').replace(/"/g, '&quot;');
  const c = credit || {};
  const dataAttrs = [
    `data-credit-artist="${(c.artist || '').replace(/"/g, '&quot;')}"`,
    `data-credit-license="${(c.license || '').replace(/"/g, '&quot;')}"`,
    `data-credit-page-url="${(c.page_url || '').replace(/"/g, '&quot;')}"`,
  ].join(' ');
  const cls = `lightbox-img${extraClass ? ' ' + extraClass : ''}`;
  return `<img class="${cls}" src="${safeSrc}" alt="${safeAlt}" loading="lazy" ${dataAttrs}${extraAttrs ? ' ' + extraAttrs : ''}>`;
}

function buildWhenToVisitSection(data) {
  const w = data.when_to_visit;
  if (!w || !Array.isArray(w.months) || w.months.length !== 12) return '';

  const lang = (typeof CURRENT_LANG !== 'undefined' && CURRENT_LANG === 'el') ? 'el' : 'en';
  const monthNames = lang === 'el'
    ? ['Ιαν','Φεβ','Μάρ','Απρ','Μάι','Ιούν','Ιούλ','Αύγ','Σεπ','Οκτ','Νοέ','Δεκ']
    : ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

  // Build the ribbon: 12 colored cells, one per month. The `title` attribute
  // gives native browser tooltips on hover (desktop). Mobile users get the
  // vertical list (.wtv-vertical) instead, where labels are inline.
  // `limited: true` on a month adds the .wtv-limited modifier — visually
  // dims the cell and shows a "Limited service" prefix in the tooltip.
  const limitedLabel = lang === 'el'
    ? 'Περιορισμένη λειτουργία'
    : 'Limited service';
  const ribbonCells = w.months.map((m, i) => {
    const tag = (m.tag || 'ok').toLowerCase();
    const why = pickLang(m, 'why') || '';
    const isLimited = m.limited === true;
    const prefix = isLimited ? `${limitedLabel} — ` : '';
    const safeWhy = (prefix + why).replace(/"/g, '&quot;');
    const cls = `wtv-cell wtv-${tag}${isLimited ? ' wtv-limited' : ''}`;
    return `<div class="${cls}" title="${monthNames[i]} — ${safeWhy}">${monthNames[i]}</div>`;
  }).join('');

  // "Highlights" line above the ribbon. Groups months by tag and renders
  // "Best: Jun, Sep · Great: Jul · Avoid: Oct–May" — the reader's actual
  // question is "when do I come?" and this answers it in one line.
  const monthAbbr = monthNames; // same array
  const tagGroups = { perfect: [], great: [], ok: [], avoid: [] };
  w.months.forEach((m, i) => {
    const tag = (m.tag || 'ok').toLowerCase();
    if (tagGroups[tag]) tagGroups[tag].push(i);
  });
  // Format a list of month indices into "Jun, Sep" or "Oct–May" (range)
  // if they're contiguous (handles year-wrap for avoid months).
  const fmtMonthList = (indices) => {
    if (!indices.length) return '';
    if (indices.length <= 3) {
      return indices.map(i => monthAbbr[i]).join(', ');
    }
    // Try a contiguous run; allow year-wrap (Oct, Nov, Dec, Jan, Feb...)
    const sorted = [...indices].sort((a, b) => a - b);
    // Check wrap: is there a gap in the middle larger than the gap end→start+12?
    let gapStart = -1, maxGap = 0;
    for (let i = 0; i < sorted.length - 1; i++) {
      const g = sorted[i+1] - sorted[i];
      if (g > maxGap) { maxGap = g; gapStart = i; }
    }
    const wrapGap = (12 - sorted[sorted.length-1] - 1) + sorted[0] + 1;
    if (maxGap === 1 && wrapGap > 1) {
      // Contiguous, no wrap: e.g. May–Sep
      return `${monthAbbr[sorted[0]]}–${monthAbbr[sorted[sorted.length-1]]}`;
    }
    if (maxGap > 1 && wrapGap === 1 && sorted.length === (12 - (maxGap - 1))) {
      // Wrap-around contiguous: e.g. Oct–May (everything except Jun–Sep)
      const first = sorted[gapStart + 1];
      const last = sorted[gapStart];
      return `${monthAbbr[first]}–${monthAbbr[last]}`;
    }
    // Fallback: comma list
    return sorted.map(i => monthAbbr[i]).join(', ');
  };
  const tagLabels = lang === 'el'
    ? { perfect: 'Τέλεια', great: 'Καλά', ok: 'Μέτρια', avoid: 'Απόφυγε' }
    : { perfect: 'Best', great: 'Great', ok: 'OK', avoid: 'Avoid' };
  const highlightOrder = ['perfect', 'great', 'ok', 'avoid'];
  const highlightHtml = highlightOrder
    .filter(t => tagGroups[t].length)
    .map(t => `<span class="wtv-hl-item wtv-hl-${t}"><strong>${tagLabels[t]}:</strong> ${fmtMonthList(tagGroups[t])}</span>`)
    .join('<span class="wtv-hl-sep">·</span>');

  // Separate line for months with limited services — orthogonal to the
  // good/bad tag. An island can be a "Great" month AND have limited
  // service (shoulder season) OR can be "Avoid" but fully open (peak
  // crowds in August). This line is shown only if any month is flagged.
  const limitedIndices = [];
  w.months.forEach((m, i) => { if (m.limited === true) limitedIndices.push(i); });
  const limitedLine = limitedIndices.length
    ? `<div class="wtv-limited-note"><strong>${limitedLabel}:</strong> ${fmtMonthList(limitedIndices)}</div>`
    : '';

  const highlightsBar = highlightHtml
    ? `<div class="wtv-highlights">${highlightHtml}</div>${limitedLine}`
    : limitedLine;

  const summary = pickLang(w, 'summary') || '';
  const summaryHtml = summary ? `<p class="wtv-summary">${summary}</p>` : '';

  const tagsPresent = new Set(w.months.map(m => (m.tag || 'ok').toLowerCase()));
  const legend = highlightOrder
    .filter(t => tagsPresent.has(t))
    .map(t => `<span class="wtv-legend-item"><span class="wtv-legend-swatch wtv-${t}"></span>${tagLabels[t]}</span>`)
    .join('');

  // Mobile vertical list — 12 rows, one per month, with tag swatch + caption.
  // Limited months get a "·" indicator next to the why text.
  const verticalRows = w.months.map((m, i) => {
    const tag = (m.tag || 'ok').toLowerCase();
    const why = pickLang(m, 'why') || '';
    const isLimited = m.limited === true;
    const limitedBadge = isLimited
      ? `<span class="wtv-v-limited-badge" title="${limitedLabel}">·</span>`
      : '';
    const cls = `wtv-vrow wtv-v-${tag}${isLimited ? ' wtv-v-limited' : ''}`;
    return `<div class="${cls}">
      <div class="wtv-vmonth">${monthNames[i]}</div>
      <div class="wtv-vbar wtv-${tag}" title="${tagLabels[tag] || ''}"></div>
      <div class="wtv-vwhy">${limitedBadge}${why}</div>
    </div>`;
  }).join('');

  return `
    <details class="wtv-section" open>
      <summary class="wtv-title">${t('wtv.title')}</summary>
      ${summaryHtml}
      ${highlightsBar}
      <div class="wtv-ribbon-wrap">
        <div class="wtv-ribbon">
          ${ribbonCells}
        </div>
      </div>
      <div class="wtv-vertical">${verticalRows}</div>
      <div class="wtv-legend">${legend}</div>
    </details>`;
}

/* ============================================================
   LOCAL & SEASONAL SECTION
   Renders only if specialties / crafts / festivals are present.
============================================================ */
/* ============================================================
   "Islands like this one" — similarity recommendations
   ------------------------------------------------------------
   Computes a weighted distance over scores, character flags,
   group, and rough size. Returns the N closest matches.
   Renders a card grid below the main island content.
============================================================ */
/* ------------------------------------------------------------
   Archetype profile — derives 7 latent vibe scores from raw
   fields. This captures things like "remote outpost", "tiny
   weekend escape", "big working island" that aren't in any
   single field but emerge from combinations.
   Each archetype is 0..1.
   ------------------------------------------------------------ */
function islandArchetypes(x) {
  const pop      = x.pop || 1;
  const area     = x.area || 50;
  const beach    = x.beach || 0;
  const hist     = x.hist || 0;
  const night    = x.night || 0;
  const access   = x.access || 0;
  const drama    = !!x.drama;
  const hiking   = !!x.hiking;
  const chora    = !!x.chora;

  // Remote outpost — hard to reach + small permanent population.
  // Captures: Agios Efstratios, Kastellorizo, Gavdos, Anafi, Psara.
  const remote = Math.max(0, (3 - access)) / 3 * 0.6
               + Math.max(0, (1000 - pop)) / 1000 * 0.4;

  // Tiny weekend escape — small footprint, easy day-trip-able.
  // Captures: Agistri, Ammouliani, Schoinoussa, Therasia, Donousa.
  const tiny = Math.max(0, (40 - area)) / 40 * 0.5
             + Math.max(0, (2500 - pop)) / 2500 * 0.5;

  // Party — high nightlife AND large enough to actually host a scene.
  // Sleepy island with one beach bar shouldn't score as "party".
  const party = (night / 5) * (pop > 5000 ? 1 : pop / 5000);

  // Big working island — substantial population & area, real life beyond tourism.
  // Captures: Lesvos, Chios, Samos, Crete regions, Kefalonia, Rhodes.
  const working = (Math.min(pop / 30000, 1) + Math.min(area / 500, 1)) / 2;

  // Postcard / aesthetic — dramatic landscape, beautiful chora, top beach scores.
  // Captures: Santorini, Folegandros, Anafi, Symi, Sikinos.
  const postcard = (drama ? 0.4 : 0)
                 + beach / 5 * 0.3
                 + (chora ? 0.2 : 0)
                 + Math.max(0, (300 - area)) / 300 * 0.1;

  // Active / nature-driven — hiking flag is the main signal.
  // Captures: Andros, Crete (Chania/Lasithi), Ikaria, Naxos hinterland.
  const active = (hiking ? 0.6 : 0)
               + (drama ? 0.2 : 0)
               + Math.max(0, (3 - night)) / 3 * 0.2;

  // Historic depth — high history score, especially with chora preserved.
  const historic = (hist / 5) * (chora || hist >= 4 ? 1.0 : 0.5);

  return { remote, tiny, party, working, postcard, active, historic };
}

/* ------------------------------------------------------------
   Distance function — archetype-first.
   Primary signal: Euclidean distance over the 7 archetypes,
   weighted up by how strongly the TARGET expresses each one
   (an island that's mostly "remote" cares most about other
   islands' remote score).
   Secondary: small bonuses for same ferry region and proximity.
   ------------------------------------------------------------ */
function similarIslandDistance(target, candidate, targetArc) {
  const a = target;
  const b = candidate;
  const arcA = targetArc;          // pre-computed once per call to findSimilarIslands
  const arcB = islandArchetypes(b);

  // Weighted Euclidean over archetypes
  let arcSum = 0;
  Object.keys(arcA).forEach(k => {
    const gap = arcA[k] - arcB[k];
    const weight = 1.0 + arcA[k] * 1.5;   // 1.0 (target weak in k) → 2.5 (target strong)
    arcSum += gap * gap * weight;
  });
  let d = Math.sqrt(arcSum) * 2.5;

  // Small character-flag mismatch penalty (catches edge cases archetypes miss)
  ['drama', 'hiking', 'chora', 'sailing', 'springs'].forEach(f => {
    if (!!a[f] !== !!b[f]) d += 0.15;
  });

  // Same ferry region — modest bonus (NOT dominant — that was the old bug)
  if (a.island_group && a.island_group === b.island_group) d -= 0.4;

  // Geographic proximity — gentle factor, capped low so it never dominates archetype
  if (a.lat && a.lng && b.lat && b.lng) {
    const dLat = (a.lat - b.lat) * 111;
    const dLng = (a.lng - b.lng) * 111 * Math.cos((a.lat + b.lat) / 2 * Math.PI / 180);
    const km = Math.sqrt(dLat * dLat + dLng * dLng);
    d += Math.min(km / 500, 0.6);   // saturates at 0.6 — purely a tie-breaker
  }

  return d;
}

function findSimilarIslands(key, count = 4) {
  const target = ISLANDS_DATA[key];
  if (!target) return [];
  const targetArc = islandArchetypes(target);
  const scored = Object.keys(ISLANDS_DATA)
    .filter(k => k !== key)
    .map(k => ({ key: k, dist: similarIslandDistance(target, ISLANDS_DATA[k], targetArc) }));
  scored.sort((a, b) => a.dist - b.dist);
  return scored.slice(0, count).map(s => s.key);
}

// Build a short reason tagline highlighting why this island matches
function similarReasonTags(srcKey, dstKey) {
  const a = ISLANDS_DATA[srcKey], b = ISLANDS_DATA[dstKey];
  if (!a || !b) return '';
  const lang = (typeof CURRENT_LANG !== 'undefined' && CURRENT_LANG === 'el') ? 'el' : 'en';
  const tags = [];

  // Lead with the strongest shared archetype — this is what's actually
  // driving the match in the new algorithm. Threshold of 0.45 means
  // "both score meaningfully on this dimension".
  const arcA = islandArchetypes(a);
  const arcB = islandArchetypes(b);
  const archetypeLabels = {
    remote:   { en: 'remote outpost',     el: 'απομακρυσμένο' },
    tiny:     { en: 'tiny escape',        el: 'μικρό καταφύγιο' },
    party:    { en: 'lively scene',       el: 'ζωντανή σκηνή' },
    working:  { en: 'lived-in island',    el: 'πραγματικό νησί' },
    postcard: { en: 'postcard beauty',    el: 'ομορφιά καρτ-ποστάλ' },
    active:   { en: 'hiking & nature',    el: 'πεζοπορία & φύση' },
    historic: { en: 'rich history',       el: 'πλούσια ιστορία' },
  };
  // Sort archetypes by combined strength (min of the two scores → "shared min")
  const sharedStrength = Object.keys(arcA).map(k => ({
    key: k,
    strength: Math.min(arcA[k], arcB[k])
  })).sort((x, y) => y.strength - x.strength);

  sharedStrength.forEach(s => {
    if (s.strength >= 0.45 && tags.length < 2) {
      tags.push(archetypeLabels[s.key][lang]);
    }
  });

  // Add ferry region if shared — useful logistical info
  if (a.island_group && a.island_group === b.island_group && tags.length < 3) {
    tags.push(t(`group.${a.island_group.toLowerCase().replace(/\s+/g,'')}`) || a.island_group);
  }

  // Shared character flags as additional flavour (only if rare-vibe match)
  const charLabels = {
    drama:   { en: 'dramatic',  el: 'δραματικό' },
    hiking:  { en: 'hiking',    el: 'πεζοπορία' },
    chora:   { en: 'chora',     el: 'χώρα' },
    sailing: { en: 'sailing',   el: 'ιστιοπλοΐα' },
    springs: { en: 'springs',   el: 'ιαματικά' },
  };
  Object.keys(charLabels).forEach(f => {
    if (a[f] && b[f] && tags.length < 3) {
      const label = charLabels[f][lang];
      if (!tags.includes(label)) tags.push(label);
    }
  });

  // Last-resort fallback — "similar size" if nothing else fits
  if (tags.length === 0) {
    const aArea = a.area || 50, bArea = b.area || 50;
    const ratio = Math.max(aArea, bArea) / Math.max(Math.min(aArea, bArea), 1);
    if (ratio < 2.5) {
      const bracket = aArea < 30 ? (lang === 'el' ? 'μικρό νησί' : 'small island')
                    : aArea < 200 ? (lang === 'el' ? 'μεσαίο νησί' : 'mid-sized island')
                    : (lang === 'el' ? 'μεγάλο νησί' : 'large island');
      tags.push(bracket);
    }
  }

  return tags.slice(0, 3).join(' · ');
}

function buildSimilarIslandsSection(key) {
  if (!key || !ISLANDS_DATA[key]) return '';
  const matches = findSimilarIslands(key, 4);
  if (!matches.length) return '';
  const cards = matches.map(matchKey => {
    const m = ISLANDS_DATA[matchKey];
    const reason = similarReasonTags(key, matchKey);
    const score = (m.total || 0).toFixed(1);
    return `<a class="similar-card" href="#" onclick="navigateTo('island','${matchKey}');return false;">
      <div class="similar-card-name">${islandName(matchKey)}</div>
      <div class="similar-card-score">${scoreHtml(score)}</div>
      <div class="similar-card-reason">${reason}</div>
    </a>`;
  }).join('');
  return `<section class="similar-section">
    <h3 class="similar-title">${t('similar.title')}</h3>
    <p class="similar-intro">${t('similar.intro')}</p>
    <div class="similar-grid">${cards}</div>
  </section>`;
}

function buildLocalSection(data) {
  const specs = data.specialties || [];
  const crafts = data.crafts || [];
  const fests = data.festivals || [];
  if (!specs.length && !crafts.length && !fests.length) return '';

  const renderItem = (item) => {
    const name = pickLang(item, 'name') || '';
    const desc = pickLang(item, 'desc') || '';
    const when = pickLang(item, 'when') || '';
    const whenHtml = when ? `<span class="local-when">${when}</span>` : '';
    // Two possible image fields:
    //   item.photo = large landscape (Wikimedia) — renders as banner with credit
    //   item.image = small 80px square thumb (legacy)
    const photo = item.photo || '';
    const image = item.image || '';
    let imageHtml = '';
    let wrapClass = 'local-item';
    if (photo) {
      imageHtml = `<div class="local-item-photo-wrap">${buildLightboxImg(photo, name, item.photo_credit, 'local-item-photo', 'onerror="this.parentElement.parentElement.style.display=\'none\'"')}${buildPhotoCredit(item.photo_credit)}</div>`;
      wrapClass = 'local-item local-item-with-photo';
    } else if (image) {
      imageHtml = `<img class="local-item-image" src="${image}" alt="${name.replace(/"/g, '&quot;')}" loading="lazy" width="80" height="80">`;
      wrapClass = 'local-item local-item-with-image';
    }
    return `
      <div class="${wrapClass}">
        ${imageHtml}
        <div class="local-item-text">
          <div class="local-item-name">${name}${whenHtml}</div>
          ${desc ? `<div class="local-item-desc">${desc}</div>` : ''}
        </div>
      </div>`;
  };

  const block = (title, items, icon) => items.length ? `
    <div class="local-block">
      <h4 class="local-heading"><span class="local-icon">${icon}</span>${title}</h4>
      <div class="local-items">${items.map(renderItem).join('')}</div>
    </div>` : '';

  return `
    <div class="local-section">
      <h3 class="local-section-title">${t('local.section_title')}</h3>
      ${block(t('local.specialties'), specs, '🍽')}
      ${block(t('local.crafts'), crafts, '🧵')}
      ${block(t('local.festivals'), fests, '🎉')}
    </div>`;
}

/* ============================================================
   BEACH PHOTOS — Cloudinary URLs only (fast, no API calls)
============================================================ */
// Legacy commons field support: if a beach has 'commons' but no 'photo',
// hide the placeholder since we no longer fetch from Wikimedia.
async function loadBeachPhotos(beaches) {
  for (let i = 0; i < beaches.length; i++) {
    const b = beaches[i];
    if (b.photo) continue;
    const wrap = document.getElementById(`beach-photo-${i}-wrap`);
    if (wrap) wrap.style.display = 'none';
  }
}

/* ============================================================
   DAY FILTER
============================================================ */
function filterItinDay(day) {
  itinActiveDay = day;
  document.querySelectorAll('.itin-day-btn').forEach(btn => {
    const isActive = String(btn.dataset.day) === String(day);
    btn.classList.toggle('active', isActive);
    // Active state is handled by CSS (.itin-day-btn.active) — no inline override
    btn.style.background = '';
  });
  document.querySelectorAll('.itin-day-card').forEach(card => {
    card.style.display = (day === 'all' || card.id === `itin-day-card-${day}`) ? '' : 'none';
  });
  Object.entries(itinRouteLayers).forEach(([d, layers]) => {
    layers.forEach(l => {
      if (day === 'all' || String(d) === String(day)) l.addTo(itineraryMapInstance);
      else itineraryMapInstance.removeLayer(l);
    });
  });
  Object.entries(itinMarkerLayers).forEach(([d, markers]) => {
    markers.forEach(m => {
      if (day === 'all' || String(d) === String(day)) m.addTo(itineraryMapInstance);
      else itineraryMapInstance.removeLayer(m);
    });
  });
  // Beach markers: only visible on "All days" view (they're island-wide POIs, not per-day)
  itinBeachMarkers.forEach(m => {
    if (day === 'all') m.addTo(itineraryMapInstance);
    else itineraryMapInstance.removeLayer(m);
  });
  if (!itineraryMapInstance) return;
  if (day === 'all') {
    const allKeys = Object.keys(itinRouteLayers);
    if (!allKeys.length) return;
    const allCoords = allKeys.flatMap(d =>
      (itinRouteLayers[d][0]?.getLatLngs() || []).flat()
    );
    if (allCoords.length) itineraryMapInstance.fitBounds(L.latLngBounds(allCoords), { padding: [30, 30] });
  } else {
    const layers = itinRouteLayers[day];
    if (layers && layers[0]) {
      const coords = layers[0].getLatLngs().flat();
      if (coords.length) itineraryMapInstance.fitBounds(L.latLngBounds(coords), { padding: [50, 50] });
    }
  }
}

/* ============================================================
   POI ICONS
============================================================ */
// Full canonical taxonomy of stop types (matches data/migration spec)
const POI_EMOJIS = {
  beach:      '🏖️',
  village:    '🏘',
  harbour:    '⚓',
  city:       '🏙',
  museum:     '🏛️',
  restaurant: '🍽',
  nature:     '🌿',
  castle:     '🏰',
  church:     '⛪',
  viewpoint:  '🔭',
  ruin:       '🏛',
  departure:  '🚢',
  monastery:  '☧',
  arrival:    '🚢',
  spa:        '♨️',
  winery:     '🍷',
  distillery: '🥃',
  waterfall:  '💧',
  airport:    '✈️',
  port:       '⛴️',
};

// Zoom threshold below which markers render as small colored dots (cleaner overview),
// at-or-above renders as full emoji badges.
const POI_EMOJI_ZOOM = 11;

function poiIcon(type, color, mode, dayNum) {
  // mode: 'emoji' | 'dot'  (default 'emoji' for back-compat)
  // dayNum: optional integer (1-N). Renders a small numbered badge at the
  // top-right of the emoji marker so users can see day sequence at a glance.
  // Omitted in dot mode (markers are too small for a readable number).
  if (mode === 'dot') {
    return `<div style="width:10px;height:10px;border-radius:50%;background:${color};border:2px solid white;box-shadow:0 1px 3px rgba(0,0,0,.4)"></div>`;
  }
  const emoji = POI_EMOJIS[type] || '📍';
  // Day-number badge: small white-bordered pill in the day's color at top-right.
  // Positioned absolutely inside the 32×32 marker; uses pointer-events:none so it
  // doesn't intercept clicks meant for the marker itself.
  const badge = (typeof dayNum === 'number' && dayNum > 0)
    ? `<span style="position:absolute;top:-3px;right:-3px;background:${color};color:#fff;font:800 12px/1 system-ui,-apple-system,sans-serif;width:20px;height:20px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:2px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,.4);pointer-events:none;text-shadow:0 1px 1px rgba(0,0,0,.35);z-index:2;">${dayNum}</span>`
    : '';
  return `<div style="position:relative;font-size:22px;line-height:1;filter:drop-shadow(0 1px 3px rgba(0,0,0,.5));text-align:center;width:32px;height:32px;display:flex;align-items:center;justify-content:center;background:white;border-radius:50%;border:2px solid ${color};box-shadow:0 2px 6px rgba(0,0,0,.25);">${emoji}${badge}</div>`;
}

// Build a divIcon for a stop at the given mode (kept as one helper so the
// marker creation site and the zoom-handler stay in sync on size/anchor).
function poiDivIcon(type, color, mode, dayNum) {
  const isDot = mode === 'dot';
  return L.divIcon({
    className: 'custom-marker',
    html: poiIcon(type, color, mode, dayNum),
    iconSize:   isDot ? [14, 14] : [32, 32],
    iconAnchor: isDot ? [7, 7]   : [16, 16],
  });
}

/* ============================================================
   OSRM ROAD ROUTING
============================================================ */
async function fetchOSRMRoute(coords) {
  const coordStr = coords.map(c => `${c[1]},${c[0]}`).join(';');
  const url = `https://router.project-osrm.org/route/v1/driving/${coordStr}?overview=full&geometries=geojson`;
  try {
    const res = await fetch(url);
    const data = await res.json();
    if (data.routes && data.routes[0]) {
      return data.routes[0].geometry.coordinates.map(c => [c[1], c[0]]);
    }
  } catch(e) { console.warn('OSRM fallback', e); }
  return coords;
}

/* ============================================================
   ITINERARY MAP INIT — accepts days array from JSON
============================================================ */
// Douglas–Peucker simplification for a [lat,lng] path. The OSRM route has very
// dense vertices; when we offset the line (to separate overlapping days) those
// tiny wiggles make the offset line overshoot and look crooked/lumpy. Thinning
// the path first keeps the road shape but gives clean parallel offsets.
function _perpDistDeg(p, a, b) {
  const x = p[1], y = p[0], x1 = a[1], y1 = a[0], x2 = b[1], y2 = b[0];
  const dx = x2 - x1, dy = y2 - y1;
  if (dx === 0 && dy === 0) return Math.hypot(x - x1, y - y1);
  let t = ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy);
  t = Math.max(0, Math.min(1, t));
  return Math.hypot(x - (x1 + t * dx), y - (y1 + t * dy));
}
function simplifyPath(pts, eps) {
  if (!pts || pts.length < 3) return pts || [];
  let dmax = 0, idx = 0;
  for (let i = 1; i < pts.length - 1; i++) {
    const d = _perpDistDeg(pts[i], pts[0], pts[pts.length - 1]);
    if (d > dmax) { dmax = d; idx = i; }
  }
  if (dmax > eps) {
    const left = simplifyPath(pts.slice(0, idx + 1), eps);
    const right = simplifyPath(pts.slice(idx), eps);
    return left.slice(0, -1).concat(right);
  }
  return [pts[0], pts[pts.length - 1]];
}

async function initItineraryMap(days, beaches = []) {
  const mapEl = document.getElementById('itin-map');
  if (!mapEl) return;
  if (itineraryMapInstance) { itineraryMapInstance.remove(); itineraryMapInstance = null; }
  itinRouteLayers = {};
  itinMarkerLayers = {};

  itineraryMapInstance = L.map(mapEl, { zoomControl: true, attributionControl: true });
  addThemeAwareTiles(itineraryMapInstance, { maxZoom: 16 });
  L.control.scale({ imperial: false, position: 'bottomleft' }).addTo(itineraryMapInstance);

  const stopCoords = days.flatMap(d => d.stops.map(s => [s.lat, s.lng]));
  const beachCoords = beaches.filter(b => b.lat && b.lng).map(b => [b.lat, b.lng]);
  const allCoords = [...stopCoords, ...beachCoords];
  if (allCoords.length) itineraryMapInstance.fitBounds(L.latLngBounds(allCoords), { padding: [30, 30] });

  for (const day of days) {
    itinRouteLayers[day.day] = [];
    itinMarkerLayers[day.day] = [];

    const coords = day.stops.map(s => [s.lat, s.lng]);
    const rawRoute = await fetchOSRMRoute(coords);
    // Thin the dense OSRM path (~40m tolerance) before drawing so the offset
    // lines stay smooth instead of lumpy at every little road wiggle.
    const routeCoords = simplifyPath(rawRoute, 0.0004);

    // Lines stay exactly on the road. Overlapping days are distinguished by a
    // staggered dash pattern applied in restyleItinRoutes() (zoom-responsive),
    // so no geometry is moved off the road (which previously caused curls).
    const polyline = L.polyline(routeCoords, {
      color: day.color, weight: 5, opacity: 0.9, lineJoin: 'round'
    }).addTo(itineraryMapInstance);
    itinRouteLayers[day.day].push(polyline);

    day.stops.forEach((stop, i) => {
      // Itinerary popups: pull EL fields when on /el/, fall back to EN if a
      // particular field hasn't been translated for this island yet.
      const isEl = (typeof CURRENT_LANG !== 'undefined' && CURRENT_LANG === 'el');
      const stopName = (isEl && stop.name_el) ? stop.name_el : stop.name;
      const stopDesc = (isEl && stop.desc_el) ? stop.desc_el : stop.desc;
      const nameHtml = stop.wiki
        ? `<a href="${stop.wiki}" target="_blank" rel="noopener" style="color:${day.color};font-weight:700">${stopName}</a>`
        : `<strong>${stopName}</strong>`;
      // Stop-type labels (beach / village / castle / …) translated for popup headers
      const TYPE_LABELS_EL = {
        beach:'Παραλία', village:'Χωριό', harbour:'Λιμάνι', city:'Πόλη',
        restaurant:'Εστιατόριο', museum:'Μουσείο', nature:'Φύση',
        castle:'Κάστρο', church:'Εκκλησία', viewpoint:'Θέα', ruin:'Ερείπια',
        departure:'Αναχώρηση', monastery:'Μοναστήρι', spa:'Ιαματικά',
        arrival:'Άφιξη', winery:'Οινοποιείο', distillery:'Αποστακτήριο',
        waterfall:'Καταρράκτης', airport:'Αεροδρόμιο', port:'Λιμάνι'
      };
      const typeLabel = isEl
        ? (TYPE_LABELS_EL[stop.type] || 'Στάση')
        : (stop.type ? stop.type.charAt(0).toUpperCase() + stop.type.slice(1) : 'Stop');
      const photoLine = stop.photo
        ? `<div style="position:relative;margin-top:8px">${buildLightboxImg(stop.photo, stopName, stop.photo_credit, '', 'style="width:100%;height:120px;object-fit:cover;border-radius:6px;display:block" onerror="this.parentElement.style.display=\'none\'"')}${buildPhotoCredit(stop.photo_credit)}</div>`
        : '';
      const stopType = stop.type || 'village';
      // Icon-only type: arrival/departure describe a day-role, not a place, so
      // resolve their marker to ✈️ vs ⛴️ by the stop name (most island arrivals
      // and departures are by ferry — only real airports get the plane). The
      // popup label still uses stop.type ("Arrival"/"Departure").
      let iconType = stopType;
      if (iconType === 'arrival' || iconType === 'departure') {
        iconType = /airport|αεροδρ|flight/i.test(stop.name || '') ? 'airport' : 'port';
      }
      const initialMode = itineraryMapInstance.getZoom() >= POI_EMOJI_ZOOM ? 'emoji' : 'dot';
      // Badge shows the stop's sequence within its day (1..N), not the day number,
      // so a 5-stop day reads 1·2·3·4·5 in walking order.
      const stopNum = i + 1;
      // Popup-header words ("Day"/"Stop") also switch language
      const dayWord = isEl ? 'Ημέρα' : 'Day';
      const stopWord = isEl ? 'Στάση' : 'Stop';
      const marker = L.marker([stop.lat, stop.lng], { icon: poiDivIcon(iconType, day.color, initialMode, stopNum) })
        .addTo(itineraryMapInstance)
        .bindPopup(`<div style="min-width:200px;font-family:sans-serif"><div style="font-size:10px;font-weight:700;color:${day.color};text-transform:uppercase;letter-spacing:.6px;margin-bottom:5px">${dayWord} ${day.day} · ${stopWord} ${stopNum} · ${typeLabel}</div>${nameHtml}<p style="font-size:12px;color:#555;margin:6px 0 0;line-height:1.55">${stopDesc}</p>${photoLine}</div>`);
      // Stash the metadata on the marker so the zoom handler can re-render the icon
      marker._poiType = iconType;
      marker._poiColor = day.color;
      marker._poiDay = stopNum;
      // Bind direct click handler on lightbox images inside this popup once it opens.
      // Document-level delegation can be intercepted by Leaflet's internal handlers,
      // so direct binding is the most reliable path inside popup content.
      marker.on('popupopen', function(ev) {
        const popupNode = ev.popup.getElement();
        if (!popupNode) return;
        popupNode.querySelectorAll('img.lightbox-img').forEach(function(img) {
          if (img.dataset.lightboxBound) return;
          img.dataset.lightboxBound = '1';
          img.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            if (window.openLightbox) window.openLightbox(img);
          });
        });
      });
      itinMarkerLayers[day.day].push(marker);
    });
  }

  // Beach markers: separate always-visible layer (doesn't belong to any day)
  // Shown when "All days" is active; hidden when a specific day is selected.
  itinBeachMarkers = [];
  const BEACH_COLOR = '#0B8FAC';
  const initialBeachMode = itineraryMapInstance.getZoom() >= POI_EMOJI_ZOOM ? 'emoji' : 'dot';
  beaches.forEach(b => {
    if (!b.lat || !b.lng) return;
    const name = pickLang(b, 'name');
    const desc = pickLang(b, 'desc');
    const type = pickLang(b, 'type');
    const popupHtml = `<div style="min-width:200px;font-family:sans-serif">
      <div style="font-size:10px;font-weight:700;color:${BEACH_COLOR};text-transform:uppercase;letter-spacing:.6px;margin-bottom:5px">${t('detail.beach')}</div>
      <strong>${name}</strong>
      ${type ? `<div style="font-size:11px;color:#777;margin-top:2px">${type}</div>` : ''}
      <p style="font-size:12px;color:#555;margin:6px 0 0;line-height:1.55">${desc}</p>
    </div>`;
    const marker = L.marker([b.lat, b.lng], { icon: poiDivIcon('beach', BEACH_COLOR, initialBeachMode), zIndexOffset: -100 })
      .addTo(itineraryMapInstance)
      .bindPopup(popupHtml);
    marker._poiType = 'beach';
    marker._poiColor = BEACH_COLOR;
    itinBeachMarkers.push(marker);
  });

  // Zoom-based icon mode: render dots when zoomed out (less clutter), emojis when zoomed in.
  // Route lines use a fixed pixel weight, so on zoom-out the island shrinks but
  // the lines don't — they read as thick bands (worse with the parallel offsets).
  // Scale both weight and the per-day offset with zoom so lines stay proportional:
  // thin + tightly bundled when zoomed out, thicker + more separated when zoomed in.
  function restyleItinRoutes() {
    const z = itineraryMapInstance.getZoom();
    const weight = Math.max(2, Math.min(5, (z - 6) * 0.65));
    const N = Math.max(1, days.length);
    // Distinguish overlapping days WITHOUT moving the line off the road. Earlier
    // we offset each line perpendicular, but that curls/loops at switchbacks and
    // out-and-back legs. Instead, draw each day dashed at ~50% duty and stagger
    // the phase per day: on a shared road the colors interleave, and a solo road
    // still reads as a clean dashed line. Lines stay exactly on the road.
    const cycle = Math.max(14, weight * 4);
    const dash = `${(cycle / 2).toFixed(1)}, ${(cycle / 2).toFixed(1)}`;
    days.forEach((d, idx) => {
      const dashOffset = ((cycle / N) * idx).toFixed(1);
      (itinRouteLayers[d.day] || []).forEach(pl => {
        pl.setStyle({ weight, dashArray: dash, dashOffset, lineCap: 'butt' });
      });
    });
  }
  restyleItinRoutes();

  // Only re-render icons when crossing the threshold to avoid thrash on small zoom changes.
  let _lastPoiMode = itineraryMapInstance.getZoom() >= POI_EMOJI_ZOOM ? 'emoji' : 'dot';
  itineraryMapInstance.on('zoomend', () => {
    restyleItinRoutes();
    const mode = itineraryMapInstance.getZoom() >= POI_EMOJI_ZOOM ? 'emoji' : 'dot';
    if (mode === _lastPoiMode) return;
    _lastPoiMode = mode;
    Object.values(itinMarkerLayers).forEach(arr => {
      arr.forEach(m => {
        if (m._poiType) m.setIcon(poiDivIcon(m._poiType, m._poiColor, mode, m._poiDay));
      });
    });
    itinBeachMarkers.forEach(m => {
      // Beaches have no _poiDay (no badge needed) — passing undefined is fine.
      if (m._poiType) m.setIcon(poiDivIcon(m._poiType, m._poiColor, mode, m._poiDay));
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
  // Restore prior preference for dimension visibility
  if (localStorage.getItem('tableShowDims') === 'true') {
    document.getElementById('islands-table')?.classList.add('show-dims');
    const btn = document.getElementById('toggle-dims-btn');
    if (btn) btn.textContent = t('data.hidedims');
  }
  renderTable();
}

function toggleDimensions() {
  const table = document.getElementById('islands-table');
  if (!table) return;
  const isShowing = table.classList.toggle('show-dims');
  const btn = document.getElementById('toggle-dims-btn');
  if (btn) btn.textContent = isShowing ? t('data.hidedims') : t('data.showdims');
  localStorage.setItem('tableShowDims', isShowing);
}
window.toggleDimensions = toggleDimensions;


/* ============================================================
   SHORTLIST — save favourite islands to localStorage
============================================================ */
function getShortlist() {
  try { return JSON.parse(localStorage.getItem('islandShortlist') || '[]'); }
  catch { return []; }
}

function saveShortlist(list) {
  localStorage.setItem('islandShortlist', JSON.stringify(list));
  updateShortlistCount();
}

function isInShortlist(key) {
  return getShortlist().includes(key);
}

function toggleShortlist() {
  if (!currentIslandKey) return;
  const list = getShortlist();
  const idx = list.indexOf(currentIslandKey);
  if (idx >= 0) {
    list.splice(idx, 1);
  } else {
    list.push(currentIslandKey);
  }
  saveShortlist(list);
  updateShortlistButton();
}

function updateShortlistButton() {
  const btn = document.getElementById('detail-shortlist-btn');
  if (!btn || !currentIslandKey) return;
  const saved = isInShortlist(currentIslandKey);
  btn.textContent = saved ? t('detail.saved') : t('detail.save');
  btn.classList.toggle('saved', saved);
}

function updateShortlistCount() {
  const count = getShortlist().length;
  const badge = document.getElementById('shortlist-count');
  if (badge) {
    badge.textContent = count > 0 ? `(${count})` : '';
  }
}

function renderShortlist() {
  const container = document.getElementById('shortlist-container');
  if (!container) return;
  const list = getShortlist();
  
  if (list.length === 0) {
    container.innerHTML = `
      <div class="shortlist-empty">
        <p style="font-size:48px;margin:0 0 16px">☆</p>
        <p><strong>${t('shortlist.empty')}</strong></p>
        <p>${t('shortlist.howto')}</p>
      </div>
    `;
    return;
  }
  
  const cards = list.map(key => {
    const island = ISLANDS_DATA[key];
    if (!island) return '';
    return `
      <div class="shortlist-card" onclick="navigateTo('island','${key}')">
        <div class="shortlist-card-body">
          <h3>${islandName(key)}</h3>
          <div class="shortlist-meta">
            <span class="group-tag">${groupName(island.island_group)}</span>
            <span>${island.days ? island.days + ' ' + t('common.days') : ''}</span>
          </div>
          <div class="shortlist-rating">${starsHtml(island.total)}</div>
          <div class="shortlist-dims">
            ${t('shortlist.dim.beach')} ${fmt(island.beach)} · ${t('shortlist.dim.culture')} ${fmt(island.hist)} · ${t('shortlist.dim.night')} ${fmt(island.night)}
          </div>
          <button class="shortlist-remove" onclick="event.stopPropagation();removeFromShortlist('${key}')">${t('shortlist.remove')}</button>
        </div>
      </div>
    `;
  }).join('');
  
  container.innerHTML = `
    <div class="shortlist-grid">${cards}</div>
    <div style="text-align:center;margin-top:24px">
      <button class="shortlist-clear" onclick="clearShortlist()">${t('shortlist.clearall')}</button>
    </div>
  `;
}

function removeFromShortlist(key) {
  const list = getShortlist().filter(k => k !== key);
  saveShortlist(list);
  renderShortlist();
}

function clearShortlist() {
  if (confirm('Remove all saved islands?')) {
    saveShortlist([]);
    renderShortlist();
  }
}

// Expose for inline onclick
window.toggleShortlist = toggleShortlist;
window.removeFromShortlist = removeFromShortlist;
window.clearShortlist = clearShortlist;
window.navigateTo = navigateTo;


/* ============================================================
   BEACH COMMUNITY VOTING — stored in localStorage
============================================================ */
function starsHtml(score) {
  // Legacy name (still called from many places). Now renders a colored number
  // badge instead of star icons. The number is more honest about precision —
  // your data has 0.1 resolution and stars rounded to 0.5 was throwing it away.
  return scoreHtml(score);
}

function scoreHtml(score) {
  // Compact colored badge showing the actual numeric score with 1-decimal precision.
  // Color comes from scoreToColor() — same 4-bucket scale used in tooltips, map markers,
  // and elsewhere, so the visual language is consistent across the site.
  if (score == null || isNaN(score)) return '<span class="score-pill score-empty">—</span>';
  const color = scoreToColor(score);
  return `<span class="score-pill" style="background:${color}" title="${fmt(score)} / 5">${fmt(score)}</span>`;
}

const MAX_AREA = 2641; // Crete (Heraklion prefecture) — largest single entry
const MAX_POP = 664000; // removed Athens but keep scale reasonable — use 200000

function carNeedCompactHtml(score) {
  // Used inside the data table — keep the number visible (users sort by it)
  // but always pair it with the text label so direction is unambiguous.
  if (score == null || isNaN(score)) return '<span style="color:var(--ink-4)">—</span>';
  const n = Math.round(score);
  const keys = ['', 'car.none', 'car.helpful', 'car.useful', 'car.recommended', 'car.essential'];
  const label = (typeof t === 'function' && keys[n]) ? t(keys[n]) : '';
  const colors = ['', '#6B7280', '#8B8B8B', '#A58A3A', '#D17A2B', '#C0522A'];
  const col = colors[n] || '#888';
  return `<span class="car-compact-pill" style="background:${col}20;color:${col};border:1px solid ${col}40">${n} · ${label}</span>`;
}

function carNeedHtml(score) {
  // Used in island detail rating sidebar. Per UX feedback (the bare "1"
  // reads as "bad" since other dims are higher-is-better), this version
  // shows ONLY the text label, no visible number. The numeric score lives
  // in the title attribute for accessibility / power users.
  if (score == null || isNaN(score)) return '<span style="color:var(--ink-4)">—</span>';
  const n = Math.round(score);
  const keys = ['', 'car.none', 'car.helpful', 'car.useful', 'car.recommended', 'car.essential'];
  const label = (typeof t === 'function' && keys[n]) ? t(keys[n]) : '';
  const colors = ['', '#6B7280', '#8B8B8B', '#A58A3A', '#D17A2B', '#C0522A'];
  const col = colors[n] || '#888';
  const scaleHint = (typeof t === 'function') ? t('dim.car.hint') : '';
  const style = `background:${col}20;color:${col};border:1px solid ${col}40`;
  const inner = `<span class="car-need-icon">🚗</span><span class="car-need-label">${label}</span>`;
  // Where a car is actually useful (score > 1), make the pill a link to the
  // car-rental affiliate. Car-free islands (n <= 1) stay a plain pill — renting
  // there makes no sense (matches the hidden Rent-a-car button).
  if (n > 1) {
    const rentHint = (typeof t === 'function') ? t('detail.rentcar') : 'Rent a car';
    return `<a class="car-need-pill car-need-link" href="https://www.discovercars.com/?a_aid=antaran2" target="_blank" rel="noopener sponsored" style="${style};text-decoration:none;cursor:pointer" title="${rentHint} · ${scaleHint} (${n}/5)">${inner}<span class="car-need-go" aria-hidden="true">↗</span></a>`;
  }
  return `<span class="car-need-pill" style="${style}" title="${scaleHint} (${n}/5)">${inner}</span>`;
}

function barHtml(val, max, color) {
  const pct = Math.min(100, Math.round((val / max) * 100));
  return `<div class="table-bar-wrap"><div class="table-bar-fill" style="width:${pct}%;background:${color}"></div><span class="table-bar-label">${fmtNum(val)}</span></div>`;
}

function barStackedHtml(val, max, color) {
  const pct = Math.min(100, Math.round((val / max) * 100));
  return `<div class="table-bar-stacked"><span class="table-bar-stacked-num">${fmtNum(val)}</span><div class="table-bar-stacked-track"><div class="table-bar-stacked-fill" style="width:${pct}%;background:${color}"></div></div></div>`;
}

function renderTable() {
  const query = (document.getElementById('tableSearchInput')?.value || '').toLowerCase();
  let list = ISLANDS.filter(i => {
    if (!query) return true;
    const enName = i.name.toLowerCase();
    const elName = (typeof ISLAND_NAMES_EL !== 'undefined' && ISLAND_NAMES_EL[i.key]) ? ISLAND_NAMES_EL[i.key].toLowerCase() : '';
    return enName.includes(query) || elName.includes(query) || i.island_group.toLowerCase().includes(query);
  });
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
  tbody.innerHTML = list.map(i => `<tr data-key="${i.key}" class="table-row-clickable"><td data-label="Island" style="font-weight:600">${islandName(i.key)}</td><td data-label="Group" class="td-main"><span class="group-tag">${groupName(i.island_group)}</span></td><td data-label="Rating" class="td-main">${starsHtml(i.total)}</td><td data-label="Beach" class="td-dim">${starsHtml(i.beach)}</td><td data-label="Culture" class="td-dim">${starsHtml(i.hist)}</td><td data-label="Night" class="td-dim">${starsHtml(i.night)}</td><td data-label="Access" class="td-dim">${starsHtml(i.access)}</td><td data-label="Affordability" class="td-dim">${starsHtml(i.afford)}</td><td data-label="Car" class="td-dim td-car" title="${t('dim.car.hint')}">${carNeedCompactHtml(i.car_need)}</td><td data-label="Days" class="td-main" style="font-weight:600;color:var(--aegean)">${i.days ? i.days + ' ' + t('common.days') : '—'}</td><td data-label="Airport" class="td-main td-airport">${i.has_airport ? '<span class="airport-yes" title="Commercial airport">✈</span>' : '<span class="airport-no">—</span>'}</td><td data-label="Area (km²)" class="td-main">${barStackedHtml(i.area, 3684, 'var(--aegean)')}</td><td data-label="Population" class="td-main">${barStackedHtml(i.pop, 200000, 'var(--olive)')}</td></tr>`).join('');
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
  if (!selA || !selB) return;
  const sorted = [...ISLANDS].sort((a, b) => a.name.localeCompare(b.name));
  sorted.forEach(i => {
    [selA, selB].forEach(sel => {
      const opt = document.createElement('option');
      opt.value = i.key; opt.textContent = islandName(i.key); sel.appendChild(opt);
    });
  });
  // Apply current compareSelection (defaults: mykonos + santorini) to the dropdowns
  if (compareSelection[0]) selA.value = compareSelection[0];
  if (compareSelection[1]) selB.value = compareSelection[1];
  selA.addEventListener('change', () => { compareSelection[0] = selA.value || null; renderCompareView(); });
  selB.addEventListener('change', () => { compareSelection[1] = selB.value || null; renderCompareView(); });
  // Initial render so the chart appears immediately on page load
  renderCompareView();
}

function addToCompare(key) {
  if (compareSelection.includes(key)) return;
  // Always set the clicked island as slot A, and ensure slot B has a default
  // for an immediate chart. If user clicked Rhodes, default the other slot to Chania.
  compareSelection[0] = key;
  if (!compareSelection[1] || compareSelection[1] === key) {
    compareSelection[1] = (key === 'rhodes') ? 'chania' : 'rhodes';
  }
  const selA = document.getElementById('compare-select-a');
  const selB = document.getElementById('compare-select-b');
  if (selA && compareSelection[0]) selA.value = compareSelection[0];
  if (selB && compareSelection[1]) selB.value = compareSelection[1];
}

// Cached vs_verdicts.json + vs_faqs.json data — lazily loaded the first
// time the Compare view is opened. Both share the same key format
// 'a__b' (alphabetical pair). Verdicts contain editorial HTML;
// FAQs contain {q, a} arrays per language and become an accordion below
// the verdict prose.
let VS_VERDICTS_CACHE = null;
let VS_FAQS_CACHE = null;
async function loadVsVerdicts() {
  if (VS_VERDICTS_CACHE) return VS_VERDICTS_CACHE;
  try {
    const res = await fetch('/vs_verdicts.json');
    if (res.ok) {
      VS_VERDICTS_CACHE = await res.json();
      return VS_VERDICTS_CACHE;
    }
  } catch(e) { /* file not deployed yet — fail silently */ }
  VS_VERDICTS_CACHE = {};  // empty so we don't retry
  return VS_VERDICTS_CACHE;
}
async function loadVsFaqs() {
  if (VS_FAQS_CACHE) return VS_FAQS_CACHE;
  try {
    const res = await fetch('/vs_faqs.json');
    if (res.ok) {
      VS_FAQS_CACHE = await res.json();
      return VS_FAQS_CACHE;
    }
  } catch(e) { /* file optional — fail silently */ }
  VS_FAQS_CACHE = {};
  return VS_FAQS_CACHE;
}

// Render the editorial verdict block (if one exists for this pair).
// Called by renderCompareView after the cards have rendered. Also pulls the
// matching FAQ accordion from vs_faqs.json when available, since the FAQ
// is part of the same "verdict + supporting Q&A" section for SEO purposes.
async function renderCompareVerdict(iA, iB) {
  const el = document.getElementById('compare-verdict');
  if (!el) return;
  const [verdicts, faqsAll] = await Promise.all([loadVsVerdicts(), loadVsFaqs()]);
  const sortedPair = [iA.key, iB.key].sort();
  const pairKey = sortedPair[0] + '__' + sortedPair[1];
  const entry = verdicts[pairKey];
  const lang = (typeof CURRENT_LANG !== 'undefined' && CURRENT_LANG === 'el') ? 'el' : 'en';
  const html = entry ? (entry[lang] || entry['en'] || '') : '';
  const faqList = (faqsAll[pairKey] && faqsAll[pairKey][lang]) ? faqsAll[pairKey][lang] : [];
  // Nothing curated → hide the section entirely.
  if (!html && !faqList.length) {
    el.style.display = 'none';
    el.innerHTML = '';
    return;
  }
  const escHtml = (s) => String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const heading = lang === 'el' ? 'Η ετυμηγορία μας' : 'Our verdict';
  let faqHtml = '';
  if (faqList.length) {
    const faqHeading = lang === 'el' ? 'Συχνές ερωτήσεις' : 'Common questions';
    const items = faqList.map(item =>
      `<details><summary>${escHtml(item.q)}</summary><p>${escHtml(item.a)}</p></details>`
    ).join('');
    faqHtml = `<div class="compare-faq"><h3 class="compare-faq-heading">${faqHeading}</h3>${items}</div>`;
  }
  el.innerHTML = `<h3 class="compare-verdict-heading">${heading}</h3>${html}${faqHtml}`;
  el.style.display = '';
}

async function renderCompareView() {
  const keyA = compareSelection[0];
  const keyB = compareSelection[1];
  const iA = keyA && ISLANDS_DATA[keyA] ? { key: keyA, ...ISLANDS_DATA[keyA] } : null;
  const iB = keyB && ISLANDS_DATA[keyB] ? { key: keyB, ...ISLANDS_DATA[keyB] } : null;
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
  renderCompareVerdict(iA, iB);  // editorial paragraph for curated pairs

  // Fetch full island JSONs for WTV + beach data (non-blocking — render static parts first)
  let jsonA = null, jsonB = null;
  try {
    const [resA, resB] = await Promise.all([
      fetch(`/islands/${keyA}.json`),
      fetch(`/islands/${keyB}.json`)
    ]);
    if (resA.ok) jsonA = await resA.json();
    if (resB.ok) jsonB = await resB.json();
  } catch(e) {}

  renderCompareWTV(iA, iB, jsonA, jsonB);
  renderCompareExtra(iA, iB, jsonA, jsonB);
}

function renderCompareWTV(iA, iB, jsonA, jsonB) {
  const el = document.getElementById('compare-wtv');
  if (!el) return;

  const tagsA = WTV_TAGS[iA.key] || [];
  const tagsB = WTV_TAGS[iB.key] || [];
  // Translated month names from i18n
  const monthNames = t('months.short').split(',');
  const tagClass = ['wtv-avoid','wtv-ok','wtv-great','wtv-perfect'];
  const tagLabels = [t('wtv.tag.avoid'), t('wtv.tag.ok'), t('wtv.tag.great'), t('wtv.tag.perfect')];
  const tagLabel = (v) => tagLabels[v] || '';
  const limitedLabel = t('wtv.limited');

  // Get why-text — use EL if in Greek, EN otherwise
  const wtvLangKey = CURRENT_LANG === 'el' ? 'why_el' : 'why';
  const whyA = jsonA && jsonA.when_to_visit && jsonA.when_to_visit.months
    ? jsonA.when_to_visit.months.map(m => m[wtvLangKey] || m.why || '') : [];
  const whyB = jsonB && jsonB.when_to_visit && jsonB.when_to_visit.months
    ? jsonB.when_to_visit.months.map(m => m[wtvLangKey] || m.why || '') : [];

  // Limited-service flags per month — comes from the same JSON we already fetched.
  // Matches the per-island page redesign where `limited:true` dims the cell visually.
  const limitedA = jsonA && jsonA.when_to_visit && jsonA.when_to_visit.months
    ? jsonA.when_to_visit.months.map(m => m.limited === true) : [];
  const limitedB = jsonB && jsonB.when_to_visit && jsonB.when_to_visit.months
    ? jsonB.when_to_visit.months.map(m => m.limited === true) : [];

  const months = monthNames.map((mo, i) => {
    const tA = tagsA[i] !== undefined ? tagsA[i] : 1;
    const tB = tagsB[i] !== undefined ? tagsB[i] : 1;
    const isSweet = tA >= 2 && tB >= 2;
    const isBest  = tA >= 3 && tB >= 3;
    const wA = whyA[i] || '';
    const wB = whyB[i] || '';
    const lA = limitedA[i] === true;
    const lB = limitedB[i] === true;
    // Include 'Limited service —' prefix in tooltip when applicable
    const aTip = `${islandName(iA.key)}: ${lA ? limitedLabel + ' — ' : ''}${tagLabel(tA)}${wA ? ' \u2014 ' + wA : ''}`;
    const bTip = `${islandName(iB.key)}: ${lB ? limitedLabel + ' — ' : ''}${tagLabel(tB)}${wB ? ' \u2014 ' + wB : ''}`;
    const tooltip = `${aTip} | ${bTip}`;
    const cellAClass = `cwtv-cell cwtv-a ${tagClass[tA]}${lA ? ' wtv-limited' : ''}`;
    const cellBClass = `cwtv-cell cwtv-b ${tagClass[tB]}${lB ? ' wtv-limited' : ''}`;
    return `<div class="cwtv-col${isSweet ? ' cwtv-sweet' : ''}${isBest ? ' cwtv-best' : ''}" title="${tooltip.replace(/"/g,"'")}">
      <div class="${cellAClass}"></div>
      <div class="cwtv-month">${mo}</div>
      <div class="${cellBClass}"></div>
    </div>`;
  }).join('');

  // Verdict with translated month names
  const sweetCount = tagsA.filter((tv,i) => tv >= 2 && tagsB[i] >= 2).length;
  const bestCount  = tagsA.filter((tv,i) => tv >= 3 && tagsB[i] >= 3).length;
  let overlapMsg = '';
  if (bestCount > 0) {
    const bestMonths = monthNames.filter((_,i) => tagsA[i] >= 3 && tagsB[i] >= 3).join(', ');
    overlapMsg = `<div class="cwtv-verdict cwtv-verdict-best">${t('compare.wtv_both_perfect').replace('{months}', bestMonths)}</div>`;
  } else if (sweetCount > 0) {
    const sweetMonths = monthNames.filter((_,i) => tagsA[i] >= 2 && tagsB[i] >= 2).join(', ');
    overlapMsg = `<div class="cwtv-verdict">${t('compare.wtv_both_good').replace('{months}', sweetMonths)}</div>`;
  } else {
    overlapMsg = `<div class="cwtv-verdict cwtv-verdict-warn">${t('compare.wtv_no_overlap')}</div>`;
  }

  const nameA = islandName(iA.key);
  const nameB = islandName(iB.key);

  // Build the legend — include 'Limited service' indicator only if at least one
  // island actually has a limited month in the selection.
  const anyLimited = limitedA.some(Boolean) || limitedB.some(Boolean);
  const limitedLegendItem = anyLimited
    ? `<span class="cwtv-leg cwtv-leg-limited" aria-hidden="true"></span>${limitedLabel}`
    : '';

  el.innerHTML = `
    <div class="cwtv-legend-row">
      <div class="cwtv-legend">
        <span class="cwtv-leg wtv-perfect"></span>${t('wtv.perfect')}
        <span class="cwtv-leg wtv-great"></span>${t('wtv.great')}
        <span class="cwtv-leg wtv-ok"></span>${t('wtv.ok')}
        <span class="cwtv-leg wtv-avoid"></span>${t('wtv.avoid')}
        ${limitedLegendItem}
      </div>
    </div>
    <div class="cwtv-wrap">
      <div class="cwtv-labels">
        <div class="cwtv-label-a">${nameA}</div>
        <div class="cwtv-label-spacer"></div>
        <div class="cwtv-label-b">${nameB}</div>
      </div>
      <div class="cwtv-grid">${months}</div>
    </div>
    ${overlapMsg}`;
}

function renderCompareExtra(iA, iB, jsonA, jsonB) {
  const el = document.getElementById('compare-extra');
  if (!el) return;

  // Best-for verdict: dominant dimension
  function bestFor(island) {
    const dims = [
      { k: 'beach',  l: t('dim.beach'),   v: island.beach  },
      { k: 'hist',   l: t('dim.culture'), v: island.hist   },
      { k: 'night',  l: t('dim.night'),   v: island.night  },
      { k: 'access', l: t('dim.access'),  v: island.access },
      { k: 'afford', l: t('dim.afford'),  v: island.afford },
    ];
    const top = dims.sort((a,b) => b.v - a.v)[0];
    return `${top.l} (${fmt(top.v)})`;
  }

  // Character tags from ISLANDS_DATA booleans
  function charTags(island) {
    const tags = [];
    if (island.car_need <= 1.5) tags.push({ icon:'🚶', label: t('vibe.carfree') });
    if (island.drama)  tags.push({ icon:'🌋', label: t('vibe.drama') });
    if (island.hiking) tags.push({ icon:'🥾', label: t('vibe.hiking') });
    if (island.springs)tags.push({ icon:'♨️', label: t('vibe.springs') });
    if (island.chora)  tags.push({ icon:'🏛', label: t('vibe.chora') });
    if (island.sailing)tags.push({ icon:'⛵', label: t('vibe.sailing') });
    if (island.has_airport) tags.push({ icon:'✈️', label: t('vibe.airport') });
    return tags.map(tg => `<span class="cmp-char-tag">${tg.icon} ${tg.label}</span>`).join('');
  }

  // Beach summary from full JSON
  function beachSummary(island, json) {
    if (!json || !json.beaches || !json.beaches.length) return '';
    const types = new Set();
    const facings = new Set();
    json.beaches.forEach(b => {
      if (b.type) {
        const t = b.type.toLowerCase();
        if (t.includes('sand')) types.add('Sandy');
        else if (t.includes('pebble')) types.add('Pebble');
        else if (t.includes('rock')) types.add('Rocky');
      }
      if (b.facing) {
        const f = b.facing.toLowerCase();
        if (f.includes('shelter')) facings.add('sheltered');
        else if (f.includes('exposed') || f.includes('open sea')) facings.add('exposed');
        if (f.includes('meltemi') || f.includes('north')) facings.add('Meltemi-exposed');
      }
    });
    const parts = [...types, ...facings].slice(0, 3);
    return parts.length ? `<div class="cmp-beach-summary">🏖 ${parts.join(' · ')}</div>` : '';
  }

  // Getting there pills
  function transportPills(island, json) {
    const pills = (json && json.getting_there && json.getting_there.pills) || [];
    if (!pills.length) return '';
    return `<div class="cmp-transport">${pills.map(p => `<span class="cmp-transport-pill">${p}</span>`).join('')}</div>`;
  }

  function extraCard(island, json, other) {
    return `<div class="cmp-extra-card">
      <div class="cmp-extra-name">${islandName(island.key)}</div>
      <div class="cmp-bestfor"><strong>${t('compare.best_for')}:</strong> ${bestFor(island)}</div>
      <div class="cmp-char-tags">${charTags(island)}</div>
      ${beachSummary(island, json)}
      ${transportPills(island, json)}
    </div>`;
  }

  el.innerHTML = `<div class="cmp-extra-grid">${extraCard(iA, jsonA, iB)}${extraCard(iB, jsonB, iA)}</div>`;
}

function renderRadarChart(iA, iB) {
  if (!iA) { const kA = compareSelection[0]; const kB = compareSelection[1]; iA = kA && ISLANDS_DATA[kA] ? { key: kA, ...ISLANDS_DATA[kA] } : null; iB = kB && ISLANDS_DATA[kB] ? { key: kB, ...ISLANDS_DATA[kB] } : null; }
  if (!iA || !iB) return;
  const canvas = document.getElementById('compare-radar-chart');
  if (!canvas) return;
  if (radarChartInstance) radarChartInstance.destroy();
  const isDark = document.documentElement.classList.contains('dark');
  const gridColor = isDark ? 'rgba(255,255,255,0.15)' : 'rgba(0,0,0,0.1)';
  const labelColor = isDark ? 'rgba(255,255,255,0.85)' : 'rgba(0,0,0,0.7)';
  const tickBg = 'transparent';
  radarChartInstance = new Chart(canvas, {
    type: 'radar',
    data: {
      labels: COMPARE_DIMS.map(d => {
        const labels = { beach: t('dim.beach'), hist: t('dim.culture'), night: t('dim.night'), access: t('dim.access'), afford: t('dim.afford') };
        return labels[d];
      }),
      datasets: [
        { label: islandName(iA.key), data: COMPARE_DIMS.map(d => iA[d]), backgroundColor: isDark ? 'rgba(77,190,255,0.15)' : 'rgba(27,79,138,0.12)', borderColor: isDark ? '#4DBEFF' : '#1B4F8A', pointBackgroundColor: isDark ? '#4DBEFF' : '#1B4F8A', pointRadius: 4 },
        { label: islandName(iB.key), data: COMPARE_DIMS.map(d => iB[d]), backgroundColor: isDark ? 'rgba(255,203,82,0.15)' : 'rgba(196,150,42,0.12)', borderColor: isDark ? '#FFCB52' : '#C4962A', pointBackgroundColor: isDark ? '#FFCB52' : '#C4962A', pointRadius: 4 },
      ],
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: {
        r: {
          min: 0, max: 5,
          ticks: {
            stepSize: 1,
            font: { size: 10 },
            color: labelColor,
            backdropColor: tickBg,
            showLabelBackdrop: false
          },
          pointLabels: {
            font: { size: 12 },
            color: labelColor
          },
          grid: { color: gridColor },
          angleLines: { color: gridColor }
        }
      },
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            font: { size: 12 },
            boxWidth: 14,
            color: labelColor
          }
        }
      },
    },
  });
}

function renderCompareCards(iA, iB) {
  const container = document.getElementById('compare-cards');
  if (!container) return;

  const carWords = ['', t('car.none'), t('car.helpful'), t('car.useful'), t('car.recommended'), t('car.essential')];

  // Per-dimension scores are intentionally omitted from the cards — the radar
  // chart above shows the same data more clearly. The cards summarize each
  // island (overall total + practical info) rather than re-listing the bars.
  const card = (island) => {
    const carLabel = carWords[Math.round(island.car_need || 0)] || '—';
    const airportRow = island.has_airport ? `<div class="cmp-info-row"><span class="cmp-info-label">✈ ${t('tooltip.hasairport')}</span><span class="cmp-info-val">${t('common.yes')}</span></div>` : '';
    const daysRow = island.days ? `<div class="cmp-info-row"><span class="cmp-info-label">⏱ ${t('tooltip.suggesteddays')}</span><span class="cmp-info-val">${island.days} ${t('common.days')}</span></div>` : '';

    return `<div class="compare-card">
      <div class="compare-card-head">
        <h2>${islandName(island.key)}</h2>
        <div class="compare-total" style="color:${scoreToColor(island.total)}">${fmt(island.total)}<span>/5</span></div>
      </div>
      <div class="compare-meta">${groupName(island.island_group)} · ${fmtNum(island.area)} km² · ${t('compare.pop')}. ${fmtNum(island.pop)}</div>
      <div class="cmp-info-panel">
        <div class="cmp-info-row"><span class="cmp-info-label">🚗 ${t('dim.car')}</span><span class="cmp-info-val"><strong>${carLabel}</strong></span></div>
        ${airportRow}
        ${daysRow}
      </div>
    </div>`;
  };

  container.innerHTML = card(iA) + card(iB);
}

/* ============================================================
   HOPPING
============================================================ */
function setupHopping() {}



/* ============================================================
   FERRY ROUTES MAP — 15 most popular Greek ferry connections
============================================================ */
// Piraeus location (not an island, used as start of many routes)
const PIRAEUS = { name: 'Piraeus (Athens)', lat: 37.940, lng: 23.643 };

// Rhodes port (not the island centroid)
const RHODES_PORT = { lat: 36.451, lng: 28.227 };

// Each route: from, to, frequency (high/med/low), duration, note
// polyline: optional array of keys for multi-stop routes drawn as one line
// ============================================================
//  FERRY PLANNER — graph + Dijkstra pathfinding
//  ~170 island↔island and mainland→island routes for shortest-path queries.
//  See: findFerryRoute(fromKey, toKey) below.
// ============================================================

// Main ferry port coordinates per island. Used for the ferry network map so the
// dots sit at the actual harbour rather than the geographic centroid (matters most
// for big islands like Crete, Rhodes, Naxos where centroid != port).
const ISLAND_FERRY_PORTS = {
  'aegina': { lat: 37.745, lng: 23.43 },
  'agathonisi': { lat: 37.464, lng: 26.989 },
  'agios-efstratios': { lat: 39.51, lng: 24.998 },
  'agistri': { lat: 37.7, lng: 23.347 },
  'alonnisos': { lat: 39.149, lng: 23.857 },
  'ammouliani': { lat: 40.335, lng: 23.920 },
  'amorgos': { lat: 36.835, lng: 25.882 },
  'anafi': { lat: 36.355, lng: 25.766 },
  'andros': { lat: 37.881, lng: 24.738 },
  'antiparos': { lat: 37.041, lng: 25.084 },
  'astypalaia': { lat: 36.557, lng: 26.353 },
  'chania': { lat: 35.491, lng: 24.08 },
  'chios': { lat: 38.371, lng: 26.137 },
  'corfu': { lat: 39.624, lng: 19.92 },
  'donousa': { lat: 37.105, lng: 25.812 },
  'elafonisos': { lat: 36.499, lng: 22.978 },
  'evia-central': { lat: 38.464, lng: 23.598 },
  'evia-north': { lat: 38.901, lng: 23.04 },
  'evia-south': { lat: 38.084, lng: 24.297 },
  'folegandros': { lat: 36.612, lng: 24.913 },
  'fournoi': { lat: 37.594, lng: 26.5 },
  'gavdos': { lat: 34.844, lng: 24.124 },
  'halki': { lat: 36.224, lng: 27.617 },
  'heraklion': { lat: 35.342, lng: 25.155 },
  'hydra': { lat: 37.349, lng: 23.466 },
  'ikaria': { lat: 37.62, lng: 26.213 },
  'ios': { lat: 36.722, lng: 25.282 },
  'iraklia': { lat: 36.846, lng: 25.469 },
  'ithaca': { lat: 38.364, lng: 20.718 },
  'kalymnos': { lat: 36.948, lng: 26.989 },
  'karpathos': { lat: 35.508, lng: 27.213 },
  'kasos': { lat: 35.408, lng: 26.926 },
  'kastellorizo': { lat: 36.144, lng: 29.594 },
  'kea': { lat: 37.659, lng: 24.318 },
  'kefalonia': { lat: 38.252, lng: 20.643 },
  'kimolos': { lat: 36.794, lng: 24.575 },
  'kos': { lat: 36.893, lng: 27.288 },
  'koufonisia': { lat: 36.937, lng: 25.594 },
  'kythira': { lat: 36.270, lng: 23.079 },
  'kythnos': { lat: 37.388, lng: 24.408 },
  'lasithi': { lat: 35.197, lng: 25.722 },
  'lefkada': { lat: 38.700, lng: 20.713 },
  'leipsoi': { lat: 37.301, lng: 26.762 },
  'lemnos': { lat: 39.876, lng: 25.067 },
  'leros': { lat: 37.139, lng: 26.802 },
  'lesvos': { lat: 39.108, lng: 26.554 },
  'meganisi': { lat: 38.658, lng: 20.755 },
  'milos': { lat: 36.737, lng: 24.435 },
  'mykonos': { lat: 37.446, lng: 25.328 },
  'naxos': { lat: 37.106, lng: 25.378 },
  'nisyros': { lat: 36.378, lng: 27.143 },
  'oinousses': { lat: 38.518, lng: 26.22 },
  'paros': { lat: 37.084, lng: 25.15 },
  'patmos': { lat: 37.31, lng: 26.554 },
  'paxos': { lat: 39.196, lng: 20.187 },
  'poros': { lat: 37.499, lng: 23.451 },
  'psara': { lat: 38.534, lng: 25.561 },
  'rethymno': { lat: 35.367, lng: 24.487 },
  'rhodes': { lat: 36.451, lng: 28.227 },
  'salamis': { lat: 37.943, lng: 23.523 },
  'samos': { lat: 37.751, lng: 26.978 },
  'samothrace': { lat: 40.481, lng: 25.473 },
  'santorini': { lat: 36.413, lng: 25.43 },
  'schoinoussa': { lat: 36.864, lng: 25.527 },
  'serifos': { lat: 37.142, lng: 24.518 },
  'sifnos': { lat: 36.967, lng: 24.677 },
  'sikinos': { lat: 36.694, lng: 25.128 },
  'skiathos': { lat: 39.165, lng: 23.49 },
  'skopelos': { lat: 39.122, lng: 23.728 },
  'skyros': { lat: 38.840, lng: 24.534 },
  'spetses': { lat: 37.262, lng: 23.157 },
  'symi': { lat: 36.617, lng: 27.842 },
  'syros': { lat: 37.444, lng: 24.943 },
  'thasos': { lat: 40.776, lng: 24.713 },
  'therasia': { lat: 36.426, lng: 25.378 },
  'tilos': { lat: 36.418, lng: 27.378 },
  'tinos': { lat: 37.539, lng: 25.162 },
  'zakynthos': { lat: 37.787, lng: 20.898 },
};

const FERRY_GRAPH = [
  { a: 'aegina', b: 'agistri', dur: 15, freq: 'high', plo: 3, phi: 5, note: "multiple daily" },
  { a: 'aegina', b: 'poros', dur: 60, freq: 'high', plo: 10, phi: 16, note: "multiple daily" },
  { a: 'agathonisi', b: 'patmos', dur: 60, freq: 'low', plo: 8, phi: 14, note: "2-3/week" },
  { a: 'agathonisi', b: 'samos', dur: 90, freq: 'low', plo: 10, phi: 16, note: "2-3/week" },
  { a: 'agia-marina', b: 'nea-styra', dur: 30, freq: 'high', plo: 4, phi: 8, note: "frequent ferry to Nea Styra" },
  { a: 'alexandroupoli', b: 'samothrace', dur: 150, freq: 'med', plo: 12, phi: 22, note: "6/week" },
  { a: 'amorgos', b: 'astypalaia', dur: 180, freq: 'low', plo: 18, phi: 28, note: "2-3/week" },
  { a: 'andros', b: 'mykonos', dur: 135, freq: 'med', plo: 18, phi: 28, note: "most days" },
  { a: 'andros', b: 'syros', dur: 150, freq: 'med', plo: 14, phi: 24, note: "most days" },
  { a: 'andros', b: 'tinos', dur: 105, freq: 'high', plo: 12, phi: 20, note: "daily" },
  { a: 'arkitsa', b: 'aidipsos', dur: 40, freq: 'high', plo: 5, phi: 10, note: "every 1-2h to Loutra Aidipsou" },
  { a: 'astypalaia', b: 'kalymnos', dur: 180, freq: 'low', plo: 14, phi: 22, note: "2-3/week" },
  { a: 'astypalaia', b: 'kos', dur: 240, freq: 'low', plo: 18, phi: 28, note: "3-4/week" },
  { a: 'chios', b: 'lesvos', dur: 180, freq: 'med', plo: 18, phi: 28, note: "6/week" },
  { a: 'chios', b: 'oinousses', dur: 60, freq: 'high', plo: 4, phi: 8, note: "daily small ferry" },
  { a: 'chios', b: 'psara', dur: 240, freq: 'low', plo: 10, phi: 18, note: "2-3/week" },
  { a: 'chios', b: 'samos', dur: 240, freq: 'low', plo: 18, phi: 28, note: "3-4/week" },
  { a: 'corfu', b: 'paxos', dur: 90, freq: 'med', plo: 14, phi: 22, note: "4-5/week summer" },
  { a: 'donousa', b: 'amorgos', dur: 60, freq: 'med', plo: 8, phi: 14, note: "Skopelitis to Aegiali" },
  { a: 'folegandros', b: 'ios', dur: 45, freq: 'med', plo: 10, phi: 16, note: "most days" },
  { a: 'folegandros', b: 'milos', dur: 90, freq: 'med', plo: 12, phi: 20, note: "daily summer" },
  { a: 'folegandros', b: 'santorini', dur: 90, freq: 'med', plo: 14, phi: 22, note: "most days" },
  { a: 'folegandros', b: 'sikinos', dur: 30, freq: 'med', plo: 6, phi: 12, note: "most days" },
  { a: 'fournoi', b: 'ikaria', dur: 60, freq: 'med', plo: 6, phi: 12, note: "most days" },
  { a: 'halki', b: 'tilos', dur: 90, freq: 'low', plo: 12, phi: 18, note: "2-3/week" },
  { a: 'heraklion', b: 'ios', dur: 135, freq: 'med', plo: 28, phi: 45, note: "most days summer" },
  { a: 'heraklion', b: 'karpathos', dur: 420, freq: 'low', plo: 25, phi: 40, note: "2-3/week" },
  { a: 'heraklion', b: 'kasos', dur: 360, freq: 'low', plo: 22, phi: 35, note: "2-3/week" },
  { a: 'heraklion', b: 'mykonos', dur: 165, freq: 'med', plo: 35, phi: 60, note: "most days summer" },
  { a: 'heraklion', b: 'naxos', dur: 150, freq: 'med', plo: 30, phi: 50, note: "most days summer" },
  { a: 'heraklion', b: 'paros', dur: 180, freq: 'med', plo: 30, phi: 50, note: "most days summer" },
  { a: 'heraklion', b: 'rhodes', dur: 720, freq: 'low', plo: 35, phi: 60, note: "2-3/week" },
  { a: 'heraklion', b: 'santorini', dur: 105, freq: 'high', plo: 30, phi: 50, note: "daily SeaJets" },
  { a: 'hydra', b: 'spetses', dur: 30, freq: 'high', plo: 14, phi: 22, note: "multiple daily" },
  { a: 'igoumenitsa', b: 'corfu', dur: 90, freq: 'high', plo: 11, phi: 18, note: "multiple daily" },
  { a: 'igoumenitsa', b: 'paxos', dur: 90, freq: 'low', plo: 14, phi: 22, note: "few/week" },
  { a: 'ios', b: 'santorini', dur: 50, freq: 'high', plo: 18, phi: 28, note: "daily" },
  { a: 'iraklia', b: 'schoinoussa', dur: 30, freq: 'med', plo: 4, phi: 8, note: "Skopelitis" },
  { a: 'kalymnos', b: 'leros', dur: 45, freq: 'high', plo: 8, phi: 14, note: "daily" },
  { a: 'karpathos', b: 'kasos', dur: 60, freq: 'med', plo: 8, phi: 14, note: "4-5/week" },
  { a: 'kasos', b: 'rhodes', dur: 300, freq: 'low', plo: 22, phi: 38, note: "2-3/week" },
  { a: 'kavala', b: 'thasos', dur: 80, freq: 'high', plo: 7, phi: 12, note: "every 1-2h, also Keramoti 35min" },
  { a: 'kefalonia', b: 'ithaca', dur: 30, freq: 'high', plo: 4, phi: 7, note: "multiple daily" },
  { a: 'kefalonia', b: 'zakynthos', dur: 90, freq: 'low', plo: 12, phi: 18, note: "summer-only via Pesada" },
  { a: 'keramoti', b: 'thasos', dur: 35, freq: 'high', plo: 4, phi: 7, note: "every 30-60min" },
  { a: 'kos', b: 'kalymnos', dur: 45, freq: 'high', plo: 8, phi: 14, note: "daily catamaran + Mastichari shuttle" },
  { a: 'kos', b: 'leros', dur: 90, freq: 'high', plo: 12, phi: 20, note: "daily" },
  { a: 'kos', b: 'nisyros', dur: 75, freq: 'med', plo: 10, phi: 18, note: "most days" },
  { a: 'kos', b: 'patmos', dur: 150, freq: 'high', plo: 18, phi: 28, note: "daily" },
  { a: 'koufonisia', b: 'amorgos', dur: 75, freq: 'med', plo: 10, phi: 16, note: "Skopelitis" },
  { a: 'koufonisia', b: 'donousa', dur: 60, freq: 'med', plo: 6, phi: 12, note: "Skopelitis" },
  { a: 'kyllini', b: 'kefalonia', dur: 90, freq: 'high', plo: 11, phi: 18, note: "to Poros, multiple daily" },
  { a: 'kyllini', b: 'zakynthos', dur: 60, freq: 'high', plo: 9, phi: 15, note: "multiple daily" },
  { a: 'kymi', b: 'skyros', dur: 90, freq: 'med', plo: 12, phi: 22, note: "2/day" },
  { a: 'kythnos', b: 'kea', dur: 90, freq: 'low', plo: 8, phi: 14, note: "2-3/week" },
  { a: 'kythnos', b: 'serifos', dur: 60, freq: 'med', plo: 8, phi: 14, note: "most days" },
  { a: 'lavrio', b: 'kea', dur: 60, freq: 'high', plo: 10, phi: 16, note: "multiple daily" },
  { a: 'lavrio', b: 'kythnos', dur: 150, freq: 'med', plo: 16, phi: 24, note: "daily" },
  { a: 'lefkada', b: 'ithaca', dur: 75, freq: 'med', plo: 10, phi: 16, note: "summer" },
  { a: 'lefkada', b: 'kefalonia', dur: 90, freq: 'med', plo: 10, phi: 16, note: "from Vassiliki to Fiskardo, summer" },
  { a: 'lefkada', b: 'meganisi', dur: 25, freq: 'high', plo: 4, phi: 7, note: "multiple daily from Nydri" },
  { a: 'leipsoi', b: 'agathonisi', dur: 60, freq: 'low', plo: 8, phi: 12, note: "2-3/week" },
  { a: 'lemnos', b: 'agios-efstratios', dur: 150, freq: 'low', plo: 8, phi: 14, note: "2-3/week" },
  { a: 'lemnos', b: 'kavala', dur: 360, freq: 'low', plo: 22, phi: 35, note: "2-3/week" },
  { a: 'leros', b: 'leipsoi', dur: 30, freq: 'med', plo: 6, phi: 10, note: "most days" },
  { a: 'leros', b: 'patmos', dur: 60, freq: 'high', plo: 10, phi: 16, note: "daily" },
  { a: 'lesvos', b: 'lemnos', dur: 360, freq: 'low', plo: 22, phi: 35, note: "2/week" },
  { a: 'milos', b: 'kimolos', dur: 30, freq: 'high', plo: 4, phi: 8, note: "daily" },
  { a: 'mykonos', b: 'santorini', dur: 150, freq: 'high', plo: 35, phi: 65, note: "daily" },
  { a: 'naxos', b: 'amorgos', dur: 180, freq: 'med', plo: 16, phi: 28, note: "daily" },
  { a: 'naxos', b: 'ios', dur: 90, freq: 'high', plo: 18, phi: 28, note: "daily" },
  { a: 'naxos', b: 'iraklia', dur: 90, freq: 'med', plo: 10, phi: 16, note: "Skopelitis, 6/week" },
  { a: 'naxos', b: 'mykonos', dur: 90, freq: 'high', plo: 22, phi: 35, note: "daily" },
  { a: 'naxos', b: 'santorini', dur: 120, freq: 'high', plo: 28, phi: 50, note: "daily" },
  { a: 'neapoli', b: 'kythira', dur: 60, freq: 'high', plo: 12, phi: 18, note: "multiple daily" },
  { a: 'paros', b: 'antiparos', dur: 10, freq: 'high', plo: 1, phi: 2, note: "continuous shuttle" },
  { a: 'paros', b: 'ios', dur: 90, freq: 'high', plo: 18, phi: 28, note: "daily" },
  { a: 'paros', b: 'mykonos', dur: 45, freq: 'high', plo: 18, phi: 30, note: "multiple daily" },
  { a: 'paros', b: 'naxos', dur: 30, freq: 'high', plo: 8, phi: 14, note: "shortest major hop, 8+/day" },
  { a: 'paros', b: 'santorini', dur: 150, freq: 'high', plo: 30, phi: 55, note: "daily" },
  { a: 'patmos', b: 'ikaria', dur: 120, freq: 'med', plo: 14, phi: 22, note: "most days" },
  { a: 'patmos', b: 'leipsoi', dur: 30, freq: 'high', plo: 5, phi: 9, note: "multiple daily summer" },
  { a: 'patmos', b: 'samos', dur: 105, freq: 'med', plo: 14, phi: 22, note: "most days" },
  { a: 'patras', b: 'ithaca', dur: 210, freq: 'med', plo: 14, phi: 22, note: "to Pisaetos, daily" },
  { a: 'patras', b: 'kefalonia', dur: 180, freq: 'med', plo: 14, phi: 22, note: "to Sami, daily" },
  { a: 'perama', b: 'salamis', dur: 15, freq: 'high', plo: 1, phi: 2, note: "every 15min" },
  { a: 'piraeus', b: 'aegina', dur: 60, freq: 'high', plo: 10, phi: 15, note: "Hellenic Seaways, Saronic Ferries · multiple daily" },
  { a: 'piraeus', b: 'agistri', dur: 75, freq: 'high', plo: 10, phi: 15, note: "via Aegina, multiple daily" },
  { a: 'piraeus', b: 'amorgos', dur: 540, freq: 'med', plo: 40, phi: 55, note: "via Naxos, daily" },
  { a: 'piraeus', b: 'anafi', dur: 540, freq: 'low', plo: 42, phi: 65, note: "via Santorini, 3-4/week" },
  { a: 'piraeus', b: 'andros', dur: 240, freq: 'med', plo: 28, phi: 42, note: "via Rafina more direct" },
  { a: 'piraeus', b: 'astypalaia', dur: 660, freq: 'low', plo: 45, phi: 65, note: "2-3/week" },
  { a: 'piraeus', b: 'chios', dur: 480, freq: 'med', plo: 38, phi: 60, note: "overnight daily" },
  { a: 'piraeus', b: 'donousa', dur: 540, freq: 'low', plo: 38, phi: 55, note: "via Naxos" },
  { a: 'piraeus', b: 'folegandros', dur: 360, freq: 'med', plo: 40, phi: 60, note: "daily summer" },
  { a: 'piraeus', b: 'heraklion', dur: 540, freq: 'high', plo: 40, phi: 90, note: "overnight daily, Minoan/Anek" },
  { a: 'piraeus', b: 'hydra', dur: 120, freq: 'high', plo: 28, phi: 35, note: "Flying Cat hydrofoil" },
  { a: 'piraeus', b: 'ikaria', dur: 540, freq: 'med', plo: 40, phi: 60, note: "daily summer" },
  { a: 'piraeus', b: 'ios', dur: 420, freq: 'high', plo: 40, phi: 65, note: "multiple daily summer" },
  { a: 'piraeus', b: 'iraklia', dur: 480, freq: 'low', plo: 38, phi: 55, note: "via Naxos, Express Skopelitis" },
  { a: 'piraeus', b: 'kalymnos', dur: 720, freq: 'med', plo: 48, phi: 75, note: "daily" },
  { a: 'piraeus', b: 'karpathos', dur: 1020, freq: 'low', plo: 50, phi: 90, note: "2-3/week, via Crete" },
  { a: 'piraeus', b: 'kasos', dur: 1080, freq: 'low', plo: 50, phi: 90, note: "2-3/week, via Crete" },
  { a: 'piraeus', b: 'kimolos', dur: 270, freq: 'med', plo: 32, phi: 50, note: "via Milos most days" },
  { a: 'piraeus', b: 'kos', dur: 780, freq: 'med', plo: 50, phi: 80, note: "daily Blue Star" },
  { a: 'piraeus', b: 'koufonisia', dur: 510, freq: 'low', plo: 38, phi: 55, note: "via Naxos" },
  { a: 'piraeus', b: 'kythira', dur: 420, freq: 'low', plo: 35, phi: 55, note: "2-3/week" },
  { a: 'piraeus', b: 'kythnos', dur: 150, freq: 'high', plo: 22, phi: 32, note: "multiple daily" },
  { a: 'piraeus', b: 'lemnos', dur: 1080, freq: 'low', plo: 45, phi: 80, note: "overnight, 2-3/week" },
  { a: 'piraeus', b: 'leros', dur: 660, freq: 'med', plo: 45, phi: 70, note: "daily Blue Star" },
  { a: 'piraeus', b: 'lesvos', dur: 720, freq: 'med', plo: 40, phi: 70, note: "overnight daily" },
  { a: 'piraeus', b: 'milos', dur: 240, freq: 'high', plo: 35, phi: 55, note: "Adamantios Korais, SeaJets" },
  { a: 'piraeus', b: 'mykonos', dur: 285, freq: 'high', plo: 30, phi: 65, note: "Hellenic Seaways, SeaJets · daily" },
  { a: 'piraeus', b: 'naxos', dur: 300, freq: 'high', plo: 38, phi: 55, note: "Blue Star, SeaJets · multiple daily" },
  { a: 'piraeus', b: 'paros', dur: 240, freq: 'high', plo: 36, phi: 55, note: "Blue Star, SeaJets · multiple daily" },
  { a: 'piraeus', b: 'patmos', dur: 540, freq: 'med', plo: 42, phi: 65, note: "daily Blue Star" },
  { a: 'piraeus', b: 'poros', dur: 90, freq: 'high', plo: 14, phi: 22, note: "multiple daily" },
  { a: 'piraeus', b: 'rhodes', dur: 960, freq: 'med', plo: 55, phi: 180, note: "daily, 13-18h" },
  { a: 'piraeus', b: 'salamis', dur: 15, freq: 'high', plo: 1, phi: 2, note: "from Perama, very frequent" },
  { a: 'piraeus', b: 'samos', dur: 720, freq: 'med', plo: 42, phi: 70, note: "overnight" },
  { a: 'piraeus', b: 'santorini', dur: 450, freq: 'high', plo: 40, phi: 90, note: "Blue Star, SeaJets · daily" },
  { a: 'piraeus', b: 'schoinoussa', dur: 510, freq: 'low', plo: 38, phi: 55, note: "via Naxos" },
  { a: 'piraeus', b: 'serifos', dur: 180, freq: 'high', plo: 30, phi: 42, note: "daily" },
  { a: 'piraeus', b: 'sifnos', dur: 210, freq: 'high', plo: 32, phi: 48, note: "daily" },
  { a: 'piraeus', b: 'sikinos', dur: 420, freq: 'med', plo: 38, phi: 58, note: "via Folegandros" },
  { a: 'piraeus', b: 'spetses', dur: 130, freq: 'high', plo: 35, phi: 45, note: "Flying Cat" },
  { a: 'piraeus', b: 'syros', dur: 240, freq: 'high', plo: 28, phi: 38, note: "Blue Star, Golden Star · daily" },
  { a: 'piraeus', b: 'tinos', dur: 270, freq: 'high', plo: 30, phi: 50, note: "via Syros" },
  { a: 'poros', b: 'hydra', dur: 30, freq: 'high', plo: 12, phi: 18, note: "multiple daily" },
  { a: 'pounta', b: 'elafonisos', dur: 10, freq: 'high', plo: 1, phi: 2, note: "every 30 min" },
  { a: 'rafina', b: 'andros', dur: 120, freq: 'high', plo: 18, phi: 28, note: "multiple daily Hellenic Seaways" },
  { a: 'rafina', b: 'evia-south', dur: 60, freq: 'high', plo: 6, phi: 12, note: "to Marmari, multiple daily" },
  { a: 'rafina', b: 'mykonos', dur: 165, freq: 'high', plo: 28, phi: 50, note: "fast daily" },
  { a: 'rafina', b: 'naxos', dur: 225, freq: 'med', plo: 35, phi: 55, note: "fast daily summer" },
  { a: 'rafina', b: 'paros', dur: 195, freq: 'med', plo: 32, phi: 50, note: "fast daily summer" },
  { a: 'rafina', b: 'tinos', dur: 165, freq: 'high', plo: 22, phi: 35, note: "multiple daily" },
  { a: 'rhodes', b: 'halki', dur: 60, freq: 'high', plo: 10, phi: 18, note: "daily small ferry" },
  { a: 'rhodes', b: 'karpathos', dur: 240, freq: 'med', plo: 22, phi: 38, note: "most days" },
  { a: 'rhodes', b: 'kastellorizo', dur: 180, freq: 'low', plo: 18, phi: 30, note: "3-4/week" },
  { a: 'rhodes', b: 'kos', dur: 150, freq: 'high', plo: 22, phi: 38, note: "daily Dodekanisos Express" },
  { a: 'rhodes', b: 'nisyros', dur: 180, freq: 'low', plo: 18, phi: 28, note: "2-3/week direct, more via Kos" },
  { a: 'rhodes', b: 'symi', dur: 60, freq: 'high', plo: 12, phi: 22, note: "daily Dodekanisos Pride" },
  { a: 'rhodes', b: 'tilos', dur: 105, freq: 'med', plo: 14, phi: 24, note: "most days" },
  { a: 'samos', b: 'fournoi', dur: 90, freq: 'med', plo: 8, phi: 14, note: "most days" },
  { a: 'samos', b: 'ikaria', dur: 90, freq: 'med', plo: 12, phi: 20, note: "daily" },
  { a: 'mykonos', b: 'ikaria', dur: 180, freq: 'med', plo: 18, phi: 28, note: "Blue Star Patmos line" },
  { a: 'santorini', b: 'anafi', dur: 90, freq: 'med', plo: 15, phi: 25, note: "5-6/week" },
  { a: 'santorini', b: 'milos', dur: 180, freq: 'med', plo: 28, phi: 42, note: "daily summer" },
  { a: 'santorini', b: 'therasia', dur: 20, freq: 'high', plo: 3, phi: 5, note: "small boats from Ammoudi/Athinios" },
  { a: 'schoinoussa', b: 'koufonisia', dur: 30, freq: 'med', plo: 4, phi: 8, note: "Skopelitis" },
  { a: 'serifos', b: 'sifnos', dur: 45, freq: 'high', plo: 8, phi: 14, note: "daily" },
  { a: 'sfakia', b: 'gavdos', dur: 150, freq: 'low', plo: 14, phi: 22, note: "3-5/week summer only" },
  { a: 'sifnos', b: 'kimolos', dur: 60, freq: 'med', plo: 10, phi: 16, note: "most days" },
  { a: 'sifnos', b: 'milos', dur: 75, freq: 'high', plo: 12, phi: 20, note: "daily" },
  { a: 'sikinos', b: 'ios', dur: 60, freq: 'med', plo: 8, phi: 14, note: "most days" },
  { a: 'sikinos', b: 'santorini', dur: 120, freq: 'low', plo: 14, phi: 22, note: "4-5/week" },
  { a: 'sitia', b: 'karpathos', dur: 240, freq: 'low', plo: 14, phi: 24, note: "2-3/week" },
  { a: 'sitia', b: 'kasos', dur: 150, freq: 'low', plo: 10, phi: 18, note: "2-3/week" },
  { a: 'skiathos', b: 'alonnisos', dur: 90, freq: 'high', plo: 18, phi: 28, note: "multiple daily" },
  { a: 'skiathos', b: 'skopelos', dur: 60, freq: 'high', plo: 14, phi: 22, note: "multiple daily" },
  { a: 'skopelos', b: 'alonnisos', dur: 30, freq: 'high', plo: 8, phi: 14, note: "multiple daily" },
  { a: 'souda', b: 'piraeus', dur: 540, freq: 'high', plo: 40, phi: 120, note: "overnight" },
  { a: 'symi', b: 'kos', dur: 105, freq: 'low', plo: 14, phi: 22, note: "3-4/week" },
  { a: 'syros', b: 'mykonos', dur: 60, freq: 'med', plo: 14, phi: 22, note: "most days" },
  { a: 'syros', b: 'paros', dur: 75, freq: 'med', plo: 14, phi: 22, note: "daily" },
  { a: 'syros', b: 'tinos', dur: 30, freq: 'high', plo: 10, phi: 18, note: "daily" },
  { a: 'tilos', b: 'kos', dur: 150, freq: 'low', plo: 14, phi: 22, note: "3-4/week" },
  { a: 'tilos', b: 'symi', dur: 90, freq: 'low', plo: 12, phi: 18, note: "2-3/week" },
  { a: 'tinos', b: 'mykonos', dur: 25, freq: 'high', plo: 10, phi: 18, note: "multiple daily" },
  { a: 'tripiti', b: 'ammouliani', dur: 5, freq: 'high', plo: 1, phi: 2, note: "frequent" },
  { a: 'volos', b: 'alonnisos', dur: 300, freq: 'high', plo: 24, phi: 45, note: "multiple daily" },
  { a: 'volos', b: 'skiathos', dur: 150, freq: 'high', plo: 18, phi: 35, note: "multiple daily" },
  { a: 'volos', b: 'skopelos', dur: 240, freq: 'high', plo: 22, phi: 42, note: "multiple daily" },
  { a: 'agios-konstantinos', b: 'skiathos', dur: 165, freq: 'med', plo: 30, phi: 50, note: "Hellenic Seaways · daily summer" },
  { a: 'agios-konstantinos', b: 'skopelos', dur: 240, freq: 'med', plo: 35, phi: 55, note: "Hellenic Seaways · daily summer" },
  { a: 'agios-konstantinos', b: 'alonnisos', dur: 270, freq: 'med', plo: 38, phi: 60, note: "Hellenic Seaways · daily summer" },
  { a: 'paros', b: 'folegandros', dur: 105, freq: 'med', plo: 16, phi: 26, note: "most days" },
  { a: 'naxos', b: 'folegandros', dur: 90, freq: 'med', plo: 14, phi: 22, note: "most days" },
  { a: 'paros', b: 'milos', dur: 165, freq: 'med', plo: 18, phi: 28, note: "most days summer" },
  { a: 'naxos', b: 'milos', dur: 180, freq: 'low', plo: 18, phi: 28, note: "few/week summer" },
  { a: 'paros', b: 'sifnos', dur: 105, freq: 'low', plo: 14, phi: 22, note: "few/week" },
  { a: 'paros', b: 'serifos', dur: 135, freq: 'low', plo: 16, phi: 24, note: "few/week" },
];



// Multi-stop visual polylines for the ferry map. These represent ferries that make
// multiple stops on the same route (e.g. Volos→Skiathos→Skopelos→Alonnisos is one boat).
// The map renderer draws these as a single curved path through all stops; the
// individual edges between consecutive stops are skipped to avoid double-drawing.
// Pathfinding is unaffected — the FERRY_GRAPH still contains all individual edges.
const FERRY_VISUAL_LINES = [
  // Sporades — Volos hop
  { stops: ['volos', 'skiathos', 'skopelos', 'alonnisos'],                  freq: 'high' },
  { stops: ['agios-konstantinos', 'skiathos', 'skopelos', 'alonnisos'],     freq: 'med' },
  // Saronic chain
  { stops: ['piraeus', 'aegina', 'poros', 'hydra', 'spetses'],              freq: 'high' },
  // Cyclades from Athens — Rafina lines
  { stops: ['rafina', 'andros', 'tinos', 'mykonos'],                        freq: 'high' },
  // Cyclades from Athens — Lavrio (West Cyclades short hop)
  { stops: ['lavrio', 'kea', 'kythnos'],                                    freq: 'high' },
  // Western Cyclades — Piraeus chain (the same boat: Piraeus → Kythnos → Serifos → Sifnos → Milos)
  { stops: ['piraeus', 'kythnos', 'serifos', 'sifnos', 'milos'],            freq: 'high' },
  // Folegandros via Milos
  { stops: ['piraeus', 'milos', 'folegandros'],                             freq: 'med' },
  // Eastern Cyclades — Piraeus → Syros → Tinos → Mykonos
  { stops: ['piraeus', 'syros', 'tinos', 'mykonos'],                        freq: 'high' },
  // Central Cyclades — Piraeus → Paros → Naxos
  { stops: ['piraeus', 'paros', 'naxos'],                                   freq: 'high' },
  // Santorini line — Piraeus → Naxos → Ios → Santorini → Anafi
  { stops: ['piraeus', 'naxos', 'ios', 'santorini', 'anafi'],               freq: 'high' },
  // Small Cyclades (Express Skopelitis)
  { stops: ['naxos', 'iraklia', 'schoinoussa', 'koufonisia', 'donousa', 'amorgos'],   freq: 'low' },
  // Astypalaia via Amorgos
  { stops: ['piraeus', 'amorgos', 'astypalaia'],                            freq: 'low' },
  // NE Aegean — Piraeus → Chios → Lesvos overnight
  { stops: ['piraeus', 'chios', 'lesvos'],                                  freq: 'med' },
  // Eastern Aegean — Piraeus → Mykonos → Ikaria → Samos
  { stops: ['piraeus', 'mykonos', 'ikaria', 'samos'],                       freq: 'med' },
  // Dodecanese Blue Star — Piraeus → Kalymnos → Kos → Rhodes (the iconic SE Aegean run)
  { stops: ['piraeus', 'kalymnos', 'kos', 'rhodes'],                        freq: 'med' },
  // Karpathos / Kasos line from Rhodes
  { stops: ['rhodes', 'karpathos', 'kasos'],                                freq: 'low' },
];

// Helper: returns a Set of "a~b" keys (sorted) for every pair of stops on the
// SAME visual polyline. Used to skip drawing direct edges that would otherwise
// run parallel to a polyline. e.g. if Piraeus → Naxos → Ios → Santorini is a
// visual line, we hide the direct piraeus↔santorini edge so the map shows only
// the multi-stop curve through actual ferry stops.
function buildVisualEdgeSet() {
  const s = new Set();
  FERRY_VISUAL_LINES.forEach(line => {
    for (let i = 0; i < line.stops.length; i++) {
      for (let j = i + 1; j < line.stops.length; j++) {
        const key = [line.stops[i], line.stops[j]].sort().join('~');
        s.add(key);
      }
    }
  });
  return s;
}
const FERRY_VISUAL_EDGE_SET = buildVisualEdgeSet();

const MAINLAND_PORTS = {
  'piraeus': { name: 'Piraeus (Athens)', name_el: 'Πειραιάς (Αθήνα)', lat: 37.94, lng: 23.643 },
  'rafina': { name: 'Rafina (Athens)', name_el: 'Ραφήνα (Αθήνα)', lat: 38.024, lng: 24.005 },
  'lavrio': { name: 'Lavrio', name_el: 'Λαύριο', lat: 37.713, lng: 24.058 },
  'kyllini': { name: 'Kyllini', name_el: 'Κυλλήνη', lat: 37.939, lng: 21.146 },
  'patras': { name: 'Patras', name_el: 'Πάτρα', lat: 38.246, lng: 21.736 },
  'igoumenitsa': { name: 'Igoumenitsa', name_el: 'Ηγουμενίτσα', lat: 39.503, lng: 20.265 },
  'volos': { name: 'Volos', name_el: 'Βόλος', lat: 39.366, lng: 22.946 },
  'agios-konstantinos': { name: 'Agios Konstantinos', name_el: 'Άγιος Κωνσταντίνος', lat: 38.759, lng: 22.860 },
  'kymi': { name: 'Kymi (Evia)', name_el: 'Κύμη (Εύβοια)', lat: 38.625, lng: 24.114, onIsland: true },
  'neapoli': { name: 'Neapoli (Pelop.)', name_el: 'Νεάπολη (Πελοπ.)', lat: 36.512, lng: 23.057 },
  'pounta': { name: 'Pounta', name_el: 'Πούντα', lat: 36.521, lng: 22.979 },
  'kavala': { name: 'Kavala', name_el: 'Καβάλα', lat: 40.939, lng: 24.412 },
  'keramoti': { name: 'Keramoti', name_el: 'Κεραμωτή', lat: 40.853, lng: 24.708 },
  'alexandroupoli': { name: 'Alexandroupoli', name_el: 'Αλεξανδρούπολη', lat: 40.847, lng: 25.872 },
  'tripiti': { name: 'Tripiti (Halkidiki)', name_el: 'Τρυπητή (Χαλκιδική)', lat: 40.364, lng: 23.918 },
  'perama': { name: 'Perama (Athens)', name_el: 'Πέραμα (Αθήνα)', lat: 37.962, lng: 23.586 },
  'agia-marina': { name: 'Agia Marina', name_el: 'Αγία Μαρίνα', lat: 38.062, lng: 23.987 },
  'arkitsa': { name: 'Arkitsa', name_el: 'Αρκίτσα', lat: 38.755, lng: 23.013 },
  'sfakia': { name: 'Sfakia (Crete)', name_el: 'Σφακιά (Κρήτη)', lat: 35.201, lng: 24.137, onIsland: true },
  'sitia': { name: 'Sitia (Crete)', name_el: 'Σητεία (Κρήτη)', lat: 35.207, lng: 26.107, onIsland: true },
  'aidipsos':  { name: 'Loutra Aidipsou (Evia)',     name_el: 'Λουτρά Αιδηψού (Εύβοια)',  lat: 38.860, lng: 23.043, onIsland: true },
  'nea-styra': { name: 'Nea Styra (Evia)',           name_el: 'Νέα Στύρα (Εύβοια)',       lat: 38.180, lng: 24.208, onIsland: true },
  'souda': { name: 'Souda (Chania)', name_el: 'Σούδα (Χανιά)', lat: 35.491, lng: 24.08, onIsland: true },
};

// Ferryhopper slug conversions (some islands have non-obvious slugs there)
const FERRYHOPPER_SLUGS = {
  'lasithi': 'agios-nikolaos',
  'kefalonia': 'kefalonia-sami',
  'ithaca': 'ithaki',
  'lesvos': 'mytilene',
  'kea': 'kea-tzia',
  'thasos': 'thassos',
  'samothrace': 'samothraki',
  'salamis': 'salamina',
  // Mainland ports
  'piraeus': 'piraeus',
  'rafina': 'rafina',
  'lavrio': 'lavrio',
  'kyllini': 'kyllini',
  'patras': 'patra',
  'igoumenitsa': 'igoumenitsa',
  'volos': 'volos',
  'kymi': 'kymi',
  'neapoli': 'neapoli',
  'pounta': 'pounta',
  'kavala': 'kavala',
  'keramoti': 'keramoti',
  'alexandroupoli': 'alexandroupolis',
  'tripiti': 'tripiti',
  'perama': 'piraeus',         // close enough for booking
  'sfakia': 'chora-sfakion',
  'sitia': 'sitia',
  'souda': 'chania',            // Souda port serves Chania
  'agia-marina': 'agia-marina-attica',
  'arkitsa': 'arkitsa',
};
function ferryhopperSlug(key) {
  return FERRYHOPPER_SLUGS[key] || key;
}
function ferryhopperRouteUrl(fromKey, toKey) {
  return `https://www.ferryhopper.com/en/ferries/${ferryhopperSlug(fromKey)}/${ferryhopperSlug(toKey)}`;
}

// Build adjacency map for pathfinding (each edge stored with explicit `to`)
function buildFerryAdj() {
  const adj = {};
  FERRY_GRAPH.forEach(e => {
    if (!adj[e.a]) adj[e.a] = [];
    if (!adj[e.b]) adj[e.b] = [];
    // forward: a → b
    adj[e.a].push({ to: e.b, dur: e.dur, freq: e.freq, plo: e.plo, phi: e.phi, note: e.note });
    // reverse: b → a
    adj[e.b].push({ to: e.a, dur: e.dur, freq: e.freq, plo: e.plo, phi: e.phi, note: e.note });
  });
  return adj;
}
const FERRY_ADJ = buildFerryAdj();

// Penalty added when a route requires a transfer (in minutes)
// — encourages direct routes; transfer cost reflects waiting at port
const TRANSFER_PENALTY = 90;

// Find the best route from A to B (by total duration including transfer wait).
// Returns { hops: [...edges], totalMin, transfers, totalPriceLo, totalPriceHi } or null.
// Limits to max 2 transfers (3 hops) to keep results practical.
function findFerryRoute(fromKey, toKey) {
  if (!fromKey || !toKey || fromKey === toKey) return null;
  if (!FERRY_ADJ[fromKey]) return null;

  // Dijkstra-ish but with hop limit
  const MAX_HOPS = 3;
  const best = {};                  // key → minimum cost found so far
  const queue = [{ node: fromKey, cost: 0, path: [], hops: 0 }];
  let bestSolution = null;

  while (queue.length) {
    queue.sort((a, b) => a.cost - b.cost);
    const cur = queue.shift();
    if (cur.node === toKey) {
      if (!bestSolution || cur.cost < bestSolution.cost) {
        bestSolution = cur;
      }
      continue;
    }
    if (cur.hops >= MAX_HOPS) continue;
    if (best[cur.node] !== undefined && best[cur.node] <= cur.cost) continue;
    best[cur.node] = cur.cost;
    const edges = FERRY_ADJ[cur.node] || [];
    for (const edge of edges) {
      if (cur.path.some(h => h.to === edge.to)) continue; // no loops
      const transferCost = cur.hops > 0 ? TRANSFER_PENALTY : 0;
      const next = {
        node: edge.to,
        cost: cur.cost + edge.dur + transferCost,
        path: [...cur.path, edge],
        hops: cur.hops + 1,
      };
      queue.push(next);
    }
  }

  if (!bestSolution) return null;
  const hops = bestSolution.path;
  const totalMin = hops.reduce((s, h) => s + h.dur, 0);
  const totalPriceLo = hops.reduce((s, h) => s + h.plo, 0);
  const totalPriceHi = hops.reduce((s, h) => s + h.phi, 0);
  return {
    hops,
    totalMin,
    transfers: hops.length - 1,
    totalPriceLo,
    totalPriceHi,
  };
}

// Format minutes as "Xh Ym" or "Xm"
function formatDuration(min) {
  if (min < 60) return `${min}m`;
  const h = Math.floor(min / 60);
  const m = min % 60;
  return m === 0 ? `${h}h` : `${h}h ${m}m`;
}

// Get display name for a port/island key (handles language)
function portDisplayName(key) {
  if (MAINLAND_PORTS[key]) {
    return CURRENT_LANG === 'el' ? MAINLAND_PORTS[key].name_el : MAINLAND_PORTS[key].name;
  }
  if (ISLANDS_DATA[key]) {
    return islandName(key);
  }
  return key;
}

// All ports (mainland + islands) for the dropdowns
function allFerryPorts() {
  const islands = Object.keys(ISLANDS_DATA).filter(k => FERRY_ADJ[k]);
  const mainland = Object.keys(MAINLAND_PORTS).filter(k => FERRY_ADJ[k]);
  return { mainland, islands };
}

// Compute all reachable destinations from a node, returning {key: bestDurationMin}.
// Uses simple BFS-ish exploration with hop limit so we get realistic destinations.
function reachableFrom(fromKey, maxHops = 3) {
  if (!FERRY_ADJ[fromKey]) return {};
  const best = { [fromKey]: 0 };
  const queue = [{ node: fromKey, cost: 0, hops: 0 }];
  while (queue.length) {
    queue.sort((a, b) => a.cost - b.cost);
    const cur = queue.shift();
    if (cur.hops >= maxHops) continue;
    for (const edge of FERRY_ADJ[cur.node] || []) {
      const xfer = cur.hops > 0 ? TRANSFER_PENALTY : 0;
      const newCost = cur.cost + edge.dur + xfer;
      if (best[edge.to] === undefined || newCost < best[edge.to]) {
        best[edge.to] = newCost;
        queue.push({ node: edge.to, cost: newCost, hops: cur.hops + 1 });
      }
    }
  }
  delete best[fromKey];
  return best;
}

// Render the planner panel (called on demand from the hopping view)
function renderFerryPlanner() {
  const el = document.getElementById('ferry-planner');
  if (!el) return;

  const { mainland, islands } = allFerryPorts();
  const sortedIslands  = islands.map(k => ({ k, name: islandName(k) })).sort((a, b) => a.name.localeCompare(b.name));
  const sortedMainland = mainland.map(k => ({ k, name: portDisplayName(k) })).sort((a, b) => a.name.localeCompare(b.name));

  // FROM dropdown — full list (mainland + islands)
  const fromOptionsHtml = `<option value="">— ${t('planner.choose')} —</option>` +
    `<optgroup label="${t('planner.mainland')}">${sortedMainland.map(p => `<option value="${p.k}"${p.k === plannerState.from ? ' selected' : ''}>${p.name}</option>`).join('')}</optgroup>` +
    `<optgroup label="${t('planner.islands')}">${sortedIslands.map(p => `<option value="${p.k}"${p.k === plannerState.from ? ' selected' : ''}>${p.name}</option>`).join('')}</optgroup>`;

  el.innerHTML = `
    <div class="planner-card">
      <div class="planner-row">
        <div class="planner-field">
          <label for="planner-from">${t('planner.from')}</label>
          <select id="planner-from" class="planner-select">${fromOptionsHtml}</select>
        </div>
        <div class="planner-arrow" aria-hidden="true">→</div>
        <div class="planner-field">
          <label for="planner-to">${t('planner.to')}</label>
          <select id="planner-to" class="planner-select" disabled>
            <option value="">— ${t('planner.pickfromfirst')} —</option>
          </select>
        </div>
      </div>
      <button id="planner-go" class="planner-go-btn" disabled>${t('planner.find')}</button>
      <div id="planner-result" class="planner-result"></div>
    </div>`;

  document.getElementById('planner-from').addEventListener('change', (e) => {
    plannerState.from = e.target.value;
    plannerState.to = '';
    refreshDestinationDropdown();
    document.getElementById('planner-result').innerHTML = '';
  });
  document.getElementById('planner-to').addEventListener('change', (e) => {
    plannerState.to = e.target.value;
    document.getElementById('planner-go').disabled = !plannerState.to;
  });
  document.getElementById('planner-go').addEventListener('click', () => runPlannerSearch());

  if (plannerState.from) refreshDestinationDropdown();
}

// Update the destination dropdown to only show reachable ports, sorted by travel time
function refreshDestinationDropdown() {
  const toSelect = document.getElementById('planner-to');
  const goBtn = document.getElementById('planner-go');
  if (!toSelect) return;

  if (!plannerState.from) {
    toSelect.innerHTML = `<option value="">— ${t('planner.pickfromfirst')} —</option>`;
    toSelect.disabled = true;
    if (goBtn) goBtn.disabled = true;
    return;
  }

  const reachable = reachableFrom(plannerState.from);
  // Sort destinations by total minutes ascending
  const entries = Object.keys(reachable)
    .map(k => ({ k, cost: reachable[k], name: portDisplayName(k) }))
    .sort((a, b) => a.cost - b.cost);

  // Group by mainland vs island, but keep travel-time order within each group
  const mainlandDests = entries.filter(e => MAINLAND_PORTS[e.k]);
  const islandDests   = entries.filter(e => ISLANDS_DATA[e.k]);

  const formatOption = (e) => {
    const durLabel = formatDuration(Math.round(e.cost));
    return `<option value="${e.k}">${e.name} · ${durLabel}</option>`;
  };

  let html = `<option value="">— ${t('planner.choose')} —</option>`;
  if (islandDests.length) {
    html += `<optgroup label="${t('planner.islands')}">${islandDests.map(formatOption).join('')}</optgroup>`;
  }
  if (mainlandDests.length) {
    html += `<optgroup label="${t('planner.mainland')}">${mainlandDests.map(formatOption).join('')}</optgroup>`;
  }
  toSelect.innerHTML = html;
  toSelect.disabled = false;
  if (goBtn) goBtn.disabled = !plannerState.to;
}

const plannerState = { from: '', to: '' };

function runPlannerSearch() {
  const result = document.getElementById('planner-result');
  if (!result) return;
  if (!plannerState.from || !plannerState.to) {
    result.innerHTML = `<div class="planner-msg">${t('planner.pickboth')}</div>`;
    return;
  }
  if (plannerState.from === plannerState.to) {
    result.innerHTML = `<div class="planner-msg">${t('planner.samepoint')}</div>`;
    return;
  }
  const route = findFerryRoute(plannerState.from, plannerState.to);
  if (!route) {
    result.innerHTML = `<div class="planner-msg planner-msg-warn">${t('planner.noroute')}</div>`;
    return;
  }
  // Render route hops
  const hopsHtml = route.hops.map((h, i) => {
    const fromName = i === 0 ? portDisplayName(plannerState.from) : portDisplayName(route.hops[i - 1].to);
    const toName = portDisplayName(h.to);
    const freqLabel = t(`planner.freq.${h.freq}`);
    return `<div class="planner-hop">
      <div class="planner-hop-route">
        <strong>${fromName}</strong>
        <span class="planner-hop-arrow">⛵</span>
        <strong>${toName}</strong>
      </div>
      <div class="planner-hop-meta">
        <span class="planner-hop-dur">⏱ ${formatDuration(h.dur)}</span>
        <span class="planner-hop-freq planner-freq-${h.freq}">${freqLabel}</span>
        <span class="planner-hop-price">€${h.plo}–${h.phi}</span>
      </div>
      <div class="planner-hop-note">${h.note}</div>
    </div>`;
  }).join('');

  const transferText = route.transfers === 0
    ? t('planner.direct')
    : route.transfers === 1
    ? t('planner.onetransfer')
    : `${route.transfers} ${t('planner.transfers')}`;

  result.innerHTML = `
    <div class="planner-summary">
      <div class="planner-summary-stat">
        <span class="planner-stat-num">${formatDuration(route.totalMin)}</span>
        <span class="planner-stat-lbl">${t('planner.totaltime')}</span>
      </div>
      <div class="planner-summary-stat">
        <span class="planner-stat-num">${transferText}</span>
        <span class="planner-stat-lbl">${t('planner.routetype')}</span>
      </div>
      <div class="planner-summary-stat">
        <span class="planner-stat-num">€${route.totalPriceLo}–${route.totalPriceHi}</span>
        <span class="planner-stat-lbl">${t('planner.totalprice')}</span>
      </div>
    </div>
    <div class="planner-hops">${hopsHtml}</div>
    <div class="planner-actions">
      <a class="planner-book-btn" href="${ferryhopperRouteUrl(plannerState.from, plannerState.to)}" target="_blank" rel="noopener">
        🚢 ${t('planner.book')}
      </a>
    </div>
    <div class="planner-disclaimer">${t('planner.disclaimer')}</div>`;
}

const FERRY_ROUTES = [
  // Classic Cyclades triangle
  { from: 'piraeus', to: 'syros', freq: 'high', duration: '~4 hrs', note: 'Daily · ~4 hrs · Blue Star, Golden Star' },
  { from: 'syros', to: 'tinos', freq: 'high', duration: '~30 min', note: '6/week · ~30 min · Fast ferry' },
  { from: 'tinos', to: 'mykonos', freq: 'high', duration: '~20-30 min', note: 'Daily · short fast-ferry hop' },
  { from: 'mykonos', to: 'paros', freq: 'high', duration: '~45 min', note: 'Daily multiple · ~45 min' },
  { from: 'naxos', to: 'paros', freq: 'high', duration: '~30-45 min', note: 'Daily multiple · shortest major Cyclades hop' },

  // Santorini hub
  { from: 'santorini', to: 'mykonos', freq: 'high', duration: '2-3 hrs', note: 'Daily · 2-3 hrs · the iconic Cyclades hop' },
  { from: 'santorini', to: 'ios', freq: 'high', duration: '40-60 min', note: 'Daily · 40-60 min' },
  { from: 'santorini', to: 'naxos', freq: 'high', duration: '1.5-2 hrs', note: 'Daily · 1.5-2 hrs' },
  { from: 'santorini', to: 'milos', freq: 'med', duration: '~3 hrs', note: 'Daily in summer · ~3 hrs' },

  // Dodecanese (routes start/end at Rhodes port, not island centroid)
  { from: 'rhodes', to: 'symi', freq: 'high', duration: '~1 hr', note: 'Daily · ~1 hr · best day trip from Rhodes', useRhodesPort: true },
  { from: 'rhodes', to: 'kos', freq: 'high', duration: '2-3 hrs', note: 'Daily · 2-3 hrs', useRhodesPort: true },

  // Saronic — drawn as one polyline through all 4 ports (Piraeus → Aegina → Poros → Hydra)
  { polyline: ['piraeus', 'aegina', 'poros', 'hydra'], freq: 'high', note: 'Saronic Gulf · 5-12 daily services · Piraeus serves Aegina, Poros, Hydra (and Spetses). Frequent hydrofoils + conventional ferries.' },

  // Sporades — Skiathos/Skopelos/Alonnisos connection
  { polyline: ['skiathos', 'skopelos', 'alonnisos'], freq: 'high', note: 'Sporades · Multiple daily services · Flying Dolphins hydrofoils + Aegean Flying Cat catamarans · Skiathos ~1 hr to Skopelos, ~30 min more to Alonnisos.' },

  // NE Aegean — Lemnos to Agios Efstratios
  { from: 'lemnos', to: 'agios-efstratios', freq: 'low', duration: '~2.5 hrs', note: 'Fast Ferries Adamantios Korais · 2-3/week · ~2.5 hrs · The gateway to the most remote island in the Aegean.' },

  // Small Cyclades loop (Express Skopelitis) — drawn as one polyline
  { polyline: ['naxos', 'iraklia', 'schinoussa', 'koufonisia', 'donousa', 'amorgos'], freq: 'low', note: 'Small Cyclades Lines · Express Skopelitis · 6 days/week (one service per day) · Naxos ↔ Amorgos via Iraklia, Schinoussa, Koufonisi, Donousa' },
];

// Small Cyclades islands (some not in the main islands data - just for the map)
const EXTRA_PORTS = {
  'schinoussa': { name: 'Schinoussa', lat: 36.867, lng: 25.520 },
  'koufonisia': { name: 'Koufonisia', lat: 36.933, lng: 25.597 },
  'donousa': { name: 'Donousa', lat: 36.107, lng: 25.817 },
};

function getPortCoords(key, useRhodesPort) {
  if (key === 'piraeus') return PIRAEUS;
  if (key === 'rhodes' && useRhodesPort) {
    return { ...ISLANDS_DATA['rhodes'], lat: RHODES_PORT.lat, lng: RHODES_PORT.lng };
  }
  if (ISLANDS_DATA[key]) return ISLANDS_DATA[key];
  if (EXTRA_PORTS[key]) return EXTRA_PORTS[key];
  return null;
}

// Active frequency filters for the ferry map (set of 'high','med','low')
const FERRY_MAP_FILTERS = new Set(['high', 'med', 'low']);
let ferryMapInstance = null;
let ferryMapLayer = null;       // LayerGroup holding all current routes + markers

// Generate a slightly curved polyline between two points so routes don't all look like
// straight rulers slicing through landmasses. The curve offsets the midpoint
// perpendicular to the line by a small fraction of the distance.
function curvedRouteCoords(fromLat, fromLng, toLat, toLng, segments = 12) {
  // Midpoint
  const mLat = (fromLat + toLat) / 2;
  const mLng = (fromLng + toLng) / 2;
  // Perpendicular offset — small, scales with distance
  const dLat = toLat - fromLat;
  const dLng = toLng - fromLng;
  const dist = Math.sqrt(dLat * dLat + dLng * dLng);
  // Curve magnitude: ~7% of distance, capped
  const curveAmt = Math.min(dist * 0.07, 0.4);
  // Perpendicular vector (normalize and rotate 90°)
  if (dist < 0.01) return [[fromLat, fromLng], [toLat, toLng]];
  const perpLat = -dLng / dist * curveAmt;
  const perpLng =  dLat / dist * curveAmt;
  // Control point (offset midpoint)
  const cLat = mLat + perpLat;
  const cLng = mLng + perpLng;
  // Sample quadratic Bézier between (from, control, to)
  const out = [];
  for (let i = 0; i <= segments; i++) {
    const t = i / segments;
    const u = 1 - t;
    const lat = u * u * fromLat + 2 * u * t * cLat + t * t * toLat;
    const lng = u * u * fromLng + 2 * u * t * cLng + t * t * toLng;
    out.push([lat, lng]);
  }
  return out;
}

function getFerryPortCoords(key) {
  if (MAINLAND_PORTS[key]) return MAINLAND_PORTS[key];
  // Prefer the explicit port coords for islands when available
  if (ISLAND_FERRY_PORTS[key] && ISLANDS_DATA[key]) {
    return { ...ISLANDS_DATA[key], lat: ISLAND_FERRY_PORTS[key].lat, lng: ISLAND_FERRY_PORTS[key].lng };
  }
  if (ISLANDS_DATA[key])   return ISLANDS_DATA[key];
  if (typeof EXTRA_PORTS !== 'undefined' && EXTRA_PORTS[key]) return EXTRA_PORTS[key];
  return null;
}

function ferryPortDisplayName(key) {
  if (MAINLAND_PORTS[key]) {
    return CURRENT_LANG === 'el' ? MAINLAND_PORTS[key].name_el : MAINLAND_PORTS[key].name;
  }
  if (ISLANDS_DATA[key]) return islandName(key);
  return key;
}

function renderFerryMap() {
  const mapEl = document.getElementById('ferry-map');
  if (!mapEl) return;

  // First time: create map + persistent controls
  if (!mapEl._map) {
    ferryMapInstance = L.map('ferry-map', {
      zoomControl: true, minZoom: 6, maxZoom: 10,
      maxBounds: [[34.5, 19.0], [41.0, 29.5]], maxBoundsViscosity: 0.85
    }).setView([37.5, 25.2], 7);
    mapEl._map = ferryMapInstance;
    addThemeAwareTiles(ferryMapInstance, { maxZoom: 10 });
    L.control.scale({ imperial: false, position: 'bottomleft' }).addTo(ferryMapInstance);

  }

  // Re-draw layer (filter changes call this)
  if (ferryMapLayer) ferryMapLayer.remove();
  ferryMapLayer = L.layerGroup().addTo(ferryMapInstance);

  // Frequency styling — distinct visual tiers
  const freqStyle = {
    high: { color: '#076880', weight: 2.4, opacity: 0.78, dashArray: null },
    med:  { color: '#0B8FAC', weight: 1.9, opacity: 0.62, dashArray: null },
    low:  { color: '#C4962A', weight: 1.6, opacity: 0.65, dashArray: null },
  };

  // Draw all edges in FERRY_GRAPH that pass the filter.
  // If FERRY_FOCUS_PORT is set, only render edges touching that port.
  // Skip edges that are part of a visual polyline — those get drawn separately below.
  const drawnPorts = new Set();
  FERRY_GRAPH.forEach(edge => {
    if (!FERRY_MAP_FILTERS.has(edge.freq)) return;
    if (FERRY_FOCUS_PORT && edge.a !== FERRY_FOCUS_PORT && edge.b !== FERRY_FOCUS_PORT) return;
    // Skip if this edge is a consecutive-stop pair inside a visual polyline
    const edgeKey = [edge.a, edge.b].sort().join('~');
    if (!FERRY_FOCUS_PORT && FERRY_VISUAL_EDGE_SET.has(edgeKey)) {
      // Still record the ports so markers render
      drawnPorts.add(edge.a);
      drawnPorts.add(edge.b);
      return;
    }
    const from = getFerryPortCoords(edge.a);
    const to   = getFerryPortCoords(edge.b);
    if (!from || !to) return;

    const coords = curvedRouteCoords(from.lat, from.lng, to.lat, to.lng);
    const style  = freqStyle[edge.freq] || freqStyle.low;
    const line = L.polyline(coords, {
      color: style.color,
      weight: FERRY_FOCUS_PORT ? style.weight + 0.6 : style.weight,
      opacity: FERRY_FOCUS_PORT ? Math.min(style.opacity + 0.2, 1) : style.opacity,
      dashArray: style.dashArray,
      smoothFactor: 1.2,
    }).addTo(ferryMapLayer);

    const fromName = ferryPortDisplayName(edge.a);
    const toName   = ferryPortDisplayName(edge.b);
    const durLabel = formatDuration(edge.dur);
    const freqLabel = t(`planner.freq.${edge.freq}`);
    const tooltip = `<strong>${fromName} ↔ ${toName}</strong><br>` +
      `<span style="font-size:11px;color:var(--ink-3)">⏱ ${durLabel} · ${freqLabel} · €${edge.plo}–${edge.phi}</span><br>` +
      `<span style="font-size:11px;color:var(--ink-3)">${edge.note}</span>`;
    line.bindTooltip(tooltip, { sticky: true, opacity: 1, className: 'island-tooltip' });

    drawnPorts.add(edge.a);
    drawnPorts.add(edge.b);
  });

  // Draw each visual polyline as one continuous curved path
  if (!FERRY_FOCUS_PORT) {
    FERRY_VISUAL_LINES.forEach(line => {
      if (!FERRY_MAP_FILTERS.has(line.freq)) return;
      const coords = [];
      for (let i = 0; i < line.stops.length - 1; i++) {
        const a = getFerryPortCoords(line.stops[i]);
        const b = getFerryPortCoords(line.stops[i + 1]);
        if (!a || !b) continue;
        const segment = curvedRouteCoords(a.lat, a.lng, b.lat, b.lng, 10);
        if (i === 0) coords.push(...segment);
        else coords.push(...segment.slice(1));     // skip duplicate start point
        drawnPorts.add(line.stops[i]);
        drawnPorts.add(line.stops[i + 1]);
      }
      if (coords.length < 2) return;
      const style = freqStyle[line.freq] || freqStyle.low;
      const polyline = L.polyline(coords, {
        color: style.color,
        weight: style.weight + 0.4,           // slightly thicker so multi-stop reads as one route
        opacity: style.opacity,
        dashArray: style.dashArray,
        smoothFactor: 1.2,
      }).addTo(ferryMapLayer);
      const firstName = ferryPortDisplayName(line.stops[0]);
      const lastName  = ferryPortDisplayName(line.stops[line.stops.length - 1]);
      const stopsLabel = line.stops.map(s => ferryPortDisplayName(s)).join(' → ');
      polyline.bindTooltip(
        `<strong>${firstName} → ${lastName}</strong><br>` +
        `<span style="font-size:11px;color:var(--ink-3)">${stopsLabel}</span>`,
        { sticky: true, opacity: 1, className: 'island-tooltip' }
      );
    });
  }

  // Port markers — different size/colour for mainland vs island.
  // In focus mode: drawnPorts holds the focused port + its neighbours; also render
  // the rest as faint, smaller dots so users can click to switch focus.
  const allPorts = new Set([...Object.keys(MAINLAND_PORTS), ...Object.keys(ISLANDS_DATA)]);
  const portsToRender = FERRY_FOCUS_PORT
    ? new Set([...drawnPorts, ...[...allPorts].filter(k => FERRY_ADJ[k])])
    : drawnPorts;

  portsToRender.forEach(key => {
    const port = getFerryPortCoords(key);
    if (!port) return;
    const portMeta = MAINLAND_PORTS[key];
    const isMainland = !!portMeta && !portMeta.onIsland;
    const isHub = ['piraeus', 'rafina', 'rhodes', 'heraklion', 'mykonos', 'naxos', 'paros'].includes(key);
    const isFocused = FERRY_FOCUS_PORT === key;
    const isInFocus = drawnPorts.has(key);
    // Faint background dot for non-focus ports when in focus mode
    const faded = FERRY_FOCUS_PORT && !isInFocus;

    const marker = L.circleMarker([port.lat, port.lng], {
      radius: isFocused ? 8 : (faded ? 3 : (isHub ? 6 : (isMainland ? 5 : 4))),
      color: isMainland ? '#E8522A' : '#076880',
      fillColor: isMainland ? '#FF6B6B' : '#0B8FAC',
      fillOpacity: faded ? 0.35 : (isFocused ? 1 : 0.95),
      weight: isFocused ? 2.5 : 1.5,
    }).addTo(ferryMapLayer);
    marker.bindTooltip(`<strong>${ferryPortDisplayName(key)}</strong>`, {
      direction: 'top', opacity: 1, className: 'island-tooltip',
    });
    // Click a port: focus on its direct connections (instead of navigating away).
    // Click the same port again, or any non-adjacent port, to clear focus.
    marker.on('click', () => {
      if (FERRY_FOCUS_PORT === key) {
        FERRY_FOCUS_PORT = null;
      } else {
        FERRY_FOCUS_PORT = key;
      }
      renderFerryMap();
    });
  });

  // If a port is focused, render its callout banner above the map
  updateFerryFocusBanner();
}

let FERRY_FOCUS_PORT = null;

function updateFerryFocusBanner() {
  const banner = document.getElementById('ferry-focus-banner');
  if (!banner) return;
  if (!FERRY_FOCUS_PORT) {
    banner.innerHTML = '';
    banner.style.display = 'none';
    return;
  }
  const name = ferryPortDisplayName(FERRY_FOCUS_PORT);
  const isIsland = !!ISLANDS_DATA[FERRY_FOCUS_PORT];
  const directEdges = (FERRY_ADJ[FERRY_FOCUS_PORT] || []).filter(e => FERRY_MAP_FILTERS.has(e.freq));
  const countLabel = directEdges.length === 1
    ? t('hopping.focus.one')
    : `${directEdges.length} ${t('hopping.focus.many')}`;
  const guideBtn = isIsland
    ? `<button class="ferry-focus-btn" onclick="navigateTo('island', '${FERRY_FOCUS_PORT}')">${t('hopping.focus.guide')}</button>`
    : '';
  const bookBtn = isIsland
    ? `<a class="ferry-focus-btn" href="https://www.ferryhopper.com/en/ferries-to/${ferryhopperSlug(FERRY_FOCUS_PORT)}" target="_blank" rel="noopener">${t('detail.bookferry')}</a>`
    : '';
  banner.innerHTML = `
    <div class="ferry-focus-text">
      <strong>${name}</strong>
      <span class="ferry-focus-count">${countLabel}</span>
    </div>
    <div class="ferry-focus-actions">
      ${bookBtn}
      ${guideBtn}
      <button class="ferry-focus-clear" onclick="clearFerryFocus()">${t('hopping.focus.clear')}</button>
    </div>`;
  banner.style.display = 'flex';
}

function clearFerryFocus() {
  FERRY_FOCUS_PORT = null;
  renderFerryMap();
}

// Toggle a frequency on/off and redraw
function toggleFerryMapFilter(freq) {
  if (FERRY_MAP_FILTERS.has(freq)) {
    if (FERRY_MAP_FILTERS.size === 1) return; // never go to zero
    FERRY_MAP_FILTERS.delete(freq);
  } else {
    FERRY_MAP_FILTERS.add(freq);
  }
  document.querySelectorAll('.ferry-filter-btn').forEach(btn => {
    btn.classList.toggle('active', FERRY_MAP_FILTERS.has(btn.dataset.freq));
  });
  renderFerryMap();
}


/* ============================================================
   SUGGESTED ITINERARIES — curated multi-island routes
============================================================ */
const ITINERARIES = [
  {
    title: 'The Classic Cyclades',
    title_el: 'Οι Κλασικές Κυκλάδες',
    duration: '10 days',
    duration_el: '10 μέρες',
    vibe: 'First-time visitor',
    vibe_el: 'Για πρώτη φορά στην Ελλάδα',
    description: 'The quintessential Greek island experience — Athens' + "'" + ' nightlife, Mykonos' + "'" + ' glamour, Santorini' + "'" + 's sunsets and Naxos' + "'" + ' beaches. Hits the must-see islands.',
    description_el: 'Η απόλυτη εμπειρία ελληνικού νησιού — νυχτερινή ζωή Αθήνας, λάμψη Μυκόνου, ηλιοβασιλέματα Σαντορίνης και παραλίες Νάξου. Τα νησιά-σταθμοί.',
    stops: ['piraeus', 'mykonos', 'santorini', 'naxos', 'piraeus'],
    breakdown: [
      { from: 'Athens', from_el: 'Αθήνα', nights: 2, via: 'Fly in', via_el: 'Πτήση εισόδου' },
      { from: 'Mykonos', from_el: 'Μύκονος', nights: 3, via: 'Fast ferry from Piraeus (~3 hrs)', via_el: 'Ταχύπλοο από Πειραιά (~3 ώρες)' },
      { from: 'Santorini', from_el: 'Σαντορίνη', nights: 3, via: 'Fast ferry (2-3 hrs)', via_el: 'Ταχύπλοο (2-3 ώρες)' },
      { from: 'Naxos', from_el: 'Νάξος', nights: 2, via: 'Fast ferry (~1.5 hrs)', via_el: 'Ταχύπλοο (~1,5 ώρα)' },
    ]
  },
  {
    title: 'Quiet Cyclades',
    title_el: 'Ήσυχες Κυκλάδες',
    duration: '10 days',
    duration_el: '10 μέρες',
    vibe: 'Beach & culture, away from crowds',
    vibe_el: 'Παραλία & πολιτισμός, μακριά από πλήθη',
    description: 'The lesser-known Cyclades — Milos for its moon-landscape beaches, Sifnos for food, Folegandros for cliff views. All the water clarity of Santorini, none of the crowds.',
    description_el: 'Οι λιγότερο γνωστές Κυκλάδες — Μήλος για σεληνιακές παραλίες, Σίφνος για φαγητό, Φολέγανδρος για βραχώδεις θέες. Όλη η διαύγεια της Σαντορίνης, χωρίς το πλήθος.',
    stops: ['piraeus', 'milos', 'sifnos', 'folegandros', 'piraeus'],
    breakdown: [
      { from: 'Athens', from_el: 'Αθήνα', nights: 1, via: 'Fly in', via_el: 'Πτήση εισόδου' },
      { from: 'Milos', from_el: 'Μήλος', nights: 4, via: 'Ferry from Piraeus (~3-5 hrs)', via_el: 'Πλοίο από Πειραιά (~3-5 ώρες)' },
      { from: 'Sifnos', from_el: 'Σίφνος', nights: 3, via: 'Ferry (~1 hr)', via_el: 'Πλοίο (~1 ώρα)' },
      { from: 'Folegandros', from_el: 'Φολέγανδρος', nights: 2, via: 'Ferry (~1.5 hrs)', via_el: 'Πλοίο (~1,5 ώρα)' },
    ]
  },
  {
    title: 'Athens + Saronic Week',
    title_el: 'Αθήνα + Εβδομάδα στον Σαρωνικό',
    duration: '7 days',
    duration_el: '7 μέρες',
    vibe: 'Easy, no long ferries',
    vibe_el: 'Εύκολο, χωρίς μεγάλες διαδρομές',
    description: 'Use Athens as a base and hop to the closest islands — Hydra, Poros, Aegina. No long sailings, back to the city most evenings if you want.',
    description_el: 'Χρησιμοποίησε την Αθήνα ως βάση και πήγαινε στα πιο κοντινά νησιά — Ύδρα, Πόρο, Αίγινα. Χωρίς μακρινές διαδρομές, επιστροφή στην πόλη αν θέλεις.',
    stops: ['piraeus', 'aegina', 'poros', 'hydra', 'piraeus'],
    breakdown: [
      { from: 'Athens', from_el: 'Αθήνα', nights: 3, via: 'Fly in · Acropolis, museums', via_el: 'Πτήση εισόδου · Ακρόπολη, μουσεία' },
      { from: 'Aegina', from_el: 'Αίγινα', nights: 1, via: 'Hydrofoil (40 min)', via_el: 'Δελφίνι (40 λεπτά)' },
      { from: 'Poros', from_el: 'Πόρος', nights: 1, via: 'Hydrofoil (~1 hr)', via_el: 'Δελφίνι (~1 ώρα)' },
      { from: 'Hydra', from_el: 'Ύδρα', nights: 2, via: 'Hydrofoil (~30 min from Poros)', via_el: 'Δελφίνι (~30 λεπτά από Πόρο)' },
    ]
  },
  {
    title: 'Dodecanese Highlights',
    title_el: 'Κορυφαίες Στιγμές Δωδεκανήσων',
    duration: '10 days',
    duration_el: '10 μέρες',
    vibe: 'History + beaches',
    vibe_el: 'Ιστορία + παραλίες',
    description: 'Rhodes for medieval Europe, Symi for the most beautiful harbour in Greece, Kos for long sandy beaches and Hippocrates, Patmos for St John' + "'" + 's cave.',
    description_el: 'Ρόδος για μεσαιωνική Ευρώπη, Σύμη για το ομορφότερο λιμάνι της Ελλάδας, Κως για μεγάλες αμμουδιές και Ιπποκράτη, Πάτμος για τη σπηλιά του Ιωάννη.',
    stops: ['rhodes', 'symi', 'kos', 'patmos'],
    breakdown: [
      { from: 'Rhodes', from_el: 'Ρόδος', nights: 3, via: 'Fly direct to Rhodes', via_el: 'Απευθείας πτήση στη Ρόδο' },
      { from: 'Symi', from_el: 'Σύμη', nights: 2, via: 'Day ferry from Rhodes (~1 hr)', via_el: 'Πλοίο ημέρας από Ρόδο (~1 ώρα)' },
      { from: 'Kos', from_el: 'Κως', nights: 3, via: 'Ferry (2-3 hrs)', via_el: 'Πλοίο (2-3 ώρες)' },
      { from: 'Patmos', from_el: 'Πάτμος', nights: 2, via: 'Ferry (~3 hrs)', via_el: 'Πλοίο (~3 ώρες)' },
    ]
  },
  {
    title: 'The Small Cyclades Escape',
    title_el: 'Απόδραση στις Μικρές Κυκλάδες',
    duration: '9 days',
    duration_el: '9 μέρες',
    vibe: 'Off-grid, simple, beachy',
    vibe_el: 'Εκτός δικτύου, απλό, παραλιακό',
    description: 'The tiny islands the Express Skopelitis connects — places where life hasn' + "'" + 't changed much in decades. Perfect beaches, no resorts, basic tavernas, total peace.',
    description_el: 'Τα μικρά νησιά που συνδέει ο Εξπρές Σκοπελίτης — μέρη όπου η ζωή δεν έχει αλλάξει εδώ και δεκαετίες. Υπέροχες παραλίες, ούτε ένα ρεσόρτ, ταβερνάκια, απόλυτη ηρεμία.',
    stops: ['naxos', 'koufonisia', 'amorgos'],
    breakdown: [
      { from: 'Naxos', from_el: 'Νάξος', nights: 3, via: 'Fast ferry from Piraeus (3.5 hrs)', via_el: 'Ταχύπλοο από Πειραιά (3,5 ώρες)' },
      { from: 'Koufonisia', from_el: 'Κουφονήσια', nights: 2, via: 'Skopelitis (~2.5 hrs via Iraklia, Schinoussa)', via_el: 'Σκοπελίτης (~2,5 ώρες μέσω Ηρακλειάς, Σχοινούσας)' },
      { from: 'Amorgos', from_el: 'Αμοργός', nights: 3, via: 'Skopelitis (~2 hrs via Donousa)', via_el: 'Σκοπελίτης (~2 ώρες μέσω Δονούσας)' },
      { from: 'Return', from_el: 'Επιστροφή', nights: 1, via: 'Blue Star back to Piraeus or via Paros', via_el: 'Blue Star επιστροφή στον Πειραιά ή μέσω Πάρου' },
    ]
  },
  {
    title: 'Classic Cyclades Triangle',
    title_el: 'Κλασικό Τρίγωνο Κυκλάδων',
    duration: '11 days',
    duration_el: '11 μέρες',
    vibe: 'Slow pace, Cycladic architecture',
    vibe_el: 'Αργός ρυθμός, κυκλαδίτικη αρχιτεκτονική',
    description: 'The original Cyclades connection — Syros, Tinos and Mykonos. Ermoupolis on Syros is the most beautiful town in the Aegean. Tinos has 1000 chapels. Then Mykonos for the full contrast.',
    description_el: 'Η αρχική σύνδεση των Κυκλάδων — Σύρος, Τήνος και Μύκονος. Η Ερμούπολη της Σύρου είναι η πιο όμορφη πόλη του Αιγαίου. Η Τήνος έχει 1000 εκκλησάκια. Μετά η Μύκονος για την πλήρη αντίθεση.',
    stops: ['piraeus', 'syros', 'tinos', 'mykonos', 'piraeus'],
    breakdown: [
      { from: 'Athens', from_el: 'Αθήνα', nights: 1, via: 'Fly in', via_el: 'Πτήση εισόδου' },
      { from: 'Syros', from_el: 'Σύρος', nights: 3, via: 'Ferry (~2-4 hrs)', via_el: 'Πλοίο (~2-4 ώρες)' },
      { from: 'Tinos', from_el: 'Τήνος', nights: 3, via: 'Ferry (~30 min)', via_el: 'Πλοίο (~30 λεπτά)' },
      { from: 'Mykonos', from_el: 'Μύκονος', nights: 3, via: 'Ferry (~20-30 min)', via_el: 'Πλοίο (~20-30 λεπτά)' },
      { from: 'Return', from_el: 'Επιστροφή', nights: 1, via: 'Fast ferry to Piraeus (~3 hrs)', via_el: 'Ταχύπλοο στον Πειραιά (~3 ώρες)' },
    ]
  },
  {
    title: 'Santorini + Milos',
    title_el: 'Σαντορίνη + Μήλος',
    duration: '8 days',
    duration_el: '8 μέρες',
    vibe: 'Two extraordinary islands',
    vibe_el: 'Δύο εξαιρετικά νησιά',
    description: 'The two most photogenic islands in Greece paired together — Santorini for the caldera, Milos for the lunar beaches. Very different, both unmissable.',
    description_el: 'Τα δύο πιο φωτογενή νησιά της Ελλάδας μαζί — Σαντορίνη για την καλντέρα, Μήλος για τις σεληνιακές παραλίες. Πολύ διαφορετικά, και τα δύο αναντικατάστατα.',
    stops: ['santorini', 'milos'],
    breakdown: [
      { from: 'Athens', from_el: 'Αθήνα', nights: 1, via: 'Fly in', via_el: 'Πτήση εισόδου' },
      { from: 'Santorini', from_el: 'Σαντορίνη', nights: 4, via: 'Fly direct or fast ferry (~5 hrs)', via_el: 'Απευθείας πτήση ή ταχύπλοο (~5 ώρες)' },
      { from: 'Milos', from_el: 'Μήλος', nights: 3, via: 'Daily summer ferry (~3 hrs)', via_el: 'Καθημερινό θερινό πλοίο (~3 ώρες)' },
    ]
  },
  {
    title: 'Rhodes + Symi',
    title_el: 'Ρόδος + Σύμη',
    duration: '7 days',
    duration_el: '7 μέρες',
    vibe: 'Easy pair, one flight',
    vibe_el: 'Εύκολο ζεύγος, μια πτήση',
    description: 'The simplest Dodecanese combination — fly into Rhodes, three nights in the old town, then a quick ferry to Symi for three nights in the painted harbour. One flight, one ferry.',
    description_el: 'Ο πιο απλός συνδυασμός Δωδεκανήσων — πτήση στη Ρόδο, τρία βράδια στην παλιά πόλη, μετά γρήγορο πλοίο στη Σύμη για τρία βράδια στο πολύχρωμο λιμάνι. Μία πτήση, ένα πλοίο.',
    stops: ['rhodes', 'symi'],
    breakdown: [
      { from: 'Rhodes', from_el: 'Ρόδος', nights: 4, via: 'Fly direct · Old Town, Lindos, Kallithea', via_el: 'Απευθείας πτήση · Παλιά Πόλη, Λίνδος, Καλλιθέα' },
      { from: 'Symi', from_el: 'Σύμη', nights: 3, via: 'Daily ferry from Rhodes port (~1 hr)', via_el: 'Καθημερινό πλοίο από λιμάνι Ρόδου (~1 ώρα)' },
    ]
  },
  {
    title: 'The Other Aegean (Sporades)',
    title_el: 'Το Άλλο Αιγαίο (Σποράδες)',
    duration: '9 days',
    duration_el: '9 μέρες',
    vibe: 'Pine forests, green coastline',
    vibe_el: 'Πευκοδάση, καταπράσινες ακτές',
    description: 'The Sporades — an entirely different kind of Aegean island. Pine forest running to the sea, no whitewashed cubes, lush green hills. Alonnisos is the heart of the National Marine Park, where monk seals live. Very different from anything in the Cyclades.',
    description_el: 'Οι Σποράδες — εντελώς διαφορετικό είδος νησιού Αιγαίου. Πευκοδάση που κατεβαίνουν στη θάλασσα, καθόλου κυβάκια λευκά, κατάπρασινοι λόφοι. Η Αλόννησος είναι το κέντρο του Θαλάσσιου Πάρκου, όπου ζουν οι φώκιες μοναχούς. Πολύ διαφορετικό από οτιδήποτε στις Κυκλάδες.',
    stops: ['skiathos', 'skopelos', 'alonnisos'],
    breakdown: [
      { from: 'Skiathos', from_el: 'Σκιάθος', nights: 3, via: 'Fly direct · sandy beaches, lively town', via_el: 'Απευθείας πτήση · αμμουδιές, ζωντανή πόλη' },
      { from: 'Skopelos', from_el: 'Σκόπελος', nights: 3, via: 'Frequent ferries (~1 hr) · Mamma Mia filming location', via_el: 'Συχνά πλοία (~1 ώρα) · τοποθεσία γυρισμάτων Mamma Mia' },
      { from: 'Alonnisos', from_el: 'Αλόννησος', nights: 3, via: 'Ferry from Skopelos (~30 min) · marine park, snorkelling', via_el: 'Πλοίο από Σκόπελο (~30 λεπτά) · θαλάσσιο πάρκο, κατάδυση' },
    ]
  },
  {
    title: 'Ultimate Off the Beaten Path',
    title_el: 'Η Απόλυτη Εκτός Πεπατημένης',
    duration: '7 days',
    duration_el: '7 μέρες',
    vibe: 'True island isolation',
    vibe_el: 'Πραγματική νησιωτική απομόνωση',
    description: 'For travellers who have already done Santorini and Mykonos. Lemnos is Greece' + "'" + 's underrated northern island — long empty beaches, wine traditions, military history. Agios Efstratios has 270 residents, no cars, black volcanic sand beaches and the oak forest of the Aegean. No crowds because no one comes.',
    description_el: 'Για ταξιδιώτες που έχουν ήδη επισκεφτεί Σαντορίνη και Μύκονο. Η Λήμνος είναι το υποτιμημένο βόρειο νησί της Ελλάδας — μακριές άδειες παραλίες, παραδόσεις κρασιού, στρατιωτική ιστορία. Ο Άγιος Ευστράτιος έχει 270 κατοίκους, κανένα αυτοκίνητο, μαύρες ηφαιστειακές παραλίες και το δάσος βελανιδιάς του Αιγαίου. Ούτε ένα πλήθος γιατί δεν έρχεται κανείς.',
    stops: ['lemnos', 'agios-efstratios'],
    breakdown: [
      { from: 'Athens', from_el: 'Αθήνα', nights: 1, via: 'Fly in', via_el: 'Πτήση εισόδου' },
      { from: 'Lemnos', from_el: 'Λήμνος', nights: 4, via: 'Fly direct (~1 hr) · beaches, wine villages', via_el: 'Απευθείας πτήση (~1 ώρα) · παραλίες, χωριά κρασιού' },
      { from: 'Agios Efstratios', from_el: 'Άγιος Ευστράτιος', nights: 2, via: 'Ferry from Lemnos (~2-3 hrs) · true isolation', via_el: 'Πλοίο από Λήμνο (~2-3 ώρες) · πραγματική απομόνωση' },
    ]
  },
];

function renderItineraries() {
  const container = document.getElementById('hopping-list');
  if (!container) return;
  
  container.innerHTML = ITINERARIES.map((it, idx) => {
    const stopsLine = it.breakdown.map(b => {
      const fromText = pickLang(b, 'from');
      const viaText = pickLang(b, 'via');
      const nightsLabel = b.nights === 1 ? t('hopping.night') : t('hopping.nights');
      return `<div class="itin-leg"><div class="itin-leg-place"><strong>${fromText}</strong> <span class="itin-nights">${b.nights} ${nightsLabel}</span></div><div class="itin-leg-via">${viaText}</div></div>`;
    }).join('');

    const islandKeys = it.stops.filter(s => s !== 'piraeus' && ISLANDS_DATA[s]);
    const islandLinks = islandKeys.map(k =>
      `<a class="itin-island-link" href="#island/${k}" onclick="event.preventDefault();navigateTo('island','${k}')">${islandName(k)}</a>`
    ).join(' · ');

    return `
      <div class="itin-card">
        <div class="itin-card-header">
          <div>
            <h3 class="itin-title">${pickLang(it, 'title')}</h3>
            <div class="itin-meta">
              <span class="itin-duration">⏱ ${pickLang(it, 'duration')}</span>
              <span class="itin-vibe">${pickLang(it, 'vibe')}</span>
            </div>
          </div>
        </div>
        <p class="itin-desc">${pickLang(it, 'description')}</p>
        <div class="itin-legs">${stopsLine}</div>
        ${islandLinks ? `<div class="itin-links">${t('hopping.visit')} ${islandLinks}</div>` : ''}
      </div>
    `;
  }).join('');
}

function renderHopping() {
  renderFerryMap();
  renderItineraries();
}

/* ============================================================
   INTERNATIONAL ESCAPES — ferry routes to Turkey & Albania
============================================================ */

// Foreign ports (not in ISLANDS_DATA)
// rating: 1-5 how worth visiting. context: single-sentence insider summary
const FOREIGN_PORTS = {
  'saranda': {
    name: 'Saranda', name_el: 'Αγ. Σαράντα',
    country: 'Albania', country_el: 'Αλβανία',
    lat: 39.8753, lng: 20.0056,
    rating: 4,
    context: 'Mediocre seafront town, but the gateway to Butrint UNESCO site (30 min south) and the Ksamil beaches — among the best in the Balkans.',
    context_el: 'Μέτρια παραλιακή πόλη, αλλά πύλη για τον αρχαιολογικό χώρο UNESCO της Βουθρωτής (30 λεπτά νότια) και τις παραλίες Ksamil — από τις καλύτερες στα Βαλκάνια.',
  },
  'ayvalik': {
    name: 'Ayvalık', name_el: 'Αϊβαλί',
    country: 'Turkey', country_el: 'Τουρκία',
    lat: 39.3095, lng: 26.6930,
    rating: 4,
    context: 'Beautiful old Greek-Ottoman town with preserved 19th-century stone houses. Base for day trips to ancient Pergamon.',
    context_el: 'Όμορφη παλιά ελληνοτουρκική πόλη με διατηρημένες πέτρινες κατοικίες του 19ου αιώνα. Βάση για εκδρομές στην αρχαία Πέργαμο.',
  },
  'cesme': {
    name: 'Çeşme', name_el: 'Τσεσμές',
    country: 'Turkey', country_el: 'Τουρκία',
    lat: 38.3236, lng: 26.3042,
    rating: 3,
    context: 'Upscale beach resort with an Ottoman fortress, thermal springs, and some of the best windsurfing in the Aegean. Lively but touristy in summer.',
    context_el: 'Κοσμοπολίτικο θέρετρο με οθωμανικό κάστρο, ιαματικές πηγές, και από το καλύτερο windsurfing του Αιγαίου. Ζωντανό αλλά τουριστικό το καλοκαίρι.',
  },
  'kusadasi': {
    name: 'Kuşadası', name_el: 'Κουσάντασι',
    country: 'Turkey', country_el: 'Τουρκία',
    lat: 37.8600, lng: 27.2561,
    rating: 4,
    context: 'Main gateway to Ephesus (18 km inland) — one of the most important ancient cities in the world. The town itself is packed with cruise-ship crowds.',
    context_el: 'Η κύρια πύλη για την Έφεσο (18 χλμ εσωτερικά) — μία από τις σημαντικότερες αρχαίες πόλεις στον κόσμο. Η ίδια η πόλη γεμάτη κρουαζιερόπλοια.',
  },
  'seferihisar': {
    name: 'Seferihisar', name_el: 'Σεφέριχισαρ',
    country: 'Turkey', country_el: 'Τουρκία',
    lat: 38.1962, lng: 26.8379,
    rating: 3,
    context: 'Turkey\'s first official "Slow Food" town. Beautiful Sigacik marina, a restored citadel, and the ruins of ancient Teos nearby.',
    context_el: 'Η πρώτη επίσημη "Slow Food" πόλη της Τουρκίας. Όμορφη μαρίνα Sigacik, αναπαλαιωμένη ακρόπολη, και τα ερείπια της αρχαίας Τέω κοντά.',
  },
  'bodrum': {
    name: 'Bodrum', name_el: 'Μπόντρουμ',
    country: 'Turkey', country_el: 'Τουρκία',
    lat: 37.0344, lng: 27.4305,
    rating: 5,
    context: 'The most beautiful port town on the Turkish Aegean — a crusader Castle of St Peter dominates the harbor, the old town is whitewashed, the nightlife is legendary. Halicarnassus was here.',
    context_el: 'Η πιο όμορφη παραλιακή πόλη του τουρκικού Αιγαίου — το σταυροφορικό Κάστρο του Αγίου Πέτρου δεσπόζει στο λιμάνι, η παλιά πόλη είναι ασπρισμένη, η νυχτερινή ζωή θρυλική. Η Αλικαρνασσός ήταν εδώ.',
  },
  'turgutreis': {
    name: 'Turgutreis', name_el: 'Τουργκούτ',
    country: 'Turkey', country_el: 'Τουρκία',
    lat: 37.0164, lng: 27.2556,
    rating: 3,
    context: 'Quieter beach town on the Bodrum peninsula with a long sandy beach and one of Turkey\'s best sunset viewpoints.',
    context_el: 'Πιο ήσυχη παραλιακή πόλη στη χερσόνησο του Μπόντρουμ με μεγάλη αμμουδιά και από τα καλύτερα ηλιοβασιλέματα της Τουρκίας.',
  },
  'marmaris': {
    name: 'Marmaris', name_el: 'Μαρμαρίς',
    country: 'Turkey', country_el: 'Τουρκία',
    lat: 36.8550, lng: 28.2700,
    rating: 3,
    context: 'Large resort town with a pretty harbor and pine-wooded bay. Best used as a gateway to the Dalyan mud baths or the Lycian coast.',
    context_el: 'Μεγάλο θέρετρο με γραφικό λιμάνι και πευκόφυτο κόλπο. Καλύτερη χρήση ως πύλη για τις λουτροθεραπείες Dalyan ή την ακτή της Λυκίας.',
  },
  'fethiye': {
    name: 'Fethiye', name_el: 'Φετχιγιέ',
    country: 'Turkey', country_el: 'Τουρκία',
    lat: 36.6214, lng: 29.1128,
    rating: 5,
    context: 'Stunning harbor town and gateway to Ölüdeniz lagoon — one of the most photographed beaches in the world — and the 540 km Lycian Way hiking trail.',
    context_el: 'Εκπληκτική παραλιακή πόλη και πύλη για τη λιμνοθάλασσα Ölüdeniz — μία από τις πιο φωτογραφημένες παραλίες στον κόσμο — και το μονοπάτι Lycian Way.',
  },
  'kas': {
    name: 'Kaş', name_el: 'Κας',
    country: 'Turkey', country_el: 'Τουρκία',
    lat: 36.2020, lng: 29.6420,
    rating: 5,
    context: 'Charming bohemian Lycian town with Greek-style architecture, reachable only by winding coastal road. Incredible diving and paragliding. Kastellorizo visible from the harbor.',
    context_el: 'Γοητευτική μποέμικη Λυκιακή πόλη με ελληνικού τύπου αρχιτεκτονική, προσβάσιμη μόνο μέσω κυκλικού παραλιακού δρόμου. Εκπληκτικές καταδύσεις και paragliding. Το Καστελλόριζο φαίνεται από το λιμάνι.',
  },
  'datca': {
    name: 'Datça', name_el: 'Ντατσά',
    country: 'Turkey', country_el: 'Τουρκία',
    lat: 36.7310, lng: 27.6844,
    rating: 4,
    context: 'Peaceful peninsula town, "where Aegean meets Mediterranean." Ancient Knidos ruins at the peninsula\'s tip, almond groves, uncrowded beaches.',
    context_el: 'Ήσυχη πόλη σε χερσόνησο, "όπου το Αιγαίο συναντά τη Μεσόγειο." Τα ερείπια της αρχαίας Κνίδου στην άκρη της χερσονήσου, αμυγδαλιές, άδειες παραλίες.',
  },
};

const INTERNATIONAL_ROUTES = [
  // Corfu ↔ Saranda (Albania)
  {
    from: 'corfu', to: 'saranda',
    country: 'Albania', country_el: 'Αλβανία',
    duration: '30–90 min', duration_el: '30–90 λεπτά',
    frequency: 'high',
    frequency_label: 'Up to 30 daily in summer', frequency_label_el: 'Έως 30 ημερησίως το καλοκαίρι',
    price: '€15–€25',
    operators: 'Finikas Lines · Ionian Seaways · Albania Luxury Ferries',
    note: 'Day trip to Butrint UNESCO ruins or Ksamil beaches. No rental cars allowed on the crossing.',
    note_el: 'Μονοήμερη για τα ερείπια UNESCO της Βουθρωτής ή τις παραλίες του Ξαμίλ. Δεν επιτρέπονται τα ενοικιαζόμενα αυτοκίνητα στο πέρασμα.',
  },
  // Lesvos ↔ Ayvalık
  {
    from: 'lesvos', to: 'ayvalik',
    country: 'Turkey', country_el: 'Τουρκία',
    duration: '90 min', duration_el: '90 λεπτά',
    frequency: 'med',
    frequency_label: 'Daily in summer', frequency_label_el: 'Καθημερινά το καλοκαίρι',
    price: '€25–€45',
    operators: 'Jale Tour · Turyol',
    note: 'Closest port to ancient Pergamon and the Aeolian coast.',
    note_el: 'Το πλησιέστερο λιμάνι στην αρχαία Πέργαμο και στην Αιολική ακτή.',
  },
  // Chios ↔ Çeşme
  {
    from: 'chios', to: 'cesme',
    country: 'Turkey', country_el: 'Τουρκία',
    duration: '45 min', duration_el: '45 λεπτά',
    frequency: 'high',
    frequency_label: 'Multiple daily in summer', frequency_label_el: 'Πολλά ημερησίως το καλοκαίρι',
    price: '€25–€35',
    operators: 'ERTURK · Miniotis Lines · Turyol',
    note: 'Çeşme is a resort town 85 km from İzmir — continue by bus/train to Ephesus.',
    note_el: 'Το Çeşme είναι τουριστικό θέρετρο, 85 χλμ από τη Σμύρνη — συνεχίστε με λεωφορείο στην Έφεσο.',
  },
  // Samos ↔ Kuşadası
  {
    from: 'samos', to: 'kusadasi',
    country: 'Turkey', country_el: 'Τουρκία',
    duration: '90 min', duration_el: '90 λεπτά',
    frequency: 'high',
    frequency_label: 'Daily in summer, 4-5/week in shoulder', frequency_label_el: 'Καθημερινά το καλοκαίρι',
    price: '€35–€55',
    operators: 'Meander Travel · Sea Dreams',
    note: 'Kuşadası is the gateway to Ephesus — one of the most important ancient sites in the world. Day trip doable but tight.',
    note_el: 'Το Κουσάντασι είναι η πύλη για την Έφεσο — από τους σημαντικότερους αρχαιολογικούς χώρους.',
  },
  // Samos ↔ Seferihisar (new route)
  {
    from: 'samos', to: 'seferihisar',
    country: 'Turkey', country_el: 'Τουρκία',
    duration: '60 min', duration_el: '60 λεπτά',
    frequency: 'med',
    frequency_label: '~7/week in summer', frequency_label_el: '~7 εβδομαδιαίως το καλοκαίρι',
    price: '€30',
    operators: 'Sunrise Lines',
    note: 'Newer route. Seferihisar is a slow-food certified town, great for food travelers.',
    note_el: 'Πιο πρόσφατη διαδρομή. Το Seferihisar είναι slow-food πόλη, ιδανική για γαστρονομικά ταξίδια.',
  },
  // Kos ↔ Bodrum
  {
    from: 'kos', to: 'bodrum',
    country: 'Turkey', country_el: 'Τουρκία',
    duration: '30 min', duration_el: '30 λεπτά',
    frequency: 'high',
    frequency_label: 'Multiple daily in summer', frequency_label_el: 'Πολλά ημερησίως το καλοκαίρι',
    price: '€25–€45',
    operators: 'Bodrum Express Lines · Yeşil Marmaris',
    note: 'Shortest Greek-Turkey crossing. Bodrum has the Castle of St Peter, Halicarnassus ruins, and great nightlife.',
    note_el: 'Η συντομότερη διαδρομή Ελλάδας-Τουρκίας. Το Μπόντρουμ έχει το Κάστρο του Αγίου Πέτρου και τα ερείπια της Αλικαρνασσού.',
  },
  // Kos ↔ Turgutreis
  {
    from: 'kos', to: 'turgutreis',
    country: 'Turkey', country_el: 'Τουρκία',
    duration: '30 min', duration_el: '30 λεπτά',
    frequency: 'low',
    frequency_label: 'Seasonal — check before booking', frequency_label_el: 'Εποχιακό — ελέγξτε πριν κλείσετε',
    price: '€21',
    operators: 'Bodrum Express Lines',
    note: 'Smaller port than Bodrum, reaches the quieter Bodrum peninsula villages.',
    note_el: 'Μικρότερο λιμάνι από το Μπόντρουμ, οδηγεί στα πιο ήσυχα χωριά της χερσονήσου.',
  },
  // Rhodes ↔ Marmaris
  {
    from: 'rhodes', to: 'marmaris',
    country: 'Turkey', country_el: 'Τουρκία',
    duration: '50 min (hydrofoil) – 2h', duration_el: '50 λεπτά (ιπτάμενο) – 2 ώρες',
    frequency: 'high',
    frequency_label: '5-7 crossings per week', frequency_label_el: '5-7 δρομολόγια ανά εβδομάδα',
    price: '€45–€65',
    operators: 'Yeşil Marmaris · Sky Marine',
    note: 'Marmaris is a resort town with a fine old quarter and fast access to the Lycian coast.',
    note_el: 'Το Μαρμαρίς είναι τουριστικό θέρετρο με ωραία παλιά πόλη και εύκολη πρόσβαση στη Λυκιακή ακτή.',
  },
  // Rhodes ↔ Fethiye
  {
    from: 'rhodes', to: 'fethiye',
    country: 'Turkey', country_el: 'Τουρκία',
    duration: '1h 40min', duration_el: '1 ώρα 40 λεπτά',
    frequency: 'med',
    frequency_label: '1-2 daily in summer', frequency_label_el: '1-2 ημερησίως το καλοκαίρι',
    price: '€35–€55',
    operators: 'Yeşil Marmaris · Sky Marine',
    note: 'Fethiye is the gateway to the Lycian Way hiking trail and Ölüdeniz beach.',
    note_el: 'Το Fethiye είναι η είσοδος στο μονοπάτι Lycian Way και στην παραλία Ölüdeniz.',
  },
  // Rhodes ↔ Bodrum
  {
    from: 'rhodes', to: 'bodrum',
    country: 'Turkey', country_el: 'Τουρκία',
    duration: '2h', duration_el: '2 ώρες',
    frequency: 'med',
    frequency_label: '3-5 per week in summer', frequency_label_el: '3-5 ανά εβδομάδα το καλοκαίρι',
    price: '€55',
    operators: 'Yeşil Marmaris',
    note: 'Seasonal route — summer only.',
    note_el: 'Εποχιακή διαδρομή — μόνο το καλοκαίρι.',
  },
  // Symi ↔ Datça
  {
    from: 'symi', to: 'datca',
    country: 'Turkey', country_el: 'Τουρκία',
    duration: '1h 30min', duration_el: '1,5 ώρα',
    frequency: 'low',
    frequency_label: '2-3 per week in summer', frequency_label_el: '2-3 ανά εβδομάδα το καλοκαίρι',
    price: '€45',
    operators: 'Datça Seyahat',
    note: 'Datça is a peaceful peninsula on the way to the ancient city of Knidos.',
    note_el: 'Το Datça είναι ήρεμη χερσόνησος που οδηγεί στην αρχαία πόλη Κνίδο.',
  },
  // Kastellorizo ↔ Kaş
  {
    from: 'kastellorizo', to: 'kas',
    country: 'Turkey', country_el: 'Τουρκία',
    duration: '20 min', duration_el: '20 λεπτά',
    frequency: 'high',
    frequency_label: 'Daily in summer', frequency_label_el: 'Καθημερινά το καλοκαίρι',
    price: '€20–€35',
    operators: 'Meis Express',
    note: 'Shortest and one of the oldest Greek-Turkish crossings. Kastellorizo lies literally opposite the Turkish coast.',
    note_el: 'Η συντομότερη και μία από τις παλιότερες διαδρομές. Το Καστελλόριζο βρίσκεται ακριβώς απέναντι από την τουρκική ακτή.',
  },
];

function renderInternational() {
  renderInternationalMap();
  renderInternationalList();
}

let internationalMapInstance = null;

function renderInternationalMap() {
  const container = document.getElementById('international-map');
  if (!container) return;

  // Clean up any prior Leaflet instance before re-creating
  if (internationalMapInstance) {
    try { internationalMapInstance.remove(); } catch(e) {}
    internationalMapInstance = null;
  }
  container.innerHTML = '';

  const map = L.map(container, {
    zoomControl: true,
    attributionControl: true,
    minZoom: 6, maxZoom: 10,
  }).setView([38.5, 26.0], 6);
  internationalMapInstance = map;

  if (typeof addThemeAwareTiles === 'function') {
    addThemeAwareTiles(map, { attribution: '© OpenStreetMap · CARTO' });
  } else {
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
      subdomains: 'abcd',
      attribution: '© OpenStreetMap · CARTO',
    }).addTo(map);
  }

  // Frequency → line style
  const STYLES = {
    high: { color: '#0B8FAC', weight: 4, opacity: 0.9 },
    med:  { color: '#FF6B6B', weight: 3, opacity: 0.9 },
    low:  { color: '#C4962A', weight: 2.5, opacity: 0.85, dashArray: '6, 4' },
  };

  // For multi-port islands, use the actual ferry port coordinate (not the island centroid).
  // This matters for large islands where ferries depart from a specific town.
  const PORT_OVERRIDES = {
    'rhodes': { lat: 36.4512, lng: 28.2244 },  // Rhodes Town commercial port (Akandia / Mandraki)
    'lesvos': { lat: 39.1080, lng: 26.5543 },  // Mytilene port
    'symi':   { lat: 36.6167, lng: 27.8394 },  // Yialos port (Symi town)
    'samos':  { lat: 37.754,  lng: 26.977 },   // Vathi (Samos Town) — already the main coord
    'kos':    { lat: 36.8936, lng: 27.2925 },  // Kos Town port
    'chios':  { lat: 38.3696, lng: 26.1356 },  // Chios Town port
    'corfu':  { lat: 39.6270, lng: 19.9212 },  // Corfu New Port
    'kastellorizo': { lat: 36.1455, lng: 29.5928 },
  };

  const portCoord = (key) => {
    const o = PORT_OVERRIDES[key];
    if (o) return [o.lat, o.lng];
    const isl = ISLANDS_DATA[key];
    return isl ? [isl.lat, isl.lng] : null;
  };

  // Draw each route
  INTERNATIONAL_ROUTES.forEach(r => {
    const from = portCoord(r.from);
    const to = FOREIGN_PORTS[r.to];
    if (!from || !to) return;
    const line = L.polyline(
      [from, [to.lat, to.lng]],
      STYLES[r.frequency] || STYLES.med
    ).addTo(map);
    line.bindTooltip(
      `<div style="font-family:sans-serif;font-size:12px;min-width:180px">
        <div style="font-weight:700;color:var(--ink-1)">${islandName(r.from)} ↔ ${pickLang(to, 'name')}</div>
        <div style="color:var(--ink-3);margin-top:2px">${pickLang(r, 'duration')} · ${pickLang(r, 'frequency_label')}</div>
        <div style="color:var(--aegean);font-weight:600;margin-top:2px">${r.price}</div>
      </div>`,
      { sticky: true }
    );
  });

  // Greek island markers (clickable → island page)
  const greekPorts = new Set(INTERNATIONAL_ROUTES.map(r => r.from));
  greekPorts.forEach(key => {
    const coord = portCoord(key);
    if (!coord) return;
    const marker = L.circleMarker(coord, {
      radius: 8,
      fillColor: '#0B8FAC',
      color: '#fff',
      weight: 2,
      opacity: 1,
      fillOpacity: 1,
    }).addTo(map);
    marker.bindTooltip(`🇬🇷 ${islandName(key)}`, { permanent: false, direction: 'top' });
    marker.on('click', () => navigateTo('island', key));
  });

  // Foreign port markers (not clickable)
  Object.entries(FOREIGN_PORTS).forEach(([key, port]) => {
    // Only draw ports that appear in routes
    if (!INTERNATIONAL_ROUTES.some(r => r.to === key)) return;
    const flag = port.country === 'Albania' ? '🇦🇱' : '🇹🇷';
    L.circleMarker([port.lat, port.lng], {
      radius: 7,
      fillColor: '#C0522A',
      color: '#fff',
      weight: 2,
      opacity: 1,
      fillOpacity: 1,
    }).bindTooltip(`${flag} ${pickLang(port, 'name')}, ${pickLang(port, 'country')}`, { direction: 'top' }).addTo(map);
  });
}

function renderInternationalList() {
  const container = document.getElementById('international-list');
  if (!container) return;

  // Group routes by country
  const albaniaRoutes = INTERNATIONAL_ROUTES.filter(r => r.country === 'Albania');
  const turkeyRoutes = INTERNATIONAL_ROUTES.filter(r => r.country === 'Turkey');

  const renderRoute = (r) => {
    const from = ISLANDS_DATA[r.from];
    const to = FOREIGN_PORTS[r.to];
    if (!from || !to) return '';
    const flag = r.country === 'Albania' ? '🇦🇱' : '🇹🇷';
    const freqClass = r.frequency === 'high' ? 'freq-high' : r.frequency === 'med' ? 'freq-med' : 'freq-low';
    const rating = to.rating || 0;
    const stars = Array.from({length: 5}, (_, i) =>
      `<span class="intl-star ${i < rating ? 'on' : ''}">★</span>`
    ).join('');
    // Ferryhopper search-URL pattern (works as search prefill)
    const ferryhopperUrl = `https://www.ferryhopper.com/en/ferry-routes/direct/${r.from}-${r.to}`;
    return `
      <div class="intl-route-card">
        <div class="intl-route-header">
          <div class="intl-route-title">
            <span class="intl-flag-from">🇬🇷</span>
            <strong>${islandName(r.from)}</strong>
            <span class="intl-arrow">↔</span>
            <strong>${pickLang(to, 'name')}</strong>
            <span class="intl-flag-to">${flag}</span>
          </div>
          <span class="intl-freq-badge ${freqClass}">${pickLang(r, 'frequency_label')}</span>
        </div>
        <div class="intl-route-meta">
          <span class="intl-meta-item">⏱ ${pickLang(r, 'duration')}</span>
          <span class="intl-meta-item">💶 ${r.price}</span>
          <span class="intl-meta-item">🚢 ${r.operators}</span>
        </div>
        <div class="intl-destination-block">
          <div class="intl-destination-top">
            <span class="intl-destination-label">${pickLang(to, 'name')} — ${t('international.destination.worth')}</span>
            <span class="intl-stars">${stars}</span>
          </div>
          <p class="intl-destination-context">${pickLang(to, 'context')}</p>
        </div>
        <div class="intl-route-footer">
          <p class="intl-route-note">${pickLang(r, 'note')}</p>
          <a class="intl-schedule-btn" href="${ferryhopperUrl}" target="_blank" rel="noopener">🗓 ${t('international.schedule.btn')}</a>
        </div>
      </div>
    `;
  };

  const albaniaSection = albaniaRoutes.length ? `
    <h3 class="intl-country-heading">🇦🇱 ${t('international.country.albania')}</h3>
    ${albaniaRoutes.map(renderRoute).join('')}
  ` : '';

  const turkeySection = turkeyRoutes.length ? `
    <h3 class="intl-country-heading">🇹🇷 ${t('international.country.turkey')}</h3>
    ${turkeyRoutes.map(renderRoute).join('')}
  ` : '';

  container.innerHTML = albaniaSection + turkeySection;
}

window.renderInternational = renderInternational;

/* ============================================================
   QUIZ
============================================================ */
const WTV_TAGS = {
  "aegina": [2, 1, 2, 2, 3, 3, 1, 0, 3, 2, 2, 2],
  "agathonisi": [0, 0, 0, 0, 1, 3, 2, 1, 3, 0, 0, 0],
  "agios-efstratios": [0, 0, 0, 0, 1, 3, 2, 1, 3, 0, 0, 0],
  "agistri": [1, 1, 2, 2, 3, 3, 1, 1, 3, 2, 1, 1],
  "alonnisos": [0, 0, 1, 2, 3, 3, 2, 1, 3, 2, 1, 0],
  "ammouliani": [0, 0, 1, 2, 2, 3, 1, 0, 3, 2, 0, 0],
  "amorgos": [0, 0, 1, 2, 2, 3, 2, 1, 3, 2, 1, 0],
  "anafi": [0, 0, 0, 1, 1, 3, 2, 1, 3, 1, 0, 0],
  "antikythera": [0, 0, 0, 1, 2, 3, 2, 2, 3, 1, 0, 0],
  "andros": [1, 1, 2, 2, 3, 3, 1, 0, 3, 2, 1, 1],
  "antiparos": [0, 0, 1, 2, 3, 3, 2, 1, 3, 2, 1, 0],
  "astypalaia": [0, 0, 1, 2, 2, 3, 2, 1, 3, 2, 0, 0],
  "chania": [1, 1, 2, 2, 3, 3, 1, 0, 3, 2, 2, 1],
  "chios": [1, 1, 2, 2, 3, 3, 2, 1, 3, 2, 2, 1],
  "corfu": [1, 1, 2, 2, 3, 3, 1, 0, 3, 2, 2, 1],
  "donousa": [0, 0, 0, 1, 2, 3, 2, 1, 3, 1, 0, 0],
  "elafonisos": [0, 0, 1, 2, 3, 3, 1, 0, 3, 2, 0, 0],
  "evia-central": [1, 1, 2, 2, 3, 3, 1, 1, 3, 2, 2, 1],
  "evia-north": [2, 2, 2, 2, 2, 3, 1, 0, 3, 2, 2, 2],
  "evia-south": [1, 1, 2, 2, 3, 3, 1, 1, 3, 2, 2, 1],
  "folegandros": [0, 0, 1, 2, 3, 3, 2, 1, 3, 2, 1, 0],
  "fournoi": [0, 0, 1, 2, 2, 3, 2, 1, 3, 2, 0, 0],
  "gavdos": [0, 0, 0, 1, 2, 3, 1, 0, 3, 1, 0, 0],
  "halki": [0, 0, 1, 2, 2, 3, 1, 0, 3, 2, 0, 0],
  "heraklion": [1, 1, 2, 2, 2, 3, 0, 0, 3, 2, 2, 1],
  "hydra": [1, 1, 2, 2, 3, 3, 1, 0, 3, 2, 2, 1],
  "ikaria": [1, 1, 2, 2, 3, 3, 2, 2, 3, 2, 2, 1],
  "ios": [0, 0, 1, 1, 2, 2, 0, 0, 3, 2, 1, 0],
  "iraklia": [0, 0, 0, 1, 2, 3, 2, 1, 3, 1, 0, 0],
  "ithaca": [1, 1, 2, 2, 3, 3, 2, 1, 3, 2, 2, 1],
  "kalymnos": [2, 2, 3, 2, 2, 3, 1, 0, 3, 3, 2, 2],
  "karpathos": [0, 0, 1, 2, 2, 3, 2, 1, 3, 3, 1, 0],
  "kasos": [0, 0, 0, 1, 1, 3, 2, 1, 3, 0, 0, 0],
  "kastellorizo": [0, 0, 1, 2, 2, 3, 2, 0, 3, 2, 0, 0],
  "kea": [1, 1, 2, 2, 3, 2, 1, 1, 3, 2, 1, 1],
  "kefalonia": [1, 1, 2, 2, 3, 3, 2, 1, 3, 2, 2, 1],
  "kimolos": [0, 0, 1, 2, 2, 3, 1, 1, 3, 2, 0, 0],
  "kos": [1, 1, 2, 2, 3, 3, 1, 0, 3, 2, 2, 1],
  "koufonisia": [0, 0, 0, 1, 2, 3, 2, 1, 3, 2, 0, 0],
  "kythira": [1, 1, 2, 2, 3, 3, 2, 1, 3, 2, 2, 1],
  "kythnos": [1, 1, 2, 2, 3, 3, 1, 0, 3, 2, 1, 1],
  "lasithi": [1, 1, 2, 2, 3, 3, 1, 0, 3, 2, 2, 1],
  "lefkada": [1, 1, 2, 2, 3, 3, 1, 0, 3, 2, 2, 1],
  "leipsoi": [0, 0, 0, 1, 2, 3, 2, 1, 3, 0, 0, 0],
  "lemnos": [1, 1, 2, 2, 3, 3, 2, 2, 3, 2, 2, 1],
  "leros": [1, 1, 1, 2, 2, 3, 2, 1, 3, 2, 1, 1],
  "lesvos": [1, 1, 2, 2, 3, 3, 2, 1, 3, 2, 2, 1],
  "meganisi": [0, 0, 1, 2, 2, 3, 2, 1, 3, 2, 0, 0],
  "milos": [0, 0, 1, 2, 3, 3, 1, 0, 3, 2, 1, 0],
  "mykonos": [0, 0, 1, 2, 2, 3, 0, 0, 3, 2, 1, 0],
  "naxos": [0, 0, 1, 2, 3, 3, 1, 0, 3, 2, 1, 0],
  "nisyros": [0, 0, 1, 2, 2, 3, 1, 0, 3, 2, 0, 0],
  "oinousses": [0, 0, 1, 2, 2, 3, 2, 1, 3, 0, 0, 0],
  "paros": [0, 0, 1, 2, 2, 3, 1, 0, 3, 2, 1, 0],
  "patmos": [0, 0, 1, 2, 3, 3, 1, 0, 3, 2, 1, 0],
  "paxos": [0, 0, 1, 2, 2, 3, 1, 0, 3, 2, 0, 0],
  "poros": [1, 1, 2, 2, 3, 3, 1, 1, 3, 2, 2, 1],
  "psara": [0, 0, 0, 1, 2, 3, 2, 1, 3, 0, 0, 0],
  "rethymno": [1, 1, 2, 2, 3, 3, 1, 0, 3, 2, 2, 1],
  "rhodes": [2, 1, 2, 2, 2, 3, 1, 0, 3, 2, 2, 1],
  "salamis": [1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 1, 1],
  "samos": [1, 1, 2, 2, 3, 3, 1, 1, 3, 2, 2, 1],
  "samothrace": [0, 0, 1, 2, 2, 3, 2, 1, 3, 2, 1, 0],
  "santorini": [0, 0, 1, 2, 2, 3, 0, 0, 3, 2, 1, 0],
  "schoinoussa": [0, 0, 0, 1, 2, 3, 2, 1, 3, 1, 0, 0],
  "serifos": [0, 0, 1, 2, 2, 3, 1, 0, 3, 2, 1, 0],
  "sifnos": [0, 0, 1, 2, 2, 3, 2, 1, 3, 2, 1, 0],
  "sikinos": [0, 0, 0, 1, 2, 3, 1, 1, 3, 1, 0, 0],
  "skiathos": [0, 0, 1, 2, 2, 3, 1, 0, 3, 2, 1, 0],
  "skopelos": [0, 0, 1, 2, 2, 3, 1, 0, 3, 2, 1, 0],
  "skyros": [1, 2, 2, 2, 3, 3, 2, 1, 3, 2, 1, 1],
  "spetses": [1, 1, 2, 2, 3, 3, 1, 0, 3, 2, 2, 1],
  "symi": [0, 0, 1, 2, 3, 3, 1, 0, 3, 2, 2, 0],
  "syros": [1, 1, 2, 2, 3, 3, 2, 1, 3, 2, 2, 1],
  "thasos": [1, 1, 2, 2, 3, 3, 1, 0, 3, 2, 2, 1],
  "therasia": [0, 0, 0, 1, 2, 3, 2, 1, 3, 1, 0, 0],
  "tilos": [0, 0, 1, 2, 2, 3, 2, 1, 3, 2, 0, 0],
  "tinos": [0, 0, 1, 2, 3, 3, 2, 0, 3, 2, 1, 0],
  "zakynthos": [1, 1, 2, 2, 3, 3, 1, 0, 3, 2, 2, 1],
};

const QUIZ_QUESTIONS = [
  {
    question: 'What kind of trip are you planning?',
    question_el: 'Τι είδους ταξίδι σχεδιάζεις;',
    options: ['Solo adventure', 'Couple getaway', 'Family vacation', 'Friend group'],
    options_el: ['Μόνος/-η περιπέτεια', 'Ζευγάρι', 'Οικογενειακές διακοπές', 'Παρέα φίλων']
  },
  {
    question: 'What matters most to you?',
    question_el: 'Τι σε ενδιαφέρει περισσότερο;',
    options: ['Beaches & swimming', 'History & culture', 'Nightlife & food', 'Peace & nature'],
    options_el: ['Παραλίες & μπάνιο', 'Ιστορία & πολιτισμός', 'Νυχτερινή ζωή & φαγητό', 'Ηρεμία & φύση']
  },
  {
    question: 'What is your budget level?',
    question_el: 'Ποιο είναι το μπάτζετ σου;',
    options: ['Budget (backpacker)', 'Mid-range', 'Splurge-ready', 'No limit'],
    options_el: ['Οικονομικό', 'Μεσαίο', 'Γενναιόδωρο', 'Χωρίς όριο']
  },
  {
    question: 'How do you feel about crowds?',
    question_el: 'Πώς νιώθεις με τον κόσμο;',
    options: ['Love the buzz', 'Some is fine', 'Prefer quiet', 'Must be secluded'],
    options_el: ['Μου αρέσει η ζωντάνια', 'Παν μέτρον άριστον', 'Προτιμώ ηρεμία', 'Θέλω απομόνωση']
  },
  {
    question: 'When are you travelling?',
    question_el: 'Πότε ταξιδεύεις;',
    options: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    options_el: ['Ιαν','Φεβ','Μαρ','Απρ','Μάι','Ιουν','Ιουλ','Αυγ','Σεπ','Οκτ','Νοε','Δεκ'],
    month_picker: true
  },
  {
    question: 'How are you getting there?',
    question_el: 'Πώς φτάνεις στο νησί;',
    options: ['By car', 'Ferry — up to 5 hours', 'Ferry — more than 5 hours', 'Fly in'],
    options_el: ['Με το αυτοκίνητό μου', 'Πλοίο — έως 5 ώρες', 'Πλοίο — πάνω από 5 ώρες', 'Αεροπλάνο']
  },
  {
    question: 'Will you have a car on the island?',
    question_el: 'Θα έχεις αυτοκίνητο στο νησί;',
    options: ['Yes, I want to rent one', 'No, I prefer walking / public transport'],
    options_el: ['Ναι, θα νοικιάσω', 'Όχι, προτιμώ περπάτημα / ΜΜΜ']
  },
];
let quizAnswers = {};
let quizStep = 0;
let quizInitialized = false;
let quizDirection = 1; // 1 = forward, -1 = back

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
  const questionText = pickLang(q, 'question');
  const options = (CURRENT_LANG === 'el' && q.options_el) ? q.options_el : q.options;
  const backLabel = t('quiz.back');
  const isMonthPicker = !!q.month_picker;

  // Options HTML — month picker gets a compact 4-col grid
  const optionsHtml = isMonthPicker
    ? `<div class="quiz-options quiz-month-grid">${options.map((opt, i) => `<button class="quiz-option quiz-month-btn ${quizAnswers[quizStep] === i ? 'selected' : ''}" data-idx="${i}">${opt}</button>`).join('')}</div>`
    : `<div class="quiz-options">${options.map((opt, i) => `<button class="quiz-option ${quizAnswers[quizStep] === i ? 'selected' : ''}" data-idx="${i}">${opt}</button>`).join('')}</div>`;

  container.innerHTML = `<div class="quiz-progress">${QUIZ_QUESTIONS.map((_, i) => `<div class="quiz-dot ${i < quizStep ? 'done' : i === quizStep ? 'current' : ''}"></div>`).join('')}<span class="quiz-step-label">${quizStep + 1} / ${QUIZ_QUESTIONS.length}</span></div><div class="quiz-card quiz-card-entering quiz-card-from-${quizDirection > 0 ? 'right' : 'left'}"><div class="quiz-question">${questionText}</div>${optionsHtml}${quizStep > 0 ? `<div class="quiz-nav-back"><button class="quiz-back-btn">← ${backLabel}</button></div>` : ''}</div>`;

  // Trigger animation: remove entering class after one frame so transition fires
  requestAnimationFrame(() => {
    const card = container.querySelector('.quiz-card');
    if (card) card.classList.remove('quiz-card-entering');
  });

  container.querySelectorAll('.quiz-option').forEach(btn => {
    btn.addEventListener('click', () => {
      quizAnswers[quizStep] = parseInt(btn.dataset.idx);
      if (quizStep < QUIZ_QUESTIONS.length - 1) {
        quizDirection = 1;
        quizStep++;
        renderQuizStep();
      } else {
        computeQuizResults();
      }
    });
  });
  const backBtn = container.querySelector('.quiz-back-btn');
  if (backBtn) backBtn.addEventListener('click', () => {
    if (quizStep > 0) { quizDirection = -1; quizStep--; renderQuizStep(); }
  });
}

function computeQuizResults() {
  const priorityDims = ['beach', 'hist', 'night', 'afford'];
  const priority = priorityDims[quizAnswers[1]] || 'total';
  const budgetMod = [2, 0.5, -0.5, -2][quizAnswers[2]] || 0;
  const crowdPref = quizAnswers[3];

  // Q5 season — now a single month index (0=Jan … 11=Dec)
  // Use the chosen month plus neighbours for scoring to be more forgiving
  const seasonIdx = quizAnswers[4];
  const seasonMonths = {};
  for (let m = 0; m < 12; m++) {
    seasonMonths[m] = [m]; // single month — exact match
  }

  // Q6 transport: 0=car/bridge, 1=short ferry <2h, 2=long ferry ok, 3=fly
  const transportPref = quizAnswers[5];

  // Islands reachable by car/bridge (drive-on ferry exists or bridge)
  const driveOnIslands = new Set(['lefkada','evia-north','evia-central','evia-south',
    'thasos','corfu','kefalonia','zakynthos','salamis','poros','aegina','agistri',
    'spetses','hydra','elafonisos','kythira','ithaca','ammouliani']);

  const scored = ISLANDS.map(i => {
    let s = i[priority] * 2.5 + i.total * 1.5;
    if (budgetMod > 0) s += budgetMod * i.afford;
    else if (budgetMod < 0) s += Math.abs(budgetMod) * (5 - i.afford);
    if (crowdPref >= 2) s += crowdPref * Math.max(0, 4 - Math.log10(i.pop + 1)) * 0.5;
    if (quizAnswers[0] === 2) { s += i.access * 0.5; if (i.night > 4) s -= 0.5; }

    // Season fit — boost islands rated perfect/great in chosen months, penalise avoid
    if (seasonIdx !== undefined && WTV_TAGS[i.key]) {
      const tags = WTV_TAGS[i.key];
      const months = seasonMonths[seasonIdx] || [];
      let seasonBonus = 0;
      months.forEach(mi => {
        const tag = tags[mi];
        if (tag === 3) seasonBonus += 1.2;       // perfect
        else if (tag === 2) seasonBonus += 0.5;  // great
        else if (tag === 0) seasonBonus -= 1.0;  // avoid
      });
      s += seasonBonus / months.length;
    }

    // Transport preference
    if (transportPref === 0) {
      // Car/bridge: strongly favour drive-on islands, penalise fly-only
      if (driveOnIslands.has(i.key)) s += 2.0;
      else if (!i.has_airport && i.access < 3) s -= 1.5;
    } else if (transportPref === 1) {
      // Ferry up to 5h — most islands with access >= 3, penalise truly remote ones
      if (i.access >= 3.0) s += 1.2;
      else if (i.access < 2.0) s -= 1.5;
    } else if (transportPref === 2) {
      // Ferry more than 5h — boost remote/hard-to-reach, no penalty on accessible ones
      if (i.access <= 2.5) s += 1.2;
      else if (i.access >= 4.5) s -= 0.5;
    } else if (transportPref === 3) {
      // Fly: favour airports, penalise no-airport
      if (i.has_airport) s += 1.2;
      else s -= 0.8;
    }

    // Q7: car preference. 0 = Yes (will rent), 1 = No car
    if (quizAnswers[6] === 1 && i.car_need) {
      s -= Math.max(0, i.car_need - 2) * 0.8;
    } else if (quizAnswers[6] === 0 && i.car_need) {
      s += Math.min(i.car_need, 5) * 0.1;
    }

    return { ...i, matchScore: s };
  }).sort((a, b) => b.matchScore - a.matchScore).slice(0, 6);
  const container = document.getElementById('quiz-container');
  const results = document.getElementById('quiz-results');
  if (!container || !results) return;
  container.style.display = 'none'; results.style.display = '';
  const dimLabels = (CURRENT_LANG === 'el')
    ? ['Παραλία', 'Πολιτισμός', 'Νυχτερινή ζωή', 'Προσιτή τιμή']
    : ['Beach', 'Culture', 'Nightlife', 'Affordability'];
  const dimLabel = dimLabels[quizAnswers[1]] || (CURRENT_LANG === 'el' ? 'Συνολικά' : 'Overall');
  const driveOnSet = new Set(['lefkada','evia-north','evia-central','evia-south',
    'thasos','corfu','kefalonia','zakynthos','salamis','poros','aegina','agistri',
    'spetses','hydra','elafonisos','kythira','ithaca','ammouliani']);
  const whyText = (island) => {
    const reasons = [];
    if (island[priority] >= 4.5) reasons.push(`${t('quiz.why.top')} ${dimLabel.toLowerCase()} (${fmt(island[priority])})`);
    else if (island[priority] >= 3.8) reasons.push(`${t('quiz.why.strong')} ${dimLabel.toLowerCase()} (${fmt(island[priority])})`);
    if (budgetMod > 0 && island.afford >= 4) reasons.push(t('quiz.why.affordable'));
    if (crowdPref >= 2 && island.pop < 5000) reasons.push(t('quiz.why.lowcrowds'));
    if (seasonIdx !== undefined && WTV_TAGS[island.key]) {
      const months = seasonMonths[seasonIdx] || [];
      const allPerfect = months.every(mi => WTV_TAGS[island.key][mi] === 3);
      if (allPerfect) reasons.push(t('quiz.why.season'));
    }
    if (transportPref === 0 && driveOnSet.has(island.key)) reasons.push(t('quiz.why.transport.car'));
    else if (transportPref === 3 && island.has_airport) reasons.push(t('quiz.why.transport.fly'));
    if (!reasons.length) reasons.push(`${t('quiz.why.overall')} ${fmt(island.total)}`);
    return reasons.slice(0, 2).join(' · ');
  };
  results.innerHTML = `<div class="quiz-results-header"><div class="quiz-results-title">${t('match.results.title')}</div><div class="quiz-results-sub">${t('match.results.sub')}</div></div>${scored.map((island, idx) => `<div class="result-island-card" data-key="${island.key}"><div class="result-rank">${idx + 1}</div><div class="result-info"><div class="result-name">${islandName(island.key)}</div><div class="result-why">${whyText(island)}</div></div><div class="result-score" style="color:${scoreToColor(island.total)}">${fmt(island.total)}</div></div>`).join('')}<div class="quiz-retake-row"><button class="quiz-retake-btn">${t('match.retake')}</button></div>`;
  results.querySelectorAll('.result-island-card').forEach(card => { card.addEventListener('click', () => navigateTo('island', card.dataset.key)); });
  results.querySelector('.quiz-retake-btn').addEventListener('click', () => { quizAnswers = {}; quizStep = 0; renderQuizStep(); });
}

/* ============================================================
   LIGHTBOX
   Click any <img class="lightbox-img"> to open in a fullscreen
   overlay. Arrow keys / swipe to navigate. Esc / click-outside
   / X to close. Reads CC credit from data-credit-* attributes.
============================================================ */
(function() {
  let overlay = null;
  let imgEl = null;
  let captionEl = null;
  let prevBtn = null;
  let nextBtn = null;
  let closeBtn = null;
  let currentIndex = 0;
  let imageSet = []; // array of <img> nodes that participate in lightbox
  let touchStartX = 0;
  let touchStartY = 0;
  let lastFocused = null;
  let bodyOverflow = '';

  function buildOverlay() {
    overlay = document.createElement('div');
    overlay.className = 'lightbox-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', 'Image viewer');
    overlay.innerHTML = ''
      + '<button class="lightbox-close" aria-label="Close">&times;</button>'
      + '<button class="lightbox-prev" aria-label="Previous image">&#8249;</button>'
      + '<button class="lightbox-next" aria-label="Next image">&#8250;</button>'
      + '<div class="lightbox-content">'
      +   '<img class="lightbox-content-img" alt="">'
      +   '<div class="lightbox-caption"></div>'
      + '</div>';
    document.body.appendChild(overlay);

    imgEl     = overlay.querySelector('.lightbox-content-img');
    captionEl = overlay.querySelector('.lightbox-caption');
    prevBtn   = overlay.querySelector('.lightbox-prev');
    nextBtn   = overlay.querySelector('.lightbox-next');
    closeBtn  = overlay.querySelector('.lightbox-close');

    prevBtn.addEventListener('click',  function(e) { e.stopPropagation(); navigate(-1); });
    nextBtn.addEventListener('click',  function(e) { e.stopPropagation(); navigate(1); });
    closeBtn.addEventListener('click', function(e) { e.stopPropagation(); close(); });
    overlay.addEventListener('click',  function(e) {
      // click-outside-image closes
      if (e.target === overlay || e.target.classList.contains('lightbox-content')) close();
    });

    // Touch / swipe
    overlay.addEventListener('touchstart', function(e) {
      if (e.touches.length === 1) {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
      }
    }, { passive: true });
    overlay.addEventListener('touchend', function(e) {
      if (touchStartX === 0) return;
      const t = e.changedTouches[0];
      const dx = t.clientX - touchStartX;
      const dy = t.clientY - touchStartY;
      touchStartX = 0;
      // Horizontal swipe > 50px and not too vertical = navigate
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) {
        navigate(dx > 0 ? -1 : 1);
      }
    }, { passive: true });
  }

  function buildCaption(img) {
    const artist  = img.getAttribute('data-credit-artist')   || '';
    const license = img.getAttribute('data-credit-license')  || '';
    const pageUrl = img.getAttribute('data-credit-page-url') || '';
    if (!artist && !license) return '';
    const text = artist
      ? (license ? '© ' + artist + ' / ' + license : '© ' + artist)
      : license;
    if (pageUrl) {
      return '<a href="' + pageUrl.replace(/"/g, '&quot;')
        + '" target="_blank" rel="noopener noreferrer">' + text + '</a>';
    }
    return text;
  }

  function show(index) {
    if (!imageSet.length) return;
    currentIndex = (index + imageSet.length) % imageSet.length;
    const src = imageSet[currentIndex];
    imgEl.src = src.src;
    imgEl.alt = src.alt || '';
    captionEl.innerHTML = buildCaption(src);
    // Hide nav buttons if only one image
    const single = imageSet.length <= 1;
    prevBtn.style.display = single ? 'none' : '';
    nextBtn.style.display = single ? 'none' : '';
  }

  function navigate(delta) { show(currentIndex + delta); }

  function open(triggerImg) {
    if (!overlay) buildOverlay();
    // Re-collect image set every open — page content may have changed
    imageSet = Array.prototype.slice.call(
      document.querySelectorAll('img.lightbox-img')
    ).filter(function(img) { return img.src && img.offsetParent !== null; });
    // The triggering image might not be in the set if it's inside a popup —
    // include it explicitly at the appropriate index.
    if (imageSet.indexOf(triggerImg) === -1) {
      imageSet = [triggerImg];
      currentIndex = 0;
    } else {
      currentIndex = imageSet.indexOf(triggerImg);
    }
    show(currentIndex);
    overlay.classList.add('lightbox-open');
    lastFocused = document.activeElement;
    closeBtn.focus();
    bodyOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
  }

  function close() {
    if (!overlay) return;
    overlay.classList.remove('lightbox-open');
    imgEl.src = '';
    document.body.style.overflow = bodyOverflow;
    if (lastFocused && typeof lastFocused.focus === 'function') {
      try { lastFocused.focus(); } catch (e) {}
    }
  }

  // Global delegated click handler — catches clicks on lightbox-img anywhere
  // in the document, INCLUDING inside Leaflet popups. We use the CAPTURE phase
  // (third arg = true) so we receive the click BEFORE any handler down the
  // tree can call e.stopPropagation() — Leaflet does this on popup content
  // to prevent map-click events, which would otherwise stop our delegation.
  document.addEventListener('click', function(e) {
    const target = e.target;
    // Don't open lightbox if the click is on/inside the credit badge —
    // that has its own toggle behaviour.
    if (target && target.closest && target.closest('.photo-credit-badge')) return;
    if (target && target.tagName === 'IMG' && target.classList.contains('lightbox-img')) {
      e.preventDefault();
      e.stopPropagation();
      open(target);
    }
  }, true);

  // Click anywhere outside an open credit badge collapses it.
  document.addEventListener('click', function(e) {
    const t = e.target;
    if (t && t.closest && t.closest('.photo-credit-badge')) return;
    document.querySelectorAll('.photo-credit-badge.open').forEach(function(b) {
      b.classList.remove('open');
    });
  });

  // Keyboard
  document.addEventListener('keydown', function(e) {
    if (!overlay || !overlay.classList.contains('lightbox-open')) return;
    if (e.key === 'Escape')      { e.preventDefault(); close(); }
    else if (e.key === 'ArrowLeft')  { e.preventDefault(); navigate(-1); }
    else if (e.key === 'ArrowRight') { e.preventDefault(); navigate(1); }
  });

  // Expose open() globally so direct-bound handlers (e.g. inside Leaflet popups,
  // where document-level delegation can be unreliable) can trigger the lightbox.
  window.openLightbox = open;
})();
