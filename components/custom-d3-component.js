const React = require('react');
const d3 = require('d3');

class CustomD3Component extends React.Component {
  constructor(props) {
    super(props);
    this.svgRef = React.createRef();
    this.xScale = null;
    this.y1Scale = null;
    this.y2Scale = null;
    this.svg = null;
    this.width = 0; // Define width variable
    this.height = 0; // Define height variable
  }

  componentDidMount() {
    this.initializeChart();
    this.drawChart();
  }

  componentDidUpdate(prevProps) {
    if (prevProps.scrollProgress !== this.props.scrollProgress) {
      this.updateChart();
    }
  }

  initializeChart() {
    const { x, y1_1, y1_2, y2 } = this.props.data;

    // Define dimensions and margins
    const margin = { top: 10, right: 80, bottom: 30, left: 50 };
    this.width = 960 - margin.left - margin.right;
    this.height = 500 - margin.top - margin.bottom;

    // Append SVG object to the body of the page
    this.svg = d3
      .select(this.svgRef.current)
      .append('svg')
      .attr('width', this.width + margin.left + margin.right)
      .attr('height', this.height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    // Define scales
    this.xScale = d3.scaleLinear().range([0, this.width]);
    this.y1Scale = d3.scaleLinear().range([this.height, 0]);
    this.y2Scale = d3.scaleLinear().range([this.height, 0]);
  }

  drawChart() {
    const { x, y1_1, y1_2, y2 } = this.props.data;

    // Update scales domain
    this.xScale.domain(d3.extent(x));
    this.y1Scale.domain([0, d3.max([...y1_1, ...y1_2])]);
    this.y2Scale.domain([0, d3.max(y2)]);

    // Add X axis
    this.svg
      .append('g')
      .attr('class', 'x axis')
      .attr('transform', 'translate(0,' + this.height + ')')
      .call(d3.axisBottom(this.xScale));

    // Add Y1 axis
    this.svg.append('g').call(d3.axisLeft(this.y1Scale));

    // Add Y2 axis
    this.svg
      .append('g')
      .attr('transform', `translate(${this.width}, 0)`)
      .call(d3.axisRight(this.y2Scale));

    // Add Line y1_1
    const line1 = d3
      .line()
      .x((d, i) => this.xScale(x[i]))
      .y(d => this.y1Scale(d));

    this.svg
      .append('path')
      .datum(y1_1)
      .attr('fill', 'none')
      .attr('stroke', 'steelblue')
      .attr('stroke-width', 1.5)
      .attr('d', line1);

    // Add Line y1_2
    const line2 = d3
      .line()
      .x((d, i) => this.xScale(x[i]))
      .y(d => this.y1Scale(d));

    this.svg
      .append('path')
      .datum(y1_2)
      .attr('fill', 'none')
      .attr('stroke', 'green')
      .attr('stroke-width', 1.5)
      .attr('d', line2);

    // Add dashed Line y2
    const stepLine = d3
      .line()
      .x((d, i) => this.xScale(x[i]))
      .y(d => this.y2Scale(d))
      .curve(d3.curveStepAfter);

    this.svg
      .append('path')
      .datum(y2)
      .attr('fill', 'none')
      .attr('stroke', 'red')
      .attr('stroke-width', 1.5)
      .attr('stroke-dasharray', '5,5')
      .attr('d', stepLine);
  }

updateChart() {
  const { scrollProgress } = this.props;

  // Adjust chart based on scrollProgress
  const numPointsToShow = Math.floor(scrollProgress * this.props.data.x.length);

  // Update the opacity of lines based on scrollProgress
  this.svg.selectAll('.line')
    .style('opacity', (d, i) => i <= numPointsToShow ? 1 : 0);

  // Update the x-axis domain
  const newDomain = [
    this.props.data.x[0],
    this.props.data.x[numPointsToShow]
  ];
  this.xScale.domain(newDomain);
  this.svg.select('.x.axis').call(d3.axisBottom(this.xScale)); // Update x-axis
}


  render() {
    return <div ref={this.svgRef}></div>;
  }
}

module.exports = CustomD3Component;
