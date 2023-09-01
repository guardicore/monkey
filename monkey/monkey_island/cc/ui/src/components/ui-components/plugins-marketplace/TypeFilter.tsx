import React, {useEffect, useState} from 'react';
import SelectComponent, {SelectVariant} from '../Select';
import _ from 'lodash';
import {AvailablePlugin} from '../../contexts/plugins/PluginsContext';

type SetFiltersFunc = (filters: { [name: string]: number } ) => void;

type TypeFilterProps = {
  allPlugins: AvailablePlugin[],
  filters: { [name: string]: SetFiltersFunc } ,
  setFilters: (filters: { [name: string]: SetFiltersFunc } ) => void
}

type SelectOption = {
  value: string,
  label: string
}

const anyTypeOption :SelectOption = {value: "", label: "All"}

const TypeFilter = ({allPlugins, filters, setFilters} :TypeFilterProps) => {
  const [selectedType, setSelectedType] = useState(anyTypeOption)
  const [typeFilters, setTypeFilters] = useState([])

  useEffect(() => {
    let allTypes = [];
    allTypes = allPlugins.map(plugin => plugin.pluginType)
    allTypes = [...new Set(allTypes)]
    allTypes = allTypes.map(selectOptionFromValue)
    allTypes.unshift(anyTypeOption)
    setTypeFilters(allTypes)
  }, [allPlugins])

  useEffect(() => {
    let newFilters = {...filters};
    newFilters['type'] = getFilterForType(selectedType);
    setFilters(newFilters);
  }, [selectedType])

  const selectOptionFromValue = (value) :SelectOption => {
    return {value: value, label: _.startCase(value)}
  }

  const handleTypeChange = (event) => {
    setSelectedType(selectOptionFromValue(event.target.value))
  }

  const getFilterForType = (typeOption :SelectOption) => {
    if (typeOption.value === "") {
      return () => true;
    }

    const typeFilter = (plugin :AvailablePlugin) :boolean => {
      let pluginType = plugin.pluginType
      return pluginType === typeOption.value
    }
    return typeFilter;
  }

  return (
    <SelectComponent placeholder={"Type"} options={typeFilters}
                     selectedOption={selectedType} onChange={handleTypeChange}
                     variant={SelectVariant.Standard}/>
  )
}

export default TypeFilter;
