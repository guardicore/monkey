'use client';
import '../../styles/globals.scss';
import useAuthenticatedRedirect from '@/app/(auth)/_lib/useAuthenticatedRedirect';
import ParticleBackground from '@/app/(auth)/_lib/ParticleBackground';
import * as React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import createAuthenticationTheme from '@/app/(auth)/authenticationTheme';

export default function AppLayout({ children }: { children: React.ReactNode }) {
    useAuthenticatedRedirect();

    return (
        <ThemeProvider theme={(theme) => createAuthenticationTheme(theme)}>
            <ParticleBackground />
            {children};
        </ThemeProvider>
    );
}
