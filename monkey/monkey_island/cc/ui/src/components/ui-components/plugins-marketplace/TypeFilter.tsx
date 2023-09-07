import React, {useEffect, useState} from 'react';
import {PluginRow} from './PluginTable';
import MonkeySelect, {MONKEY_SELECT_ALL_VALUE} from '../MonkeySelect';

type SetFiltersFunc = (filters: { [name: string]: number }) => void;

type TypeFilterProps = {
  allRows: PluginRow[],
  setFilters: (filters: { [name: string]: SetFiltersFunc }) => void
}

type SelectOption = {
  value: string,
  label: string
}

const anyTypeOption: SelectOption = {label: 'All', value: ''};

const TypeFilter = ({allRows, setFilters}: TypeFilterProps) => {
  const [selectedType, setSelectedType] = useState(MONKEY_SELECT_ALL_VALUE)
  const [typeFilters, setTypeFilters] = useState([])

  useEffect(() => {
    let allTypes = [];
    allTypes = allRows.map(row => row.pluginType);
    allTypes = [...new Set(allTypes)]
    allTypes = allTypes.map(selectOptionFromValue)
    setTypeFilters(allTypes)
  }, [allRows])

  useEffect(() => {
    setFilters((prevState) => {
      return {...prevState, pluginType: getFilterForType(selectedType)}
    })
  }, [selectedType])

  const selectOptionFromValue = (value): SelectOption => {
    return value === '' ? anyTypeOption : {label: value, value: value};
  }

  const handleTypeChange = (value) => {
    setSelectedType(selectOptionFromValue(value))
  }

  const getFilterForType = (typeOption: SelectOption) => {
    if (typeOption.value === anyTypeOption.value) {
      return () => true;
    }

    return (row: PluginRow): boolean => {
      let pluginType = row.pluginType
      return pluginType === typeOption.value
    };
  }

  return (
    <MonkeySelect options={typeFilters}
                  setAllOption={true}
                  defaultSelectedOptionValue={MONKEY_SELECT_ALL_VALUE}
                  onSelectValueChange={handleTypeChange}
                  label="Type"/>
  )
}

export default TypeFilter;
