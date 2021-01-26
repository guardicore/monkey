import React from 'react';
import {Button, Form} from 'react-bootstrap';

import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCheckSquare} from '@fortawesome/free-solid-svg-icons';
import {faSquare} from '@fortawesome/free-regular-svg-icons';

function ChildCheckbox(props) {
  const {
    onPaneClick,
    onClick,
    value,
    disabled,
    label,
    checkboxState
  } = props;

  return (
    <Form.Group onClick={() => onPaneClick(value)}>
      <Button value={value} variant={'link'} disabled={disabled} onClick={() => onClick(value)}>
        <FontAwesomeIcon icon={checkboxState ? faCheckSquare : faSquare}/>
      </Button>
      <span className={'option-text'}>{label}</span>
    </Form.Group>
  );
}

export default ChildCheckbox;
