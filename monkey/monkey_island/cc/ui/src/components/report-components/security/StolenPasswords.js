import React from 'react';
import ReactTable from 'react-table'

const columns = [
  {
    Header: 'Stolen Credentials',
    columns: [
      {Header: 'Username', accessor: 'username'},
      {Header: 'Type', accessor: 'type'},
      {Header: 'Stolen From', accessor: 'origin'}
    ]
  }
];

const pageSize = 10;

class StolenPasswordsComponent extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    let defaultPageSize = this.props.data.length > pageSize ? pageSize : this.props.data.length;
    let showPagination = this.props.data.length > pageSize;
    return (
      <div className="data-table-container">
        <ReactTable
          columns={columns}
          data={this.props.data}
          showPagination={showPagination}
          defaultPageSize={defaultPageSize}
        />
      </div>
    );
  }
}

export default StolenPasswordsComponent;
