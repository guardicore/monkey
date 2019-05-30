import React from 'react';
import '../../../styles/Collapse.scss'
import ReactTable from "react-table";


class T1110 extends React.Component {

  constructor(props) {
    super(props);
  }

  static getServiceColumns() {
    return ([{
      columns: [
        {Header: 'Machine', id: 'machine', accessor: x => this.renderMachine(x.machine),
          style: { 'whiteSpace': 'unset' }, width: 200},
        {Header: 'Service', id: 'service', accessor: x => x.info.display_name, style: { 'whiteSpace': 'unset' }, width: 170},
        {Header: 'Started', id: 'started', accessor: x => x.info.started, style: { 'whiteSpace': 'unset' }},
        {Header: 'Finished', id: 'finished', accessor: x => x.info.finished, style: { 'whiteSpace': 'unset' }},
        {Header: 'Attempts', id: 'attempts', accessor: x => x.attempts.length, style: { 'whiteSpace': 'unset' }},
        {Header: 'Successful credentials', id: 'credentials', accessor: x => this.renderCredentials(x.attempts), style: { 'whiteSpace': 'unset' }},
        ]
    }])};

  static renderMachine(val){
    return (
      <span>{val.ip_addr} {(val.domain_name ? " (".concat(val.domain_name, ")") : "")}</span>
    )
  };

  static renderCredentials(creds){
    let content = '';
    creds.forEach((cred) => {
      if (cred.result){
        if (cred.ntlm_hash){
          content += <span>{cred.user} ; NTLM hash: {cred.ntlm_hash}</span>
        } else if (cred.ssh_key){
          content += <span>{cred.user} ; SSH key: {cred.ssh_key}</span>
        } else if (cred.lm_hash){
          content += <span>{cred.user} ; LM hash: {cred.lm_hash}</span>
        } else if (cred.password){
          content += <span>{cred.user} : {cred.password}</span>
        }
        content += <span>{cred.user} : {cred.password}</span>
      }
    })
  }

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <ReactTable
            columns={T1110.getServiceColumns()}
            data={this.props.data.services}
            showPagination={false}
            defaultPageSize={this.props.data.services.length}
        />
      </div>
    );
  }
}

export default T1110;
