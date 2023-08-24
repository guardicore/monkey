import React, {useEffect, useMemo, useState} from 'react';
import {Box} from '@mui/material';
import XDataGrid from '../XDataGrid';
import {getPlugins, getPluginsGridHeaders, getPluginsGridRows} from './mocksHelper';
import styles from '../../../styles/components/plugins-marketplace/BasePlugins.module.scss';

const DEFAULT_LOADING_MESSAGE = 'Loading plugins...';
const initialState = {
  sorting: {
    sortModel: [{field: 'name', sort: 'asc'}]
  }
};

const BasePlugins = (props) => {
  const {plugins, setPlugins, getRowActions, onRefreshCallback, loadingMessage = DEFAULT_LOADING_MESSAGE} = {...props};

  const [isLoadingPlugins, setIsLoadingPlugins] = useState(false);

  useEffect(() => {
    setPluginsList();
  }, []);

  const rows = useMemo(() => {
    return getPluginsGridRows(plugins);
  }, [plugins]);

  const setPluginsList = () => {
    if(plugins.length === 0) {
      setIsLoadingPlugins(true);
      getPlugins(false, false, true).then(plugins => {
        setPlugins(plugins);
      }).finally(() => {
        setIsLoadingPlugins(false);
      });
    }
  };

  // eslint-disable-next-line no-unused-vars
  const onRefreshClick = () => {
    setPluginsList();
    if(onRefreshCallback) {
      onRefreshCallback();
    }
  }

  return (
    <Box className={styles['plugins-wrapper']}>
      {/*<PluginsActions showUpgradableToggle={showUpgradableToggle}/>*/}

       {isLoadingPlugins
        ? loadingMessage
        : <XDataGrid columns={getPluginsGridHeaders(getRowActions)}
                     rows={[...rows]}
                     rowHeight={'25px'}
                     showToolbar={false}
                     maxHeight={'500px'}
                     className="marketplace-plugins-list"
                     initialState={initialState}
                     needCustomWorkaround={false}
                     setFlex={false}/>
      }
    </Box>
  )
}

export default BasePlugins;
