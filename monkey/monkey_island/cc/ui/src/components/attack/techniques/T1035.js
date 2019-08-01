import React from 'react';
import '../../../styles/Collapse.scss'
import ReactTable from "react-table";
import { renderMachineFromSystemData } from "./Helpers"


class T1035 extends React.Component {

  constructor(props) {
    super(props);
  }

  static getServiceColumns() {
    return ([{
      columns: [
        {Header: 'Machine',
          id: 'machine',
          accessor: x => renderMachineFromSystemData(x._id.machine),
          style: { 'whiteSpace': 'unset' },
          width: 300},
        {Header: 'Usage',
          id: 'usage',
          accessor: x => x._id.usage,
          style: { 'whiteSpace': 'unset' }}]
    }])};

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <br/>
        {this.props.data.services.length !== 0 ?
          <ReactTable
              columns={T1035.getServiceColumns()}
              data={this.props.data.services}
              showPagination={false}
              defaultPageSize={this.props.data.services.length}
          /> : ""}
      </div>
    );
  }
}

export default T1035;
