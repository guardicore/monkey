'use client';

import { ReactNode, useEffect } from 'react';
import { signOut, useSession } from 'next-auth/react';
import { AUTH_PATHS } from '@/constants/paths.constants';

const UNAUTHENTICATED: string = 'unauthenticated';

const isPathInAuthPaths = (path: string) => {
    // @ts-ignore
    return Object.values(AUTH_PATHS).includes(path);
};

const isSessionHasError = (data: any) => {
    if (data && data?.error) {
        return true;
    }
    return false;
};

export function AuthProvider({ children }: { children: ReactNode }) {
    const { status, data } = useSession();

    useEffect(() => {
        const currentPathName: string = window.location.pathname;
        isSessionHasError(data);
        if (
            (status === UNAUTHENTICATED || isSessionHasError(data)) &&
            !isPathInAuthPaths(currentPathName)
        ) {
            signOut({ callbackUrl: AUTH_PATHS.SIGN_IN });
        }
    }, [status]);

    return <>{children}</>;
}
