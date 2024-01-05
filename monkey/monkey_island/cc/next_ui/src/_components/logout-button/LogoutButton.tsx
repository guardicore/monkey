'use client';
import * as React from 'react';
import Button from '@mui/material/Button';
import LogoutIcon from '@mui/icons-material/Logout';

const LogoutButton = () => {
    const handleButtonClick = async () => {
        // @ts-ignore
        logout();
    };

    return (
        <Button
            onClick={handleButtonClick}
            variant="outlined"
            startIcon={<LogoutIcon />}
            color="error"></Button>
    );
};

export default LogoutButton;
