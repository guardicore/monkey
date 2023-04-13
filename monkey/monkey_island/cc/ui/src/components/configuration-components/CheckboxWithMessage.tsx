import React from 'react';
import InfoBox from './InfoBox';
import WarningBox from './WarningBox';

export default function CheckboxWithMessage(props) {

  const getWarningMessageComponent = () => {
    if (Object.prototype.hasOwnProperty.call(props.schema, 'warning_message')) {
      return <WarningBox message={props.schema.warning_message}/>;
    }
    return <></>;
  }

  const getInfoMessageComponent = () => {
    if (Object.prototype.hasOwnProperty.call(props.schema, 'info_message')) {
      return <InfoBox message={props.schema.info_message}/>;
    }
    return <></>;
  }

  const handleChange = (event) => {
    props.onChange(event.target.checked);
  }

  return (
    <div>
      <label>
        <input type='checkbox' checked={props.value} onChange={handleChange} /> {props.schema.title}
      </label>
      {getWarningMessageComponent()}
      {getInfoMessageComponent()}
    </div>
  );
}
