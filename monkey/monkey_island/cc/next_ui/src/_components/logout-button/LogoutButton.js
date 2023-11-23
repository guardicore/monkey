'use client';
import * as React from 'react';
import Button from '@mui/material/Button';
import { useLogoutMutation } from '@/redux/features/api/authentication/internalAuthApi';
import { useSession } from 'next-auth/react';
import { AUTH_STATUS } from '@/constants/authStatus.constants';

const LogoutButton = () => {
    const { status } = useSession();
    const [logout, { isLoading }] = useLogoutMutation();

    const handleButtonClick = async () => {
        logout(); // logout from server
    };

    if (
        status === AUTH_STATUS.UNAUTHENTICATED ||
        status === AUTH_STATUS.LOADING
    ) {
        return null;
    }

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
