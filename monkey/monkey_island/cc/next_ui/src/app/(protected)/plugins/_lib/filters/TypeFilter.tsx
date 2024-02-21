import React, { useEffect, useState } from 'react';
import MonkeySelect, { SelectVariant } from '@/_components/select/MonkeySelect';
import { FilterProps } from '@/app/(protected)/plugins/available/AvailablePluginFilters';
import { PluginRow } from '@/app/(protected)/plugins/_lib/PluginTable';

type TypeFilterProps = FilterProps & {
    allRows: PluginRow[];
};

type SelectOption = {
    value: string;
    label: string;
};

const anyTypeOption: SelectOption = { value: '', label: 'All' };

const TypeFilter = ({ allRows, setFiltersCallback }: TypeFilterProps) => {
    const [selectedType, setSelectedType] = useState(anyTypeOption);
    const [typeFilters, setTypeFilters] = useState<SelectOption[]>([]);

    useEffect(() => {
        let allTypes: string[] = [];
        allTypes = allRows.map((row) => row.pluginType);
        allTypes = [...new Set(allTypes)];
        const selectOptions: SelectOption[] = allTypes.map(
            selectOptionFromValue
        );
        selectOptions.unshift(anyTypeOption);
        setTypeFilters(selectOptions);
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
