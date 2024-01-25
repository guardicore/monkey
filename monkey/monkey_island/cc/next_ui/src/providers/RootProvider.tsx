'use client';

import { ReactNode } from 'react';
import { ReduxProvider } from '@/providers/reduxProvider/provider';
import ThemeRegistry from '@/providers/theme/ThemeRegistry';
import { AuthProvider } from '@/providers/authProvider/provider';
import { RepositoryProvider } from '@/providers/repositoryProvider/provider';

export function RootProvider({ children }: { children: ReactNode }) {
    return (
        <>
            <ReduxProvider>
                <RepositoryProvider>
                    <AuthProvider>
                        <ThemeRegistry>{children}</ThemeRegistry>
                    </AuthProvider>
                </RepositoryProvider>
            </ReduxProvider>
        </>
    );
}
