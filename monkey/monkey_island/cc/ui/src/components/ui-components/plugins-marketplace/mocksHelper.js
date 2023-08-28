import {nanoid} from 'nanoid';
import {generatePluginId} from './utils';

const HEADER_SUFFIX = '--header';

const versions = ['1.0.0', '1.1.1', '2.1.3'];
const types = ['exploiter', 'credentials'];
const upgradeableOptions = [true, false];

const generateData = (num, isInstalled= false) => {
  let arr = [];
  for(let i=0;i<num;i++){
    const type = types[Math.floor(Math.random() * types.length)];
    const description = `${type} ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum`;
    const obj = {
      id: nanoid(),
      name: `plugin_${i}`,
      version: versions[Math.floor(Math.random() * versions.length)],
      type: type,
      author: `Monkey Team - ${nanoid()}`,
      description: description
    }
    if(isInstalled) {
      obj['upgradeable'] = upgradeableOptions[Math.floor(Math.random() * upgradeableOptions.length)]
    }
    arr.push(obj);
  }
  return arr;
}

export const getPlugins = (installed = false, shouldResolveEmpty = false, shouldResolve = true) => {
  return new Promise((resolve, reject) => {
    setTimeout(()=>{
      if(shouldResolve) {
        shouldResolveEmpty ? resolve([]) : (installed ? resolve(generateData(20, true)) : resolve(generateData(15)));
      } else {
        reject('Errorrr')
      }
    }, 0);
  })
};

export const installPlugin = (id, success = true) => {
  return new Promise((resolve, reject) => {
    setTimeout(()=>{
      if(success) {
        resolve(id);
      } else {
        reject('Errorrr install')
      }
    }, 5000);
  })
}

export const uninstallPlugin = (id, success = true) => {
  return new Promise((resolve, reject) => {
    setTimeout(()=>{
      if(success) {
        resolve(id);
      } else {
        reject('Errorrr uninstall')
      }
    }, 5000);
  })
}

export const upgradePlugin = (id, success = true) => {
  return new Promise((resolve, reject) => {
    setTimeout(()=>{
      if(success) {
        resolve(id);
      } else {
        reject('Errorrr upgrade')
      }
    }, 5000);
  })
}

// Returns GridColDef[]
export const getPluginsGridHeaders = (getRowActions) => [
  {headerName: 'Name', field: 'name', sortable: true, filterable: false, flex: 0.4, minWidth: 150, flexValue: 0.5},
  {headerName: 'Version', field: 'version', sortable: false, filterable: false, flex: 0.1, minWidth: 100, flexValue: 0.5},
  {headerName: 'Type', field: 'type', sortable: true, filterable: false, flex: 0.2, minWidth: 150, flexValue: 0.5},
  {headerName: 'Author', field: 'author', sortable: true, filterable: false, minWidth: 150, flex: 0.25, flexValue: 0.5},
  {headerName: 'Description', field: 'description', sortable: false, filterable: false, minWidth: 150, flex: 1},
  // This column is a GridActionsColDef
  {
    headerName: '',
    field: 'row_actions',
    type: 'actions',
    minWidth: 100,
    flex: 0.1,
    flexValue: 0.5,
    headerClassName: `row-actions${HEADER_SUFFIX}`,
    cellClassName: `row-actions`,
    // params is a GridRowParams
    getActions: (params) => {
      return getRowActions(params.row);
    }
  }
]

export const getPluginsGridRows = (pluginsList) => {
  let plugins = [];
  for (const plugin of pluginsList) {
    const {name, version, type_, author, description} = {...plugin};
    plugins.push({
        id: generatePluginId(plugin),
        name: name,
        version: version,
        type: type_,
        author: author,
        description: description
      });
  }

  return plugins;
}
