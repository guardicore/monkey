import React from 'react';
import { PluginRow } from '@/app/(protected)/plugins/_lib/PluginTable';
import MonkeySearchBar from '@/_components/search-bar/MonkeySearchBar';
import { FilterProps } from '@/app/(protected)/plugins/available/AvailablePluginFilters';

type SearchFilterProps = FilterProps & {
    searchableColumns: string[];
};

const SearchFilter = (props: SearchFilterProps) => {
    const { searchableColumns, setFilterCallback } = props;

    const onSearchChanged = (query: string) => {
        const filterOnText = (pluginRow: PluginRow): boolean => {
            for (const field of searchableColumns) {
                const fieldValue = pluginRow[field];
                if (fieldValue?.toLowerCase()?.includes(query?.toLowerCase())) {
                    return true;
                }
            }
            return false;
        };

        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        const noOp = (_) => true;

        const filter = query === '' ? noOp : filterOnText;

        setFilterCallback('text', filter);
    };

    return <MonkeySearchBar setQuery={onSearchChanged} />;
};

export default SearchFilter;
