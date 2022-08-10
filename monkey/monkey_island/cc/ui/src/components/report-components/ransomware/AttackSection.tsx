import React, {ReactElement, ReactFragment, useEffect, useState} from 'react';
import IslandHttpClient from '../../IslandHttpClient';
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
    IslandHttpClient.get('/api/telemetry?telem_category=file_encryption')
      .then(resp => setTableData(processTelemetry(resp.body)));
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

function processTelemetry(telemetry): Array<TableRow> {
  // Sort ascending so that newer telemetry records overwrite older ones.
  sortTelemetry(telemetry);

  let latestTelemetry = getLatestTelemetry(telemetry);
  let tableData = getDataForTable(latestTelemetry);

  return tableData;
}

function sortTelemetry(telemetry): void {
  telemetry.objects.sort((a, b) => {
    if (a.timestamp > b.timestamp) {
      return 1;
    } else if (a.timestamp < b.timestamp) {
      return -1;
    }

    return 0;
  });
}

function getLatestTelemetry(telemetry) {
  let latestTelemetry = {};
  for (let i = 0; i < telemetry.objects.length; i++) {
    let monkey = telemetry.objects[i].monkey

    if (! (monkey in latestTelemetry)) {
      latestTelemetry[monkey] = {};
    }

    telemetry.objects[i].data.files.forEach((file_encryption_telemetry) => {
      latestTelemetry[monkey][file_encryption_telemetry.path] = file_encryption_telemetry.success
    });
  }

  return latestTelemetry;
}

function getDataForTable(telemetry): Array<TableRow> {
  let tableData = [];

  for (const monkey in telemetry) {
    for (const path in telemetry[monkey]) {
      if (telemetry[monkey][path]) {
        tableData.push({'hostname': parseHostname(monkey), 'file_path': path});
      }
    }
  }

  return tableData;
}

function parseHostname(monkey: string): string {
    return monkey.match(HOSTNAME_REGEX)[2];
}

export default AttackSection;
