'use client';
import * as React from 'react';
import Button from '@mui/material/Button';
import LogoutIcon from '@mui/icons-material/Logout';
import { store } from '@/redux/store';

const LogoutButton = () => {
    const handleButtonClick = async () => {
        store.dispatch({ type: 'LOGOUT' });
    };

    return (
        <Button
            onClick={handleButtonClick}
            variant="outlined"
            startIcon={<LogoutIcon />}
            color="error">
            Logout
        </Button>
    );
};

export default LogoutButton;
