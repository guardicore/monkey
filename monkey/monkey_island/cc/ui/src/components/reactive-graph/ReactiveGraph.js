import React from 'react';
import Graph from 'react-graph-vis';
import { getOptions, edgeGroupToColor } from 'components/map/MapOptions';
import { CommunicationTypes } from 'components/types/MapNode';

// This determines the priority of the connection types.
// If an edge has more than one connection type, then this array will be used to determine which communication type to use.
// The array is in priority order, so the first item has priority over the second, and so on.
const priorityList = [CommunicationTypes.relay, CommunicationTypes.cc, CommunicationTypes.exploited, CommunicationTypes.scanned];

export default class GraphWrapper extends React.Component {

  constructor(props) {
    super(props);
  }

  getConnectionType(connectionTypes) {
    for (const priority of priorityList) {
      if (connectionTypes.includes(priority)) {
        return priority;
      }
    }

    throw new Error(`Connection types could not be prioritized: ${connectionTypes}`);
  }

  generateEdges(mapNodes) {
    let edges = [];
    for (const mapNode of mapNodes) {
      for (const [connectedTo, connectionTypes] of Object.entries(mapNode.connections)) {
        const connectionType = this.getConnectionType(connectionTypes);
        edges.push({
          from: mapNode.machine_id,
          to: connectedTo,
          color: edgeGroupToColor(connectionType)
        });
      }
    }

    return edges;
  }

  generateNodes(mapNodes) {
    let nodes = [];
    for (const mapNode of mapNodes) {
      nodes.push({
        id: mapNode.machine_id,
        group: mapNode.calculateNodeGroup(),
        label: mapNode.getLabel()
      });
    }
    return nodes;
  }

  generateGraph(mapNodes) {
    return {
      edges: this.generateEdges(mapNodes),
      nodes: this.generateNodes(mapNodes)
    };
  }

  render() {
    let options = getOptions();
    let graph = this.generateGraph(this.props.mapNodes);
    return (
      <div className={'net-graph-wrapper'}>
        <Graph graph={graph} options={options} events={this.props.events} />
      </div>
    )
  }
}
