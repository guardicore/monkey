'use client';
import { Button } from '@mui/material';
import * as React from 'react';
import { useState } from 'react';
import Avatar from '@mui/material/Avatar';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { useRouter } from 'next/navigation';
import { PATHS } from '@/constants/paths.constants';
import {
    ErrorResponse,
    SuccessfulAuthenticationResponse,
    useRegisterMutation
} from '@/redux/features/api/authentication/authenticationEndpoints';
import setAuthenticationTimer from '@/redux/features/api/authentication/_lib/setAuthenticationTimer';
import handleAuthToken from '@/redux/features/api/authentication/_lib/handleAuthToken';
import { instanceOfError } from '@/lib/typeChecks';

const RegisterPage = () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const router = useRouter();

    const [registerFormValues, setRegisterFormValues] = useState({
        username: '',
        password: ''
    });
    const [register, { isError, error }] = useRegisterMutation();
    const [serverError, setServerError] = useState(null);

    const handleSubmit = async (event: any) => {
        event.preventDefault();
        const registrationResponse:
            | { data: SuccessfulAuthenticationResponse }
            | { error: ErrorResponse | Error } =
            await register(registerFormValues);

        if ('data' in registrationResponse) {
            handleAuthToken(registrationResponse.data);
            setAuthenticationTimer();
            router.push(PATHS.ROOT);
        } else if (instanceOfError(registrationResponse.error)) {
            setServerError(registrationResponse.error);
        }
    };

    const handleRegisterFormValueChange = (e: any) => {
        const name = e.target.name;
        const value =
            e.target.type === 'checkbox' ? e.target.checked : e.target.value;
        setRegisterFormValues({ ...registerFormValues, [name]: value });
    };

    const renderRegisterForm = () => {
        if (serverError) {
            throw serverError;
        }
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
                            {/* @ts-ignore */}
                            {isError &&
                                Array.isArray(error) &&
                                error.map((item, index) => (
                                    <div key={index} style={{ color: 'red' }}>
                                        {item}
                                    </div>
                                ))}
                        </Box>
                    </Box>
                </Container>
            </>
        );
    };

    return renderRegisterForm();
};

export default RegisterPage;
