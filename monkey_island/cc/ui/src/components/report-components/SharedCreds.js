import React from 'react';
import ReactTable from 'react-table'

let renderArray = function(val) {
  console.log(val);
  return <div>{val.map(x => <div>{x}</div>)}</div>;
};

const columns = [
  {
    Header: 'Shared Credentials',
    columns: [
      {Header: 'Credential Group', id: 'cred_group', accessor: x => renderArray(x.cred_group) }
      ]
  }
];

const pageSize = 10;

class SharedCredsComponent extends React.Component {
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

export default SharedCredsComponent;
