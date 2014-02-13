function main() {
    console.log("JS file loaded!");
    d3.json('/src/mp1/data.json', function(data) {
        data = _.map(data, function(elem) {
            return {name: elem.word, value: elem.freq, ch: elem.ch};
        });
        histogram("#main", data);
    });

}
function histogram(id, data) {
    // Get size of container and set some defaults.
    var width = $(id).width() || 303;
    var height = $(id).height() || 871;

    // A few colors to mess with
    var color = d3.scale.category10();
    // Insert a new SVG element (our chart)
    var chart = d3.select(id)
            .append("svg")
            .attr("width", width)
            .attr("height", height);

    var hashCode = function(str){
      var hash = 0;
      if (str.length === 0) return hash;
      for (i = 0; i < str.length; i++) {
        char = str.charCodeAt(i);
        hash = ((hash<<5)-hash)+char;
        hash = hash & hash; // Convert to 32bit integer
      }
      return hash;
    }

    var squeeze = 120;
    var xScale = d3.scale.linear()
                 .domain([0, width-1])
                 .range([squeeze, width-squeeze]);

    var yScale = d3.scale.linear()
                 .domain([0, height-1])
                 .range([squeeze, height-squeeze]);
    var x = function(word){
      return xScale((3*width + hashCode(word)) % width);
    }

    var y = function(word){
      return yScale((3*height + hashCode(word)) % height);
    }

    var radius = d3.scale.linear()
                .domain([0, d3.max(data, function(d) { return d.value; })])
                .range([0, height/8]);

    function order(a, b){
      radius(b) - radius(a);
    }

    // The g elements represent a data point.
    var g = chart.selectAll("g")
            .data(data)
            .sort(order)
            .enter()
            .append("g");
        
    g.append("circle")
        .attr("cx", function(d, i) { return x(d.name);})
        .attr("cy", function(d, i) { return height - y(d.name) - 25;})
        .style("stroke", "gray")
        .style("fill", function(d, i) { return color(d.ch); })
        .attr("r", function(d, i){ return radius(d.value); })

}
