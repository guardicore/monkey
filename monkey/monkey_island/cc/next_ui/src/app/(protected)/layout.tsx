import '../../styles/globals.scss';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { RootProvider } from '@/providers/RootProvider';
import MainLayout from '@/layouts/main-layout/MainLayout';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
    title: 'Infection Monkey',
    description: 'Adversary Emulation Platform'
};

export default function RootLayout({
    children
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body className={inter.className}>
                <RootProvider>
                    <MainLayout>{children}</MainLayout>
                </RootProvider>
            </body>
        </html>
    );
}
