import React from 'react';
import {Button, Card} from 'react-bootstrap';

import {cloneDeep} from 'lodash';

import {getDefaultPaneParams, InfoPane, WarningType} from './InfoPane';
import {MasterCheckbox, MasterCheckboxState} from './MasterCheckbox';
import ChildCheckboxContainer from './ChildCheckbox';
import {getFullDefinitionByKey} from './JsonSchemaHelpers';

export function AdvancedMultiSelectHeader(props) {
  const {
    title,
    onCheckboxClick,
    checkboxState,
    hideReset,
    onResetClick,
    resetButtonTitle
  } = props;


  return (
    <Card.Header className="d-flex justify-content-between">
      <MasterCheckbox title={title} onClick={onCheckboxClick} checkboxState={checkboxState}/>
      <Button className={'reset-safe-defaults'} type={'reset'} variant={'warning'}
              hidden={hideReset} onClick={onResetClick}>
        {resetButtonTitle}
      </Button>
    </Card.Header>
  );
}

class AdvancedMultiSelect extends React.Component {
  constructor(props) {
    super(props);
    let nameOptions = this.getOptions();
    let allPluginNames = nameOptions.map(v => v.value);

    this.state = {
      nameOptions: nameOptions
    };
    this.state = {
      nameOptions: nameOptions,
      infoPaneParams: getDefaultPaneParams(
        this.props.schema.items,
        this.isUnsafeOptionSelected(this.getSelectedPluginNames())
      ),
      allPluginNames: allPluginNames,
      masterCheckboxState: this.getMasterCheckboxState(this.getSelectedPluginNames()),
      pluginDefinitions: this.props.schema.items.pluginDefs
    };
  }

  getOptions(activeElementKey) {
    let names = this.props.schema.items.properties.name.anyOf;
    names = names.map(v => ({
      label: v.title,
      schema: v,
      value: v.enum[0],
      isActive: (v.enum[0] === activeElementKey)
    }));
    return names.sort(this.compareOptions);
  }

  getSelectedPluginNames = () => {
    return this.props.value.map(v => v.name);
  }

  onChange = (strValues) => {
    let pluginArray = this.namesToPlugins(strValues, this.state.pluginDefinitions);
    this.props.onChange(pluginArray)
  }

  namesToPlugins = (names, allPlugins) => {
    let plugins = [];
    for (let i = 0; i < names.length; i++) {
      plugins.push(cloneDeep(allPlugins[names[i]]));
    }
    return plugins
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
    let checkboxState = this.getMasterCheckboxState(this.getSelectedPluginNames());
    if (checkboxState === MasterCheckboxState.ALL) {
      var newValues = [];
    } else {
      newValues = this.getOptions().map(({value}) => value);
    }

    this.onChange(newValues);
  }

  onChildCheckboxClick = (value) => {
    let selectValues = this.getSelectValuesAfterClick(value);
    this.onChange(selectValues);
  }

  getSelectValuesAfterClick(clickedValue) {
    const valueArray = cloneDeep(this.getSelectedPluginNames());

    if (valueArray.includes(clickedValue)) {
      return valueArray.filter(e => e !== clickedValue);
    } else {
      valueArray.push(clickedValue);
      return valueArray;
    }
  }

  getMasterCheckboxState(selectValues) {
    if (selectValues.length === 0) {
      return MasterCheckboxState.NONE;
    }

    if (selectValues.length !== this.getOptions().length) {
      return MasterCheckboxState.MIXED;
    }

    return MasterCheckboxState.ALL;
  }

  onResetClick = () => {
    this.setPaneInfoToSafe();
  }

  getHideResetState(selectValues) {
    return !(this.isUnsafeOptionSelected(selectValues))
  }

  isUnsafeOptionSelected(selectValues) {
    return !(selectValues.every((value) => this.isSafe(value)));
  }

  isSafe = (itemKey) => {
    let fullDef = getFullDefinitionByKey(this.props.schema.items.properties.name, itemKey);
    return fullDef.safe;
  }

  setPaneInfo = (itemKey) => {
    let definitionObj = getFullDefinitionByKey(this.props.schema.items.properties.name, itemKey);
    this.setState(
      {
        nameOptions: this.getOptions(itemKey),
        infoPaneParams: {
          title: definitionObj.title,
          content: definitionObj.info,
          link: definitionObj.link,
          warningType: this.isSafe(itemKey) ? WarningType.NONE : WarningType.SINGLE
        }
      }
    );
  }

  setPaneInfoToSafe() {
    let safePluginNames = this.state.allPluginNames.filter(pluginName => this.isSafe(pluginName));
    this.onChange(safePluginNames);
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
      <div className={'advanced-multi-select'} onFocus={this.props.onFocus}>
        <AdvancedMultiSelectHeader title={schema.title}
                                   onCheckboxClick={this.onMasterCheckboxClick}
                                   checkboxState={this.getMasterCheckboxState(
                                     this.getSelectedPluginNames())}
                                   hideReset={this.getHideResetState(
                                     this.getSelectedPluginNames())}
                                   onResetClick={this.onResetClick}/>

        <ChildCheckboxContainer id={id} multiple={multiple} required={required}
                                autoFocus={autofocus} isSafe={this.isSafe}
                                onPaneClick={this.setPaneInfo}
                                onCheckboxClick={this.onChildCheckboxClick}
                                selectedValues={this.getSelectedPluginNames()}
                                enumOptions={this.state.nameOptions}/>

        <InfoPane title={this.state.infoPaneParams.title}
                  body={this.state.infoPaneParams.content}
                  link={this.state.infoPaneParams.link}
                  warningType={this.state.infoPaneParams.warningType}/>
      </div>
    );
  }
}

export default AdvancedMultiSelect;
