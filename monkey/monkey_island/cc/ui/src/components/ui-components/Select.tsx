import React from 'react';
import {FormControl, InputLabel, MenuItem, Select, SelectChangeEvent,
  SelectProps as MUISelectProps} from '@mui/material';

export enum SelectVariant {
  Standard = 'standard',
  Outlined = 'outlined',
  Filled = 'filled'
}

type Option = {
  label: string,
  value: string,
}

type SelectProps = MUISelectProps & {
  placeholder: string,
  options: Option[],
  selectedOption: Option,
  onChange: (event: SelectChangeEvent) => void,
  variant?: SelectVariant
}

const SelectComponent = (props: SelectProps) => {
  const {placeholder, options, selectedOption, onChange, ...rest} = {...props};
  rest['variant'] = rest['variant'] || SelectVariant.Outlined;

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
        variant={'standard'}
        defaultValue={selectedOption.value}
        onChange={onChange}
        {...rest}
      >
        {selectOptions}
      </Select>
    </FormControl>
  )
}

export default SelectComponent;
