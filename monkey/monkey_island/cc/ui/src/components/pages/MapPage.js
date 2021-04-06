import React from 'react';
import {Col, Modal, Row} from 'react-bootstrap';
import {Link} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faStopCircle} from '@fortawesome/free-solid-svg-icons/faStopCircle';
import {faMinus} from '@fortawesome/free-solid-svg-icons/faMinus';
import PreviewPaneComponent from 'components/map/preview-pane/PreviewPane';
import {ReactiveGraph} from 'components/reactive-graph/ReactiveGraph';
import {getOptions, edgeGroupToColor} from 'components/map/MapOptions';
import AuthComponent from '../AuthComponent';
import '../../styles/components/Map.scss';
import {faInfoCircle} from '@fortawesome/free-solid-svg-icons/faInfoCircle';

class MapPageComponent extends AuthComponent {
  constructor(props) {
    super(props);
    this.state = {
      graph: {nodes: [], edges: []},
      nodeStateList:[],
      selected: null,
      selectedType: null,
      killPressed: false,
      showKillDialog: false,
      telemetry: [],
      telemetryLastTimestamp: null,
      isScrolledUp: false,
      telemetryLines: 0,
      telemetryCurrentLine: 0,
      telemetryUpdateInProgress: false
    };
    this.telemConsole = React.createRef();
    this.handleScroll = this.handleScroll.bind(this);
    this.scrollTop = 0;
  }

  events = {
    select: event => this.selectionChanged(event)
  };

  componentDidMount() {
    this.getNodeStateListFromServer();
    this.updateMapFromServer();
    this.interval = setInterval(this.timedEvents, 5000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  getNodeStateListFromServer = () => {
    this.authFetch('/api/netmap/nodeStates')
      .then(res => res.json())
      .then(res => {
        this.setState({nodeStateList: res.node_states});
      });
  };

  timedEvents = () => {
    this.updateMapFromServer();
    this.updateTelemetryFromServer();
  };

  updateMapFromServer = () => {
    this.authFetch('/api/netmap')
      .then(res => res.json())
      .then(res => {
        if (Object.prototype.hasOwnProperty.call(res, 'edges')) {
          res.edges.forEach(edge => {
            edge.color = {'color': edgeGroupToColor(edge.group)};
          });
          this.setState({graph: res});
          this.props.onStatusChange();
        }
      });
  };

  updateTelemetryFromServer = () => {
    if (this.state.telemetryUpdateInProgress) {
      return
    }
    this.setState({telemetryUpdateInProgress: true});
    this.authFetch('/api/telemetry-feed?timestamp=' + this.state.telemetryLastTimestamp)
      .then(res => res.json())
      .then(res => {
        if ('telemetries' in res) {
          let newTelem = this.state.telemetry.concat(res['telemetries']);
          this.setState(
            {
              telemetry: newTelem,
              telemetryLastTimestamp: res['timestamp'],
              telemetryUpdateInProgress: false
            });
          this.props.onStatusChange();

          let telemConsoleRef = this.telemConsole.current;
          if (!this.state.isScrolledUp) {
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

  handleScroll(e) {
    let element = e.target;

    let telemetryStyle = window.getComputedStyle(element);
    let telemetryLineHeight = parseInt((telemetryStyle.lineHeight).replace('px', ''));

    this.setState({
      isScrolledUp: (element.scrollTop < this.scrollTop),
      telemetryCurrentLine: Math.trunc(element.scrollTop / telemetryLineHeight) + 1,
      telemetryLines: Math.trunc(element.scrollHeight / telemetryLineHeight)
    });
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

  renderTelemetryLineCount() {
    return (
      <div className="telemetry-lines">
        <b>[{this.state.telemetryCurrentLine}/{this.state.telemetryLines}]</b>
      </div>
    );
  }

  render() {
    return (
      <Col sm={{offset: 3, span: 9}} md={{offset: 3, span: 9}}
           lg={{offset: 3, span: 9}} xl={{offset: 2, span: 10}}
           className={'main'}>
        <Row>
          {this.renderKillDialogModal()}
          <Col xs={12} lg={8}>
            <h1 className="page-title">2. Infection Map</h1>
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
            <div style={{height: '80vh'}} className={'map-window'}>
              {this.renderTelemetryLineCount()}
              {this.renderTelemetryConsole()}
              <ReactiveGraph graph={this.state.graph} options={getOptions(this.state.nodeStateList)}
                             events={this.events}/>
            </div>
          </Col>
          <Col xs={4}>
            <div style={{'overflow': 'auto', 'marginBottom': '1em'}}>
              <Link to="/infection/telemetry" className="btn btn-light pull-left" style={{'width': '48%'}}>Monkey
                Telemetry</Link>
              <button onClick={() => this.setState({showKillDialog: true})} className="btn btn-danger pull-right"
                      style={{'width': '48%'}}>
                <FontAwesomeIcon icon={faStopCircle} style={{'marginRight': '0.5em'}}/>
                Kill All Monkeys
              </button>
            </div>
            {this.state.killPressed ?
              <div className="alert alert-info">
                <FontAwesomeIcon icon={faInfoCircle} style={{'marginRight': '5px'}} />
                Kill command sent to all monkeys
              </div>
              : ''}

            <PreviewPaneComponent item={this.state.selected} type={this.state.selectedType}/>
          </Col>
        </Row>
      </Col>
    );
  }
}

export default MapPageComponent;
