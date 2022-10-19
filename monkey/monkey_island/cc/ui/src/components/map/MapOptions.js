import { CommunicationType, NodeGroup } from 'components/types/MapNode';

let getGroupsOptions = (stateList) => {
  let groupOptions = {};
  for (let stateName of stateList) {
    groupOptions[stateName] =
    {
      shape: 'image',
      size: 50,
      image: require('../../images/nodes/' + stateName + '.png')
    };
  }

  return groupOptions;
};

export const basic_options = {
  autoResize: true,
  layout: {
    improvedLayout: false
  },
  edges: {
    width: 2,
    smooth: {
      type: 'curvedCW'
    }
  },
  physics: {
    barnesHut: {
      gravitationalConstant: -120000,
      avoidOverlap: 0.5,
      springLength: 100,
      springConstant: 0.025
    },
    minVelocity: 0.7,
    maxVelocity: 25
  }
};

const nodeStates = Object.keys(NodeGroup);
const groupsOptions = getGroupsOptions(nodeStates);

export function getOptions() {
  let opts = JSON.parse(JSON.stringify(basic_options)); /* Deep copy */
  opts.groups = groupsOptions;
  return opts;
}

export function edgeGroupToColor(group) {
  switch (group) {
    case CommunicationType.exploited:
      return '#c00';
    case CommunicationType.relay:
      return '#0058aa';
    case CommunicationType.scanned:
      return '#f90';
    case CommunicationType.cc:
      return '#aaa';
  }
  return 'black';
}
