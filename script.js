const VERSION_ID = "v39.0 - Final Navigation & Map Restore";
let mainMap, miniMap, markerLayerGroup, legendControl;
const markerStore = {};
let currentMode = 'overall';
let islandData = {};

window.onload = function() {
    document.getElementById('version-display').innerText = VERSION_ID;
    initMap();
    // Replace with your actual data fetching if needed, or use the 80 island JSON provided previously
    fetch('map_data.json?v=' + new Date().getTime())
        .then(res => res.json())
        .then(data => { 
            islandData = data; 
            renderMarkers(); 
        })
        .catch(err => console.error("Could not load island data:", err));
};

function initMap() {
    const mapDiv = document.getElementById('main-map');
    if (!mapDiv) return;

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

function hideAll() {
    document.getElementById('home-view').style.display = 'none';
    document.getElementById('detail-view').style.display = 'none';
    document.getElementById('mission-view').style.display = 'none';
    document.getElementById('hopping-view').style.display = 'none';
    document.body.classList.add('subpage-active');
}

function showHome() {
    hideAll();
    document.body.classList.remove('subpage-active');
    document.getElementById('home-view').style.display = 'block';
    if(mainMap) {
        setTimeout(() => {
            mainMap.invalidateSize();
        }, 200);
    }
}

function showMission() {
    hideAll();
    document.getElementById('mission-view').style.display = 'block';
    window.scrollTo(0,0);
}

function showHopping() {
    hideAll();
    document.getElementById('hopping-view').style.display = 'block';
    window.scrollTo(0,0);
}

function showDetail(id) {
    hideAll();
    document.getElementById('detail-view').style.display = 'block';
    document.getElementById('island-name').innerText = islandData[id].name;
    window.scrollTo(0,0);
    
    fetch(`islands/${id}.json?v=` + new Date().getTime())
        .then(res => res.json())
        .then(d_detail => renderDetailView(Object.assign({}, islandData[id], d_detail)))
        .catch(() => console.log("Itinerary data not found for " + id));
}

function updateLegendContent(div) {
    const title = currentMode.charAt(0).toUpperCase() + currentMode.slice(1);
    div.innerHTML = `<strong>${title} Level</strong><br>` +
        `<div class="legend-item"><span style="font-size:14px; margin-right:5px;">⭐</span> Elite (4.1+)</div>` +
        `<div class="legend-item"><span class="dot" style="background:#3b82f6"></span> High (3.5+)</div>` +
        `<div class="legend-item"><span class="dot" style="background:#f1c40f"></span> Average (3.0+)</div>` +
        `<div class="legend-item"><span class="dot" style="background:#e67e22"></span> Niche (<3.0)</div>`;
}

function getColor(score) {
    if (score >= 4.1) return "#27ae60";
    if (score >= 3.5) return "#3b82f6";
    if (score >= 3.0) return "#f1c40f";
    return "#e67e22";
}

function renderMarkers() {
    if (!markerLayerGroup) return;
    markerLayerGroup.clearLayers();
    
    const starIcon = L.divIcon({
        html: '<div style="font-size: 26px; color: #fbbf24; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">⭐</div>',
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

function updateMapMode(mode) {
    currentMode = mode;
    document.querySelectorAll('.vibe-chip').forEach(el => el.classList.remove('active'));
    document.getElementById('btn-' + mode).classList.add('active');
    const legendDiv = document.querySelector('.info.legend');
    if (legendDiv) updateLegendContent(legendDiv);
    renderMarkers();
}

function filterIslands() {
    const q = document.getElementById('islandSearch').value.toLowerCase();
    Object.keys(markerStore).forEach(k => {
        const match = markerStore[k].data.name.toLowerCase().includes(q);
        const item = markerStore[k];
        if (item.isStar) item.marker.setOpacity(match ? 1 : 0.1);
        else item.marker.setStyle({ opacity: match ? 1 : 0.1, fillOpacity: match ? 1 : 0.1 });
    });
}

function renderDetailView(d) {
    document.getElementById('island-pic').src = d.img || "";
    document.getElementById('island-guide').innerHTML = d.guide || "Itinerary coming soon.";
    ['beach', 'hist', 'night', 'access', 'afford'].forEach(cat => {
        const el = document.getElementById(`star-${cat}`);
        if(el) el.style.width = (d[cat] / 5 * 100) + "%";
    });

    if (miniMap) miniMap.remove();
    miniMap = L.map('island-mini-map', { zoomControl: true });
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(miniMap);
    
    // Check if there is itinerary data to plot
    if (d.itinerary && d.itinerary.length > 0) {
        const points = d.itinerary.map(p => [p.lat, p.lng]);
        miniMap.fitBounds(L.latLngBounds(points), { padding: [40, 40] });
        
        d.itinerary.forEach(stop => {
             L.marker([stop.lat, stop.lng]).addTo(miniMap).bindTooltip(stop.name);
        });
    } else {
        miniMap.setView([d.lat, d.lng], 11);
    }
}
