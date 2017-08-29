import React from 'react';
import {Col} from 'react-bootstrap';
import Graph from 'react-graph-vis';
import {Icon} from 'react-fa'


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
      graph: {nodes: [], edges: []}
    };
  }

  events = {
    select: event => this.selectionChanged(event)
  };

  componentDidMount() {
    fetch('/api/netmap')
      .then(res => res.json())
      .then(res => this.setState({graph: res}));
  }

  selectionChanged(event) {
    if (event.nodes.length === 1) {
      console.log('selected node:', event.nodes[0]);
    }
    else if (event.edges.length === 1) {
      console.log('selected edge:', event.edges[0]);
    }
    else {
      console.log('no preview.');
    }
  }

  render() {
    return (
      <div>
        <Col xs={12}>
          <h1 className="page-title">Infection Map</h1>
        </Col>
        <Col xs={8}>
          <div className="pull-left">
            <input placeholder="Search" />
          </div>
          <Graph graph={this.state.graph} options={options} events={this.events}/>
        </Col>
        <Col xs={4}>
          <div className="panel panel-default preview">
            <div className="panel-heading">
              <h3>
                <Icon name="fire"/>
                vm4
                <small>Infected Asset</small>
              </h3>
            </div>

            <div className="panel-body">
              <h4>Machine Info</h4>
              <p>...</p>

              <h4 style={{'marginTop': '2em'}}>Exploit Method</h4>
              <p>...</p>

              <h4 style={{'marginTop': '2em'}}>Timeline</h4>
              <ul className="timeline">
                <li>
                  <div className="bullet"></div>
                  failed attempt1
                </li>
                <li>
                  <div className="bullet"></div>
                  failed attempt2
                </li>
                <li>
                  <div className="bullet bad"></div>
                  Infection!
                </li>
              </ul>
            </div>
          </div>
        </Col>
      </div>
    );
  }
}

export default MapPageComponent;
