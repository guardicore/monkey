import Grid from '@mui/material/Grid';
import React, { useState } from 'react';
import SearchFilter from '@/app/(protected)/plugins/_lib/filters/SearchFilter';
import TypeFilter from '@/app/(protected)/plugins/_lib/filters/TypeFilter';
import InstalledPluginFilter from '@/app/(protected)/plugins/_lib/filters/InstalledPluginFilter';
import { PluginRow } from '@/app/(protected)/plugins/_lib/PluginTable';

type AvailablePluginFiltersProps = {
    allPluginRows: PluginRow[];
    filtersChanged: (filters: { [key: string]: number }) => void;
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

const AvailablePluginFilters = (props: AvailablePluginFiltersProps) => {
    const { allPluginRows, filtersChanged } = props;
    const [filters, setFilters] = useState({});

    const setFiltersCallback = (updatedFilters: any) => {
        const newFilters = { ...filters, ...updatedFilters };
        setFilters(newFilters);
        filtersChanged(newFilters);
    };

    return (
        <Grid container spacing={2} sx={{ margin: 0 }}>
            <InstalledPluginFilter setFiltersCallback={setFiltersCallback} />
            <Grid xs={4} item sx={{ alignItems: 'flex-end', display: 'flex' }}>
                <SearchFilter
                    setFiltersCallback={setFiltersCallback}
                    searchableColumns={defaultSearchableColumns}
                />
            </Grid>
            <Grid xs={3} item sx={{ alignItems: 'flex-end', display: 'flex' }}>
                <TypeFilter
                    setFiltersCallback={setFiltersCallback}
                    allRows={allPluginRows}
                />
            </Grid>
        </Grid>
    );
};

export default AvailablePluginFilters;
