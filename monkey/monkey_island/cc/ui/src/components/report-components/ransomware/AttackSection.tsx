import React, {ReactElement, ReactFragment, useEffect, useState} from 'react';
import IslandHttpClient, {APIEndpoint} from '../../IslandHttpClient';
import {FileEncryptionTable, TableRow} from './FileEncryptionTable';
import NumberedReportSection from './NumberedReportSection';
import LoadingIcon from '../../ui-components/LoadingIcon';
import ExternalLink from '../common/ExternalLink';

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
                               text="Learn about the financial impact of ransomware on Guardicore's blog"
                             />
                           </>

const HOSTNAME_REGEX = /^(.* - )?(\S+) :.*$/;

function AttackSection(): ReactElement {
  const [tableData, setTableData] = useState(null);

  useEffect(() => {
    let url_args = {'type': 'FileEncryptionEvent'};
    IslandHttpClient.get(APIEndpoint.agentEvents, url_args)
      .then(resp => setTableData(processEvents(resp.body)));
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

function processEvents(events): Array<TableRow> {
  // Sort events by timestamp, latest first
  sortEvents(events);
  let tableData = getDataForTable(events);
  return tableData;
}

function sortEvents(events): void {
  events.objects.sort((a, b) => {
    if (a.timestamp > b.timestamp) {
      return 1;
    } else if (a.timestamp < b.timestamp) {
      return -1;
    }

    return 0;
  });
}

function getDataForTable(events): Array<TableRow> {
  let tableData = [];

  for (let event in events) {
    if (event['success']) {
      tableData.push({'hostname': parseHostname(event['target']), 'file_path': event['path']});
    }
  }

  return tableData;
}

function parseHostname(monkey: string): string {
    return monkey.match(HOSTNAME_REGEX)[2];
}

export default AttackSection;
