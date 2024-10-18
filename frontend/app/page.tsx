import dynamic from 'next/dynamic';
import { Metadata } from 'next';

const ChatInterface = dynamic(() => import('@/components/ChatInterface'), { ssr: false });

export const metadata: Metadata = {
  title: 'Serendipity Task Assistant',
  description: 'An AI-powered task assistant with advanced tool selection',
};

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <ChatInterface />
    </div>
  );
}
