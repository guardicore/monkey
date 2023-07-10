import { Modal } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';
import React from 'react';
import '../../styles/components/ErrorModal.scss';

interface Props {
    showModal: boolean;
    onClose: () => void;
    errorMessage: string;
    errorDetails?: string;
    errorLevel?: string;
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
                <div className={'error-modal'}>
                    <div className={`alert alert-${errorLevel}`}>
                        <FontAwesomeIcon
                            icon={faExclamationTriangle}
                            style={{ marginRight: '5px' }}
                        />
                        {errorMessage}
                    </div>
                </div>
                {errorDetails !== undefined && (
                    <div>
                        <hr />
                        <h4>Error Details</h4>
                        <p className={'error-details'}>{errorDetails}</p>
                    </div>
                )}
            </Modal.Body>
        </Modal>
    );
};

export default ErrorModal;
