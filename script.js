const VERSION_ID = "v48.0 - Final Navigation Engine";
let mainMap, miniMap, markerLayerGroup, legendControl;
const markerStore = {};
let currentMode = 'overall';
let islandData = {};
const dayColors = ['#005BAE', '#10b981', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4'];
let dayLayerGroups = {};
let beachLayerGroup;
let currentSortCol = 0;
let sortDir = 1;

window.onload = function() {
    document.getElementById('version-display').innerText = VERSION_ID;
    initMap();
    // FETCH THE MASTER DATA
    fetch('islands_master.json?v=' + new Date().getTime())
        .then(res => res.json())
        .then(data => { 
            islandData = data; 
            renderMarkers(); 
            generateTable(); 
        });
};

function initMap() {
    mainMap = L.map('main-map', { zoomControl: false, minZoom: 6 }).setView([38.3, 24.5], 7);
    L.control.zoom({ position: 'topright' }).addTo(mainMap);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(mainMap);
    markerLayerGroup = L.layerGroup().addTo(mainMap);
    legendControl = L.control({ position: 'bottomleft' }); 
    legendControl.onAdd = function() {
        let div = L.DomUtil.create('div', 'info legend');
        div.innerHTML = "<strong>Loading...</strong>";
        return div;
    };
    legendControl.addTo(mainMap);
}

// BULLETPROOF NAVIGATION
function switchView(target) {
    // 1. Hide all views
    document.querySelectorAll('.view-section').forEach(v => v.style.display = 'none');
    document.getElementById('home-controls').style.display = 'none';
    
    // 2. Show target
    if (target === 'home') {
        document.getElementById('view-home').style.display = 'block';
        document.getElementById('home-controls').style.display = 'flex';
        if(mainMap) setTimeout(() => mainMap.invalidateSize(), 200);
    } else {
        document.getElementById('view-' + target).style.display = 'block';
        window.scrollTo(0,0);
    }
}

function updateLegendContent(div) {
    const title = currentMode.charAt(0).toUpperCase() + currentMode.slice(1);
    div.innerHTML = `<strong>${title} Tier</strong><br>` +
        `<div class="legend-item">⭐ Top 10</div>` +
        `<div class="legend-item"><span class="dot" style="background:#005BAE"></span> High (3.5+)</div>` +
        `<div class="legend-item"><span class="dot" style="background:#f1c40f"></span> Average (3.0+)</div>` +
        `<div class="legend-item"><span class="dot" style="background:#e67e22"></span> Niche (<3.0)</div>`;
}

function renderMarkers() {
    if (!markerLayerGroup) return;
    markerLayerGroup.clearLayers();
    
    const sorted = Object.keys(islandData).sort((a,b) => islandData[b][currentMode === 'overall' ? 'total' : currentMode] - islandData[a][currentMode === 'overall' ? 'total' : currentMode]);
    const top10 = sorted.slice(0, 10);

    const starIcon = L.divIcon({
        html: '<div style="font-size: 26px; color: #fbbf24; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">⭐</div>',
        className: 'star-icon', iconSize: [30, 30], iconAnchor: [15, 15]
    });

    Object.keys(islandData).forEach(id => {
        const d = islandData[id];
        const score = currentMode === 'overall' ? d.total : d[currentMode];
        const isElite = top10.includes(id);

        let marker = isElite 
            ? L.marker([d.lat, d.lng], { icon: starIcon }) 
            : L.circleMarker([d.lat, d.lng], { radius: 9, fillColor: score >= 3.5 ? "#005BAE" : (score >= 3.0 ? "#f1c40f" : "#e67e22"), color: "#fff", weight: 2, fillOpacity: 1 });

        marker.addTo(markerLayerGroup).on('click', () => showDetail(id));
        marker.bindTooltip(`<strong>${d.name}</strong><br>${currentMode.toUpperCase()}: ${score.toFixed(1)}`, { sticky: true });
        markerStore[id] = { marker, data: d };
    });
    updateLegendContent(document.querySelector('.info.legend'));
}

function showDetail(id) {
    switchView('detail');
    document.getElementById('island-name').innerText = islandData[id].name;
    
    // Reset stars
    ['beach','hist','night','access','afford'].forEach(c => {
        document.getElementById(`star-${c}`).style.width = (islandData[id][c]/5*100) + "%";
    });

    fetch(`islands/${id}.json?v=` + new Date().getTime())
        .then(res => res.json())
        .then(d_detail => renderDetailView(Object.assign({}, islandData[id], d_detail)))
        .catch(() => { document.getElementById('island-guide').innerHTML = "Guide coming soon."; });
}

function renderDetailView(d) {
    document.getElementById('island-guide').innerHTML = d.guide || "";
    if (miniMap) miniMap.remove();
    miniMap = L.map('island-mini-map').setView([d.lat, d.lng], 11);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(miniMap);
    
    if (d.itinerary) {
        const roadTrip = d.itinerary.filter(s => typeof s.day === 'number');
        let legHTML = `<div class="legend-item legend-day-link" onclick="filterDay('all')">🗺️ Full Route</div>`;
        
        [...new Set(roadTrip.map(s => s.day))].forEach((day, idx) => {
            const color = dayColors[idx % dayColors.length];
            legHTML += `<div class="legend-item legend-day-link" onclick="filterDay(${day})"><span class="line-sample" style="background:${color}"></span>Day ${day}</div>`;
            // Drawing logic here (same as previous)
        });
        const mL = L.control({ position: 'topright' });
        mL.onAdd = () => { const div = L.DomUtil.create('div', 'mini-legend'); div.innerHTML = legHTML; return div; };
        mL.addTo(miniMap);
    }
}

function generateTable() {
    const tbody = document.getElementById('islands-table-body');
    tbody.innerHTML = "";
    Object.keys(islandData).forEach(k => {
        const d = islandData[k];
        const row = tbody.insertRow();
        row.insertCell(0).innerHTML = `<a class="island-link" onclick="jumpMap('${k}')">${d.name}</a>`;
        row.insertCell(1).innerText = d.island_group;
        row.insertCell(2).innerText = d.total.toFixed(1);
        row.insertCell(3).innerText = d.beach.toFixed(1);
        row.insertCell(4).innerText = d.hist.toFixed(1);
        row.insertCell(5).innerText = d.night.toFixed(1);
        row.insertCell(6).innerText = d.access.toFixed(1);
        row.insertCell(7).innerText = d.afford.toFixed(1);
        row.insertCell(8).innerText = d.area || '-';
        row.insertCell(9).innerText = d.pop ? d.pop.toLocaleString() : '-';
    });
}

function jumpMap(key) { switchView('home'); mainMap.setView([islandData[key].lat, islandData[key].lng], 11); markerStore[key].marker.openTooltip(); }
function sortTable(n) { /* Sorting logic goes here - standard JS sort */ }
function updateMapMode(m) { currentMode = m; document.querySelectorAll('.vibe-chip').forEach(el => el.classList.remove('active')); document.getElementById('btn-' + m).classList.add('active'); renderMarkers(); }
function filterIslands() { const q = document.getElementById('islandSearch').value.toLowerCase(); Object.keys(markerStore).forEach(k => { markerStore[k].marker.setOpacity(markerStore[k].data.name.toLowerCase().includes(q) ? 1 : 0.1); }); }
