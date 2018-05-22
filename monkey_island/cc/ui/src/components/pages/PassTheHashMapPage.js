import React from 'react';
import {Col} from 'react-bootstrap';
import {ReactiveGraph} from 'components/reactive-graph/ReactiveGraph';
import AuthComponent from '../AuthComponent';
import Graph from 'react-graph-vis';

const options = {
  autoResize: true,
  layout: {
    improvedLayout: false
  },
  edges: {
    width: 2,
    smooth: {
      type: 'curvedCW'
    }
  },
  physics: {
    barnesHut: {
      gravitationalConstant: -120000,
      avoidOverlap: 0.5
    },
    minVelocity: 0.75
  }
};

class PassTheHashMapPageComponent extends AuthComponent {
  constructor(props) {
    super(props);
    this.state = {
      graph: {nodes: [], edges: []},
      report: "",
      selected: null,
      selectedType: null,
      killPressed: false,
      showKillDialog: false,
      telemetry: [],
      telemetryLastTimestamp: null
    };
  }

  componentDidMount() {
    this.updateMapFromServer();
    this.interval = setInterval(this.timedEvents, 1000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  timedEvents = () => {
    this.updateMapFromServer();
  };

  updateMapFromServer = () => {
    this.authFetch('/api/pthmap')
      .then(res => res.json())
      .then(res => {
        this.setState({graph: res});
        this.props.onStatusChange();
      });
    this.authFetch('/api/pthreport')
      .then(res => res.json())
      .then(res => {
        this.setState({report: res.html});
        this.props.onStatusChange();
      });
  };

  render() {
    return (
      <div>
        <Col xs={12} lg={8}>
          <h1 className="page-title">Pass The Hash Map</h1>
        </Col>
        <Col xs={12}>
          <div>
            <Graph graph={this.state.graph} options={options} />
          </div>
          <div dangerouslySetInnerHTML={{__html: this.state.report}}></div>
        </Col>
      </div>
    );
  }
}

export default PassTheHashMapPageComponent;
