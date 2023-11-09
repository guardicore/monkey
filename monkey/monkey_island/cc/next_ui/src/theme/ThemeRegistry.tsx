'use client';
import * as React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import NextAppDirEmotionCacheProvider from './EmotionCache';
import { deepmerge } from '@mui/utils';
import { useSelector } from 'react-redux';
import { RootState } from '@/redux/store';
import { useMemo } from 'react';
import themeOptions from './theme';

export default function ThemeRegistry({
    children
}: {
    children: React.ReactNode;
}) {
    const defaultThemeOptions = deepmerge({}, themeOptions);
    const themeAppearance = useSelector(
        (state: RootState) => state.theme.themeAppearance
    );

    const currentTheme = useMemo(
        () =>
            createTheme(
                deepmerge(defaultThemeOptions, {
                    palette: {
                        mode: themeAppearance
                    }
                })
            ),
        // eslint-disable-next-line react-hooks/exhaustive-deps
        [themeAppearance]
    );

    return (
        <NextAppDirEmotionCacheProvider options={{ key: 'mui' }}>
            <ThemeProvider theme={currentTheme}>
                {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
                <CssBaseline />
                {children}
            </ThemeProvider>
        </NextAppDirEmotionCacheProvider>
    );
}
