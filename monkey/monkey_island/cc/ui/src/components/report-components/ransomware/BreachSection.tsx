import React, {useEffect, useState} from 'react';
import NumberedReportSection from './NumberedReportSection';
import LoadingIcon from '../../ui-components/LoadingIcon';
import {renderLimitedArray} from '../common/RenderArrays';
import ExternalLink from '../common/ExternalLink';
import {getAllAgents, getAllMachines, getManuallyStartedAgents, getMachineByAgent, getMachineHostname} from '../../utils/ServerUtils';

const BREACH_DESCRIPTION = <>
                             Ransomware attacks start after machines in the internal network get
                             compromised. The initial compromise was simulated by running Monkey Agents
                             manually. Detecting ransomware at this stage will minimize the impact to the
                             organization.
                             <br />
                             <br />
                             <ExternalLink
                               url="https://www.akamai.com/blog/security/4-techniques-for-early-ransomware-detection/?utm_medium=monkey-request&utm_source=web-report&utm_campaign=monkey-security-report"
                               text="Learn techniques for early ransomware detection on Guardicore's blog"
                             />
                           </>

function BreachSection() {
  const [agents, setAgents] = useState(null);
  const [machines, setMachines] = useState(null);

  useEffect(() => {
    getAllAgents().then(agents => setAgents(agents));
    getAllMachines().then(machines => setMachines(machines));
  }, []);

  if((machines !== null) && (agents !== null)){
    let manuallyExploitedMachines = getManuallyExploitedMachines(agents, machines);
    let body = getBreachSectionBody(manuallyExploitedMachines);
    return (<NumberedReportSection index={1} title={'Breach'} description={BREACH_DESCRIPTION} body={body}/>)
  } else {
    return <LoadingIcon />
  }
}

function getManuallyExploitedMachines(agents, machines){
  let manuallyExploitedMachines = [];
  let manuallyStartedAgents = getManuallyStartedAgents(agents);
  for (let agent of manuallyStartedAgents) {
    let machine = getMachineByAgent(agent, machines);
    if (machine !== null){
      let manuallyExploitatedMachine = {};
      manuallyExploitatedMachine['hostname'] = getMachineHostname(machine);
      manuallyExploitatedMachine['ip_addresses'] = machine['network_interfaces'].map(network_interface => network_interface.split('/')[0]);
      manuallyExploitatedMachine['start_time'] = startTimeToLocaleString(agent['start_time']);

      manuallyExploitedMachines.push(manuallyExploitatedMachine);
    }
  }

  return manuallyExploitedMachines;
}

function startTimeToLocaleString(startTime) {
  let startTimeTimestamp = Date.parse(startTime);
  let startTimeDate = new Date();
  startTimeDate.setTime(startTimeTimestamp);

  return startTimeDate.toLocaleString('en-us');
}

function getBreachSectionBody(machines) {
    let machineList = [];
    for(let i = 0; i < machines.length; i++){
      machineList.push(getMachine(machines[i]));
    }
    return (
      <div className={'ransomware-breach-section'}>
        <p>Ransomware attack started from these machines on the network:</p>
        <ul>
          {machineList}
        </ul>
      </div>
    )
  }

function getMachine(machine) {
  return (
    <li key={machine['hostname']+machine['start_time']}>
    <b>{machine['hostname']}</b>&nbsp;
      ({renderLimitedArray(machine['ip_addresses'], 2, 'ip-address')}) at <b>{machine['start_time']}</b>
    </li>
  )
}

export default BreachSection;
