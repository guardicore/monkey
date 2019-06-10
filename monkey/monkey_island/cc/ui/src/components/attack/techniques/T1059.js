import React from 'react';
import '../../../styles/Collapse.scss'
import ReactTable from "react-table";
import { RenderMachine } from "./Helpers"


class T1059 extends React.Component {

  constructor(props) {
    super(props);
  }

  static getHashColumns() {
    return ([{
      columns: [
        {Header: 'Machine', id: 'machine', accessor: x => RenderMachine(x.machine), style: { 'whiteSpace': 'unset' }},
        {Header: 'Command', id: 'command', accessor: x => x.attempts[0].hashType, style: { 'whiteSpace': 'unset' }},
        ]
    }])};

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <br/>
        {this.props.data.status === 'USED' ?
          <ReactTable
              columns={T1059.getHashColumns()}
              data={this.props.data.successful_logins}
              showPagination={false}
              defaultPageSize={this.props.data.successful_logins.length}
          /> : ""}
      </div>
    );
  }
}

export default T1059;
