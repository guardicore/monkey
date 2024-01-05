'use client';
import * as React from 'react';
import Button from '@mui/material/Button';
import LogoutIcon from '@mui/icons-material/Logout';
import { removeToken } from '@/_lib/authentication';
import { useRouter } from 'next/navigation';
import { PATHS } from '@/constants/paths.constants';

const LogoutButton = () => {
    const router = useRouter();
    const handleButtonClick = async () => {
        removeToken();
        router.push(PATHS.SIGN_IN);
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
