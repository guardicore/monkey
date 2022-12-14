import React from 'react';
import Graph from 'react-graph-vis';
import {getOptions} from '../map/MapOptions';


const GraphWrapper = (props: { graph: Graph, events: any }) => {

  let options = getOptions();
  return (
    <div className={'net-graph-wrapper'}>
      <Graph graph={props.graph} options={options} events={props.events}
      getNetwork={network => {
        // Move the center of the camera to the right
        // to compensate for the side panel on the right
        network.moveTo({'position': {'x': 100, 'y': 0}})
      }}/>
    </div>
  )
}

export default GraphWrapper;
