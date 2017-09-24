import React from 'react';
import {Col} from 'react-bootstrap';
import Graph from 'react-graph-vis';
import PreviewPane from 'components/preview-pane/PreviewPane';
import {Link} from 'react-router-dom';
import {Icon} from 'react-fa';

let groupsToGroupsOptions = (groupNames) => {
  let groupOptions = {};
  for (let groupName of groupNames) {
    groupOptions[groupName] =
      {
        shape: 'image',
        size: 50,
        image: '../images/nodes/' + groupName + '.png'
      };
  }
  return groupOptions;
};

let options = {
  layout: {
    improvedLayout: false
  },
  groups: groupsToGroupsOptions(['clean_linux', 'clean_windows', 'exploited_linux', 'exploited_windows', 'island',
    'island_monkey_linux', 'island_monkey_linux_running', 'island_monkey_windows', 'island_monkey_windows_running',
    'manual_linux', 'manual_linux_running', 'manual_windows', 'manual_windows_running', 'monkey_linux',
    'monkey_linux_running', 'monkey_windows', 'monkey_windows_running'])
};

class MapPageComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      graph: {nodes: [], edges: []},
      selected: null,
      selectedType: null,
      killPressed: false
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
    this.updateMapFromServer();
    this.interval = setInterval(this.updateMapFromServer, 1000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  updateMapFromServer = () => {
    fetch('/api/netmap')
      .then(res => res.json())
      .then(res => {
        res.edges.forEach(edge => {
          edge.color = this.edgeGroupToColor(edge.group);
        });
        this.setState({graph: res});
        this.props.onStatusChange();
      });
  };

  selectionChanged(event) {
    if (event.nodes.length === 1) {
      console.log('selected node:', event.nodes[0]); // eslint-disable-line no-console
      fetch('/api/netmap/node?id='+event.nodes[0])
        .then(res => res.json())
        .then(res => this.setState({selected: res, selectedType: 'node'}));
    }
    else if (event.edges.length === 1) {
      let displayedEdge = this.state.graph.edges.find(
        function(edge) {
          return edge['id'] === event.edges[0];
        });
      if (displayedEdge['group'] == 'island') {
        this.setState({selected: displayedEdge, selectedType: 'island_edge'});
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
  };

  killAllMonkeys = () => {
    fetch('/api?action=killall')
      .then(res => res.json())
      .then(res => this.setState({killPressed: (res.status==="OK")}));
  };

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
            <Link to="/infection/telemetry" className="btn btn-default pull-left" style={{'width': '48%'}}>Monkey Telemetry</Link>
            <button onClick={this.killAllMonkeys} className="btn btn-danger pull-right" style={{'width': '48%'}}>
              <Icon name="stop-circle" style={{'marginRight': '0.5em'}} />
              Kill All Monkeys
            </button>
          </div>
          {this.state.killPressed ?
            <div className="alert alert-info">
              <i className="glyphicon glyphicon-info-sign" style={{'marginRight': '5px'}}/>
              Kill command sent to all monkeys
            </div>
            : ''}

          <PreviewPane item={this.state.selected} type={this.state.selectedType} />
        </Col>
      </div>
    );
  }
}

export default MapPageComponent;
