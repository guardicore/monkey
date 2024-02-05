'use client';
import '../../styles/globals.scss';
import useAuthenticatedRedirect from '@/app/(auth)/_lib/useAuthenticatedRedirect';
import ParticleBackground from '@/app/(auth)/_lib/ParticleBackground';
import { ThemeProvider } from '@mui/material/styles';
import createAuthenticationTheme from '@/app/(auth)/authenticationTheme';
import SVGBackgroundHexagons from '@/app/(auth)/_lib/SVGBackgroundHexagons';
import SVGBackgroundCurves from '@/app/(auth)/_lib/SVGBackgroundCurves';
import SVGBackgroundPolygons from '@/app/(auth)/_lib/SVGBackgroundPolygons';
import React from 'react';

export default function AppLayout({ children }: { children: React.ReactNode }) {
    useAuthenticatedRedirect();

    return (
        <ThemeProvider theme={(theme) => createAuthenticationTheme(theme)}>
            <SVGBackgroundPolygons />
            {children};
        </ThemeProvider>
    );
}
