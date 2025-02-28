import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import ClientTelegramWrapper from '@/components/ClientTelegramWrapper';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Serendipity Task Assistant',
  description: 'An AI-powered task assistant with advanced tool selection',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-background text-foreground`}>
        {children}
        <ClientTelegramWrapper />
      </body>
    </html>
  );
}
