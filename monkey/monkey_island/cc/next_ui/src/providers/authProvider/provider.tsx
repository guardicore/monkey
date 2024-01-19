'use client';

import { ReactNode } from 'react';
import { useDispatch } from 'react-redux';
import { AuthenticationActions } from '@/redux/features/api/authentication/authenticationActions';
import { setTimer } from '@/redux/features/api/authenticationTimeoutSlice';

export function AuthProvider({ children }: { children: ReactNode }) {
    const dispatch = useDispatch();
    const authenticationTimer = setTimeout(() => {
        dispatch(AuthenticationActions.logout);
    }, 1000 * 8);
    setTimer(authenticationTimer);

    return children;
}
