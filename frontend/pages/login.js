// pages/login.js
import { useState, useEffect } from 'react';
import Router from 'next/router';
import Cookies from 'js-cookie';
import qs from 'qs';
import axiosInstance from '../utils/axios';

const LoginPage = () => {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Check if user is already logged in
    const token = Cookies.get('token');
    if (token) {
      Router.replace('/dashboard');
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const data = {
        username: phoneNumber,
        password: password,
      };
      
      const response = await axiosInstance.post(
        '/login',
        qs.stringify(data),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );
      
      const { access_token } = response.data;
      
      if (!access_token) {
        throw new Error('No token received from server');
      }

      // Store the token
      Cookies.set('token', access_token, {
        path: '/',
        sameSite: 'Lax',
        secure: process.env.NODE_ENV === 'production'
      });

      // Use Router.replace instead of push to prevent back navigation
      await Router.replace('/dashboard');
      
    } catch (err) {
      console.error('Login Error:', err);
      setError(err.response?.data?.detail || 'An error occurred during login.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Phone Number:
          <input
            type="text"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            required
            placeholder="Enter your phone number"
          />
        </label>
        <br />
        <label>
          Password:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            placeholder="Enter your password"
          />
        </label>
        <br />
        {error && <p className="error">{error}</p>}
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      <style jsx>{`
        .container {
          max-width: 400px;
          margin: 0 auto;
          padding-top: 100px;
        }
        .error {
          color: red;
          margin: 10px 0;
        }
        input {
          width: 100%;
          padding: 8px;
          margin-top: 4px;
          margin-bottom: 12px;
          box-sizing: border-box;
        }
        button {
          width: 100%;
          padding: 10px;
          background-color: #0070f3;
          color: white;
          border: none;
          cursor: pointer;
        }
        button:hover {
          background-color: #0059c1;
        }
      `}</style>
    </div>
  );
};

export default LoginPage;