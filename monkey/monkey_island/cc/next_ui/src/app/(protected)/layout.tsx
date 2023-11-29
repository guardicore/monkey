import '../../styles/globals.scss';
import MainLayout from '@/layouts/main-layout/MainLayout';

export default function AppLayout({ children }: { children: React.ReactNode }) {
    return <MainLayout>{children}</MainLayout>;
}
