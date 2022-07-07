import {Button, Col, Container, Modal, NavLink, Row} from 'react-bootstrap';
import React, {useState} from 'react';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faExclamationTriangle} from '@fortawesome/free-solid-svg-icons/faExclamationTriangle';

import '../../styles/components/IslandResetModal.scss';
import {Routes} from '../Main';
import LoadingIcon from './LoadingIcon';
import {faCheck} from '@fortawesome/free-solid-svg-icons';
import AuthService from '../../services/AuthService';

type Props = {
  show: boolean,
  allMonkeysAreDead: boolean,
  onClose: () => void
}

// Button statuses
const Idle = 1;
const Loading = 2;
const Done = 3;

const IslandResetModal = (props: Props) => {

  const [resetAllStatus, setResetAll] = useState(Idle);
  const [deleteStatus, setDeleteStatus] = useState(Idle);
  const auth = new AuthService();

  return (
    <Modal show={props.show} onHide={() => {
      setDeleteStatus(Idle);
      props.onClose()
    }} size={'lg'}>
      <Modal.Header closeButton>
        <Modal.Title>Reset the Island</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {
          !props.allMonkeysAreDead ?
            <div className='alert alert-warning'>
              <FontAwesomeIcon icon={faExclamationTriangle} style={{'marginRight': '5px'}}/>
              Please stop all running agents before attempting to reset the Island.
            </div>
            :
            showModalButtons()
        }
      </Modal.Body>
    </Modal>
  )

  function displayDeleteData() {
    if (deleteStatus === Idle) {
      return (
        <button type='button' className='btn btn-danger btn-lg' style={{margin: '5px'}}
                onClick={() => {
                  setDeleteStatus(Loading);
                  clearSimulationData(() => {
                      setDeleteStatus(Done)
                    })
                }}>
          Delete data
        </button>
      )
    } else if (deleteStatus === Loading) {
      return (<LoadingIcon/>)
    } else if (deleteStatus === Done) {
      return (<FontAwesomeIcon icon={faCheck} className={'status-success'} size={'2x'}/>)
    }
  }

  function displayResetAll() {
    if (resetAllStatus === Idle) {
      return (
        <button type='button' className='btn btn-danger btn-lg' style={{margin: '5px'}}
                onClick={() => {
                  setResetAll(Loading);
                  try {
                    resetAll();
                    setResetAll(Done);
                    props.onClose();
                  } catch (err) {
                    // TODO: Display error message to user
                    console.error(err)
                  }
                }}>
          Reset the Island
        </button>
      )
    } else if (resetAllStatus === Loading) {
      return (<LoadingIcon/>)
    } else if (resetAllStatus === Done) {
      return (<FontAwesomeIcon icon={faCheck} className={'status-success'} size={'2x'}/>)
    }
  }

  function clearSimulationData(callback: () => void) {
    auth.authFetch('/api/clear-simulation-data', {method: 'POST'})
      .then(res => {
        if (res.status === 200) {
          callback();
        }
      })
  }

  function resetAll() {
    auth.authFetch('/api/reset-agent-configuration', {method: 'POST'})
      .then(res => {
        if (res.status === 200) {
            return auth.authFetch('/api/clear-simulation-data', {method: 'POST'})
        }
      })
      .then(res => {
        if (res.status === 200) {
          return auth.authFetch('/api/reset-configured-propagation-credentials', {method: 'POST'})
        }
      })
      .then(res => {
        if (res.status === 200) {
            return auth.authFetch('/api/island-mode', {method: 'POST', body: '{"mode": "unset"}'})
        }
      })
      .then(res => {
        if (res.status !== 200) {
          throw 'Error resetting the simulation'
        }
      })
  }

  function showModalButtons() {
    return (<Container className={`text-left island-reset-modal`}>
      <Row>
        <Col>
          <p>Delete data gathered by Monkey agents.</p>
          <p>This will reset the Map and reports.</p>
        </Col>
        <Col sm={4} className={'text-center'}>
          {displayDeleteData()}
        </Col>
      </Row>
      <hr/>
      <Row>
        <Col>
          <p>Reset everything.</p>
          <p>You might want to <Button variant={'link'} href={Routes.ConfigurePage}>export
            configuration</Button> before doing this.</p>
        </Col>
        <Col sm={4} className={'text-center'}>
          {displayResetAll()}
        </Col>
      </Row>
    </Container>)
  }
}

export default IslandResetModal;
