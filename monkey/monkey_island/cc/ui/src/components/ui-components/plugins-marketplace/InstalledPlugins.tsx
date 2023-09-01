import React, {useContext, useEffect, useState} from 'react';
import {InstalledPlugin, PluginsContext} from '../../contexts/plugins/PluginsContext';
import {shallowAdditionOfUniqueValueToArray, shallowRemovalOfUniqueValueFromArray} from '../../../utils/objectUtils';
import {GridActionsCellItem} from '@mui/x-data-grid';
import {Grid, Stack} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AutoDeleteIcon from '@mui/icons-material/AutoDelete';
import DownloadingIcon from '@mui/icons-material/Downloading';
import DownloadDoneIcon from '@mui/icons-material/DownloadDone';
import UpgradeIcon from '@mui/icons-material/Upgrade';
import RemoveDoneIcon from '@mui/icons-material/RemoveDone';
import BasePlugins from './BasePlugins';
import AuthComponent from '../../AuthComponent';
import MonkeyToggle from '../MonkeyToggle';
import SearchBar from '../SearchBar';
import TypeFilter from './TypeFilter';
import semver from 'semver';


const InstalledPlugins = (props) => {
  const {
    successfullyUpdatedPluginsIds, setSuccessfullyUpdatedPluginsIds,
    pluginsInUpdateProcess, setPluginsInUpdateProcess,
    successfullyUninstalledPluginsIds, setSuccessfullyUninstalledPluginsIds,
    pluginsInUninstallProcess, setPluginsInUninstallProcess
  } = {...props};
  const {installedPlugins, refreshInstalledPlugins, availablePlugins} = useContext(PluginsContext);
  const [displayedPlugins, setDisplayedPlugins] = useState([]);
  const [filters, setFilters] = useState({});
  const authComponent = new AuthComponent({});

  useEffect(() => {
    setDisplayedPlugins(installedPlugins)
  }, []);

  useEffect(() => {
    let shownPlugins = installedPlugins;
    for (const filter of Object.values(filters)) {
      shownPlugins = shownPlugins.filter(filter);
    }
    setDisplayedPlugins(shownPlugins);
  }, [installedPlugins, filters]);

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
    setPluginsInUpdateProcess((prevState) => {
      return shallowAdditionOfUniqueValueToArray(prevState, pluginId);
    });

    upgradePlugin(pluginType, name, version).then(() => {
      setSuccessfullyUpdatedPluginsIds((prevState) => {
        return shallowAdditionOfUniqueValueToArray(prevState, pluginId);
      });
      refreshInstalledPlugins();
    }).catch(() => {
      console.log('error upgrading plugin');
    }).finally(() => {
      setPluginsInUpdateProcess((prevState => {
        return shallowRemovalOfUniqueValueFromArray(prevState, pluginId);
      }));
    });
  }

  const isPluginUpgradable = (plugin :InstalledPlugin) => {
    const latestVersion = getLatestVersion(plugin);
    if (latestVersion) {
      return semver.gt(latestVersion, plugin.version);
    } else {
      return false;
    }
  }

  const getLatestVersion = (plugin :InstalledPlugin) :string => {
    const latestPlugin = availablePlugins.find(availablePlugin => {
      return availablePlugin.name === plugin.name && availablePlugin.pluginType === plugin.pluginType
    });
    if (!latestPlugin) {
      // Custom plugin might not be available in the marketplace
      return undefined;
    } else {
      return latestPlugin.version;
    }
  }

  const getUpgradeAction = (row) => {
    const plugin = installedPlugins.find(installedPlugin => installedPlugin.id === row.id);
    const pluginId = row.id;
    if (pluginsInUpdateProcess.includes(pluginId)) {
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

    if (successfullyUpdatedPluginsIds.includes(pluginId)) {
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

    if ((!pluginsInUninstallProcess.includes(pluginId))
        && (!successfullyUninstalledPluginsIds.includes(pluginId))
        && isPluginUpgradable(plugin)) {
      return [
        <GridActionsCellItem
        key={pluginId + 'upgrade'}
        icon={<UpgradeIcon/>}
        label="Upgrade"
        className="textPrimary"
        onClick={() => onUpgradeClick(pluginId, row.type, row.name, getLatestVersion(plugin))}
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
          icon={<AutoDeleteIcon/>}
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

    if (pluginsInUpdateProcess.includes(pluginId)) {
      return [
        <GridActionsCellItem
          key={pluginId + 'uninstall'}
          icon={<DeleteIcon/>}
          label="Uninstalling"
          className="textPrimary"
          disabled={true}
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

  const onSearchChanged = (query) => {
    const filterOnText = (plugin) => {
      for (const property in plugin) {
        if (typeof plugin[property] === 'string' && plugin[property].toLowerCase().includes(query.toLowerCase())) {
          return true;
        }
      }
    }
    setFilters((prevState) => {
      return {...prevState, text: filterOnText};
    });
  }

  const onToggleChanged = (selectedValue) => {
    if (selectedValue === 'upgradable') {
      setFilters((prevState) => {
        return {...prevState, upgradable: (plugin) => isPluginUpgradable(plugin)};
      });
    }
    else {
      setFilters((prevState) => {
        return {...prevState, upgradable: () => true};
      });
    }
  }

  return (
    <Stack spacing={2} height='100%'>
      <Grid container spacing={2}>
        <Grid xs={4} item>
          <SearchBar setQuery={onSearchChanged} />
        </Grid>
        <Grid xs={3} item>
          <TypeFilter allPlugins={installedPlugins}
                        filters={filters}
                        setFilters={setFilters}
                        className={'type-filter-box'}/>
        </Grid>
        <Grid xs={2} item />
        <Grid xs={3} item >
          <MonkeyToggle options={[{value: 'all', label: 'All'},{value: 'upgradable', label: 'Upgradable'}]}
                      setSelectedValues={onToggleChanged}/>
        </Grid>
      </Grid>
      <BasePlugins plugins={displayedPlugins}
                  loadingMessage="Loading all available plugins..."
                  onRefreshCallback={onRefreshCallback}
                  getRowActions={getRowActions}
      />
    </Stack>
  )
};

export default InstalledPlugins;