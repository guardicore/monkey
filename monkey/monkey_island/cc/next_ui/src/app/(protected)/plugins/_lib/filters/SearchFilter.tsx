import React from 'react';
import { PluginRow } from '@/app/(protected)/plugins/_lib/PluginTable';
import MonkeySearchBar from '@/_components/search-bar/MonkeySearchBar';

type SearchFilterProps = {
    setFiltersCallback: (filters: any) => void;
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

        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        const noOp = (_) => true;

        const filter = query === '' ? noOp : filterOnText;

        props.setFiltersCallback((prevState) => {
            return { ...prevState, text: filter };
        });
    };

    return <MonkeySearchBar setQuery={onSearchChanged} />;
};

export default SearchFilter;
