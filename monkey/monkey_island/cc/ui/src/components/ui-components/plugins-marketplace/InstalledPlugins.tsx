import React, {useContext, useEffect, useMemo, useState} from 'react';
import {
  generatePluginId,
  InstalledPlugin,
  PluginsContext
} from '../../contexts/plugins/PluginsContext';
import {shallowAdditionOfUniqueValueToArray, shallowRemovalOfUniqueValueFromArray} from '../../../utils/objectUtils';
import {GridActionsCellItem} from '@mui/x-data-grid';
import {Grid, Stack} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import DownloadDoneIcon from '@mui/icons-material/DownloadDone';
import UpgradeIcon from '@mui/icons-material/Upgrade';
import RemoveDoneIcon from '@mui/icons-material/RemoveDone';
import PluginTable, {
  generatePluginsTableColumns,
  generatePluginsTableRows,
} from './PluginTable';
import MonkeyToggle from '../MonkeyToggle';
import TypeFilter from './TypeFilter';
import LoadingIcon from '../LoadingIconMUI';
import semver from 'semver';
import SearchFilter, {defaultSearchableColumns} from './SearchFilter';
import IslandHttpClient, { APIEndpoint } from '../../IslandHttpClient';


const UPGRADEABLE_VALUE = 'upgradeable';
const NO_INSTALLED_PLUGINS_MESSAGE = 'There are no plugins installed';
const FETCHING_ERROR_MESSAGE = 'An error occurred while retrieving the installed plugins';

