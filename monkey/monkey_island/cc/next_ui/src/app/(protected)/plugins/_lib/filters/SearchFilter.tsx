import React from 'react';
import { PluginRow } from '@/app/(protected)/plugins/_lib/PluginTable';
import MonkeySearchBar from '@/_components/search-bar/MonkeySearchBar';

type SearchFilterProps = {
    setFilters: (filters: any) => void;
    searchableColumns: string[];
};

const SearchFilter = (props: SearchFilterProps) => {
    const onSearchChanged = (query: string) => {
        const filterOnText = (pluginRow: PluginRow): boolean => {
            for (const field of props.searchableColumns) {
                const fieldValue = pluginRow[field];
                if (fieldValue?.toLowerCase()?.includes(query?.toLowerCase())) {
                    return true;
                }
            }
        };

        const noOp = (query) => true;

        const filter = query === '' ? noOp : filterOnText;

        props.setFilters((prevState) => {
            return { ...prevState, text: filter };
        });
    };

    return <MonkeySearchBar setQuery={onSearchChanged} />;
};

export default SearchFilter;
