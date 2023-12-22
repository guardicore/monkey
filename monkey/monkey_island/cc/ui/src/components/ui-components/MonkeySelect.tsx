import React from 'react';
import {
  FormControl, Input,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
  SelectProps as MUISelectProps
} from '@mui/material';
import MonkeyTooltip from './MonkeyTooltip';
import {styled} from '@mui/material/styles';

export enum SelectVariant {
  Standard = 'standard',
  Outlined = 'outlined',
  Filled = 'filled'
}

type Option = {
  label: string,
  value: string,
}

type SelectProps = Omit<MUISelectProps, 'variant'> & {
  placeholder: string,
  options: Option[],
  selectedOption: Option,
  onChange: (event: SelectChangeEvent) => void,
  variant: SelectVariant
}

const MonkeySelectStyled = styled(Input)(({ theme }) => ({
  '& .MuiInputBase-input': {
    'paddingLeft': '10px'
  }
}));

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
      <InputLabel id="demo-simple-select-label"
                  shrink={true}
                  sx={{'left': '-13px'}}>
        {placeholder}
      </InputLabel>
      <Select
        variant={variant}
        defaultValue={selectedOption.value}
        input={<MonkeySelectStyled/>}
        onChange={onChange}
        displayEmpty={true}
        sx={{'marginTop': '7px !important'}}
        {...rest}
      >
        {
          options.map((option) => {
            return (
                <MenuItem value={option.value} sx={{'paddingLeft': '5px'}} key={option.value}>
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
