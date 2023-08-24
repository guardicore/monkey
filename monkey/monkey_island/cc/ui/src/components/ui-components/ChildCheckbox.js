import React from 'react';
import {Button, Form} from 'react-bootstrap';

import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCheckSquare} from '@fortawesome/free-solid-svg-icons';
import {faSquare} from '@fortawesome/free-regular-svg-icons';

import WarningIcon from './WarningIcon';

function ChildCheckboxContainer(props) {
  const {
    enumOptions,
    id,
    multiple,
    required,
    autofocus,
    onPaneClick,
    onCheckboxClick,
    selectedValues,
    isSafe
  } = props;

  return(
    <Form.Group
      style={{height: 'auto', maxHeight: '250px'}}
      id={id} multiple={multiple} className='choice-block form-control'
      required={required} autoFocus={autofocus}>
      {
        enumOptions.map(({value, label, isActive}, i) => {

          return (
            <ChildCheckbox key={i} onPaneClick={onPaneClick}
            onClick={onCheckboxClick} value={value}
            label={label} checkboxState={selectedValues.includes(value)}
            safe={isSafe(value)} active={isActive}/>
          );
        }
      )}
    </Form.Group>
  );
}

function ChildCheckbox(props) {
  const {
    onPaneClick,
    onClick,
    value,
    label,
    checkboxState,
    safe,
    active
  } = props;

  return (
    <Form.Group onClick={() => onPaneClick(value)} className={active ? 'active-checkbox': ''}>
      <Button value={value} variant={'link'} onClick={() => onClick(value)}>
        <FontAwesomeIcon icon={checkboxState ? faCheckSquare : faSquare}/>
      </Button>
      <span key={'label'} className={'option-text'}>{label}</span>
      {!safe && <WarningIcon key="warning-icon"/>}
    </Form.Group>
  );
}

export default ChildCheckboxContainer;
