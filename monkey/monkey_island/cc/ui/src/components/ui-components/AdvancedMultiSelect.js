import React from "react";
import {Card, Button, Form} from 'react-bootstrap';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCheckSquare} from '@fortawesome/free-solid-svg-icons';
import {faSquare} from '@fortawesome/free-regular-svg-icons';
import {cloneDeep} from 'lodash';

import {getComponentHeight} from './utils/HeightCalculator';
import {resolveObjectPath} from './utils/ObjectPathResolver';
import InfoPane from './InfoPane';


// Definitions passed to components only contains value and label,
// custom fields like "info" or "links" must be pulled from registry object using this function
function getFullDefinitionsFromRegistry(refString, registry) {
  return getObjectFromRegistryByRef(refString, registry).anyOf;
}

function getObjectFromRegistryByRef(refString, registry) {
  let refArray = refString.replace('#', '').split('/');
  return resolveObjectPath(refArray, registry);
}

function getFullDefinitionByKey(refString, registry, itemKey) {
  let fullArray = getFullDefinitionsFromRegistry(refString, registry);
  return fullArray.filter(e => (e.enum[0] === itemKey))[0];
}

function getDefaultPaneParams(refString, registry) {
  let configSection = getObjectFromRegistryByRef(refString, registry);
  return ({title: configSection.title, content: configSection.description});
}

function MasterCheckbox(props) {
    const {
        title,
        value,
        disabled,
        onClick,
        checkboxState
    } = props;

    return (
        <Card.Header>
            <Button key={`${title}-button`} value={value}
                variant={'link'} disabled={disabled}
                onClick={onClick}>
                <FontAwesomeIcon icon={checkboxState ? faCheckSquare : faSquare}/>
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

class AdvancedMultiSelect extends React.Component {
  constructor(props) {
    super(props)
    this.state = {masterCheckbox: true, infoPaneParams: getDefaultPaneParams(props.schema.items.$ref, props.registry)};
    this.onMasterCheckboxClick = this.onMasterCheckboxClick.bind(this);
    this.onChildCheckboxClick = this.onChildCheckboxClick.bind(this);
    this.setPaneInfo = this.setPaneInfo.bind(this, props.schema.items.$ref, props.registry);
  }

  onMasterCheckboxClick() {
    if (this.state.masterCheckbox) {
      this.props.onChange([]);
    } else {
      this.props.onChange(this.props.schema.default);
    }

    this.toggleMasterCheckbox();
  }

  onChildCheckboxClick(value) {
    this.props.onChange(this.getSelectValuesAfterClick(value));
  }

  getSelectValuesAfterClick(clickedValue) {
    const valueArray = cloneDeep(this.props.value);

    if (valueArray.includes(clickedValue)) {
      return valueArray.filter((e) => {
        return e !== clickedValue;
      });
    } else {
      valueArray.push(clickedValue);
      return valueArray;
    }
  }

  toggleMasterCheckbox() {
    this.setState((state) => ({
      masterCheckbox: !state.masterCheckbox
    }));
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
      autofocus,
      onChange,
      registry
    } = this.props;

    const {enumOptions} = options;
    getDefaultPaneParams(schema.items.$ref, registry);

    return (
      <div className={'advanced-multi-select'}>
        <MasterCheckbox title={schema.title} value={value}
          disabled={disabled} onClick={this.onMasterCheckboxClick}
          checkboxState={this.state.masterCheckbox}/>
        <Form.Group
          style={{height: `${getComponentHeight(enumOptions.length)}px`}}
          id={id}
          multiple={multiple}
          className='choice-block form-control'
          required={required}
          disabled={disabled || readonly}
          autoFocus={autofocus}>
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

export default AdvancedMultiSelect;
