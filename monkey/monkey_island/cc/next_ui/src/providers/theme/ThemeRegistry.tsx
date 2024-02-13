'use client';
import * as React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import appTheme from '@/providers/theme/appTheme';
import { CssBaseline } from '@mui/material';

export default function ThemeRegistry({
    children
}: {
    children: React.ReactNode;
}) {
    return (
        <ThemeProvider theme={appTheme}>
            <CssBaseline />
            {children}
        </ThemeProvider>
    );
}
