import React from 'react';
import {Form} from 'react-bootstrap';

import {cloneDeep} from 'lodash';

import {getComponentHeight} from './utils/HeightCalculator';
import InfoPane from './InfoPane';
import {MasterCheckbox, MasterCheckboxState} from './MasterCheckbox';
import ChildCheckbox from './ChildCheckbox';
import {getFullDefinitionByKey, getDefaultPaneParams} from './JsonSchemaHelpers.js';

class AdvancedMultiSelect extends React.Component {
  constructor(props) {
    super(props)

    this.enumOptions = props.options.enumOptions;

    this.state = {
      masterCheckboxState: this.getMasterCheckboxState(props.value),
      infoPaneParams: getDefaultPaneParams(props.schema.items.$ref, props.registry)
    };

    this.onMasterCheckboxClick = this.onMasterCheckboxClick.bind(this);
    this.onChildCheckboxClick = this.onChildCheckboxClick.bind(this);
    this.setPaneInfo = this.setPaneInfo.bind(this, props.schema.items.$ref, props.registry);
  }

  onMasterCheckboxClick() {
    if (this.state.masterCheckboxState === MasterCheckboxState.ALL) {
      var newValues = [];
    } else {
      newValues = this.enumOptions.map(({value}) => value);
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
    if (selectValues.length === 0) {
      return MasterCheckboxState.NONE;
    }

    if (selectValues.length != this.enumOptions.length) {
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
      required,
      disabled,
      readonly,
      multiple,
      autofocus
    } = this.props;

    return (
      <div className={'advanced-multi-select'}>
        <MasterCheckbox title={schema.title}
          disabled={disabled} onClick={this.onMasterCheckboxClick}
          checkboxState={this.state.masterCheckboxState}/>
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
