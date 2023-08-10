import React from 'react';
import VisGraph, {GraphData, GraphEvents} from 'react-vis-graph-wrapper';
import {getOptions, startingPosition} from '../map/MapOptions';


const GraphWrapper = (props: { graph: GraphData, events: GraphEvents }) => {

  let options = getOptions();
  return (
    <div className={'net-graph-wrapper'}>
      <VisGraph graph={props.graph} options={options} events={props.events}
      getNetwork={network => {
        network.moveTo(startingPosition);
      }}/>
    </div>
  )
}

export default GraphWrapper;
