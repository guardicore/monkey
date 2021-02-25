import React from 'react';
import {Modal, Button} from 'react-bootstrap';

function UnsafeOptionsConfirmationModal(props) {
  return (
    <Modal show={props.show}>
      <Modal.Body>
        <h2>
          <div className='text-center'>Warning</div>
        </h2>
        <p className='text-center' style={{'fontSize': '1.2em', 'marginBottom': '2em'}}>
          You have selected some options which are not safe for all environments.
          These options could cause some systems to become unstable or malfunction.
          Are you sure you want to use the selected settings?
        </p>
        <div className='text-center'>
          <Button type='button'
                  className='btn btn-success'
                  size='lg'
                  style={{margin: '5px'}}
                  onClick={() => {props.onCancelClick()}}>
            Cancel
          </Button>
          <Button type='button'
                  className='btn btn-danger'
                  size='lg'
                  style={{margin: '5px'}}
                  onClick={() => {props.onContinueClick()}}>
            I know what I'm doing.
          </Button>
        </div>
      </Modal.Body>
    </Modal>
  )
}

export default UnsafeOptionsConfirmationModal;
