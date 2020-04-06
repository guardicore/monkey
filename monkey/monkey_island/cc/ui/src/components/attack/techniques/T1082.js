import React from 'react';
import ReactTable from 'react-table';
import {renderMachineFromSystemData, renderUsageFields, ScanStatus} from './Helpers'
import MitigationsComponent from './MitigationsComponent';


class T1082 extends React.Component {

  constructor(props) {
    super(props);
  }

  static getSystemInfoColumns() {
    return ([{
      columns: [
        {
          Header: 'Machine',
          id: 'machine',
          accessor: x => renderMachineFromSystemData(x.machine),
          style: {'whiteSpace': 'unset'}
        },
        {
          Header: 'Gathered info',
          id: 'info',
          accessor: x => renderUsageFields(x.collections),
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
            columns={T1082.getSystemInfoColumns()}
            data={this.props.data.system_info}
            showPagination={false}
            defaultPageSize={this.props.data.system_info.length}
          /> : ''}
        <MitigationsComponent mitigations={this.props.data.mitigations}/>
      </div>
    );
  }
}

export default T1082;
