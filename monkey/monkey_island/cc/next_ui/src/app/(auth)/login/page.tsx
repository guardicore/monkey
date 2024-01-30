'use client';
import * as React from 'react';
import { useState } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import Checkbox from '@mui/material/Checkbox';
import Container from '@mui/material/Container';
import FormControlLabel from '@mui/material/FormControlLabel';
import Grid from '@mui/material/Grid';
import Link from '@mui/material/Link';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
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
import useRedirectToRegistration from '@/app/(auth)/login/useRedirectToRegistration';
import ErrorAlerts from '@/_components/alerts/ErrorAlerts';
import LoadingIcon from '@/_components/icons/LoadingIcon';
import MonkeyLogo from '@/_components/icons/MonkeyLogo';
import classes from './page.module.scss';

const LoginPage = () => {
    const router = useRouter();
    const [loginFormValues, setLoginFormValues] = useState({
        username: '',
        password: ''
    });
    const [login, { isError, isLoading, isSuccess, error }] =
        useLoginMutation();
    const [serverError, setServerError] = useState<Error | null>(null);

    useRedirectToRegistration();

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
            <Container id={classes.container} component="main" maxWidth="xs">
                <Stack direction="column" alignItems={'center'} spacing={2}>
                    <MonkeyLogo id={classes.logo} />
                    {renderFormCard()}
                </Stack>
            </Container>
        );
    };

    const renderFormCard = () => {
        return (
            <Card id={classes.card} variant="outlined">
                <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
                    <Typography component="h1" variant="h5">
                        Login
                    </Typography>
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
                        control={<Checkbox value="remember" color="primary" />}
                        label="Remember me"
                    />
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{ mt: 3, mb: 2 }}>
                        {renderSubmitButtonContent()}
                    </Button>

                    {renderErrors()}

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
            </Card>
        );
    };

    const renderSubmitButtonContent = () => {
        if (isLoading) {
            return <LoadingIcon />;
        } else if (isSuccess) {
            return 'Success!';
        }
        return 'Sign In';
    };

    const renderErrors = () => {
        if (isError && Array.isArray(error)) {
            return <ErrorAlerts errors={error} />;
        }
    };

    return renderLoginForm();
};
export default LoginPage;
