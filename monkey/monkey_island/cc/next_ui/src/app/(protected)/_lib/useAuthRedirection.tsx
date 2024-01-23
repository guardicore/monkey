'use client';
import { useRouter } from 'next/navigation';
import { tokenStored } from '@/_lib/authentication';
import { PATHS } from '@/constants/paths.constants';
import { Events } from '@/constants/events.constants';
import { useEffect } from 'react';

export default function useAuthRedirection() {
    const router = useRouter();

    function checkToken() {
        if (!tokenStored()) {
            router.push(PATHS.SIGN_IN);
        }
    }

    useEffect(() => {
        checkToken();
        window.addEventListener(Events.LOGOUT, checkToken);

        return () => {
            window.removeEventListener(Events.LOGOUT, checkToken);
        };
    });
}
