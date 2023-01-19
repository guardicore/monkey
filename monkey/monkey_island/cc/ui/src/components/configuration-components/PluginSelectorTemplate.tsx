import {getDefaultFormState, ObjectFieldTemplateProps} from '@rjsf/utils';
import React, {useEffect, useState} from 'react';
import _ from 'lodash';
import ChildCheckboxContainer from '../ui-components/ChildCheckbox';
import {AdvancedMultiSelectHeader} from '../ui-components/AdvancedMultiSelect';
import {MasterCheckboxState} from '../ui-components/MasterCheckbox';
import {InfoPane, WarningType} from '../ui-components/InfoPane';
import {EXPLOITERS_PATH_PROPAGATION} from './PropagationConfig';


export default function PluginSelectorTemplate(props: ObjectFieldTemplateProps) {

  let [activePlugin, setActivePlugin] = useState(null);

  useEffect(() => updateUISchema(), [props.formContext.selectedExploiters]);

  function getPluginDisplay(plugin, allPlugins) {
    let activePlugins = allPlugins.filter((pluginInArray) => pluginInArray.name == plugin);
    if (activePlugins.length === 1) {
      let activePlugin = activePlugins[0];
      let pluginWarningType = isPluginSafe(activePlugin.name) ?
        WarningType.NONE : WarningType.SINGLE;
      return <InfoPane title={''}
                       body={activePlugin.content}
                       link={activePlugin.content.props.schema.link}
                       warningType={pluginWarningType}/>
    }
    return <InfoPane title={props.schema.title}
                     body={props.schema.description}
                     warningType={WarningType.NONE}/>
  }

  function getOptions() {
    let selectorOptions = [];
    for (let [name, schema] of Object.entries(props.schema.properties)) {
      selectorOptions.push({label: schema.title, value: name, isActive: (name === activePlugin)});
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
    props.formContext.setSelectedExploiters(plugins);
  }

  function updateUISchema(){
    let uiSchema = _.cloneDeep(props.uiSchema);
    for(let pluginName of Object.keys(generateDefaultConfig())) {
      if(!props.formContext.selectedExploiters.has(pluginName)){
        uiSchema[pluginName] = {"ui:readonly": true};
      } else {
        uiSchema[pluginName] = {};
      }
    }
    props.formContext.setUiSchema(uiSchema, EXPLOITERS_PATH_PROPAGATION);
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
    let checkboxState = getMasterCheckboxState([...props.formContext.selectedExploiters]);
    if (checkboxState == MasterCheckboxState.ALL) {
      props.formContext.setSelectedExploiters(new Set());
    } else {
      props.formContext.setSelectedExploiters(new Set(Object.keys(generateDefaultConfig())));
    }
  }

  function isPluginSafe(itemKey) {
    let itemSchema = Object.entries(props.schema.properties).filter(e => e[0] == itemKey)[0][1];
    return itemSchema['safe'];
  }

  function getHideResetState(selectValues) {
    return !(isUnsafePluginSelected(selectValues))
  }

  function isUnsafePluginSelected(selectValues) {
    return !(selectValues.every((value) => isPluginSafe(value)));
  }

  function onResetClick() {
    let safePluginNames = [...props.formContext.selectedExploiters].filter(
      pluginName => isPluginSafe(pluginName));
    props.formContext.setSelectedExploiters(new Set(safePluginNames));
  }

  return (
    <div className={'advanced-multi-select'}>
      <AdvancedMultiSelectHeader title={props.schema.title}
                                 onCheckboxClick={onMasterPluginCheckboxClick}
                                 checkboxState={
                                   getMasterCheckboxState(
                                     [...props.formContext.selectedExploiters])}
                                 hideReset={getHideResetState(
                                       [...props.formContext.selectedExploiters])}
                                 onResetClick={onResetClick}
                                 resetButtonTitle={'Disable unsafe exploiters'}/>
      <ChildCheckboxContainer multiple={true} required={false}
                              autoFocus={true}
                              selectedValues={[...props.formContext.selectedExploiters]}
                              onCheckboxClick={togglePluggin}
                              isSafe={isPluginSafe}
                              onPaneClick={setActivePlugin}
                              enumOptions={getOptions()}/>
      {getPluginDisplay(activePlugin, props.properties)}
    </div>
  );
}
