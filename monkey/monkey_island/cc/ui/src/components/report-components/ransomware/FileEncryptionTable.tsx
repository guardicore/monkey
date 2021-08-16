import React from 'react';
import ReactTable from 'react-table';


type TableRow = {
  hostname: string,
  file_path: number,
}

const PAGE_SIZE = 10;
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

const FileEncryptionTable = ({tableData}: {tableData: Array<TableRow>}) => {
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

export {FileEncryptionTable, TableRow};
