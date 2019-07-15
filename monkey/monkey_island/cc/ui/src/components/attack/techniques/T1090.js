import React from 'react';
import '../../../styles/Collapse.scss'
import ReactTable from "react-table";
import { renderMachineFromSystemData, scanStatus } from "./Helpers"


class T1090 extends React.Component {

  constructor(props) {
    super(props);
  }

  static getProxyColumns() {
    return ([{
      Header: "Proxies were used to communicate with:",
      columns: [
        {Header: 'Machines',
          id: 'machine',
          accessor: x => renderMachineFromSystemData(x),
          style: { 'whiteSpace': 'unset', textAlign: 'center' }}]}])
  };

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <br/>
        {this.props.data.status === scanStatus.USED ?
          <ReactTable
              columns={T1090.getProxyColumns()}
              data={this.props.data.proxies}
              showPagination={false}
              defaultPageSize={this.props.data.proxies.length}
          /> : ""}
      </div>
    );
  }
}

export default T1090;
