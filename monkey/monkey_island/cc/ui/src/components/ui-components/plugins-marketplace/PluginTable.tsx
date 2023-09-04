import React, {useMemo, useState} from 'react';
import {Box} from '@mui/material';
import XDataGrid from '../XDataGrid';
import HealthAndSafetyOutlinedIcon from '@mui/icons-material/HealthAndSafetyOutlined';
import WarningAmberOutlinedIcon from '@mui/icons-material/WarningAmberOutlined';
import styles from '../../../styles/components/plugins-marketplace/BasePlugins.module.scss';
import {AgentPlugin} from '../../contexts/plugins/PluginsContext';
import _ from 'lodash';
import MonkeyTooltip from '../MonkeyTooltip';

const DEFAULT_LOADING_MESSAGE = 'Loading plugins...';
const initialState = {
  sorting: {
    sortModel: [{field: 'name', sort: 'asc'}]
  }
};

const HEADER_SUFFIX = '--header';

const getPluginsTableHeaders = (getRowActions) => [
  {headerName: 'Name', field: 'name', sortable: true, filterable: false, flex: 0.4, minWidth: 150, isTextual: true},
  {headerName: 'Version', field: 'version', sortable: false, filterable: false, flex: 0.1, minWidth: 100, isTextual: true},
  {headerName: 'Type', field: 'type', sortable: true, filterable: false, flex: 0.2, minWidth: 150, isTextual: true},
  {headerName: 'Author', field: 'author', sortable: true, filterable: false, minWidth: 150, flex: 0.25, isTextual: true},
  {headerName: 'Description', field: 'description', sortable: false, filterable: false, minWidth: 150, flex: 1, isTextual: true},
  {headerName: 'Safety', field: 'safe', sortable: true, filterable: false, flex: 0.1, minWidth: 100, renderCell: renderSafetyCell},
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

const renderSafetyCell = (params) => {
  const SAFE = 'Safe', UNSAFE = 'Unsafe';
  return (
    <div style={{display: 'flex', alignItems: 'center'}}>
      <MonkeyTooltip title={params.value ? SAFE : UNSAFE}>
        {params.value ? (
          <HealthAndSafetyOutlinedIcon style={{color: 'green'}}/>
        ) : (
          <WarningAmberOutlinedIcon style={{color: 'red'}}/>
        )}
      </MonkeyTooltip>
    </div>
  );
}


export const getPluginsTableRows = (pluginsList :AgentPlugin[]) => {
  const plugins = pluginsList?.map((pluginObject) => {
    const {id, name, safe, version, pluginType, description} = {...pluginObject};
    return {
      id: id,
      name: name,
      safe: safe,
      version: version,
      type: _.startCase(pluginType),
      author: "Akamai",
      description: description,
    }
  })

  return plugins || [];
}


const PluginTable = (props) => {
  const {plugins, getRowActions, loadingMessage = DEFAULT_LOADING_MESSAGE} = {...props};

  const [isLoadingPlugins] = useState(false);

  const rows = useMemo(() => {
    return getPluginsTableRows(plugins);
  }, [plugins]);


  return (
    <Box className={styles['plugins-wrapper']} minHeight={0}>
      {/*<PluginsActions showUpgradableToggle={showUpgradableToggle}/>*/}

       {isLoadingPlugins
        ? loadingMessage
        : <XDataGrid columns={getPluginsTableHeaders(getRowActions)}
                     rows={[...rows]}
                     rowHeight={'25px'}
                     showToolbar={false}
                     height={'100%'}
                     minHeight={0}
                     className="marketplace-plugins-list"
                     initialState={initialState}
                     needCustomWorkaround={false}
                     setFlex={false}/>
      }
    </Box>
  )
}

export default PluginTable;
