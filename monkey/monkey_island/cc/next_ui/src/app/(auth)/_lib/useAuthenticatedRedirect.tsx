'use client';
import { useRouter } from 'next/navigation';
import { tokenIsStored } from '@/lib/authenticationToken';
import { PATHS } from '@/constants/paths.constants';
import { useEffect } from 'react';

export default function useAuthenticatedRedirect() {
    const router = useRouter();

    useEffect(() => {
        if (tokenIsStored()) {
            router.push(PATHS.ROOT);
        }
    });
}
