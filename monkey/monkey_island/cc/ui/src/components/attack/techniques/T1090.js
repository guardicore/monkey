import React from 'react';
import ReactTable from 'react-table';
import {renderMachineFromSystemData, ScanStatus} from './Helpers'
import MitigationsComponent from './MitigationsComponent';


class T1090 extends React.Component {

  constructor(props) {
    super(props);
  }

  static getProxyColumns() {
    return ([{
      columns: [
        {
          Header: 'Machines',
          id: 'machine',
          accessor: x => renderMachineFromSystemData(x),
          style: {'whiteSpace': 'unset', textAlign: 'center'}
        }]
    }])
  }

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <br/>
        {this.props.data.status === ScanStatus.USED ?
          <ReactTable
            columns={T1090.getProxyColumns()}
            data={this.props.data.proxies}
            showPagination={false}
            defaultPageSize={this.props.data.proxies.length}
          /> : ''}
        <MitigationsComponent mitigations={this.props.data.mitigations}/>
      </div>
    );
  }
}

export default T1090;
