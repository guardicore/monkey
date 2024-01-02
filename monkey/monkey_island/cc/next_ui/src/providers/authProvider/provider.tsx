'use client';

import { ReactNode, useEffect } from 'react';
import { signOut, useSession } from 'next-auth/react';
import { Session } from 'next-auth';
import { PATHS, PROTECTED_PATHS } from '@/constants/paths.constants';
import { AUTH_STATUS } from '@/constants/authStatus.constants';

const pathIsProtected = (path: string) => {
    // @ts-ignore
    return PROTECTED_PATHS.includes(path);
};

const isSessionHasError = (session: Session) => {
    return !!session?.error;
};

export function AuthProvider({ children }: { children: ReactNode }) {
    const { status, data } = useSession();

    useEffect(() => {
        const currentPathName: string = window.location.pathname;

        if (
            (status === AUTH_STATUS.UNAUTHENTICATED ||
                isSessionHasError(data)) &&
            !pathIsProtected(currentPathName)
        ) {
            signOut({ callbackUrl: PATHS.SIGN_IN });
        }
    }, [status, data]);

    return <>{children}</>;
}
