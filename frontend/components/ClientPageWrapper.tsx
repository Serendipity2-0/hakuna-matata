'use client';

import React, { Suspense } from 'react';
import dynamic from 'next/dynamic';

const ClientSideHome = dynamic(() => import('@/components/ClientSideHome'), {
  ssr: false,
  loading: () => <p>Loading...</p>
});

const DynamicAdaptiveLayout = dynamic(() => import('@/components/AdaptiveLayout'), {
  ssr: false,
  loading: () => <p>Loading layout...</p>
});

export default function ClientPageWrapper() {
  return (
    <Suspense fallback={<p>Loading...</p>}>
      <DynamicAdaptiveLayout>
        <ClientSideHome />
      </DynamicAdaptiveLayout>
    </Suspense>
  );
}
