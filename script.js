const VERSION_ID = "v53.1 - Mac Support Build";
let mainMap, miniMap, markerLayerGroup, legendControl;
let currentMode = 'overall';
let islandData = {};
const dayColors = ['#005BAE', '#10b981', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4'];
let markerStore = {};
let currentSortCol = 2; 
let sortDir = -1;

window.onload = function() {
    document.getElementById('version-display').innerText = VERSION_ID;
    initMap();
    // Use Cache-Busting to force fresh data load
    fetch('islands_master.json?v=' + Date.now())
        .then(res => res.json())
        .then(data => { 
            console.log("Database successfully loaded.");
            islandData = data; 
            renderMarkers(); 
            generateTable(); 
        }).catch(err => {
            console.error("CRITICAL: Failed to load islands_master.json. Check file name and JSON syntax.", err);
        });
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
    
    // Sort to find Top 10
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

function renderStars(rating) {
    const r = Math.round(rating || 0);
    return `<span class="table-stars">${"★".repeat(r)}${"☆".repeat(5-r)}</span>`;
}

function handleNav(t) { 
    document.querySelectorAll('.view-section').forEach(v => v.style.display = 'none');
    document.getElementById('home-controls').style.display = (t === 'home') ? 'flex' : 'none';
    document.getElementById('view-' + t).style.display = 'block';
    document.getElementById('main-nav').classList.remove('active');
    if (t === 'home' && mainMap) setTimeout(() => mainMap.invalidateSize(), 200);
    window.scrollTo(0,0);
}

function toggleMenu() { document.getElementById('main-nav').classList.toggle('active'); }
function jumpMap(key) { handleNav('home'); mainMap.setView([islandData[key].lat, islandData[key].lng], 11); markerStore[key].marker.openTooltip(); }

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

function updateMapMode(m) { 
    currentMode = m; 
    document.querySelectorAll('.vibe-chip').forEach(el => el.classList.remove('active'));
    document.getElementById('btn-' + m).classList.add('active'); 
    renderMarkers(); 
    updateLegendContent(document.querySelector('.info.legend')); 
}

function filterIslands() { 
    const q = document.getElementById('islandSearch').value.toLowerCase(); 
    Object.keys(markerStore).forEach(k => { 
        markerStore[k].marker.setOpacity(markerStore[k].data.name.toLowerCase().includes(q) ? 1 : 0.1); 
    }); 
}

function showDetail(id) { 
    handleNav('detail'); 
    document.getElementById('island-name').innerText = islandData[id].name; 
    fetch(`islands/${id}.json?v=`+Date.now()).then(res=>res.json()).then(d_detail=>{
        document.getElementById('island-guide').innerHTML = d_detail.guide || "";
        if(miniMap) miniMap.remove();
        miniMap = L.map('island-mini-map').setView([islandData[id].lat, islandData[id].lng], 11);
        L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(miniMap);
    }).catch(() => document.getElementById('island-guide').innerHTML = "Guide coming soon.");
}
