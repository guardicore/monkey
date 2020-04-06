import React from 'react';
import ReactTable from 'react-table';
import {renderMachineFromSystemData, renderUsageFields, ScanStatus} from './Helpers'
import MitigationsComponent from './MitigationsComponent';


class T1016 extends React.Component {

  constructor(props) {
    super(props);
  }

  static getNetworkInfoColumns() {
    return ([{
      Header: 'Network configuration info gathered',
      columns: [
        {
          Header: 'Machine',
          id: 'machine',
          accessor: x => renderMachineFromSystemData(x.machine),
          style: {'whiteSpace': 'unset'}
        },
        {Header: 'Network info', id: 'info', accessor: x => renderUsageFields(x.info), style: {'whiteSpace': 'unset'}}
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
            columns={T1016.getNetworkInfoColumns()}
            data={this.props.data.network_info}
            showPagination={false}
            defaultPageSize={this.props.data.network_info.length}
          /> : ''}
        <MitigationsComponent mitigations={this.props.data.mitigations}/>
      </div>
    );
  }
}

export default T1016;
