import dynamic from 'next/dynamic';
import ChatInterface from '@/components/ChatInterface';
import { Metadata } from 'next';

const GitCommitInterface = dynamic(() => import('@/components/GitCommitInterface'), { ssr: false });

export const metadata: Metadata = {
  title: 'Task Assistant Chatbot',
  description: 'An AI-powered chatbot with human-in-the-loop capabilities',
};

export default function Home() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6 text-center">Task Assistant</h1>
      <ChatInterface />
      <GitCommitInterface />
    </div>
  );
}
