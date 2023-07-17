/* same code in the index.html.. You can choose to use any of the two */

const width = window.innerWidth;
const height = window.innerHeight;

const svg = d3.select("svg").attr("width", width).attr("height", height);
var tooltip = d3.select("#tooltip");

const chuckSize = 50;
//const delaySeconds = 1;

function loadFeatures(features, startIdx) {
  var gfg = d3
    .geoMercator()
    .scale(width / 0.1 / Math.PI) //==uganda===
    //.scale(width / 1.2 / Math.PI)
    .rotate([90, 0])
    //.center([110, 0])
    //.center([120, 0])
    .center([122, 1])
    .translate([width / 2, height / 2]);

  const path = d3.geoPath().projection(gfg);

  var colorScale = d3
    .scaleThreshold()
    .domain([0, 12, 35.5, 55.5, 150.5, 250.4])
    .range(["green", "yellow", "orange", "red", "purple", "maroon"]);

  svg
    .append("g")
    .selectAll("path")
    .data(features)
    .enter()
    .append("path")
    .attr("d", path)
    //.attr("fill", "Turquoise")
    .attr("fill", function (d) {
      var pm = d.properties.pm2_5;
      return colorScale(pm);
    })
    .attr("stroke", "#ffff")
    .attr("stroke-width", 1)

    .on("mouseover", function (d) {
      d3.select(this).attr("fill", "black");

      //tooltip
      tooltip
        .style("visibility", "visible")
        .html(d.properties.parish + "<br>" + "pm2_5: " + d.properties.pm2_5)
        .style("left", d3.event.pageX + 20 + "px")
        .style("top", d3.event.pageY - 10 + "px");
    })
    .on("mouseout", function (d) {
      d3.select(this)
        //.attr("fill", "Turquoise")
        .attr("fill", function (d) {
          var pm = d.properties.pm2_5;
          return colorScale(pm);
        })
        .style("stroke", "#ffff")
        .style("stroke-width", 1);

      tooltip.style("visibility", "hidden");
    });
  console.log("mapping is done!");
}

function fetchAndRenderMap(offset) {
  d3.json(`/map?offset=${offset}`, function (data) {
    console.log("Inside.. and plotting next");
    console.log(data.features);

    loadFeatures(data.features, 0);

    if (data.features.length > 0) {
      const nextOffset = offset + data.features.length;
      console.log("nextOffset is ", nextOffset);
      fetchAndRenderMap(nextOffset);
    }
  });
}

console.log("am here ==> ");
fetchAndRenderMap(0);

// =============================== 1st try ===========================================
// plotting the features after certain seconds

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
