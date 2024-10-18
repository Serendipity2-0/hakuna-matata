import { Metadata } from 'next';
import dynamic from 'next/dynamic';

const ClientSideHome = dynamic(() => import('@/components/ClientSideHome'), {
  ssr: false,
  loading: () => <p>Loading...</p>
});

export const metadata: Metadata = {
  title: 'Serendipity Task Assistant',
  description: 'An AI-powered task assistant with advanced tool selection',
};

export default function Home() {
  return <ClientSideHome />;
}
