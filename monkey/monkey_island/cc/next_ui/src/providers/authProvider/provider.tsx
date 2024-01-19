'use client';

import { ReactNode } from 'react';
import setAuthenticationTimer from '@/app/(auth)/_lib/setAuthenticationTimer';

export function AuthProvider({ children }: { children: ReactNode }) {
    setAuthenticationTimer();
    return children;
}
