import React from 'react';
import {Col} from 'react-bootstrap';
import Graph from 'react-graph-vis';
import PreviewPane from 'components/preview-pane/PreviewPane';
import {Link} from 'react-router-dom';
import {Icon} from 'react-fa';

let options = {
  layout: {
    improvedLayout: false
  },
  groups: {
    manuallyInfected: {
      shape: 'icon',
      icon: {
        face: 'FontAwesome',
        code: '\uf120',
        size: 50,
        color: '#8f5a0b'
      }
    },
    infected: {
      shape: 'icon',
      icon: {
        face: 'FontAwesome',
        code: '\uf06d',
        size: 50,
        color: '#d30d09'
      }
    },
    clean: {
      shape: 'icon',
      icon: {
        face: 'FontAwesome',
        code: '\uf108',
        size: 50,
        color: '#999'
      }
    }
  }

};

class MapPageComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      graph: {nodes: [], edges: []},
      selected: null,
      selectedType: null
    };
  }

  events = {
    select: event => this.selectionChanged(event)
  };

  edgeGroupToColor(group) {
    switch (group) {
      case 'exploited':
        return '#c00';
        break;
      case 'tunnel':
        return '#aaa';
        break;
      case 'scan':
        return '#f90';
        break;
      case 'island':
        return '#aaa';
        break;
    }
    return 'black';
  }

  componentDidMount() {
    fetch('/api/netmap')
      .then(res => res.json())
      .then(res => {
        res.edges.forEach(edge => {
          edge.color = this.edgeGroupToColor(edge.group);
        });
        this.setState({graph: res});
        this.props.onStatusChange();
      });
  }

  selectionChanged(event) {
    if (event.nodes.length === 1) {
      console.log('selected node:', event.nodes[0]); // eslint-disable-line no-console
      fetch('/api/netmap/node?id='+event.nodes[0])
        .then(res => res.json())
        .then(res => this.setState({selected: res, selectedType: 'node'}));
    }
    else if (event.edges.length === 1) {
      let edgeGroup = this.state.graph.edges.filter(
        function(edge) {
          return edge['id'] === event.edges[0];
        })[0]['group'];
      if (edgeGroup == 'island') {
        console.log('selection cleared.'); // eslint-disable-line no-console
        this.setState({selected: null, selectedType: null});
      } else {
        fetch('/api/netmap/edge?id='+event.edges[0])
          .then(res => res.json())
          .then(res => this.setState({selected: res.edge, selectedType: 'edge'}));
      }
    }
    else {
      console.log('selection cleared.'); // eslint-disable-line no-console
      this.setState({selected: null, selectedType: null});
    }
  }

  render() {
    return (
      <div>
        <Col xs={12}>
          <h1 className="page-title">Infection Map</h1>
        </Col>
        <Col xs={8}>
          <Graph graph={this.state.graph} options={options} events={this.events}/>
        </Col>
        <Col xs={4}>
          <input className="form-control input-block"
                 placeholder="Find on map"
                 style={{'marginBottom': '1em'}}/>

          <div style={{'overflow': 'auto', 'marginBottom': '1em'}}>
            <Link to="/infection/logs" className="btn btn-default pull-left" style={{'width': '48%'}}>Monkey Telemetry</Link>
            <button onClick={this.killAllMonkeys} className="btn btn-danger pull-right" style={{'width': '48%'}}>
              <Icon name="stop-circle" style={{'marginRight': '0.5em'}}></Icon>
              Kill All Monkeys
            </button>
          </div>

          <PreviewPane item={this.state.selected} type={this.state.selectedType} />
        </Col>
      </div>
    );
  }
}

export default MapPageComponent;
