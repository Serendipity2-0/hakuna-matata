"use client";

import Header from '@/components/Header';
import Button from '@/components/Button';
import { useRouter } from 'next/navigation';
import ClientSideHome from '@/components/ClientSideHome';

export default function HomeContent() {
    const router = useRouter();

    const handleGetStarted = () => {
        router.push('/register');
    };

    return (
        <div className="min-h-screen flex flex-col bg-black text-white">
            <Header />

            <main className="flex flex-col items-center justify-center flex-grow text-center p-8">
                <h1 className="text-6xl md:text-7xl font-bold mb-8 max-w-4xl leading-tight">
                    Documentation brings clarity to department
                </h1>
                <p className="text-xl text-gray-400 max-w-2xl mb-12">
                    Documentation serves as a vital tool for fostering clarity within a department by ensuring that
                    <span className="text-white"> processes, roles, and guidelines</span> are easily accessible and understood by all team members.
                </p>
                <div className="flex gap-4">
                    <Button
                        label="Get Started"
                        onClick={handleGetStarted}
                        className="bg-white text-black hover:bg-gray-100 border-0"
                    />
                    <Button
                        label="Learn more"
                        className="bg-transparent border-white hover:bg-gray-900"
                    />
                </div>
            </main>

            {/* <ClientSideHome /> */}
        </div>
    );
}
