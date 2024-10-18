import dynamic from 'next/dynamic';
import { Metadata } from 'next';
import HumanReviewModal from '@/components/HumanReviewModal';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import WorkingDirectoryModal from '@/components/WorkingDirectoryModal';

const GitCommitInterface = dynamic(() => import('@/components/GitCommitInterface'), { ssr: false });
const ChatInterface = dynamic(() => import('@/components/ChatInterface'), { ssr: false });

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
