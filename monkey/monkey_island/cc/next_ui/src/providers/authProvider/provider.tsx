'use client';

import { ReactNode } from 'react';
import { setAuthenticationTimer } from '@/redux/features/api/authentication/lib/authenticationTimer';

export function AuthProvider({ children }: { children: ReactNode }) {
    setAuthenticationTimer();
    return children;
}
