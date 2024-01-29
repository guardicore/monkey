'use client';

import { ReactNode } from 'react';
import { setAuthenticationTimer } from '@/redux/features/api/authentication/_lib/authenticationTimer';

export function AuthProvider({ children }: { children: ReactNode }) {
    setAuthenticationTimer();
    return children;
}
