'use client';

import { motion } from 'framer-motion';
import dynamic from 'next/dynamic';

const ChatInterface = dynamic(() => import('@/components/ChatInterface'), { ssr: false });

export default function ClientSideHome() {
  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen bg-gradient-to-br from-purple-400 via-pink-500 to-red-500 flex items-center justify-center p-4"
    >
      <motion.div
        initial={{ scale: 0.9, y: 20 }}
        animate={{ scale: 1, y: 0 }}
        transition={{ type: "spring", stiffness: 260, damping: 20 }}
        className="w-full max-w-4xl"
      >
        <ChatInterface />
      </motion.div>
    </motion.div>
  );
}
