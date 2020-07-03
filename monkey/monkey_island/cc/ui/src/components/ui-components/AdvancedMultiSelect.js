import React, {useState} from 'react';

import {Card, Button, Form} from 'react-bootstrap';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faSquare, faCheckSquare} from '@fortawesome/free-solid-svg-icons';
import {cloneDeep} from 'lodash';

import {getComponentHeight} from './utils/HeightCalculator';
import {resolveObjectPath} from './utils/ObjectPathResolver';
import InfoPane from './InfoPane';


function getSelectValuesAfterClick(valueArray, clickedValue) {
  if (valueArray.includes(clickedValue)) {
    return valueArray.filter((e) => {
      return e !== clickedValue;
    });
  } else {
    valueArray.push(clickedValue);
    return valueArray;
  }
}

function onMasterCheckboxClick(checkboxValue, defaultArray, onChangeFnc) {
  if (checkboxValue) {
    onChangeFnc([]);
  } else {
    onChangeFnc(defaultArray);
  }
}

// Definitions passed to components only contains value and label,
// custom fields like "info" or "links" must be pulled from registry object using this function
function getFullDefinitionsFromRegistry(refString, registry) {
  let refArray = refString.replace('#', '').split('/');
  let definitionObject = resolveObjectPath(refArray, registry);
  return definitionObject.anyOf;
}

function getFullDefinitionByKey(refString, registry, itemKey) {
  let fullArray = getFullDefinitionsFromRegistry(refString, registry);
  return fullArray.filter(e => (e.enum[0] === itemKey))[0];
}

function setPaneInfo(refString, registry, itemKey, setPaneInfoFnc) {
  let definitionObj = getFullDefinitionByKey(refString, registry, itemKey);
  setPaneInfoFnc({title: definitionObj.title, content: definitionObj.info, link: definitionObj.link});
}

function AdvancedMultiSelect(props) {
  const [masterCheckbox, setMasterCheckbox] = useState(true);
  const {
    schema,
    id,
    options,
    value,
    required,
    disabled,
    readonly,
    multiple,
    autofocus,
    onChange,
    registry
  } = props;
  const {enumOptions, defaultPaneParams} = options;
  const [infoPaneParams, setInfoPaneParams] = useState(defaultPaneParams);
  const selectValue = cloneDeep(value);
  return (
    <div className={'advanced-multi-select'}>
      <Card.Header>
        <Button key={`${props.schema.title}-button`} value={value}
                variant={'link'} disabled={disabled}
                onClick={() => {
                  onMasterCheckboxClick(masterCheckbox, schema.default, onChange);
                  setMasterCheckbox(!masterCheckbox);
                }}
        >
          <FontAwesomeIcon icon={masterCheckbox ? faCheckSquare : faSquare}/>
        </Button>
        <span className={'header-title'}>{props.schema.title}</span>
      </Card.Header>
      <Form.Group
        style={{height: `${getComponentHeight(enumOptions.length)}px`}}
        id={id}
        multiple={multiple}
        className='choice-block form-control'
        required={required}
        disabled={disabled || readonly}
        autoFocus={autofocus}>
        {enumOptions.map(({value, label}, i) => {
          return (
            <Form.Group
              key={i}
              onClick={() => setPaneInfo(schema.items.$ref, registry, value, setInfoPaneParams)}>
              <Button value={value} variant={'link'} disabled={disabled}
                      onClick={() => onChange(getSelectValuesAfterClick(selectValue, value))}>
                <FontAwesomeIcon icon={selectValue.includes(value) ? faCheckSquare : faSquare}/>
              </Button>
              <span className={'option-text'}>
                {label}
              </span>
            </Form.Group>
          );
        })}
      </Form.Group>
      <InfoPane title={infoPaneParams.title} body={infoPaneParams.content} link={infoPaneParams.link}/>
    </div>
  );
}

export default AdvancedMultiSelect;
