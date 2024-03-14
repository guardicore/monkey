'use client';
import { useGetAvailablePluginsQuery } from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import React, { useMemo } from 'react';
import Stack from '@mui/material/Stack';
import PluginTable, {
    generatePluginsTableColumns,
    generatePluginsTableRows,
    PluginRow
} from '@/app/(protected)/plugins/_lib/PluginTable';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import { GridActionsCellItem } from '@mui/x-data-grid';
import AvailablePluginFilters from '@/app/(protected)/plugins/available/AvailablePluginFilters';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import InstallAllSafePluginsButton from '@/app/(protected)/plugins/_lib/InstallAllSafePluginsButton';
import MonkeyButton, {
    ButtonVariant
} from '@/_components/buttons/MonkeyButton';
import RefreshIcon from '@mui/icons-material/Refresh';
import _ from 'lodash';

export default function AvailablePluginsPage() {
    const {
        data: availablePlugins,
        isLoading: isLoadingAvailablePlugins,
        isError
    } = useGetAvailablePluginsQuery();
    const [displayedRows, setDisplayedRows] = React.useState<PluginRow[]>([]);
    const [isLoadingRows, setIsLoadingRows] = React.useState(false);

    const onInstallClick = (
        pluginId: string,
        pluginName: string,
        pluginType: string,
        pluginVersion: string
    ) => {
        console.log(
            'Install plugin',
            pluginId,
            pluginName,
            pluginType,
            pluginVersion
        );
    };

    const getRowActions = (row) => {
        const plugin = availablePlugins?.find((plugin) => plugin.id === row.id);
        if (!plugin) return [];

        return [
            <GridActionsCellItem
                key={plugin.id}
                icon={<FileDownloadIcon />}
                label="Download"
                className="textPrimary"
                onClick={() =>
                    onInstallClick(
                        plugin.id,
                        plugin.name,
                        plugin.pluginType,
                        plugin.version
                    )
                }
                color="inherit"
            />
        ];
    };

    const getOverlayMessage = () => {
        if (isError) {
            return 'Failed to load available plugins';
        }
        if (isLoadingAvailablePlugins) {
            return 'Loading all available plugins...';
        }
        return 'No available plugins';
    };

    const filterRows = (rows: PluginRow[], filters: any): PluginRow[] => {
        let filteredRows = _.cloneDeep(rows);
        for (const filter of Object.values(filters)) {
            // @ts-ignore
            filteredRows = filteredRows.filter(filter);
        }
        return filteredRows;
    };

    const allPluginRows: PluginRow[] = useMemo(() => {
        if (!availablePlugins) return [];
        const rows = generatePluginsTableRows(availablePlugins);
        return rows;
    }, [availablePlugins]);

    const handleFiltersChanged = (filters: any) => {
        setIsLoadingRows(true);
        const filteredRows = filterRows(allPluginRows, filters);
        setDisplayedRows(filteredRows);
        setIsLoadingRows(false);
    };

    return (
        <Stack spacing={2}>
            <Grid container spacing={2}>
                <Grid item xs={7} md={6}>
                    {availablePlugins && availablePlugins.length > 0 ? (
                        <AvailablePluginFilters
                            allPluginRows={allPluginRows}
                            filtersChanged={handleFiltersChanged}
                        />
                    ) : null}
                </Grid>
                <Grid item justifyContent={'flex-end'} xs={5} md={4} lg={5}>
                    <Box
                        display="flex"
                        justifyContent="flex-end"
                        sx={{ mr: '10px' }}>
                        <InstallAllSafePluginsButton
                            onInstallClick={() => {}}
                            pluginsInInstallationProcess={[]}
                        />
                    </Box>
                </Grid>
                <Grid item xs={1} md={2} lg={1}>
                    <MonkeyButton
                        onClick={() => {}}
                        variant={ButtonVariant.Contained}>
                        <RefreshIcon />
                    </MonkeyButton>
                </Grid>
            </Grid>
            <PluginTable
                rows={displayedRows}
                columns={generatePluginsTableColumns(getRowActions)}
                loading={isLoadingRows || isLoadingRows}
                noRowsOverlayMessage={getOverlayMessage()}
            />
        </Stack>
    );
}
