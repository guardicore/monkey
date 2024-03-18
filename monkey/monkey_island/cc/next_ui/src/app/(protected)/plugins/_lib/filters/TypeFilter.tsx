import React, { useState } from 'react';
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

const TypeFilter = ({ allRows, setFilterCallback }: TypeFilterProps) => {
    const [selectedType, setSelectedType] = useState(anyTypeOption);
    const selectOptionFromValue = (value): SelectOption => {
        return { value: value, label: value };
    };

    let allTypes: string[] = [];
    allTypes = allRows.map((row) => row.pluginType);
    allTypes = [...new Set(allTypes)];
    const selectOptions: SelectOption[] = allTypes.map(selectOptionFromValue);
    selectOptions.unshift(anyTypeOption);

    const handleTypeChange = (event) => {
        const selectOptionChosen = selectOptionFromValue(event.target.value);
        setSelectedType(selectOptionChosen);
        setFilterCallback('pluginType', getFilterForType(selectOptionChosen));
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
            options={selectOptions}
            selectedOption={selectedType}
            onChange={handleTypeChange}
            variant={SelectVariant.Standard}
            defaultValue={''}
        />
    );
};

export default TypeFilter;
