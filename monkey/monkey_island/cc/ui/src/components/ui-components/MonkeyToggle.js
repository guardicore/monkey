import React, {useEffect, useState} from 'react';
import {nanoid} from 'nanoid';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';

export const TOGGLE_SIZE = {
  'SMALL': 'small',
  'MEDIUM': 'medium',
  'LARGE': 'large'
}

const DEFAULT_SIZE = TOGGLE_SIZE.MEDIUM;

const MonkeyToggle = (props) => {
  const {
    options = [],
    defaultValues = [],
    isExclusive = true,
    size = DEFAULT_SIZE,
    enforceValueSet = true,
    setSelectedValues
  } = {...props};
  const [toggleOptions, setToggleOptions] = useState(options);
  const [optionsRefId, setOptionsRefId] = useState(null);
  const [currentValues, setCurrentValues] = useState(defaultValues?.length > 0 ? defaultValues : ([options?.[0]?.value] || []));

  useEffect(() => {
    if (!optionsRefId && options?.length > 0) {
      setToggleOptions(options?.sort());
      setOptionsRefId(nanoid());
    }
  }, [options, optionsRefId])

  useEffect(() => {
    setSelectedValues && setSelectedValues(currentValues);
  }, [currentValues])

  const handleValuesChange = (_event, newValues) => {
    if (enforceValueSet && newValues !== null) {
      setCurrentValues(newValues);
    } else if (!enforceValueSet) {
      setCurrentValues(newValues);
    }
  }

  if (!Array.isArray(options) || options?.length === 0) {
    return null;
  }

  return (
    <ToggleButtonGroup
      value={currentValues}
      onChange={handleValuesChange}
      exclusive={isExclusive}
      size={size}
      aria-label="toggle">
      {
        toggleOptions?.map((option) => {
          const value = option?.value;
          const valueAsLabel = typeof value === 'string' ? value?.trim().toUpperCase() : null;
          const label = typeof option?.label === 'string' ? option?.label.toUpperCase() : (option?.label || valueAsLabel);
          return (
            <ToggleButton key={value || nanoid()} value={value} aria-label={value || ''}>
              {label}
            </ToggleButton>
          )
        })
      }
    </ToggleButtonGroup>
  );
}

export default MonkeyToggle;
