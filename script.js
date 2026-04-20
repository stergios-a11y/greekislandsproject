const VERSION_ID = "v53.2 - Detail Restore Build";
let mainMap, miniMap, markerLayerGroup, legendControl;
let currentMode = 'overall';
let islandData = {};
const dayColors = ['#005BAE', '#10b981', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4'];
let markerStore = {};
let currentSortCol = 2; 
let sortDir = -1;
let dayLayerGroups = {};
let beachLayerGroup;

window.onload = function() {
    document.getElementById('version-display').innerText = VERSION_ID;
    initMap();
    fetch('islands_master.json?v=' + Date.now())
        .then(res => res.json())
        .then(data => { 
            islandData = data; 
            renderMarkers(); 
            generateTable(); 
        }).catch(err => console.error("Database connection lost.", err));
};

function initMap() {
    mainMap = L.map('main-map', { zoomControl: false, minZoom: 6 }).setView([38.3, 24.5], 7);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(mainMap);
    markerLayerGroup = L.layerGroup().addTo(mainMap);
    legendControl = L.control({ position: 'bottomleft' }); 
    legendControl.onAdd = () => {
        let div = L.DomUtil.create('div', 'info legend');
        updateLegendContent(div);
        return div;
    };
    legendControl.addTo(mainMap);
}

function updateLegendContent(div) {
    div.innerHTML = `<strong>${currentMode.toUpperCase()} TIER</strong><br>` +
        `<div class="legend-item">⭐ Elite (Top 10)</div>` +
        `<div class="legend-item"><span class="dot" style="background:#005BAE"></span> High (3.5+)</div>` +
        `<div class="legend-item"><span class="dot" style="background:#f1c40f"></span> Avg (3.0+)</div>` +
        `<div class="legend-item"><span class="dot" style="background:#e67e22"></span> Niche (<3.0)</div>`;
}

function getScore(d, mode) {
    if (!d) return 0;
    if (mode === 'overall') return d.total || d.overall || 0;
    return d[mode] || 0;
}

function renderMarkers() {
    if (!markerLayerGroup) return;
    markerLayerGroup.clearLayers();
    const sortedIds = Object.keys(islandData).sort((a,b) => getScore(islandData[b], currentMode) - getScore(islandData[a], currentMode));
    const top10 = sortedIds.slice(0, 10);
    const starIcon = L.divIcon({ html: '<div style="font-size:24px; color:#fbbf24; text-shadow:0 2px 4px rgba(0,0,0,0.3);">⭐</div>', className:'star-icon', iconSize:[30,30], iconAnchor:[15,15] });

    Object.keys(islandData).forEach(id => {
        const d = islandData[id];
        const score = getScore(d, currentMode);
        const color = score >= 3.5 ? "#005BAE" : (score >= 3.0 ? "#f1c40f" : "#e67e22");
        let marker = top10.includes(id) ? L.marker([d.lat, d.lng], {icon: starIcon}) : L.circleMarker([d.lat, d.lng], {radius:9, fillColor:color, color:"#fff", weight:2, fillOpacity:1});
        marker.addTo(markerLayerGroup).on('click', () => showDetail(id));
        marker.bindTooltip(`<strong>${d.name}</strong><br>${currentMode}: ${score.toFixed(1)}`);
        markerStore[id] = { marker, data: d };
    });
}

function handleNav(t) { 
    document.querySelectorAll('.view-section').forEach(v => v.style.display = 'none');
    document.getElementById('home-controls').style.display = (t === 'home') ? 'flex' : 'none';
    document.getElementById('view-' + t).style.display = 'block';
    document.getElementById('main-nav').classList.remove('active');
    if (t === 'home' && mainMap) setTimeout(() => mainMap.invalidateSize(), 200);
    window.scrollTo(0,0);
}

function showDetail(id) { 
    handleNav('detail'); 
    const d = islandData[id];
    document.getElementById('island-name').innerText = d.name; 
    
    // Set Star Bars
    const cats = ['beach','hist','night','access','afford'];
    cats.forEach(c => {
        const score = d[c] || 0;
        document.getElementById(`star-${c}`).style.width = (score/5*100) + "%";
    });

    fetch(`islands/${id}.json?v=` + Date.now())
        .then(res => res.json())
        .then(d_detail => {
            renderDetailView(Object.assign({}, d, d_detail));
        }).catch(() => {
            renderDetailView(Object.assign({}, d, { guide: "Full blueprint coming soon." }));
        });
}

function renderDetailView(d) {
    document.getElementById('island-guide').innerHTML = d.guide || "";
    
    if (miniMap) miniMap.remove();
    
    // Visibility delay for Leaflet stabilization
    setTimeout(() => {
        miniMap = L.map('island-mini-map').setView([d.lat, d.lng], 11);
        L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(miniMap);
        
        dayLayerGroups = {};
        beachLayerGroup = L.layerGroup().addTo(miniMap);

        if (d.itinerary && d.itinerary.length > 0) {
            const roadTrip = d.itinerary.filter(s => typeof s.day === 'number').sort((a,b) => a.day - b.day);
            const dayList = [...new Set(roadTrip.map(s => s.day))];
            let legendHTML = `<div class="legend-item legend-day-link" onclick="filterDay('all')">🗺️ Full Route</div>`;

            dayList.forEach((day, index) => {
                const color = dayColors[index % dayColors.length];
                dayLayerGroups[day] = L.layerGroup().addTo(miniMap);
                
                let segment = roadTrip.filter(s => s.day === day);
                if (segment.length >= 2) {
                    const coords = segment.map(p => `${p.lng},${p.lat}`).join(';');
                    fetch(`https://router.project-osrm.org/route/v1/driving/${coords}?overview=full&geometries=geojson`)
                        .then(r => r.json())
                        .then(rd => {
                            L.geoJSON(rd.routes[0].geometry, {style:{color:color, weight:6, opacity:0.8}}).addTo(dayLayerGroups[day]);
                        });
                }
                legendHTML += `<div class="legend-item legend-day-link" onclick="filterDay(${day})"><span class="line-sample" style="background:${color}"></span>Day ${day}</div>`;
            });

            d.itinerary.forEach(stop => {
                let emoji = stop.name.toLowerCase().includes("port") ? "⚓" : (stop.name.toLowerCase().includes("airport") ? "✈️" : (stop.day === "Beach" ? "🏖️" : "🏛️"));
                const marker = L.marker([stop.lat, stop.lng], {
                    icon: L.divIcon({ html: `<div style="font-size:22px;">${emoji}</div>`, className: 'custom-pin', iconAnchor: [11, 11] })
                }).bindTooltip(stop.name);
                if (typeof stop.day === 'number') marker.addTo(dayLayerGroups[stop.day]);
                else marker.addTo(beachLayerGroup);
            });

            const mL = L.control({ position: 'topright' });
            mL.onAdd = () => { const div = L.DomUtil.create('div', 'mini-legend'); div.innerHTML = legendHTML; return div; };
            mL.addTo(miniMap);
            miniMap.fitBounds(L.latLngBounds(roadTrip.map(p => [p.lat, p.lng])), { padding: [50, 50] });
        }
    }, 300);
}

function filterDay(day) { 
    Object.values(dayLayerGroups).forEach(g => miniMap.removeLayer(g)); 
    beachLayerGroup.addTo(miniMap); // Beaches always stay
    if (day === 'all') Object.values(dayLayerGroups).forEach(g => g.addTo(miniMap)); 
    else dayLayerGroups[day].addTo(miniMap); 
}

function toggleMenu() { document.getElementById('main-nav').classList.toggle('active'); }
function jumpMap(key) { handleNav('home'); mainMap.setView([islandData[key].lat, islandData[key].lng], 11); markerStore[key].marker.openTooltip(); }
function generateTable() {
    const tbody = document.getElementById('islands-table-body');
    if (!tbody) return;
    tbody.innerHTML = "";
    Object.keys(islandData).forEach(k => {
        const d = islandData[k];
        const row = tbody.insertRow();
        row.insertCell(0).innerHTML = `<a class="island-link" onclick="jumpMap('${k}')">${d.name}</a>`;
        row.insertCell(1).innerText = d.island_group || '-';
        row.insertCell(2).innerHTML = renderStars(getScore(d, 'overall'));
        row.insertCell(3).innerHTML = renderStars(d.beach);
        row.insertCell(4).innerHTML = renderStars(d.hist);
        row.insertCell(5).innerHTML = renderStars(d.night);
        row.insertCell(6).innerHTML = renderStars(d.access);
        row.insertCell(7).innerHTML = renderStars(d.afford);
        const areaCell = row.insertCell(8); areaCell.innerText = d.area ? d.area.toLocaleString() : '-'; areaCell.className = 'text-right';
        const popCell = row.insertCell(9); popCell.innerText = d.pop ? d.pop.toLocaleString() : '-'; popCell.className = 'text-right';
    });
}
function renderStars(rating) { const r = Math.round(rating || 0); return `<span class="table-stars">${"★".repeat(r)}${"☆".repeat(5-r)}</span>`; }
function sortTable(n) {
    if (n === currentSortCol) { sortDir *= -1; } else { currentSortCol = n; sortDir = (n < 2) ? 1 : -1; }
    const keys = ['name','island_group','total','beach','hist','night','access','afford','area','pop'];
    const sorted = Object.keys(islandData).sort((a,b) => {
        let vA = islandData[a][keys[n]] || 0, vB = islandData[b][keys[n]] || 0;
        return (typeof vA === 'string') ? vA.localeCompare(vB) * sortDir : (vA - vB) * sortDir;
    });
    const newData = {}; sorted.forEach(k => newData[k] = islandData[k]);
    islandData = newData; generateTable();
}
function updateMapMode(m) { currentMode = m; document.querySelectorAll('.vibe-chip').forEach(el => el.classList.remove('active')); document.getElementById('btn-' + m).classList.add('active'); renderMarkers(); updateLegendContent(document.querySelector('.info.legend')); }
function filterIslands() { const q = document.getElementById('islandSearch').value.toLowerCase(); Object.keys(markerStore).forEach(k => { markerStore[k].marker.setOpacity(markerStore[k].data.name.toLowerCase().includes(q) ? 1 : 0.1); }); }
