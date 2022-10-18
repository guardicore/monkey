import React, {useEffect, useState} from 'react';
import IslandHttpClient, {APIEndpoint} from '../IslandHttpClient';
import {arrayToObject, getCollectionObject} from '../utils/ServerUtils';
import MapPage from '../pages/MapPage';
import MapNode, {Agent, Machine, Node} from '../types/MapNode';
import _ from 'lodash';

const MapPageWrapper = (props) => {
  function getPropagationEvents() {
    let url_args = {'type': 'PropagationEvent', 'success': true};
    return IslandHttpClient.get(APIEndpoint.agentEvents, url_args)
      .then(res => arrayToObject(res.body, 'target'));
  }

  const [mapNodes, setMapNodes] = useState([]);
  const [nodes, setNodes] = useState<Record<string, Node>>({});
  const [machines, setMachines] = useState<Record<string, Machine>>({});
  const [agents, setAgents] = useState<Record<string, Agent>>({});
  const [propagationEvents, setPropagationEvents] = useState({});

  useEffect(() => {
    getCollectionObject(APIEndpoint.nodes, 'machine_id').then(nodeObj => setNodes(nodeObj));
    getCollectionObject(APIEndpoint.machines, 'id').then(machineObj => setMachines(machineObj));
    getCollectionObject(APIEndpoint.agents, 'id').then(agentObj => setAgents(agentObj));
    getPropagationEvents().then(events => setPropagationEvents(events));
  }, []);

  function isAllDataFetched(): boolean{
    return !_.isEmpty(nodes) && !_.isEmpty(machines) &&
      !_.isEmpty(propagationEvents) && !_.isEmpty(agents);
  }

  useEffect(() => {
    if (isAllDataFetched()) {
      setMapNodes(buildMapNodes());
    }
  }, [nodes, machines, propagationEvents])

  function buildMapNodes() {
    // Build the MapNodes list
    let mapNodes = [];
    for (const node of Object.values(nodes)) {
      let machine = machines[node.machine_id];

      let running = false;
      let agentID = null;
      let parentID = null;
      if (node.machine_id in agents) {
        let agent = agents[node.machine_id];
        running = (agent.stop_time > agent.start_time);
        agentID = agent.id;
        parentID = agent.parent_id;
      }

      let propagatedTo = wasMachinePropagated(machine, propagationEvents);

      mapNodes.push(new MapNode(
        machine.id,
        machine.network_interfaces,
        running,
        node.connections,
        machine.operating_system,
        machine.hostname,
        machine.island,
        propagatedTo,
        agentID,
        parentID
      ));
    }

    return mapNodes;
  }

  function wasMachinePropagated(machine, propagationEvents): boolean {
    let ip = getMachineIp(machine);
    return ip in propagationEvents
  }

  console.log(nodes)
  console.log(machines)
  console.log(agents)
  console.log(propagationEvents)
  return (<MapPage mapNodes={mapNodes} {...props}/>);
}


export default MapPageWrapper
