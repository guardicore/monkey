import React, {useEffect, useState} from 'react';
import ReactTable from 'react-table'
import IslandHttpClient, {APIEndpoint} from '../../IslandHttpClient';
import LoadingIcon from '../../ui-components/LoadingIcon';
import {
  getAllSecrets,
  getCredentialsUsernames
} from '../credentialParsing';
import _ from 'lodash';


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
    IslandHttpClient.get(APIEndpoint.stolenCredentials)
      .then(res => res.body)
      .then(creds => setCredentialsTableData(getCredentialsTableData(creds)))
  })

  if(credentialsTableData === null){
    return (<LoadingIcon />)
  } else {

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
}

export default StolenCredentialsTable;


function getCredentialsTableData(credentials){
  let tableData = [];

  let identites = getCredentialsUsernames(credentials);
  let secrets = getAllSecrets(credentials, [])

  for (let i = 0; i < credentials.length; i++) {
    let rowData = {};
    rowData['username'] = identites[i];
    rowData['title'] = secrets[i]['title'];
    if (! _.find(tableData, rowData)){
      tableData.push(rowData);
    }
  }

  return tableData;
}
