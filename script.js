const VERSION_ID = "v55.0 - Ultimate Layout Build";
let mainMap, miniMap, markerLayerGroup, legendControl;
let currentMode = 'overall';
let islandData = {};
const dayColors = ['#005BAE', '#10b981', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4'];
let markerStore = {};
let currentSortCol = 2; 
let sortDir = -1;
let dayLayerGroups = {};

window.onload = function() {
    document.getElementById('version-display').innerText = VERSION_ID;
    initMap();
    fetch('islands_master.json?v=' + Date.now())
        .then(res => res.json())
        .then(data => { 
            islandData = data; 
            renderMarkers(); 
            generateTable(); 
            handleInitialRouting();
        });
};

window.onhashchange = function() { handleInitialRouting(); };

function initMap() {
    mainMap = L.map('main-map', { zoomControl: false, minZoom: 6 }).setView([38.3, 24.5], 7);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(mainMap);
    markerLayerGroup = L.layerGroup().addTo(mainMap);
    legendControl = L.control({ position: 'bottomleft' }); 
    legendControl.onAdd = () => {
        let div = L.DomUtil.create('div', 'info legend');
        setTimeout(() => updateLegendContent(div), 100);
        return div;
    };
    legendControl.addTo(mainMap);
}

function handleInitialRouting() {
    const hash = window.location.hash.replace('#', '');
    if (!hash || hash === 'home') handleNav('home', false);
    else if (islandData[hash]) showDetail(hash, false);
    else handleNav('home', false);
}

function updateLegendContent(div) {
    const target = div || document.querySelector('.info.legend');
    if (!target) return;
    target.innerHTML = `<strong>${currentMode.toUpperCase()} TIER</strong><br>` +
        `<div class="legend-item">⭐ Elite Top 10</div>` +
        `<div class="legend-item"><span class="dot" style="background:#005BAE"></span> High</div>` +
        `<div class="legend-item"><span class="dot" style="background:#f1c40f"></span> Avg</div>` +
        `<div class="legend-item"><span class="dot" style="background:#e67e22"></span> Niche</div>`;
}

function renderMarkers() {
    markerLayerGroup.clearLayers();
    const sorted = Object.keys(islandData).sort((a,b) => (islandData[b].total || 0) - (islandData[a].total || 0));
    const top10 = sorted.slice(0, 10);
    const starIcon = L.divIcon({ html: '<div style="font-size:24px; color:#fbbf24;">⭐</div>', className:'star-icon', iconSize:[30,30], iconAnchor:[15,15] });

    Object.keys(islandData).forEach(id => {
        const d = islandData[id];
        const score = (currentMode === 'overall' ? d.total : d[currentMode]) || 0;
        const color = score >= 3.5 ? "#005BAE" : (score >= 3.0 ? "#f1c40f" : "#e67e22");
        let marker = top10.includes(id) ? L.marker([d.lat, d.lng], {icon: starIcon}) : L.circleMarker([d.lat, d.lng], {radius:9, fillColor:color, color:"#fff", weight:2, fillOpacity:1});
        marker.addTo(markerLayerGroup).on('click', () => showDetail(id));
        marker.bindTooltip(`<strong>${d.name}</strong><br>${currentMode}: ${score.toFixed(1)}`);
        markerStore[id] = { marker, data: d };
    });
}

function showDetail(id, updateHash = true) { 
    handleNav('detail', false); 
    if (updateHash) window.location.hash = id;
    const d = islandData[id];
    
    // UI RECOVERY
    document.getElementById('island-name').innerText = d.name; 
    document.getElementById('stat-area').innerText = d.area ? d.area + " km²" : "-";
    document.getElementById('stat-pop').innerText = d.pop ? d.pop.toLocaleString() : "-";
    document.getElementById('stat-group').innerText = d.island_group || "Other";
    document.getElementById('island-meta-info').innerText = (d.island_group || "Greek Island") + " • " + (d.total || 0).toFixed(1) + " Total Score";

    ['beach','hist','night','access','afford'].forEach(c => {
        const bar = document.getElementById(`star-${c}`);
        if (bar) bar.style.width = ((d[c] || 0)/5*100) + "%";
    });

    fetch(`islands/${id}.json?v=` + Date.now()).then(res => res.json()).then(d_detail => {
        renderDetailView(Object.assign({}, d, d_detail));
    }).catch(() => renderDetailView(Object.assign({}, d, { guide: "Blueprint coming soon." })));
}

function renderDetailView(d) {
    document.getElementById('island-guide').innerHTML = d.guide || "";
    if (miniMap) miniMap.remove();
    setTimeout(() => {
        miniMap = L.map('island-mini-map').setView([d.lat, d.lng], 11);
        L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(miniMap);
        miniMap.invalidateSize();
        
        if (d.itinerary) {
            const roadTrip = d.itinerary.filter(s => typeof s.day === 'number').sort((a,b) => a.day - b.day);
            let legHTML = `<div class="legend-item legend-day-link" onclick="filterDay('all')">🗺️ Full Route</div>`;
            dayLayerGroups = {};
            [...new Set(roadTrip.map(s => s.day))].forEach((day, idx) => {
                const color = dayColors[idx % dayColors.length];
                dayLayerGroups[day] = L.layerGroup().addTo(miniMap);
                let segment = roadTrip.filter(s => s.day === day);
                if (segment.length >= 2) {
                    const coords = segment.map(p => `${p.lng},${p.lat}`).join(';');
                    fetch(`https://router.project-osrm.org/route/v1/driving/${coords}?overview=full&geometries=geojson`)
                        .then(r => r.json()).then(rd => L.geoJSON(rd.routes[0].geometry, {style:{color:color, weight:6}}).addTo(dayLayerGroups[day]));
                }
                legHTML += `<div class="legend-item legend-day-link" onclick="filterDay(${day})"><span class="line-sample" style="background:${color}"></span>Day ${day}</div>`;
            });
            const mL = L.control({ position: 'topright' });
            mL.onAdd = () => { const div = L.DomUtil.create('div', 'mini-legend'); div.innerHTML = legHTML; return div; };
            mL.addTo(miniMap);
            miniMap.fitBounds(L.latLngBounds(roadTrip.map(p => [p.lat, p.lng])), { padding: [40, 40] });
        }
    }, 250);
}

function filterDay(day) { Object.values(dayLayerGroups).forEach(g => miniMap.removeLayer(g)); if (day === 'all') Object.values(dayLayerGroups).forEach(g => g.addTo(miniMap)); else dayLayerGroups[day].addTo(miniMap); }
function handleNav(t, updateHash = true) { 
    document.querySelectorAll('.view-section').forEach(v => v.style.display = 'none');
    document.getElementById('home-controls').style.display = (t === 'home') ? 'flex' : 'none';
    const targetView = document.getElementById('view-' + t);
    if (targetView) targetView.style.display = 'block';
    if (updateHash) window.location.hash = t;
    if (t === 'home' && mainMap) setTimeout(() => mainMap.invalidateSize(), 100);
    window.scrollTo(0,0);
}
function toggleMenu() { document.getElementById('main-nav').classList.toggle('active'); }
function generateTable() {
    const tbody = document.getElementById('islands-table-body');
    if (!tbody) return;
    tbody.innerHTML = "";
    Object.keys(islandData).forEach(k => {
        const d = islandData[k];
        const row = tbody.insertRow();
        row.insertCell(0).innerHTML = `<a class="island-link" onclick="jumpMap('${k}')">${d.name}</a>`;
        row.insertCell(1).innerText = d.island_group || '-';
        row.insertCell(2).innerHTML = renderStars(d.total || 0);
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
function jumpMap(key) { handleNav('home'); mainMap.setView([islandData[key].lat, islandData[key].lng], 11); }
function updateMapMode(m) { currentMode = m; renderMarkers(); updateLegendContent(); }
function filterIslands() { const q = document.getElementById('islandSearch').value.toLowerCase(); Object.keys(markerStore).forEach(k => { markerStore[k].marker.setOpacity(markerStore[k].data.name.toLowerCase().includes(q) ? 1 : 0.1); }); }
