'use client';

import { useUser } from '@clerk/nextjs';
import { useEffect } from 'react';

const UserSync = () => {
  const { isLoaded, isSignedIn, user } = useUser();

  useEffect(() => {
    const syncUserToBackend = async () => {
      if (isLoaded && isSignedIn && user) {
        try {
          const response = await fetch('/api/users', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              id: user.id,
              username: user.username || user.firstName || 'user',
              email: user.primaryEmailAddress?.emailAddress,
              first_name: user.firstName,
              last_name: user.lastName,
            }),
          });

          if (!response.ok) {
            console.error('Failed to sync user to backend:', await response.text());
          }
        } catch (error) {
          console.error('Error syncing user to backend:', error);
        }
      }
    };

    syncUserToBackend();
  }, [isLoaded, isSignedIn, user]);

  // This component doesn't render anything
  return null;
};

export default UserSync;
