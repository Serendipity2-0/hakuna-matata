'use client';

import { useUser } from '@clerk/nextjs';
import { useState, useEffect } from 'react';

export default function UserTestPage() {
  const { isLoaded, isSignedIn, user } = useUser();
  const [backendUser, setBackendUser] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchUserFromBackend = async () => {
    if (!isLoaded || !isSignedIn || !user) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`/api/users?id=${user.id}`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch user: ${await response.text()}`);
      }
      
      const data = await response.json();
      setBackendUser(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      console.error('Error fetching user from backend:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isLoaded && isSignedIn && user) {
      fetchUserFromBackend();
    }
  }, [isLoaded, isSignedIn, user]);

  if (!isLoaded) {
    return <div className="p-4">Loading...</div>;
  }

  if (!isSignedIn) {
    return <div className="p-4">Please sign in to view this page.</div>;
  }

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">User Synchronization Test</h1>
      
      <div className="mb-8 p-4 border rounded-lg">
        <h2 className="text-xl font-semibold mb-2">Clerk User Information</h2>
        <div className="grid grid-cols-2 gap-2">
          <div className="font-medium">User ID:</div>
          <div>{user.id}</div>
          
          <div className="font-medium">Username:</div>
          <div>{user.username || '(not set)'}</div>
          
          <div className="font-medium">Email:</div>
          <div>{user.primaryEmailAddress?.emailAddress || '(not set)'}</div>
          
          <div className="font-medium">First Name:</div>
          <div>{user.firstName || '(not set)'}</div>
          
          <div className="font-medium">Last Name:</div>
          <div>{user.lastName || '(not set)'}</div>
        </div>
      </div>
      
      <div className="mb-4 p-4 border rounded-lg">
        <h2 className="text-xl font-semibold mb-2">Backend User Information</h2>
        
        {loading ? (
          <div>Loading backend user data...</div>
        ) : error ? (
          <div className="text-red-500">{error}</div>
        ) : backendUser ? (
          <div className="grid grid-cols-2 gap-2">
            <div className="font-medium">User ID:</div>
            <div>{backendUser.id}</div>
            
            <div className="font-medium">Username:</div>
            <div>{backendUser.username || '(not set)'}</div>
            
            <div className="font-medium">Email:</div>
            <div>{backendUser.email || '(not set)'}</div>
            
            <div className="font-medium">First Name:</div>
            <div>{backendUser.first_name || '(not set)'}</div>
            
            <div className="font-medium">Last Name:</div>
            <div>{backendUser.last_name || '(not set)'}</div>
          </div>
        ) : (
          <div>No backend user data found.</div>
        )}
      </div>
      
      <button
        onClick={fetchUserFromBackend}
        disabled={loading}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
      >
        {loading ? 'Loading...' : 'Refresh Backend Data'}
      </button>
    </div>
  );
}
