import React, {ReactElement} from 'react';
import {FileEncryptionTable, TableRow} from './FileEncryptionTable';
import NumberedReportSection from './NumberedReportSection';

const ATTACK_DESCRIPTION = 'After the attacker or malware has propagated through your network, \
                            your data is at risk on any machine the attacker can access. It can be \
                            encrypted and held for ransomware, exfiltrated, or manipulated in \
                            whatever way the attacker chooses.'
const HOSTNAME_REGEX = /^(.* - )?(\S+) :.*$/;

function AttackSection({telemetry}: {telemetry: object}): ReactElement {
  let tableData = processTelemetry(telemetry);
  let body = (
    <>
      <p>Infection Monkey has encrypted <strong>{tableData.length} files</strong> on your network:</p>
      <FileEncryptionTable tableData={tableData} />
    </>
  );

  return (
    <NumberedReportSection
      index={3}
      title='Attack'
      description={ATTACK_DESCRIPTION}
      body={body}
    />
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
