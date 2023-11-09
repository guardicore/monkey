import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import ThemeRegistry from '@/theme/ThemeRegistry';
import { ReduxProvider } from '@/redux/provider';
import { NextAuthProvider } from '@/nextAuthProvider/provider';

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
                <NextAuthProvider>
                    <ReduxProvider>
                        <ThemeRegistry>{children}</ThemeRegistry>
                    </ReduxProvider>
                </NextAuthProvider>
            </body>
        </html>
    );
}
