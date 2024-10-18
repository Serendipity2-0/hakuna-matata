import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import dynamic from 'next/dynamic';

const inter = Inter({ subsets: ['latin'] });

const TelegramChatBox = dynamic(() => import('@/components/TelegramChatBox'), { ssr: false });

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
        <TelegramChatBox />
      </body>
    </html>
  );
}
