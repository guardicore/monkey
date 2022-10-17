import React from 'react';
import Graph from 'react-graph-vis';
import { getOptions } from 'components/map/MapOptions';
import { Connection, MapNode, NodeGroup } from 'components/map/MapNode';

class GraphWrapper extends React.Component {

  constructor(props) {
    super(props);
  }

  getLabel(mapNode) {
    if (mapNode.hostname) {
      return mapNode.hostname;
    }
    return mapNode.network_interfaces[0];
  }

  generateNodes(mapNodes) {
    let nodes = [];
    for (const mapNode of mapNodes) {
      nodes.push({
        id: mapNode.machine_id,
        group: NodeGroup.clean_unknown,
        label: this.getLabel(mapNode)
      });
    }
    return nodes;
  }

  generateGraph(mapNodes) {
    return {
      edges: [],
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
