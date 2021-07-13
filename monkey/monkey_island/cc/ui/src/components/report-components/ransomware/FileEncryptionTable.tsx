import React from 'react';
import ReactTable from 'react-table';
import {renderArray} from '../common/RenderArrays';


type Props = {
  tableData: [TableRow]
}

type TableRow = {
  exploits: [string],
  total_attempts: number,
  successful_encryptions: number,
  hostname: string
}

const pageSize = 10;


const FileEncryptionTable = (props: Props) => {
  let defaultPageSize = props.tableData.length > pageSize ? pageSize : props.tableData.length;
  let showPagination = props.tableData.length > pageSize;
  return (
    <>
      <h3 className={'report-section-header'}>
          File encryption
      </h3>
      <div className="data-table-container">
        <ReactTable
          columns={columns}
          data={props.tableData}
          showPagination={showPagination}
          defaultPageSize={defaultPageSize}
        />
      </div>
    </>
  );
}

const columns = [
  {
    Header: 'Ransomware info',
    columns: [
      {Header: 'Machine', id: 'machine', accessor: x => x.hostname},
      {Header: 'Exploits', id: 'exploits', accessor: x => renderArray(x.exploits)},
      {Header: 'Files encrypted',
        id: 'files_encrypted',
        accessor: x => renderFileEncryptionStats(x.successful_encryptions, x.total_attempts)}
    ]
  }
];

function renderFileEncryptionStats(successful: number, total: number) {
  let textClassName = ''

  if(successful > 0) {
    textClassName = 'text-success'
  } else {
    textClassName = 'text-danger'
  }

  return (<p className={textClassName}>{successful} out of {total}</p>);
}


export default FileEncryptionTable;
