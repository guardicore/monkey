import React from 'react';
import ReactTable from 'react-table';
import {renderArray} from '../common/RenderArrays';
import renderBool from "../common/RenderBool";


const columns = [
  {
    Header: 'Ransomware info',
    columns: [
      {Header: 'Machine', id: 'machine', accessor: x => x.hostname},
      {Header: 'Exploits', id: 'exploits', accessor: x => renderArray(x.exploits)},
      {Header: 'Files got encrypted?', id: 'files_encrypted', accessor: x => renderBool(x.files_encrypted)}
    ]
  }
];

const pageSize = 10;

type TableRow = {
  exploits: [string],
  files_encrypted: boolean,
  hostname: string
}

type Props = {
  tableData: [TableRow]
}

const FileEncryptionTable = (props: Props) => {
  let defaultPageSize = props.tableData.length > pageSize ? pageSize : props.tableData.length;
  let showPagination = props.tableData.length > pageSize;
  return (
    <>
      <h3>
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

export default FileEncryptionTable;
