import React from 'react';
import ReactTable from 'react-table'

let renderArray = function (val) {
  return <div>{val.map(x => <div>{x}</div>)}</div>;
};

let renderIpAddresses = function (val) {
  return <div>{renderArray(val.ip_addresses)} {(val.domain_name ? " (".concat(val.domain_name, ")") : "")} </div>;
};

const columns = [
  {
    Header: 'Scanned Servers',
    columns: [
      {Header: 'Machine', accessor: 'label'},
      {
        Header: 'IP Addresses', id: 'ip_addresses',
        accessor: x => renderIpAddresses(x)
      },
      {Header: 'Accessible From', id: 'accessible_from_nodes', accessor: x => renderArray(x.accessible_from_nodes)},
      {Header: 'Services', id: 'services', accessor: x => renderArray(x.services)}
    ]
  }
];

const pageSize = 10;

class ScannedServersComponent extends React.Component {
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

export default ScannedServersComponent;
