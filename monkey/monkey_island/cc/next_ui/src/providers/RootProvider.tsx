'use client';

import { ReactNode } from 'react';
import { NextAuthProvider } from '@/providers/nextAuthProvider/provider';
import { AuthProvider } from '@/providers/authProvider/provider';
import { ReduxProvider } from '@/providers/reduxProvider/provider';
import ThemeRegistry from '@/providers/theme/ThemeRegistry';

export function RootProvider({ children }: { children: ReactNode }) {
    return (
        <>
            <NextAuthProvider>
                <AuthProvider>
                    <ReduxProvider>
                        <ThemeRegistry>{children}</ThemeRegistry>
                    </ReduxProvider>
                </AuthProvider>
            </NextAuthProvider>
        </>
    );
}
