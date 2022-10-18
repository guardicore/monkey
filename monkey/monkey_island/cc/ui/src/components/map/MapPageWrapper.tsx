import React, {useEffect, useState} from 'react';
import IslandHttpClient, {APIEndpoint} from '../IslandHttpClient';
import {arrayToObject, getCollectionObject} from '../utils/ServerUtils';
import MapPage from '../pages/MapPage';

const MapPageWrapper = (props) => {
  function getPropagationEvents(){
    let url_args = {'type': 'PropagationEvent', 'success': true};
    return IslandHttpClient.get(APIEndpoint.agentEvents, url_args)
      .then(res => arrayToObject(res.body, "target"));
  }

  const [mapNodes, setMapNodes] = useState([]);
  const [nodes, setNodes] = useState({});
  const [machines, setMachines] = useState({});
  const [propagationEvents, setPropagationEvents] = useState({});

  useEffect(() => {
    getCollectionObject(APIEndpoint.nodes, "machine_id").then(nodeObj => setNodes(nodeObj));
    getCollectionObject(APIEndpoint.machines, "id").then(machineObj => setMachines(machineObj));
    getPropagationEvents().then(events => setPropagationEvents(events));
  }, [])
  console.log(nodes)
  console.log(machines)
  console.log(propagationEvents)
  return (<MapPage {...props}></MapPage>);
}


export default MapPageWrapper
