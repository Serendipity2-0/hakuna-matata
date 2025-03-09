import './globals.css';
import type { Metadata } from 'next';
import ClientTelegramWrapper from '@/components/ClientTelegramWrapper';
import Sidebar from '@/components/Sidebar';
import {
  ClerkProvider,
  SignInButton,
  
  SignedIn,
  SignedOut,
  UserButton,
} from '@clerk/nextjs';
import { GeistSans } from 'geist/font/sans';
import { GeistMono } from 'geist/font/mono';

const geistSans = GeistSans;
const geistMono = GeistMono;

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
    <ClerkProvider>
      <html lang="en">
        <body className={`${geistSans.variable} ${geistMono.variable} bg-background text-foreground antialiased`}>
          <div className="flex flex-col min-h-screen">
            <header className="flex justify-end items-center p-4 gap-4 h-16 border-b">
              <SignedOut>
                <SignInButton />
                
              </SignedOut>
              <SignedIn>
                <UserButton />
              </SignedIn>
            </header>
            <div className="flex flex-1">
              <Sidebar />
              <main className="flex-1">
                {children}
              </main>
            </div>
          </div>
          <ClientTelegramWrapper />
        </body>
      </html>
    </ClerkProvider>
  );
}
