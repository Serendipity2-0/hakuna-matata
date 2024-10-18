import { Metadata } from 'next';
import dynamic from 'next/dynamic';

const ClientSideHome = dynamic(() => import('@/components/ClientSideHome'), {
  ssr: false,
  loading: () => <p>Loading...</p>
});

const DynamicAdaptiveLayout = dynamic(() => import('@/components/AdaptiveLayout'), {
  ssr: false,
});

export const metadata: Metadata = {
  title: 'Serendipity Task Assistant',
  description: 'An AI-powered task assistant with advanced tool selection',
};

export default function Home() {
  return (
    <DynamicAdaptiveLayout>
      <ClientSideHome />
    </DynamicAdaptiveLayout>
  );
}
