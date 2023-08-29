import React, {useContext, useEffect, useState} from 'react';
import {
  shallowAdditionOfUniqueValueToArray,
  shallowRemovalOfUniqueValueFromArray
} from '../../../utils/objectUtils';
import {PluginsContext} from './PluginsContext';
import {GridActionsCellItem} from '@mui/x-data-grid';
import {nanoid} from 'nanoid';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import DownloadDoneIcon from '@mui/icons-material/DownloadDone';
import BasePlugins from './BasePlugins';
import SearchBar from '../SearchBar';
import {Box} from '@mui/material';
import AuthComponent from '../../AuthComponent';
import { Button, Col, Row } from 'react-bootstrap';
import RefreshIcon from '@mui/icons-material/Refresh';
import {generatePluginId, installedPluginsToArray, pluginIndexToArray} from './utils';
import '../../../styles/components/plugins-marketplace/AvailablePlugins.scss'
import LoadingIcon from '../LoadingIconMUI';


const AvailablePlugins = () => {
  const {availablePlugins} = useContext(PluginsContext);
  const {installedPlugins} = useContext(PluginsContext);
  const {refreshAvailablePlugins} = useContext(PluginsContext);
  const {refreshInstalledPlugins} = useContext(PluginsContext);
  const [displayedPlugins, setDisplayedPlugins] = useState([]);

  const [successfullyInstalledPluginsIds, setSuccessfullyInstalledPluginsIds] = useState([]);
  const [pluginsInInstallationProcess, setPluginsInInstallationProcess] = useState([]);
  const authComponent = new AuthComponent({});

  useEffect(() => {
    let installedPluginsIds = installedPluginsToArray(installedPlugins).map(generatePluginId);
    const installedFilter = (plugin) => !installedPluginsIds.includes(generatePluginId(plugin));
    let shownPlugins = pluginIndexToArray(availablePlugins).filter(installedFilter)
    setDisplayedPlugins(shownPlugins);
  }, [installedPlugins, availablePlugins]);

  const onRefreshCallback = () => {
    setSuccessfullyInstalledPluginsIds([]);
  }

  const onInstallClick = (pluginId, pluginName, pluginType, pluginVersion) => {
    console.log('installing plugin: ', pluginName)

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
      <Row className='grid-tools'>
        <Col>
          <SearchBar />
        </Col>
        <Col className='actions'>
          <Button onClick={() => refreshAvailablePlugins(true)}><RefreshIcon/></Button>
        </Col>
      </Row>
      <BasePlugins plugins={displayedPlugins}
                   loadingMessage="Loading all available plugins..."
                   onRefreshCallback={onRefreshCallback}
                   getRowActions={getRowActions}
      />
    </Box>
  )
};

export default AvailablePlugins;
