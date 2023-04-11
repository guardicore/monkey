import * as React from 'react';
import InfoBox from './InfoBox';
import WarningBox from './WarningBox';

class CheckboxWithMessage extends React.Component {

  render() {
    let warningMessageComponent = <></>;
    let infoMessageComponent = <></>;

    if (Object.prototype.hasOwnProperty.call(this.props.schema, 'warning_message')) {
      warningMessageComponent = <WarningBox message={this.props.schema.warning_message}/>;
    }

    if (Object.prototype.hasOwnProperty.call(this.props.schema, 'info_message')) {
      infoMessageComponent = <InfoBox message={this.props.schema.info_message}/>;
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
