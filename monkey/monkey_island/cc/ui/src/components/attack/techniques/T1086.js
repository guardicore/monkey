import React from 'react';
import '../../../styles/Collapse.scss'
import ReactTable from "react-table";
import { renderMachine } from "./Helpers"


class T1086 extends React.Component {

  constructor(props) {
    super(props);
  }

  static getPowershellColumns() {
    return ([{
      Header: 'Example Powershell commands used',
      columns: [
        {Header: 'Machine', id: 'machine', accessor: x => renderMachine(x.data[0].machine), style: { 'whiteSpace': 'unset'}, width: 160 },
        {Header: 'Approx. Time', id: 'time', accessor: x => x.data[0].info.finished, style: { 'whiteSpace': 'unset' }},
        {Header: 'Command', id: 'command', accessor: x => x.data[0].info.executed_cmds[0].cmd, style: { 'whiteSpace': 'unset' }},
        ]
    }])};

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <br/>
        {this.props.data.status === 'USED' ?
          <ReactTable
              columns={T1086.getPowershellColumns()}
              data={this.props.data.cmds}
              showPagination={false}
              defaultPageSize={this.props.data.cmds.length}
          /> : ""}
      </div>
    );
  }
}

export default T1086;
