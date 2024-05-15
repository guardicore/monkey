import Grid from '@mui/material/Grid';
import React, { useEffect, useMemo, useState } from 'react';
import SearchFilter from '@/app/(protected)/plugins/_lib/filters/SearchFilter';
import TypeFilter from '@/app/(protected)/plugins/_lib/filters/TypeFilter';
import { useGetInstalledPluginsQuery } from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import {
    generatePluginsTableRows,
    PluginRow
} from '@/app/(protected)/plugins/_lib/PluginTable';
import _ from 'lodash';

type InstalledPluginFilterProps = {
    setDisplayedRowsCallback: (rows: PluginRow[]) => void;
    setIsFilteringCallback: (isFiltering: boolean) => void;
};

export type FilterProps = {
    setFiltersCallback: (filters: any) => void;
};

export const defaultSearchableColumns = [
    'name',
    'pluginType',
    'version',
    'author'
];

const InstalledPluginFilters = (props: InstalledPluginFilterProps) => {
    const { setDisplayedRowsCallback, setIsFilteringCallback } = props;

    const { data: installedPlugins } = useGetInstalledPluginsQuery();
    const [filters, setFilters] = useState({});

    const filterRows = (rows: PluginRow[]): PluginRow[] => {
        setIsFilteringCallback(true);
        let filteredRows = _.cloneDeep(rows);
        for (const filter of Object.values(filters)) {
            // @ts-ignore
            filteredRows = filteredRows.filter(filter);
        }
        setIsFilteringCallback(false);
        return filteredRows;
    };

    const allPluginRows: PluginRow[] = useMemo(() => {
        if (!installedPlugins) return [];
        return generatePluginsTableRows(installedPlugins);
    }, [installedPlugins]);

    useEffect(() => {
        if (allPluginRows) {
            const filteredRows = filterRows(allPluginRows);
            setDisplayedRowsCallback(filteredRows);
        }
    }, [allPluginRows, filters]);

    if (installedPlugins && installedPlugins.length > 0) {
        return (
            <Grid container spacing={2} sx={{ margin: 0 }}>
                <Grid
                    xs={7}
                    item
                    sx={{ alignItems: 'flex-end', display: 'flex' }}>
                    <SearchFilter
                        setFiltersCallback={setFilters}
                        searchableColumns={defaultSearchableColumns}
                    />
                </Grid>
                <Grid
                    xs={5}
                    item
                    sx={{ alignItems: 'flex-end', display: 'flex' }}>
                    <TypeFilter
                        setFiltersCallback={setFilters}
                        allRows={allPluginRows}
                    />
                </Grid>
            </Grid>
        );
    }
    return null;
};

export default InstalledPluginFilters;
