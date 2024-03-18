import Grid from '@mui/material/Grid';
import React, { useEffect, useMemo, useState } from 'react';
import SearchFilter from '@/app/(protected)/plugins/_lib/filters/SearchFilter';
import TypeFilter from '@/app/(protected)/plugins/_lib/filters/TypeFilter';
import { useGetAvailablePluginsQuery } from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import {
    generatePluginsTableRows,
    PluginRow
} from '@/app/(protected)/plugins/_lib/PluginTable';
import _ from 'lodash';
import InstalledPluginFilter from '@/app/(protected)/plugins/_lib/filters/InstalledPluginFilter';

type AvailablePluginFiltersProps = {
    setDisplayedRowsCallback: (rows: PluginRow[]) => void;
    setIsFilteringCallback: (isFiltering: boolean) => void;
};

type PluginFilterFunc = (row: PluginRow) => boolean;

export type FilterProps = {
    setFilterCallback: (
        filterName: string,
        filterFunc: PluginFilterFunc
    ) => void;
};

export const defaultSearchableColumns = [
    'name',
    'pluginType',
    'version',
    'author'
];

const AvailablePluginFilters = (props: AvailablePluginFiltersProps) => {
    const { setDisplayedRowsCallback, setIsFilteringCallback } = props;

    const { data: availablePlugins } = useGetAvailablePluginsQuery();
    const [filters, setFilters] = useState({});

    const setFilterCallback = (
        filterName: string,
        filterFunc: PluginFilterFunc
    ) => {
        setFilters((prevState) => {
            return { ...prevState, [filterName]: filterFunc };
        });
    };

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
        if (!availablePlugins) return [];
        return generatePluginsTableRows(availablePlugins);
    }, [availablePlugins]);

    useEffect(() => {
        if (allPluginRows) {
            const filteredRows = filterRows(allPluginRows);
            setDisplayedRowsCallback(filteredRows);
        }
    }, [allPluginRows, filters]);

    if (availablePlugins && availablePlugins.length > 0) {
        return (
            <Grid container spacing={2} sx={{ margin: 0 }}>
                <InstalledPluginFilter setFilterCallback={setFilterCallback} />
                <Grid
                    xs={4}
                    item
                    sx={{ alignItems: 'flex-end', display: 'flex' }}>
                    <SearchFilter
                        setFilterCallback={setFilterCallback}
                        searchableColumns={defaultSearchableColumns}
                    />
                </Grid>
                <Grid
                    xs={3}
                    item
                    sx={{ alignItems: 'flex-end', display: 'flex' }}>
                    <TypeFilter
                        setFilterCallback={setFilterCallback}
                        allRows={allPluginRows}
                    />
                </Grid>
            </Grid>
        );
    }
    return null;
};

export default AvailablePluginFilters;
