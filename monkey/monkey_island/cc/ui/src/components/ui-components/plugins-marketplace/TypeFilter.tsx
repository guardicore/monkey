import React, {useEffect, useState} from 'react';
import SelectComponent, {SelectVariant} from '../MonkeySelect';
import {PluginRow} from './PluginTable';

type SetFiltersFunc = (filters: { [name: string]: number } ) => void;

type TypeFilterProps = {
  allRows: PluginRow[],
  setFilters: (filters: { [name: string]: SetFiltersFunc } ) => void
}

type SelectOption = {
  value: string,
  label: string
}

const anyTypeOption :SelectOption = {value: "", label: "All"}

const TypeFilter = ({allRows, setFilters} :TypeFilterProps) => {
  const [selectedType, setSelectedType] = useState(anyTypeOption)
  const [typeFilters, setTypeFilters] = useState([])

  useEffect(() => {
    let allTypes = [];
    allTypes = allRows.map(row => row.pluginType)
    allTypes = [...new Set(allTypes)]
    allTypes = allTypes.map(selectOptionFromValue)
    allTypes.unshift(anyTypeOption)
    setTypeFilters(allTypes)
  }, [allRows])

  useEffect(() => {
    setFilters((prevState) => {
      return {...prevState, pluginType: getFilterForType(selectedType)}
    })}, [selectedType])

  const selectOptionFromValue = (value) :SelectOption => {
    return {value: value, label: value}
  }

  const handleTypeChange = (event) => {
    setSelectedType(selectOptionFromValue(event.target.value))
  }

  const getFilterForType = (typeOption :SelectOption) => {
    if (typeOption.value === "") {
      return () => true;
    }

    return (row: PluginRow): boolean => {
      let pluginType = row.pluginType
      return pluginType === typeOption.value
    };
  }

  return (
    <SelectComponent placeholder={"Type"} options={typeFilters}
                     selectedOption={selectedType} onChange={handleTypeChange}
                     variant={SelectVariant.Standard}
                     defaultValue={''}/>
  )
}

export default TypeFilter;
