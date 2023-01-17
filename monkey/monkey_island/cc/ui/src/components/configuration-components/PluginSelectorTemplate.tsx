import {getDefaultFormState, ObjectFieldTemplateProps} from '@rjsf/utils';
import React, {useState} from 'react';
import ChildCheckboxContainer from '../ui-components/ChildCheckbox';
import {AdvancedMultiSelectHeader} from '../ui-components/AdvancedMultiSelect';
import {MasterCheckboxState} from '../ui-components/MasterCheckbox';


export default function PluginSelectorTemplate(props: ObjectFieldTemplateProps) {

  let [selectedPlugin, setSelectedPlugin] = useState(null);

  function getPluginDisplay(plugin, allPlugins) {
    let selectedPlugin = allPlugins.filter((pluginInArray) => pluginInArray.name == plugin)
    if (selectedPlugin.length === 1) {
      return <div className="property-wrapper">{selectedPlugin[0].content}</div>
    }
  }

  function getOptions() {
    let selectorOptions = [];
    for (let [name, schema] of Object.entries(props.schema.properties)) {
      selectorOptions.push({label: schema.title, value: name});
    }
    return selectorOptions;
  }

  function togglePluggin(pluginName) {
    let plugins = new Set(props.formContext.selectedExploiters);
    if (props.formContext.selectedExploiters.has(pluginName)) {
      plugins.delete(pluginName);
    } else {
      plugins.add(pluginName);
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
      props.formContext.setSelectedExploiters([]);
    } else {
      props.formContext.setSelectedExploiters(Object.keys(generateDefaultConfig()));
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
                                   getMasterCheckboxState(
                                     [...props.formContext.selectedExploiters])}
                                 hideReset={false}
                                 onResetClick={() => {
                                 }}/>

      <ChildCheckboxContainer id={'abc'} multiple={true} required={false}
                              autoFocus={false}
                              selectedValues={[...props.formContext.selectedExploiters]}
                              onCheckboxClick={togglePluggin}
                              isSafe={isPluginSafe}
                              onPaneClick={setSelectedPlugin}
                              enumOptions={getOptions()}/>
      {getPluginDisplay(selectedPlugin, props.properties)}
    </div>
  );
}
