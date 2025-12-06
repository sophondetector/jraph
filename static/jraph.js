const DEFAULT_LAT = 43.206879
const DEFAULT_LNG = -71.538162
const DEFAULT_ZOOM = 7

const map = L.map('map').setView([DEFAULT_LAT, DEFAULT_LNG], DEFAULT_ZOOM);

const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const control = L.Control.fileLayerLoad({
  layer: L.geoJson,
  layerOptions: { style: { color: 'red' } },
  addToMap: true,
  fileSizeLimit: 1024,
  formats: [
    '.geojson',
    '.kml',
  ]
}).addTo(map);

control.loader.on('data:error', function (error) {
  console.log('ERROR', error);
});
let currentLayer = null; // To remove previous results

function handleResponse(respJson) {
  // Auto-load KML into map from server response

  // Append previous query to previous query list
  prevEntry = document.createElement('li')
  prevEntry.textContent = respJson.previousQuery
  document.getElementById('prev').appendChild(prevEntry)

  // Step 2: Parse KML to GeoJSON using togeojson
  const geojson = respJson.geoJson

  // Step 3: Remove previous layer
  if (currentLayer) {
    map.removeLayer(currentLayer);
  }

  // Step 4: Add new GeoJSON layer
  currentLayer = L.geoJSON(geojson, {
    style: { color: 'blue', weight: 4 },
    onEachFeature: function (feature, layer) {
      if (feature.properties && feature.properties.name) {
        layer.bindPopup(feature.properties.name);
      }
      if (feature.properties && feature.properties.description) {
        layer.bindPopup(feature.properties.description);
      }
    }
  }).addTo(map);

  // Step 5: Fit map to bounds
  if (geojson.features.length > 0) {
    map.fitBounds(currentLayer.getBounds());
  } else {
    alert('No features found for this query.');
  }

}

let drawCircle = null;
map.on('mousedown', async e => {
  if (!e.originalEvent.altKey) return;

  if (drawCircle) drawCircle.remove()
  map.dragging.disable();

  const center = e.latlng;
  let radius = 0

  drawCircle = L.circle(center, { radius: radius, fill: false }).addTo(map);

  const moveHandler = e => {
    radius = center.distanceTo(e.latlng);
    drawCircle.setRadius(radius);
  };

  const upHandler = async () => {
    map.off('mousemove', moveHandler);
    map.off('mouseup', upHandler);
    map.dragging.enable();

    const formData = new FormData()
    formData.append("lat", center.lat)
    formData.append("lng", center.lng)
    formData.append("rad", radius)

    const response = await fetch('/nodes-within-radius', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      console.warn(`something went wrong: ${response.error}`)
      alert('something went wrong with your request, please try again')
      return
    }

    const respJson = await response.json()
    handleResponse(respJson)
  };

  map.on('mousemove', moveHandler);
  map.on('mouseup', upHandler);
});


document.getElementById('query-form').addEventListener('submit', async function (e) {
  e.preventDefault(); // Prevent full page reload

  const formData = new FormData(this);

  const response = await fetch('/', {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    cosnole.warn(`search query failed: ${response.error}`)
    alert(`query failed`)
    return
  }

  respJson = await response.json()
  handleResponse(respJson)
});


