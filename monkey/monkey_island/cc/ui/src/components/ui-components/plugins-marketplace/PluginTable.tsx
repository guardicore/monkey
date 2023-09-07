import React, {useState} from 'react';
import {Box} from '@mui/material';
import XDataGrid from '../XDataGrid';
import HealthAndSafetyOutlinedIcon from '@mui/icons-material/HealthAndSafetyOutlined';
import WarningAmberOutlinedIcon from '@mui/icons-material/WarningAmberOutlined';
import styles from '../../../styles/components/plugins-marketplace/PluginTable.module.scss';
import {AgentPlugin} from '../../contexts/plugins/PluginsContext';
import _ from 'lodash';
import MonkeyTooltip from '../MonkeyTooltip';


const DEFAULT_LOADING_MESSAGE = 'Loading plugins...';
const HEADER_SUFFIX = '--header';

const initialState = {
  sorting: {
    sortModel: [{field: 'name', sort: 'asc'}]
  }
};


type getRowActionsType = (plugin: PluginRow) => any[];

export const generatePluginsTableColumns = (getRowActions :getRowActionsType) => [
  {
    headerName: 'Name',
    field: 'name',
    sortable: true,
    filterable: false,
    flex: 0.4,
    minWidth: 150,
    isTextual: true
  },
  {
    headerName: 'Version',
    field: 'version',
    sortable: false,
    filterable: false,
    flex: 0.1,
    minWidth: 100,
    isTextual: true
  },
  {
    headerName: 'Type',
    field: 'pluginType',
    sortable: true,
    filterable: false,
    flex: 0.2,
    minWidth: 150,
    isTextual: true
  },
  {
    headerName: 'Description',
    field: 'description',
    sortable: false,
    filterable: false,
    minWidth: 150,
    flex: 1,
    isTextual: true
  },
  {
    headerName: 'Safety',
    field: 'safe',
    sortable: true,
    filterable: false,
    flex: 0.1,
    minWidth: 100,
    renderCell: renderSafetyCell
  },
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
    <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', width: '100%'}}>
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

export type PluginRow = {
  id: string,
  name: string,
  version: string,
  pluginType: string,
  description: string,
  safe: boolean
};

export const generatePluginsTableRows = (pluginsList: AgentPlugin[]) :PluginRow[] => {
  const plugins = pluginsList?.map((pluginObject) => {
    const {id, name, safe, version, pluginType, description} = {...pluginObject};
    return {
      id: id,
      name: name,
      safe: safe,
      version: version,
      pluginType: _.startCase(pluginType),
      description: description,
    }
  })

  return plugins || [];
}

const PluginTable = (props) => {
  const {rows, columns, loadingMessage = DEFAULT_LOADING_MESSAGE, ...rest} = {...props};

  const [isLoadingPlugins] = useState(false);

  return (
    <Box className={styles['plugins-wrapper']} minHeight={0}>
      {isLoadingPlugins
        ? loadingMessage
        : <XDataGrid columns={columns}
                     rows={[...rows]}
                     rowHeight={'25px'}
                     showToolbar={false}
                     height={'100%'}
                     minHeight={0}
                     className="marketplace-plugins-list"
                     initialState={initialState}
                     needCustomWorkaround={false}
                     setFlex={false}
                     {...rest}/>
      }
    </Box>
  )
}

export default PluginTable;
