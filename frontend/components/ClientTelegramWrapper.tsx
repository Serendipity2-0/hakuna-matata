'use client';

import dynamic from 'next/dynamic';

const TelegramChatBox = dynamic(() => import('@/components/TelegramChatBox'), { 
  ssr: false 
});

export default function ClientTelegramWrapper() {
  return <TelegramChatBox />;
}