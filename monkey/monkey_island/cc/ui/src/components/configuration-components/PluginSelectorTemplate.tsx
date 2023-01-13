import {getDefaultFormState, ObjectFieldTemplateProps} from '@rjsf/utils';
import React, {useState} from 'react';
import _ from 'lodash';
import ChildCheckboxContainer from '../ui-components/ChildCheckbox';
import {AdvancedMultiSelectHeader} from '../ui-components/AdvancedMultiSelect';
import {MasterCheckboxState} from '../ui-components/MasterCheckbox';


export default function PluginSelectorTemplate(props: ObjectFieldTemplateProps) {

  function getPluginDisplay(plugin, allPlugins){
    let selectedPlugin = allPlugins.filter((pluginInArray) => pluginInArray.name == plugin)
    if(selectedPlugin.length === 1){
      return <div className="property-wrapper">{selectedPlugin[0].content}</div>
    }
  }

  let [plugin, setPlugin] = useState(null);

  function getOptions() {
    let selectorOptions = [];
    for (let [name, schema] of Object.entries(props.schema.properties)) {
      selectorOptions.push({label: schema.title, value: name});
    }
    return selectorOptions;
  }

  function getEnabledPlugins() {
    let enabled = [];
    for (let plugin of Object.keys(props.formContext.selectedExploiters)) {
      enabled.push(plugin);
    }
    return enabled;
  }

  function togglePluggin(pluginName) {
    let plugins = _.cloneDeep(props.formContext.selectedExploiters);
    if (Object.prototype.hasOwnProperty.call(props.formContext.selectedExploiters, pluginName)) {
      _.unset(plugins, pluginName);
    } else {
      plugins[plugin] = props.formData[plugin];
    }
    props.formContext.setSelectedExploiters(plugins)
  }

  function getMasterCheckboxState(selectValues) {
    if (Object.keys(selectValues).length === 0) {
      return MasterCheckboxState.NONE;
    }

    if (Object.keys(selectValues).length !== getOptions().length) {
      return MasterCheckboxState.MIXED;
    }

    return MasterCheckboxState.ALL;
  }

  function generateDefaultConfig() {
    return getDefaultFormState(props.registry.schemaUtils.validator,
      props.schema, {}, props.registry.rootSchema, true);
  }

  function onMasterPluginCheckboxClick() {
    let checkboxState = getMasterCheckboxState(props.formContext.selectedExploiters);
    if (checkboxState == MasterCheckboxState.ALL) {
      props.formContext.setSelectedExploiters({});
    } else {
      props.formContext.setSelectedExploiters(generateDefaultConfig());
    }
  }

  function isPluginSafe(itemKey) {
    let itemSchema = Object.entries(props.schema.properties).filter(e => e[0] == itemKey)[0][1];
    return itemSchema['safe'];
  }

  return (
    <div className={'advanced-multi-select'}>
      <AdvancedMultiSelectHeader title={props.schema.title}
                                 onCheckboxClick={onMasterPluginCheckboxClick}
                                 checkboxState={
                                   getMasterCheckboxState(props.formContext.selectedExploiters)}
                                 hideReset={false}
                                 onResetClick={() => {
                                 }}/>

      <ChildCheckboxContainer id={'abc'} multiple={true} required={false}
                              autoFocus={false}
                              selectedValues={getEnabledPlugins()}
                              onCheckboxClick={togglePluggin}
                              isSafe={isPluginSafe}
                              onPaneClick={setPlugin}
                              enumOptions={getOptions()}/>
      {getPluginDisplay(plugin, props.properties)}
    </div>
  );
}
