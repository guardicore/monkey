'use client';
import { useRouter } from 'next/navigation'
import { Button } from '@mui/material';
import React from 'react';
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
import {useEffect, useState} from 'react';

const RegistrationPage = () => {

    const [successfulRegistration, setSuccessfulRegistration] = useState(false);
    const router = useRouter()

    useEffect(() => {
        if (successfulRegistration) {
            router.push("/")
        }
    }, [successfulRegistration])

    const register = async (registrationFormValues: any) => {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(registrationFormValues)
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data)
            localStorage.setItem('authentication_token', data.response.user.authentication_token);
            setSuccessfulRegistration(true)
        } else {
            console.log('Registration failed.');
        }
    }

    const [loading, setLoading] = React.useState(false);

    const [registrationFormValues, setRegistrationFormValues] = React.useState({
        username: '',
        password: ''
    });

    const handleSubmit = async (event: any) => {
        event.preventDefault();
        await register(registrationFormValues);
    };

    const handleRegistrationFormValueChange = (e: any) => {
        const name = e.target.name;
        const value =
            e.target.type === 'checkbox' ? e.target.checked : e.target.value;
        setRegistrationFormValues({ ...registrationFormValues, [name]: value });
    };

    const renderRegistrationForm = () => {
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
                            Registration
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
                                value={registrationFormValues.username}
                                onChange={handleRegistrationFormValueChange}
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
                                value={registrationFormValues.password}
                                onChange={handleRegistrationFormValueChange}
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
                                disabled={loading}
                                type="submit"
                                fullWidth
                                variant="contained"
                                sx={{ mt: 3, mb: 2 }}>
                                {loading ? 'Loading...' : 'Register'}
                            </Button>

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

    return renderRegistrationForm();
};

export default RegistrationPage;
