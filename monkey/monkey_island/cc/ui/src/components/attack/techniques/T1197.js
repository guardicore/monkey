import React from 'react';
import '../../../styles/Collapse.scss'
import ReactTable from "react-table";


class T1210 extends React.Component {

  constructor(props) {
    super(props);
    this.columns = [ {Header: 'Machine',
                      id: 'machine', accessor: x => T1210.renderMachine(x),
                      style: { 'whiteSpace': 'unset' },
                      width: 200},
                    {Header: 'Time',
                      id: 'time', accessor: x => x.time,
                      style: { 'whiteSpace': 'unset' },
                      width: 170},
                    {Header: 'Usage',
                      id: 'usage', accessor: x => x.usage,
                      style: { 'whiteSpace': 'unset' }}
      ]
  }

  static renderMachine = (val) => {
    return (
      <span>{val.ip_addr} {(val.domain_name ? " (".concat(val.domain_name, ")") : "")}</span>
    )
  };

  render() {
    return (
      <div className="data-table-container">
        <div>
          <div>{this.props.data.message}</div>
          {this.props.data.bits_jobs.length > 0 ? <div>BITS jobs were used in these machines: </div> : ''}
        </div>
        <br/>
        <ReactTable
          columns={this.columns}
          data={this.props.data.bits_jobs}
          showPagination={false}
          defaultPageSize={this.props.data.bits_jobs.length}
        />
      </div>
    );
  }
}

export default T1210;
