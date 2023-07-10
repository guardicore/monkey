import React from 'react';
import { Modal, Button } from 'react-bootstrap';

function UnsafeConfigOptionsConfirmationModal(props) {
    return (
        <Modal
            show={props.show}
            className={'unsafe-config-options-confirmation-modal'}
            backdropClassName={'unsafe-config-options-confirmation-modal-backdrop'}>
            <Modal.Body>
                <h2>
                    <div className="text-center">Warning</div>
                </h2>
                <p className="text-center" style={{ fontSize: '1.2em', marginBottom: '2em' }}>
                    Some of the configuration options selected could cause systems to become
                    unstable or malfunction.
                    <br />
                    <br />
                    Are you sure you want to submit the selected settings?
                </p>
                <div className="text-center">
                    <Button
                        type="button"
                        className="btn btn-secondary"
                        size="lg"
                        style={{ margin: '5px' }}
                        onClick={props.onCancelClick}>
                        Cancel
                    </Button>
                    <Button
                        type="button"
                        className="btn btn-danger"
                        size="lg"
                        style={{ margin: '5px' }}
                        onClick={props.onContinueClick}>
                        Submit
                    </Button>
                </div>
            </Modal.Body>
        </Modal>
    );
}

export default UnsafeConfigOptionsConfirmationModal;
