import React from 'react';
import ReactTable  from 'react-table'
import {getCredentialsTableData} from '../credentialParsing.js';

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

class StolenCredentialsTable extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    let defaultPageSize = this.props.data.length > pageSize ? pageSize : this.props.data.length;
    let showPagination = this.props.data.length > pageSize;
    let table_data = this.props.data;
    if(this.props.format) {
      // Note: This formatting is needed because StolenPasswords
      // is used in Security and Attack report with different data
      table_data = getCredentialsTableData(this.props.data);
    }

    return (
      <div className="data-table-container">
        <ReactTable
          columns={columns}
          data={table_data}
          showPagination={showPagination}
          defaultPageSize={defaultPageSize}
        />
      </div>
    );
  }
}

export default StolenCredentialsTable;
