import React from 'react';
import ReactTable from 'react-table';


type Props = {
  telemetry: object,
}

type TableRow = {
  hostname: string,
  file_path: number,
}

const PAGE_SIZE = 10;
const HOSTNAME_REGEX = /^(.* - )?(\S+) :.*$/
const columns = [
  {
    Header: 'Encrypted Files',
    columns: [
      {Header: 'Host', id: 'host', accessor: x => x.hostname},
      {Header: 'File Path', id: 'file_path', accessor: x => x.file_path},
      {Header: 'Encryption Algorithm',
        id: 'encryption_algorithm',
        accessor: () => {return 'Bit Flip'}}
    ]
  }
];

const FileEncryptionTable = (props: Props) => {
  let tableData = processTelemetry(props.telemetry);
  let defaultPageSize = tableData.length > PAGE_SIZE ? PAGE_SIZE : tableData.length;
  let showPagination = tableData.length > PAGE_SIZE;

  return (
    <>
      <h3 className={'report-section-header'}>
          File encryption
      </h3>
      <div className="data-table-container">
        <ReactTable
          columns={columns}
          data={tableData}
          showPagination={showPagination}
          defaultPageSize={defaultPageSize}
        />
      </div>
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
    } else if (a.timestamp > b.timestamp) {
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

  return latestTelemetry
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

function parseHostname(monkey) {
    return monkey.match(HOSTNAME_REGEX)[2]
}

export default FileEncryptionTable;
