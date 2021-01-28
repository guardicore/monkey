import React from 'react';
import {Button, Form} from 'react-bootstrap';

import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCheckSquare, faExclamationTriangle} from '@fortawesome/free-solid-svg-icons';
import {faSquare} from '@fortawesome/free-regular-svg-icons';

function ChildCheckbox(props) {
  const {
    onPaneClick,
    onClick,
    value,
    disabled,
    label,
    checkboxState,
    safe
  } = props;

  let displayLabel = [<span key={'label'} className={'option-text'}>{label}</span>];

  if (!safe) {
    displayLabel.push(<FontAwesomeIcon key="unsafe-indicator" className="unsafe-indicator" icon={faExclamationTriangle}/>)
  }

  return (
    <Form.Group onClick={() => onPaneClick(value)}>
      <Button value={value} variant={'link'} disabled={disabled} onClick={() => onClick(value)}>
        <FontAwesomeIcon icon={checkboxState ? faCheckSquare : faSquare}/>
      </Button>
      {displayLabel}
    </Form.Group>
  );
}

export default ChildCheckbox;
