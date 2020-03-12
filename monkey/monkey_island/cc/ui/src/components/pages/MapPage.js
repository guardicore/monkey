import React from 'react';
import {Col, Modal} from 'react-bootstrap';
import {Link} from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faStopCircle, faMinus } from '@fortawesome/free-solid-svg-icons'
import InfMapPreviewPaneComponent from 'components/map/preview-pane/InfMapPreviewPane';
import {ReactiveGraph} from 'components/reactive-graph/ReactiveGraph';
import {options, edgeGroupToColor} from 'components/map/MapOptions';
import AuthComponent from '../AuthComponent';

class MapPageComponent extends AuthComponent {
  constructor(props) {
    super(props);
    this.state = {
      graph: {nodes: [], edges: []},
      selected: null,
      selectedType: null,
      killPressed: false,
      showKillDialog: false,
      telemetry: [],
      telemetryLastTimestamp: null,
      movedTop: false,
    };
    this.telemConsole = React.createRef();
    this.handleScroll = this.handleScroll.bind(this);
    this.scrollTop = 0;
  }

  events = {
    select: event => this.selectionChanged(event)
  };

  componentDidMount() {
    this.updateMapFromServer();
    this.interval = setInterval(this.timedEvents, 5000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  timedEvents = () => {
    this.updateMapFromServer();
    this.updateTelemetryFromServer();
  };

  updateMapFromServer = () => {
    this.authFetch('/api/netmap')
      .then(res => res.json())
      .then(res => {
        if (res.hasOwnProperty('edges')) {
          res.edges.forEach(edge => {
            edge.color = {'color': edgeGroupToColor(edge.group)};
          });
          this.setState({graph: res});
          this.props.onStatusChange();
        }
      });
  };

  updateTelemetryFromServer = () => {
    this.authFetch('/api/telemetry-feed?timestamp=' + this.state.telemetryLastTimestamp)
      .then(res => res.json())
      .then(res => {
        if ('telemetries' in res) {
          let newTelem = this.state.telemetry.concat(res['telemetries']);

          this.setState(
            {
              telemetry: newTelem,
              telemetryLastTimestamp: res['timestamp']
            });
          this.props.onStatusChange();

          let telemConsoleRef = this.telemConsole.current;
          if(!this.state.movedTop){
            telemConsoleRef.scrollTop = telemConsoleRef.scrollHeight - telemConsoleRef.clientHeight;
            this.scrollTop = telemConsoleRef.scrollTop;
          }
        }
      });
  };

  selectionChanged(event) {
    if (event.nodes.length === 1) {
      this.authFetch('/api/netmap/node?id=' + event.nodes[0])
        .then(res => res.json())
        .then(res => this.setState({selected: res, selectedType: 'node'}));
    } else if (event.edges.length === 1) {
      let displayedEdge = this.state.graph.edges.find(
        function (edge) {
          return edge['id'] === event.edges[0];
        });
      if (displayedEdge['group'] === 'island') {
        this.setState({selected: displayedEdge, selectedType: 'island_edge'});
      } else {
        this.authFetch('/api/netmap/edge?id=' + event.edges[0])
          .then(res => res.json())
          .then(res => this.setState({selected: res.edge, selectedType: 'edge'}));
      }
    } else {
      this.setState({selected: null, selectedType: null});
    }
  }

  killAllMonkeys = () => {
    this.authFetch('/api?action=killall')
      .then(res => res.json())
      .then(res => this.setState({killPressed: (res.status === 'OK')}));
  };

  renderKillDialogModal = () => {
    return (
      <Modal show={this.state.showKillDialog} onHide={() => this.setState({showKillDialog: false})}>
        <Modal.Body>
          <h2>
            <div className="text-center">Are you sure you want to kill all monkeys?</div>
          </h2>
          <p style={{'fontSize': '1.2em', 'marginBottom': '2em'}}>
            This might take a few moments...
          </p>
          <div className="text-center">
            <button type="button" className="btn btn-danger btn-lg" style={{margin: '5px'}}
                    onClick={() => {
                      this.killAllMonkeys();
                      this.setState({showKillDialog: false});
                    }}>
              Kill all monkeys
            </button>
            <button type="button" className="btn btn-success btn-lg" style={{margin: '5px'}}
                    onClick={() => this.setState({showKillDialog: false})}>
              Cancel
            </button>
          </div>
        </Modal.Body>
      </Modal>
    )

  };

  renderTelemetryEntry(telemetry) {
    return (
      <div key={telemetry.id}>
        <span className="date">{telemetry.timestamp}</span>
        <span className="source"> {telemetry.hostname}:</span>
        <span className="event"> {telemetry.brief}</span>
      </div>
    );
  }

  handleScroll(e){

    let element = e.target;
    if(element.scrollTop < this.scrollTop){
      this.setState({movedTop: true});
    }else{
      this.setState({movedTop: false});
    }

  }

  renderTelemetryConsole() {
    return (
      <div className="telemetry-console" onScroll={this.handleScroll} ref={this.telemConsole}>
        {
          this.state.telemetry.map(this.renderTelemetryEntry)
        }
      </div>
    );
  }

  render() {
    return (
      <div>
        {this.renderKillDialogModal()}
        <Col xs={12} lg={8}>
          <h1 className="page-title">3. Infection Map</h1>
        </Col>
        <Col xs={8}>
          <div className="map-legend">
            <b>Legend: </b>
            <span>Exploit <FontAwesomeIcon icon={faMinus} size="lg" style={{color: '#cc0200'}}/></span>
            <b style={{color: '#aeaeae'}}> | </b>
            <span>Scan <FontAwesomeIcon icon={faMinus} size="lg" style={{color: '#ff9900'}}/></span>
            <b style={{color: '#aeaeae'}}> | </b>
            <span>Tunnel <FontAwesomeIcon icon={faMinus} size="lg" style={{color: '#0158aa'}}/></span>
            <b style={{color: '#aeaeae'}}> | </b>
            <span>Island Communication <FontAwesomeIcon icon={faMinus} size="lg" style={{color: '#a9aaa9'}}/></span>
          </div>
          {this.renderTelemetryConsole()}
          <div style={{height: '80vh'}}>
            <ReactiveGraph graph={this.state.graph} options={options} events={this.events}/>
          </div>
        </Col>
        <Col xs={4}>
          <input className="form-control input-block"
                 placeholder="Find on map"
                 style={{'marginBottom': '1em'}}/>

          <div style={{'overflow': 'auto', 'marginBottom': '1em'}}>
            <Link to="/infection/telemetry" className="btn btn-default pull-left" style={{'width': '48%'}}>Monkey
              Telemetry</Link>
            <button onClick={() => this.setState({showKillDialog: true})} className="btn btn-danger pull-right"
                    style={{'width': '48%'}}>
              <FontAwesomeIcon icon={faStopCircle} style={{'marginRight': '0.5em'}}/>
              Kill All Monkeys
            </button>
          </div>
          {this.state.killPressed ?
            <div className="alert alert-info">
              <i className="glyphicon glyphicon-info-sign" style={{'marginRight': '5px'}}/>
              Kill command sent to all monkeys
            </div>
            : ''}

          <InfMapPreviewPaneComponent item={this.state.selected} type={this.state.selectedType}/>
        </Col>
      </div>
    );
  }
}

export default MapPageComponent;
