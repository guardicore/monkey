import React from 'react';
import ReactTable from 'react-table'

let renderArray = function(val) {
  return <div>{val.map(x => <div>{x}</div>)}</div>;
};

const columns = [
  {
    Header: 'Shared Admins Between Machines',
    columns: [
      { Header: 'Username', accessor: 'username'},
      { Header: 'Domain', accessor: 'domain'},
      { Header: 'Machines', id: 'machines', accessor: x => renderArray(x.machines)},
    ]
  }
];

const pageSize = 10;

class SharedAdminsComponent extends React.Component {
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

export default SharedAdminsComponent;
