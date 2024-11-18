// components/withAuth.js
import React, { useEffect, useState } from 'react';
import Router from 'next/router';
import Cookies from 'js-cookie';
import { jwtDecode } from 'jwt-decode';

const withAuth = (WrappedComponent) => {
  const Wrapper = (props) => {
    const [verified, setVerified] = useState(null);
    const [userRole, setUserRole] = useState(null);

    useEffect(() => {
      const verifyToken = async () => {
        const token = Cookies.get('token');
        
        if (!token) {
          console.log('No token found');
          setVerified(false);
          await Router.replace('/login');
          return;
        }

        try {
          const decoded = jwtDecode(token);
          if (!decoded || !decoded.roles) {
            throw new Error('Invalid token structure');
          }
          
          const roles = decoded.roles;
          console.log('Decoded token roles:', roles);
          setUserRole(roles[0]);
          setVerified(true);
        } catch (err) {
          console.error('Token verification failed:', err);
          Cookies.remove('token');
          setVerified(false);
          await Router.replace('/login');
        }
      };

      verifyToken();
    }, []);

    if (verified === null) {
      return (
        <div className="loading-container">
          <p>Loading...</p>
          <style jsx>{`
            .loading-container {
              display: flex;
              justify-content: center;
              align-items: center;
              height: 100vh;
            }
          `}</style>
        </div>
      );
    }

    if (!verified) {
      return null;
    }

    return <WrappedComponent {...props} userRole={userRole} />;
  };

  return Wrapper;
};

export default withAuth;
