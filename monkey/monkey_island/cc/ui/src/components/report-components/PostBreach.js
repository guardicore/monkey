import React from 'react';
import ReactTable from 'react-table'

let renderArray = function(val) {
  return <span>{val.map(x => <span key={x}> {x}</span>)}</span>;
};

let renderIpAddresses = function (val) {
  return <span> {renderArray(val.ip_addresses)} {(val.domain_name ? " (".concat(val.domain_name, ")") : "")} </span>;
};

let renderMachine = function (data) {
  return <div>{data.label} ( {renderIpAddresses(data)} )</div>
};

let renderPbaResults = function (results) {
  let pbaClass = "";
  if (results[1]){
    pbaClass="pba-success"
  } else {
    pbaClass="pba-danger"
  }
  return <div className={pbaClass}> {results[0]} </div>
};

const subColumns = [
  {id: 'pba_name', Header: "Name", accessor: x => x.name, style: { 'whiteSpace': 'unset' }},
  {id: 'pba_output', Header: "Output", accessor: x => renderPbaResults(x.result), style: { 'whiteSpace': 'unset' }}
];

let renderDetails = function (data) {
  let defaultPageSize = data.length > pageSize ? pageSize : data.length;
  let showPagination = data.length > pageSize;
  return <ReactTable
                  data={data}
                  columns={subColumns}
                  defaultPageSize={defaultPageSize}
                  showPagination={showPagination}
                  style={{"backgroundColor": "#ededed"}}
                />
};

const columns = [
  {
    Header: 'Post breach actions',
    columns: [
      {id: 'pba_machine', Header:'Machine', accessor: x => renderMachine(x)}
    ]
  }
];

const pageSize = 10;

class PostBreachComponent extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    let pbaMachines = this.props.data.filter(function(value, index, arr){
        return ( value.pba_results !== "None" && value.pba_results.length > 0);
    });
    let defaultPageSize = pbaMachines.length > pageSize ? pageSize : pbaMachines.length;
    let showPagination = pbaMachines > pageSize;
    return (
      <div className="data-table-container">
        <ReactTable
          columns={columns}
          data={pbaMachines}
          showPagination={showPagination}
          defaultPageSize={defaultPageSize}
          SubComponent={row => {
            return renderDetails(row.original.pba_results);
          }}
        />
      </div>

    );
  }
}

export default PostBreachComponent;
