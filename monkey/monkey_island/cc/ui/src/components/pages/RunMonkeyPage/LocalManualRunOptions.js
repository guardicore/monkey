import React, {useEffect, useState} from 'react';
import InlineSelection from '../../ui-components/inline-selection/InlineSelection';
import DropdownSelect from '../../ui-components/DropdownSelect';
import {OS_TYPES} from './OsTypes';
import GenerateLocalWindowsCmd from './commands/local_windows_cmd';
import GenerateLocalWindowsPowershell from './commands/local_windows_powershell';
import GenerateLocalLinuxWget from './commands/local_linux_wget';
import GenerateLocalLinuxCurl from './commands/local_linux_curl';
import CommandDisplay from './CommandDisplay';


const LocalManualRunOptions = (props) => {
  return InlineSelection(getContents, {
    ...props,
    onBackButtonClick: () => {props.setComponent()}
  })
}

const getContents = (props) => {

  const osTypes = {
    [OS_TYPES.WINDOWS_64]: 'Windows 64bit',
    [OS_TYPES.WINDOWS_32]: 'Windows 32bit',
    [OS_TYPES.LINUX_64]: 'Linux 64bit',
    [OS_TYPES.LINUX_32]: 'Linux 32bit'
  }

  const [osType, setOsType] = useState(OS_TYPES.WINDOWS_64);
  const [selectedIp, setSelectedIp] = useState(props.ips[0]);
  const [commands, setCommands] = useState(generateCommands());

  useEffect(() => {
    setCommands(generateCommands());
  }, [osType, selectedIp])

  function setIp(index) {
    setSelectedIp(props.ips[index]);
  }

  function generateCommands() {
    if (osType === OS_TYPES.WINDOWS_64 || osType === OS_TYPES.WINDOWS_32) {
      return [{type: 'CMD', command: GenerateLocalWindowsCmd(selectedIp, osType)},
        {type: 'Powershell', command: GenerateLocalWindowsPowershell(selectedIp, osType)}]
    } else {
      return [{type: 'CURL', command: GenerateLocalLinuxCurl(selectedIp, osType)},
        {type: 'WGET', command: GenerateLocalLinuxWget(selectedIp, osType)}]
    }
  }

  return (
    <>
      <DropdownSelect defaultKey={OS_TYPES.WINDOWS_64} options={osTypes} onClick={setOsType} variant={'outline-monkey'}/>
      <DropdownSelect defaultKey={0} options={props.ips} onClick={setIp} variant={'outline-monkey'}/>
      <CommandDisplay commands={commands}/>
    </>
  )
}

export default LocalManualRunOptions;
