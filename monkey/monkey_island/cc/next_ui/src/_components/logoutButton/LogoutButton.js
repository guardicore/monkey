'use client';
import * as React from 'react';
import Button from '@mui/material/Button';
import { useLogoutMutation } from '@/redux/features/api/authentication/internalAuthApi';

const LogoutButton = () => {
    const [logout, { isLoading }] = useLogoutMutation();

    const handleButtonClick = async () => {
        logout(); // logout from server
    };

    return (
        <Button
            disabled={isLoading}
            onClick={handleButtonClick}
            variant="outlined"
            color="error">
            {isLoading ? 'Logging Out..' : 'Logout'}
        </Button>
    );
};

export default LogoutButton;
