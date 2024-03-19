'use client';
import { useGetInstalledPluginsQuery } from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import React from 'react';
import Stack from '@mui/material/Stack';
import PluginTable, {
    generatePluginsTableColumns,
    PluginRow
} from '@/app/(protected)/plugins/_lib/PluginTable';
import Grid from '@mui/material/Grid';
import { InstalledPlugin } from '@/redux/features/api/agentPlugins/types';
import InstalledPluginFilters from '@/app/(protected)/plugins/installed/InstalledPluginFilters';

export default function InstalledPluginsPage() {
    const {
        data: installedPlugins,
        isLoading: isLoadingInstalledPlugins,
        isError: isInstalledPluginsError
    } = useGetInstalledPluginsQuery();
    const [displayedRows, setDisplayedRows] = React.useState<PluginRow[]>([]);
    const [isLoadingRows, setIsLoadingRows] = React.useState(false);

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const getUpgradeAction = (plugin: InstalledPlugin) => {
        return [];
    };

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const getUninstallAction = (plugin: InstalledPlugin) => {
        return [];
    };

    const getRowActions = (row: PluginRow) => {
        if (!installedPlugins) return [];
        const plugin = installedPlugins.find(
            (installedPlugin) => installedPlugin.id === row.id
        );
        if (!plugin) return [];
        return [...getUpgradeAction(plugin), ...getUninstallAction(plugin)];
    };

    const getOverlayMessage = () => {
        if (isInstalledPluginsError) {
            return 'Failed to load installed plugins';
        }
        if (isLoadingInstalledPlugins) {
            return 'Loading all installed plugins...';
        }
        return 'No installed plugins';
    };

    return (
        <Stack spacing={2}>
            <Grid container spacing={2}>
                <Grid item xs={7} md={6} sm={5} lg={3}>
                    <InstalledPluginFilters
                        setDisplayedRowsCallback={setDisplayedRows}
                        setIsFilteringCallback={setIsLoadingRows}
                    />
                </Grid>
                <Grid
                    item
                    xs={5}
                    md={6}
                    sm={7}
                    lg={9}
                    sx={{ alignItems: 'flex-end', display: 'flex' }}>
                    <Grid container spacing={2}></Grid>
                </Grid>
            </Grid>
            <PluginTable
                rows={displayedRows}
                columns={generatePluginsTableColumns(getRowActions)}
                loading={isLoadingRows}
                noRowsOverlayMessage={getOverlayMessage()}
            />
        </Stack>
    );
}
