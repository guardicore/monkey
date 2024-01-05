'use client';
import { Button } from '@mui/material';
import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { PATHS } from '@/constants/paths.constants';
import { HTTP_METHODS } from '@/constants/http.constants';
import handleAuthToken from '@/app/(auth)/_lib/handleAuthToken';

type RegistrationParams = {
    username: string;
    password: string;
};

const sendRegistrationRequest = async (
    registrationParams: RegistrationParams
) => {
    const response = await fetch(`/api/register`, {
        method: HTTP_METHODS.POST,
        headers: {
            'Content-Type': 'application/json'
        },
        // @ts-ignore
        body: JSON.stringify(registrationParams)
    });

    if (response.status !== 200) {
        return null;
    }

    return await handleAuthToken(response);
};

const RegisterPage = () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const router = useRouter();

    const [registerFormValues, setRegisterFormValues] = useState({
        username: '',
        password: ''
    });

    const handleSubmit = async (event: any) => {
        event.preventDefault();
        const success = await sendRegistrationRequest(registerFormValues);
        if (success) {
            router.push(PATHS.ROOT);
        }
    };

    const handleRegisterFormValueChange = (e: any) => {
        const name = e.target.name;
        const value =
            e.target.type === 'checkbox' ? e.target.checked : e.target.value;
        setRegisterFormValues({ ...registerFormValues, [name]: value });
    };

    const renderRegisterForm = () => {
        return (
            <>
                <Container component="main" maxWidth="xs">
                    <CssBaseline />
                    <Box
                        sx={{
                            marginTop: 8,
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center'
                        }}>
                        <Avatar sx={{ m: 1, bgcolor: 'primary.main' }}>
                            <LockOutlinedIcon />
                        </Avatar>
                        <Typography component="h1" variant="h5">
                            Register
                        </Typography>
                        <Box
                            component="form"
                            onSubmit={handleSubmit}
                            sx={{ mt: 1 }}>
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                id="username"
                                label="username"
                                name="username"
                                autoComplete="username"
                                value={registerFormValues.username}
                                onChange={handleRegisterFormValueChange}
                                autoFocus
                            />
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                name="password"
                                label="Password"
                                type="password"
                                id="password"
                                autoComplete="current-password"
                                value={registerFormValues.password}
                                onChange={handleRegisterFormValueChange}
                            />
                            <Button
                                type="submit"
                                fullWidth
                                variant="contained"
                                sx={{ mt: 3, mb: 2 }}>
                                Sign Up
                            </Button>
                        </Box>
                    </Box>
                </Container>
            </>
        );
    };

    return renderRegisterForm();
};

export default RegisterPage;
