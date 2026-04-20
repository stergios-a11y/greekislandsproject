const VERSION_ID = "v33.0 - Dynamic UI Filtering";
let mainMap, miniMap, markerLayerGroup, legendControl;
const markerStore = {};
let currentMode = 'overall';
let islandData = {};

const dayColors = ['#3498db', '#2ecc71', '#9b59b6', '#f39c12', '#e74c3c', '#1abc9c'];
let dayLayerGroups = {};
let beachLayerGroup;

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
    
    L.control.scale({ imperial: false, position: 'bottomleft' }).addTo(mainMap);
    
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
    div.innerHTML = `<strong>${title} Level</strong><br>` +
        `<div class="legend-item"><span style="font-size:14px; margin-right:8px;">⭐</span> Elite (4.1+)</div>` +
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

function showDetail(id) {
    // Hide Main Map and Search/Filters
    document.getElementById('home-view').style.display = 'none';
    document.querySelector('.search-container').style.display = 'none';
    
    // Show Island Detail
    document.getElementById('detail-view').style.display = 'block';
    document.getElementById('island-name').innerText = islandData[id].name;
    window.scrollTo(0,0);
    
    fetch(`islands/${id}.json?v=` + new Date().getTime())
        .then(res => res.json())
        .then(d_detail => renderDetailView(Object.assign({}, islandData[id], d_detail)))
        .catch(() => alert("Guide under development."));
}

function filterDay(day) {
    Object.values(dayLayerGroups).forEach(group => miniMap.removeLayer(group));
    miniMap.removeLayer(beachLayerGroup);

    if (day === 'all') {
        Object.values(dayLayerGroups).forEach(group => group.addTo(miniMap));
        beachLayerGroup.addTo(miniMap);
        const allLayers = L.featureGroup(Object.values(dayLayerGroups).concat(beachLayerGroup));
        miniMap.fitBounds(allLayers.getBounds(), { padding: [50, 50] });
    } else {
        dayLayerGroups[day].addTo(miniMap);
        miniMap.fitBounds(dayLayerGroups[day].getBounds(), { padding: [100, 100] });
    }
}

function renderDetailView(d) {
    document.getElementById('island-pic').src = d.img;
    document.getElementById('island-guide').innerHTML = d.guide;
    ['beach', 'hist', 'night', 'access', 'afford'].forEach(cat => {
        const el = document.getElementById(`star-${cat}`);
        if(el) el.style.width = (d[cat] / 5 * 100) + "%";
    });

    if (miniMap) miniMap.remove();
    miniMap = L.map('island-mini-map', { zoomControl: true, scrollWheelZoom: true });
    
    L.control.scale({ imperial: false, position: 'bottomleft' }).addTo(miniMap);
    
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(miniMap);

    dayLayerGroups = {};
    beachLayerGroup = L.layerGroup().addTo(miniMap);

    if (d.itinerary && d.itinerary.length > 0) {
        const roadTrip = d.itinerary.filter(s => typeof s.day === 'number').sort((a,b) => a.day - b.day);
        const dayList = [...new Set(roadTrip.map(s => s.day))];

        let miniLegendHTML = `<div class="legend-item legend-day-link" onclick="filterDay('all')" style="margin-bottom:10px;"><strong>🗺️ Full Route</strong></div>`;

        dayList.forEach((day, index) => {
            const color = dayColors[index % dayColors.length];
            dayLayerGroups[day] = L.layerGroup().addTo(miniMap);
            
            let segmentPoints = [];
            if (index > 0) {
                const prevDayPoints = roadTrip.filter(s => s.day === dayList[index - 1]);
                segmentPoints.push(prevDayPoints[prevDayPoints.length - 1]);
            }
            const currentDayPoints = roadTrip.filter(s => s.day === day);
            segmentPoints = segmentPoints.concat(currentDayPoints);

            if (segmentPoints.length >= 2) {
                const coords = segmentPoints.map(p => `${p.lng},${p.lat}`).join(';');
                fetch(`https://router.project-osrm.org/route/v1/driving/${coords}?overview=full&geometries=geojson`)
                    .then(r => r.json())
                    .then(routeData => {
                        const route = routeData.routes[0];
                        const km = (route.distance / 1000).toFixed(1);
                        const mins = Math.round(route.duration / 60);
                        const hours = Math.floor(mins / 60);
                        const displayTime = hours > 0 ? `${hours}h ${mins % 60}m` : `${mins} min`;

                        L.geoJSON(route.geometry, { style: { color: color, weight: 6, opacity: 0.9 } }).addTo(dayLayerGroups[day]);
                        const statsEl = document.getElementById(`stats-day-${day}`);
                        if (statsEl) statsEl.innerText = `${km}km • ${displayTime}`;
                    });
            }

            miniLegendHTML += `
                <div class="legend-item legend-day-link" onclick="filterDay(${day})">
                    <span class="line-sample" style="background:${color}"></span>
                    <span>Day ${day}</span>
                </div>
                <span class="day-stats" id="stats-day-${day}">...</span>`;
        });

        d.itinerary.forEach(stop => {
            let emoji = "🏛️";
            const n = stop.name.toLowerCase();
            if (n.includes("airport")) emoji = "✈️";
            else if (n.includes("port") && !n.includes("airport")) emoji = "⚓";
            else if (stop.day === "Beach") emoji = "🏖️";
            else if (n.includes("springs")) emoji = "♨️";
            else if (n.includes("monastery") || n.includes("moni")) emoji = "⛪";
            else if (n.includes("hotel") || n.includes("stay")) emoji = "🏨";
            else if (n.includes("distillery") || n.includes("ouzo")) emoji = "🥃";
            else if (n.includes("forest") || n.includes("salt") || n.includes("museum")) emoji = "📷";

            const marker = L.marker([stop.lat, stop.lng], {
                icon: L.divIcon({ html: `<div style="font-size:22px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));">${emoji}</div>`, className: 'custom-pin', iconAnchor: [11, 11] })
            }).bindTooltip(stop.name);

            if (typeof stop.day === 'number') marker.addTo(dayLayerGroups[stop.day]);
            else marker.addTo(beachLayerGroup);
        });

        const miniLegend = L.control({ position: 'topright' });
        miniLegend.onAdd = () => {
            const div = L.DomUtil.create('div', 'mini-legend');
            div.innerHTML = miniLegendHTML;
            return div;
        };
        miniLegend.addTo(miniMap);
        
        const allPoints = roadTrip.map(p => [p.lat, p.lng]);
        miniMap.fitBounds(L.latLngBounds(allPoints), { padding: [80, 80] });
    }
}

function showHome() { 
    // Show Main Map and Search/Filters
    document.getElementById('home-view').style.display = 'block'; 
    document.querySelector('.search-container').style.display = 'flex';
    
    // Hide Island Detail
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
        else item.marker.setStyle({ opacity: match ? 1 : 0.1, fillOpacity: match ? 1 : 0.1 });
    });
}
