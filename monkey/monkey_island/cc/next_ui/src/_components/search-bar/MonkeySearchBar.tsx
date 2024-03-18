import React, { useState } from 'react';
import {
    Box,
    IconButton,
    InputAdornment,
    TextField,
    TextFieldProps
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import ClearIcon from '@mui/icons-material/Clear';
import { nanoid } from 'nanoid';

const EMPTY_STRING = '';
const DEFAULT_VARIANT = 'standard';
const DEFAULT_PLACEHOLDER = 'Search';

type SearchBarProps = TextFieldProps & {
    setQuery?: (query: string) => void;
};

const MonkeySearchBar = (props: SearchBarProps) => {
    const {
        variant = DEFAULT_VARIANT,
        placeholder = DEFAULT_PLACEHOLDER,
        label = null,
        setQuery,
        ...rest
    } = { ...props };
    const [currentValue, setCurrentValue] = useState(EMPTY_STRING);

    const handleValueChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newSearchQuery = e?.target?.value?.trim() || EMPTY_STRING;
        setCurrentValue(newSearchQuery);
        setQuery && setQuery(newSearchQuery);
    };

    const clearValue = () => {
        setCurrentValue(EMPTY_STRING);
        setQuery && setQuery(EMPTY_STRING);
    };

    return (
        <Box className="search-bar-wrapper">
            <TextField
                id={`search-bar-${nanoid()}`}
                fullWidth
                variant={variant}
                label={label}
                value={currentValue}
                placeholder={placeholder}
                onChange={handleValueChange}
                InputProps={{
                    startAdornment: (
                        <InputAdornment position="start">
                            <SearchIcon />
                        </InputAdornment>
                    ),
                    endAdornment: currentValue !== '' && (
                        <InputAdornment position="end">
                            <IconButton onClick={clearValue}>
                                <ClearIcon />
                            </IconButton>
                        </InputAdornment>
                    )
                }}
                {...rest}
            />
        </Box>
    );
};

export default MonkeySearchBar;
