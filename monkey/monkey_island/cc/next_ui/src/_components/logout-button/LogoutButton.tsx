'use client';
import * as React from 'react';
import Button from '@mui/material/Button';
import LogoutIcon from '@mui/icons-material/Logout';
import { useLogoutMutation } from '@/redux/features/api/authentication/internalAuthApi';

const LogoutButton = () => {
    const [logout, { isLoading }] = useLogoutMutation();

    const handleButtonClick = async () => {
        // @ts-ignore
        logout();
    };

    return (
        <Button
            disabled={isLoading}
            onClick={handleButtonClick}
            variant="outlined"
            startIcon={<LogoutIcon />}
            color="error">
            {isLoading ? 'Logging Out..' : 'Logout'}
        </Button>
    );
};

export default LogoutButton;
