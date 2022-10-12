import React, {useEffect, useState} from 'react';
import ReactTable from 'react-table';
import Pluralize from 'pluralize';
import IslandHttpClient from '../../IslandHttpClient';

const machinesEndpoint = '/api/machines';
const nodesEndpoint = '/api/netmap/node';
const scanCommunicationType = 'scanned';

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
  const [allNodes, setAllNodes] = useState([]);
  const [allMachines, setAllMachines] = useState([]);

  useEffect(() => {
    IslandHttpClient.get(nodesEndpoint)
      .then(res => setAllNodes(res.body))
    IslandHttpClient.get(machinesEndpoint)
      .then(res => setAllMachines(res.body))
  }, [])

  function getScannedMachineIds(nodes) {
    let machineIds = new Set();
    for (let i = 0; i < nodes.length; i++) {
      for (const [machineId, communications] of Object.entries(nodes[i].connections)) {
        if (communications.includes(scanCommunicationType)) {
          machineIds.add(parseInt(machineId));
        }
      }
    }
    return machineIds;
  }

  useEffect(() => {
    if (allNodes !== [] && allMachines !== []) {
      let scannedMachines = [];
      let scannedIds = getScannedMachineIds(allNodes);
      for (const scannedId of scannedIds) {
        let scannedMachine = allMachines.filter(machine => machine.id === scannedId)[0];
        if (scannedMachine) {
          scannedMachines.push(scannedMachine);
        }
      }
      setScannedMachines(scannedMachines);
    }
  }, [allNodes, allMachines])

  let defaultPageSize = props.data.length > pageSize ? pageSize : props.data.length;
  let showPagination = props.data.length > pageSize;

  const scannedMachinesCount = props.data.length;
  const reducerFromScannedServerToServicesAmount = (accumulated, scannedServer) => accumulated + scannedServer['services'].length;
  const scannedServicesAmount = props.data.reduce(reducerFromScannedServerToServicesAmount, 0);

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
          data={scannedMachines}
          showPagination={showPagination}
          defaultPageSize={defaultPageSize}
        />
      </div>
    </>
  );
}

export default ScannedServersComponent;
