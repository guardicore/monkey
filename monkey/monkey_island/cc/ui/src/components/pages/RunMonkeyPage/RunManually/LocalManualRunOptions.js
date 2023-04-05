import React, {useEffect, useState} from 'react';
import InlineSelection from '../../../ui-components/inline-selection/InlineSelection';
import DropdownSelect from '../../../ui-components/DropdownSelect';
import {OS_TYPES} from '../utils/OsTypes';
import GenerateLocalWindowsPowershell from '../commands/local_windows_powershell';
import GenerateLocalLinuxWget from '../commands/local_linux_wget';
import GenerateLocalLinuxCurl from '../commands/local_linux_curl';
import CommandDisplay from '../utils/CommandDisplay';
import {Button, Form, Col} from 'react-bootstrap';
import IslandHttpClient, { APIEndpoint } from '../../../IslandHttpClient';


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

  const [otp, setOtp] = useState('');
  const [osType, setOsType] = useState(OS_TYPES.WINDOWS_64);
  const [selectedIp, setSelectedIp] = useState(props.ips[0]);
  const [customUsername, setCustomUsername] = useState('');
  const [commands, setCommands] = useState(generateCommands());


  useEffect(() => {
    getOtp();
  }, [])
  useEffect(() => {
    setCommands(generateCommands());
  }, [osType, selectedIp, customUsername, otp])

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

  function getOtp() {
    IslandHttpClient.get(APIEndpoint.agent_otp).then(res =>{
      setOtp(res.body.otp);
    });
  }

  function generateCommands() {
    if (osType === OS_TYPES.WINDOWS_64) {
      return [{type: 'PowerShell', command: GenerateLocalWindowsPowershell(selectedIp, customUsername, otp)}]
    } else {
      return [{type: 'cURL', command: GenerateLocalLinuxCurl(selectedIp, customUsername, otp)},
        {type: 'Wget', command: GenerateLocalLinuxWget(selectedIp, customUsername, otp)}]
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
      <CommandDisplay commands={commands} onCopy={getOtp} />
        <Col lg={{span:3, offset: 9}} md={{span:4, offset: 8}} sm={{span:4, offset: 8}} xs={12}>
          <Button style={{'float': 'right'}} title="Refresh OTP" onClick={getOtp}>Refresh OTP</Button>
        </Col>
    </>
  )
}

export default LocalManualRunOptions;
