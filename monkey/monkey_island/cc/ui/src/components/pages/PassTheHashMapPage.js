import React from 'react';
import {ReactiveGraph} from 'components/reactive-graph/ReactiveGraph';
import AuthComponent from '../AuthComponent';
import {optionsPth} from '../map/MapOptions';
import {Col} from 'react-bootstrap';

class PassTheHashMapPageComponent extends AuthComponent {
  constructor(props) {
    super(props);
    this.state = {
      graph: props.graph,
      selected: null,
      selectedType: null
    };
  }

  events = {
    select: event => this.selectionChanged(event)
  };

  selectionChanged(event) {
    if (event.nodes.length === 1) {
      let displayedNode = this.state.graph.nodes.find(
        function (node) {
          return node['id'] === event.nodes[0];
        });
      this.setState({selected: displayedNode, selectedType: 'node'})
    } else if (event.edges.length === 1) {
      let displayedEdge = this.state.graph.edges.find(
        function (edge) {
          return edge['id'] === event.edges[0];
        });
      this.setState({selected: displayedEdge, selectedType: 'edge'});
    } else {
      this.setState({selected: null, selectedType: null});
    }
  }

  render() {
    return (
      <div>
        <Col xs={12}>
          <div style={{height: '70vh'}}>
            <ReactiveGraph graph={this.state.graph} options={optionsPth} events={this.events}/>
          </div>
        </Col>
      </div>
    );
  }
}

export default PassTheHashMapPageComponent;
