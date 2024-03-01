'use client';
import { useGetAvailablePluginsQuery } from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import React from 'react';
import Stack from '@mui/material/Stack';
import PluginTable, {
    generatePluginsTableColumns,
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

export default function AvailablePluginsPage() {
    const {
        data: availablePlugins,
        isLoading,
        isError
    } = useGetAvailablePluginsQuery();
    const [displayedRows, setDisplayedRows] = React.useState<PluginRow[]>([]);
    const [isFiltering, setIsFiltering] = React.useState(false);

    const onInstallClick = (
        pluginId: string,
        pluginName: string,
        pluginType: string,
        pluginVersion: string
    ) => {
        console.log('Install plugin', pluginId);
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
        if (isLoading) {
            return 'Loading all available plugins...';
        }
        return 'No available plugins';
    };

    return (
        <Stack spacing={2}>
            <Grid container spacing={2}>
                <Grid xs={7} md={6}>
                    <AvailablePluginFilters
                        setDisplayedRowsCallback={setDisplayedRows}
                        setIsFilteringCallback={setIsFiltering}
                    />
                </Grid>
                <Grid item justifyContent={'flex-end'} xs={5} md={4} lg={5}>
                    <Box
                        display="flex"
                        justifyContent="flex-end"
                        sx={{ mr: '10px' }}>
                        <InstallAllSafePluginsButton
                            onInstallClick={() => {}}
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
                loadingMessage="Loading all available plugins..."
                loading={isFiltering}
                noRowsOverlayMessage={getOverlayMessage()}
            />
        </Stack>
    );
}
