import {Button, Modal, Form} from 'react-bootstrap';
import React from 'react';

type Props = {
  show: boolean,
  onClick: () => void
}


const PasswordInput = (props) => {
  return (
    <div className={'config-export-password-input'}>
      <p>Encrypt with a password:</p>
      <Form.Control type='password' placeholder='Password' />
    </div>
  )
}


const ConfigExportModal = (props: Props) => {
  return (
    <Modal show={props.show}
           onHide={props.onClick}
           size={'lg'}>
      <Modal.Header closeButton>
        <Modal.Title>Configuration export</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <div key={'config-export-option'} className='mb-3'>
          <Form.Check
            type={'radio'}
            id={'password'}
            label={<PasswordInput/>}
          />

          <Form.Check
            type={'radio'}
            label={'Skip encryption (export as plaintext)'}
          />
        </div>
      </Modal.Body>
      <Modal.Footer>
        <Button variant='secondary' onClick={props.onClick}>
          Close
        </Button>
        <Button variant='primary' onClick={props.onClick}>
          Save Changes
        </Button>
      </Modal.Footer>
    </Modal>)
}

export default ConfigExportModal;
