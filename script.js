'use strict';

const VERSION = 'v4.0';

const ISLANDS_DATA = {
  "lefkada":      { name:"Lefkada",          lat:38.706, lng:20.648, beach:4.9, hist:2.5, night:3.2, access:4.5, afford:4.0, car_need:4.0, has_airport:true, total:3.9, area:335,   pop:22600,   days:4, island_group:"Ionian", drama:false, hiking:true, springs:false, chora:false, sailing:true },
  "meganisi":     { name:"Meganisi",         lat:38.643, lng:20.783, beach:4.0, hist:2.5, night:2.8, access:3.2, afford:3.2, car_need:3.0, has_airport:false, total:3.5, area:22,    pop:1041,    days:2, island_group:"Ionian", drama:false, hiking:false, springs:false, chora:false, sailing:true },
  "ithaca":       { name:"Ithaca",           lat:38.366, lng:20.716, beach:3.8, hist:4.9, night:2.5, access:2.5, afford:3.5, car_need:4.0, has_airport:false, total:3.8, area:96,    pop:3231,    days:3, island_group:"Ionian", drama:false, hiking:true, springs:false, chora:false, sailing:true },
  "kefalonia":    { name:"Kefalonia",        lat:38.175, lng:20.569, beach:4.7, hist:3.2, night:3.2, access:3.5, afford:3.8, car_need:5.0, has_airport:true, total:4.1, area:773,   pop:35800,   days:5, island_group:"Ionian", drama:false, hiking:true, springs:false, chora:false, sailing:true },
  "zakynthos":    { name:"Zakynthos",        lat:37.787, lng:20.899, beach:4.8, hist:2.5, night:4.5, access:3.7, afford:3.5, car_need:4.0, has_airport:true, total:4.1, area:405,   pop:40700,   days:4, island_group:"Ionian", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "kythira":      { name:"Kythira",          lat:36.250, lng:23.000, beach:4.2, hist:4.5, night:2.5, access:2.5, afford:3.8, car_need:5.0, has_airport:true, total:3.7, area:279,   pop:3973,    days:4, island_group:"Ionian", drama:false, hiking:true, springs:false, chora:false, sailing:false },
  "elafonisos":   { name:"Elafonisos",       lat:36.480, lng:22.980, beach:5.0, hist:2.0, night:2.5, access:2.5, afford:3.8, car_need:1.0, has_airport:false, total:4.0, area:19,    pop:1041,    days:2, island_group:"Other", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "paros":        { name:"Paros",            lat:37.085, lng:25.148, beach:5.0, hist:3.8, night:5.0, access:4.5, afford:2.2, car_need:3.0, has_airport:true, total:4.1, area:196,   pop:13700,   days:3, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:true },
  "chania":       { name:"Crete (Chania)",   lat:35.512, lng:24.018, beach:5.0, hist:4.7, night:4.0, access:4.5, afford:3.4, car_need:5.0, has_airport:true, total:4.9, area:2376,  pop:108000,  days:5, island_group:"Crete", drama:false, hiking:true, springs:false, chora:false, sailing:false },
  "heraklion":    { name:"Crete (Heraklion)",lat:35.338, lng:25.131, beach:3.5, hist:5.0, night:4.7, access:5.0, afford:3.5, car_need:5.0, has_airport:true, total:4.3, area:2641,  pop:173000,  days:5, island_group:"Crete", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "rethymno":     { name:"Crete (Rethymno)", lat:35.367, lng:24.475, beach:3.8, hist:4.5, night:3.8, access:3.5, afford:3.7, car_need:5.0, has_airport:false, total:4.0, area:1496,  pop:34300,   days:4, island_group:"Crete", drama:false, hiking:true, springs:false, chora:false, sailing:false },
  "lasithi":      { name:"Crete (Lasithi)",  lat:35.188, lng:25.715, beach:4.0, hist:3.5, night:3.4, access:3.2, afford:3.2, car_need:5.0, has_airport:true, total:4.0, area:1823,  pop:76000,   days:4, island_group:"Crete", drama:false, hiking:true, springs:false, chora:false, sailing:false },
  "santorini":    { name:"Santorini",        lat:36.393, lng:25.461, beach:3.2, hist:5.0, night:4.2, access:4.7, afford:1.0, car_need:3.0, has_airport:true, total:4.8, area:76,    pop:15500,   days:3, island_group:"Cyclades", drama:true, hiking:false, springs:false, chora:false, sailing:false },
  "milos":        { name:"Milos",            lat:36.732, lng:24.429, beach:5.0, hist:3.5, night:3.0, access:3.2, afford:2.8, car_need:4.0, has_airport:true, total:4.7, area:151,   pop:4900,    days:4, island_group:"Cyclades", drama:true, hiking:false, springs:false, chora:false, sailing:false },
  "rhodes":       { name:"Rhodes",           lat:36.170, lng:27.910, beach:4.2, hist:5.0, night:4.1, access:4.8, afford:3.5, car_need:5.0, has_airport:true, total:4.4, area:1400,  pop:115000,  days:5, island_group:"Dodecanese", drama:false, hiking:false, springs:false, chora:true, sailing:true },
  "naxos":        { name:"Naxos",            lat:37.105, lng:25.376, beach:4.8, hist:4.4, night:3.5, access:3.8, afford:4.0, car_need:4.0, has_airport:true, total:4.5, area:429,   pop:18900,   days:4, island_group:"Cyclades", drama:false, hiking:true, springs:false, chora:true, sailing:true },
  "mykonos":      { name:"Mykonos",          lat:37.446, lng:25.328, beach:4.3, hist:3.0, night:5.0, access:4.8, afford:1.0, car_need:4.0, has_airport:true, total:4.3, area:85,    pop:10100,   days:3, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:true },
  "corfu":        { name:"Corfu",            lat:39.624, lng:19.921, beach:3.9, hist:4.8, night:4.2, access:4.7, afford:3.2, car_need:4.0, has_airport:true, total:4.2, area:593,   pop:102000,  days:5, island_group:"Ionian", drama:false, hiking:false, springs:false, chora:false, sailing:true },


  "hydra":        { name:"Hydra",            lat:37.350, lng:23.466, beach:2.2, hist:4.2, night:3.8, access:4.2, afford:1.8, car_need:1.0, has_airport:false, total:4.1, area:52,    pop:2700,    days:2, island_group:"Saronic", drama:false, hiking:false, springs:false, chora:false, sailing:true },
  "folegandros":  { name:"Folegandros",      lat:36.630, lng:24.900, beach:3.9, hist:3.8, night:3.5, access:2.8, afford:2.2, car_need:3.0, has_airport:false, total:4.0, area:32,    pop:765,     days:3, island_group:"Cyclades", drama:true, hiking:false, springs:false, chora:true, sailing:false },
  "koufonisia":   { name:"Koufonisia",       lat:36.930, lng:25.600, beach:5.0, hist:2.0, night:4.0, access:3.0, afford:3.0, car_need:1.0, has_airport:false, total:4.0, area:26,    pop:399,     days:3, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "evia-north":   { name:"Evia (North)",     lat:38.850, lng:23.200, beach:3.8, hist:3.5, night:2.5, access:4.5, afford:4.8, car_need:5.0, has_airport:false, total:3.7, area:1200,  pop:48000,   days:3, island_group:"Evia", drama:false, hiking:true, springs:true, chora:false, sailing:false },
  "evia-central": { name:"Evia (Central)",   lat:38.500, lng:23.850, beach:3.5, hist:4.5, night:3.5, access:5.0, afford:4.6, car_need:5.0, has_airport:false, total:3.9, area:1700,  pop:120000,  days:3, island_group:"Evia", drama:false, hiking:true, springs:false, chora:false, sailing:false },
  "evia-south":   { name:"Evia (South)",     lat:38.016, lng:24.420, beach:4.2, hist:3.5, night:2.5, access:4.5, afford:4.5, car_need:5.0, has_airport:false, total:3.9, area:780,   pop:42000,   days:3, island_group:"Evia", drama:false, hiking:true, springs:false, chora:false, sailing:false },
  "lesvos":       { name:"Lesvos",           lat:39.21,  lng:26.21,  beach:4.0, hist:4.7, night:3.0, access:3.5, afford:4.6, car_need:5.0, has_airport:true, total:4.0, area:1633,  pop:83000,   days:6, island_group:"NE Aegean", drama:false, hiking:true, springs:true, chora:true, sailing:false },
  "chios":        { name:"Chios",            lat:38.368, lng:26.135, beach:3.2, hist:4.7, night:2.5, access:3.2, afford:4.5, car_need:4.0, has_airport:true, total:3.6, area:842,   pop:51000,   days:4, island_group:"NE Aegean", drama:false, hiking:false, springs:false, chora:true, sailing:false },
  "kos":          { name:"Kos",              lat:36.891, lng:27.287, beach:4.0, hist:4.2, night:4.0, access:4.6, afford:3.8, car_need:4.0, has_airport:true, total:3.7, area:287,   pop:33300,   days:4, island_group:"Dodecanese", drama:false, hiking:false, springs:false, chora:false, sailing:true },
  "samos":        { name:"Samos",            lat:37.754, lng:26.977, beach:3.5, hist:4.6, night:3.0, access:3.5, afford:4.2, car_need:4.0, has_airport:true, total:3.3, area:477,   pop:32900,   days:4, island_group:"NE Aegean", drama:false, hiking:true, springs:false, chora:false, sailing:false },

  "syros":        { name:"Syros",            lat:37.444, lng:24.942, beach:2.8, hist:4.3, night:3.5, access:4.5, afford:3.5, car_need:3.0, has_airport:true, total:3.8, area:84,    pop:21500,   days:2, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "lemnos":       { name:"Lemnos",           lat:39.916, lng:25.166, beach:4.3, hist:3.5, night:2.2, access:3.0, afford:4.4, car_need:4.0, has_airport:true, total:3.5, area:476,   pop:16900,   days:3, island_group:"NE Aegean", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "agios-efstratios": { name:"Agios Efstratios", lat:39.515, lng:25.007, beach:4.5, hist:2.8, night:1.5, access:1.5, afford:4.5, car_need:1.0, has_airport:false, total:3.3, area:43,    pop:270,     days:1, island_group:"NE Aegean", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "psara":        { name:"Psara",            lat:38.541, lng:25.560, beach:3.8, hist:3.5, night:1.5, access:1.5, afford:4.2, car_need:1.0, has_airport:false, total:3.0, area:40,    pop:450,     days:1, island_group:"NE Aegean", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "oinousses":    { name:"Oinousses",        lat:38.520, lng:26.202, beach:3.5, hist:3.2, night:1.8, access:2.0, afford:4.0, car_need:1.0, has_airport:false, total:3.0, area:14,    pop:820,     days:1, island_group:"NE Aegean", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "iraklia":      { name:"Iraklia",          lat:36.840, lng:25.467, beach:4.2, hist:2.5, night:1.5, access:2.0, afford:4.3, car_need:1.0, has_airport:false, total:3.3, area:18,    pop:140,     days:1, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "kalymnos":     { name:"Kalymnos",         lat:36.983, lng:26.983, beach:3.5, hist:4.0, night:3.0, access:3.2, afford:4.2, car_need:4.0, has_airport:true, total:3.5, area:110,   pop:16179,   days:3, island_group:"Dodecanese", drama:false, hiking:true, springs:false, chora:false, sailing:false },
  "thasos":       { name:"Thasos",           lat:40.666, lng:24.666, beach:4.2, hist:3.2, night:3.0, access:3.2, afford:4.1, car_need:4.0, has_airport:false, total:3.7, area:379,   pop:13700,   days:3, island_group:"Other", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "aegina":       { name:"Aegina",           lat:37.750, lng:23.500, beach:2.5, hist:4.2, night:3.2, access:5.0, afford:3.5, car_need:3.0, has_airport:false, total:3.4, area:87,    pop:13000,   days:1, island_group:"Saronic", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "tinos":        { name:"Tinos",            lat:37.583, lng:25.166, beach:3.5, hist:4.0, night:3.0, access:4.2, afford:3.2, car_need:4.0, has_airport:false, total:3.7, area:194,   pop:8600,    days:2, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "andros":       { name:"Andros",           lat:37.830, lng:24.930, beach:3.8, hist:4.0, night:2.8, access:4.0, afford:3.2, car_need:4.0, has_airport:false, total:3.7, area:380,   pop:9200,    days:3, island_group:"Cyclades", drama:false, hiking:true, springs:false, chora:true, sailing:false },
  "ikaria":       { name:"Ikaria",           lat:37.600, lng:26.166, beach:4.0, hist:3.0, night:4.5, access:2.5, afford:4.5, car_need:4.0, has_airport:true, total:3.8, area:255,   pop:8400,    days:4, island_group:"NE Aegean", drama:true, hiking:true, springs:true, chora:false, sailing:false },
  "leros":        { name:"Leros",            lat:37.150, lng:26.850, beach:3.2, hist:4.0, night:3.0, access:3.2, afford:4.2, car_need:3.0, has_airport:true, total:3.3, area:53,    pop:7900,    days:2, island_group:"Dodecanese", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "karpathos":    { name:"Karpathos",        lat:35.583, lng:27.133, beach:4.4, hist:4.0, night:2.2, access:2.0, afford:3.8, car_need:5.0, has_airport:true, total:3.8, area:300,   pop:6200,    days:4, island_group:"Dodecanese", drama:true, hiking:true, springs:false, chora:false, sailing:false },
  "skiathos":     { name:"Skiathos",         lat:39.163, lng:23.490, beach:4.6, hist:2.0, night:4.7, access:4.5, afford:3.0, car_need:3.0, has_airport:true, total:3.9, area:49,    pop:6088,    days:3, island_group:"Sporades", drama:false, hiking:false, springs:false, chora:false, sailing:true },
  "skopelos":     { name:"Skopelos",         lat:39.121, lng:23.726, beach:4.2, hist:3.2, night:2.5, access:2.5, afford:3.8, car_need:4.0, has_airport:false, total:3.6, area:96,    pop:4960,    days:3, island_group:"Sporades", drama:false, hiking:true, springs:false, chora:false, sailing:true },
  "patmos":       { name:"Patmos",           lat:37.322, lng:26.545, beach:3.0, hist:4.8, night:2.8, access:2.2, afford:2.5, car_need:3.0, has_airport:false, total:3.6, area:34,    pop:3047,    days:2, island_group:"Dodecanese", drama:false, hiking:false, springs:false, chora:true, sailing:false },
  "poros":        { name:"Poros",            lat:37.510, lng:23.470, beach:3.0, hist:4.2, night:3.5, access:4.8, afford:3.2, car_need:3.0, has_airport:false, total:3.5, area:23,    pop:3993,    days:1, island_group:"Saronic", drama:false, hiking:false, springs:false, chora:false, sailing:true },
  "alonnisos":    { name:"Alonnisos",        lat:39.216, lng:23.916, beach:4.4, hist:3.0, night:2.5, access:2.5, afford:4.0, car_need:3.0, has_airport:false, total:3.8, area:64,    pop:2750,    days:3, island_group:"Sporades", drama:false, hiking:true, springs:false, chora:false, sailing:true },
  "skyros":       { name:"Skyros",           lat:38.866, lng:24.533, beach:4.0, hist:3.8, night:2.8, access:2.5, afford:4.2, car_need:4.0, has_airport:true, total:3.4, area:209,   pop:2994,    days:3, island_group:"Sporades", drama:true, hiking:false, springs:false, chora:true, sailing:false },

  "sifnos":       { name:"Sifnos",           lat:36.966, lng:24.716, beach:3.8, hist:4.0, night:3.2, access:3.5, afford:3.5, car_need:4.0, has_airport:false, total:3.9, area:73,    pop:2625,    days:3, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:true, sailing:false },
  "symi":         { name:"Symi",             lat:36.583, lng:27.833, beach:3.0, hist:4.8, night:3.5, access:3.5, afford:2.5, car_need:3.0, has_airport:false, total:3.8, area:58,    pop:2590,    days:2, island_group:"Dodecanese", drama:false, hiking:false, springs:false, chora:false, sailing:true },
  "paxos":        { name:"Paxos",            lat:39.200, lng:20.150, beach:4.2, hist:3.0, night:3.5, access:2.8, afford:2.5, car_need:2.0, has_airport:false, total:4.0, area:19,    pop:2300,    days:3, island_group:"Ionian", drama:false, hiking:false, springs:false, chora:false, sailing:true },
  "kea":          { name:"Kea (Tzia)",       lat:37.616, lng:24.333, beach:3.8, hist:3.8, night:3.0, access:4.5, afford:3.0, car_need:4.0, has_airport:false, total:3.5, area:131,   pop:2455,    days:2, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "ios":          { name:"Ios",              lat:36.723, lng:25.281, beach:4.6, hist:2.5, night:5.0, access:3.2, afford:3.5, car_need:3.0, has_airport:false, total:3.9, area:109,   pop:2024,    days:3, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:true, sailing:false },
  "amorgos":      { name:"Amorgos",          lat:36.833, lng:25.900, beach:4.0, hist:3.8, night:3.5, access:2.5, afford:3.5, car_need:4.0, has_airport:false, total:4.0, area:126,   pop:1973,    days:4, island_group:"Cyclades", drama:true, hiking:true, springs:false, chora:true, sailing:false },
  "kythnos":      { name:"Kythnos",          lat:37.383, lng:24.416, beach:4.2, hist:3.2, night:3.0, access:3.5, afford:3.8, car_need:3.0, has_airport:false, total:3.5, area:100,   pop:1456,    days:2, island_group:"Cyclades", drama:false, hiking:false, springs:true, chora:false, sailing:false },
  "astypalaia":   { name:"Astypalaia",       lat:36.550, lng:26.350, beach:4.0, hist:4.2, night:3.0, access:2.5, afford:3.8, car_need:4.0, has_airport:true, total:3.8, area:97,    pop:1334,    days:3, island_group:"Dodecanese", drama:true, hiking:false, springs:false, chora:true, sailing:false },
  "antiparos":    { name:"Antiparos",        lat:37.000, lng:25.080, beach:4.5, hist:3.0, night:4.0, access:3.5, afford:2.8, car_need:3.0, has_airport:false, total:4.0, area:35,    pop:1211,    days:2, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "serifos":      { name:"Serifos",          lat:37.150, lng:24.483, beach:4.5, hist:3.2, night:3.0, access:3.5, afford:3.8, car_need:3.0, has_airport:false, total:3.9, area:75,    pop:1420,    days:2, island_group:"Cyclades", drama:true, hiking:false, springs:false, chora:false, sailing:false },
  "agistri":      { name:"Agistri",          lat:37.700, lng:23.350, beach:3.5, hist:2.5, night:3.5, access:4.5, afford:4.0, car_need:1.0, has_airport:false, total:3.2, area:13,    pop:1142,    days:1, island_group:"Saronic", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "nisyros":      { name:"Nisyros",          lat:36.583, lng:27.166, beach:3.0, hist:5.0, night:2.5, access:2.8, afford:4.0, car_need:3.0, has_airport:false, total:3.8, area:41,    pop:1008,    days:1, island_group:"Dodecanese", drama:true, hiking:false, springs:false, chora:false, sailing:false },
  "kimolos":      { name:"Kimolos",          lat:36.800, lng:24.570, beach:4.5, hist:3.2, night:2.5, access:3.0, afford:3.8, car_need:3.0, has_airport:false, total:3.7, area:36,    pop:910,     days:2, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "kastellorizo": { name:"Kastellorizo",     lat:36.140, lng:29.580, beach:2.0, hist:5.0, night:2.8, access:1.2, afford:3.5, car_need:1.0, has_airport:true, total:4.0, area:12,    pop:492,     days:2, island_group:"Dodecanese", drama:true, hiking:false, springs:false, chora:false, sailing:false },
  "sikinos":      { name:"Sikinos",          lat:36.683, lng:25.116, beach:3.5, hist:4.2, night:2.2, access:2.5, afford:4.0, car_need:3.0, has_airport:false, total:3.4, area:42,    pop:273,     days:2, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:true, sailing:false },
  "anafi":        { name:"Anafi",            lat:36.366, lng:25.766, beach:4.5, hist:3.2, night:2.5, access:2.0, afford:4.2, car_need:3.0, has_airport:false, total:3.9, area:38,    pop:271,     days:2, island_group:"Cyclades", drama:true, hiking:false, springs:false, chora:true, sailing:false },
  "samothrace":   { name:"Samothrace",       lat:40.466, lng:25.533, beach:3.0, hist:4.1, night:2.5, access:1.8, afford:4.5, car_need:3.0, has_airport:false, total:3.2, area:178,   pop:2859,    days:2, island_group:"Other", drama:true, hiking:true, springs:true, chora:false, sailing:false },
  "fournoi":      { name:"Fournoi",          lat:37.580, lng:26.500, beach:3.8, hist:3.0, night:1.8, access:2.0, afford:4.5, car_need:3.0, has_airport:false, total:3.2, area:45,    pop:1459,    days:2, island_group:"Other", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "spetses":      { name:"Spetses",          lat:37.260, lng:23.130, beach:2.8, hist:4.2, night:4.2, access:4.2, afford:2.0, car_need:3.0, has_airport:false, total:3.7, area:22,    pop:4027,    days:2, island_group:"Saronic", drama:false, hiking:false, springs:false, chora:false, sailing:true },
  "tilos":        { name:"Tilos",            lat:36.416, lng:27.366, beach:3.8, hist:3.5, night:2.0, access:2.2, afford:4.2, car_need:3.0, has_airport:false, total:3.5, area:61,    pop:780,     days:2, island_group:"Dodecanese", drama:false, hiking:true, springs:false, chora:false, sailing:false },
  "leipsoi":      { name:"Leipsoi",          lat:37.300, lng:26.750, beach:4.0, hist:3.0, night:2.0, access:2.5, afford:4.5, car_need:2.0, has_airport:false, total:3.4, area:16,    pop:790,     days:1, island_group:"Dodecanese", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "halki":        { name:"Halki",            lat:36.220, lng:27.610, beach:3.8, hist:4.0, night:2.0, access:2.5, afford:4.0, car_need:3.0, has_airport:false, total:3.6, area:28,    pop:478,     days:2, island_group:"Dodecanese", drama:false, hiking:false, springs:false, chora:true, sailing:false },
  "ammouliani":   { name:"Ammouliani",       lat:40.332, lng:23.916, beach:4.5, hist:2.0, night:3.0, access:3.0, afford:4.0, car_need:2.0, has_airport:false, total:3.5, area:4,     pop:547,     days:2, island_group:"Other", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "salamis":      { name:"Salamis",          lat:37.933, lng:23.500, beach:2.0, hist:3.5, night:3.0, access:5.0, afford:4.5, car_need:3.0, has_airport:false, total:2.8, area:95,    pop:39283,   days:1, island_group:"Saronic", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "therasia":     { name:"Therasia",         lat:36.433, lng:25.350, beach:3.0, hist:3.5, night:1.5, access:3.0, afford:3.5, car_need:1.0, has_airport:false, total:3.1, area:9,     pop:319,     days:1, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "schoinoussa":  { name:"Schoinoussa",      lat:36.866, lng:25.516, beach:4.5, hist:2.0, night:2.5, access:2.5, afford:3.8, car_need:1.0, has_airport:false, total:3.4, area:8,     pop:227,     days:2, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "donousa":      { name:"Donousa",          lat:37.100, lng:25.800, beach:4.5, hist:2.0, night:2.5, access:2.2, afford:3.8, car_need:1.0, has_airport:false, total:3.4, area:13,    pop:167,     days:2, island_group:"Cyclades", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "kasos":        { name:"Kasos",            lat:35.383, lng:26.916, beach:3.2, hist:3.8, night:1.5, access:1.5, afford:4.5, car_need:3.0, has_airport:true, total:2.8, area:66,    pop:1084,    days:2, island_group:"Dodecanese", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "agathonisi":   { name:"Agathonisi",       lat:37.466, lng:26.966, beach:3.5, hist:2.0, night:1.5, access:1.8, afford:4.5, car_need:2.0, has_airport:false, total:3.0, area:13,    pop:185,     days:1, island_group:"Dodecanese", drama:false, hiking:false, springs:false, chora:false, sailing:false },
  "gavdos":       { name:"Gavdos",           lat:34.840, lng:24.080, beach:4.8, hist:2.0, night:2.5, access:1.0, afford:4.5, car_need:1.0, has_airport:false, total:2.5, area:33,    pop:152,     days:3, island_group:"Crete", drama:true, hiking:false, springs:false, chora:false, sailing:false }
};

const ISLANDS = Object.entries(ISLANDS_DATA).map(([key, data]) => ({ key, ...data }));

let mapInstance = null;
let mapMarkers = {};
let miniMapInstance = null;
let itineraryMapInstance = null;
let currentMapMode = 'overall';
let currentGroupFilter = 'all';
let compareSelection = ['chania', 'rhodes'];
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

  // Fall back to hash routing (the SPA's native navigation)
  const hash = window.location.hash.replace('#', '').trim();
  if (!hash) return { view: 'home', param: null };
  if (hash.startsWith('island/')) return { view: 'island', param: hash.replace('island/', '') };
  return { view: VIEW_HASH_MAP[hash] || 'home', param: null };
}


/* ============================================================
   MAP TILES — switch between light and dark tiles based on theme
============================================================ */
function getMapTileUrl() {
  const isDark = document.documentElement.classList.contains('dark');
  return isDark
    ? 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png'
    : 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
}

function getMapTileAttribution() {
  const isDark = document.documentElement.classList.contains('dark');
  return isDark
    ? '© OpenStreetMap contributors © CARTO'
    : '© OpenStreetMap contributors';
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

  // Map (theme-aware) layer
  const mapLayer = L.tileLayer(getMapTileUrl(), {
    attribution: options.attribution || getMapTileAttribution(),
    maxZoom: maxZoom,
    subdomains: isDark ? 'abcd' : 'abc',
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

  if (view === 'island') {
    const el = document.getElementById('view-detail');
    if (el) el.style.display = '';
    homeControls.style.display = 'none';
    const helpBtn = document.getElementById('help-btn');
    if (helpBtn) helpBtn.style.display = 'none';
    document.body.classList.remove('home-view-active');
    if (param) renderIslandPage(param);
    return;
  }
  const target = document.getElementById(`view-${view}`);
  if (target) target.style.display = '';
  homeControls.style.display = (view === 'home') ? '' : 'none';
  const navLink = document.getElementById(`nav-${view}`);
  if (navLink) navLink.classList.add('active');
  // Help button is only relevant on the home/map view
  const helpBtn = document.getElementById('help-btn');
  if (helpBtn) helpBtn.style.display = (view === 'home') ? '' : 'none';
  // Lock body scroll when on home view (map shouldn't be scrollable)
  document.body.classList.toggle('home-view-active', view === 'home');
  if (nav && nav.classList.contains('open')) nav.classList.remove('open');
  if (view === 'home' && mapInstance) setTimeout(() => mapInstance.invalidateSize(), 100);
  if (view === 'hopping') setTimeout(renderHopping, 50);
  if (view === 'international') setTimeout(renderInternational, 50);
  if (view === 'match') setupQuizIfNeeded();
  if (view === 'shortlist') renderShortlist();
  if (view === 'compare') setTimeout(renderCompareView, 50);
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
  try { DIM_LABELS = getDimLabels(); } catch(e) { console.warn('dimLabels', e); }
  try { setupLanguageToggle(); } catch(e) { console.warn('langToggle', e); }
  updateShortlistCount();
  try { setupDarkMode(); } catch(e) { console.warn('setupDarkMode', e); }
  try { setupVibeChips(); } catch(e) { console.warn('setupVibeChips', e); }
  try { setupVibeTags(); } catch(e) { console.warn('setupVibeTags', e); }
  try { setupGroupFilter(); } catch(e) { console.warn('setupGroupFilter', e); }
  try { setupMap(); } catch(e) { console.warn('setupMap', e); }
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
  if (localStorage.getItem('darkMode') === 'true') { root.classList.add('dark'); btn.textContent = '☀'; }
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
          <div class="itt-overall">${t('tooltip.overall')}: <strong style="color:${scoreToColor(island.total)}">${fmt(island.total)} ★</strong></div>
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

  document.getElementById('island-name').textContent = islandName(island.key);
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

  const guide = document.getElementById('island-guide');
  if (!guide) return;

  // Show loading state
  guide.innerHTML = `<div class="island-guide-box" style="text-align:center;padding:40px;color:var(--ink-3)">${t('fallback.loading').replace('{NAME}', islandName(key))}</div>`;

  // Try to fetch the island's JSON page data
  try {
    const res = await fetch(`/islands/${key}.json`);
    if (res.ok) {
      const data = await res.json();
      guide.innerHTML = buildIslandPage(data);
      setTimeout(() => initItineraryMap(data.itinerary.days, data.beaches || []), 80);
      if (data.beaches) setTimeout(() => loadBeachPhotos(data.beaches), 150);
      setTimeout(() => initBeachVotes(), 200);
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
function buildIslandPage(data) {
  const itin = data.itinerary;

  const dayBtns = itin.days.map(d =>
    `<button class="itin-day-btn" data-day="${d.day}" onclick="filterItinDay(${d.day})" style="border-color:${d.color};color:${d.color}"><span>${t("detail.day")} ${d.day}: ${pickLang(d, "title")}</span></button>`
  ).join('');

  const dayCards = itin.days.map(d => {
    const stops = d.stops.map((s, i) => {
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
            <div class="itin-stop-desc">${pickLang(s, "desc")}</div>
          </div>
          ${photoHtml}
        </div>
      </div>`;
    }).join('');
    const driveInfo = d.km ? `<span class="itin-day-meta">${d.km} ${t('common.km')} · ${d.drive_mins} ${t('common.mindrive')}</span>` : '';
    const overnightHtml = d.overnight ? `<span class="itin-overnight" style="border-color:${d.color};color:${d.color}">🌙 ${t('common.sleep')}: ${pickLang(d, 'overnight')}</span>` : '';
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
              <div class="beach-rating-block">
                <span class="beach-rating-label">${t("detail.yourrating")} <span class="beach-vote-count" id="vote-count-${beachId}"></span></span>
                <div class="beach-vote-stars" id="vote-stars-${beachId}" data-beach-id="${beachId}">
                  ${[1,2,3,4,5].map(s => `<span class="vote-star" data-score="${s}" onclick="voteBeach('${beachId}',${s})">☆</span>`).join('')}
                </div>
              </div>
            </div>
          </div>
        </div>
        <p class="beach-desc">${pickLang(b, "desc")}</p>
        <div class="beach-specs">
          <div class="beach-spec"><span class="beach-spec-label">${t("detail.spec.type")}</span><span class="beach-spec-val">${pickLang(b, "type")}</span></div>
          <div class="beach-spec"><span class="beach-spec-label">${t("detail.spec.length")}</span><span class="beach-spec-val">${pickLang(b, "length")}</span></div>
          <div class="beach-spec"><span class="beach-spec-label">${t("detail.spec.depth")}</span><span class="beach-spec-val">${pickLang(b, "depth")}</span></div>
          <div class="beach-spec"><span class="beach-spec-label">${t("detail.spec.wind")}</span><span class="beach-spec-val">${pickLang(b, "facing")}</span></div>
          <div class="beach-spec beach-spec-full"><span class="beach-spec-label">${t("detail.spec.facilities")}</span><span class="beach-spec-val">${pickLang(b, "facilities")}</span></div>
        </div>
      </div>
    </div>`;
  }).join('');

  const introHtml = data.intro ? `<div class="itin-island-intro"><p>${pickLang(data, 'intro')}</p></div>` : '';
  const gettingThereHtml = buildGettingThereSection(data);
  const beachSection = beachCards ? `
    <div class="itin-beaches-section">
      <div class="itin-beaches-header">
        <h2 class="itin-beaches-title">${t("detail.beaches.title")} ${islandName(currentIslandKey)}</h2>
        <p class="itin-beaches-sub">${t("detail.beaches.sub")}</p>
      </div>
      <div class="itin-beaches-list">${beachCards}</div>
    </div>` : '';

  return `
    <div class="itin-wrapper">
      <div class="itin-hero">
        <h2 class="itin-title">${pickLang(itin, "title")}</h2>
        <p class="itin-subtitle">${pickLang(itin, "subtitle")}</p>
      </div>
      ${introHtml}
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
    </div>`;
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

  const pills = (lang === 'el' ? gt.pills_el : gt.pills) || [];
  const summary = (lang === 'el' ? gt.summary_el : gt.summary) || '';
  const tip = lang === 'el' ? gt.tip_el : gt.tip;

  const pillHtml = pills.length
    ? `<div class="itin-gt-pills">${pills.map(p => `<span class="itin-gt-pill">${escHtml(p)}</span>`).join('')}</div>`
    : '';
  const summaryHtml = summary ? `<p class="itin-gt-summary">${escHtml(summary)}</p>` : '';
  const tipHtml = tip ? `<p class="itin-gt-tip"><strong>${escHtml(tipLabel)}:</strong> ${escHtml(tip)}</p>` : '';

  if (!pillHtml && !summaryHtml) return '';

  return `
    <section class="itin-getting-there">
      <h3 class="itin-getting-there-title">${escHtml(title)}</h3>
      ${pillHtml}
      ${summaryHtml}
      ${tipHtml}
    </section>`;
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

  // Three rows in the ribbon grid:
  //   Row 1: 6 above-captions (odd months: Jan/Mar/May/Jul/Sep/Nov), each spans 2 columns
  //   Row 2: 12 ribbon cells (one per month)
  //   Row 3: 6 below-captions (even months: Feb/Apr/Jun/Aug/Oct/Dec), each spans 2 columns
  const aboveCaps = [];
  const belowCaps = [];
  const ribbonCells = [];

  w.months.forEach((m, i) => {
    const tag = (m.tag || 'ok').toLowerCase();
    const why = pickLang(m, 'why') || '';
    const safeWhy = why.replace(/"/g, '&quot;');

    let capClass = '';
    if (tag === 'perfect')                     capClass = ' wtv-cap-peak';
    else if (tag === 'avoid' || tag === 'ok')  capClass = ' wtv-cap-muted';

    if (i % 2 === 0) {
      aboveCaps.push(`<div class="wtv-cap-above${capClass}"><span class="wtv-cap-text">${why}</span></div>`);
    } else {
      belowCaps.push(`<div class="wtv-cap-below${capClass}"><span class="wtv-cap-text">${why}</span></div>`);
    }

    ribbonCells.push(
      `<div class="wtv-cell wtv-${tag}" title="${safeWhy}">${monthNames[i]}</div>`
    );
  });

  const summary = pickLang(w, 'summary') || '';
  const summaryHtml = summary ? `<p class="wtv-summary">${summary}</p>` : '';

  const tagsPresent = new Set(w.months.map(m => (m.tag || 'ok').toLowerCase()));
  const legendOrder = ['perfect', 'great', 'ok', 'avoid'];
  const legendLabels = lang === 'el'
    ? { perfect: 'Τέλεια', great: 'Καλά', ok: 'Μέτρια', avoid: 'Απόφυγε' }
    : { perfect: 'Perfect', great: 'Great', ok: 'OK', avoid: 'Avoid' };
  const legend = legendOrder
    .filter(t => tagsPresent.has(t))
    .map(t => `<span class="wtv-legend-item"><span class="wtv-legend-swatch wtv-${t}"></span>${legendLabels[t]}</span>`)
    .join('');

  // Build mobile vertical list — 12 rows, one per month, with tag swatch + caption
  const tagLabels = lang === 'el'
    ? { perfect: 'Τέλεια', great: 'Καλά', ok: 'Μέτρια', avoid: 'Απόφυγε' }
    : { perfect: 'Perfect', great: 'Great', ok: 'OK', avoid: 'Avoid' };
  const verticalRows = w.months.map((m, i) => {
    const tag = (m.tag || 'ok').toLowerCase();
    const why = pickLang(m, 'why') || '';
    return `<div class="wtv-vrow wtv-v-${tag}">
      <div class="wtv-vmonth">${monthNames[i]}</div>
      <div class="wtv-vbar wtv-${tag}" title="${tagLabels[tag] || ''}"></div>
      <div class="wtv-vwhy">${why}</div>
    </div>`;
  }).join('');

  return `
    <section class="wtv-section">
      <h3 class="wtv-title">${t('wtv.title')}</h3>
      ${summaryHtml}
      <div class="wtv-ribbon-wrap">
        <div class="wtv-ribbon">
          ${aboveCaps.join('')}
          ${ribbonCells.join('')}
          ${belowCaps.join('')}
        </div>
      </div>
      <div class="wtv-vertical">${verticalRows}</div>
      <div class="wtv-legend">${legend}</div>
    </section>`;
}

/* ============================================================
   LOCAL & SEASONAL SECTION
   Renders only if specialties / crafts / festivals are present.
============================================================ */
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
function poiIcon(type, color) {
  const emojis = {
    city:       '🏙',
    castle:     '🏰',
    beach:      '🏖️',
    village:    '🏘',
    nature:     '🌿',
    spa:        '♨️',
    church:     '⛪',
    distillery: '🥃',
    harbour:    '⚓',
    museum:     '🏛️',
    forest:     '🌲',
  };
  const emoji = emojis[type] || '📍';
  return `<div style="font-size:22px;line-height:1;filter:drop-shadow(0 1px 3px rgba(0,0,0,.5));text-align:center;width:32px;height:32px;display:flex;align-items:center;justify-content:center;background:white;border-radius:50%;border:2px solid ${color};box-shadow:0 2px 6px rgba(0,0,0,.25);">${emoji}</div>`;
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
    const routeCoords = await fetchOSRMRoute(coords);

    const polyline = L.polyline(routeCoords, { color: day.color, weight: 5, opacity: 0.88 }).addTo(itineraryMapInstance);
    itinRouteLayers[day.day].push(polyline);

    day.stops.forEach((stop, i) => {
      const nameHtml = stop.wiki
        ? `<a href="${stop.wiki}" target="_blank" rel="noopener" style="color:${day.color};font-weight:700">${stop.name}</a>`
        : `<strong>${stop.name}</strong>`;
      const typeLabel = stop.type ? stop.type.charAt(0).toUpperCase() + stop.type.slice(1) : 'Stop';
      const photoLine = stop.photo
        ? `<div style="position:relative;margin-top:8px">${buildLightboxImg(stop.photo, stop.name, stop.photo_credit, '', 'style="width:100%;height:120px;object-fit:cover;border-radius:6px;display:block" onerror="this.parentElement.style.display=\'none\'"')}${buildPhotoCredit(stop.photo_credit)}</div>`
        : '';
      const icon = L.divIcon({
        className: 'custom-marker',
        html: poiIcon(stop.type || 'village', day.color),
        iconSize: [32, 32], iconAnchor: [16, 16],
      });
      const marker = L.marker([stop.lat, stop.lng], { icon })
        .addTo(itineraryMapInstance)
        .bindPopup(`<div style="min-width:200px;font-family:sans-serif"><div style="font-size:10px;font-weight:700;color:${day.color};text-transform:uppercase;letter-spacing:.6px;margin-bottom:5px">Day ${day.day} · ${typeLabel}</div>${nameHtml}<p style="font-size:12px;color:#555;margin:6px 0 0;line-height:1.55">${stop.desc}</p>${photoLine}</div>`);
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
  beaches.forEach(b => {
    if (!b.lat || !b.lng) return;
    const name = pickLang(b, 'name');
    const desc = pickLang(b, 'desc');
    const type = pickLang(b, 'type');
    const icon = L.divIcon({
      className: 'custom-marker',
      html: poiIcon('beach', BEACH_COLOR),
      iconSize: [32, 32], iconAnchor: [16, 16],
    });
    const popupHtml = `<div style="min-width:200px;font-family:sans-serif">
      <div style="font-size:10px;font-weight:700;color:${BEACH_COLOR};text-transform:uppercase;letter-spacing:.6px;margin-bottom:5px">${t('detail.beach')}</div>
      <strong>${name}</strong>
      ${type ? `<div style="font-size:11px;color:#777;margin-top:2px">${type}</div>` : ''}
      <p style="font-size:12px;color:#555;margin:6px 0 0;line-height:1.55">${desc}</p>
    </div>`;
    const marker = L.marker([b.lat, b.lng], { icon, zIndexOffset: -100 })
      .addTo(itineraryMapInstance)
      .bindPopup(popupHtml);
    itinBeachMarkers.push(marker);
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
function voteBeach(beachId, score) {
  // Save this user's vote
  const votes = JSON.parse(localStorage.getItem('beachVotes') || '{}');
  const userVotes = JSON.parse(localStorage.getItem('beachUserVotes') || '{}');
  const prevVote = userVotes[beachId] || 0;

  if (!votes[beachId]) votes[beachId] = { total: 0, count: 0 };

  // Adjust for previous vote
  if (prevVote > 0) {
    votes[beachId].total -= prevVote;
    votes[beachId].count -= 1;
  }

  votes[beachId].total += score;
  votes[beachId].count += 1;
  userVotes[beachId] = score;

  localStorage.setItem('beachVotes', JSON.stringify(votes));
  localStorage.setItem('beachUserVotes', JSON.stringify(userVotes));

  renderBeachVotes(beachId);
}

function renderBeachVotes(beachId) {
  const votes = JSON.parse(localStorage.getItem('beachVotes') || '{}');
  const userVotes = JSON.parse(localStorage.getItem('beachUserVotes') || '{}');
  const starsEl = document.getElementById(`vote-stars-${beachId}`);
  const countEl = document.getElementById(`vote-count-${beachId}`);
  if (!starsEl) return;

  const data = votes[beachId];
  const userScore = userVotes[beachId] || 0;
  const avg = data && data.count > 0 ? data.total / data.count : 0;
  const displayScore = userScore > 0 ? userScore : avg;

  // Update stars
  starsEl.querySelectorAll('.vote-star').forEach(star => {
    const s = parseInt(star.dataset.score);
    star.textContent = s <= Math.round(displayScore) ? '★' : '☆';
    star.style.color = userScore > 0 ? 'var(--aegean)' : 'var(--gold)';
    star.classList.toggle('voted', userScore > 0);
  });

  // Update count
  if (countEl && data && data.count > 0) {
    const avgStr = (data.total / data.count).toFixed(1);
    countEl.textContent = `${avgStr} (${data.count} vote${data.count !== 1 ? 's' : ''})`;
  }
}

function initBeachVotes() {
  // Render all vote stars on the page
  document.querySelectorAll('.beach-vote-stars').forEach(el => {
    renderBeachVotes(el.dataset.beachId);
  });
}

function starsHtml(score) {
  // Round to nearest 0.5
  const rounded = Math.round(score * 2) / 2;
  const full = Math.floor(rounded);
  const half = rounded % 1 !== 0;
  const empty = 5 - full - (half ? 1 : 0);
  const isFiveStars = rounded >= 5;
  const color = isFiveStars ? '#E8522A' : '#C4962A';
  let html = '';
  for (let i = 0; i < full; i++) html += `<span style="color:${color}">★</span>`;
  if (half) html += `<span style="color:${color}">½</span>`;
  for (let i = 0; i < empty; i++) html += `<span style="color:#DDD">★</span>`;
  return `<span class="star-rating" title="${score}">${html}</span>`;
}

const MAX_AREA = 2641; // Crete (Heraklion prefecture) — largest single entry
const MAX_POP = 664000; // removed Athens but keep scale reasonable — use 200000

function carNeedCompactHtml(score) {
  if (score == null || isNaN(score)) return '<span style="color:var(--ink-4)">—</span>';
  const n = Math.round(score);
  const labelsEN = ['', 'Useless', 'E-scooter', 'Useful', 'Very useful', 'Essential'];
  const labelsEL = ['', 'Άχρηστο', 'Πατίνι', 'Χρήσιμο', 'Πολύ χρήσιμο', 'Απαραίτητο'];
  const labels = (typeof CURRENT_LANG !== 'undefined' && CURRENT_LANG === 'el') ? labelsEL : labelsEN;
  const colors = ['', '#6B7280', '#8B8B8B', '#A58A3A', '#D17A2B', '#C0522A'];
  const col = colors[n] || '#888';
  return `<span class="car-compact-pill" style="background:${col}20;color:${col};border:1px solid ${col}40">${n} · ${labels[n]}</span>`;
}

function carNeedHtml(score) {
  // 1 = car useless, 5 = car essential. Display as a labeled pill.
  if (score == null || isNaN(score)) return '<span style="color:var(--ink-4)">—</span>';
  const n = Math.round(score);
  const labelsEN = ['', 'Useless', 'E-scooter', 'Useful', 'Very useful', 'Essential'];
  const labelsEL = ['', 'Άχρηστο', 'Πατίνι', 'Χρήσιμο', 'Πολύ χρήσιμο', 'Απαραίτητο'];
  const labels = (typeof CURRENT_LANG !== 'undefined' && CURRENT_LANG === 'el') ? labelsEL : labelsEN;
  const colors = ['', '#6B7280', '#8B8B8B', '#A58A3A', '#D17A2B', '#C0522A'];
  const col = colors[n] || '#888';
  const label = labels[n] || '';
  return `<span class="car-need-pill" style="background:${col}20;color:${col};border:1px solid ${col}40"><span class="car-need-icon">🚗</span><span class="car-need-score">${n}</span><span class="car-need-label">${label}</span></span>`;
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
  // Apply current compareSelection (defaults: chania + rhodes) to the dropdowns
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

  // Get why-text — use EL if in Greek, EN otherwise
  const wtvLangKey = CURRENT_LANG === 'el' ? 'why_el' : 'why';
  const whyA = jsonA && jsonA.when_to_visit && jsonA.when_to_visit.months
    ? jsonA.when_to_visit.months.map(m => m[wtvLangKey] || m.why || '') : [];
  const whyB = jsonB && jsonB.when_to_visit && jsonB.when_to_visit.months
    ? jsonB.when_to_visit.months.map(m => m[wtvLangKey] || m.why || '') : [];

  const months = monthNames.map((mo, i) => {
    const tA = tagsA[i] !== undefined ? tagsA[i] : 1;
    const tB = tagsB[i] !== undefined ? tagsB[i] : 1;
    const isSweet = tA >= 2 && tB >= 2;
    const isBest  = tA >= 3 && tB >= 3;
    const wA = whyA[i] || '';
    const wB = whyB[i] || '';
    const tooltip = `${islandName(iA.key)}: ${tagLabel(tA)}${wA ? ' \u2014 ' + wA : ''} | ${islandName(iB.key)}: ${tagLabel(tB)}${wB ? ' \u2014 ' + wB : ''}`;
    return `<div class="cwtv-col${isSweet ? ' cwtv-sweet' : ''}${isBest ? ' cwtv-best' : ''}" title="${tooltip.replace(/"/g,"'")}">
      <div class="cwtv-cell cwtv-a ${tagClass[tA]}"></div>
      <div class="cwtv-month">${mo}</div>
      <div class="cwtv-cell cwtv-b ${tagClass[tB]}"></div>
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

  el.innerHTML = `
    <div class="cwtv-legend-row">
      <div class="cwtv-legend">
        <span class="cwtv-leg wtv-perfect"></span>${t('wtv.perfect')}
        <span class="cwtv-leg wtv-great"></span>${t('wtv.great')}
        <span class="cwtv-leg wtv-ok"></span>${t('wtv.ok')}
        <span class="cwtv-leg wtv-avoid"></span>${t('wtv.avoid')}
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
  const dimLabels = { beach: t('dim.beach'), hist: t('dim.culture'), night: t('dim.night'), access: t('dim.access'), afford: t('dim.afford') };

  const card = (island, other) => {
    const barsHtml = COMPARE_DIMS.map(dim => {
      const wins = island[dim] >= other[dim];
      return `<div class="cmp-bar-row"><span class="cmp-dim-label">${dimLabels[dim]}</span><div class="cmp-bar-track"><div class="cmp-bar-fill cmp-bar-${dim}" style="width:${(island[dim]/5)*100}%"></div></div><span class="cmp-dim-val ${wins ? 'wins' : ''}">${fmt(island[dim])}</span></div>`;
    }).join('');

    const carLabel = carWords[Math.round(island.car_need || 0)] || '—';
    const airportRow = island.has_airport ? `<div class="cmp-info-row"><span class="cmp-info-label">✈ ${t('tooltip.hasairport')}</span><span class="cmp-info-val">${t('common.yes')}</span></div>` : '';
    const daysRow = island.days ? `<div class="cmp-info-row"><span class="cmp-info-label">⏱ ${t('tooltip.suggesteddays')}</span><span class="cmp-info-val">${island.days} ${t('common.days')}</span></div>` : '';

    return `<div class="compare-card">
      <h2>${islandName(island.key)}</h2>
      <div class="compare-meta">${groupName(island.island_group)} · ${fmtNum(island.area)} km² · ${t('compare.pop')}. ${fmtNum(island.pop)}</div>
      <div class="compare-total" style="color:${scoreToColor(island.total)}">${fmt(island.total)}<span>/5</span></div>
      <div class="compare-bars">${barsHtml}</div>
      <div class="cmp-info-panel">
        <div class="cmp-info-row"><span class="cmp-info-label">🚗 ${t('dim.car')}</span><span class="cmp-info-val"><strong>${carLabel}</strong></span></div>
        ${airportRow}
        ${daysRow}
      </div>
    </div>`;
  };

  container.innerHTML = card(iA, iB) + card(iB, iA);
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

function renderFerryMap() {
  const mapEl = document.getElementById('ferry-map');
  if (!mapEl || mapEl._map) return; // already rendered
  
  const ferryMap = L.map('ferry-map', {
    zoomControl: true, minZoom: 6, maxZoom: 10,
    maxBounds: [[34.5, 19.0], [41.0, 29.5]], maxBoundsViscosity: 0.85
  }).setView([37.5, 25.2], 7);
  
  mapEl._map = ferryMap;
  addThemeAwareTiles(ferryMap, { maxZoom: 10 });
  L.control.scale({ imperial: false, position: 'bottomleft' }).addTo(ferryMap);
  
  // Frequency colours & weights
  const freqStyle = {
    high: { color: '#0B8FAC', weight: 4, opacity: 0.85 },
    med:  { color: '#FF6B6B', weight: 3, opacity: 0.75 },
    low:  { color: '#C4962A', weight: 2.5, opacity: 0.7 },
  };
  
  // Draw routes
  const drawnPorts = new Set();
  FERRY_ROUTES.forEach(route => {
    const style = freqStyle[route.freq] || freqStyle.low;
    
    // Multi-stop polyline route
    if (route.polyline) {
      const coords = [];
      route.polyline.forEach(key => {
        const port = getPortCoords(key);
        if (port) {
          coords.push([port.lat, port.lng]);
          drawnPorts.add(key);
        }
      });
      if (coords.length < 2) return;
      
      const line = L.polyline(coords, {
        color: style.color, weight: style.weight, opacity: style.opacity,
        dashArray: route.freq === 'low' ? '8, 6' : null,
      }).addTo(ferryMap);
      
      const firstName = getPortCoords(route.polyline[0]).name;
      const lastName = getPortCoords(route.polyline[route.polyline.length - 1]).name;
      const tooltip = `<strong>${firstName} → ${lastName}</strong><br><span style="font-size:11px;color:var(--ink-3)">${route.note}</span>`;
      line.bindTooltip(tooltip, { sticky: true, opacity: 1, className: 'island-tooltip' });
      return;
    }
    
    // Simple from→to route
    const from = getPortCoords(route.from, route.useRhodesPort);
    const to = getPortCoords(route.to, route.useRhodesPort);
    if (!from || !to) return;
    
    const line = L.polyline([[from.lat, from.lng], [to.lat, to.lng]], {
      color: style.color, weight: style.weight, opacity: style.opacity,
      dashArray: route.freq === 'low' ? '8, 6' : null,
    }).addTo(ferryMap);
    
    const tooltip = `<strong>${from.name} ↔ ${to.name}</strong><br><span style="font-size:11px;color:var(--ink-3)">${route.note}</span>`;
    line.bindTooltip(tooltip, { sticky: true, opacity: 1, className: 'island-tooltip' });
    
    drawnPorts.add(route.from);
    drawnPorts.add(route.to);
  });
  
  // Draw port markers
  drawnPorts.forEach(key => {
    // For Rhodes, place the marker at the port (matches where the Dodecanese lines start)
    const port = key === 'rhodes' 
      ? { ...ISLANDS_DATA['rhodes'], lat: RHODES_PORT.lat, lng: RHODES_PORT.lng }
      : getPortCoords(key);
    if (!port) return;
    const isPiraeus = key === 'piraeus';
    const marker = L.circleMarker([port.lat, port.lng], {
      radius: isPiraeus ? 8 : 6,
      color: isPiraeus ? '#E8522A' : '#076880',
      fillColor: isPiraeus ? '#FF6B6B' : '#0B8FAC',
      fillOpacity: 0.9,
      weight: 2,
    }).addTo(ferryMap);
    
    marker.bindTooltip(`<strong>${port.name}</strong>`, { 
      direction: 'top', opacity: 1, className: 'island-tooltip' 
    });
    
    // Click to navigate to island if it has a page
    if (ISLANDS_DATA[key]) {
      marker.on('click', () => navigateTo('island', key));
    }
  });
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
    ? ['Παραλία', 'Πολιτισμός', 'Νυχτερινή ζωή', 'Φιλικό στο πορτοφόλι']
    : ['Beach', 'Culture', 'Nightlife', 'Price-friendly'];
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
