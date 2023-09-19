import React, {useEffect, useState} from 'react';
import IslandHttpClient, {APIEndpoint} from '../IslandHttpClient';
import {arrayToObject, getAllAgents, getCollectionObject} from '../utils/ServerUtils';
import MapPage from '../pages/MapPage';
import MapNode, {
  Agent,
  Communications,
  CommunicationType,
  getMachineIp,
  Machine,
  Node
} from '../types/MapNode';
import _ from 'lodash';
import generateGraph, {Graph} from './GraphCreator';

const MapPageWrapper = (props) => {

  function getPropagationEvents(refreshToken: boolean) {
    let url_args = {'type': 'PropagationEvent', 'success': true};
    return IslandHttpClient.getJSON(APIEndpoint.agentEvents, url_args, refreshToken)
      .then(res => arrayToObject(res.body, 'target'));
  }

  const [updateInProgress, setUpdateInProgress] = useState(false);
  const [mapNodes, setMapNodes] = useState<MapNode[]>([]);
  const [nodes, setNodes] = useState<Record<string, Node>>({});
  const [machines, setMachines] = useState<Record<string, Machine>>({});
  const [agents, setAgents] = useState<Agent[]>([]);
  const [propagationEvents, setPropagationEvents] = useState({});

  const [graph, setGraph] = useState<Graph>({edges: [], nodes: []});
  // We need to avoid re-drawing the map, but the original data gets modified
  // by the "react-graph-vis". This snapshot stores unmodified data for comparison
  const [graphSnapshot, setGraphSnapshot] = useState<Graph>({edges: [], nodes: []});


  async function fetchMapNodes(refreshToken: boolean) {
    await getCollectionObject(APIEndpoint.nodes, 'machine_id', refreshToken).then(nodeObj => setNodes(nodeObj));
    await getCollectionObject(APIEndpoint.machines, 'id', refreshToken).then(machineObj => setMachines(machineObj));
    await getAllAgents(refreshToken).then(agents => setAgents(agents?.sort()));
    return getPropagationEvents(refreshToken).then(events => setPropagationEvents(events));
  }

  useEffect(() => {
    if (!updateInProgress) {
      let oneSecond = 1000;
      setUpdateInProgress(true);
      fetchMapNodes(false)
        .then(() => new Promise(r => setTimeout(r, oneSecond * 2)))
        .then(() => setUpdateInProgress(false));
    }
  }, [updateInProgress])

  useEffect(() => {
    let localGraph = generateGraph(mapNodes);
    if (mapNodes.length !== 0 && !_.isEqual(localGraph, graphSnapshot)) {
      setGraphSnapshot(_.cloneDeep(localGraph));
      setGraph(localGraph);
    }
  }, [mapNodes]);

  useEffect(() => {
    let newNodes = buildMapNodes();
    if (JSON.stringify(newNodes) !== JSON.stringify(mapNodes)) {
      setMapNodes(newNodes);
    }
  }, [nodes, machines, propagationEvents]);

  function addRelayCommunications(communications: Communications) {
    for (let [machineId, commTypes] of Object.entries(communications)) {
      let machine = machines[machineId];
      if (machine !== undefined && !machine.island
        && commTypes.includes(CommunicationType.cc)
        && !commTypes.includes(CommunicationType.relay)) {
        commTypes.push(CommunicationType.relay);
      }
    }
  }

  function buildMapNodes(): MapNode[] {
    // Build the MapNodes list
    let mapNodes: MapNode[] = [];
    for (const machine of Object.values(machines)) {
      let node = nodes[machine.id] || null;
      let communications;
      if (node !== null) {
        communications = node.connections;
        addRelayCommunications(communications);
      } else {
        communications = [];
      }
      let running = false;
      let agentIDs: string[] = [];
      let parentIDs: string[] = [];
      let agentsStartTime: Record<string, Date> = {};
      if (node !== null) {
        const nodeAgents = agents.filter(a => a.machine_id === machine.id);
        nodeAgents.forEach((nodeAgent) => {
          if (!running) {
            running = isAgentRunning(nodeAgent);
          }
          agentIDs.push(nodeAgent.id);
          parentIDs.push(nodeAgent.parent_id);
          agentsStartTime[nodeAgent.id] = new Date(nodeAgent.start_time);
        });
      }

      let propagatedTo = wasMachinePropagated(machine, propagationEvents);

      mapNodes.push(new MapNode(
        machine.id,
        machine.network_interfaces,
        running,
        communications,
        machine.operating_system,
        machine.hostname,
        machine.island,
        propagatedTo,
        agentsStartTime,
        agentIDs,
        parentIDs
      ));

    }

    return mapNodes;
  }

  function isAgentRunning(agent: Agent): boolean {
    return !Boolean(agent.stop_time)
  }

  function wasMachinePropagated(machine, propagationEvents): boolean {
    let ip = getMachineIp(machine);
    return ip in propagationEvents
  }

  return (<MapPage mapNodes={mapNodes} graph={graph} />);
}


export default MapPageWrapper
