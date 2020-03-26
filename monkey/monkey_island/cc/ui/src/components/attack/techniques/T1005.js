import React from 'react';
import ReactTable from 'react-table';
import {renderMachineFromSystemData, ScanStatus} from './Helpers';
import MitigationsComponent from './MitigationsComponent';

class T1005 extends React.Component {

  constructor(props) {
    super(props);
  }

  static getDataColumns() {
    return ([{
      Header: 'Sensitive data',
      columns: [
        {
          Header: 'Machine',
          id: 'machine',
          accessor: x => renderMachineFromSystemData(x.machine),
          style: {'whiteSpace': 'unset'}
        },
        {Header: 'Type', id: 'type', accessor: x => x.gathered_data_type, style: {'whiteSpace': 'unset'}},
        {Header: 'Info', id: 'info', accessor: x => x.info, style: {'whiteSpace': 'unset'}}
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
            columns={T1005.getDataColumns()}
            data={this.props.data.collected_data}
            showPagination={false}
            defaultPageSize={this.props.data.collected_data.length}
          /> : ''}
        <MitigationsComponent mitigations={this.props.data.mitigations}/>
      </div>
    );
  }
}

export default T1005;
