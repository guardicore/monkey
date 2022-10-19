import {edgeGroupToColor} from './MapOptions';
import MapNode, {CommunicationType} from '../types/MapNode';


const priorityList = [CommunicationType.relay, CommunicationType.cc,
  CommunicationType.exploited, CommunicationType.scanned];

export type Edge = {
  from: Number;
  to: Number;
  color: string;
}

export type GraphNode = {
  id: Number;
  group: string;
  label: string;
}

export type Graph = {
  edges: Edge[];
  nodes: GraphNode[];
}

function getCommunicationType(communicationTypes: CommunicationType[]): CommunicationType {
  for (const priority of priorityList) {
    if (communicationTypes.includes(priority)) {
      return priority;
    }
  }

  throw new Error(`Communication types could not be prioritized: ${communicationTypes}`);
}

function generateEdges(mapNodes: MapNode[]): Edge[] {
  let edges = [];
  for (const mapNode of mapNodes) {
    for (const [connectedTo, connectionTypes] of Object.entries(mapNode.connections)) {
      const connectionType = getCommunicationType(connectionTypes);
      edges.push({
        from: mapNode.machineId,
        to: connectedTo,
        color: edgeGroupToColor(connectionType)
      });
    }
  }

  return edges;
}

function generateNodes(mapNodes: MapNode[]): GraphNode[] {
  let nodes = [];
  for (const mapNode of mapNodes) {
    nodes.push({
      id: mapNode.machineId,
      group: mapNode.calculateNodeGroup(),
      label: mapNode.getLabel()
    });
  }
  return nodes;
}

function generateGraph(mapNodes: MapNode[]): Graph {
  console.log(mapNodes)
  return {
    edges: generateEdges(mapNodes),
    nodes: generateNodes(mapNodes)
  };
}

export default generateGraph;
