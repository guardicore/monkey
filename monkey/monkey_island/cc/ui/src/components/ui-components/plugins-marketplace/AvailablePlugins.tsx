import React, {useContext, useEffect, useState} from 'react';
import {
  shallowAdditionOfUniqueValueToArray,
  shallowRemovalOfUniqueValueFromArray
} from '../../../utils/objectUtils';
import {AvailablePlugin, PluginsContext} from '../../contexts/plugins/PluginsContext';
import {GridActionsCellItem} from '@mui/x-data-grid';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import DownloadDoneIcon from '@mui/icons-material/DownloadDone';
import {Box, Grid, Stack} from '@mui/material';
import PluginTable, {getSearchableFields} from './PluginTable';
import SearchBar from '../SearchBar';
import AuthComponent from '../../AuthComponent';
import {Button} from 'react-bootstrap';
import RefreshIcon from '@mui/icons-material/Refresh';
import styles from '../../../styles/components/plugins-marketplace/AvailablePlugins.module.scss';
import LoadingIcon from '../LoadingIconMUI';
import TypeFilter from './TypeFilter';

type AvailablePluginArray = AvailablePlugin[];

const AvailablePlugins = (props) => {
  const {
    installingAllSafePlugins,
    setInstallingAllSafePlugins,
    successfullyInstalledPluginsIds,
    setSuccessfullyInstalledPluginsIds,
    pluginsInInstallationProcess,
    setPluginsInInstallationProcess
  } = {...props};
  const {availablePlugins, installedPlugins, refreshAvailablePlugins} = useContext(PluginsContext);
  const [displayedPlugins, setDisplayedPlugins] = useState<AvailablePluginArray>([]);
  const [filters, setFilters] = useState({});
  const [isSpinning, setIsSpinning] = useState(false);

  const authComponent = new AuthComponent({});

  useEffect(() => {
    setDisplayedPlugins(availablePlugins);
    setFilters((prevState) => {
      return {...prevState, installed: filterInstalledPlugins};
    });
  }, []);

  useEffect(() =>{
    disableInstallAllSafePlugins()
  }, [displayedPlugins]);

  useEffect(() => {
    filterPlugins();
  }, [availablePlugins, installedPlugins, filters]);

  useEffect(() => {
    setFilters((prevState) => {
      return {...prevState, installed: filterInstalledPlugins};
    });
  }, [installedPlugins]);

  const filterPlugins = () => {
    let shownPlugins = availablePlugins;
    for (const filter of Object.values(filters)) {
      shownPlugins = shownPlugins.filter(filter);
    }
    setDisplayedPlugins(shownPlugins);
  }

  const disableInstallAllSafePlugins = () => {
    let unSafeDispalyedPlugins = [];
    let safeDispalyedPlugins = [];
    for (const plugin of displayedPlugins) {
      if (!plugin.safe) {
        unSafeDispalyedPlugins.push(plugin.name);
      } else {
        safeDispalyedPlugins.push(plugin.name);
      }
    }
    setInstallingAllSafePlugins(unSafeDispalyedPlugins.length > 0 && safeDispalyedPlugins.length === 0 || displayedPlugins.length === 0)
  }

  const onRefreshCallback = () => {
    setSuccessfullyInstalledPluginsIds([]);
  }

  const filterInstalledPlugins = (plugin: AvailablePlugin) => {
    return installedPlugins.find(installedPlugin => {
      return installedPlugin.name === plugin.name
        && installedPlugin.pluginType === plugin.pluginType;
    }) === undefined;
  }

  const installPlugin = (pluginType: string, pluginName: string, pluginVersion: string) => {
    const options = {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({plugin_type: pluginType, name: pluginName, version: pluginVersion})
    };
    return authComponent.authFetch('/api/install-agent-plugin', options , true)
  }

  const onInstallClick = (pluginId: string, pluginName: string, pluginType: string, pluginVersion: string) => {
    setPluginsInInstallationProcess((prevState) => {
      return shallowAdditionOfUniqueValueToArray(prevState, pluginId);
    });

    installPlugin(pluginType, pluginName, pluginVersion).then(() => {
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

  const getRowActions = (row) => {
    const plugin = availablePlugins.find(plugin => plugin.id === row.id);
    if (pluginsInInstallationProcess.includes(plugin.id)) {
      return [
        <GridActionsCellItem
          key={plugin.id}
          icon={<LoadingIcon/>}
          label="Downloading"
          className="textPrimary"
          color="inherit"
        />
      ]
    }

    if (successfullyInstalledPluginsIds.includes(plugin.id)) {
      return [
        <GridActionsCellItem
          key={plugin.id}
          icon={<DownloadDoneIcon/>}
          label="Download Done"
          className="textPrimary"
          color="inherit"
        />
      ]
    }

    return [
      <GridActionsCellItem
        key={plugin.id}
        icon={<FileDownloadIcon/>}
        label="Download"
        className="textPrimary"
        onClick={() => onInstallClick(plugin.id, plugin.name, plugin.pluginType, plugin.version)}
        color="inherit"
      />
    ];
  }

  const onSearchChanged = (query: string) => {
    const filterOnText = (plugin: AvailablePlugin): boolean => {
      for (const field of getSearchableFields(plugin)) {
        if (field.toLowerCase().includes(query.toLowerCase())) {
          return true;
        }
      }
    }
    setFilters((prevState) => {
      return {...prevState, text: filterOnText};
    });
  }

  const installAllSafePlugins = () => {
    setInstallingAllSafePlugins(true);
    for (const plugin of displayedPlugins) {
      if (plugin.safe) {
        onInstallClick(plugin.id, plugin.name, plugin.pluginType, plugin.version);
      }
    }
  }

  const refreshPlugins = () => {
    setIsSpinning(true);
    refreshAvailablePlugins(true).then(() => setIsSpinning(false));
  }

  return (
    <Stack spacing={2} height='100%' id={styles['available-plugins']}>
      <Grid container spacing={2}>
        <Grid xs={4} item
              sx={{alignItems: 'flex-end', display: 'flex'}}>
          <SearchBar setQuery={onSearchChanged} />
        </Grid>
        <Grid xs={3} item >
          <TypeFilter allPlugins={availablePlugins}
                      filters={filters}
                      setFilters={setFilters}
                      className={'type-filter-box'}/>
        </Grid>
        <Grid xs={1} item/>
        <Grid xs={3} item>
          <Box display="flex" justifyContent="flex-end" >
            <Button onClick={installAllSafePlugins} disabled={installingAllSafePlugins}>
              <FileDownloadIcon/> All Safe Plugins
            </Button>
          </Box>
        </Grid>
        <Grid xs={1} item >
          <Button onClick={refreshPlugins}><RefreshIcon className={`${isSpinning && 'spinning-icon'}`}/></Button>
        </Grid>
      </Grid>
      <PluginTable plugins={displayedPlugins}
                   loadingMessage="Loading all available plugins..."
                   onRefreshCallback={onRefreshCallback}
                   getRowActions={getRowActions} />
    </Stack>
  )
};

export default AvailablePlugins;
