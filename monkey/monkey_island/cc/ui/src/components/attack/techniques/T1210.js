import React from 'react';
import ReactTable from 'react-table';
import {renderMachine} from './Helpers'
import MitigationsComponent from './MitigationsComponent';


class T1210 extends React.Component {

  constructor(props) {
    super(props);
  }

  static getScanColumns() {
    return ([{
      Header: 'Found services',
      columns: [
        {
          Header: 'Machine', id: 'machine', accessor: x => renderMachine(x.machine),
          style: {'whiteSpace': 'unset'}, width: 200
        },
        {Header: 'Time', id: 'time', accessor: x => x.time, style: {'whiteSpace': 'unset'}},
        {Header: 'Port', id: 'port', accessor: x => x.service.port, style: {'whiteSpace': 'unset'}, width: 100},
        {Header: 'Service', id: 'service', accessor: x => x.service.display_name, style: {'whiteSpace': 'unset'}}
      ]
    }])
  }

  static getExploitColumns() {
    return ([{
      Header: 'Exploited services',
      columns: [
        {
          Header: 'Machine', id: 'machine', accessor: x => renderMachine(x.machine),
          style: {'whiteSpace': 'unset'}, width: 200
        },
        {Header: 'Time', id: 'time', accessor: x => x.time, style: {'whiteSpace': 'unset'}},
        {
          Header: 'Port/url', id: 'port', accessor: x => this.renderEndpoint(x.service), style: {'whiteSpace': 'unset'},
          width: 170
        },
        {Header: 'Service', id: 'service', accessor: x => x.service.display_name, style: {'whiteSpace': 'unset'}}
      ]
    }])
  }

  static renderEndpoint(val) {
    return (
      <span>{(val.vulnerable_urls.length !== 0 ? val.vulnerable_urls[0] : val.vulnerable_ports[0])}</span>
    )
  }

  static formatScanned(data) {
    let result = [];
    for (let service in data.machine.services) {
      let scanned_service = {
        'machine': data.machine,
        'time': data.time,
        'service': {
          'port': [data.machine.services[service].port],
          'display_name': data.machine.services[service].display_name
        }
      };
      result.push(scanned_service)
    }
    return result
  }

  renderScannedServices(data) {
    return (
      <div>
        <br/>
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
        <MitigationsComponent mitigations={this.props.data.mitigations}/>
      </div>
    );
  }
}

export default T1210;
