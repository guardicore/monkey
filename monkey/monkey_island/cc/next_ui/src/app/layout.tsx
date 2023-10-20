import './globals.css';
import type {Metadata} from 'next';
import {Inter} from 'next/font/google';
import {ReduxProvider} from '@/features/provider';

const inter = Inter({subsets: ['latin']});

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
            <ReduxProvider>
                <body className={inter.className}>
                    <h1>Infection Monkey</h1>
                    {children}
                </body>
            </ReduxProvider>
        </html>
    );
}
