const VERSION_ID = "v14.0 - JSON Architecture Live";
let mainMap, miniMap;
let markerLayerGroup; 
const markerStore = {}; 
let currentMode = 'overall';
let islandData = {}; // Will be filled by the fetch

// 1. FETCH DATA FROM JSON FILE
window.onload = function() {
    // Safety check: Only update the version if the element exists
    const versionEl = document.getElementById('version-display');
    if (versionEl) {
        versionEl.innerText = VERSION_ID;
    }

    // Fetch the data and load the map
    fetch('data.json?v=' + new Date().getTime())
        .then(response => response.json())
        .then(data => {
            islandData = data;
            initMap();
        })
        .catch(error => {
            console.error("Error loading island data:", error);
            alert("Warning: Could not load the island data. Check your data.json file for typos!");
        });
};

function initMap() {
    const bounds = L.latLngBounds([34.0, 18.5], [42.0, 30.5]);
    mainMap = L.map('main-map', { minZoom: 7, maxZoom: 12, maxBounds: bounds, maxBoundsViscosity: 1.0 }).setView([38.3, 24.5], 7);
    
    // NEW MINIMALIST TILE LAYER
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap &copy; CARTO'
    }).addTo(mainMap);
    
    markerLayerGroup = L.layerGroup().addTo(mainMap);
    renderMarkers();
}

function getColor(score) {
    if (score >= 4.0) return "#27ae60"; 
    if (score >= 3.5) return "#2ecc71"; 
    if (score >= 3.0) return "#f1c40f"; 
    return "#e67e22"; 
}

function updateTooltip(marker, data, currentScore) {
    marker.bindTooltip(`
        <div class="leaflet-tooltip-island">
            <strong>${data.name}</strong><br>
            <span>Rating: ${currentScore}</span>
        </div>
    `, { sticky: true });
}

function renderMarkers() {
    markerLayerGroup.clearLayers();
    
    // UPGRADED STAR: Larger font, heavy black shadow for massive contrast
    const starIcon = L.divIcon({
        html: '<div style="font-size: 28px; color: #ffcc00; text-shadow: 2px 2px 5px rgba(0,0,0,0.8);">⭐</div>',
        className: 'star-icon', 
        iconSize: [30, 30], 
        iconAnchor: [15, 15] // Keeps the star perfectly centered on the coordinates
    });

    Object.keys(islandData).forEach(id => {
        const d = islandData[id];
        const score = (currentMode === 'overall') ? d.overall : d[currentMode];
        
        // UPGRADED DOTS: Larger radius, dark grey border instead of white, fully opaque
        let marker = (score >= 4.0) 
            ? L.marker([d.lat, d.lng], { icon: starIcon }) 
            : L.circleMarker([d.lat, d.lng], { 
                radius: 12, 
                fillColor: getColor(score), 
                color: "#2c3e50", // Dark slate border for high contrast
                weight: 3,        // Thicker border
                fillOpacity: 1.0 
            });

        marker.addTo(markerLayerGroup);
        updateTooltip(marker, d, score);
        marker.on('click', () => showDetail(id));
        markerStore[id] = { marker, data: d, isStar: (score >= 4.0) };
    });
}

function updateMapMode(mode) {
    showHome(); 
    currentMode = mode;
    document.querySelectorAll('.vibe-chip').forEach(el => el.classList.remove('active'));
    document.getElementById('btn-' + mode).classList.add('active');
    
    const titles = {overall: 'Best Overall', beach: 'Beach Lovers', hist: 'Culture Buffs', night: 'Party Animals', access: 'Accessibility', afford: 'Affordability'};
    document.getElementById('legend-title').innerText = titles[mode];
    renderMarkers();
    filterIslands(); 
}

function showDetail(id) {
    const d = islandData[id];
    document.getElementById('home-view').style.display = 'none';
    document.getElementById('detail-view').style.display = 'block';
    window.scrollTo(0,0);
    
    document.getElementById('island-name').innerText = d.name;
    document.getElementById('island-total-score').innerText = d.overall;
    document.getElementById('island-pic').src = d.img || "https://images.unsplash.com/photo-1516483638261-f4dbaf036963?w=1200";
    document.getElementById('island-guide').innerHTML = d.guide || "";
    
    setStars('star-beach', d.beach); setStars('star-hist', d.hist); setStars('star-night', d.night); setStars('star-access', d.access); setStars('star-afford', d.afford);
    
if (miniMap) miniMap.remove();
    miniMap = L.map('island-mini-map', { zoomControl: false, scrollWheelZoom: false });
    
    // NEW MINIMALIST TILE LAYER FOR MINI-MAP
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap &copy; CARTO'
    }).addTo(miniMap);

    // DYNAMIC ITINERARY DRAWING LOGIC
    if (d.itinerary && d.itinerary.length > 0) {
        // Extract coordinates into an array
        const routeCoords = d.itinerary.map(stop => [stop.lat, stop.lng]);
        
        // Draw the driving route line
        const drivingRoute = L.polyline(routeCoords, {
            color: '#ff7f50', weight: 4, dashArray: '5, 10'
        }).addTo(miniMap);

        // Drop markers on the stops
        d.itinerary.forEach(stop => {
            const stopMarker = L.circleMarker([stop.lat, stop.lng], {
                radius: 6, fillColor: '#005BAE', color: '#fff', weight: 2, fillOpacity: 1
            }).addTo(miniMap);
            stopMarker.bindTooltip(`Day ${stop.day}: ${stop.name}`, {permanent: true, direction: 'right'});
        });

        // Automatically zoom map to fit the entire route
        miniMap.fitBounds(drivingRoute.getBounds(), { padding: [30, 30] });
    } else {
        // Default behavior if no itinerary exists yet
        miniMap.setView([d.lat, d.lng], d.zoom || 11);
        L.marker([d.lat, d.lng]).addTo(miniMap);
    }
}

function setStars(id, val) { document.getElementById(id).style.width = (val / 5 * 100) + "%"; }
function showHome() { document.getElementById('home-view').style.display = 'block'; document.getElementById('detail-view').style.display = 'none'; if(mainMap) setTimeout(() => mainMap.invalidateSize(), 200); }
function filterIslands() {
    const q = document.getElementById('islandSearch').value.toLowerCase();
    Object.keys(markerStore).forEach(k => {
        const m = markerStore[k].data.name.toLowerCase().includes(q);
        const item = markerStore[k];
        if (item.isStar) { item.marker.setOpacity(m ? 1 : 0.1); } 
        else { item.marker.setStyle({ opacity: m ? 1 : 0.1, fillOpacity: m ? 0.95 : 0.1 }); }
    });
}
