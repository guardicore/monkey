import React, {useEffect, useState} from 'react';
import InlineSelection from '../../../ui-components/inline-selection/InlineSelection';
import DropdownSelect from '../../../ui-components/DropdownSelect';
import {OS_TYPES} from '../utils/OsTypes';
import GenerateLocalWindowsPowershell from '../commands/local_windows_powershell';
import GenerateLocalLinuxWget from '../commands/local_linux_wget';
import GenerateLocalLinuxCurl from '../commands/local_linux_curl';
import CommandDisplay from '../utils/CommandDisplay';
import {Button, Form} from 'react-bootstrap';
import IslandHttpClient, { APIEndpoint } from '../../../IslandHttpClient';
import { useTimer } from 'react-timer-hook';
import { CommandExpirationTimer } from '../utils/CommandExpirationTimer';


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

  const {
    seconds,
    minutes,
    restart
  } = useTimer({ expiryTimestamp: new Date(), onExpire: () => getOtp() });

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
    IslandHttpClient.getJSON(APIEndpoint.agent_otp, {}, true).then(res => {
      setOtp(res.body.otp);
      restart(newExpirationTime());
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

  function newExpirationTime() {
    const time = new Date();
    time.setSeconds(time.getSeconds() + 120);
    console.log('timeout is now: ' + time);
    return time;
  }

  return (
    <>
      <p style={{'fontSize': '1.2em'}}>
        Choose the platform of the machine on which you want to run the Monkey:
      </p>
      <DropdownSelect defaultKey={OS_TYPES.WINDOWS_64} options={osTypes} onClick={setOsType} variant={'outline-monkey'}/>
      <p/>

      <p style={{'fontSize': '1.2em'}}>
        Choose the server from which the machine should download the binary:
      </p>
      <DropdownSelect defaultKey={0} options={props.ips} onClick={setIp} variant={'outline-monkey'}/>
      <p/>

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

      <div style={{'marginTop': '1.4em'}}></div>
      <CommandDisplay commands={commands} onCopy={() => {
        props.tracking.trackEvent({ key: 'agent-start-method', method: 'manual' });
        getOtp();
      }} />
      <div style={{marginTop: '-0.5em', marginBottom: '0.5em'}}>
        <CommandExpirationTimer minutes={minutes} seconds={seconds}/>
      </div>
      <div style={{textAlign: 'right'}}>
        <span>
          <Button title="Copy to Clipboard" onClick={getOtp}>Refresh OTP</Button>
        </span>
      </div>
    </>
  )
}

export default LocalManualRunOptions;
