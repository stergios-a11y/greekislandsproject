const VERSION_ID = "v21.0 - Optimized Engine";
let mainMap, miniMap, markerLayerGroup;
const markerStore = {};
let currentMode = 'overall';
let islandData = {};

window.onload = function() {
    document.getElementById('version-display').innerText = VERSION_ID;
    initMap();
    // Cache buster included to ensure new scores/data load instantly
    fetch('map_data.json?v=' + new Date().getTime())
        .then(res => res.json())
        .then(data => { 
            islandData = data; 
            renderMarkers(); 
        });
};

function initMap() {
    // Main map initialization
    mainMap = L.map('main-map').setView([38.3, 24.5], 7);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; CARTO'
    }).addTo(mainMap);
    markerLayerGroup = L.layerGroup().addTo(mainMap);
}

function getColor(score) {
    if (score >= 4.1) return "#27ae60"; // Elite
    if (score >= 3.5) return "#2ecc71"; // High
    if (score >= 3.0) return "#f1c40f"; // Average
    return "#e67e22"; // Niche
}

function renderMarkers() {
    markerLayerGroup.clearLayers();
    const starIcon = L.divIcon({
        html: '<div style="font-size: 28px; color: #ffcc00; text-shadow: 2px 2px 5px rgba(0,0,0,0.8);">⭐</div>',
        className: 'star-icon', iconSize: [30, 30], iconAnchor: [15, 15]
    });

    Object.keys(islandData).forEach(id => {
        const d = islandData[id];
        const score = (currentMode === 'overall') ? d.overall : d[currentMode];
        
        let marker = (score >= 4.1) 
            ? L.marker([d.lat, d.lng], { icon: starIcon }) 
            : L.circleMarker([d.lat, d.lng], { radius: 12, fillColor: getColor(score), color: "#2c3e50", weight: 3, fillOpacity: 1.0 });

        marker.addTo(markerLayerGroup).on('click', () => showDetail(id));
        marker.bindTooltip(`<strong>${d.name}</strong><br>Rating: ${score}`, { sticky: true });
        markerStore[id] = { marker, data: d, isStar: (score >= 4.1) };
    });
}

function showDetail(id) {
    const homeView = document.getElementById('home-view');
    const detailView = document.getElementById('detail-view');
    const nameLabel = document.getElementById('island-name');

    homeView.style.display = 'none';
    detailView.style.display = 'block';
    nameLabel.innerText = islandData[id].name;
    window.scrollTo(0,0);
    
    fetch(`islands/${id}.json?v=` + new Date().getTime())
        .then(res => res.json())
        .then(d_detail => {
            // Combine basic map data with the deep guide data
            const fullData = Object.assign({}, islandData[id], d_detail);
            renderDetailView(fullData);
        })
        .catch(() => alert("Island guide under construction!"));
}

function renderDetailView(d) {
    // Update UI elements
    document.getElementById('island-pic').src = d.img;
    document.getElementById('island-guide').innerHTML = d.guide;
    
    // Optimized star rendering (Consolidated from 15 lines down to 3)
    ['beach', 'hist', 'night', 'access', 'afford'].forEach(cat => {
        const el = document.getElementById(`star-${cat}`);
        if (el) el.style.width = (d[cat] / 5 * 100) + "%";
    });

    // Reset and Setup Mini-Map
    if (miniMap) miniMap.remove();
    miniMap = L.map('island-mini-map', { zoomControl: true, scrollWheelZoom: true });
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(miniMap);

    if (d.itinerary && d.itinerary.length > 0) {
        const roadTrip = d.itinerary.filter(s => typeof s.day === 'number');
        
        // Fetch Real-Road Routing from OSRM
        if (roadTrip.length >= 2) {
            const coords = roadTrip.map(p => `${p.lng},${p.lat}`).join(';');
            fetch(`https://router.project-osrm.org/route/v1/driving/${coords}?overview=full&geometries=geojson`)
                .then(r => r.json())
                .then(route => {
                    const line = L.geoJSON(route.routes[0].geometry, { 
                        style: { color: '#ff7f50', weight: 4, opacity: 0.8, dashArray: '8, 12' } 
                    }).addTo(miniMap);
                    // High padding forces the map to zoom out to show everything
                    miniMap.fitBounds(line.getBounds(), { padding: [150, 150] });
                });
        }

        // Drop Pins with Icon Priority Logic
        d.itinerary.forEach(stop => {
            let emoji = "📍";
            const n = stop.name.toLowerCase();
            
            if (n.includes("airport")) emoji = "✈️";
            else if (n.includes("port") && !n.includes("airport")) emoji = "⚓";
            else if (stop.day === "Beach") emoji = "🏖️";
            else if (n.includes("hotel") || n.includes("stay") || n.includes("base")) emoji = "🏨";

            L.marker([stop.lat, stop.lng], {
                icon: L.divIcon({ 
                    html: `<div style="font-size:24px; filter: drop-shadow(0 0 3px white); cursor: pointer;">${emoji}</div>`, 
                    className: 'custom-pin', 
                    iconAnchor: [12, 12] 
                })
            }).addTo(miniMap).bindTooltip(`<strong>${stop.name}</strong>`);
        });
    }
}

function showHome() { 
    document.getElementById('home-view').style.display = 'block'; 
    document.getElementById('detail-view').style.display = 'none'; 
    // Fix for Leaflet tiles not loading correctly after resize
    if(mainMap) setTimeout(() => mainMap.invalidateSize(), 200);
}

function updateMapMode(mode) {
    currentMode = mode;
    document.querySelectorAll('.vibe-chip').forEach(el => el.classList.remove('active'));
    document.getElementById('btn-' + mode).classList.add('active');
    renderMarkers();
}

function filterIslands() {
    const q = document.getElementById('islandSearch').value.toLowerCase();
    Object.keys(markerStore).forEach(k => {
        const match = markerStore[k].data.name.toLowerCase().includes(q);
        const item = markerStore[k];
        if (item.isStar) { 
            item.marker.setOpacity(match ? 1 : 0.1); 
        } else { 
            item.marker.setStyle({ opacity: match ? 1 : 0.1, fillOpacity: match ? 0.95 : 0.1 }); 
        }
    });
}
