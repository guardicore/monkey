import React from 'react';
import {InputLabel, FormControl, Select, MenuItem, SelectChangeEvent} from '@mui/material';


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
  for(let i = 0; i < props.options.length; i++) {
    selectOptions.push(<MenuItem value={props.options[i].value}>{props.options[i].label}</MenuItem>)
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
