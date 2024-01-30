'use client';
import * as React from 'react';
import Button from '@mui/material/Button';
import LogoutIcon from '@mui/icons-material/Logout';
import { useLogoutMutation } from '@/redux/features/api/authentication/authenticationEndpoints';

const LogoutButton = () => {
    const [logout] = useLogoutMutation();

    return (
        <Button
            onClick={() => logout()}
            variant="outlined"
            startIcon={<LogoutIcon />}
            color="error">
            Logout
        </Button>
    );
};

export default LogoutButton;
