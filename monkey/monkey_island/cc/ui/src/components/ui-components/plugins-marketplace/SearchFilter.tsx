import SearchBar from '../SearchBar';
import React from 'react';
import {PluginRow} from './PluginTable';

type SearchFilterProps = {
  setFilters: (filters: any) => void;
  searchableColumns: string[];
}

export const defaultSearchableColumns = ['name', 'pluginType', 'version', 'author'];


const SearchFilter = (props :SearchFilterProps) => {

  const onSearchChanged = (query :string) => {
    const filterOnText = (pluginRow :PluginRow): boolean => {
      for (const field of props.searchableColumns) {
        const fieldValue = pluginRow[field];
        if (fieldValue.toLowerCase().includes(query.toLowerCase())) {
          return true;
        }
      }
    }

    const noOp = (query) => true;

    let filter = query === '' ? noOp : filterOnText;

    props.setFilters((prevState) => {
      return {...prevState, text: filter};
    });
  }

  return (
    <SearchBar setQuery={onSearchChanged} />
  )
}

export default SearchFilter;
