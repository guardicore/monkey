import React, {useEffect, useState} from 'react';
import NextSelectionButton from '../../ui-components/inline-selection/NextSelectionButton';
import InlineSelection from '../../ui-components/inline-selection/InlineSelection';
import CommandSection from '../../ui-components/inline-selection/CommandSection';
import LocalManualRunOptions from './LocalManualRunOptions';

function InterfaceSelection(props) {
  return InlineSelection(getContents, props, LocalManualRunOptions)
}

const getContents = (props) => {
  const ips = props.ips.map((ip) =>
    <div>{ip}</div>
  );
  return (<div>{ips}</div>);
}

const setCommandAsContent = (props) => {
  let commandComponent = () => InlineSelection(CommandSection,
    {
      commands: win64commands,
      setComponent: props.setComponent
    },
    LocalManualRunOptions
  );
  props.setComponent(commandComponent, props);
}

export default InterfaceSelection;
