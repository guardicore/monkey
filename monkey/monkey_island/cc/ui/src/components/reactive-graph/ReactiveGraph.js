import React from 'react';
import Graph from 'react-graph-vis';
import { getOptions } from 'components/map/MapOptions';

class GraphWrapper extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    let options = getOptions();
    return (
      <div className={'net-graph-wrapper'}>
        <Graph graph={this.props.graph} options={options} events={this.props.events} />
      </div>
    )
  }
}

let ReactiveGraph = GraphWrapper;
export {ReactiveGraph};
