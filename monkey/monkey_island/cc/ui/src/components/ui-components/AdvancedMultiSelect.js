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

    this.state = {
      allPluginNames: this.props.value.map(v => v.name),
      masterCheckboxState: this.getMasterCheckboxState(this.props.value.map(v => v.name)),
      pluginDefinitions: getObjectFromRegistryByRef(this.props.schema.items.$ref,
        this.props.registry).pluginDefs,
      selectedPluginNames: this.props.value.map(v => v.name)
    };
  }

  getOptionList = () => {
    return this.props.options.enumOptions.sort(this.compareOptions);
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
    this.setState({selectedPluginNames: newValues.map(v => v.name)});
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
    let checkboxState = this.getMasterCheckboxState(this.state.selectedPluginNames);
    if (checkboxState === MasterCheckboxState.ALL) {
      var newValues = [];
    } else {
      newValues = this.getOptionList().map(({value}) => value);
    }

    this.onChange(newValues);
  }

  onChildCheckboxClick = (value) => {
    let selectValues = this.getSelectValuesAfterClick(value);
    this.onChange(selectValues);

    this.setHideResetState(selectValues);
  }

  getSelectValuesAfterClick(clickedValue) {
    const valueArray = cloneDeep(this.state.selectedPluginNames);

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

    if (selectValues.length !== this.getOptionList().length) {
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
    let fullDef = getFullDefinitionByKey(this.props.schema.items.$ref,
      this.props.registry, itemKey);
    return fullDef.safe;
  }

  setPaneInfo = (itemKey) => {
    let definitionObj = getFullDefinitionByKey(this.props.schema.items.$ref,
      this.props.registry, itemKey);
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
    let safePluginNames = this.state.allPluginNames.filter(pluginName => this.isSafe(pluginName));
    this.setState({selectedPluginNames: safePluginNames});
  }

  render() {
    const {
      autofocus,
      id,
      multiple,
      required,
      schema
    } = this.props;

    let paneParams = getDefaultPaneParams(
      this.props.schema.items.$ref,
      this.props.registry,
      this.isUnsafeOptionSelected(this.state.selectedPluginNames)
    );

    return (
      <div className={'advanced-multi-select'}>
        <AdvancedMultiSelectHeader title={schema.title}
                                   onCheckboxClick={this.onMasterCheckboxClick}
                                   checkboxState={this.getMasterCheckboxState(
                                     this.state.selectedPluginNames)}
                                   hideReset={this.getHideResetState(
                                     this.state.allPluginNames)}
                                   onResetClick={this.onResetClick}/>

        <ChildCheckboxContainer id={id} multiple={multiple} required={required}
                                autoFocus={autofocus} isSafe={this.isSafe}
                                onPaneClick={this.setPaneInfo}
                                onCheckboxClick={this.onChildCheckboxClick}
                                selectedValues={this.state.selectedPluginNames}
                                enumOptions={this.getOptionList()}/>

        <InfoPane title={paneParams.title}
                  body={paneParams.content}
                  link={paneParams.link}
                  warningType={paneParams.warningType}/>
      </div>
    );
  }
}

export default AdvancedMultiSelect;
