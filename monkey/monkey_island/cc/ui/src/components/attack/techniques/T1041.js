import React from 'react';
import '../../../styles/Collapse.scss'
import ReactTable from "react-table";
import {scanStatus} from "./Helpers";

class T1041 extends React.Component {

  constructor(props) {
    super(props);
  }

  static getC2Columns() {
    return ([{
      Header: "Data exfiltration channels",
      columns: [
        {Header: 'Source', id: 'src', accessor: x => x.src, style: { 'whiteSpace': 'unset' }},
        {Header: 'Destination', id: 'dst', accessor: x => x.dst, style: { 'whiteSpace': 'unset' }}
        ]}])};

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <br/>
        {this.props.data.status === scanStatus.USED ?
          <ReactTable
              columns={T1041.getC2Columns()}
              data={this.props.data.c2_info}
              showPagination={false}
              defaultPageSize={this.props.data.c2_info.length}
          /> : ""}
      </div>
    );
  }
}

export default T1041;
