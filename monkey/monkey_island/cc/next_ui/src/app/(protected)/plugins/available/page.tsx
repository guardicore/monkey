'use client';
import { useGetAvailablePluginsQuery } from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
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
import RefreshIcon from '@mui/icons-material/Refresh';
import PluginInstallationButton from '@/app/(protected)/plugins/available/PluginInstallationButton';

export default function AvailablePluginsPage() {
    const {
        data: availablePlugins,
        isLoading: isLoadingAvailablePlugins,
        isError
    } = useGetAvailablePluginsQuery();
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
                <Grid item xs={7} md={6}>
                    <AvailablePluginFilters
                        setDisplayedRowsCallback={setDisplayedRows}
                        setIsFilteringCallback={setIsLoadingRows}
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
                loading={isLoadingRows || isLoadingRows}
                noRowsOverlayMessage={getOverlayMessage()}
            />
        </Stack>
    );
}
