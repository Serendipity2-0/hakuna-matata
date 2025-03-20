'use client';
import ContentCalendar from './ContentCalendar';
import Typing from './Typing';
import UserTest from './UserTest';
import { useState, useRef, useEffect } from 'react';

export default function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(true);
  const sidebarRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (sidebarRef.current && !sidebarRef.current.contains(event.target as Node)) {
        setIsCollapsed(true);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleSidebarClick = () => {
    setIsCollapsed(false);
  };

  return (
    <div 
      ref={sidebarRef}
      className={`
        transition-all duration-300 ease-in-out
        min-h-screen bg-pink-100 dark:bg-pink-900 
        border-r border-gray-200 dark:border-gray-700 
        shadow-lg
        ${isCollapsed ? 'w-16' : 'w-[400px]'}
      `}
      onClick={handleSidebarClick}
    >
      {/* Sidebar Header */}
      <div className={`
        p-4 border-b border-gray-200 dark:border-gray-700
        ${isCollapsed ? 'text-center' : ''}
      `}>
        {isCollapsed ? (
          <div className="text-2xl">☰</div>
        ) : (
          <h1 className="text-xl font-bold text-gray-800 dark:text-white">Dashboard</h1>
        )}
      </div>

      {/* Navigation Items */}
      <nav className={`
        p-4 space-y-6
        ${isCollapsed ? 'hidden' : 'block'}
      `}>
        <ContentCalendar />
        <Typing />
        <UserTest />
      </nav>

      {/* Optional: Footer Section */}
      <div className={`
        absolute bottom-0 w-full p-4 
        border-t border-gray-200 dark:border-gray-700
        ${isCollapsed ? 'hidden' : 'block'}
      `}>
        <p className="text-sm text-gray-600 dark:text-gray-400">© 2025 Serendipity</p>
      </div>
    </div>
  );
}
