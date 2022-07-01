import React from 'react';
import {Button, Card} from 'react-bootstrap';

import {cloneDeep} from 'lodash';

import {getDefaultPaneParams, InfoPane, WarningType} from './InfoPane';
import {MasterCheckbox, MasterCheckboxState} from './MasterCheckbox';
import ChildCheckboxContainer from './ChildCheckbox';
import {getFullDefinitionByKey, getObjectFromRegistryByRef} from './JsonSchemaHelpers';

function AdvancedMultiSelectHeader(props) {
  const {
    title,
    onCheckboxClick,
    checkboxState,
    hideReset,
    onResetClick
  } = props;


  return (
    <Card.Header className="d-flex justify-content-between">
      <MasterCheckbox title={title} onClick={onCheckboxClick} checkboxState={checkboxState}/>
      <Button className={'reset-safe-defaults'} type={'reset'} variant={'warning'}
              hidden={hideReset} onClick={onResetClick}>
        Reset to safe options
      </Button>
    </Card.Header>
  );
}

class AdvancedMultiSelect extends React.Component {
  constructor(props) {
    super(props);
    this.infoPaneRefString = props.schema.items.$ref;
    this.registry = props.registry;
    this.enumOptions = props.options.enumOptions.sort(this.compareOptions);
    this.pluginNames = props.value.map(v => v.name);

    this.state = {
      masterCheckboxState: this.getMasterCheckboxState(this.pluginNames),
      infoPaneParams: getDefaultPaneParams(
        this.infoPaneRefString,
        this.registry,
        this.isUnsafeOptionSelected(this.pluginNames)
      ),
      pluginDefinitions: getObjectFromRegistryByRef(this.infoPaneRefString,
        this.registry).pluginDefs,
      pluginNames: props.value.map(v => v.name)
    };
  }

  onChange = (strValues) => {
    let newValues = [];
    for (let j = 0; j < strValues.length; j++) {
      let found = false;
      for (let i = 0; i < this.props.value.length; i++) {
        if (strValues[j] === this.props.value[i]['name']) {
          newValues.push(JSON.parse(JSON.stringify(this.props.value[i])))
          found = true;
          break;
        }
      }
      if (!found) {
        newValues.push(this.state.pluginDefinitions[strValues[j]]);
      }
    }
    newValues = JSON.parse(JSON.stringify(newValues));
    this.props.onChange(newValues)
    this.setState({pluginNames: newValues.map(v => v.name)});
  }

  // Sort options alphabetically. "Unsafe" options float to the top so that they
  // do not get selected and hidden at the bottom of the list.
  compareOptions = (a, b) => {
    // Apparently, you can use additive operators with boolean types. Ultimately,
    // the ToNumber() abstraction operation is called to convert the booleans to
    // numbers: https://tc39.es/ecma262/#sec-tonumeric
    if (this.isSafe(a.value) - this.isSafe(b.value) !== 0) {
      return this.isSafe(a.value) - this.isSafe(b.value);
    }

    return a.value.localeCompare(b.value);
  }

  onMasterCheckboxClick = () => {
    let checkboxState = this.getMasterCheckboxState(this.state.pluginNames);
    if (checkboxState === MasterCheckboxState.ALL) {
      var newValues = [];
    } else {
      newValues = this.enumOptions.map(({value}) => value);
    }

    this.onChange(newValues);
  }

  onChildCheckboxClick = (value) => {
    let selectValues = this.getSelectValuesAfterClick(value);
    this.onChange(selectValues);

    this.setHideResetState(selectValues);
  }

  getSelectValuesAfterClick(clickedValue) {
    const valueArray = cloneDeep(this.state.pluginNames);

    if (valueArray.includes(clickedValue)) {
      return valueArray.filter(e => e !== clickedValue);
    } else {
      valueArray.push(clickedValue);
      return valueArray;
    }
  }

  setMasterCheckboxState(selectValues) {
    let newState = this.getMasterCheckboxState(selectValues);
    if (newState !== this.state.masterCheckboxState) {
      this.setState({masterCheckboxState: newState});
    }
  }

  getMasterCheckboxState(selectValues) {
    if (selectValues.length === 0) {
      return MasterCheckboxState.NONE;
    }

    if (selectValues.length !== this.enumOptions.length) {
      return MasterCheckboxState.MIXED;
    }

    return MasterCheckboxState.ALL;
  }

  onResetClick = () => {
    this.onChange(this.defaultValues);
    this.setHideResetState(this.defaultValues);
    this.setPaneInfoToSafe(this.isUnsafeOptionSelected(this.defaultValues));
  }

  setHideResetState(selectValues) {
    this.setState(() => ({
      hideReset: this.getHideResetState(selectValues)
    }));
  }

  getHideResetState(selectValues) {
    return !(this.isUnsafeOptionSelected(selectValues))
  }

  isUnsafeOptionSelected(selectValues) {
    return !(selectValues.every((value) => this.isSafe(value)));
  }

  isSafe = (itemKey) => {
    return getFullDefinitionByKey(this.infoPaneRefString, this.registry, itemKey).safe;
  }

  setPaneInfo = (itemKey) => {
    let definitionObj = getFullDefinitionByKey(this.infoPaneRefString, this.registry, itemKey);
    this.setState(
      {
        infoPaneParams: {
          title: definitionObj.title,
          content: definitionObj.info,
          link: definitionObj.link,
          warningType: this.isSafe(itemKey) ? WarningType.NONE : WarningType.SINGLE
        }
      }
    );
  }

  setPaneInfoToSafe(isUnsafeOptionSelected) {
    this.setState(() => ({
      infoPaneParams: getDefaultPaneParams(
        this.props.schema.items.$ref,
        this.props.registry,
        isUnsafeOptionSelected
      )
    }));
  }

  render() {
    const {
      autofocus,
      id,
      multiple,
      required,
      schema
    } = this.props;

    return (
      <div className={'advanced-multi-select'}>
        <AdvancedMultiSelectHeader title={schema.title}
                                   onCheckboxClick={this.onMasterCheckboxClick}
                                   checkboxState={this.getMasterCheckboxState(this.state.pluginNames)}
                                   hideReset={this.getHideResetState(this.pluginNames)}
                                   onResetClick={this.onResetClick}/>

        <ChildCheckboxContainer id={id} multiple={multiple} required={required}
                                autoFocus={autofocus} isSafe={this.isSafe}
                                onPaneClick={this.setPaneInfo}
                                onCheckboxClick={this.onChildCheckboxClick}
                                selectedValues={this.state.pluginNames}
                                enumOptions={this.enumOptions}/>

        <InfoPane title={this.state.infoPaneParams.title}
                  body={this.state.infoPaneParams.content}
                  link={this.state.infoPaneParams.link}
                  warningType={this.state.infoPaneParams.warningType}/>
      </div>
    );
  }
}

export default AdvancedMultiSelect;
