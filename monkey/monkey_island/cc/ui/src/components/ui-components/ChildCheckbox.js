import React from 'react';
import {Button, Form} from 'react-bootstrap';

import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCheckSquare} from '@fortawesome/free-solid-svg-icons';
import {faSquare} from '@fortawesome/free-regular-svg-icons';

import {getComponentHeight} from './utils/HeightCalculator';
import WarningIcon from './WarningIcon';

function ChildCheckboxContainer(props) {
  const {
    enumOptions,
    id,
    multiple,
    required,
    disabled,
    autofocus,
    onPaneClick,
    onCheckboxClick,
    selectedValues,
    isSafe
  } = props;

  return(
    <Form.Group
      style={{height: `${getComponentHeight(enumOptions.length)}px`}}
      id={id} multiple={multiple} className='choice-block form-control'
      required={required} disabled={disabled} autoFocus={autofocus}>
      {
        enumOptions.map(({value, label}, i) => {
          return (
            <ChildCheckbox key={i} onPaneClick={onPaneClick}
            onClick={onCheckboxClick} value={value}
            disabled={disabled} label={label} checkboxState={selectedValues.includes(value)}
            safe={isSafe(value)}/>
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
    disabled,
    label,
    checkboxState,
    safe
  } = props;

  return (
    <Form.Group onClick={() => onPaneClick(value)}>
      <Button value={value} variant={'link'} disabled={disabled} onClick={() => onClick(value)}>
        <FontAwesomeIcon icon={checkboxState ? faCheckSquare : faSquare}/>
      </Button>
      <span key={'label'} className={'option-text'}>{label}</span>
      {!safe && <WarningIcon key="warning-icon"/>}
    </Form.Group>
  );
}

export default ChildCheckboxContainer;
