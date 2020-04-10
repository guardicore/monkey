import React from 'react';
import ReactTable from 'react-table';
import {ScanStatus} from './Helpers';
import MitigationsComponent from './MitigationsComponent';

class T1041 extends React.Component {

  constructor(props) {
    super(props);
  }

  static getC2Columns() {
    return ([{
      Header: 'Data exfiltration channels',
      columns: [
        {Header: 'Source', id: 'src', accessor: x => x.src, style: {'whiteSpace': 'unset'}},
        {Header: 'Destination', id: 'dst', accessor: x => x.dst, style: {'whiteSpace': 'unset'}}
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
            columns={T1041.getC2Columns()}
            data={this.props.data.command_control_channel}
            showPagination={false}
            defaultPageSize={this.props.data.command_control_channel.length}
          /> : ''}
        <MitigationsComponent mitigations={this.props.data.mitigations}/>
      </div>
    );
  }
}

export default T1041;
