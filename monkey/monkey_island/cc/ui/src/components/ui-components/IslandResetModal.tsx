import React, {useState} from 'react';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faExclamationTriangle} from '@fortawesome/free-solid-svg-icons/faExclamationTriangle';

import '../../styles/components/IslandResetModal.scss';
import LoadingIcon from './LoadingIcon';
import {faCheck} from '@fortawesome/free-solid-svg-icons';
import AuthService from '../../services/AuthService';
import {Modal} from 'react-bootstrap';
import {Grid} from '@mui/material';

type Props = {
  show: boolean,
  allMonkeysAreDead: boolean,
  onClose: () => void,
  onReset: () => void
}

// Button statuses
const Idle = 1;
const Loading = 2;
const Done = 3;

const IslandResetModal = (props: Props) => {

  const [deleteStatus, setDeleteStatus] = useState(Idle);
  const auth = new AuthService();

  return (
    <Modal show={props.show} onHide={() => {
      setDeleteStatus(Idle);
      props.onClose()
    }} size={'lg'}>
      <Modal.Header closeButton>
        <Modal.Title>Reset simulation</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {
          !props.allMonkeysAreDead ?
            <div className='alert alert-warning'>
              <FontAwesomeIcon icon={faExclamationTriangle} style={{'marginRight': '5px'}}/>
              Please stop all running agents before attempting to delete gathered data.
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

  function clearSimulationData(callback: () => void) {
    auth.authFetch('/api/clear-simulation-data', {method: 'POST'})
      .then(res => {
        if (res.ok) {
          callback();
        }
      })
  }

  function showModalButtons() {
    return (
    <Grid container rowSpacing={3}>
      <Grid xs={12} item>
        <h5 style={{'textAlign': 'center'}}>This action will reset the map and reports.</h5>
      </Grid>
      <Grid xs={12} item style={{'textAlign': 'center'}}>
          {displayDeleteData()}
      </Grid>
    </Grid>)
  }
}

export default IslandResetModal;
