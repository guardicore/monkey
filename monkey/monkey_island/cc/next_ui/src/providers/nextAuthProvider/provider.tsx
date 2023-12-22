'use client';
import { SessionProvider } from 'next-auth/react';
import { ReactNode } from 'react';

export function NextAuthProvider({ children }: { children: ReactNode }) {
    // refetchInterval - How often should the data be refetched (in seconds). When set to 0, polling is disabled.
    return (
        <SessionProvider
            refetchOnWindowFocus={true}
            refetchInterval={5 * 60}
            refetchWhenOffline={false}>
            {children}
        </SessionProvider>
    );
}
