import React from 'react';
import ReactTable from 'react-table';
import {renderMachineFromSystemData, ScanStatus} from './Helpers';
import MitigationsComponent from './MitigationsComponent';

class T1216 extends React.Component {

  constructor(props) {
    super(props);
  }

  static getColumns() {
      return ([{
        columns: [
            { Header: 'Machine',
              id: 'machine',
              accessor: x => renderMachineFromSystemData(x.machine),
              style: {'whiteSpace': 'unset'}},
            { Header: 'Result',
              id: 'result',
              accessor: x => x.result,
              style: {'whiteSpace': 'unset'}}
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
            columns={T1216.getColumns()}
            data={this.props.data.info}
            showPagination={false}
            defaultPageSize={this.props.data.info.length}
          /> : ''}
          <MitigationsComponent mitigations={this.props.data.mitigations}/>
      </div>
    );
  }
}

export default T1216;
