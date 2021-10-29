import React from 'react';
import ReactTable from 'react-table';
import {renderMachine, renderMachineFromSystemData, ScanStatus} from './Helpers'
import MitigationsComponent from './MitigationsComponent';


class T1086 extends React.Component {

  constructor(props) {
    super(props);
  }

  static getPowershellColumnsForExploits() {
    return ([{
      Header: 'Exploiters',
      columns: [
        {
          Header: 'Machine',
          id: 'machine',
          accessor: x => renderMachine(x.data[0].machine),
          style: {'whiteSpace': 'unset'},
          width: 160
        },
        {Header: 'Approx. Time', id: 'time', accessor: x => x.data[0].info.finished, style: {'whiteSpace': 'unset'}},
        {
          Header: 'Command',
          id: 'command',
          accessor: x => x.data[0].info.executed_cmds[0].cmd,
          style: {'whiteSpace': 'unset'}
        }
      ]
    }])
  }

  static getPowershellColumnsForPBAs() {
    return ([{
      Header: 'Post-Breach Actions',
      columns: [
        {
          Header: 'Machine',
          id: 'machine',
          accessor: x => renderMachineFromSystemData(x.machine),
          style: {'whiteSpace': 'unset'}
        },
        {
          Header: 'Information',
          id: 'information',
          accessor: x => x.info,
          style: {'whiteSpace': 'unset'}
        }
      ]
    }])
  }

  segregatePowershellDataPerCategory() {
    let exploitCategoryName = 'exploit';
    let pbaCategoryName = 'post_breach';

    let dataFromExploits = [];
    let dataFromPBAs = [];

    for (let rowIdx in this.props.data.cmds) {
      let row = this.props.data.cmds[rowIdx];
      if (row.telem_category == exploitCategoryName) {
        dataFromExploits.push(row);
      }
      else if (row.telem_category == pbaCategoryName) {
        dataFromPBAs.push(row);
      }
    }

    return [dataFromExploits, dataFromPBAs]
  }

  render() {
    let segregatedData = this.segregatePowershellDataPerCategory();
    let dataFromExploits = segregatedData[0];
    let dataFromPBAs = segregatedData[1];

    return (
      <div>
        <div>{this.props.data.message_html}</div>
        <br/>
        {this.props.data.status === ScanStatus.USED ?
          <div>
          <ReactTable
            columns={T1086.getPowershellColumnsForExploits()}
            data={dataFromExploits}
            showPagination={false}
            defaultPageSize={dataFromExploits.length}
          />
          <br/>
          <br/>
          <ReactTable
            columns={T1086.getPowershellColumnsForPBAs()}
            data={dataFromPBAs}
            showPagination={false}
            defaultPageSize={dataFromPBAs.length}
          />
          </div> : ''}
        <MitigationsComponent mitigations={this.props.data.mitigations}/>
      </div>
    );
  }
}

export default T1086;
