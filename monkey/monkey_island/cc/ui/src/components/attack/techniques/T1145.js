import React from 'react';
import ReactTable from 'react-table';
import {renderMachineFromSystemData, ScanStatus} from './Helpers'
import MitigationsComponent from './MitigationsComponent';


class T1145 extends React.Component {

  constructor(props) {
    super(props);
  }

  static renderSSHKeys(keys) {
    let output = [];
    keys.forEach(function (keyInfo) {
      output.push(<div key={keyInfo['name'] + keyInfo['home_dir']}>
        SSH key pair used by <b>{keyInfo['name']}</b> user found in {keyInfo['home_dir']}</div>)
    });
    return (<div>{output}</div>);
  }

  static getKeysInfoColumns() {
    return ([{
      columns: [
        {
          Header: 'Machine',
          id: 'machine',
          accessor: x => renderMachineFromSystemData(x.machine),
          style: {'whiteSpace': 'unset'}
        },
        {
          Header: 'Keys found',
          id: 'keys',
          accessor: x => T1145.renderSSHKeys(x.ssh_info),
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
            columns={T1145.getKeysInfoColumns()}
            data={this.props.data.ssh_info}
            showPagination={false}
            defaultPageSize={this.props.data.ssh_info.length}
          /> : ''}
        <MitigationsComponent mitigations={this.props.data.mitigations}/>
      </div>
    );
  }
}

export default T1145;
