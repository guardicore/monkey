import {getDefaultFormState, ObjectFieldTemplateProps} from '@rjsf/utils';
import React, {useEffect, useState} from 'react';
import _ from 'lodash';
import ChildCheckboxContainer from '../ui-components/ChildCheckbox';
import {AdvancedMultiSelectHeader} from '../ui-components/AdvancedMultiSelect';
import {MasterCheckboxState} from '../ui-components/MasterCheckbox';
import {InfoPane, WarningType} from '../ui-components/InfoPane';
import {EXPLOITERS_PATH_PROPAGATION} from './PropagationConfig';
import MarkdownDescriptionTemplate from './MarkdownDescriptionTemplate';

export const CREDENTIALS_COLLECTORS_CONFIG_PATH = 'credentials_collectors';
const PLUGIN_SCHEMA_PATH = {'propagation': EXPLOITERS_PATH_PROPAGATION, 'credentials_collectors': CREDENTIALS_COLLECTORS_CONFIG_PATH}


export default function PluginSelectorTemplate(props: ObjectFieldTemplateProps) {

  let [activePlugin, setActivePlugin] = useState(null);

  useEffect(() => updateUISchema(), [props.formContext.selectedPlugins]);

  function getPluginDisplay(plugin, allPlugins) {
    let activePlugins = allPlugins.filter((pluginInArray) => pluginInArray.name == plugin);
    if (activePlugins.length === 1) {
      let activePlugin = activePlugins[0];
      let pluginWarningType = isPluginSafe(activePlugin.name) ?
        WarningType.NONE : WarningType.SINGLE;
      return <InfoPane title={''}
                       body={activePlugin.content}
                       link={activePlugin.content.props.schema.link_to_documentation}
                       warningType={pluginWarningType}/>
    }
    return <InfoPane title={props.schema.title}
                     body={props.schema.description}
                     warningType={WarningType.NONE}/>
  }

  function getOptions() {
    let selectorOptions = [];
    for (let [name, schema] of Object.entries(props.schema.properties)) {
      // @ts-expect-error
      selectorOptions.push({label: schema.title, value: name, isActive: (name === activePlugin)});
    }
    return selectorOptions;
  }

  function togglePluggin(pluginName) {
    let plugins = new Set(props.formContext.selectedPlugins);
    if (props.formContext.selectedPlugins.has(pluginName)) {
      plugins.delete(pluginName);
    } else {
      plugins.add(pluginName);
    }
    props.formContext.setSelectedPlugins(plugins, props.formContext.section);
  }

  function updateUISchema(){
    let uiSchema = _.cloneDeep(props.uiSchema);
    for(let pluginName of Object.keys(generateDefaultConfig())) {
      if(!props.formContext.selectedPlugins.has(pluginName)){
        uiSchema[pluginName] = {"ui:readonly": true,
          'ui:DescriptionFieldTemplate': MarkdownDescriptionTemplate};
      } else {
        uiSchema[pluginName] = {'ui:DescriptionFieldTemplate': MarkdownDescriptionTemplate};
      }
    }
    props.formContext.setUiSchema(uiSchema, PLUGIN_SCHEMA_PATH[props.formContext.section]);
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
    // @ts-expect-error
    return getDefaultFormState(props.registry.schemaUtils.validator,
      props.schema, {}, props.registry.rootSchema, true);
  }

  function onMasterPluginCheckboxClick() {
    let checkboxState = getMasterCheckboxState([...props.formContext.selectedPlugins]);
    let selectedSection = props.formContext.section
    if (checkboxState == MasterCheckboxState.ALL) {
      props.formContext.setSelectedPlugins(new Set(), selectedSection);
    } else {
     props.formContext.setSelectedPlugins(new Set(Object.keys(generateDefaultConfig())), selectedSection);
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
    let safePluginNames = [...props.formContext.selectedPlugins].filter(
      pluginName => isPluginSafe(pluginName));
    props.formContext.setSelectedPlugins(new Set(safePluginNames), props.formContext.section);
  }

  return (
    <div className={'advanced-multi-select'}>
      <AdvancedMultiSelectHeader title={props.schema.title}
                                 onCheckboxClick={onMasterPluginCheckboxClick}
                                 checkboxState={
                                   getMasterCheckboxState(
                                     [...props.formContext.selectedPlugins])}
                                 hideReset={getHideResetState(
                                       [...props.formContext.selectedPlugins])}
                                 onResetClick={onResetClick}
                                 resetButtonTitle={'Disable unsafe'}/>
      <ChildCheckboxContainer multiple={true} required={false}
                              autoFocus={true}
                              selectedValues={[...props.formContext.selectedPlugins]}
                              onCheckboxClick={togglePluggin}
                              isSafe={isPluginSafe}
                              onPaneClick={setActivePlugin}
                              enumOptions={getOptions()}/>
      {getPluginDisplay(activePlugin, props.properties)}
    </div>
  );
}
