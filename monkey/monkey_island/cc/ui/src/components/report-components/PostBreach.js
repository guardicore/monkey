import React from 'react';
import ReactTable from 'react-table'

let renderArray = function(val) {
  return <div>{val.map(x => <div>{x}</div>)}</div>;
};

let renderIpAddresses = function (val) {
  return <div>{renderArray(val.ip_addresses)} {(val.domain_name ? " (".concat(val.domain_name, ")") : "")} </div>;
};

let renderPostBreach = function (machine, pbaList) {
  if (pbaList.length === 0){
    return
  } else {
      return <div>Machine: {machine.label}<br/>
             {pbaList.map(x => <div>Name: {x.name}<br/>
                                    Command: {x.command}<br/>
                                    Output: {x.output}<br/></div>)}
                                    </div>;
  }
};

let renderMachine = function (val) {
  if (val.pba_results.length === 0){
    return
  }
  return <div>{val.label} {renderIpAddresses(val)}</div>
};

const columns = [
  {
    Header: 'Post breach actions',
    columns: [
      {id: 'post_breach_actions', accessor: x => renderPostBreach(x, x.pba_results)}
    ]
  }
];

const pageSize = 10;

class PostBreachComponent extends React.Component {
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

export default PostBreachComponent;
