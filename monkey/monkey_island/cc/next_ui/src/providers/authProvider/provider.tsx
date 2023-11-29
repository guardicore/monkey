'use client';

import { ReactNode, useEffect } from 'react';
import { signOut, useSession } from 'next-auth/react';
import { AUTHENTICATION_PATHS, PATHS } from '@/constants/paths.constants';
import { AUTH_STATUS } from '@/constants/authStatus.constants';

const isPathInAuthPaths = (path: string) => {
    // @ts-ignore
    return AUTHENTICATION_PATHS.includes(path);
};

const isSessionHasError = (data: any) => {
    return !!(data && data?.error);
};

export function AuthProvider({ children }: { children: ReactNode }) {
    const { status, data } = useSession();

    useEffect(() => {
        const currentPathName: string = window.location.pathname;
        isSessionHasError(data);
        if (
            (status === AUTH_STATUS.UNAUTHENTICATED ||
                isSessionHasError(data)) &&
            !isPathInAuthPaths(currentPathName)
        ) {
            signOut({ callbackUrl: PATHS.SIGN_IN });
        }
    }, [status, data]);

    return <>{children}</>;
}
