import React from 'react';
import {FormControl, InputLabel, MenuItem, Select, SelectChangeEvent} from '@mui/material';


type Option = {
  label: string,
  value: string,
}

type SelectProps = {
  placeholder: string,
  options: Option[],
  selectedOption: Option,
  onChange: (event: SelectChangeEvent) => void
}

const SelectComponent = (props: SelectProps) => {
  const {placeholder, options, selectedOption, onChange} = {...props};
  let selectOptions = [];
  for (let i = 0; i < options.length; i++) {
    let menuItem = (
      <MenuItem value={options[i].value}
                key={options[i].value}>
        {options[i].label}
      </MenuItem>
    )
    selectOptions.push(menuItem)
  }

  return (
    <FormControl fullWidth>
      <InputLabel id="demo-simple-select-label">{placeholder}</InputLabel>
      <Select
        defaultValue={selectedOption.value}
        onChange={onChange}
      >
        {selectOptions}
      </Select>
    </FormControl>
  )
}

export default SelectComponent;
