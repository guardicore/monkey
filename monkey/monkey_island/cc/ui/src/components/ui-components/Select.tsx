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
  let selectOptions = [];
  for (let i = 0; i < props.options.length; i++) {
    let menuItem = (
      <MenuItem value={props.options[i].value}
                key={props.options[i].value}>
        {props.options[i].label}
      </MenuItem>
    )
    selectOptions.push(menuItem)
  }

  return (
    <FormControl fullWidth>
      <InputLabel id="demo-simple-select-label">{props.placeholder}</InputLabel>
      <Select
        defaultValue={props.selectedOption.value}
        onChange={props.onChange}
      >
        {selectOptions}
      </Select>
    </FormControl>
  )
}

export default SelectComponent;
