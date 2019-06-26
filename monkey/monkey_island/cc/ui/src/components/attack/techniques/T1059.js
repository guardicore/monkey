import React from 'react';
import '../../../styles/Collapse.scss'
import ReactTable from "react-table";
import { renderMachine } from "./Helpers"


class T1059 extends React.Component {

  constructor(props) {
    super(props);
  }

  static getCommandColumns() {
    return ([{
      Header: 'Example commands used',
      columns: [
        {Header: 'Machine', id: 'machine', accessor: x => renderMachine(x.data.machine), style: { 'whiteSpace': 'unset'}, width: 160 },
        {Header: 'Approx. Time', id: 'time', accessor: x => x.data.info.finished, style: { 'whiteSpace': 'unset' }},
        {Header: 'Command', id: 'command', accessor: x => x.data.info.executed_cmds.cmd, style: { 'whiteSpace': 'unset' }},
        ]
    }])};

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <br/>
        {this.props.data.status === 'USED' ?
          <ReactTable
              columns={T1059.getCommandColumns()}
              data={this.props.data.cmds}
              showPagination={false}
              defaultPageSize={this.props.data.cmds.length}
          /> : ""}
      </div>
    );
  }
}

export default T1059;
