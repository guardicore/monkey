import {ObjectFieldTemplateProps} from '@rjsf/utils';
import React, {useState} from 'react';
import {Dropdown} from 'react-bootstrap';
import ChildCheckboxContainer from '../ui-components/ChildCheckbox';
import {AdvancedMultiSelectHeader} from '../ui-components/AdvancedMultiSelect';
import {MasterCheckboxState} from '../ui-components/MasterCheckbox';

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

  let selectorOptions = [];
  for(let [name, schema] of Object.entries(props.schema.properties)) {
    selectorOptions.push({label: schema.title, value: name});
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

  return (
    <div className={'advanced-multi-select'}>
      <AdvancedMultiSelectHeader title={props.schema.title}
                                 onCheckboxClick={() => {}}
                                 checkboxState={MasterCheckboxState.NONE}
                                 hideReset={false}
                                 onResetClick={() => {}}/>

      <ChildCheckboxContainer id={"abc"} multiple={true} required={false}
                              autoFocus={false} selectedValues={enabledPlugins}
                              onCheckboxClick={toggleEnabledPluggin}
                              isSafe={(something) => true}
                              onPaneClick={setPlugin}
                              enumOptions={selectorOptions}/>
      {getPluginDisplay(plugin, props.properties)}
    </div>
  );
}
