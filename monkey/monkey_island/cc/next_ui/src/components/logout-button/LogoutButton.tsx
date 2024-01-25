'use client';
import * as React from 'react';
import Button from '@mui/material/Button';
import LogoutIcon from '@mui/icons-material/Logout';
import { RepositoryContext } from '@/providers/repositoryProvider/provider';

const LogoutButton = () => {
    const { authenticationRepository } = React.useContext(RepositoryContext);

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

export default LogoutButton;
