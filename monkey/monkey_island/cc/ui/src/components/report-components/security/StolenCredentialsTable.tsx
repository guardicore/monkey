import React, {useEffect, useState} from 'react';
import LoadingIcon from '../../ui-components/LoadingIcon';
import {reformatSecret} from '../credentialParsing';
import _ from 'lodash';
import IslandHttpClient, {APIEndpoint} from '../../IslandHttpClient';
import XDataGrid, {X_DATA_GRID_CLASSES, XDataGridTitle} from '../../ui-components/XDataGrid';
import {nanoid} from 'nanoid';

const customToolbar = () => {
  return <XDataGridTitle title={'Stolen Credentials'} showDataActionsToolbar={false}/>;
}

const columns = [
  {headerName: 'Username', field: 'username', sortable: false},
  {headerName: 'Type', field: 'title', sortable: false}
];

const StolenCredentialsTable = () => {

  const [credentialsTableData, setCredentialsTableData] = useState(null);

  useEffect(() => {
    IslandHttpClient.getJSON(APIEndpoint.stolenCredentials, {}, true).then(
      res => {
        setCredentialsTableData(getCredentialsTableData(res.body));
      });
  }, [])

  if (credentialsTableData === null) {
    return <LoadingIcon/>
  }

  return (
    <XDataGrid
      toolbar={customToolbar}
      showToolbar={true}
      columns={columns}
      rows={credentialsTableData}
      maxHeight={'250px'}
      columnWidth={{min: 150, max: -1}}
      getRowClassName={() => X_DATA_GRID_CLASSES.HIDDEN_LAST_EMPTY_CELL}
    />
  );
};

export default StolenCredentialsTable;


const getCredentialsTableData = (credentials) => {
  let tableData = [];

  for (let credential of credentials) {
    let rowData = {};
    rowData['username'] = '[No username]';
    let identity = credential['identity'];
    if (identity !== null) {
      if ('username' in identity) {
        rowData['username'] = identity['username'];
      }
    }
    rowData['title'] = reformatSecret(credential['secret'])['title'];
    rowData['id'] = nanoid();
    if (!_.find(tableData, rowData)) {
      tableData.push(rowData);
    }
  }

  return tableData;
};
