import React, {useContext, useEffect, useMemo, useState} from 'react';
import {
  shallowAdditionOfUniqueValueToArray,
  shallowRemovalOfUniqueValueFromArray
} from '../../../utils/objectUtils';
import {PluginsContext} from '../../contexts/plugins/PluginsContext';
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


type AvailablePluginRowArray = PluginRow[];

const CONNECTION_ERROR_MESSAGE = 'An error occurred while retrieving the available plugins';

const AvailablePlugins = (props) => {
  const {
    installingAllSafePlugins,
    setInstallingAllSafePlugins,
    successfullyInstalledPluginsIds,
    setSuccessfullyInstalledPluginsIds,
    pluginsInInstallationProcess,
    setPluginsInInstallationProcess
  } = {...props};
  const {availablePlugins, installedPlugins, refreshAvailablePlugins, refreshAvailablePluginsFailure} = useContext(PluginsContext);
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

  useEffect(() =>{
    disableInstallAllSafePlugins()
  }, [displayedRows]);

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

  //TODO refactor this method
  const disableInstallAllSafePlugins = () => {
    let unSafeDispalyedPlugins = [];
    let safeDispalyedPlugins = [];
    for (const plugin of displayedRows) {
      if (!plugin.safe) {
        unSafeDispalyedPlugins.push(plugin.name);
      } else {
        safeDispalyedPlugins.push(plugin.name);
      }
    }
    setInstallingAllSafePlugins(unSafeDispalyedPlugins.length > 0 && safeDispalyedPlugins.length === 0 || displayedRows.length === 0)
  }

  const filterInstalledPlugins = (row: PluginRow) => {
    let availablePlugin = availablePlugins.find(availablePlugin => row.id === availablePlugin.id);
    return installedPlugins.find(installedPlugin => {
      return installedPlugin.name === availablePlugin.name
        && installedPlugin.pluginType === availablePlugin.pluginType;
    }) === undefined;
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

  const installAllSafePlugins = () => {
    setInstallingAllSafePlugins(true);
    for (const row of availablePluginRows) {
      if (row.safe) {
        onInstallClick(row.id, row.name, row.pluginType, row.version);
      }
    }
  }

  const refreshPlugins = () => {
    setIsSpinning(true);
    refreshAvailablePlugins(true).then(() => setIsSpinning(false));
  }

  return (
    <Stack spacing={2} height='100%' id={styles['available-plugins']}>
      {availablePlugins?.length > 0 && (
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
              <Button onClick={installAllSafePlugins} disabled={installingAllSafePlugins}>
                <FileDownloadIcon/> All Safe Plugins
              </Button>
            </Box>
          </Grid>
          <Grid xs={1} item>
            <Button onClick={refreshPlugins}><RefreshIcon className={`${isSpinning && 'spinning-icon'}`}/></Button>
          </Grid>
        </Grid>
      )}
      <PluginTable rows={displayedRows}
                   columns={generatePluginsTableColumns(getRowActions)}
                   loadingMessage="Loading all available plugins..."
                   noRowsOverlayMessage={refreshAvailablePluginsFailure && CONNECTION_ERROR_MESSAGE} />
    </Stack>
  )
};

export default AvailablePlugins;
