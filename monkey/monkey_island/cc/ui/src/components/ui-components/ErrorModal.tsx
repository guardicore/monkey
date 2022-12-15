import {Modal} from 'react-bootstrap';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faExclamationTriangle} from '@fortawesome/free-solid-svg-icons';
import React from 'react';


interface Props {
  showModal: boolean,
  onClose: () => void,
  errorMessage: string,
  errorDetails?: string,
  errorLevel?: string
}


export const ErrorModal = ({
                             showModal,
                             onClose,
                             errorMessage,
                             errorDetails = undefined,
                             errorLevel = 'danger'
                           }: Props) => {
  return (
    <Modal show={showModal} onHide={() => onClose()}>
      <Modal.Header closeButton>
        <Modal.Title> Uh oh... </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <div style={{'marginTop': '1em', 'marginBottom': '1em'}}>
          <div className={`alert alert-${errorLevel}`}>
            <FontAwesomeIcon icon={faExclamationTriangle} style={{'marginRight': '5px'}}/>
            {errorMessage}
          </div>
        </div>
        {errorDetails !== undefined &&
          <div>
            <hr/>
            <h4>Error Details</h4>
            <p style={{'word-wrap': 'break-word', 'white-space': 'pre-wrap'}}>
              {errorDetails}
            </p>
          </div>
        }
      </Modal.Body>
    </Modal>
  )
};


export default ErrorModal;
