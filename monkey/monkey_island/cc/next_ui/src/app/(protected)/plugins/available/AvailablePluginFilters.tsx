import Grid from '@mui/material/Grid';
import React, { useMemo, useState } from 'react';
import Box from '@mui/material/Box';
import MonkeyButton, {
    ButtonVariant
} from '@/_components/buttons/MonkeyButton';
import { AgentPlugin } from '@/redux/features/api/agentPlugins/types';
import SearchFilter from '@/app/(protected)/plugins/_lib/filters/SearchFilter';
import TypeFilter from '@/app/(protected)/plugins/_lib/filters/TypeFilter';
import InstallAllSafePluginsButton from '@/app/(protected)/plugins/_lib/InstallAllSafePluginsButton';
import RefreshIcon from '@mui/icons-material/Refresh';
import { useGetAvailablePluginsQuery } from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import {
    generatePluginsTableRows,
    PluginRow
} from '@/app/(protected)/plugins/_lib/PluginTable';

type AvailablePluginFiltersProps = {
    availablePlugins: AgentPlugin[];
    setFiltersCallback: (filters: any) => void;
    pluginInstallationCallback: (pluginId: string) => void;
    refreshPluginsCallback: () => void;
};

export const defaultSearchableColumns = [
    'name',
    'pluginType',
    'version',
    'author'
];

const AvailablePluginFilters = (props: AvailablePluginFiltersProps) => {
    const {
        setFiltersCallback,
        pluginInstallationCallback,
        refreshPluginsCallback
    } = props;

    const {
        data: availablePlugins,
        error,
        isLoading,
        isError,
        isSuccess
    } = useGetAvailablePluginsQuery();
    const [isSpinning, setIsSpinning] = useState(false);
    const availablePluginRows: PluginRow[] = useMemo(() => {
        return generatePluginsTableRows(availablePlugins);
    }, [availablePlugins]);

    if (availablePlugins && availablePlugins.length > 0) {
        return (
            <>
                <Grid container spacing={2}>
                    <Grid
                        xs={4}
                        item
                        sx={{ alignItems: 'flex-end', display: 'flex' }}>
                        <SearchFilter
                            setFilters={setFiltersCallback}
                            searchableColumns={defaultSearchableColumns}
                        />
                    </Grid>
                    <Grid
                        xs={3}
                        item
                        sx={{ alignItems: 'flex-end', display: 'flex' }}>
                        <TypeFilter
                            setFilters={setFiltersCallback}
                            allRows={availablePluginRows}
                        />
                    </Grid>
                    <Grid xs={1} item />
                    <Grid xs={3} item>
                        <Box display="flex" justifyContent="flex-end">
                            <InstallAllSafePluginsButton
                                onInstallClick={() => {}}
                            />
                        </Box>
                    </Grid>
                    <Grid xs={1} item>
                        <MonkeyButton
                            onClick={refreshPluginsCallback}
                            variant={ButtonVariant.Contained}>
                            <RefreshIcon
                                className={`${isSpinning && 'spinning-icon'}`}
                            />
                        </MonkeyButton>
                    </Grid>
                </Grid>
            </>
        );
    }
    return null;
};

export default AvailablePluginFilters;
