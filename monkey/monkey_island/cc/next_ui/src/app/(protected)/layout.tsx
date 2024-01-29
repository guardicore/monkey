'use client';
import '../../styles/globals.scss';
import MainLayout from '@/layouts/main-layout/MainLayout';
import useRedirectionOnLogout from '@/app/(protected)/_lib/useRedirectionOnLogout';
import useRedirectionWhenUnauthenticated from '@/app/(protected)/_lib/useRedirectionWhenUnauthenticated';

export default function AppLayout({ children }: { children: React.ReactNode }) {
    useRedirectionOnLogout();
    useRedirectionWhenUnauthenticated();

    return <MainLayout>{children}</MainLayout>;
}
