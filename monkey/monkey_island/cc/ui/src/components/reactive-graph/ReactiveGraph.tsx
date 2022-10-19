import React from 'react';
import Graph from 'react-graph-vis';
import {getOptions} from '../map/MapOptions';


const GraphWrapper = (props: { graph: Graph, events: any }) => {

  let options = getOptions();
  return (
    <div className={'net-graph-wrapper'}>
      <Graph graph={props.graph} options={options} events={props.events}/>
    </div>
  )
}

export default GraphWrapper;
