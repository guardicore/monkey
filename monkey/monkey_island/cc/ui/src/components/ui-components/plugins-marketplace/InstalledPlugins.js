import React, {useContext, useState} from 'react';
import {PluginsContext} from '../../contexts/plugins/PluginsContext';
import {shallowAdditionOfUniqueValueToArray, shallowRemovalOfUniqueValueFromArray} from '../../../utils/objectUtils';
import {installPlugin, uninstallPlugin} from './mocksHelper';
import {GridActionsCellItem} from '@mui/x-data-grid';
import {nanoid} from 'nanoid';
import DownloadingIcon from '@mui/icons-material/Downloading';
import DownloadDoneIcon from '@mui/icons-material/DownloadDone';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import BasePlugins from './BasePlugins';

const InstalledPlugins = () => {
  const {installedPlugins, setInstalledPlugins} = useContext(PluginsContext);

  const [successfullyUninstalledPluginsIds, setSuccessfullyUninstalledPluginsIds] = useState([]);
  const [pluginsInUninstallProcess, setPluginsInUninstallProcess] = useState([]);

  const onRefreshCallback = () => {
    setSuccessfullyUninstalledPluginsIds([]);
  }

  const onUninstallClick = (pluginId) => {
    setPluginsInUninstallProcess((prevState) => {
      return shallowAdditionOfUniqueValueToArray(prevState, pluginId);
    });

    uninstallPlugin(pluginId).then(() => {
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
  };

  const getRowActions = (pluginId) => {
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

    return [
      <GridActionsCellItem
        key={nanoid()}
        icon={<FileDownloadIcon/>}
        label="Download"
        className="textPrimary"
        onClick={() => onUninstallClick(pluginId)}
        color="inherit"
      />
    ];
  }

  return (
    <BasePlugins plugins={installedPlugins}
                 setPlugins={setInstalledPlugins}
                 loadingMessage="Loading all available plugins..."
                 onRefreshCallback={onRefreshCallback}
                 getRowActions={getRowActions}
    />
  )
};

export default InstalledPlugins;
