import {Modal} from 'react-bootstrap';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faExclamationTriangle} from '@fortawesome/free-solid-svg-icons';
import React, {useEffect, useState} from 'react';


export const ErrorModal = ({showModal,
                            onClose,
                            errorMessage,
                            errorDetails = undefined,
                            errorLevel = 'alert alert-danger'}
                          ) => {
  return (
    <Modal show={showModal} onHide={() => onClose()}>
      <Modal.Header closeButton>
        <Modal.Title> Uh oh... </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <div style={{'marginTop': '1em', 'marginBottom': '1em'}}>
          <div className={errorLevel !== undefined ? errorLevel : "alert alert-danger"}>
            <FontAwesomeIcon icon={faExclamationTriangle} style={{'marginRight': '5px'}}/>
            {errorMessage}
          </div>
        </div>
        {errorDetails !== undefined &&
          <div>
            <hr/>
            <h4>Error Details</h4>
            <p style={{'word-wrap': 'break-word'}}>
              {errorDetails}
            </p>
          </div>
        }
      </Modal.Body>
    </Modal>
  )
};


export default ErrorModal;
