var LM = function(selector, width, height) {
  this.w = width;
  this.h = height;
  var margin = {
    top:300,
    right:0,
    bottom:0,
    left:500
  };

  this.x = d3.scale.ordinal().rangeBands([0, width]),
  this.z = d3.scale.linear().domain([0, 4]).clamp(true),
  this.c = d3.scale.category10().domain(d3.range(10));
  
  d3.select(selector).selectAll("svg").remove();
  this.svg = d3.select(selector).append("svg:svg")
    .attr('width', width+margin.left+margin.right)
    .attr('height', height+margin.top+margin.bottom)
    .style('margin-left', -margin.left + "px")
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top +")");

  this.svg.append("svg:rect")
    .style("stroke", "#000")
    .style("fill", "#000")
    .attr('width', width+margin.left+margin.right)
    .attr('height', height+margin.top+margin.bottom)
    .append("g")

}

LM.prototype.update = function(json) {

  if(json)
    this.json = json;
  this.json.fixed = true;

  var matrix = [],
  nodes = json.nodes,
  n = nodes.length;
  
  nodes.forEach(function(node, i) {
    node.index = i;
    node.count = 0;
    matrix[i] = d3.range(n).map(function(j) { return {x: j, y: i, z: 0}; });
  });

  json.links.forEach(function(link) {
    matrix[link.source][link.target].z += link.value;
    matrix[link.target][link.source].z += link.value;
    matrix[link.source][link.source].z += link.value;
    matrix[link.target][link.target].z += link.value;
    nodes[link.source].count += link.value;
    nodes[link.target].count += link.value;
  });

  var orders = {
    name: d3.range(n).sort(function(a, b) { return d3.ascending(nodes[a].name, nodes[b].name); }),
    count: d3.range(n).sort(function(a, b) { return nodes[b].count - nodes[a].count; }),
    group: d3.range(n).sort(function(a, b) { return nodes[b].group - nodes[a].group; })
  };

  this.x.domain(orders.name);
  var x = this.x;
  var z = this.z;
  var c = this.c;

  var row = this.svg.selectAll(".row")
    .data(matrix)
    .enter().append("g")
    .attr("class", "row")
    .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
    .each(row);

  var width = this.w;
  var height = this.h;

  row.append("line")
  .attr("x2", width);

  row.append("text")
  .attr("x", -6)
  .attr("y", this.x.rangeBand() / 2)
  .attr("dy", ".32em")
  .attr("text-anchor", "end")
  .text(function(d, i) { return nodes[i].name; });

  var column = this.svg.selectAll(".column")
  .data(matrix)
  .enter().append("g")
  .attr("class", "column")
  .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });

  column.append("line")
  .attr("x1", -width);

  column.append("text")
  .attr("x", 6)
  .attr("y", x.rangeBand() / 2)
  .attr("dy", ".32em")
  .attr("text-anchor", "start")
  .text(function(d, i) { return nodes[i].name; });

  function row(row) {
    var cell = d3.select(this).selectAll(".cell")
      .data(row.filter(function(d) { return d.z; }))
      .enter().append("rect")
      .attr("class", "cell")
      .attr("x", function(d) { return x(d.x); })
      .attr("width", x.rangeBand())
      .attr("height", x.rangeBand())
      .style("fill-opacity", function(d) { return z(d.z); })
      .style("fill", function(d) { return nodes[d.x].group == nodes[d.y].group ? c(nodes[d.x].group) : null; })
      .on("mouseover", mouseover)
      .on("mouseout", mouseout);
  }

  var svg = this.svg;

  function mouseover(p) {
    d3.selectAll(".row text").classed("active", function(d, i) { return i == p.y; });
    d3.selectAll(".column text").classed("active", function(d, i) { return i == p.x; });
  }

  function mouseout() {
    d3.selectAll("text").classed("active", false);
  }

  d3.select("#order").on("change", function() {
    clearTimeout(timeout);
    order(this.value);
  });


  function order(value) {
    x.domain(orders[value]);
    var t = svg.transition().duration(2500);

    t.selectAll(".row")
    .delay(function(d, i) { return x(i) * 4; })
    .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
    .selectAll(".cell")
    .delay(function(d) { return x(d.x) * 4; })
    .attr("x", function(d) { return x(d.x); });

    t.selectAll(".column")
    .delay(function(d, i) { return x(i) * 4; })
    .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });
  }

  var timeout = setTimeout(function() {
    order("group");
    d3.select("#order").property("selectedIndex", 2).node().focus();
  }, 5000);

}


function main() {
  var myLM;
  var createLM = function(json){
    myLM = new LM("#visualization", 720, 720).update(json);
  };
  d3.json('/src/mp3/data.json', createLM);
}

