'use client';
import { Button } from '@mui/material';
import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { PATHS } from '@/constants/paths.constants';
import {
    ErrorResponse,
    SuccessfulAuthenticationResponse,
    useLoginMutation
} from '@/redux/features/api/authentication/authenticationEndpoints';
import { setAuthenticationTimer } from '@/redux/features/api/authentication/lib/authenticationTimer';
import handleAuthToken from '@/redux/features/api/authentication/lib/handleAuthToken';
import { instanceOfError } from '@/lib/typeChecks';

const SignInPage = () => {
    const router = useRouter();
    const [loginFormValues, setLoginFormValues] = useState({
        username: '',
        password: ''
    });
    const [login, { isError, error }] = useLoginMutation();
    const [serverError, setServerError] = useState(null);

    const handleSubmit = async (event: any) => {
        event.preventDefault();
        const loginResponse:
            | { data: SuccessfulAuthenticationResponse }
            | { error: ErrorResponse | Error } = await login(loginFormValues);

        if ('data' in loginResponse) {
            handleAuthToken(loginResponse.data);
            setAuthenticationTimer();
            router.push(PATHS.ROOT);
        } else if (instanceOfError(loginResponse.error)) {
            setServerError(loginResponse.error);
        }
    };

    const handleLoginFormValueChange = (e: any) => {
        const name = e.target.name;
        const value =
            e.target.type === 'checkbox' ? e.target.checked : e.target.value;
        setLoginFormValues({ ...loginFormValues, [name]: value });
    };

    const renderLoginForm = () => {
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
                            Sign in
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
                                value={loginFormValues.username}
                                onChange={handleLoginFormValueChange}
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
                                value={loginFormValues.password}
                                onChange={handleLoginFormValueChange}
                            />
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        value="remember"
                                        color="primary"
                                    />
                                }
                                label="Remember me"
                            />
                            <Button
                                type="submit"
                                fullWidth
                                variant="contained"
                                sx={{ mt: 3, mb: 2 }}>
                                Sign In
                            </Button>

                            {isError &&
                                Array.isArray(error) &&
                                error.map((item, index) => (
                                    <div key={index} style={{ color: 'red' }}>
                                        {item}
                                    </div>
                                ))}

                            <Grid container>
                                <Grid item xs>
                                    <Link href="#" variant="body2">
                                        Forgot password?
                                    </Link>
                                </Grid>
                                <Grid item>
                                    <Link href="#" variant="body2">
                                        {"Don't have an account? Sign Up"}
                                    </Link>
                                </Grid>
                            </Grid>
                        </Box>
                    </Box>
                </Container>
            </>
        );
    };

    return renderLoginForm();
};
export default SignInPage;
