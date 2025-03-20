'use client';

import Link from 'next/link';

export default function UserTest() {
  return (
    <div className="mb-6">
      <h2 className="text-lg font-semibold mb-2 text-gray-800 dark:text-white">User Test</h2>
      <div className="space-y-2">
        <Link 
          href="/user-test" 
          className="block p-2 rounded hover:bg-pink-200 dark:hover:bg-pink-800 text-gray-700 dark:text-gray-300"
        >
          User Sync Test
        </Link>
      </div>
    </div>
  );
}
