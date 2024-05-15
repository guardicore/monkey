'use client';
import {
    useGetAvailablePluginsQuery,
    useGetInstalledPluginsQuery
} from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import React from 'react';
import Stack from '@mui/material/Stack';
import PluginTable, {
    generatePluginsTableColumns,
    PluginRow
} from '@/app/(protected)/plugins/_lib/PluginTable';
import AvailablePluginFilters from '@/app/(protected)/plugins/available/AvailablePluginFilters';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import InstallAllSafePluginsButton from '@/app/(protected)/plugins/_lib/InstallAllSafePluginsButton';
import MonkeyButton, {
    ButtonVariant
} from '@/_components/buttons/MonkeyButton';
import PluginInstallationButton from '@/app/(protected)/plugins/available/PluginInstallationButton';
import MonkeyRefreshIcon from '@/_components/icons/MonkeyRefreshIcon';

export default function AvailablePluginsPage() {
    const {
        data: availablePlugins,
        isLoading: isLoadingAvailablePlugins,
        isError,
        refetch: refreshAvailablePlugins,
        isFetching: isFetchingAvailablePlugins
    } = useGetAvailablePluginsQuery();
    const {
        refetch: refreshInstalledPlugins,
        isFetching: isFetchingInstalledPlugins
    } = useGetInstalledPluginsQuery();
    const [displayedRows, setDisplayedRows] = React.useState<PluginRow[]>([]);
    const [isLoadingRows, setIsLoadingRows] = React.useState(false);

    const getRowActions = (row) => {
        const plugin = availablePlugins?.find((plugin) => plugin.id === row.id);
        if (!plugin) return [];

        return [
            <PluginInstallationButton
                key={plugin.id}
                pluginType={plugin.pluginType}
                pluginName={plugin.name}
                pluginVersion={plugin.version}
                pluginId={plugin.id}
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

    return (
        <Stack spacing={2}>
            <Grid container spacing={2}>
                <Grid item xs={7} md={6} sm={5} lg={3}>
                    <AvailablePluginFilters
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
                    <Grid container spacing={2}>
                        <Grid
                            item
                            xs={10}
                            md={8}
                            lg={11}
                            sx={{ textAlign: 'right' }}>
                            <Box sx={{ mr: '10px' }}>
                                <InstallAllSafePluginsButton />
                            </Box>
                        </Grid>
                        <Grid item xs={2} md={4} lg={1}>
                            <MonkeyButton
                                onClick={() => {
                                    refreshAvailablePlugins();
                                    refreshInstalledPlugins();
                                }}
                                variant={ButtonVariant.Contained}>
                                <MonkeyRefreshIcon
                                    isSpinning={isFetchingAvailablePlugins}
                                />
                            </MonkeyButton>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
            <PluginTable
                rows={displayedRows}
                columns={generatePluginsTableColumns(getRowActions)}
                loading={
                    isFetchingAvailablePlugins ||
                    isLoadingRows ||
                    isFetchingInstalledPlugins
                }
                noRowsOverlayMessage={getOverlayMessage()}
            />
        </Stack>
    );
}
