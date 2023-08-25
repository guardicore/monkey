import React, {useContext, useState} from 'react';
import {installPlugin} from './mocksHelper';
import {shallowAdditionOfUniqueValueToArray, shallowRemovalOfUniqueValueFromArray} from '../../../utils/objectUtils';
import {PluginsContext} from './PluginsContext';
import {GridActionsCellItem} from '@mui/x-data-grid';
import {nanoid} from 'nanoid';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import DownloadDoneIcon from '@mui/icons-material/DownloadDone';
import DownloadingIcon from '@mui/icons-material/Downloading';
import BasePlugins from './BasePlugins';
import SearchBar from '../SearchBar';
import {Box} from '@mui/material';

// Provides the plugins, filtering out the installed plugins
class AvailablePluginsView {
  availablePlugins = []; // all plugins, grouped by type then name
  installedPlugins = []; // all installed plugins, grouped by type then name

  constructor(availablePlugins, installedPlugins) {
    this.availablePlugins = availablePlugins;
    this.installedPlugins = installedPlugins;
  }

  pluginInstalled(plugin_type, plugin_name) {
    return plugin_type in this.installedPlugins && plugin_name in this.installedPlugins[plugin_type];
  }

  * makeAvailablePluginsIterator() {
    for (const plugin_type in this.availablePlugins) {
      for (const plugin_name in this.availablePlugins[plugin_type]) {
        if (!this.pluginInstalled(plugin_type, plugin_name)) {
          // There may be multiple versions of the same plugin, so we only want the latest one
          yield this.availablePlugins[plugin_type][plugin_name].slice(-1)[0];
        }
      }
    }
  }

  [Symbol.iterator]() {
    return this.makeAvailablePluginsIterator();
  }
};

const AvailablePlugins = () => {
  const {availablePlugins} = useContext(PluginsContext);
  const {installedPlugins} = useContext(PluginsContext);
  const availablePluginsView = new AvailablePluginsView(availablePlugins, installedPlugins);

  const [successfullyInstalledPluginsIds, setSuccessfullyInstalledPluginsIds] = useState([]);
  const [pluginsInInstallationProcess, setPluginsInInstallationProcess] = useState([]);

  const onRefreshCallback = () => {
    setSuccessfullyInstalledPluginsIds([]);
  }

  const onInstallClick = (pluginId) => {
    setPluginsInInstallationProcess((prevState) => {
      return shallowAdditionOfUniqueValueToArray(prevState, pluginId);
    });

    installPlugin(pluginId).then(() => {
      setSuccessfullyInstalledPluginsIds((prevState) => {
        return shallowAdditionOfUniqueValueToArray(prevState, pluginId);
      });
    }).catch(() => {
      console.log('error installing plugin');
    }).finally(() => {
      setPluginsInInstallationProcess((prevState => {
        return shallowRemovalOfUniqueValueFromArray(prevState, pluginId);
      }));
    });
  };

  const getRowActions = (pluginId) => {
    if (pluginsInInstallationProcess.includes(pluginId)) {
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

    if (successfullyInstalledPluginsIds.includes(pluginId)) {
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

    return [
      <GridActionsCellItem
        key={nanoid()}
        icon={<FileDownloadIcon/>}
        label="Download"
        className="textPrimary"
        onClick={() => onInstallClick(pluginId)}
        color="inherit"
      />
    ];
  }

  return (
    <Box>
      <SearchBar />
      <BasePlugins plugins={availablePluginsView}
                   loadingMessage="Loading all available plugins..."
                   onRefreshCallback={onRefreshCallback}
                   getRowActions={getRowActions}
      />
    </Box>
  )
};

export default AvailablePlugins;
