import React from 'react';
import '../../../styles/Collapse.scss'
import ReactTable from "react-table";


class T1210 extends React.Component {

  constructor(props) {
    super(props);
  }

  static getScanColumns() {
    return ([{
      columns: [
        {Header: 'Machine', id: 'machine', accessor: x => this.renderMachine(x.machine),
          style: { 'whiteSpace': 'unset' }, width: 200},
        {Header: 'Time', id: 'time', accessor: x => x.time, style: { 'whiteSpace': 'unset' }, width: 170},
        {Header: 'Port', id: 'port', accessor: x =>x.service.port, style: { 'whiteSpace': 'unset' }},
        {Header: 'Service', id: 'service', accessor: x => x.service.display_name, style: { 'whiteSpace': 'unset' }}
        ]
  }])}

  static getExploitColumns() {
    return ([{
      columns: [
        {Header: 'Machine', id: 'machine', accessor: x => this.renderMachine(x.machine),
          style: { 'whiteSpace': 'unset' }, width: 200},
        {Header: 'Time', id: 'time', accessor: x => x.time, style: { 'whiteSpace': 'unset' }, width: 170},
        {Header: 'Port/url', id: 'port', accessor: x =>this.renderEndpoint(x.service), style: { 'whiteSpace': 'unset' }},
        {Header: 'Service', id: 'service', accessor: x => x.service.display_name, style: { 'whiteSpace': 'unset' }}
        ]
    }])};

  static renderMachine(val){
    return (
      <span>{val.ip_addr} {(val.domain_name ? " (".concat(val.domain_name, ")") : "")}</span>
    )
  };

  static renderEndpoint(val){
    return (
      <span>{(val.vulnerable_urls.length !== 0 ? val.vulnerable_urls[0] : val.vulnerable_ports[0])}</span>
    )
  };

  static formatScanned(data){
    let result = [];
    for(let service in data.machine.services){
      let scanned_service = {'machine': data.machine,
                             'time': data.time,
                             'service': {'port': [data.machine.services[service].port],
                                         'display_name': data.machine.services[service].display_name}};
      result.push(scanned_service)
    }
    return result
  };

  renderScannedServices(data) {
    return (
      <div>
        <br/>
        <div>Found services: </div>
        <ReactTable
            columns={T1210.getScanColumns()}
            data={data}
            showPagination={false}
            defaultPageSize={data.length}
        />
      </div>)
  }

  renderExploitedServices(data) {
    return (
      <div>
        <br/>
        <div>Exploited services: </div>
        <ReactTable
            columns={T1210.getExploitColumns()}
            data={data}
            showPagination={false}
            defaultPageSize={data.length}
        />
      </div>)
  }

  render() {
    let scanned_services = this.props.data.scanned_services.map(T1210.formatScanned).flat();
    return (
      <div>
        <div>{this.props.data.message}</div>
        {scanned_services.length > 0 ?
          this.renderScannedServices(scanned_services) : ''}
        {this.props.data.exploited_services.length > 0 ?
          this.renderExploitedServices(this.props.data.exploited_services) : ''}
      </div>
    );
  }
}

export default T1210;
