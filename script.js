const VERSION_ID = "v18.0 - Pro Transport Hubs";

let mainMap, miniMap;
let markerLayerGroup; 
const markerStore = {}; 
let currentMode = 'overall';
let islandData = {}; 

window.onload = function() {
    const versionEl = document.getElementById('version-display');
    if (versionEl) versionEl.innerText = VERSION_ID;

    initMap();

    fetch('map_data.json?v=' + new Date().getTime())
        .then(response => {
            if (!response.ok) throw new Error("Map data missing.");
            return response.json();
        })
        .then(data => {
            islandData = data;
            renderMarkers(); 
        })
        .catch(error => console.error("Load Error:", error));
};

function initMap() {
    const bounds = L.latLngBounds([34.0, 18.5], [42.0, 30.5]);
    mainMap = L.map('main-map', { 
        minZoom: 7, 
        maxZoom: 12, 
        maxBounds: bounds, 
        maxBoundsViscosity: 1.0 
    }).setView([38.3, 24.5], 7);
    
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', { 
        attribution: '&copy; CARTO' 
    }).addTo(mainMap);
    
    markerLayerGroup = L.layerGroup().addTo(mainMap);
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
        html: '<div style="font-size: 28px; color: #ffcc00; text-shadow: 2px 2px 5px rgba(0,0,0,0.8);">⭐</div>',
        className: 'star-icon', iconSize: [30, 30], iconAnchor: [15, 15] 
    });

    Object.keys(islandData).forEach(id => {
        const d = islandData[id];
        const score = (currentMode === 'overall') ? d.overall : d[currentMode];
        let marker = (score >= 4.1) 
            ? L.marker([d.lat, d.lng], { icon: starIcon }) 
            : L.circleMarker([d.lat, d.lng], { radius: 12, fillColor: getColor(score), color: "#2c3e50", weight: 3, fillOpacity: 1.0 });

        marker.addTo(markerLayerGroup);
        marker.bindTooltip(`<strong>${d.name}</strong><br>Rating: ${score}`, { sticky: true });
        marker.on('click', () => showDetail(id));
        markerStore[id] = { marker, data: d, isStar: (score >= 4.1) };
    });
}

function showDetail(id) {
    const d_base = islandData[id];
    const homeView = document.getElementById('home-view');
    const detailView = document.getElementById('detail-view');
    const nameLabel = document.getElementById('island-name');

    if (!homeView || !detailView) return;

    homeView.style.display = 'none';
    detailView.style.display = 'block';
    window.scrollTo(0,0);
    if (nameLabel) nameLabel.innerText = d_base.name;
    
    fetch(`islands/${id}.json?v=` + new Date().getTime())
        .then(res => res.json())
        .then(d_detail => {
            const d = Object.assign({}, d_base, d_detail);
            renderDetailView(d);
        })
        .catch(() => {
            const fallback = Object.assign({}, d_base, {
                img: "https://images.unsplash.com/photo-1516483638261-f4dbaf036963?w=1200",
                guide: "<div style='background:#fff3cd; padding:20px; border-radius:8px; border:2px dashed #ffc107;'><h2>🚧 Guide Coming Soon</h2></div>",
                itinerary: []
            });
            renderDetailView(fallback);
        });
}

function renderDetailView(d) {
    document.getElementById('island-total-score').innerText = d.overall;
    document.getElementById('island-pic').src = d.img;
    document.getElementById('island-guide').innerHTML = d.guide;
    
    setStars('star-beach', d.beach); 
    setStars('star-hist', d.hist); 
    setStars('star-night', d.night); 
    setStars('star-access', d.access); 
    setStars('star-afford', d.afford);
    
    if (miniMap) miniMap.remove();
    miniMap = L.map('island-mini-map', { zoomControl: false, scrollWheelZoom: false });
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(miniMap);

    if (d.itinerary && d.itinerary.length > 0) {
        const roadTripPoints = d.itinerary.filter(stop => typeof stop.day === 'number');

        // Draw Real Road Routing
        if (roadTripPoints.length >= 2) {
            const coordsString = roadTripPoints.map(p => `${p.lng},${p.lat}`).join(';');
            fetch(`https://router.project-osrm.org/route/v1/driving/${coordsString}?overview=full&geometries=geojson`)
                .then(r => r.json())
                .then(routeData => {
                    const roadLine = L.geoJSON(routeData.routes[0].geometry, {
                        style: { color: '#ff7f50', weight: 5, opacity: 0.8, dashArray: '10, 15' }
                    }).addTo(miniMap);
                    miniMap.fitBounds(roadLine.getBounds(), { padding: [50, 50] });
                });
        } else {
            miniMap.setView([d.lat, d.lng], 10);
        }

        // Add Markers with Special Symbols
        d.itinerary.forEach(stop => {
            let iconEmoji = "📍";
            const stopName = stop.name.toLowerCase();
            
            if (stop.day === "Beach") iconEmoji = "🏖️";
            if (stopName.includes("airport")) iconEmoji = "✈️";
            if (stopName.includes("port")) iconEmoji = "⚓";
            if (stopName.includes("hotel") || stopName.includes("stay")) iconEmoji = "🏨";

            L.marker([stop.lat, stop.lng], {
                icon: L.divIcon({
                    html: `<div style="font-size:22px; filter: drop-shadow(0 0 2px white);">${iconEmoji}</div>`,
                    className: 'custom-pin',
                    iconAnchor: [11, 11]
                })
            }).addTo(miniMap).bindTooltip(`<strong>${stop.name}</strong>`);
        });
    } else {
        miniMap.setView([d.lat, d.lng], 11);
        L.marker([d.lat, d.lng]).addTo(miniMap);
    }
}

function setStars(id, val) { 
    const el = document.getElementById(id);
    if (el) el.style.width = (val / 5 * 100) + "%"; 
}

function showHome() { 
    document.getElementById('home-view').style.display = 'block'; 
    document.getElementById('detail-view').style.display = 'none'; 
    if(mainMap) setTimeout(() => mainMap.invalidateSize(), 200); 
}

function updateMapMode(mode) {
    showHome(); 
    currentMode = mode;
    document.querySelectorAll('.vibe-chip').forEach(el => el.classList.remove('active'));
    document.getElementById('btn-' + mode).classList.add('active');
    document.getElementById('legend-title').innerText = mode.charAt(0).toUpperCase() + mode.slice(1);
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
