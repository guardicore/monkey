import React from "react";
import {Card, Button, Form} from 'react-bootstrap';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCheckSquare} from '@fortawesome/free-solid-svg-icons';
import {faMinusSquare} from '@fortawesome/free-solid-svg-icons';
import {faSquare} from '@fortawesome/free-regular-svg-icons';
import {cloneDeep} from 'lodash';

import {getComponentHeight} from './utils/HeightCalculator';
import {resolveObjectPath} from './utils/ObjectPathResolver';
import InfoPane from './InfoPane';

const MasterCheckboxState = {
  NONE: 0,
  MIXED: 1,
  ALL: 2
}

function getFullDefinitionByKey(refString, registry, itemKey) {
  let fullArray = getFullDefinitionsFromRegistry(refString, registry);
  return fullArray.filter(e => (e.enum[0] === itemKey))[0];
}

// Definitions passed to components only contains value and label,
// custom fields like "info" or "links" must be pulled from registry object using this function
function getFullDefinitionsFromRegistry(refString, registry) {
  return getObjectFromRegistryByRef(refString, registry).anyOf;
}

function getObjectFromRegistryByRef(refString, registry) {
  let refArray = refString.replace('#', '').split('/');
  return resolveObjectPath(refArray, registry);
}

function getDefaultPaneParams(refString, registry) {
  let configSection = getObjectFromRegistryByRef(refString, registry);
  return ({title: configSection.title, content: configSection.description});
}

class AdvancedMultiSelect extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      masterCheckboxState: this.getMasterCheckboxState(props.value),
      infoPaneParams: getDefaultPaneParams(props.schema.items.$ref, props.registry)
    };

    this.onMasterCheckboxClick = this.onMasterCheckboxClick.bind(this);
    this.onChildCheckboxClick = this.onChildCheckboxClick.bind(this);
    this.setPaneInfo = this.setPaneInfo.bind(this, props.schema.items.$ref, props.registry);
  }

  onMasterCheckboxClick() {
    let newValues = this.props.options.enumOptions.map(({value}) => value);

    if (this.state.masterCheckboxState == MasterCheckboxState.ALL) {
      newValues = [];
    }

    this.props.onChange(newValues);
    this.setMasterCheckboxState(newValues);
  }

  onChildCheckboxClick(value) {
    let selectValues = this.getSelectValuesAfterClick(value)
    this.props.onChange(selectValues);

    this.setMasterCheckboxState(selectValues);
  }

  getSelectValuesAfterClick(clickedValue) {
    const valueArray = cloneDeep(this.props.value);

    if (valueArray.includes(clickedValue)) {
      return valueArray.filter(e => e !== clickedValue);
    } else {
      valueArray.push(clickedValue);
      return valueArray;
    }
  }

  setMasterCheckboxState(selectValues) {
    this.setState(() => ({
      masterCheckboxState: this.getMasterCheckboxState(selectValues)
    }));
  }

  getMasterCheckboxState(selectValues) {
    if (selectValues.length == 0) {
      return MasterCheckboxState.NONE;
    }

    if (selectValues.length != this.props.options.enumOptions.length) {
      return MasterCheckboxState.MIXED;
    }

    return MasterCheckboxState.ALL;
  }

  setPaneInfo(refString, registry, itemKey) {
    let definitionObj = getFullDefinitionByKey(refString, registry, itemKey);
    this.setState({infoPaneParams: {title: definitionObj.title, content: definitionObj.info, link: definitionObj.link}});
  }

  render() {
    const {
      schema,
      id,
      options,
      value,
      required,
      disabled,
      readonly,
      multiple,
      autofocus
    } = this.props;

    const {enumOptions} = options;

    return (
      <div className={'advanced-multi-select'}>
        <MasterCheckbox title={schema.title} value={value}
          disabled={disabled} onClick={this.onMasterCheckboxClick}
          checkboxState={this.state.masterCheckboxState}/>
        <Form.Group
          style={{height: `${getComponentHeight(enumOptions.length)}px`}}
          id={id} multiple={multiple} className='choice-block form-control'
          required={required} disabled={disabled || readonly} autoFocus={autofocus}>
          {
            enumOptions.map(({value, label}, i) => {
              return (
                <ChildCheckbox key={i} onPaneClick={this.setPaneInfo}
                onClick={this.onChildCheckboxClick} value={value}
                disabled={disabled} label={label} checkboxState={this.props.value.includes(value)}/>
              );
            }
          )}
        </Form.Group>
        <InfoPane title={this.state.infoPaneParams.title}
          body={this.state.infoPaneParams.content}
          link={this.state.infoPaneParams.link}/>
      </div>
    );
  }
}

function MasterCheckbox(props) {
    const {
        title,
        value,
        disabled,
        onClick,
        checkboxState
    } = props;

    let newCheckboxIcon = faCheckSquare;

    if (checkboxState == MasterCheckboxState.NONE) {
      newCheckboxIcon = faSquare;
    } else if (checkboxState == MasterCheckboxState.MIXED) {
      newCheckboxIcon = faMinusSquare;
    }

    return (
        <Card.Header>
            <Button key={`${title}-button`} value={value}
                variant={'link'} disabled={disabled}
                onClick={onClick}>
                <FontAwesomeIcon icon={newCheckboxIcon}/>
            </Button>
            <span className={'header-title'}>{title}</span>
        </Card.Header>
    );
}

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
            <span className={'option-text'}>
                {label}
            </span>
        </Form.Group>
    );
}

export default AdvancedMultiSelect;
