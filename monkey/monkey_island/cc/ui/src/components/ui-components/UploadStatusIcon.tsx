import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';
import React from 'react';

export const UploadStatuses = {
    clean: 'clean',
    success: 'success',
    error: 'error'
};

const UploadStatusIcon = (props: { status: string }) => {
    switch (props.status) {
        case UploadStatuses.success:
            return <FontAwesomeIcon icon={faCheck} className={'upload-status-icon-success'} />;
        case UploadStatuses.error:
            return <FontAwesomeIcon icon={faTimes} className={'upload-status-icon-error'} />;
        default:
            return null;
    }
};

export default UploadStatusIcon;
