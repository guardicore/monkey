import React from 'react';
import ReactTable from 'react-table'
import Pluralize from "pluralize";

let renderArray = function (val) {
  return <div>{val.map(x => <div>{x}</div>)}</div>;
};

let renderIpAddresses = function (val) {
  return <div>{renderArray(val.ip_addresses)} {(val.domain_name ? ' ('.concat(val.domain_name, ')') : '')} </div>;
};

const columns = [
  {
    Header: 'Breached Servers',
    columns: [
      {Header: 'Machine', accessor: 'label'},
      {
        Header: 'IP Addresses', id: 'ip_addresses',
        accessor: x => renderIpAddresses(x)
      },
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
      <>
        <p>
          The Monkey successfully breached <span
          className="label label-danger">{this.props.data.length}</span> {Pluralize('machines', this.props.data.length)}:
        </p>
        <div className="data-table-container">
          <ReactTable
            columns={columns}
            data={this.props.data}
            showPagination={showPagination}
            defaultPageSize={defaultPageSize}
          />
        </div>
      </>
    );
  }
}

export default BreachedServersComponent;
