import React from 'react';
import {Button, Card, Form} from 'react-bootstrap';

import {cloneDeep} from 'lodash';

import {getComponentHeight} from './utils/HeightCalculator';
import InfoPane from './InfoPane';
import {MasterCheckbox, MasterCheckboxState} from './MasterCheckbox';
import ChildCheckbox from './ChildCheckbox';
import {getFullDefinitionByKey, getDefaultPaneParams} from './JsonSchemaHelpers';

function AdvancedMultiSelectHeader(props) {
  const {
    title,
    disabled,
    onCheckboxClick,
    checkboxState,
    hideReset,
    onResetClick
  } = props;

  return (
    <Card.Header className="d-flex justify-content-between">
      <MasterCheckbox title={title} disabled={disabled} onClick={onCheckboxClick} checkboxState={checkboxState}/>
      <Button className={'reset-safe-defaults'} type={'reset'} variant={'warning'}
        hidden={hideReset} onClick={onResetClick}>
        Reset to safe defaults
      </Button>
    </Card.Header>
  );
}

class AdvancedMultiSelect extends React.Component {
  constructor(props) {
    super(props);

    this.enumOptions = props.options.enumOptions;
    this.defaultValues = props.schema.default;
    this.infoPaneRefString = props.schema.items.$ref;
    this.registry = props.registry;

    this.state = {
      masterCheckboxState: this.getMasterCheckboxState(props.value),
      hideReset: this.getHideResetState(props.value),
      infoPaneParams: getDefaultPaneParams(this.infoPaneRefString, this.registry)
    };
  }

  onMasterCheckboxClick = () => {
    if (this.state.masterCheckboxState === MasterCheckboxState.ALL) {
      var newValues = [];
    } else {
      newValues = this.enumOptions.map(({value}) => value);
    }

    this.props.onChange(newValues);
    this.setMasterCheckboxState(newValues);
    this.setHideResetState(newValues);
  }

  onChildCheckboxClick = (value) => {
    let selectValues = this.getSelectValuesAfterClick(value);
    this.props.onChange(selectValues);

    this.setMasterCheckboxState(selectValues);
    this.setHideResetState(selectValues);
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
    if (selectValues.length === 0) {
      return MasterCheckboxState.NONE;
    }

    if (selectValues.length != this.enumOptions.length) {
      return MasterCheckboxState.MIXED;
    }

    return MasterCheckboxState.ALL;
  }

  onResetClick = () => {
    this.props.onChange(this.defaultValues);
    this.setHideResetState(this.defaultValues);
    this.setMasterCheckboxState(this.defaultValues);
    this.setPaneInfoToDefault();
  }

  setHideResetState(selectValues) {
    this.setState(() => ({
      hideReset: this.getHideResetState(selectValues)
    }));
  }

  getHideResetState(selectValues) {
    return selectValues.every((value) => this.defaultValues.includes(value));
  }

  setPaneInfo = (itemKey) =>  {
    let definitionObj = getFullDefinitionByKey(this.infoPaneRefString, this.registry, itemKey);
    this.setState({infoPaneParams: {title: definitionObj.title, content: definitionObj.info, link: definitionObj.link}});
  }

  setPaneInfoToDefault() {
    this.setState(() => ({
      infoPaneParams: getDefaultPaneParams(this.props.schema.items.$ref, this.props.registry)
    }));
  }

  render() {
    const {
      schema,
      id,
      required,
      disabled,
      readonly,
      multiple,
      autofocus
    } = this.props;

    return (
      <div className={'advanced-multi-select'}>
        <AdvancedMultiSelectHeader title={schema.title}
          disabled={disabled} onCheckboxClick={this.onMasterCheckboxClick}
          checkboxState={this.state.masterCheckboxState}
          hideReset={this.state.hideReset} onResetClick={this.onResetClick}/>
        <Form.Group
          style={{height: `${getComponentHeight(this.enumOptions.length)}px`}}
          id={id} multiple={multiple} className='choice-block form-control'
          required={required} disabled={disabled || readonly} autoFocus={autofocus}>
          {
            this.enumOptions.map(({value, label}, i) => {
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
