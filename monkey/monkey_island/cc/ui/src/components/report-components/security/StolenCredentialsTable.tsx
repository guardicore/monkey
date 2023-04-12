import React, {useEffect, useState} from 'react';
import ReactTable from 'react-table'
import LoadingIcon from '../../ui-components/LoadingIcon';
import {reformatSecret} from '../credentialParsing';
import _ from 'lodash';
import IslandHttpClient, { APIEndpoint } from '../../IslandHttpClient';


const columns = [
  {
    Header: 'Stolen Credentials',
    columns: [
      {Header: 'Username', accessor: 'username'},
      {Header: 'Type', accessor: 'title'}
    ]
  }
];

const pageSize = 10;

const StolenCredentialsTable = () => {

  const [credentialsTableData, setCredentialsTableData] = useState(null);

  useEffect(() => {
    IslandHttpClient.get(APIEndpoint.stolenCredentials, {}, true).then(
      res => setCredentialsTableData(getCredentialsTableData(res.body))
    );
  }, [])

  if (credentialsTableData === null) {
    return <LoadingIcon />
  }

  let defaultPageSize = credentialsTableData.length > pageSize ? pageSize : credentialsTableData.length;
  let showPagination = credentialsTableData.length > pageSize;
  return (
    <div className="data-table-container">
      <ReactTable
        columns={columns}
        data={credentialsTableData}
        showPagination={showPagination}
        defaultPageSize={defaultPageSize}
      />
    </div>
  );
}

export default StolenCredentialsTable;


function getCredentialsTableData(credentials){
  let tableData = [];

  for (let credential of credentials) {
    let rowData = {};
    rowData['username'] = '[No username]';
    if (credential['identity'] !== null) {
      rowData['username'] = credential['identity']['username'];
    }
    rowData['title'] = reformatSecret(credential['secret'])['title'];
    if (! _.find(tableData, rowData)) {
      tableData.push(rowData);
    }
  }

  return tableData;
}
