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
            <AvailablePluginFilters
                setDisplayedRowsCallback={setDisplayedRows}
                setIsFilteringCallback={setIsFiltering}
            />
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
