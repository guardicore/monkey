import React, {useContext, useState} from 'react';
import {PluginsContext} from '../../contexts/plugins/PluginsContext';
import {shallowAdditionOfUniqueValueToArray, shallowRemovalOfUniqueValueFromArray} from '../../../utils/objectUtils';
import {GridActionsCellItem} from '@mui/x-data-grid';
import DeleteIcon from '@mui/icons-material/Delete';
import DownloadingIcon from '@mui/icons-material/Downloading';
import DownloadDoneIcon from '@mui/icons-material/DownloadDone';
import UpgradeIcon from '@mui/icons-material/Upgrade';
import RemoveDoneIcon from '@mui/icons-material/RemoveDone';
import BasePlugins from './BasePlugins';
import AuthComponent from '../../AuthComponent';
import semver from 'semver';

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
        const installed_version = this.installedPlugins[plugin_type][plugin_name]['version'];
        const latest_version = this.availablePlugins[plugin_type][plugin_name].slice(-1)[0]['version'];
        const update_available = semver.gt(latest_version, installed_version)
        yield {...this.installedPlugins[plugin_type][plugin_name], update_available};
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

  const [successfullyInstalledPluginsIds, setSuccessfullyInstalledPluginsIds] = useState([]);
  const [pluginsInInstallProcess, setPluginsInInstallProcess] = useState([]);
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
  }

  const upgradePlugin = (pluginType, name, version) => {
    const options = {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({plugin_type: pluginType, name: name, version: version})
    }
    return authComponent.authFetch('/api/install-agent-plugin', options, true);
  }

  const onUpgradeClick = (pluginId, pluginType, name, version) => {
    setPluginsInInstallProcess((prevState) => {
      return shallowAdditionOfUniqueValueToArray(prevState, pluginId);
    });

    upgradePlugin(pluginType, name, version).then(() => {
      setSuccessfullyInstalledPluginsIds((prevState) => {
        return shallowAdditionOfUniqueValueToArray(prevState, pluginId);
      });
      refreshInstalledPlugins();
    }).catch(() => {
      console.log('error upgrading plugin');
    }).finally(() => {
      setPluginsInInstallProcess((prevState => {
        return shallowRemovalOfUniqueValueFromArray(prevState, pluginId);
      }));
    });
  }

  const getUpgradeAction = (row) => {
    const pluginId = row.id;
    if (pluginsInInstallProcess.includes(pluginId)) {
      return [
        <GridActionsCellItem
          key={pluginId + 'upgrade'}
          icon={<DownloadingIcon/>}
          label="Upgrading"
          className="textPrimary"
          color="inherit"
        />
      ]
    }

    if (successfullyInstalledPluginsIds.includes(pluginId)) {
      return [
        <GridActionsCellItem
          key={pluginId + 'upgrade'}
          icon={<DownloadDoneIcon/>}
          label="Upgrade Complete"
          className="textPrimary"
          color="inherit"
        />
      ]
    }

    if (row.update_available) {
      const latest_plugin = availablePlugins[row.type][row.name].slice(-1)[0]
      return [
        <GridActionsCellItem
        key={pluginId + 'upgrade'}
        icon={<UpgradeIcon/>}
        label="Upgrade"
        className="textPrimary"
        onClick={() => onUpgradeClick(pluginId, row.type, row.name, latest_plugin.version)}
        color="inherit"
      />
      ]
    }

    return [
      <GridActionsCellItem
      key={pluginId + 'upgrade'}
      icon={<UpgradeIcon/>}
      label="Upgrade"
      className="textPrimary"
      disabled={true}
      color="inherit"
    />
    ];
  }

  const getUninstallAction = (row) => {
    const pluginId = row.id;
    if (pluginsInUninstallProcess.includes(pluginId)) {
      return [
        <GridActionsCellItem
          key={pluginId + 'uninstall'}
          icon={<DownloadingIcon/>}
          label="Uninstalling"
          className="textPrimary"
          color="inherit"
        />
      ]
    }

    if (successfullyUninstalledPluginsIds.includes(pluginId)) {
      return [
        <GridActionsCellItem
          key={pluginId + 'uninstall'}
          icon={<RemoveDoneIcon/>}
          label="Uninstall Complete"
          className="textPrimary"
          color="inherit"
        />
      ]
    }

    const pluginName = row.name;
    const pluginType = row.type;
    return [
      <GridActionsCellItem
        key={pluginId + 'uninstall'}
        icon={<DeleteIcon/>}
        label="Uninstall"
        className="textPrimary"
        onClick={() => onUninstallClick(pluginId, pluginType, pluginName)}
        color="inherit"
      />
    ];
  }

  const getRowActions = (row) => {
    return [...getUpgradeAction(row), ...getUninstallAction(row)]
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
