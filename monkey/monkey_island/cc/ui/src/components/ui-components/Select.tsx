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

  return (
    <FormControl fullWidth>
      <InputLabel id="demo-simple-select-label">{placeholder}</InputLabel>
      <Select
        variant={'standard'}
        defaultValue={selectedOption.value}
        onChange={onChange}
        {...rest}
      >
        {
          options.map((option) => {
            return (
              <MenuItem value={option.value} key={option.value}>
                {option.label}
              </MenuItem>
            )
          })
        }
      </Select>
    </FormControl>
  )
}

export default SelectComponent;
