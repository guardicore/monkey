'use client';

import { ReactNode } from 'react';
import { ReduxProvider } from '@/providers/reduxProvider/provider';
import ThemeRegistry from '@/providers/theme/ThemeRegistry';

export function RootProvider({ children }: { children: ReactNode }) {
    return (
        <>
            <ReduxProvider>
                <ThemeRegistry>{children}</ThemeRegistry>
            </ReduxProvider>
        </>
    );
}
