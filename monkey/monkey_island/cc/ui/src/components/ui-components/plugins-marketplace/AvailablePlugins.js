import React, {useContext, useEffect, useState} from 'react';
import {
  shallowAdditionOfUniqueValueToArray,
  shallowRemovalOfUniqueValueFromArray
} from '../../../utils/objectUtils';
import {PluginsContext} from '../../contexts/plugins/PluginsContext';
import {GridActionsCellItem} from '@mui/x-data-grid';
import {nanoid} from 'nanoid';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import DownloadDoneIcon from '@mui/icons-material/DownloadDone';
import {Box, Grid} from '@mui/material';
import BasePlugins from './BasePlugins';
import SearchBar from '../SearchBar';
import AuthComponent from '../../AuthComponent';
import {Button} from 'react-bootstrap';
import RefreshIcon from '@mui/icons-material/Refresh';
import _ from 'lodash';
import {generatePluginId, installedPluginsToArray, pluginIndexToArray} from './utils';
import '../../../styles/components/plugins-marketplace/AvailablePlugins.scss'
import LoadingIcon from '../LoadingIconMUI';
import TypeFilter from './TypeFilter';


const AvailablePlugins = () => {
  const {availablePlugins, installedPlugins, refreshAvailablePlugins, refreshInstalledPlugins} = useContext(PluginsContext);
  const [displayedPlugins, setDisplayedPlugins] = useState([]);

  const [availablePluginsArray, setAvailablePluginsArray] = useState([]);
  const [installedPluginsArray, setInstalledPluginsArray] = useState([]);
  const [successfullyInstalledPluginsIds, setSuccessfullyInstalledPluginsIds] = useState([]);
  const [pluginsInInstallationProcess, setPluginsInInstallationProcess] = useState([]);
  const authComponent = new AuthComponent({});

  useEffect(() => {
    setAvailablePluginsArray(pluginIndexToArray(availablePlugins))
  }, [availablePlugins]);

  useEffect(() => {
    setInstalledPluginsArray(installedPluginsToArray(installedPlugins));
  }, [installedPlugins]);

  useEffect(() => {
    setDisplayedPlugins(availablePluginsArray)
  }, [installedPluginsArray, availablePluginsArray]);

  useEffect(() => {
    let installedPluginsIds = installedPluginsArray.map(generatePluginId);
    const installedFilter = (plugin) => !installedPluginsIds.includes(generatePluginId(plugin));
    let shownPlugins = displayedPlugins.filter(installedFilter)
    if(!_.isEqual(displayedPlugins, shownPlugins)){
      setDisplayedPlugins(shownPlugins);
    }
  }, [displayedPlugins]);

  const onRefreshCallback = () => {
    setSuccessfullyInstalledPluginsIds([]);
  }

  const onInstallClick = (pluginId, pluginName, pluginType, pluginVersion) => {
    setPluginsInInstallationProcess((prevState) => {
      return shallowAdditionOfUniqueValueToArray(prevState, pluginId);
    });

    authComponent.authFetch('/api/install-agent-plugin', {method: 'PUT', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({plugin_type: pluginType, name: pluginName, version: pluginVersion})}, true).then(() => {
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
          key={nanoid()}
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
    const pluginVersion = row.version;
    return [
      <GridActionsCellItem
        key={nanoid()}
        icon={<FileDownloadIcon/>}
        label="Download"
        className="textPrimary"
        onClick={() => onInstallClick(pluginId, pluginName, pluginType, pluginVersion)}
        color="inherit"
      />
    ];
  }

  return (
    <Box>
      <Grid container spacing={2} rowSpacing={1} columnSpacing={2}>
        <Grid xs={4} item>
          <SearchBar />
        </Grid>
        <Grid xs={4} item />
        <Grid xs={3} item >
          <TypeFilter allPlugins={availablePluginsArray}
                      displayedPlugins={displayedPlugins}
                      setDisplayedPlugins={setDisplayedPlugins}
                      className={'type-filter-box'}/>
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