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

// TODO write makeNodeFeatureDiv and makeEdgeFeatureDiv
function makeFeatureDiv(feature) {
  const featureDiv = document.createElement('div')

  if (feature.id) {
    const idPara = document.createElement('p')
    idPara.textContent = `Node Id: ${feature.id}`
    featureDiv.appendChild(idPara)
  }

  if (feature.properties && feature.properties.name) {
    const namePara = document.createElement('p')
    namePara.textContent = feature.properties.name
    featureDiv.appendChild(namePara)
  }

  if (feature.properties && feature.properties.description) {
    const descPara = document.createElement('p')
    descPara.textContent = feature.properties.description
    featureDiv.appendChild(descPara)
  }

  if (feature.properties && feature.properties.label) {
    const labPara = document.createElement('p')
    labPara.textContent = feature.properties.label
    featureDiv.appendChild(labPara)
  }

  // There being a feature.id means its a Node feature
  // We only want to add the get related nodes button 
  // if its a Node feature
  if (feature.id) {
    const button = document.createElement('button')
    button.textContent = "Get Related Nodes"

    const formData = new FormData()
    formData.append("nodeId", feature.id)

    button.addEventListener('click', async () => {
      const resp = await fetch('/related-nodes', {
        method: 'POST',
        body: formData
      })

      if (!resp.ok) {
        console.log('SERVER ERROR')
        const body = await resp.body()
        console.log(body)
        return
      }

      const json = await resp.json()
      handleResponse(json)
    })

    featureDiv.appendChild(button)
  }


  return featureDiv
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


