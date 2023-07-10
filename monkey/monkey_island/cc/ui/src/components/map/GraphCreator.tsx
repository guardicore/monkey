import { edgeGroupToColor } from "./MapOptions";
import MapNode, { CommunicationType } from "../types/MapNode";

// This determines the display priority of the connection types, from highest to lowest
const priorityList = [
  CommunicationType.relay,
  CommunicationType.cc,
  CommunicationType.exploited,
  CommunicationType.scanned,
];

export type Edge = {
  from: Number;
  to: Number;
  color: string;
};

export type GraphNode = {
  id: Number;
  group: string;
  label: string;
};

export type Graph = {
  edges: Edge[];
  nodes: GraphNode[];
};

function getCommunicationType(
  communicationTypes: CommunicationType[],
): CommunicationType {
  for (const priority of priorityList) {
    if (communicationTypes.includes(priority)) {
      return priority;
    }
  }

  throw new Error(
    `Communication types could not be prioritized: ${communicationTypes}`,
  );
}

function generateEdges(mapNodes: MapNode[]): Edge[] {
  let edges = [];
  for (const mapNode of mapNodes) {
    for (const [connectedTo, communicationTypes] of Object.entries(
      mapNode.communications,
    )) {
      const commType = getCommunicationType(communicationTypes);
      if (mapNode.island && String(connectedTo) === String(mapNode.machineId)) {
        // Don't draw an edge from island to island
        continue;
      }
      edges.push({
        from: mapNode.machineId,
        to: connectedTo,
        color: edgeGroupToColor(commType),
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
      label: mapNode.getLabel(),
    });
  }
  return nodes;
}

function generateGraph(mapNodes: MapNode[]): Graph {
  return {
    edges: generateEdges(mapNodes),
    nodes: generateNodes(mapNodes),
  };
}

export default generateGraph;
