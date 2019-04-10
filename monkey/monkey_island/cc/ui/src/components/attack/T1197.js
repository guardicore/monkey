import React from 'react';
import '../../styles/Collapse.scss'
import ReactTable from "react-table";

let renderMachine = function (val) {
  return (
    <span>{val.ip_addr} {(val.domain_name ? " (".concat(val.domain_name, ")") : "")}</span>
  )
};

const columns = [
  {
    columns: [
      {Header: 'Machine', id: 'machine', accessor: x => renderMachine(x), style: { 'whiteSpace': 'unset' }, width: 200},
      {Header: 'Time', id: 'time', accessor: x => x.time, style: { 'whiteSpace': 'unset' }, width: 170},
      {Header: 'Usage', id: 'usage', accessor: x => x.usage, style: { 'whiteSpace': 'unset' }}
      ]
  }
];

class T1210 extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="data-table-container">
        <div>
          <div>{this.props.data.message}</div>
          {this.props.data.bits_jobs.length > 0 ? <div>BITS jobs were used in these machines: </div> : ''}
        </div>
        <br/>
        <ReactTable
          columns={columns}
          data={this.props.data.bits_jobs}
          showPagination={false}
          defaultPageSize={this.props.data.bits_jobs.length}
        />
      </div>
    );
  }
}

export default T1210;
