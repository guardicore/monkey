'use client';
import * as React from 'react';
import Button from '@mui/material/Button';
import { useLogoutMutation } from '@/redux/features/api/authentication/internalAuthApi';
//eslint-disable-next-line @typescript-eslint/no-unused-vars
import { signOut } from 'next-auth/react';

const LogoutButton = () => {
    //const { data: session, status } = useSession();
    //console.log(session, status);

    // const isLoggedIn = useAuth();
    //eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [logout, { isSuccess, isLoading }] = useLogoutMutation();

    const handleButtonClick = async () => {
        logout(); // logout from server
    };

    return (
        // isLoggedIn && (
        <Button
            disabled={isLoading}
            onClick={handleButtonClick}
            variant="outlined"
            color="error">
            {isLoading ? 'Logging Out..' : 'Logout'}
        </Button>
        // )
    );
};

export default LogoutButton;
