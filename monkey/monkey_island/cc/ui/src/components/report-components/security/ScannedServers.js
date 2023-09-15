import React, {useEffect, useState} from 'react';
import Pluralize from 'pluralize';
import {APIEndpoint} from '../../IslandHttpClient';
import _ from 'lodash';
import {CommunicationType} from '../../types/MapNode';
import {getCollectionObject} from '../../utils/ServerUtils';
import XDataGrid, {X_DATA_GRID_CLASSES, XDataGridTitle} from '../../ui-components/XDataGrid';
import {nanoid} from 'nanoid';

const customToolbar = () => {
  return <XDataGridTitle title={'Scanned Servers'} showDataActionsToolbar={false}/>;
}

function getMachineRepresentationString(machine) {
  return `${machine.hostname}(${machine.network_interfaces.toString()})`;
}

function getMachineServices(machine) {
  return <div style={{display: 'flex', flexDirection: 'column', justifyContent: 'flex-start', width: '100%'}}>
    {
      Object.entries(machine?.network_services || {})?.map(([socketAddress, serviceName]) => {
        return <div key={socketAddress}>{socketAddress} - {serviceName}</div>
      })
    }
  </div>
}

const columns = [
    {headerName: 'Machine', field: 'machine', sortable: false},
    {headerName: 'Services found', field: 'services', renderCell: ({value})=>{return value;}, sortable: false}
];

const prepareData = (scannedMachines) => {
  return scannedMachines.map((scannedMachine)=>{
    return {
      id: nanoid(),
      machine: getMachineRepresentationString(scannedMachine),
      services: getMachineServices(scannedMachine)
    }
  });
}

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
    setScannedMachines(prepareData(getScannedMachines()));
  }, [allNodes, allMachines])

  const scannedMachinesCount = props.data.length;
  const reducerFromScannedServerToServicesCount = (accumulated, scannedServer) => accumulated + scannedServer.services.props.children.length;
  const scannedServicesCount = scannedMachines.reduce(reducerFromScannedServerToServicesCount, 0);

  return (
    <>
      <p>
        Infection Monkey discovered&nbsp;
        <span className="badge text-bg-danger">{scannedServicesCount}</span> open&nbsp;
        {Pluralize('service', scannedServicesCount)} on&nbsp;
        <span className="badge text-bg-warning">{scannedMachinesCount}</span>&nbsp;
        {Pluralize('machine', scannedMachinesCount)}:
      </p>
      <XDataGrid
        toolbar={customToolbar}
        showToolbar={true}
        columns={columns}
        rows={scannedMachines}
        maxHeight={'250px'}
        columnWidth={{min: 150, max: -1}}
        getRowClassName={() => X_DATA_GRID_CLASSES.HIDDEN_LAST_EMPTY_CELL}
      />
    </>
  );
}

export default ScannedServersComponent;
