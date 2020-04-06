import React from 'react';
import ReactTable from 'react-table';
import {renderMachineFromSystemData, renderMachine, ScanStatus} from './Helpers'
import MitigationsComponent from './MitigationsComponent';


class T1018 extends React.Component {

  constructor(props) {
    super(props);
  }

  static renderMachines(machines) {
    let output = [];
    machines.forEach(function (machine) {
      output.push(renderMachine(machine))
    });
    return (<div>{output}</div>);
  }

  static getScanInfoColumns() {
    return ([{
      columns: [
        {
          Header: 'Machine',
          id: 'machine',
          accessor: x => renderMachineFromSystemData(x.monkey),
          style: {'whiteSpace': 'unset'}
        },
        {Header: 'First scan', id: 'started', accessor: x => x.started, style: {'whiteSpace': 'unset'}},
        {Header: 'Last scan', id: 'finished', accessor: x => x.finished, style: {'whiteSpace': 'unset'}},
        {
          Header: 'Systems found',
          id: 'systems',
          accessor: x => T1018.renderMachines(x.machines),
          style: {'whiteSpace': 'unset'}
        }
      ]
    }])
  }

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <br/>
        {this.props.data.status === ScanStatus.USED ?
          <ReactTable
            columns={T1018.getScanInfoColumns()}
            data={this.props.data.scan_info}
            showPagination={false}
            defaultPageSize={this.props.data.scan_info.length}
          /> : ''}
        <MitigationsComponent mitigations={this.props.data.mitigations}/>
      </div>
    );
  }
}

export default T1018;
