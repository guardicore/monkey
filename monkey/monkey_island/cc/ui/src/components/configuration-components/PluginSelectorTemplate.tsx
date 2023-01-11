import {ObjectFieldTemplateProps} from '@rjsf/utils';
import React, {useState} from 'react';
import {Dropdown} from 'react-bootstrap';

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

  let [element, setElement] = useState(null);
  return (
    <div>
      {props.title}
      {props.description}
      <PluginSelector plugins={props.schema.properties}
                      onClick={(pluginName) => {
        setElement(pluginName)
      }}/>
      {getPluginDisplay(element, props.properties)}
    </div>
  );
}
