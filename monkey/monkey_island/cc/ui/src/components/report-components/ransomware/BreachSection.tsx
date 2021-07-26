import React, {useEffect, useState} from 'react';
import IslandHttpClient from '../../IslandHttpClient';
import NumberedReportSection from './NumberedReportSection';
import LoadingIcon from '../../ui-components/LoadingIcon';
import {renderLimitedArray} from '../common/RenderArrays';

function BreachSection() {
  const [machines, setMachines] = useState(null);
  let description = 'Ransomware attacks start after machines in the internal network get compromised. ' +
    'The initial compromise was simulated by running monkeys manually.';

  useEffect(() => {
    IslandHttpClient.get('/api/exploitations/manual')
      .then(resp => setMachines(resp.body['manual_exploitations']));
  }, []);

  if(machines !== null){
    let body = getBreachSectionBody(machines);
    return (<NumberedReportSection index={1} title={'Breach'} description={description} body={body}/>)
  } else {
    return <LoadingIcon />
  }
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
    <li key={machine['hostname']}>
    <b>{machine['hostname']}</b>
      ({renderLimitedArray(machine['ip_addresses'], 2, 'ip-address')}) at {machine['start_time']}
    </li>
  )
}

export default BreachSection;
