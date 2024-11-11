// app/client-side-home/page.tsx

import dynamic from 'next/dynamic';

// Dynamically import ClientSideHome with no server-side rendering
const ClientSideHome = dynamic(() => import('@/components/ClientSideHome'), { ssr: false });

export default function ClientSideHomePage() {
    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <ClientSideHome />
        </div>
    );
}
