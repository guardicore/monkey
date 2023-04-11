import * as React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons/faExclamationTriangle';

class CheckboxWithMessage extends React.Component {

  render() {
    let warningMessageComponent = <></>;
    let infoMessageComponent = <></>;

    if (Object.prototype.hasOwnProperty.call(this.props.schema, 'warning_message')) {
      warningMessageComponent = (
        <div className='alert alert-warning'>
          <FontAwesomeIcon icon={faExclamationTriangle} style={{ 'marginRight': '5px' }} />
          {this.props.schema.warning_message}
        </div>
      );
    }

    if (Object.prototype.hasOwnProperty.call(this.props.schema, 'info_message')) {
      infoMessageComponent = (
        <div className='alert alert-info'>
          <FontAwesomeIcon icon={faExclamationTriangle} style={{ 'marginRight': '5px' }} />
          {this.props.schema.info_message}
        </div>
      );
    }

    return (
      <div>
        <label>
          <input type='checkbox' /> {this.props.schema.title}
        </label>
        {warningMessageComponent}
        {infoMessageComponent}
      </div>
    );
  }
}

export default CheckboxWithMessage;
