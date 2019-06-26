import React from 'react';
import '../../../styles/Collapse.scss'
import ReactTable from "react-table";
import { renderMachine } from "./Helpers"


class T1210 extends React.Component {

  constructor(props) {
    super(props);
    this.columns = [ {Header: 'Machine',
                      id: 'machine', accessor: x => renderMachine(x),
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

  renderExploitedMachines(){
    if (this.props.data.bits_jobs.length === 0){
      return (<div />)
    } else {
      return (<ReactTable
                columns={this.columns}
                data={this.props.data.bits_jobs}
                showPagination={false}
                defaultPageSize={this.props.data.bits_jobs.length}
              />)
    }
  }

  render() {
    return (
      <div className="data-table-container">
        <div>
          <div>{this.props.data.message}</div>
          {this.props.data.bits_jobs.length > 0 ? <div>BITS jobs were used in these machines: </div> : ''}
        </div>
        <br/>
        {this.renderExploitedMachines()}
      </div>
    );
  }
}

export default T1210;
