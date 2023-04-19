import React, {useEffect, useState} from 'react';
import ReactTable from 'react-table';
import Pluralize from 'pluralize';
import {APIEndpoint} from '../../IslandHttpClient';
import _ from 'lodash';
import {CommunicationType} from '../../types/MapNode';
import {getCollectionObject} from '../../utils/ServerUtils';


function getMachineRepresentationString(machine) {
  return `${machine.hostname}(${machine.network_interfaces.toString()})`;
}


function getMachineServices(machine) {
  let services = [];
  for (const [socketAddress, serviceName] of Object.entries(machine.network_services)) {
    services.push(<div key={socketAddress}>{socketAddress} - {serviceName}</div>);
  }
  return services
}

const columns = [
  {
    Header: 'Scanned Servers',
    columns: [
      {Header: 'Machine', id: 'machine', accessor: getMachineRepresentationString},
      {Header: 'Services found', id: 'services', accessor: getMachineServices}
    ]
  }
];

const pageSize = 10;

function ScannedServersComponent(props) {

  const [scannedMachines, setScannedMachines] = useState([]);
  const [allNodes, setAllNodes] = useState({});
  const [allMachines, setAllMachines] = useState({});

  useEffect(() => {
    getCollectionObject(APIEndpoint.nodes, 'machine_id', true)
      .then(nodesObj => setAllNodes(nodesObj));
    getCollectionObject(APIEndpoint.machines, 'id', true)
      .then(machinesObj => setAllMachines(machinesObj));
  }, [])

  function getScannedMachines() {
    let scannedMachines = new Set();
    for (const node of Object.values(allNodes)) {
      for (const [targetMachineId, communications] of Object.entries(node.connections)) {
        if (communications.includes(CommunicationType.scanned)) {
          scannedMachines.add(allMachines[targetMachineId]);
        }
      }
    }
    return Array.from(scannedMachines);
  }

  useEffect(() => {
    if (_.isEmpty(allNodes) || _.isEmpty(allMachines)) {
      return;
    }
    setScannedMachines(getScannedMachines());
  }, [allNodes, allMachines])

  let defaultPageSize = props.data.length > pageSize ? pageSize : props.data.length;
  let showPagination = props.data.length > pageSize;

  const scannedMachinesCount = props.data.length;
  const reducerFromScannedServerToServicesAmount = (accumulated, scannedServer) => accumulated + scannedServer['services'].length;
  const scannedServicesAmount = props.data.reduce(reducerFromScannedServerToServicesAmount, 0);

  return (
    <>
      <p>
        Infection Monkey discovered&nbsp;
        <span className="badge badge-danger">{scannedServicesAmount}</span> open&nbsp;
        {Pluralize('service', scannedServicesAmount)} on&nbsp;
        <span className="badge badge-warning">{scannedMachinesCount}</span>&nbsp;
        {Pluralize('machine', scannedMachinesCount)}:
      </p>
      <div className="data-table-container">
        <ReactTable
          columns={columns}
          data={scannedMachines}
          showPagination={showPagination}
          defaultPageSize={defaultPageSize}
        />
      </div>
    </>
  );
}

export default ScannedServersComponent;
