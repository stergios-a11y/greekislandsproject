const VERSION_ID = "v47.0 PRO - Database Launch";
let mainMap, miniMap, markerLayerGroup, legendControl;
const markerStore = {};
let currentMode = 'overall';
let islandData = {};
const dayColors = ['#005BAE', '#10b981', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4'];
let dayLayerGroups = {};
let beachLayerGroup;
let currentSortColumn = 0;
let sortDirection = 1;

window.onload = function() {
    document.getElementById('version-display').innerText = VERSION_ID;
    initMap();
    fetch('islands_master.json?v=' + new Date().getTime())
        .then(res => res.json())
        .then(data => { 
            islandData = data; 
            renderMarkers(); 
            generateDataPage(); 
        });
};

function initMap() {
    mainMap = L.map('main-map', { zoomControl: false, minZoom: 6, maxZoom: 13 }).setView([38.3, 24.5], 7);
    L.control.zoom({ position: 'topright' }).addTo(mainMap);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(mainMap);
    markerLayerGroup = L.layerGroup().addTo(mainMap);
    legendControl = L.control({ position: 'bottomleft' }); 
    legendControl.onAdd = function() {
        let div = L.DomUtil.create('div', 'info legend');
        updateLegendContent(div);
        return div;
    };
    legendControl.addTo(mainMap);
}

function updateLegendContent(div) {
    const title = currentMode.charAt(0).toUpperCase() + currentMode.slice(1);
    div.innerHTML = `<strong>${title} Tier</strong><br>` +
        `<div class="legend-item"><span style="font-size:16px; margin-right:6px;">⭐</span> Elite (Top 10)</div>` +
        `<div class="legend-item"><span class="dot" style="background:#005BAE"></span> High (3.5+)</div>` +
        `<div class="legend-item"><span class="dot" style="background:#f1c40f"></span> Average (3.0+)</div>` +
        `<div class="legend-item"><span class="dot" style="background:#e67e22"></span> Niche (<3.0)</div>`;
}

function getColor(score) {
    if (score >= 3.5) return "#005BAE"; 
    if (score >= 3.0) return "#f1c40f"; 
    return "#e67e22"; 
}

function renderMarkers() {
    if (!markerLayerGroup) return;
    markerLayerGroup.clearLayers();
    const sorted = Object.keys(islandData).sort((a,b) => islandData[b][currentMode === 'overall' ? 'total' : currentMode] - islandData[a][currentMode === 'overall' ? 'total' : currentMode]);
    const top10Ids = sorted.slice(0, 10);
    const starIcon = L.divIcon({ html: '<div style="font-size:26px; color:#fbbf24; text-shadow:0 2px 4px rgba(0,0,0,0.3);">⭐</div>', className:'star-icon', iconSize:[30,30], iconAnchor:[15,15] });

    Object.keys(islandData).forEach(id => {
        const d = islandData[id];
        const score = currentMode === 'overall' ? d.total : d[currentMode];
        const isElite = top10Ids.includes(id);
        let marker = isElite ? L.marker([d.lat, d.lng], {icon:starIcon}) : L.circleMarker([d.lat, d.lng], {radius:9, fillColor:getColor(score), color:"#fff", weight:2, fillOpacity:1});
        marker.addTo(markerLayerGroup).on('click', () => showDetail(id));
        marker.bindTooltip(`<strong>${d.name}</strong><br>${currentMode.toUpperCase()}: ${score.toFixed(1)}`, {sticky:true});
        markerStore[id] = { marker, data: d, isElite };
    });
}

function generateDataPage() {
    const tableBody = document.getElementById('islands-table-body');
    tableBody.innerHTML = "";
    Object.keys(islandData).forEach(key => {
        const d = islandData[key];
        const row = tableBody.insertRow();
        row.insertCell(0).innerHTML = `<a class="island-link" onclick="jumpToIslandOnMap('${key}')">${d.name}</a>`;
        row.insertCell(1).innerText = d.island_group || 'Other';
        row.insertCell(2).innerText = (d.total || 0).toFixed(1);
        row.insertCell(3).innerText = (d.beach || 0).toFixed(1);
        row.insertCell(4).innerText = (d.hist || 0).toFixed(1);
        row.insertCell(5).innerText = (d.night || 0).toFixed(1);
        row.insertCell(6).innerText = (d.access || 0).toFixed(1);
        row.insertCell(7).innerText = (d.afford || 0).toFixed(1);
        row.insertCell(8).innerText = d.area ? d.area.toLocaleString() : '-';
        row.insertCell(9).innerText = d.pop ? d.pop.toLocaleString() : '-';
    });
}

function sortTable(n) {
    if (n === currentSortColumn) { sortDirection *= -1; } else { currentSortColumn = n; sortDirection = 1; }
    const keys = Object.keys(islandData);
    const sortedKeys = keys.sort((a,b) => {
        let valA, valB;
        const keysArr = ['name','island_group','total','beach','hist','night','access','afford','area','pop'];
        valA = islandData[a][keysArr[n]]; valB = islandData[b][keysArr[n]];
        if (typeof valA === 'string') return valA.localeCompare(valB) * sortDirection;
        return (valA - valB) * sortDirection;
    });
    const sortedData = {}; sortedKeys.forEach(k => { sortedData[k] = islandData[k]; });
    islandData = sortedData; generateDataPage();
}

function jumpToIslandOnMap(key) { showHome(); mainMap.setView([islandData[key].lat, islandData[key].lng], 11); markerStore[key].marker.openTooltip(); }

function showHome() { document.body.classList.remove('subpage-active'); document.getElementById('home-view').style.display = 'block'; document.getElementById('detail-view').style.display='none'; document.getElementById('mission-view').style.display='none'; document.getElementById('hopping-view').style.display='none'; document.getElementById('data-view').style.display='none'; if(mainMap) setTimeout(() => mainMap.invalidateSize(), 200); }
function showMission() { showHome(); document.getElementById('home-view').style.display = 'none'; document.getElementById('mission-view').style.display = 'block'; }
function showHopping() { showHome(); document.getElementById('home-view').style.display = 'none'; document.getElementById('hopping-view').style.display = 'block'; }
function showDataPage() { showHome(); document.getElementById('home-view').style.display = 'none'; document.getElementById('data-view').style.display = 'block'; }

function showDetail(id) {
    showHome(); document.getElementById('home-view').style.display = 'none'; document.getElementById('detail-view').style.display = 'block'; document.getElementById('island-name').innerText = islandData[id].name;
    fetch(`islands/${id}.json?v=` + new Date().getTime()).then(res => res.json()).then(d_detail => renderDetailView(Object.assign({}, islandData[id], d_detail))).catch(() => renderDetailView(Object.assign({}, islandData[id], { guide: "Itinerary coming soon." })));
}

function renderDetailView(d) {
    document.getElementById('island-guide').innerHTML = d.guide || "";
    const cats = ['beach','hist','night','access','afford'];
    cats.forEach(c => { const el = document.getElementById(`star-${c}`); if(el) el.style.width = (d[c]/5*100) + "%"; });
    if (miniMap) miniMap.remove();
    miniMap = L.map('island-mini-map').setView([d.lat, d.lng], 11);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(miniMap);
    dayLayerGroups = {}; beachLayerGroup = L.layerGroup().addTo(miniMap);
    if (d.itinerary) {
        const roadTrip = d.itinerary.filter(s => typeof s.day === 'number').sort((a,b) => a.day - b.day);
        let legendHTML = `<div class="legend-item legend-day-link" onclick="filterDay('all')">🗺️ Full Route</div>`;
        [...new Set(roadTrip.map(s => s.day))].forEach((day, idx) => {
            const color = dayColors[idx % dayColors.length];
            dayLayerGroups[day] = L.layerGroup().addTo(miniMap);
            let segment = roadTrip.filter(s => s.day === day);
            if (segment.length >= 2) {
                fetch(`https://router.project-osrm.org/route/v1/driving/${segment.map(p => `${p.lng},${p.lat}`).join(';')}?overview=full&geometries=geojson`)
                    .then(r => r.json()).then(rd => { L.geoJSON(rd.routes[0].geometry, {style:{color:color, weight:6}}).addTo(dayLayerGroups[day]); });
            }
            legendHTML += `<div class="legend-item legend-day-link" onclick="filterDay(${day})"><span class="line-sample" style="background:${color}"></span>Day ${day}</div>`;
        });
        const mL = L.control({ position: 'topright' });
        mL.onAdd = () => { const div = L.DomUtil.create('div', 'mini-legend'); div.innerHTML = legendHTML; return div; };
        mL.addTo(miniMap);
    }
}

function filterDay(day) { Object.values(dayLayerGroups).forEach(g => miniMap.removeLayer(g)); if (day === 'all') Object.values(dayLayerGroups).forEach(g => g.addTo(miniMap)); else dayLayerGroups[day].addTo(miniMap); }
function updateMapMode(m) { currentMode = m; document.querySelectorAll('.vibe-chip').forEach(el => el.classList.remove('active')); document.getElementById('btn-' + m).classList.add('active'); updateLegendContent(document.querySelector('.info.legend')); renderMarkers(); }
function filterIslands() { const q = document.getElementById('islandSearch').value.toLowerCase(); Object.keys(markerStore).forEach(k => { markerStore[k].marker.setOpacity(markerStore[k].data.name.toLowerCase().includes(q) ? 1 : 0.1); }); }
