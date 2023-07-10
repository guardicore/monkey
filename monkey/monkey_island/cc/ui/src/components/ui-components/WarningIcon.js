import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';
import React from 'react';

function WarningIcon() {
    return <FontAwesomeIcon className="warning-icon" icon={faExclamationTriangle} />;
}

export default WarningIcon;
