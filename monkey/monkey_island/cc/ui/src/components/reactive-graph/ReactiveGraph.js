import React from 'react';
import Graph from 'react-graph-vis';
import { getOptions } from 'components/map/MapOptions';

class GraphWrapper extends React.Component {

  constructor(props) {
    super(props);
  }

  generateGraph() {
    return {
      edges: [],
      nodes: []
    };
  }

  render() {
    let options = getOptions();
    let graph = this.generateGraph();
    return (
      <div className={'net-graph-wrapper'}>
        <Graph graph={graph} options={options} events={this.props.events} />
      </div>
    )
  }
}

let ReactiveGraph = GraphWrapper;
export {ReactiveGraph};
