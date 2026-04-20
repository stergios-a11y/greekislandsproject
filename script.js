const VERSION_ID = "v50.0 - Pro Menu & Stars";
let mainMap, miniMap, markerLayerGroup, legendControl;
let currentMode = 'overall';
let islandData = {};
let currentSortCol = 2; // Default to Total
let sortDir = -1; // Default to Descending

window.onload = function() {
    document.getElementById('version-display').innerText = VERSION_ID;
    initMap();
    fetch('islands_master.json?v=' + new Date().getTime())
        .then(res => res.json())
        .then(data => { 
            islandData = data; 
            renderMarkers(); 
            generateTable(); 
        });
};

function toggleMenu() {
    document.getElementById('main-nav').classList.toggle('active');
}

function handleNav(target) {
    switchView(target);
    document.getElementById('main-nav').classList.remove('active'); // Auto-close on click
}

// HELPERS
function renderStars(rating) {
    const rounded = Math.round(rating);
    return `<span class="table-stars">${"★".repeat(rounded)}${"☆".repeat(5 - rounded)}</span>`;
}

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
        row.insertCell(3).innerHTML = renderStars(d.beach || 0);
        row.insertCell(4).innerHTML = renderStars(d.hist || 0);
        row.insertCell(5).innerHTML = renderStars(d.night || 0);
        row.insertCell(6).innerHTML = renderStars(d.access || 0);
        row.insertCell(7).innerHTML = renderStars(d.afford || 0);
        row.insertCell(8).innerText = d.area ? d.area.toLocaleString() : '-';
        row.insertCell(9).innerText = d.pop ? d.pop.toLocaleString() : '-';
    });
}

function sortTable(n) {
    if (n === currentSortCol) { sortDir *= -1; } else { currentSortCol = n; sortDir = (n === 0 || n === 1) ? 1 : -1; }
    const keysArr = ['name','island_group','total','beach','hist','night','access','afford','area','pop'];
    const sortedKeys = Object.keys(islandData).sort((a,b) => {
        let valA = islandData[a][keysArr[n]];
        let valB = islandData[b][keysArr[n]];
        if (typeof valA === 'string') return valA.localeCompare(valB) * sortDir;
        return (valA - valB) * sortDir;
    });
    const newData = {};
    sortedKeys.forEach(k => { newData[k] = islandData[k]; });
    islandData = newData;
    generateTable();
}

function switchView(target) {
    document.querySelectorAll('.view-section').forEach(v => v.style.display = 'none');
    document.getElementById('home-controls').style.display = target === 'home' ? 'flex' : 'none';
    document.getElementById('view-' + target).style.display = 'block';
    if (target === 'home' && mainMap) setTimeout(() => mainMap.invalidateSize(), 200);
    window.scrollTo(0,0);
}

function initMap() {
    mainMap = L.map('main-map', { zoomControl: false, minZoom: 6 }).setView([38.3, 24.5], 7);
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
    div.innerHTML = `<strong>${currentMode.toUpperCase()}</strong><br>` +
        `<div class="legend-item">⭐ Top 10</div>` +
        `<div class="legend-item"><span class="dot" style="background:#005BAE"></span> High</div>` +
        `<div class="legend-item"><span class="dot" style="background:#f1c40f"></span> Average</div>` +
        `<div class="legend-item"><span class="dot" style="background:#e67e22"></span> Niche</div>`;
}

function renderMarkers() {
    markerLayerGroup.clearLayers();
    const sorted = Object.keys(islandData).sort((a,b) => (islandData[b][currentMode === 'overall' ? 'total' : currentMode] || 0) - (islandData[a][currentMode === 'overall' ? 'total' : currentMode] || 0));
    const top10 = sorted.slice(0, 10);
    const starIcon = L.divIcon({ html: '<div style="font-size:26px; color:#fbbf24; text-shadow:0 2px 4px rgba(0,0,0,0.3);">⭐</div>', className:'star-icon', iconSize:[30,30], iconAnchor:[15,15] });

    Object.keys(islandData).forEach(id => {
        const d = islandData[id];
        const score = (currentMode === 'overall' ? d.total : d[currentMode]) || 0;
        const isElite = top10.includes(id);
        const color = score >= 3.5 ? "#005BAE" : (score >= 3.0 ? "#f1c40f" : "#e67e22");
        let marker = isElite ? L.marker([d.lat, d.lng], {icon: starIcon}) : L.circleMarker([d.lat, d.lng], {radius:9, fillColor:color, color:"#fff", weight:2, fillOpacity:1});
        marker.addTo(markerLayerGroup).on('click', () => showDetail(id));
        marker.bindTooltip(`<strong>${d.name}</strong><br>${currentMode}: ${score.toFixed(1)}`);
        markerStore[id] = { marker, data: d };
    });
}

function jumpMap(key) { switchView('home'); mainMap.setView([islandData[key].lat, islandData[key].lng], 11); markerStore[key].marker.openTooltip(); }
function updateMapMode(m) { currentMode = m; document.querySelectorAll('.vibe-chip').forEach(el => el.classList.remove('active')); document.getElementById('btn-' + m).classList.add('active'); renderMarkers(); }
function filterIslands() { const q = document.getElementById('islandSearch').value.toLowerCase(); Object.keys(markerStore).forEach(k => { markerStore[k].marker.setOpacity(markerStore[k].data.name.toLowerCase().includes(q) ? 1 : 0.1); }); }
