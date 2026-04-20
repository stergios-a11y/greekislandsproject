const VERSION_ID = "v24.0 - Multi-Color Day Routing";
let mainMap, miniMap, markerLayerGroup, legendControl;
const markerStore = {};
let currentMode = 'overall';
let islandData = {};

// Color palette for itinerary days
const dayColors = ['#3498db', '#2ecc71', '#9b59b6', '#f39c12', '#e74c3c', '#1abc9c'];

window.onload = function() {
    document.getElementById('version-display').innerText = VERSION_ID;
    initMap();
    fetch('map_data.json?v=' + new Date().getTime())
        .then(res => res.json())
        .then(data => { islandData = data; renderMarkers(); });
};

function initMap() {
    mainMap = L.map('main-map').setView([38.3, 24.5], 7);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(mainMap);
    markerLayerGroup = L.layerGroup().addTo(mainMap);

    legendControl = L.control({ position: 'bottomright' });
    legendControl.onAdd = function() {
        let div = L.DomUtil.create('div', 'info legend');
        updateLegendContent(div);
        return div;
    };
    legendControl.addTo(mainMap);
}

function updateLegendContent(div) {
    const title = currentMode.charAt(0).toUpperCase() + currentMode.slice(1);
    div.innerHTML = `<strong>${title} Rating</strong><br>` +
        `<div class="legend-item"><span class="dot" style="background:#27ae60"></span> Elite (4.1+)</div>` +
        `<div class="legend-item"><span class="dot" style="background:#2ecc71"></span> High (3.5+)</div>` +
        `<div class="legend-item"><span class="dot" style="background:#f1c40f"></span> Avg (3.0+)</div>` +
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
        html: '<div style="font-size: 26px; color: #ffcc00; text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">⭐</div>',
        className: 'star-icon', iconSize: [30, 30], iconAnchor: [15, 15]
    });

    Object.keys(islandData).forEach(id => {
        const d = islandData[id];
        const score = (currentMode === 'overall') ? d.overall : d[currentMode];
        let marker = (score >= 4.1) 
            ? L.marker([d.lat, d.lng], { icon: starIcon }) 
            : L.circleMarker([d.lat, d.lng], { radius: 10, fillColor: getColor(score), color: "#fff", weight: 2, fillOpacity: 0.9 });

        marker.addTo(markerLayerGroup).on('click', () => showDetail(id));
        marker.bindTooltip(`<strong>${d.name}</strong>: ${score}`, { sticky: true });
        markerStore[id] = { marker, data: d, isStar: (score >= 4.1) };
    });
}

function showDetail(id) {
    document.getElementById('home-view').style.display = 'none';
    document.getElementById('detail-view').style.display = 'block';
    document.getElementById('island-name').innerText = islandData[id].name;
    window.scrollTo(0,0);
    
    fetch(`islands/${id}.json?v=` + new Date().getTime())
        .then(res => res.json())
        .then(d_detail => renderDetailView(Object.assign({}, islandData[id], d_detail)))
        .catch(() => alert("Guide not found."));
}

function renderDetailView(d) {
    document.getElementById('island-pic').src = d.img;
    document.getElementById('island-guide').innerHTML = d.guide;
    ['beach', 'hist', 'night', 'access', 'afford'].forEach(cat => {
        document.getElementById(`star-${cat}`).style.width = (d[cat] / 5 * 100) + "%";
    });

    if (miniMap) miniMap.remove();
    miniMap = L.map('island-mini-map', { zoomControl: true, scrollWheelZoom: true });
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(miniMap);

    if (d.itinerary && d.itinerary.length > 0) {
        const roadTrip = d.itinerary.filter(s => typeof s.day === 'number').sort((a,b) => a.day - b.day);
        
        // 1. Multi-Color Routing Logic
        if (roadTrip.length >= 2) {
            let miniLegendHTML = `<strong>Itinerary Routes</strong><br>`;
            const dayList = [...new Set(roadTrip.map(s => s.day))];
            
            dayList.forEach((day, index) => {
                const color = dayColors[index % dayColors.length];
                const dayPoints = roadTrip.filter(s => s.day === day);
                
                // If it's the start, or we need to connect from the previous day's last point
                let segmentPoints = [];
                if (index > 0) {
                    const prevDayPoints = roadTrip.filter(s => s.day === dayList[index - 1]);
                    segmentPoints.push(prevDayPoints[prevDayPoints.length - 1]);
                }
                segmentPoints = segmentPoints.concat(dayPoints);

                if (segmentPoints.length >= 2) {
                    const coords = segmentPoints.map(p => `${p.lng},${p.lat}`).join(';');
                    fetch(`https://router.project-osrm.org/route/v1/driving/${coords}?overview=full&geometries=geojson`)
                        .then(r => r.json())
                        .then(route => {
                            L.geoJSON(route.routes[0].geometry, { 
                                style: { color: color, weight: 5, opacity: 0.8 } 
                            }).addTo(miniMap);
                        });
                }
                miniLegendHTML += `<div class="legend-item"><span class="line-sample" style="background:${color}"></span> Day ${day}</div>`;
            });

            // Add Mini Legend to Map
            const miniLegend = L.control({ position: 'topright' });
            miniLegend.onAdd = () => {
                const div = L.DomUtil.create('div', 'mini-legend');
                div.innerHTML = miniLegendHTML;
                return div;
            };
            miniLegend.addTo(miniMap);

            // Set Initial View
            const allCoords = roadTrip.map(p => [p.lat, p.lng]);
            miniMap.fitBounds(L.latLngBounds(allCoords), { padding: [80, 80] });
        }

        // 2. Drop Markers
        d.itinerary.forEach(stop => {
            let emoji = "🏛️";
            const n = stop.name.toLowerCase();
            if (n.includes("airport")) emoji = "✈️";
            else if (n.includes("port") && !n.includes("airport")) emoji = "⚓";
            else if (stop.day === "Beach") emoji = "🏖️";
            else if (n.includes("hotel") || n.includes("stay")) emoji = "🏨";
            else if (n.includes("forest") || n.includes("salt") || n.includes("wetlands")) emoji = "📷";

            L.marker([stop.lat, stop.lng], {
                icon: L.divIcon({ html: `<div style="font-size:22px; filter: drop-shadow(0 0 2px white);">${emoji}</div>`, className: 'custom-pin', iconAnchor: [11, 11] })
            }).addTo(miniMap).bindTooltip(stop.name);
        });
    }
}

function showHome() { 
    document.getElementById('home-view').style.display = 'block'; 
    document.getElementById('detail-view').style.display = 'none'; 
    if(mainMap) setTimeout(() => mainMap.invalidateSize(), 200);
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
        else item.marker.setStyle({ opacity: match ? 1 : 0.1, fillOpacity: match ? 0.9 : 0.1 });
    });
}
