import React, {useContext, useEffect, useMemo, useState} from 'react';
import {
  shallowAdditionOfUniqueValueToArray,
  shallowRemovalOfUniqueValueFromArray
} from '../../../utils/objectUtils';
import {
  AvailablePlugin,
  InstalledPlugin,
  PluginsContext
} from '../../contexts/plugins/PluginsContext';
import {GridActionsCellItem} from '@mui/x-data-grid';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import DownloadDoneIcon from '@mui/icons-material/DownloadDone';
import {Box, Grid, Stack} from '@mui/material';
import PluginTable, {
  generatePluginsTableColumns,
  generatePluginsTableRows, PluginRow,
} from './PluginTable';
import AuthComponent from '../../AuthComponent';
import {Button} from 'react-bootstrap';
import RefreshIcon from '@mui/icons-material/Refresh';
import styles from '../../../styles/components/plugins-marketplace/AvailablePlugins.module.scss';
import LoadingIcon from '../LoadingIconMUI';
import TypeFilter from './TypeFilter';
import SearchFilter, {defaultSearchableColumns} from './SearchFilter';
import IslandHttpClient, { APIEndpoint } from '../../IslandHttpClient';
import InstallAllSafePluginsButton from './InstallAllSafePluginsButton';


type AvailablePluginRowArray = PluginRow[];

export const isPluginInstalled = (availablePlugin :AvailablePlugin,
                                  installedPlugins :InstalledPlugin[]) => {
  return ! (installedPlugins.find(installedPlugin => {
      return installedPlugin.name === availablePlugin.name
        && installedPlugin.pluginType === availablePlugin.pluginType;
    }) === undefined);
}

const NO_AVAILABLE_PLUGINS_MESSAGE = 'There are no available plugins to be installed';
const FETCHING_ERROR_MESSAGE = 'Couldn\'t fetch available plugins, check your internet connection and try again';

const AvailablePlugins = (props) => {
  const {
    successfullyInstalledPluginsIds,
    setSuccessfullyInstalledPluginsIds,
    pluginsInInstallationProcess,
    setPluginsInInstallationProcess
  } = {...props};
  const {availablePlugins, installedPlugins,
    refreshAvailablePlugins, refreshInstalledPlugins, refreshAvailablePluginsFailure} = useContext(PluginsContext);
  const [displayedRows, setDisplayedRows] = useState<AvailablePluginRowArray>([]);
  const [filters, setFilters] = useState({});
  const [isSpinning, setIsSpinning] = useState(false);

  const authComponent = new AuthComponent({});

  const availablePluginRows :PluginRow[] = useMemo(() => {
    return generatePluginsTableRows(availablePlugins);
  }, [availablePlugins]);

  useEffect(() => {
    setDisplayedRows(availablePluginRows);
    setFilters((prevState) => {
      return {...prevState, installed: filterInstalledPlugins};
    });
  }, []);

  useEffect(() => {
    filterRows();
  }, [availablePlugins, installedPlugins, filters]);

  useEffect(() => {
    setFilters((prevState) => {
      return {...prevState, installed: filterInstalledPlugins};
    });
  }, [installedPlugins]);

  const filterRows = () => {
    let allRows = availablePluginRows;
    for (const filter of Object.values(filters)) {
      allRows = allRows.filter(filter);
    }
    setDisplayedRows(allRows);
  }

  const filterInstalledPlugins = (row: PluginRow) => {
    let availablePlugin = availablePlugins.find(availablePlugin => row.id === availablePlugin.id);
    return !isPluginInstalled(availablePlugin, installedPlugins) ||
      successfullyInstalledPluginsIds.includes(row.id);
  }

  const installPlugin = (pluginType: string, pluginName: string, pluginVersion: string) => {
    let contents = {plugin_type: pluginType, name: pluginName, version: pluginVersion};
    return IslandHttpClient.putJSON(APIEndpoint.installAgentPlugin, contents, true)
  }

  const onInstallClick = (pluginId: string, pluginName: string,
                          pluginType: string, pluginVersion: string) => {
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
      setPluginsInInstallationProcess((prevState) => {
        return shallowRemovalOfUniqueValueFromArray(prevState, pluginId);
      });
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

  const refreshPlugins = () => {
    setIsSpinning(true);
    refreshAvailablePlugins(true).then(() => setIsSpinning(false));
  }

  const renderFilters = () => {
    if (availablePlugins?.length > 0) {
      return (
        <>
          <Grid container spacing={2}>
            <Grid xs={4} item
                  sx={{alignItems: 'flex-end', display: 'flex'}}>
              <SearchFilter setFilters={setFilters}
                            searchableColumns={defaultSearchableColumns}/>
            </Grid>
            <Grid xs={3} item>
              <TypeFilter setFilters={setFilters}
                          allRows={availablePluginRows}/>
            </Grid>
            <Grid xs={1} item/>
            <Grid xs={3} item>
              <Box display="flex" justifyContent="flex-end">
                <InstallAllSafePluginsButton onInstallClick={onInstallClick}
                                         pluginsInInstallationProcess={pluginsInInstallationProcess} />
              </Box>
            </Grid>
            <Grid xs={1} item>
              <Button onClick={refreshPlugins}><RefreshIcon className={`${isSpinning && 'spinning-icon'}`}/></Button>
            </Grid>
          </Grid>
        </>
      )
    }
    return null;
  }

  const getOverlayMessage = () => {
    if(refreshAvailablePluginsFailure) {
      return FETCHING_ERROR_MESSAGE;
    } else if(availablePlugins?.length === 0) {
      return NO_AVAILABLE_PLUGINS_MESSAGE;
    }
    return null;
  }

  return (
    <Stack spacing={2} height='100%' id={styles['available-plugins']}>
      {renderFilters()}
      <PluginTable rows={displayedRows}
                   columns={generatePluginsTableColumns(getRowActions)}
                   loadingMessage="Loading all available plugins..."
                   noRowsOverlayMessage={getOverlayMessage()} />
    </Stack>
  )
};

export default AvailablePlugins;
