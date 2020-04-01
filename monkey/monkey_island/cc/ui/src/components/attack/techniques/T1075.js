import React from 'react';
import ReactTable from 'react-table';
import {renderMachine, ScanStatus} from './Helpers'
import MitigationsComponent from './MitigationsComponent';


class T1075 extends React.Component {

  constructor(props) {
    super(props);
    this.props.data.successful_logins.forEach((login) => this.setLoginHashType(login))
  }

  setLoginHashType(login) {
    if (login.attempts[0].ntlm_hash !== '') {
      login.attempts[0].hashType = 'NTLM';
    } else if (login.attempts[0].lm_hash !== '') {
      login.attempts[0].hashType = 'LM';
    }
  }

  static getHashColumns() {
    return ([{
      columns: [
        {Header: 'Machine', id: 'machine', accessor: x => renderMachine(x.machine), style: {'whiteSpace': 'unset'}},
        {Header: 'Service', id: 'service', accessor: x => x.info.display_name, style: {'whiteSpace': 'unset'}},
        {Header: 'Username', id: 'username', accessor: x => x.attempts[0].user, style: {'whiteSpace': 'unset'}},
        {Header: 'Hash type', id: 'hash', accessor: x => x.attempts[0].hashType, style: {'whiteSpace': 'unset'}}
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
            columns={T1075.getHashColumns()}
            data={this.props.data.successful_logins}
            showPagination={false}
            defaultPageSize={this.props.data.successful_logins.length}
          /> : ''}
        <MitigationsComponent mitigations={this.props.data.mitigations}/>
      </div>
    );
  }
}

export default T1075;
