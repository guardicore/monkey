import React from 'react';
import ReactTable from 'react-table'

let renderArray = function(val) {
  return <div>{val.map(x => <div>{x}</div>)}</div>;
};

let renderIpAddresses = function (val) {
  return <div>{renderArray(val.ip_addresses)} {(val.domain_name ? " (".concat(val.domain_name, ")") : "")} </div>;
};

let renderPostBreach = function (val) {
  return <div>{val.map(x => <div>Name: {x.name}<br/>Command: {x.command}<br/>Output: {x.output}<br/></div>)}</div>;
};

const columns = [
  {
    Header: 'Breached Servers',
    columns: [
      {Header: 'Machine', accessor: 'label'},
      {Header: 'IP Addresses', id: 'ip_addresses',
       accessor: x => renderIpAddresses(x)},
      {Header: 'Exploits', id: 'exploits', accessor: x => renderArray(x.exploits)},
      {Header: 'Post breach actions:', id: 'post_breach_actions', accessor: x => renderPostBreach(x.post_breach_actions)}

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
