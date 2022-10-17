import React from 'react';
import Graph from 'react-graph-vis';
import { getOptions, edgeGroupToColor } from 'components/map/MapOptions';
import { Connection, MapNode, NodeGroup } from 'components/map/MapNode';

class GraphWrapper extends React.Component {

  constructor(props) {
    super(props);
  }

  getGroupOperatingSystem(mapNode) {
    if (mapNode.operating_system) {
      return mapNode.operating_system;
    }

    return 'unknown';
  }

  calculateNodeGroup(mapNode) {
    let group_components = [];
    if (mapNode.island) {
      group_components.push('island');
    }

    if (mapNode.agent_id) {
      if (!mapNode.island && !mapNode.parent_id) {
        group_components.push('manual');
      }
      else {
        group_components.push('monkey');
      }
    }
    else if (mapNode.propagated_to) {
      group_components.push('propagated');
    }
    else if (!mapNode.island) { // No "clean" for island
      group_components.push('clean');
    }

    group_components.push(this.getGroupOperatingSystem(mapNode));

    if (mapNode.agent_is_running) {
      group_components.push('running');
    }

    let group = group_components.join('_');
    if (!(group in NodeGroup)) {
      return NodeGroup[NodeGroup.clean_unknown];
    }

    return group;
  }

  getLabel(mapNode) {
    if (mapNode.hostname) {
      return mapNode.hostname;
    }
    return mapNode.network_interfaces[0];
  }

  generateEdges(mapNodes) {
    let edges = [];
    console.log(mapNodes);
    for (const mapNode of mapNodes) {
      for (const connection of mapNode.connections) {
        edges.push({
          from: mapNode.machine_id,
          to: connection.to,
          color: edgeGroupToColor(connection.type)
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
        group: this.calculateNodeGroup(mapNode),
        label: this.getLabel(mapNode)
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
        'windows',
        'island',
        ['10.10.0.1'],
        true,
        true,
        false,
        [
          new Connection(2, 'exploited'),
          new Connection(3, 'exploited')
        ],
        1,
        null
      ),
      new MapNode(
        2,
        'linux',
        'lin-1',
        ['10.10.0.2'],
        true,
        false,
        true,
        [
          new Connection(1, 'island'),
          new Connection(3, 'scan')
        ],
        2,
        1
      ),
      new MapNode(
        3,
        'linux',
        'lin-2',
        ['10.10.0.3'],
        true,
        false,
        true,
        [
          new Connection(1, 'island'),
          new Connection(4, 'scan')
        ],
        3,
        1
      ),
      new MapNode(
        4,
        'linux',
        'lin-3',
        ['10.10.0.4'],
        false,
        false,
        true,
        [],
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

let ReactiveGraph = GraphWrapper;
export {ReactiveGraph};
