// 'use client';

// import { motion } from 'framer-motion';
// import dynamic from 'next/dynamic';

// const ChatInterface = dynamic(() => import('@/components/ChatInterface'), { ssr: false });

// export default function ClientSideHome() {
//   return (
//     <motion.div 
//       initial={{ opacity: 0 }}
//       animate={{ opacity: 1 }}
//       transition={{ duration: 0.5 }}
//       className="min-h-screen bg-gradient-to-br from-purple-400 via-pink-500 to-red-500 flex items-center justify-center p-4"
//     >
//       <motion.div
//         initial={{ scale: 0.9, y: 20 }}
//         animate={{ scale: 1, y: 0 }}
//         transition={{ type: "spring", stiffness: 260, damping: 20 }}
//         className="w-full max-w-4xl"
//       >
//         <ChatInterface />
//       </motion.div>
//     </motion.div>
//   );
// }
'use client';

import { motion } from 'framer-motion';
import dynamic from 'next/dynamic';

// Dynamically import the ChatInterface component for client-side rendering only
const ChatInterface = dynamic(() => import('@/components/ChatInterface'), { ssr: false });

export default function ClientSideHome() {
  return (
    <motion.div
      initial={{ opacity: 0 }}                    // Initial opacity for fade-in effect
      animate={{ opacity: 1 }}                    // Target opacity for fade-in effect
      transition={{ duration: 0.5 }}              // Duration of the fade-in transition
      className="min-h-screen bg-gradient-to-br from-purple-400 via-pink-500 to-red-500 flex items-center justify-center p-4"
    >
      <motion.div
        initial={{ scale: 0.9, y: 20 }}           // Initial scale and position for entrance effect
        animate={{ scale: 1, y: 0 }}              // Target scale and position for entrance effect
        transition={{ type: "spring", stiffness: 260, damping: 20 }}  // Spring animation for smooth entrance
        className="w-full max-w-4xl bg-white p-6 rounded-lg shadow-lg" // Styling for the inner container
      >
        <ChatInterface />                          {/* Render the ChatInterface component */}
      </motion.div>
    </motion.div>
  );
}
