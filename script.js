const VERSION_ID = "v46.0 PRO - Top 10 Engine";
let mainMap, miniMap, markerLayerGroup, legendControl;
const markerStore = {};
let currentMode = 'overall';
let islandData = {};
const dayColors = ['#005BAE', '#10b981', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4'];
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
    // MAX ZOOM OUT TO SEE GREECE + SLIGHT BUFFER
    mainMap = L.map('main-map', { 
        zoomControl: false,
        minZoom: 6,
        maxZoom: 14
    }).setView([38.3, 24.5], 7);
    
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

function updateLegendContent(div) {
    div.innerHTML = `<strong>${currentMode.toUpperCase()}</strong><br>` +
        `<div class="legend-item"><span style="font-size:14px; margin-right:5px;">⭐</span> Top 10</div>` +
        `<div class="legend-item"><span class="dot" style="background:#005BAE"></span> High</div>` +
        `<div class="legend-item"><span class="dot" style="background:#f1c40f"></span> Average</div>` +
        `<div class="legend-item"><span class="dot" style="background:#e67e22"></span> Niche</div>`;
}

function getColor(score) {
    if (score >= 4.1) return "#10b981";
    if (score >= 3.5) return "#005BAE";
    if (score >= 3.0) return "#f1c40f";
    return "#e67e22";
}

function renderMarkers() {
    markerLayerGroup.clearLayers();
    
    // MATHEMATICAL TOP 10 CALCULATION
    const sorted = Object.keys(islandData).sort((a,b) => islandData[b][currentMode] - islandData[a][currentMode]);
    const top10Ids = sorted.slice(0, 10);

    const starIcon = L.divIcon({
        html: '<div style="font-size: 24px; color: #fbbf24; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">⭐</div>',
        className: 'star-icon', iconSize: [30, 30], iconAnchor: [15, 15]
    });

    Object.keys(islandData).forEach(id => {
        const d = islandData[id];
        const score = d[currentMode];
        const isElite = top10Ids.includes(id);

        let marker = isElite 
            ? L.marker([d.lat, d.lng], { icon: starIcon }) 
            : L.circleMarker([d.lat, d.lng], { radius: 8, fillColor: getColor(score), color: "#fff", weight: 2, fillOpacity: 1 });
            
        marker.addTo(markerLayerGroup).on('click', () => showDetail(id));
        marker.bindTooltip(`<strong>${d.name}</strong>`, { sticky: true });
        markerStore[id] = { marker, data: d, isElite };
    });
}

function showHome() {
    document.body.classList.remove('subpage-active');
    document.getElementById('home-view').style.display = 'block';
    document.getElementById('detail-view').style.display = 'none';
    document.getElementById('mission-view').style.display = 'none';
    document.getElementById('hopping-view').style.display = 'none';
    if(mainMap) setTimeout(() => {
        mainMap.invalidateSize();
        mainMap.setView([38.3, 24.5], 7); // Reset to "Max zoom out" view
    }, 200);
}

function showMission() {
    document.body.classList.add('subpage-active');
    document.getElementById('home-view').style.display = 'none';
    document.getElementById('detail-view').style.display = 'none';
    document.getElementById('mission-view').style.display = 'block';
    document.getElementById('hopping-view').style.display = 'none';
    window.scrollTo(0,0);
}

function showDetail(id) {
    document.body.classList.add('subpage-active');
    document.getElementById('home-view').style.display = 'none';
    document.getElementById('detail-view').style.display = 'block';
    document.getElementById('island-name').innerText = islandData[id].name;
    window.scrollTo(0,0);
    fetch(`islands/${id}.json?v=` + new Date().getTime())
        .then(res => res.json())
        .then(d_detail => renderDetailView(Object.assign({}, islandData[id], d_detail)))
        .catch(() => renderDetailView(Object.assign({}, islandData[id], { guide: "Full blueprint coming soon." })));
}

function renderDetailView(d) {
    document.getElementById('island-guide').innerHTML = d.guide || "";
    ['beach', 'hist', 'night', 'access', 'afford'].forEach(cat => {
        const el = document.getElementById(`star-${cat}`);
        if(el) el.style.width = (d[cat] / 5 * 100) + "%";
    });

    if (miniMap) miniMap.remove();
    miniMap = L.map('island-mini-map', { zoomControl: true });
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(miniMap);

    dayLayerGroups = {};
    beachLayerGroup = L.layerGroup().addTo(miniMap);

    if (d.itinerary && d.itinerary.length > 0) {
        const roadTrip = d.itinerary.filter(s => typeof s.day === 'number').sort((a,b) => a.day - b.day);
        const dayList = [...new Set(roadTrip.map(s => s.day))];
        let miniLegendHTML = `<div class="legend-item legend-day-link" onclick="filterDay('all')"><strong>🗺️ Full Route</strong></div>`;

        dayList.forEach((day, index) => {
            const color = dayColors[index % dayColors.length];
            dayLayerGroups[day] = L.layerGroup().addTo(miniMap);
            let segmentPoints = roadTrip.filter(s => s.day === day);
            if (index > 0) {
                const prev = roadTrip.filter(s => s.day === dayList[index-1]);
                segmentPoints.unshift(prev[prev.length - 1]);
            }
            if (segmentPoints.length >= 2) {
                const coords = segmentPoints.map(p => `${p.lng},${p.lat}`).join(';');
                fetch(`https://router.project-osrm.org/route/v1/driving/${coords}?overview=full&geometries=geojson`)
                    .then(r => r.json())
                    .then(routeData => {
                        const route = routeData.routes[0];
                        L.geoJSON(route.geometry, { style: { color: color, weight: 6, opacity: 0.9 } }).addTo(dayLayerGroups[day]);
                        document.getElementById(`stats-day-${day}`).innerText = `${(route.distance/1000).toFixed(1)}km • ${Math.round(route.duration/60)}m`;
                    });
            }
            miniLegendHTML += `<div class="legend-item legend-day-link" onclick="filterDay(${day})"><span class="line-sample" style="background:${color}"></span>Day ${day}</div><span class="day-stats" id="stats-day-${day}">...</span>`;
        });

        d.itinerary.forEach(stop => {
            let emoji = stop.name.toLowerCase().includes("airport") ? "✈️" : (stop.name.toLowerCase().includes("port") ? "⚓" : (stop.day === "Beach" ? "🏖️" : "🏛️"));
            const marker = L.marker([stop.lat, stop.lng], {
                icon: L.divIcon({ html: `<div style="font-size:20px;">${emoji}</div>`, className: 'custom-pin', iconAnchor: [10, 10] })
            }).bindTooltip(stop.name);
            if (typeof stop.day === 'number') marker.addTo(dayLayerGroups[stop.day]);
            else marker.addTo(beachLayerGroup);
        });

        const mL = L.control({ position: 'topright' });
        mL.onAdd = () => { const div = L.DomUtil.create('div', 'mini-legend'); div.innerHTML = miniLegendHTML; return div; };
        mL.addTo(miniMap);
        miniMap.fitBounds(L.latLngBounds(roadTrip.map(p => [p.lat, p.lng])), { padding: [40, 40] });
    } else {
        miniMap.setView([d.lat, d.lng], 11);
    }
}

function filterDay(day) {
    Object.values(dayLayerGroups).forEach(g => miniMap.removeLayer(g));
    miniMap.removeLayer(beachLayerGroup);
    if (day === 'all') { Object.values(dayLayerGroups).forEach(g => g.addTo(miniMap)); beachLayerGroup.addTo(miniMap); }
    else { dayLayerGroups[day].addTo(miniMap); }
}

function updateMapMode(m) {
    currentMode = m;
    document.querySelectorAll('.vibe-chip').forEach(el => el.classList.remove('active'));
    document.getElementById('btn-' + m).classList.add('active');
    updateLegendContent(document.querySelector('.info.legend'));
    renderMarkers();
}

function filterIslands() {
    const q = document.getElementById('islandSearch').value.toLowerCase();
    Object.keys(markerStore).forEach(k => {
        const match = markerStore[k].data.name.toLowerCase().includes(q);
        const item = markerStore[k];
        item.marker.setOpacity(match ? 1 : 0.1);
    });
}
