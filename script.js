const VERSION_ID = "v37.0 - Mission Page Fix";
let mainMap, miniMap, markerLayerGroup, legendControl;
const markerStore = {};
let currentMode = 'overall';
let islandData = {};

window.onload = function() {
    document.getElementById('version-display').innerText = VERSION_ID;
    initMap();
    fetch('map_data.json?v=' + new Date().getTime())
        .then(res => res.json())
        .then(data => { islandData = data; renderMarkers(); });
};

function initMap() {
    mainMap = L.map('main-map', { zoomControl: false }).setView([38.3, 24.5], 7);
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

// UI NAVIGATION FUNCTIONS
function hideAllViews() {
    document.getElementById('home-view').style.display = 'none';
    document.getElementById('detail-view').style.display = 'none';
    document.getElementById('mission-view').style.display = 'none';
    document.getElementById('hopping-view').style.display = 'none';
    document.body.classList.add('subpage-active'); // Hides the search container
}

function showHome() {
    hideAllViews();
    document.body.classList.remove('subpage-active'); // Shows the search container
    document.getElementById('home-view').style.display = 'block';
    if(mainMap) setTimeout(() => mainMap.invalidateSize(), 200);
}

function showMission() {
    hideAllViews();
    document.getElementById('mission-view').style.display = 'block';
    window.scrollTo(0, 0);
}

function showHopping() {
    hideAllViews();
    document.getElementById('hopping-view').style.display = 'block';
    window.scrollTo(0, 0);
}

function showDetail(id) {
    hideAllViews();
    document.getElementById('detail-view').style.display = 'block';
    document.getElementById('island-name').innerText = islandData[id].name;
    window.scrollTo(0, 0);
    
    fetch(`islands/${id}.json?v=` + new Date().getTime())
        .then(res => res.json())
        .then(d_detail => renderDetailView(Object.assign({}, islandData[id], d_detail)))
        .catch(() => alert("Guide under development."));
}

// ... Rest of your renderDetailView, updateMapMode, and filterIslands logic remains the same ...

function updateLegendContent(div) {
    const title = currentMode.charAt(0).toUpperCase() + currentMode.slice(1);
    div.innerHTML = `<strong>${title} Level</strong><br>` +
        `<div class="legend-item">⭐ Elite (4.1+)</div>` +
        `<div class="legend-item"><span class="dot" style="background:#2ecc71"></span> High (3.5+)</div>` +
        `<div class="legend-item"><span class="dot" style="background:#f1c40f"></span> Average (3.0+)</div>` +
        `<div class="legend-item"><span class="dot" style="background:#e67e22"></span> Niche (<3.0)</div>`;
}

function getColor(score) {
    if (score >= 4.1) return "#27ae60";
    if (score >= 3.5) return "#2ecc71";
    if (score >= 3.0) return "#f1c40f";
    return "#e67e22";
}

function renderMarkers() {
    markerLayerGroup.clearLayers();
    const starIcon = L.divIcon({
        html: '<div style="font-size: 26px; color: #fbbf24;">⭐</div>',
        className: 'star-icon', iconSize: [30, 30], iconAnchor: [15, 15]
    });

    Object.keys(islandData).forEach(id => {
        const d = islandData[id];
        const score = (currentMode === 'overall') ? d.overall : d[currentMode];
        let marker = (score >= 4.1) 
            ? L.marker([d.lat, d.lng], { icon: starIcon }) 
            : L.circleMarker([d.lat, d.lng], { radius: 9, fillColor: getColor(score), color: "#fff", weight: 2, fillOpacity: 1 });

        marker.addTo(markerLayerGroup).on('click', () => showDetail(id));
        marker.bindTooltip(`<strong>${d.name}</strong>`, { sticky: true });
        markerStore[id] = { marker, data: d, isStar: (score >= 4.1) };
    });
}
