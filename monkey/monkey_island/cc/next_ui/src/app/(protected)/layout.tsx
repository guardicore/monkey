'use client';
import '../../styles/globals.scss';
import MainLayout from '@/layouts/main-layout/MainLayout';
import { useRouter } from 'next/navigation';
import { tokenStored } from '@/_lib/authentication';
import { PATHS } from '@/constants/paths.constants';

export default function AppLayout({ children }: { children: React.ReactNode }) {
    const router = useRouter();
    if (!tokenStored()) {
        router.push(PATHS.SIGN_IN);
    }
    return <MainLayout>{children}</MainLayout>;
}
