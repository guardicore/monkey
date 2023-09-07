import React, {useEffect, useState} from 'react';
import {Box, MenuItem, TextField} from '@mui/material';
import {nanoid} from 'nanoid';
import _ from 'lodash';
import MonkeyTooltip from './MonkeyTooltip';

export const SELECT_VARIANTS = {
  'STANDARD': 'standard',
  'OUTLINED': 'outlined',
  'FILLED': 'filled'
}

export const MONKEY_SELECT_ALL_VALUE = 'All';

const ALL_OPTION = {label: 'All', value: MONKEY_SELECT_ALL_VALUE};

const getDefaultValue = (defaultValue, options) => {
  const initialDefaultValue = options?.[0]?.value || '';
  if(options.length > 1) {
    return defaultValue || initialDefaultValue;
  }
  return initialDefaultValue;
}

const isContained = (arr1, arr2, isAllOptionSet) => {
  const arr1Values = arr1.map((item)=> item?.value);
  const arr2Values = arr2.map((item)=> item?.value);
  const diff = _.difference(arr1Values, arr2Values);
  if (isAllOptionSet) {
    return diff?.length === 1 && diff[0] === MONKEY_SELECT_ALL_VALUE;
  }
  return diff?.length === 0;
}

const MonkeySelect = (props) => {
  const {
    options = [],
    variant = SELECT_VARIANTS.STANDARD,
    setAllOption = false,
    defaultSelectedOptionValue,
    onSelectValueChange,
    ...rest
  } = {...props};
  const [selectOptions, setSelectOptions] = useState([]);
  const [currentValue, setCurrentValue] = useState(getDefaultValue(defaultSelectedOptionValue, options));

  useEffect(() => {
    setSelectOptions((prevState) => {
      if (options?.length > 0 && !isContained(prevState, options, setAllOption)) {
        let copyOfOptions = [...options];

        if (copyOfOptions?.length > 1) {
          copyOfOptions?.sort();
          if (setAllOption && selectOptions[0]?.value !== MONKEY_SELECT_ALL_VALUE) {
            copyOfOptions?.splice(0, 0, ALL_OPTION);
          }
        }
        setCurrentValue(getDefaultValue(defaultSelectedOptionValue, options))
        return copyOfOptions;
      }
     return prevState;
    });
  }, [options]);

  useEffect(() => {
    if(onSelectValueChange) {
      if (currentValue === MONKEY_SELECT_ALL_VALUE) {
        onSelectValueChange('');
      } else {
        onSelectValueChange(currentValue);
      }
    }
  }, [currentValue])

  const handleValueChange = (event) => {
    setCurrentValue(event?.target?.value?.trim());
  }

  if (options?.length === 0) {
    return null;
  }

  return (
    selectOptions?.length > 0
      ? (
        <Box className="select-wrapper">
          <TextField
            select
            fullWidth
            id={`select-${nanoid()}`}
            value={currentValue}
            onChange={handleValueChange}
            variant={variant}
            {...rest}>
            {
              selectOptions?.map((option) => {
                return option.value
                  ? (
                    <MenuItem key={option.value} value={option.value}>
                      <MonkeyTooltip isOverflow={true} title={option?.label}>
                        {_.capitalize(option.label?.toString())}
                      </MonkeyTooltip>
                    </MenuItem>
                  )
                  : null;
              })
            }
          </TextField>
        </Box>
      )
      : null
  )
}

export default MonkeySelect;
