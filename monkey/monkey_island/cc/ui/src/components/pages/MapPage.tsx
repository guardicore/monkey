import React, {useState} from 'react';
import { Col, Modal, Row } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faStopCircle } from '@fortawesome/free-solid-svg-icons/faStopCircle';
import { faMinus } from '@fortawesome/free-solid-svg-icons/faMinus';
import AuthComponent from '../AuthComponent';
import '../../styles/components/Map.scss';
import { faInfoCircle } from '@fortawesome/free-solid-svg-icons/faInfoCircle';
import ReactiveGraph from '../reactive-graph/ReactiveGraph';
import NodePreviewPane from '../map/preview-pane/NodePreviewPane';


function MapPageComponent (props) {
  const [selected, setSelected] = useState(null);
  const [selectedType, setSelectedType] = useState(null);
  const [killPressed, setKillPressed] = useState(false);
  const [showKillDialog, setShowKillDialog] = useState(false);
  const authComponent = new AuthComponent({});

  const graphEvents = {
    click: event => selectionChanged(event)
  };

  const selectionChanged = (event) => {
    if (event.nodes.length === 1) {
      for (const node of props.mapNodes) {
        if (node.machineId === event.nodes[0]) {
          setSelected(node);
          setSelectedType('node');
          break;
        }
      }
    } else {
      setSelected(null)
      setSelectedType(null);
    }
  }

  const killAllMonkeys = () => {
    authComponent.authFetch('/api/agent-signals/terminate-all-agents',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        // Python uses floating point seconds, Date.now uses milliseconds, so convert
        body: JSON.stringify({ timestamp: Date.now() / 1000.0 })
      },
      true
    )
      .then(() => { setKillPressed(true) });
  };

  const renderKillDialogModal = () => {
    return (
      <Modal show={showKillDialog} onHide={() => setShowKillDialog(false)}>
        <Modal.Body>
          <h2>
            <div className="text-center">Are you sure you want to kill all monkeys?</div>
          </h2>
          <p style={{ 'fontSize': '1.2em', 'marginBottom': '2em' }}>
            This might take up to <b>2 minutes</b>...
          </p>
          <div className="text-center">
            <button type="button" className="btn btn-danger btn-lg" style={{ margin: '5px' }}
              onClick={() => {
                killAllMonkeys();
                setShowKillDialog(false);
              }}>
              Kill all monkeys
            </button>
            <button type="button" className="btn btn-success btn-lg" style={{ margin: '5px' }}
              onClick={() => setShowKillDialog(false)}>
              Cancel
            </button>
          </div>
        </Modal.Body>
      </Modal>
    )
  };

  return (
    <Col sm={{ offset: 3, span: 9 }} md={{ offset: 3, span: 9 }}
      lg={{ offset: 3, span: 9 }} xl={{ offset: 2, span: 10 }}
      className={'main'}>
      <Row>
        {renderKillDialogModal()}
        <Col xs={12} >
          <h1 className="page-title map-page-title">2. Infection Map</h1>
        </Col>
        <Col xs={8} id="map-column">
          <div className="map-legend">
            <b>Legend: </b>
            <span>Exploit <FontAwesomeIcon icon={faMinus} size="lg" style={{ color: '#cc0200' }} /></span>
            <b style={{ color: '#aeaeae' }}> | </b>
            <span>Scan <FontAwesomeIcon icon={faMinus} size="lg" style={{ color: '#ff9900' }} /></span>
            <b style={{ color: '#aeaeae' }}> | </b>
            <span>Tunnel <FontAwesomeIcon icon={faMinus} size="lg" style={{ color: '#0158aa' }} /></span>
            <b style={{ color: '#aeaeae' }}> | </b>
            <span>Island Communication <FontAwesomeIcon icon={faMinus} size="lg" style={{ color: '#a9aaa9' }} /></span>
          </div>
          <div style={{ height: '80vh' }} className={'map-window'}>
            {props.graph?.nodes.length > 0 && <ReactiveGraph graph={props.graph} events={graphEvents} />}
          </div>
        </Col>
        <div style={{width: 0}}>
          <Col xs={3} id="map-preview-column">
            <div style={{ 'overflow': 'auto', 'marginBottom': '1em' }}>
              <Link to="/infection/events" className="btn btn-light pull-left" style={{ 'width': '48%' }}>Monkey
                Events</Link>
              <button onClick={() => setShowKillDialog(true)} className="btn btn-danger pull-right"
                style={{ 'width': '48%' }}>
                <FontAwesomeIcon icon={faStopCircle} style={{ 'marginRight': '0.5em' }} />
                Kill All Monkeys
              </button>
            </div>
            {killPressed ?
              <div className="alert alert-info">
                <FontAwesomeIcon icon={faInfoCircle} style={{ 'marginRight': '5px' }} />
                Kill command sent to all monkeys
              </div>
              : ''}

            <NodePreviewPane item={selected} type={selectedType}
            allNodes={props.mapNodes} />
          </Col>
        </div>
      </Row>
    </Col>
  );
}

export default React.memo(MapPageComponent);
