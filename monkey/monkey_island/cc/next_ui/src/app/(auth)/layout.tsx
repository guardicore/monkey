'use client';
import '../../styles/globals.scss';
import useAuthenticatedRedirect from '@/app/(auth)/_lib/useAuthenticatedRedirect';

export default function AppLayout({ children }: { children: React.ReactNode }) {
    useAuthenticatedRedirect();

    return children;
}