const InstalledPlugins = (props) => {
  const {
    successfullyUpdatedPluginsIds, setSuccessfullyUpdatedPluginsIds,
    pluginsInUpdateProcess, setPluginsInUpdateProcess,
    successfullyUninstalledPluginsIds, setSuccessfullyUninstalledPluginsIds,
    pluginsInUninstallProcess, setPluginsInUninstallProcess
  } = {...props};
  const {installedPlugins, refreshInstalledPlugins, availablePlugins, refreshInstalledPluginsFailure} = useContext(PluginsContext);
  const [displayedRows, setDisplayedRows] = useState([]);
  const [filters, setFilters] = useState({});

  const installedPluginRows = useMemo(() => {
    return generatePluginsTableRows(installedPlugins);
  }, [installedPlugins]);

  useEffect(() => {
    let allRows = installedPluginRows;
    for (const filter of Object.values(filters)) {
      allRows = allRows.filter(filter);
    }
    setDisplayedRows(allRows);
  }, [installedPlugins, filters]);

  const uninstallPlugin = (pluginType, pluginName) => {
    let contents = {plugin_type: pluginType, name: pluginName};
    return IslandHttpClient.postJSON(APIEndpoint.uninstallAgentPlugin, contents, true)
  }

  const onUninstallClick = (pluginId, pluginType, pluginName) => {
    setPluginsInUninstallProcess((prevState) => {
      return shallowAdditionOfUniqueValueToArray(prevState, pluginId);
    });

    uninstallPlugin(pluginType, pluginName).then(() => {
      setSuccessfullyUninstalledPluginsIds((prevState) => {
        return shallowAdditionOfUniqueValueToArray(prevState, pluginId);
      });
    }).catch(() => {
      console.log('error uninstalling plugin');
    }).finally(() => {
      setPluginsInUninstallProcess((prevState => {
        return shallowRemovalOfUniqueValueFromArray(prevState, pluginId);
      }));
    });
  }

  const upgradePlugin = (pluginType, name, version) => {
    let contents = {plugin_type: pluginType, name: name, version: version};
    return IslandHttpClient.putJSON(APIEndpoint.installAgentPlugin, contents, true)
  }

  const onUpgradeClick = (pluginId, pluginType, name, version) => {
    setPluginsInUpdateProcess((prevState) => {
      return shallowAdditionOfUniqueValueToArray(prevState, pluginId);
    });

    upgradePlugin(pluginType, name, version).then(() => {
      setSuccessfullyUpdatedPluginsIds((prevState) => {
        const newPluginId = generatePluginId(name, pluginType, version);
        return shallowAdditionOfUniqueValueToArray(prevState, newPluginId);
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

  const getUpgradeAction = (plugin :InstalledPlugin) => {
    if (pluginsInUpdateProcess.includes(plugin.id)) {
      return [
        <GridActionsCellItem
          key={plugin.id + 'upgrade'}
          icon={<LoadingIcon/>}
          label="Upgrading"
          className="textPrimary"
          color="inherit"
        />
      ]
    }

    if (successfullyUpdatedPluginsIds.includes(plugin.id)) {
      return [
        <GridActionsCellItem
          key={plugin.id + 'upgrade'}
          icon={<DownloadDoneIcon/>}
          label="Upgrade Complete"
          className="textPrimary"
          color="inherit"
        />
      ]
    }

    if ((!pluginsInUninstallProcess.includes(plugin.id))
        && (!successfullyUninstalledPluginsIds.includes(plugin.id))
        && isPluginUpgradable(plugin)) {
      return [
        <GridActionsCellItem
        key={plugin.id + 'upgrade'}
        icon={<UpgradeIcon/>}
        label="Upgrade"
        className="textPrimary"
        onClick={() => onUpgradeClick(plugin.id, plugin.pluginType, plugin.name, getLatestVersion(plugin))}
        color="inherit"
      />
      ]
    }

    return [
      <GridActionsCellItem
      key={plugin.id + 'upgrade'}
      icon={<UpgradeIcon/>}
      label="Upgrade"
      className="textPrimary"
      disabled={true}
      color="inherit"
    />
    ];
  }

  const getUninstallAction = (plugin :InstalledPlugin) => {
    if (pluginsInUninstallProcess.includes(plugin.id)) {
      return [
        <GridActionsCellItem
          key={plugin.id + 'uninstall'}
          icon={<LoadingIcon/>}
          label="Uninstalling"
          className="textPrimary"
          color="inherit"
        />
      ]
    }

    if (successfullyUninstalledPluginsIds.includes(plugin.id)) {
      return [
        <GridActionsCellItem
          key={plugin.id + 'uninstall'}
          icon={<RemoveDoneIcon/>}
          label="Uninstall Complete"
          className="textPrimary"
          color="inherit"
        />
      ]
    }

    if (pluginsInUpdateProcess.includes(plugin.id)) {
      return [
        <GridActionsCellItem
          key={plugin.id + 'uninstall'}
          icon={<DeleteIcon/>}
          label="Uninstalling"
          className="textPrimary"
          disabled={true}
          color="inherit"
        />
      ]
    }

    return [
      <GridActionsCellItem
        key={plugin.id + 'uninstall'}
        icon={<DeleteIcon/>}
        label="Uninstall"
        className="textPrimary"
        onClick={() => onUninstallClick(plugin.id, plugin.pluginType, plugin.name)}
        color="inherit"
      />
    ];
  }

  const getRowActions = (row) => {
    const plugin = installedPlugins.find(installedPlugin => installedPlugin.id === row.id);
    if(!plugin) return [];
    return [...getUpgradeAction(plugin), ...getUninstallAction(plugin)]
  }

  const onToggleChanged = (selectedValue) => {

    const noOp = (row) => true;

    const upgradeFilter = (row) => {
      let plugin = installedPlugins.find(plugin => plugin.id === row.id)
      if(plugin){
        return isPluginUpgradable(plugin);
      } else {
        return false;
      }
    }

    let filter = selectedValue === UPGRADEABLE_VALUE ? upgradeFilter : noOp

    setFilters((prevState) => {
      return {...prevState, upgradable: filter};
    });
  }

  const renderFilters = () => {
    if(installedPlugins?.length > 0) {
      return (
        <>
          <Grid container spacing={2}>
            <Grid xs={4} item
                  sx={{alignItems: 'flex-end', display: 'flex'}}>
              <SearchFilter setFilters={setFilters}
                            searchableColumns={defaultSearchableColumns}/>
            </Grid>
            <Grid xs={3} item
                  sx={{alignItems: 'flex-end', display: 'flex'}}>
              <TypeFilter allRows={installedPluginRows}
                          setFilters={setFilters}/>
            </Grid>
            <Grid xs={2} item/>
            <Grid xs={3} item>
              <MonkeyToggle options={[{value: 'all', label: 'All'},
                {value: UPGRADEABLE_VALUE, label: 'Upgradable'}]}
                            setSelectedValues={onToggleChanged}/>
            </Grid>
          </Grid>
        </>
      )
    }
    return null;
  }

  const getOverlayMessage = () => {
    if(refreshInstalledPluginsFailure) {
      return FETCHING_ERROR_MESSAGE;
    } else if(installedPlugins?.length === 0) {
      return NO_INSTALLED_PLUGINS_MESSAGE;
    }
    return null;
  }

  return (
    <Stack spacing={2} height='100%'>
      {renderFilters()}
      <PluginTable rows={displayedRows}
                   columns={generatePluginsTableColumns(getRowActions)}
                   loadingMessage="Loading all installed plugins..."
                   noRowsOverlayMessage={getOverlayMessage()}
                   getRowActions={getRowActions}
      />
    </Stack>
  )
};

export default InstalledPlugins;
