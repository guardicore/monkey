const groupNames = ['clean_unknown', 'clean_linux', 'clean_windows', 'exploited_linux', 'exploited_windows', 'island',
  'island_monkey_linux', 'island_monkey_linux_running', 'island_monkey_windows', 'island_monkey_windows_running',
  'manual_linux', 'manual_linux_running', 'manual_windows', 'manual_windows_running', 'monkey_linux',
  'monkey_linux_running', 'monkey_windows', 'monkey_windows_running'];

let getGroupsOptions = () => {
  let groupOptions = {};
  for (let groupName of groupNames) {
    groupOptions[groupName] =
      {
        shape: 'image',
        size: 50,
        image: require('../../images/nodes/' + groupName + '.png')
      };
  }
  return groupOptions;
};

const groupNamesPth = ['normal', 'critical'];

let getGroupsOptionsPth = () => {
  let groupOptions = {};
  for (let groupName of groupNamesPth) {
    groupOptions[groupName] =
      {
        shape: 'image',
        size: 50,
        image: require('../../images/nodes/pth/' + groupName + '.png')
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
      avoidOverlap: 0.5
    },
    minVelocity: 0.75
  }
};

export const options = (() => {
  let opts = JSON.parse(JSON.stringify(basic_options)); /* Deep copy */
  opts.groups = getGroupsOptions();
  return opts;
})();

export const optionsPth = (() => {
  let opts = JSON.parse(JSON.stringify(basic_options)); /* Deep copy */
  opts.groups = getGroupsOptionsPth();
  opts.physics.barnesHut.gravitationalConstant = -20000;
  return opts;
})();

export function edgeGroupToColor(group) {
  switch (group) {
    case 'exploited':
      return '#c00';
    case 'tunnel':
      return '#0058aa';
    case 'scan':
      return '#f90';
    case 'island':
      return '#aaa';
  }
  return 'black';
}
