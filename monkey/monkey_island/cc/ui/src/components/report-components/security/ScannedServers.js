import React from 'react';
import ReactTable from 'react-table';
import Pluralize from 'pluralize';
import {renderArray, renderIpAddresses} from '../common/RenderArrays';


const columns = [
  {
    Header: 'Scanned Servers',
    columns: [
      {Header: 'Machine', accessor: 'label'},
      {
        Header: 'IP Addresses', id: 'ip_addresses',
        accessor: x => renderIpAddresses(x)
      },
      {Header: 'Accessible From', id: 'accessible_from_nodes', accessor: x => renderArray(x.accessible_from_nodes)},
      {Header: 'Services', id: 'services', accessor: x => renderArray(x.services)}
    ]
  }
];

const pageSize = 10;

class ScannedServersComponent extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {

    let defaultPageSize = this.props.data.length > pageSize ? pageSize : this.props.data.length;
    let showPagination = this.props.data.length > pageSize;

    const scannedMachinesCount = this.props.data.length;
    const reducerFromScannedServerToServicesAmount = (accumulated, scannedServer) => accumulated + scannedServer['services'].length;
    const scannedServicesAmount = this.props.data.reduce(reducerFromScannedServerToServicesAmount, 0);

    return (
      <>
        <p>
          The Monkey discovered&nbsp;
          <span className="badge badge-danger">{scannedServicesAmount}</span> open&nbsp;
          {Pluralize('service', scannedServicesAmount)} on&nbsp;
          <span className="badge badge-warning">{scannedMachinesCount}</span>&nbsp;
          {Pluralize('machine', scannedMachinesCount)}:
        </p>
        <div className="data-table-container">
          <ReactTable
            columns={columns}
            data={this.props.data}
            showPagination={showPagination}
            defaultPageSize={defaultPageSize}
          />
        </div>
      </>
    );
  }
}

export default ScannedServersComponent;
