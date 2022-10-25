import React, {useEffect, useState} from 'react';
import IslandHttpClient, {APIEndpoint} from '../../IslandHttpClient';
import NumberedReportSection from './NumberedReportSection';
import LoadingIcon from '../../ui-components/LoadingIcon';
import {renderLimitedArray} from '../common/RenderArrays';
import ExternalLink from '../common/ExternalLink';

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
  const [machines, setMachines] = useState(null);

  useEffect(() => {
      IslandHttpClient.get(APIEndpoint.manual_exploitation)
      .then(resp => setMachines(resp.body['manual_exploitations']));
  }, []);

  if(machines !== null){
    let body = getBreachSectionBody(machines);
    return (<NumberedReportSection index={1} title={'Breach'} description={BREACH_DESCRIPTION} body={body}/>)
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
    <b>{machine['hostname']}</b>&nbsp;
      ({renderLimitedArray(machine['ip_addresses'], 2, 'ip-address')}) at <b>{machine['start_time']}</b>
    </li>
  )
}

export default BreachSection;
