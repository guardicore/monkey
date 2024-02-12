'use client';
import useAuthenticatedRedirect from '@/app/(auth)/_lib/useAuthenticatedRedirect';
import ParticleBackground from '@/app/(auth)/_lib/ParticleBackground';
import * as React from 'react';

export default function AppLayout({ children }: { children: React.ReactNode }) {
    useAuthenticatedRedirect();

    return (
        <>
            <ParticleBackground />
            {children};
        </>
    );
}
