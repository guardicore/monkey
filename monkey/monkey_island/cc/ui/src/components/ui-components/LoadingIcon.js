import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSync } from '@fortawesome/free-solid-svg-icons';
import React from 'react';

function LoadingIcon() {
    return <FontAwesomeIcon icon={faSync} className={`spinning-icon loading-icon`} />;
}

export default LoadingIcon;
