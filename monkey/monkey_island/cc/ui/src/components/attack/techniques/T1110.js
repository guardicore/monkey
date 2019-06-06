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
          style: { 'whiteSpace': 'unset' }, width: 160},
        {Header: 'Service', id: 'service', accessor: x => x.info.display_name, style: { 'whiteSpace': 'unset' }, width: 100},
        {Header: 'Started', id: 'started', accessor: x => x.info.started, style: { 'whiteSpace': 'unset' }},
        {Header: 'Finished', id: 'finished', accessor: x => x.info.finished, style: { 'whiteSpace': 'unset' }},
        {Header: 'Attempts', id: 'attempts', accessor: x => x.attempt_cnt, style: { 'whiteSpace': 'unset' }, width: 160},
        {Header: 'Successful credentials', id: 'credentials', accessor: x => this.renderCreds(x.successful_creds), style: { 'whiteSpace': 'unset' }},
        ]
    }])};

  static renderCreds(creds) {
    return <span>{creds.map(cred => <div>{cred}</div>)}</span>
  };

  static renderMachine(val){
    return (
      <span>{val.ip_addr} {(val.domain_name ? " (".concat(val.domain_name, ")") : "")}</span>
    )
  };

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <br/>
        {(this.props.data.status === 'SCANNED' || this.props.data.status === 'USED') ?
          <ReactTable
            columns={T1110.getServiceColumns()}
            data={this.props.data.services}
            showPagination={false}
            defaultPageSize={this.props.data.services.length}
          /> : ""}
      </div>
    );
  }
}

export default T1110;
