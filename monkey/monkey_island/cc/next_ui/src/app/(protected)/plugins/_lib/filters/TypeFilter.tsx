import React, { useEffect, useState } from 'react';
import { PluginRow } from './PluginTable';
import MonkeySelect, { SelectVariant } from '@/_components/select/MonkeySelect';

type TypeFilterProps = {
    allRows: PluginRow[];
    setFiltersCallback: (filters: (prevState) => any) => void;
};

type SelectOption = {
    value: string;
    label: string;
};

const anyTypeOption: SelectOption = { value: '', label: 'All' };

const TypeFilter = ({ allRows, setFiltersCallback }: TypeFilterProps) => {
    const [selectedType, setSelectedType] = useState(anyTypeOption);
    const [typeFilters, setTypeFilters] = useState([]);

    useEffect(() => {
        let allTypes = [];
        allTypes = allRows.map((row) => row.pluginType);
        allTypes = [...new Set(allTypes)];
        allTypes = allTypes.map(selectOptionFromValue);
        allTypes.unshift(anyTypeOption);
        setTypeFilters(allTypes);
    }, [allRows]);

    useEffect(() => {
        setFiltersCallback((prevState) => {
            return { ...prevState, pluginType: getFilterForType(selectedType) };
        });
    }, [selectedType, setFiltersCallback]);

    const selectOptionFromValue = (value): SelectOption => {
        return { value: value, label: value };
    };

    const handleTypeChange = (event) => {
        setSelectedType(selectOptionFromValue(event.target.value));
    };

    const getFilterForType = (typeOption: SelectOption) => {
        if (typeOption.value === '') {
            return () => true;
        }

        return (row: PluginRow): boolean => {
            const pluginType = row.pluginType;
            return pluginType === typeOption.value;
        };
    };

    return (
        <MonkeySelect
            placeholder={'Type'}
            options={typeFilters}
            selectedOption={selectedType}
            onChange={handleTypeChange}
            variant={SelectVariant.Standard}
            defaultValue={''}
        />
    );
};

export default TypeFilter;
