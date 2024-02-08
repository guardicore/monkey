'use client';
import * as React from 'react';
import { useState } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Link from '@mui/material/Link';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
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
import ErrorList from '@/_components/errors/ErrorList';
import LoadingIcon from '@/_components/icons/LoadingIcon';
import MonkeyLogo from '@/_components/icons/MonkeyLogo';
import { useTheme } from '@mui/material/styles';
import { cardStyle, containerStyle } from '@/app/(auth)/login/style';

const LoginPage = () => {
    const router = useRouter();
    const theme = useTheme();
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
            <Container component="main" maxWidth="xs" sx={containerStyle}>
                <Stack direction="column" alignItems={'center'} spacing={2}>
                    {renderFormCard()}
                </Stack>
            </Container>
        );
    };

    const renderFormCard = () => {
        return (
            <Card variant="outlined" sx={cardStyle(theme)}>
                <MonkeyLogo sx={{ height: '50px' }} />
                <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        id="username"
                        label="Username"
                        name="username"
                        autoComplete="username"
                        value={loginFormValues.username}
                        onChange={handleLoginFormValueChange}
                        autoFocus
                        sx={{ bgcolor: 'background.default' }}
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
                        sx={{ bgcolor: 'background.default' }}
                    />
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{ mt: 3, mb: 2 }}>
                        {renderSubmitButtonContent()}
                    </Button>

                    {isError && Array.isArray(error) && (
                        <ErrorList errors={error} />
                    )}

                    <Grid container>
                        <Grid item xs>
                            <Link
                                href="https://techdocs.akamai.com/infection-monkey/docs/frequently-asked-questions#reset-the-monkey-island-password"
                                target={'_blank'}>
                                Forgot password?
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
        return 'Login';
    };

    return renderLoginForm();
};
export default LoginPage;
