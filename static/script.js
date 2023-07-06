// Width and height of the map container
const width = 800;
// const width = innerWidth;
const height = 600;
// const height = innerHeight;


// Create a SVG element to hold the map
const svg = d3
  .select("#map")
  .append("svg")
  .attr("width", width)
  .attr("height", height);

// Load the GeoJSON file
d3.json("/").then(function (data) {
    console.log(data.features);

  // Create a projection based on the map's bounding box
  const projection = d3
    .geoMercator()
    .scale(1000)
    .center([0, 20])
    .translate([width / 2, height / 2]);
  // .fitSize([width, height], data);


  // Create a path generator
  const path = d3.geoPath().projection(projection);


  // Render the map
  svg
    .selectAll("path")
    .data(data.features)
    .enter()
    .append("path")
    .attr("d", path)
    .attr("fill", "lightblue")
    .attr("stroke", "white")
    .attr("stroke-width", 2);
});




/*

const geojsonPath = "/static/gad.json";

const chunkSize = 100;
const delaySeconds = 2;

function loadFeatures(features, startIdx) {
  if (startIdx >= features.length) {
    //console.log("all is done");
    return;
  }

  const endIdx = Math.min(startIdx + chunkSize, features.length);
  const chunk = features.slice(startIdx, endIdx);

  const projection = d3
    .geoMercator()
    .scale(1000)
    .translate([width/2, height/2])
    .fitSize([width, height], { type: "FeatureCollection", features: chunk });

  const path = d3.geoPath().projection(projection);

  svg
    .selectAll("path")
    .data(chunk)
    .enter()
    .append("path")
    .attr("d", path)
    .attr("fill", "lightblue")
    .attr("stroke", "black")
    .attr("stroke-width", 1);

  // Schedule the next chunk after the delay
  setTimeout(function () {
    loadFeatures(features, endIdx);
  }, delaySeconds * 1000);
}

d3.json(geojsonPath)
  .then(function (data) {

    const features = data.features;
    loadFeatures(features, 0);

  })
  .catch(function (error) {
    console.error("Error loading the GeoJSON file:", error);
  });
*/
