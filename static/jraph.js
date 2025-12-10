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

let currentLayer = null;
let drawCircle = null;

function downloadFromResp(resp, filename) {
  resp.blob().then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
  })
}

function makeNodeFeatureDiv(feature) {
  const featureDiv = document.createElement('div')

  const idPara = document.createElement('p')
  idPara.textContent = `Node Id: ${feature.id}`
  featureDiv.appendChild(idPara)

  for (const [k, v] of Object.entries(feature.properties)) {
    if (!v) continue
    const para = document.createElement('p')
    para.textContent = `${k}: ${v}`
    featureDiv.appendChild(para)
  }

  const button = document.createElement('button')
  button.textContent = "Get Related Nodes"

  const formData = new FormData()
  formData.append("nodeId", feature.id)

  button.addEventListener('click', () => {
    fetch('/related-nodes', {
      method: 'POST',
      body: formData
    }).then(resp => resp.json())
      .then(handleResponse)
  })

  featureDiv.appendChild(button)

  return featureDiv
}

function makeEdgeFeatureDiv(feature) {
  const featureDiv = document.createElement('div')

  const { sourceId, targetId } = feature.properties
  const edgeHeaderPara = document.createElement('p')
  edgeHeaderPara.textContent = `${sourceId} -> ${targetId}`
  featureDiv.appendChild(edgeHeaderPara)

  for (const [k, v] of Object.entries(feature.properties)) {
    if (k === 'sourceId' || k === 'targetId') continue
    const para = document.createElement('p')
    para.textContent = `${k}: ${v}`
    featureDiv.appendChild(para)
  }

  return featureDiv
}

function makeFeatureDiv(feature) {
  if (feature.id !== undefined) return makeNodeFeatureDiv(feature)
  return makeEdgeFeatureDiv(feature)
}

// TODO turn this to typescript and give respJson an interface
function handleResponse(respJson) {
  // Append previous query to previous query list
  prevEntry = document.createElement('li')
  prevEntry.textContent = respJson.previousQuery
  document.getElementById('prev').appendChild(prevEntry)

  const geojson = respJson.geoJson

  // Remove previous layer and drawCircle
  if (currentLayer && geojson.features.length > 0) {
    map.removeLayer(currentLayer);
    if (drawCircle) drawCircle.remove()
  }

  // Add new GeoJSON layer
  currentLayer = L.geoJSON(geojson, {
    style: { color: 'blue', weight: 4 },
    onEachFeature: function (feature, layer) {
      const featureDiv = makeFeatureDiv(feature)
      layer.bindPopup(featureDiv)
    }
  }).addTo(map);

  // Fit map to bounds
  if (geojson.features.length > 0) {
    map.fitBounds(currentLayer.getBounds());
  } else {
    alert('No features found for this query.');
  }
}

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

    fetch('/nodes-within-radius', {
      method: 'POST',
      body: formData
    }).then(resp => resp.json())
      .then(handleResponse)
  };

  map.on('mousemove', moveHandler);
  map.on('mouseup', upHandler);
});


document.getElementById('query-form').addEventListener('submit', function (e) {
  e.preventDefault(); // Prevent full page reload

  const formData = new FormData(this);

  fetch('/search', {
    method: 'POST',
    body: formData
  }).then(resp => resp.json())
    .then(handleResponse)
});

// TODO do file downloads entirely clientside
document.getElementById('download-kml').addEventListener('click', function () {
  if (!currentLayer) {
    alert('no data to download')
    return
  }

  const geojson = currentLayer.toGeoJSON(false)
  const formData = new FormData()
  formData.append('geojson', JSON.stringify(geojson))

  fetch('/download-kml', {
    method: 'POST',
    body: formData
  }).then(resp => downloadFromResp(resp, 'jraph-data.kml'))
})

document.getElementById('download-gpkg').addEventListener('click', function () {
  if (!currentLayer) {
    alert('no data to download')
    return
  }

  const geojson = currentLayer.toGeoJSON(false)
  const formData = new FormData()
  formData.append('geojson', JSON.stringify(geojson))

  fetch('/download-gpkg', {
    method: 'POST',
    body: formData
  }).then(resp => downloadFromResp(resp, 'jraph-data.gpkg'))
})

