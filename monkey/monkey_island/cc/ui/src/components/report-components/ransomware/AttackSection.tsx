import React, {ReactElement, ReactFragment, useEffect, useState} from 'react';
import IslandHttpClient, {APIEndpoint} from '../../IslandHttpClient';
import {FileEncryptionTable, TableRow} from './FileEncryptionTable';
import NumberedReportSection from './NumberedReportSection';
import LoadingIcon from '../../ui-components/LoadingIcon';
import ExternalLink from '../common/ExternalLink';
import {getEventSourceHostname} from '../../utils/ServerUtils';

// TODO: Fix the url
const ATTACK_DESCRIPTION = <>
                             After the attacker or malware has propagated through your network,
                             your data is at risk on any machine the attacker can access. It can be
                             encrypted and held for ransom, exfiltrated, or manipulated in
                             whatever way the attacker chooses.
                             <br />
                             <br />
                             <ExternalLink
                               url="https://web.archive.org/web/20210510221915/https://www.guardicore.com/blog/what-are-ransomware-costs/"
                               text="Learn about the financial impact of ransomware on Akamai's blog"
                             />
                           </>

const HOSTNAME_REGEX = /^(.* - )?(\S+) :.*$/;

function AttackSection(): ReactElement {
  const [tableData, setTableData] = useState(null);

  useEffect(() => {
    let agents = [];
    let machines = [];

    let agent_events_url_args = {'type': 'FileEncryptionEvent'};
    IslandHttpClient.getJSON(APIEndpoint.agents, {}, true)
      .then(res => agents = res.body)
      .then(() => IslandHttpClient.getJSON(APIEndpoint.machines, {}, true)
        .then(res => machines = res.body)
        .then(() => IslandHttpClient.getJSON(APIEndpoint.agentEvents, agent_events_url_args, true)
          .then(res => setTableData(processEvents(res.body, agents, machines)))
        )
      )
  }, []);


  if (tableData == null) {
      return <LoadingIcon />
  }

  return (
    <NumberedReportSection
      index={3}
      title='Attack'
      description={ATTACK_DESCRIPTION}
      body={getBody(tableData)}
    />
  );
}

function getBody(tableData): ReactFragment {
  return (
    <>
      <p>Infection Monkey has encrypted <strong>{tableData.length} files</strong> on your network.</p>
      {(tableData.length > 0) && <FileEncryptionTable tableData={tableData} />}
    </>
  );
}

function processEvents(events, agents, machines): Array<TableRow> {
  // Sort events by timestamp, latest first
  sortEvents(events);
  let tableData = getDataForTable(events, agents, machines);
  return tableData;
}

function sortEvents(events): void {
  events.sort((a, b) => {
    if (a.timestamp > b.timestamp) {
      return 1;
    } else if (a.timestamp < b.timestamp) {
      return -1;
    }

    return 0;
  });
}

function getDataForTable(events, agents, machines): Array<TableRow> {
  let tableData = [];

  for (let event of events) {
    if (event['success'] === true) {
      tableData.push({'hostname': getEventSourceHostname(event['source'], agents, machines), 'file_path': event['file_path']['path']});
    }
  }

  return tableData;
}

export default AttackSection;
