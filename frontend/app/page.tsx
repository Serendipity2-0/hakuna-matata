import { Metadata } from 'next';
import Link from 'next/link';
import { SignedIn, SignedOut, SignInButton } from '@clerk/nextjs';

export const metadata: Metadata = {
  title: 'Welcome to Serendipity',
  description: 'Your AI-powered task assistant',
};

export default function NewLandingPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      <h1 className="text-4xl font-bold mb-6">Welcome to Serendipity</h1>
      <p className="text-xl mb-8">Your AI-powered task assistant</p>
      
      <div className="space-y-4">
        <SignedIn>
          <Link 
            href="/dashboard" 
            className="block bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg text-center"
          >
            Go to Dashboard
          </Link>
        </SignedIn>
        
        <SignedOut>
          <SignInButton>
            <button className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg">
              Sign In to Get Started
            </button>
          </SignInButton>
        </SignedOut>
      </div>
    </div>
  );
}
