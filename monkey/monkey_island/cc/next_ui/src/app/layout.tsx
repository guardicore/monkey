import '../styles/globals.scss';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
    title: 'Infection Monkey',
    description: 'Adversary Emulation Platform'
};

// This lauout is used for all pages including the SSR pages (auth, 404, etc.)
export default function RootLayout({
    children
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body className={inter.className}>{children}</body>
        </html>
    );
}
