import '../../styles/globals.scss';
import { RootProvider } from '@/providers/RootProvider';
import MainLayout from '@/layouts/main-layout/MainLayout';

export default function AppLayout({ children }: { children: React.ReactNode }) {
    return (
        <RootProvider>
            <MainLayout>{children}</MainLayout>
        </RootProvider>
    );
}
