import {ObjectFieldTemplateProps} from '@rjsf/utils';
import React, {useState} from 'react';
import {Dropdown} from 'react-bootstrap';
import ChildCheckboxContainer from '../ui-components/ChildCheckbox';
import {AdvancedMultiSelectHeader} from '../ui-components/AdvancedMultiSelect';
import {MasterCheckboxState} from '../ui-components/MasterCheckbox';
import {getFullDefinitionByKey} from '../ui-components/JsonSchemaHelpers';

const PluginSelector = (props) => {
  let selectOptions = [];
  for (const [name, plugin] of Object.entries(props.plugins)) {
    selectOptions.push(
      <Dropdown.Item onClick={() => props.onClick(name)}
                     eventKey={`plugin['title']`}>
                     {plugin['title']}</Dropdown.Item>
  )}

  return (
    <Dropdown>
      <Dropdown.Toggle variant="success" id="dropdown-basic">
        Select a plugin
      </Dropdown.Toggle>
      <Dropdown.Menu>
        {selectOptions}
      </Dropdown.Menu>
    </Dropdown>
  )
}


export default function PluginSelectorTemplate(props: ObjectFieldTemplateProps) {

  function getPluginDisplay(plugin, allPlugins){
    let selectedPlugin = allPlugins.filter((pluginInArray) => pluginInArray.name == plugin)
    if(selectedPlugin.length === 1){
      return <div className="property-wrapper">{selectedPlugin[0].content}</div>
    }
  }

  console.log(props)

  let [plugin, setPlugin] = useState(null);
  let [enabledPlugins, setEnabledPlugins] = useState([]);

  function getOptions() {
    let selectorOptions = [];
    for(let [name, schema] of Object.entries(props.schema.properties)) {
      selectorOptions.push({label: schema.title, value: name});
    }
    return selectorOptions;
  }

  function toggleEnabledPluggin(pluginName) {
    let plugins = [];
    if(enabledPlugins.includes(pluginName)){
      plugins = enabledPlugins.filter(plugin => plugin !== pluginName)
    } else {
      plugins = [...enabledPlugins, pluginName];
    }
    setEnabledPlugins(plugins);
  }

  function  getMasterCheckboxState(selectValues) {
    if (selectValues.length === 0) {
      return MasterCheckboxState.NONE;
    }

    if (selectValues.length !== getOptions().length) {
      return MasterCheckboxState.MIXED;
    }

    return MasterCheckboxState.ALL;
  }


  function onMasterPluginCheckboxClick() {
    let checkboxState = getMasterCheckboxState(enabledPlugins);
    if (checkboxState == MasterCheckboxState.ALL){
        var newPlugins = [];
    } else {
        newPlugins = getOptions().map(({value}) => value);
    }
    setEnabledPlugins(newPlugins);
  }

  function isPluginSafe(itemKey){
    let itemSchema = Object.entries(props.schema.properties).filter(e => e[0] == itemKey)[0][1];
    return itemSchema['safe'];
  }

  return (
    <div className={'advanced-multi-select'}>
      <AdvancedMultiSelectHeader title={props.schema.title}
                                 onCheckboxClick={onMasterPluginCheckboxClick}
                                 checkboxState={getMasterCheckboxState(enabledPlugins)}
                                 hideReset={false}
                                 onResetClick={() => {}}/>

      <ChildCheckboxContainer id={"abc"} multiple={true} required={false}
                              autoFocus={false} selectedValues={enabledPlugins}
                              onCheckboxClick={toggleEnabledPluggin}
                              isSafe={isPluginSafe}
                              onPaneClick={setPlugin}
                              enumOptions={getOptions()}/>
      {getPluginDisplay(plugin, props.properties)}
    </div>
  );
}
