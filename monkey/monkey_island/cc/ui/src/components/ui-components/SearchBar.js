import React, {useEffect, useState} from 'react';
import {Box, IconButton, InputAdornment, TextField} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import ClearIcon from '@mui/icons-material/Clear';
import {nanoid} from 'nanoid';

const EMPTY_STRING = '';
const SearchBar = (props) => {
  const {variant = 'standard', label, placeholder = 'Search', setQuery} = {...props};
  const [currentValue, setCurrentValue] = useState(EMPTY_STRING);

  useEffect(() => {
    setQuery && setQuery(currentValue);
  }, [currentValue]);

  const handleValueChange = (e) => {
    const currentValue = e?.target?.value?.trim() || EMPTY_STRING;
    setCurrentValue(currentValue);
  }

  const clearValue = () => {
    setCurrentValue(EMPTY_STRING);
  }

  return (
    <Box>
      <TextField id={`search-bar-${nanoid()}`}
                 variant={variant}
                 label={label}
                 value={currentValue}
                 placeholder={placeholder}
                 onChange={handleValueChange}
                 InputProps={{
                   startAdornment: (
                     <InputAdornment position="start">
                       <SearchIcon/>
                     </InputAdornment>
                   ),
                   endAdornment: (
                     currentValue !== '' && (
                       <InputAdornment position="end">
                         <IconButton onClick={clearValue}>
                           <ClearIcon/>
                         </IconButton>
                       </InputAdornment>
                     )
                   )
                 }}/>
    </Box>
  )
}

export default SearchBar;
