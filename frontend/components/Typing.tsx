'use client';
import { useRouter } from 'next/navigation';

export default function Typing() {
  const router = useRouter();

  const handleClick = () => {
    router.push('/Typing');
  };

  return (
    <div 
      className="p-3 cursor-pointer hover:bg-gray-200 dark:hover:bg-gray-700 rounded-lg transition-all"
      onClick={handleClick}
    >
      <div className="flex items-center space-x-3">
        <svg 
          className="w-5 h-5 text-gray-600 dark:text-gray-300" 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            strokeWidth={2} 
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" 
          />
        </svg>
        <h2 className="text-lg font-medium text-gray-700 dark:text-gray-200">Typing Test</h2>
      </div>
    </div>
  );
}
