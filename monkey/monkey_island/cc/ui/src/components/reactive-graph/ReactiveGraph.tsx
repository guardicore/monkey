import React from 'react';
import Graph from 'react-graph-vis';
import {getOptions} from '../map/MapOptions';

// This determines the priority of the connection types.
// If an edge has more than one connection type,
// then this array will be used to determine which communication type to use.
// The array is in priority order, so the first item has priority over the second, and so on.

const GraphWrapper = (props: { graph: Graph, events: any }) => {

  let options = getOptions();
  return (
    <div className={'net-graph-wrapper'}>
      <Graph graph={props.graph} options={options} events={props.events}/>
    </div>
  )
}

export default GraphWrapper;
