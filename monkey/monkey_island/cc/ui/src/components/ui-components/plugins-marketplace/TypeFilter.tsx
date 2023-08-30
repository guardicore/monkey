import React, {useEffect, useState} from 'react';
import SelectComponent, {SelectVariant} from '../Select';
import _ from 'lodash';

type TypeFilterProps = {
  allPlugins: any[],
  displayedPlugins: any[],
  setDisplayedPlugins: (plugins: any[]) => void,
  className?: string
}

type SelectOption = {
  value: string,
  label: string
}

const anyTypeOption :SelectOption = {value: "", label: "All"}

const TypeFilter = (props: TypeFilterProps) => {
  const [selectedType, setSelectedType] = useState(anyTypeOption)
  const [typeFilters, setTypeFilters] = useState([])

  useEffect(() => {
    let allTypes = [];
    allTypes = props.allPlugins.map(plugin => plugin.type_ || plugin.plugin_type)
    allTypes = [...new Set(allTypes)]
    allTypes = allTypes.map(selectOptionFromValue)
    allTypes.push(anyTypeOption)
    setTypeFilters(allTypes)
  }, [props.allPlugins])

  useEffect(() => {
    filterPlugins(selectedType)
  }, [props.displayedPlugins])

  const selectOptionFromValue = (value) :SelectOption => {
    return {value: value, label: _.startCase(value)}
  }

  const handleTypeChange = (event) => {
    setSelectedType(selectOptionFromValue(event.target.value))
    props.setDisplayedPlugins(props.allPlugins)
  }

  const filterPlugins = (typeOption :SelectOption) => {
    const typeFilter = (plugin) => {
      let pluginType = plugin.type_ || plugin.plugin_type
      return pluginType === typeOption.value
    }

    if (typeOption.value) {
      let filteredPlugins = props.displayedPlugins.filter(typeFilter)
      if(!_.isEqual(filteredPlugins, props.displayedPlugins)) {
        props.setDisplayedPlugins(filteredPlugins)
      }
    }
  }

  return (
    <SelectComponent placeholder={"Type"} options={typeFilters}
                     selectedOption={selectedType} onChange={handleTypeChange}
                     variant={SelectVariant.Standard}/>
  )
}

export default TypeFilter;
