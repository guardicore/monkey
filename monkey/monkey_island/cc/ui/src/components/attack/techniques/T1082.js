import React from 'react';
import '../../../styles/Collapse.scss'
import ReactTable from "react-table";


class T1082 extends React.Component {

  constructor(props) {
    super(props);
  }

  static renderMachineString(data){
    let machineStr = data['hostname'] + " ( ";
    data['ips'].forEach(function(ipInfo){
      machineStr += ipInfo['addr'] + " ";
    });
    return machineStr + ")"
  }

  static renderCollections(collections){
    let output = [];
    collections.forEach(function(collection){
      if(collection['used']){
        output.push(<div key={collection['name']}>{collection['name']}</div>)
      }
    });
    return (<div>{output}</div>);
  }

  static getSystemInfoColumns() {
    return ([{
      columns: [
        {Header: 'Machine', id: 'machine', accessor: x => T1082.renderMachineString(x.machine), style: { 'whiteSpace': 'unset' }},
        {Header: 'Gathered info', id: 'info', accessor: x => T1082.renderCollections(x.collections), style: { 'whiteSpace': 'unset' }},
        ]
    }])};

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <br/>
        {this.props.data.status === 'USED' ?
          <ReactTable
              columns={T1082.getSystemInfoColumns()}
              data={this.props.data.system_info}
              showPagination={false}
              defaultPageSize={this.props.data.system_info.length}
          /> : ""}
      </div>
    );
  }
}

export default T1082;
