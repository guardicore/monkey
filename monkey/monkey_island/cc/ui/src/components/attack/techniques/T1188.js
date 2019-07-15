import React from 'react';
import '../../../styles/Collapse.scss'
import ReactTable from "react-table";
import { renderMachineFromSystemData, scanStatus } from "./Helpers"


class T1188 extends React.Component {

  constructor(props) {
    super(props);
  }

  static getHopColumns() {
    return ([{
      Header: "Communications trough multi-hop proxies",
      columns: [
        {Header: 'From',
          id: 'from',
          accessor: x => renderMachineFromSystemData(x.from),
          style: { 'whiteSpace': 'unset' }},
        {Header: 'To',
          id: 'to',
          accessor: x => renderMachineFromSystemData(x.to),
          style: { 'whiteSpace': 'unset' }},
        {Header: 'Hops',
          id: 'hops',
          accessor: x => x.count,
          style: { 'whiteSpace': 'unset' }},
        ]
    }])};

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <br/>
        {this.props.data.status === scanStatus.USED ?
          <ReactTable
              columns={T1188.getHopColumns()}
              data={this.props.data.hops}
              showPagination={false}
              defaultPageSize={this.props.data.hops.length}
          /> : ""}
      </div>
    );
  }
}

export default T1188;
