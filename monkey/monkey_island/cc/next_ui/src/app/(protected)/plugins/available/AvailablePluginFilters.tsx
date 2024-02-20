import Grid from '@mui/material/Grid';
import React, { useEffect, useMemo, useState } from 'react';
import Box from '@mui/material/Box';
import MonkeyButton, {
    ButtonVariant
} from '@/_components/buttons/MonkeyButton';
import SearchFilter from '@/app/(protected)/plugins/_lib/filters/SearchFilter';
import TypeFilter from '@/app/(protected)/plugins/_lib/filters/TypeFilter';
import InstallAllSafePluginsButton from '@/app/(protected)/plugins/_lib/InstallAllSafePluginsButton';
import RefreshIcon from '@mui/icons-material/Refresh';
import { useGetAvailablePluginsQuery } from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import {
    generatePluginsTableRows,
    PluginRow
} from '@/app/(protected)/plugins/_lib/PluginTable';
import _ from 'lodash';

type AvailablePluginFiltersProps = {
    setDisplayedRowsCallback: (rows: PluginRow[]) => void;
};

export const defaultSearchableColumns = [
    'name',
    'pluginType',
    'version',
    'author'
];

const AvailablePluginFilters = (props: AvailablePluginFiltersProps) => {
    const { setDisplayedRowsCallback } = props;

    const {
        data: availablePlugins,
        error,
        isLoading,
        isError,
        isSuccess
    } = useGetAvailablePluginsQuery();
    // TODO get installed plugins
    const [isSpinning, setIsSpinning] = useState(false);
    const [filters, setFilters] = useState({});

    const allPluginRows: PluginRow[] = useMemo(() => {
        return generatePluginsTableRows(availablePlugins);
    }, [availablePlugins]);

    useEffect(() => {
        if (allPluginRows) {
            const filteredRows = filterRows(allPluginRows);
            setDisplayedRowsCallback(filteredRows);
        }
    }, [allPluginRows]);

    useEffect(() => {
        setDisplayedRowsCallback(filterRows(allPluginRows));
    }, [filters]);

    const filterRows = (rows): PluginRow[] => {
        let filteredRows = _.cloneDeep(rows);
        for (const filter of Object.values(filters)) {
            // @ts-ignore
            filteredRows = filteredRows.filter(filter);
        }
        return filteredRows;
    };

    if (availablePlugins && availablePlugins.length > 0) {
        return (
            <>
                <Grid container spacing={2}>
                    <Grid
                        xs={4}
                        item
                        sx={{ alignItems: 'flex-end', display: 'flex' }}>
                        <SearchFilter
                            setFiltersCallback={setFilters}
                            searchableColumns={defaultSearchableColumns}
                        />
                    </Grid>
                    <Grid
                        xs={3}
                        item
                        sx={{ alignItems: 'flex-end', display: 'flex' }}>
                        <TypeFilter
                            setFiltersCallback={setFilters}
                            allRows={allPluginRows}
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
                            onClick={() => {}}
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
