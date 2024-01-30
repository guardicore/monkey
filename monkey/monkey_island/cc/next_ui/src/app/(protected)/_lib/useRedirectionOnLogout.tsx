'use client';
import { useRouter } from 'next/navigation';
import { tokenIsStored } from '@/lib/authenticationToken';
import { PATHS } from '@/constants/paths.constants';
import { Events } from '@/constants/events.constants';
import { useEffect } from 'react';

export default function useRedirectionOnLogout() {
    const router = useRouter();
    const checkToken = () => {
        if (!tokenIsStored()) {
            router.push(PATHS.REGISTRATION);
        }
    };

    useEffect(() => {
        window.addEventListener(Events.LOGOUT, checkToken);

        return () => {
            window.removeEventListener(Events.LOGOUT, checkToken);
        };
    });
}
