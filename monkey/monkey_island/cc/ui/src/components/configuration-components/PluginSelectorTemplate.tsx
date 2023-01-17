import {getDefaultFormState, ObjectFieldTemplateProps} from '@rjsf/utils';
import React, {useState} from 'react';
import ChildCheckboxContainer from '../ui-components/ChildCheckbox';
import {AdvancedMultiSelectHeader} from '../ui-components/AdvancedMultiSelect';
import {MasterCheckboxState} from '../ui-components/MasterCheckbox';
import {InfoPane, WarningType} from '../ui-components/InfoPane';


export default function PluginSelectorTemplate(props: ObjectFieldTemplateProps) {

  let [selectedPlugin, setSelectedPlugin] = useState(null);

  function getPluginDisplay(plugin, allPlugins) {
    let selectedPlugins = allPlugins.filter((pluginInArray) => pluginInArray.name == plugin)
    if (selectedPlugins.length === 1) {
      let selectedPlugin = selectedPlugins[0];
      let pluginWarningType = isPluginSafe(selectedPlugin.name) ?
        WarningType.NONE : WarningType.SINGLE;
      return <InfoPane title={''}
                       body={selectedPlugin.content}
                       link={selectedPlugin.content.props.schema.link}
                       warningType={pluginWarningType}/>
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

      <ChildCheckboxContainer multiple={true} required={false}
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
