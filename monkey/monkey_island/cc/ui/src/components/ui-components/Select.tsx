import React from 'react';
import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
  SelectProps as MUISelectProps
} from '@mui/material';
import MonkeyTooltip from './MonkeyTooltip';

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

const SelectComponent = ({
                           placeholder,
                           options,
                           selectedOption,
                           onChange,
                           variant=SelectVariant.Outlined,
                           ...rest
                         }: SelectProps) => {

  return (
    <FormControl fullWidth>
      <InputLabel id="demo-simple-select-label">{placeholder}</InputLabel>
      <Select
        variant={variant}
        defaultValue={selectedOption.value}
        onChange={onChange}
        {...rest}
      >
        {
          options.map((option) => {
            return (
                <MenuItem value={option.value} key={option.value}>
                  <MonkeyTooltip isOverflow={true} title={option.label}>
                      {option.label}
                  </MonkeyTooltip>
                </MenuItem>
            )
          })
        }
      </Select>
    </FormControl>
  )
}

export default SelectComponent;
