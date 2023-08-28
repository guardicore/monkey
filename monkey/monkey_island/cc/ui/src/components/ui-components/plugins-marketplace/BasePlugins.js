import React, {useMemo, useState} from 'react';
import {Box} from '@mui/material';
import XDataGrid from '../XDataGrid';
import styles from '../../../styles/components/plugins-marketplace/BasePlugins.module.scss';
import {generatePluginId} from './utils';

const DEFAULT_LOADING_MESSAGE = 'Loading plugins...';
const initialState = {
  sorting: {
    sortModel: [{field: 'name', sort: 'asc'}]
  }
};

const HEADER_SUFFIX = '--header';

const getPluginsGridHeaders = (getRowActions) => [
  {headerName: 'Name', field: 'name', sortable: true, filterable: false, flex: 0.4, minWidth: 150, isTextual: true},
  {headerName: 'Version', field: 'version', sortable: false, filterable: false, flex: 0.1, minWidth: 100, isTextual: true},
  {headerName: 'Type', field: 'type', sortable: true, filterable: false, flex: 0.2, minWidth: 150, isTextual: true},
  {headerName: 'Author', field: 'author', sortable: true, filterable: false, minWidth: 150, flex: 0.25, isTextual: true},
  {headerName: 'Description', field: 'description', sortable: false, filterable: false, minWidth: 150, flex: 1, isTextual: true},
  {
    headerName: '',
    field: 'row_actions',
    type: 'actions',
    minWidth: 100,
    flex: 0.1,
    flexValue: 0.5,
    headerClassName: `row-actions${HEADER_SUFFIX}`,
    cellClassName: `row-actions`,
    getActions: (params) => {
      return getRowActions(params.row);
    }
  }
]


export const getPluginsGridRows = (pluginsList) => {
  const plugins = pluginsList?.map((pluginObject) => {
    const {name, version, type_, plugin_type, author, description} = {...pluginObject};
    return {
      id: generatePluginId(pluginObject),
      name: name,
      version: version,
      type: type_ || plugin_type,
      author: author,
      description: description
    }
  })

  return plugins || [];
}


const BasePlugins = (props) => {
  const {plugins, getRowActions, loadingMessage = DEFAULT_LOADING_MESSAGE} = {...props};

  const [isLoadingPlugins] = useState(false);

  const rows = useMemo(() => {
    return getPluginsGridRows(plugins);
  }, [plugins]);


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