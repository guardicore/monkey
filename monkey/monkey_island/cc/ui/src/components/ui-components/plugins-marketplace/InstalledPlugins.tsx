import React, {useContext, useState} from 'react';
import {PluginsContext} from '../../contexts/plugins/PluginsContext';
import {shallowAdditionOfUniqueValueToArray, shallowRemovalOfUniqueValueFromArray} from '../../../utils/objectUtils';
import {GridActionsCellItem} from '@mui/x-data-grid';
import {nanoid} from 'nanoid';
import DownloadingIcon from '@mui/icons-material/Downloading';
import DownloadDoneIcon from '@mui/icons-material/DownloadDone';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import BasePlugins from './BasePlugins';
import AuthComponent from '../../AuthComponent';

class InstalledPluginsView {
  availablePlugins = []; // all plugins, grouped by type then name
  installedPlugins = []; // all installed plugins, grouped by type then name

  constructor(availablePlugins, installedPlugins) {
    this.availablePlugins = availablePlugins;
    this.installedPlugins = installedPlugins;
  }

  // TODO: Add a field for update available
  * makeInstalledPluginsIterator() {
    for (const plugin_type in this.installedPlugins) {
      for (const plugin_name in this.installedPlugins[plugin_type]) {
        yield this.installedPlugins[plugin_type][plugin_name];
      }
    }
  }

  [Symbol.iterator]() {
    return this.makeInstalledPluginsIterator();
  }
};

const InstalledPlugins = () => {
  const {availablePlugins, installedPlugins, refreshInstalledPlugins} = useContext(PluginsContext);
  const installedPluginsView = new InstalledPluginsView(availablePlugins, installedPlugins);

  const [successfullyUninstalledPluginsIds, setSuccessfullyUninstalledPluginsIds] = useState([]);
  const [pluginsInUninstallProcess, setPluginsInUninstallProcess] = useState([]);
  const authComponent = new AuthComponent({});

  const onRefreshCallback = () => {
    setSuccessfullyUninstalledPluginsIds([]);
  }

  const uninstallPlugin = (pluginType, pluginName) => {
    const options = {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({plugin_type: pluginType, name: pluginName})
    };
    return authComponent.authFetch('/api/uninstall-agent-plugin', options, true)
  }

  const onUninstallClick = (pluginId, pluginType, pluginName) => {
    setPluginsInUninstallProcess((prevState) => {
      return shallowAdditionOfUniqueValueToArray(prevState, pluginId);
    });

    uninstallPlugin(pluginType, pluginName).then(() => {
      setSuccessfullyUninstalledPluginsIds((prevState) => {
        return shallowAdditionOfUniqueValueToArray(prevState, pluginId);
      });
      refreshInstalledPlugins();
    }).catch(() => {
      console.log('error uninstalling plugin');
    }).finally(() => {
      setPluginsInUninstallProcess((prevState => {
        return shallowRemovalOfUniqueValueFromArray(prevState, pluginId);
      }));
    });
  };

  const getRowActions = (row) => {
    const pluginId = row.id;
    if (pluginsInUninstallProcess.includes(pluginId)) {
      return [
        <GridActionsCellItem
          key={nanoid()}
          icon={<DownloadingIcon/>}
          label="Downloading"
          className="textPrimary"
          color="inherit"
        />
      ]
    }

    if (successfullyUninstalledPluginsIds.includes(pluginId)) {
      return [
        <GridActionsCellItem
          key={nanoid()}
          icon={<DownloadDoneIcon/>}
          label="Download Done"
          className="textPrimary"
          color="inherit"
        />
      ]
    }

    const pluginName = row.name;
    const pluginType = row.type;
    return [
      <GridActionsCellItem
        key={nanoid()}
        icon={<FileDownloadIcon/>}
        label="Download"
        className="textPrimary"
        onClick={() => onUninstallClick(pluginId, pluginType, pluginName)}
        color="inherit"
      />
    ];
  }

  return (
    <BasePlugins plugins={[...installedPluginsView]}
                 loadingMessage="Loading all available plugins..."
                 onRefreshCallback={onRefreshCallback}
                 getRowActions={getRowActions}
    />
  )
};

export default InstalledPlugins;
