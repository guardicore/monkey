import React, { useState } from 'react';
import MonkeySelect, { SelectVariant } from '@/_components/select/MonkeySelect';
import { FilterProps } from '@/app/(protected)/plugins/available/AvailablePluginFilters';
import { PluginRow } from '@/app/(protected)/plugins/_lib/PluginTable';
import _ from 'lodash';

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

    const getSelectOptions = (rows: PluginRow[]): SelectOption[] => {
        const allTypes = _.uniq(rows.map((row) => row.pluginType));
        return [anyTypeOption, ...allTypes.map(selectOptionFromValue)];
    };
    const selectOptionFromValue = (value): SelectOption => {
        return { value: value, label: value };
    };
    const selectOptions = getSelectOptions(allRows);

    const getFilterForType = (typeOption: SelectOption) => {
        if (typeOption.value === '') {
            return () => true;
        }

        return (row: PluginRow): boolean => {
            const pluginType = row.pluginType;
            return pluginType === typeOption.value;
        };
    };

    const handleTypeChange = (event) => {
        const selectedOption = selectOptionFromValue(event.target.value);
        setSelectedType(selectedOption);
        setFiltersCallback({ pluginType: getFilterForType(selectedOption) });
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
