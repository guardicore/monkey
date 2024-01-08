'use client';
import * as React from 'react';
import Button from '@mui/material/Button';
import LogoutIcon from '@mui/icons-material/Logout';
import { removeToken } from '@/_lib/authentication';
import { useRouter } from 'next/navigation';
import { PATHS } from '@/constants/paths.constants';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';
import { store } from '@/redux/store';

const LogoutButton = () => {
    const router = useRouter();
    const handleButtonClick = async () => {
        removeToken();
        store.dispatch(islandApiSlice.util.resetApiState());
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
