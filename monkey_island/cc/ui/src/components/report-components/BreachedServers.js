import React from 'react';
import ReactTable from 'react-table'

let renderArray = function(val) {
  if (val.length === 0) {
    return '';
  }
  return val.reduce((total, new_str) => total + ', ' + new_str);
};

const columns = [
  {
    Header: 'Breached Servers',
    columns: [
      {Header: 'Machine', accessor: 'label'},
      {Header: 'IP Addresses', id: 'ip_addresses', accessor: x => renderArray(x.ip_addresses)},
      {Header: 'Exploits', id: 'exploits', accessor: x => renderArray(x.exploits)}
      ]
  }
];

const pageSize = 10;

class BreachedServersComponent extends React.Component {
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

export default BreachedServersComponent;
