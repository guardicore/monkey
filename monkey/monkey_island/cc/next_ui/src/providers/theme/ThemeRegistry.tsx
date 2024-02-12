'use client';
import * as React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import appTheme from '@/providers/theme/appTheme';

export default function ThemeRegistry({
    children
}: {
    children: React.ReactNode;
}) {
    return <ThemeProvider theme={appTheme}>{children}</ThemeProvider>;
}
