'use client';
import { Button, Typography } from '@mui/material';
import * as React from 'react';
import { useState } from 'react';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import { useRouter } from 'next/navigation';
import { PATHS } from '@/constants/paths.constants';
import {
    ErrorResponse,
    SuccessfulAuthenticationResponse,
    useRegisterMutation,
    useRegistrationStatusQuery
} from '@/redux/features/api/authentication/authenticationEndpoints';
import { setAuthenticationTimer } from '@/redux/features/api/authentication/lib/authenticationTimer';
import handleAuthToken from '@/redux/features/api/authentication/lib/handleAuthToken';
import { instanceOfError } from '@/lib/typeChecks';
import useRedirectToLogin from '@/app/(auth)/registration/useRedirectToLogin';
import ErrorList from '@/_components/errors/ErrorList';
import Card from '@mui/material/Card';
import BrandHeader from '@/_components/icons/monkey-logo/BrandHeader';
import Stack from '@mui/material/Stack';
import MonkeyLoadingIcon from '@/_components/icons/MonkeyLoadingIcon';
import { useTheme } from '@mui/material/styles';
import { cardStyle, containerStyle } from '@/app/(auth)/registration/style';

const RegisterPage = () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const router = useRouter();
    const theme = useTheme();

    const [registerFormValues, setRegisterFormValues] = useState({
        username: '',
        password: ''
    });
    const [register, { isError, error, isLoading, isSuccess }] =
        useRegisterMutation();
    const [serverError, setServerError] = useState<Error | null>(null);
    const { refetch: refetchRegistrationNeeded } = useRegistrationStatusQuery();

    useRedirectToLogin();

    const handleSubmit = async (event: any) => {
        event.preventDefault();
        const registrationResponse:
            | { data: SuccessfulAuthenticationResponse }
            | { error: ErrorResponse | Error } =
            await register(registerFormValues);

        if ('data' in registrationResponse) {
            await handleAuthToken(registrationResponse.data);
            await setAuthenticationTimer();
            await refetchRegistrationNeeded();
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
                <Container component="main" maxWidth="xs" sx={containerStyle}>
                    <Stack direction="column" alignItems={'center'} spacing={2}>
                        {renderFormCard()}
                    </Stack>
                </Container>
            </>
        );
    };
    const renderFormCard = () => {
        return (
            <Card variant="outlined" sx={cardStyle(theme)}>
                <BrandHeader sx={{ height: '50px' }} />
                <Typography
                    sx={{ mt: '20px' }}
                    color="text.secondary"
                    gutterBottom>
                    Create a new account:
                </Typography>
                <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        id="username"
                        label="Username"
                        name="username"
                        autoComplete="username"
                        value={registerFormValues.username}
                        onChange={handleRegisterFormValueChange}
                        autoFocus
                        sx={{ bgcolor: 'background.default', mt: 0 }}
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
                </Box>
            </Card>
        );
    };

    const renderSubmitButtonContent = () => {
        if (isLoading) {
            return <MonkeyLoadingIcon />;
        } else if (isSuccess) {
            return 'Success!';
        }
        return 'Register';
    };

    return renderRegisterForm();
};

export default RegisterPage;
