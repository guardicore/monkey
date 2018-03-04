import React from 'react';
import {Col} from 'react-bootstrap';
import {ReactiveGraph} from 'components/reactive-graph/ReactiveGraph';
import AuthComponent from '../AuthComponent';

class PassTheHashMapPageComponent extends AuthComponent {
  constructor(props) {
    super(props);
    this.state = {
      graph: {nodes: [], edges: []},
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
  };

  render() {
    return (
      <div>
        <Col xs={12} lg={8}>
          <h1 className="page-title">3. Pass The Hash Map</h1>
        </Col>
        <Col xs={12}>
          <div style={{height: '80vh'}}>
            <ReactiveGraph graph={this.state.graph} />
          </div>
        </Col>
      </div>
    );
  }
}

export default PassTheHashMapPageComponent;
