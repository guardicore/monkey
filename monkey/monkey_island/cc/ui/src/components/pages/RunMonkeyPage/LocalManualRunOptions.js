import React, {useEffect} from 'react';
import NextSelectionButton from '../../ui-components/inline-selection/NextSelectionButton';
import InlineSelection from '../../ui-components/inline-selection/InlineSelection';
import CommandSection from '../../ui-components/inline-selection/CommandSection';
import ManualRunOptions from './ManualRunOptions';
import InterfaceSelection from './InterfaceSelection';

const LocalManualRunOptions = (props) => {
  return InlineSelection(getContents, props, ManualRunOptions)
}

const win64commands = [{name: "CMD", command: "monkey.exe m0nk3y -s 192.168.56.1"}]

const getContents = (props) => {
  return (
    <>
      <NextSelectionButton text={'Windows 64bit'}
                           onButtonClick={() => {
                             props.setComponent(InterfaceSelection('Windows64'))
                           }}/>
      <NextSelectionButton text={'Windows 32bit'} onButtonClick={() => {
      }}/>
      <NextSelectionButton text={'Linux 64bit'} onButtonClick={() => {
      }}/>
      <NextSelectionButton text={'Linux 32bit'} onButtonClick={() => {
      }}/>
    </>
  )
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

export default LocalManualRunOptions;
