'use client';
import '../../styles/globals.scss';
import MainLayout from '@/layouts/main-layout/MainLayout';
import useAuthRedirection from '@/app/(protected)/_lib/useAuthRedirection';

export default function AppLayout({ children }: { children: React.ReactNode }) {
    useAuthRedirection();

    return <MainLayout>{children}</MainLayout>;
}
