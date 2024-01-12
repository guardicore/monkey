'use client';
import '../../styles/globals.scss';
import MainLayout from '@/layouts/main-layout/MainLayout';
import { useRouter } from 'next/navigation';
import { tokenStored } from '@/_lib/authentication';
import { PATHS } from '@/constants/paths.constants';
import { Events } from '@/constants/events.constants';
import { useEffect } from 'react';

export default function AppLayout({ children }: { children: React.ReactNode }) {
    const router = useRouter();

    useEffect(() => {
        function checkToken() {
            if (!tokenStored()) {
                router.push(PATHS.SIGN_IN);
            }
        }

        window.addEventListener(Events.LOGOUT, checkToken);

        return () => {
            window.removeEventListener(Events.LOGOUT, checkToken);
        };
    }, [router]);

    return <MainLayout>{children}</MainLayout>;
}
