'use client';
import { useRouter } from 'next/navigation';
import { tokenIsStored } from '@/lib/authenticationToken';
import { PATHS } from '@/constants/paths.constants';
import { useEffect } from 'react';
import { useRegistrationStatusQuery } from '@/redux/features/api/authentication/authenticationEndpoints';

export default function useRedirectionWhenUnauthenticated() {
    const router = useRouter();
    const { data: registrationStatus, isLoading } =
        useRegistrationStatusQuery();

    useEffect(() => {
        if (isLoading) {
            return;
        }
        if (registrationStatus?.registrationNeeded) {
            router.push(PATHS.REGISTRATION);
        } else if (!tokenIsStored()) {
            router.push(PATHS.LOGIN);
        }
    }, [router, isLoading, registrationStatus]);
}
