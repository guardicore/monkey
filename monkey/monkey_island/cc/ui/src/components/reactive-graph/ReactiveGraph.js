import React from 'react';
import Graph from 'react-graph-vis';
import { getOptions, edgeGroupToColor } from 'components/map/MapOptions';
import { CommunicationTypes, MapNode, OS } from 'components/types/MapNode';

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
    let mapNodes = [
      new MapNode(
        1,
        ['10.10.0.1'],
        true,
        {
          2: [CommunicationTypes.scanned, CommunicationTypes.exploited],
          3: [CommunicationTypes.scanned, CommunicationTypes.exploited]
        },
        OS.windows,
        'island',
        true,
        true,
        1,
        null
      ),
      new MapNode(
        2,
        ['10.10.0.2'],
        true,
        {
          1: [CommunicationTypes.cc],
          3: [CommunicationTypes.scanned]
        },
        OS.linux,
        'lin-1',
        false,
        true,
        2,
        1
      ),
      new MapNode(
        3,
        ['10.10.0.3'],
        true,
        {
          1: [CommunicationTypes.cc],
          4: [CommunicationTypes.scanned]
        },
        OS.windows,
        'win-xp',
        false,
        true,
        3,
        1
      ),
      new MapNode(
        4,
        ['10.10.0.4'],
        false,
        { 3: [CommunicationTypes.relay] },
        OS.unknown,
        'lin-2',
        false,
        true,
        null,
        null
      )
    ];
    let options = getOptions();
    let graph = this.generateGraph(mapNodes);
    return (
      <div className={'net-graph-wrapper'}>
        <Graph graph={graph} options={options} events={this.props.events} />
      </div>
    )
  }
}
