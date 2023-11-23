'use client';

import { ReactNode } from 'react';
import { NextAuthProvider } from '@/providers/nextAuthProvider/provider';
import { AuthProvider } from '@/providers/authProvider/provider';
import { ReduxProvider } from '@/providers/reduxProvider/provider';
import ThemeRegistry from '@/providers/theme/ThemeRegistry';

const getProviders = (children: ReactNode) => {
    return (
        <>
            <ReduxProvider>
                <ThemeRegistry>{children}</ThemeRegistry>
            </ReduxProvider>
        </>
    );
};
const getProductionProviders = (children: ReactNode) => {
    return (
        <>
            <NextAuthProvider>
                <AuthProvider>{getProviders(children)}</AuthProvider>
            </NextAuthProvider>
        </>
    );
};

const getDevelopmentProviders = (children: ReactNode) => {
    return (
        <>
            <NextAuthProvider>{getProviders(children)}</NextAuthProvider>
        </>
    );
};

export function RootProvider({ children }: { children: ReactNode }) {
    const isProduction =
        process.env.NODE_ENV === process.env.NEXT_PUBLIC_PRODUCTION_KEY;
    if (isProduction) {
        return getProductionProviders(children);
    }
    return getDevelopmentProviders(children);
}
