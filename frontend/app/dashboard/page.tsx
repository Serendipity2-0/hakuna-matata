import { Metadata } from 'next';
import ClientPageWrapper from '@/components/ClientPageWrapper';

export const metadata: Metadata = {
  title: 'Serendipity Task Assistant',
  description: 'An AI-powered task assistant with advanced tool selection',
};

export default function Home() {
  return <ClientPageWrapper />;
}
