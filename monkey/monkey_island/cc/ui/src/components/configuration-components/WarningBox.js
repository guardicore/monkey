import * as React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons/faExclamationTriangle';

class WarningBox extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="alert alert-warning">
                <FontAwesomeIcon icon={faExclamationTriangle} style={{ marginRight: '5px' }} />
                {this.props.message}
            </div>
        );
    }
}

export default WarningBox;
