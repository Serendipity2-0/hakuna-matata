// components/LogoutButton.js
import Router from 'next/router';
import Cookies from 'js-cookie';

const LogoutButton = () => {
  const handleLogout = () => {
    Cookies.remove('token');
    Router.push('/login');
  };

  return <button onClick={handleLogout}>Logout</button>;
};

export default LogoutButton;
