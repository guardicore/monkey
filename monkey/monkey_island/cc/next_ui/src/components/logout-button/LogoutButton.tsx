'use client';
import * as React from 'react';
import Button from '@mui/material/Button';
import LogoutIcon from '@mui/icons-material/Logout';
import IAuthenticationRepository from '@/repositories/IAuthenticationRepository';

export const buildLogoutButton =
    // eslint-disable-next-line react/display-name
    (authenticationRepository: IAuthenticationRepository) => () => {
        return (
            <Button
                onClick={() => authenticationRepository.logout()}
                variant="outlined"
                startIcon={<LogoutIcon />}
                color="error">
                Logout
            </Button>
        );
    };

export default buildLogoutButton;
