import React, { useEffect, useRef, useState } from 'react';
import MonkeyDataGrid, {
    MonkeyDataGridProps
} from '../../../../_components/tables/MonkeyDataGrid';
import HealthAndSafetyOutlinedIcon from '@mui/icons-material/HealthAndSafetyOutlined';
import WarningAmberOutlinedIcon from '@mui/icons-material/WarningAmberOutlined';
import _ from 'lodash';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import { AgentPlugin } from '@/redux/features/api/agentPlugins/types';
import { Typography } from '@mui/material';
import Box from '@mui/material/Box';
import MonkeyTooltip from '@/_components/tooltips/MonkeyTooltip';
import MonkeyButton from '@/_components/buttons/MonkeyButton';
import LoadingIcon from '@/_components/icons/loading-icon/LoadingIcon';
import { GridAlignment } from '@mui/x-data-grid';

const HEADER_SUFFIX = '--header';

const initialState = {
    sorting: {
        sortModel: [{ field: 'name', sort: 'asc' }]
    }
};

type getRowActionsType = (plugin: PluginRow) => any[];

export const generatePluginsTableColumns = (
    getRowActions: getRowActionsType
) => [
    {
        headerName: 'Name',
        field: 'name',
        sortable: true,
        filterable: false,
        flex: 0.2,
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
        renderCell: DescriptionCell
    },
    {
        headerName: 'Safety',
        field: 'safe',
        headerAlign: 'center' as GridAlignment,
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
];

const renderSafetyCell = (params) => {
    const SAFE = 'Safe',
        UNSAFE = 'Unsafe';
    return (
        <div
            style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '100%'
            }}>
            <MonkeyTooltip title={params.value ? SAFE : UNSAFE}>
                {params.value ? (
                    <HealthAndSafetyOutlinedIcon style={{ color: 'green' }} />
                ) : (
                    <WarningAmberOutlinedIcon style={{ color: 'red' }} />
                )}
            </MonkeyTooltip>
        </div>
    );
};

const DescriptionCell = (params) => {
    const ref = useRef(null);
    const [isOverflowing, setIsOverflowing] = useState(false);
    const [isExpanded, setIsExpanded] = useState(false);

    useEffect(() => {
        if (ref.current) {
            setIsOverflowing(
                ref.current['scrollWidth'] > params.colDef.computedWidth
            );
        }
    }, [ref]);

    return (
        <>
            <Typography noWrap={!isExpanded} ref={ref}>
                {params.value}
            </Typography>
            {isOverflowing && (
                <MonkeyButton onClick={() => setIsExpanded(!isExpanded)}>
                    {isExpanded ? <ExpandLess /> : <ExpandMore />}
                </MonkeyButton>
            )}
        </>
    );
};

export type PluginRow = AgentPlugin;

export const generatePluginsTableRows = (
    pluginsList: AgentPlugin[]
): PluginRow[] => {
    const plugins = pluginsList?.map((pluginObject) => {
        const { id, name, safe, version, pluginType, description } = {
            ...pluginObject
        };
        return {
            id: id,
            name: name,
            safe: safe,
            version: version,
            pluginType: _.startCase(pluginType),
            description: description
        };
    });

    return plugins || [];
};

type PluginTableProps = MonkeyDataGridProps & {
    rows?: PluginRow[];
    columns?: any[];
    loading?: boolean;
};

const PluginTable = (props: PluginTableProps) => {
    const { rows = [], columns = [], loading = false, ...rest } = { ...props };

    return (
        <Box>
            {loading ? (
                <Box sx={{ textAlign: 'center' }}>
                    <LoadingIcon sx={{ height: '50px', width: '50px' }} />
                </Box>
            ) : (
                <MonkeyDataGrid
                    columns={columns}
                    rows={[...rows]}
                    showToolbar={false}
                    className="marketplace-plugins-list"
                    initialState={initialState}
                    needCustomWorkaround={false}
                    setFlex={false}
                    {...rest}
                />
            )}
        </Box>
    );
};

export default PluginTable;
