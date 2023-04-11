import * as React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons/faExclamationTriangle';

class CheckboxWithMessage extends React.Component {

  render() {
    let configurationMessageComponent = <></>;

    if (Object.prototype.hasOwnProperty.call(this.props.schema, 'configuration_message')) {
      let className = 'alert alert-' + this.props.schema.configuration_message[0];
      configurationMessageComponent = (
        <div className={className}>
          <FontAwesomeIcon icon={faExclamationTriangle} style={{ 'marginRight': '5px' }} />
          {this.props.schema.configuration_message[1]}
        </div>
      );
    }

    return (
      <div>
        <label>
          <input type='checkbox' /> {this.props.schema.title}
        </label>
        {configurationMessageComponent}
      </div>
    );
  }
}

export default CheckboxWithMessage;
