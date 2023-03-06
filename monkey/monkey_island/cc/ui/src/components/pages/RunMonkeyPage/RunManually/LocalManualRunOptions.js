import React, {useEffect, useState} from 'react';
import InlineSelection from '../../../ui-components/inline-selection/InlineSelection';
import DropdownSelect from '../../../ui-components/DropdownSelect';
import {OS_TYPES} from '../utils/OsTypes';
import GenerateLocalWindowsPowershell from '../commands/local_windows_powershell';
import GenerateLocalLinuxWget from '../commands/local_linux_wget';
import GenerateLocalLinuxCurl from '../commands/local_linux_curl';
import CommandDisplay from '../utils/CommandDisplay';
import {Form} from 'react-bootstrap';


const LocalManualRunOptions = (props) => {
  return InlineSelection(getContents, {
    ...props,
    onBackButtonClick: () => {props.setComponent()}
  })
}

const getContents = (props) => {

  const osTypes = {
    [OS_TYPES.WINDOWS_64]: 'Windows 64bit',
    [OS_TYPES.LINUX_64]: 'Linux 64bit'
  }

  const [osType, setOsType] = useState(OS_TYPES.WINDOWS_64);
  const [selectedIp, setSelectedIp] = useState(props.ips[0]);
  const [customUsername, setCustomUsername] = useState('');
  const [commands, setCommands] = useState(generateCommands());

  useEffect(() => {
    setCommands(generateCommands());
  }, [osType, selectedIp, customUsername])

  function setIp(index) {
    setSelectedIp(props.ips[index]);
  }

  function setUsername(inputVal) {
    if (inputVal) {  // checks that it's not just whitespaces
      setCustomUsername(inputVal);
    }
    else {
      setCustomUsername('');
    }
  }

  function generateCommands() {
    if (osType === OS_TYPES.WINDOWS_64) {
      return [{type: 'Powershell', command: GenerateLocalWindowsPowershell(selectedIp, customUsername)}]
    } else {
      return [{type: 'CURL', command: GenerateLocalLinuxCurl(selectedIp, customUsername)},
        {type: 'WGET', command: GenerateLocalLinuxWget(selectedIp, customUsername)}]
    }
  }

  return (
    <>
      <DropdownSelect defaultKey={OS_TYPES.WINDOWS_64} options={osTypes} onClick={setOsType} variant={'outline-monkey'}/>
      <DropdownSelect defaultKey={0} options={props.ips} onClick={setIp} variant={'outline-monkey'}/>
      <div style={{'marginTop': '1.4em'}}>
        <p style={{'fontSize': '1.2em'}}>
          Run as a user by entering their username:
        </p>
        <div>
          <Form>
            <Form.Control
              type="text"
              onChange={input => setUsername(input.target.value.trim())}
            />
          </Form>
        </div>
      </div>
      <CommandDisplay commands={commands}/>
    </>
  )
}

export default LocalManualRunOptions;
