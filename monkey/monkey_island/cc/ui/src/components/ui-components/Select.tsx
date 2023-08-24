import React from 'react';
import {InputLabel, FormControl, Select, MenuItem, SelectChangeEvent} from '@mui/material';


type Option = {
  label: string,
  value: string,
}

type SelectProps = {
  placeholder: string,
  options: Option[],
  value: string,
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
        labelId="demo-simple-select-label"
        id="demo-simple-select"
        value={props.value}
        label="Age"
        onChange={props.onChange}
      >
        {selectOptions}
      </Select>
    </FormControl>
  )
}

export default SelectComponent;
