import '../styles/globals.scss';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { RootProvider } from '@/providers/RootProvider';
import { AuthRefresh } from '@/_components/auth-refresh/AuthRefresh';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
    title: 'Infection Monkey',
    description: 'Adversary Emulation Platform'
};

// This layout is used for all pages including the SSR pages (auth, 404, etc.)
export default function RootLayout({
    children
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body className={inter.className}>
                <RootProvider>
                    <AuthRefresh>{children}</AuthRefresh>
                </RootProvider>
            </body>
        </html>
    );
}
