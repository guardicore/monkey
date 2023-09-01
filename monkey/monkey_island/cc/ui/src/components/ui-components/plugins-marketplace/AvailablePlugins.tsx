import React, {useContext, useEffect, useState} from 'react';
import {
  shallowAdditionOfUniqueValueToArray,
  shallowRemovalOfUniqueValueFromArray
} from '../../../utils/objectUtils';
import {PluginsContext} from '../../contexts/plugins/PluginsContext';
import {GridActionsCellItem} from '@mui/x-data-grid';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import DownloadDoneIcon from '@mui/icons-material/DownloadDone';
import {Box, Grid} from '@mui/material';
import BasePlugins from './BasePlugins';
import SearchBar from '../SearchBar';
import AuthComponent from '../../AuthComponent';
import {Button} from 'react-bootstrap';
import RefreshIcon from '@mui/icons-material/Refresh';
import '../../../styles/components/plugins-marketplace/AvailablePlugins.scss'
import LoadingIcon from '../LoadingIconMUI';
import TypeFilter from './TypeFilter';

const AvailablePlugins = (props) => {
  const {
    installingAllSafePlugins,
    setInstallingAllSafePlugins,
    successfullyInstalledPluginsIds,
    setSuccessfullyInstalledPluginsIds,
    pluginsInInstallationProcess,
    setPluginsInInstallationProcess
  } = {...props};
  const {availablePlugins, installedPlugins, refreshAvailablePlugins, refreshInstalledPlugins} = useContext(PluginsContext);
  const [displayedPlugins, setDisplayedPlugins] = useState([]);
  const [filters, setFilters] = useState({});

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

  const filterInstalledPlugins = (plugin) => {
    return installedPlugins.find(installedPlugin => {
      return installedPlugin.name === plugin.name
        && installedPlugin.pluginType === plugin.pluginType;
    }) === undefined;
  }

  const installPlugin = (pluginType ,pluginName, pluginVersion) => {
    const options = {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({plugin_type: pluginType, name: pluginName, version: pluginVersion})
    };
    return authComponent.authFetch('/api/install-agent-plugin', options , true)
  }

  const onInstallClick = (pluginId, pluginName, pluginType, pluginVersion) => {
    setPluginsInInstallationProcess((prevState) => {
      return shallowAdditionOfUniqueValueToArray(prevState, pluginId);
    });

    installPlugin(pluginType, pluginName, pluginVersion).then(() => {
      setSuccessfullyInstalledPluginsIds((prevState) => {
        return shallowAdditionOfUniqueValueToArray(prevState, pluginId);
      });
      refreshInstalledPlugins();
    }).catch(() => {
      console.log('error installing plugin');
    }).finally(() => {
      setPluginsInInstallationProcess((prevState => {
        return shallowRemovalOfUniqueValueFromArray(prevState, pluginId);
      }));
    });
  };

  const getRowActions = (row) => {
    const pluginId = row.id;
    if (pluginsInInstallationProcess.includes(pluginId)) {
      return [
        <GridActionsCellItem
          key={pluginId}
          icon={<LoadingIcon/>}
          label="Downloading"
          className="textPrimary"
          color="inherit"
        />
      ]
    }

    if (successfullyInstalledPluginsIds.includes(pluginId)) {
      return [
        <GridActionsCellItem
          key={pluginId}
          icon={<DownloadDoneIcon/>}
          label="Download Done"
          className="textPrimary"
          color="inherit"
        />
      ]
    }

    const pluginName = row.name;
    const pluginType = row.type;
    const pluginVersion = row.version;
    return [
      <GridActionsCellItem
        key={pluginId}
        icon={<FileDownloadIcon/>}
        label="Download"
        className="textPrimary"
        onClick={() => onInstallClick(pluginId, pluginName, pluginType, pluginVersion)}
        color="inherit"
      />
    ];
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

  const installAllSafePlugins = () => {
    setInstallingAllSafePlugins(true);
    for (const plugin of displayedPlugins) {
      if (plugin.safe) {
        onInstallClick(plugin.id, plugin.name, plugin.pluginType, plugin.version);
      }
    }
  }

  return (
    <Box>
      <Grid container spacing={2} rowSpacing={1} columnSpacing={2}>
        <Grid xs={4} item>
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
          <Button onClick={() => refreshAvailablePlugins(true)}><RefreshIcon/></Button>
        </Grid>
        <Grid xs={12} item>
          <BasePlugins plugins={displayedPlugins}
                       loadingMessage="Loading all available plugins..."
                       onRefreshCallback={onRefreshCallback}
                       getRowActions={getRowActions} />
        </Grid>
      </Grid>
    </Box>
  )
};

export default AvailablePlugins;
