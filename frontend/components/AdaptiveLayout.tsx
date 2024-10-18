'use client';

import React, { useState, useEffect } from 'react';
import RectangleComponent from './RectangleComponent';

const AdaptiveLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [activeRectangle, setActiveRectangle] = useState<string | null>(null);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.ctrlKey || event.metaKey) {
        switch (event.key.toLowerCase()) {
          case 'w':
            setActiveRectangle(prev => prev === 'top' ? null : 'top');
            break;
          case 'd':
            setActiveRectangle(prev => prev === 'right' ? null : 'right');
            break;
          case 's':
            setActiveRectangle(prev => prev === 'bottom' ? null : 'bottom');
            break;
          case 'a':
            setActiveRectangle(prev => prev === 'left' ? null : 'left');
            break;
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const getMainContentStyle = () => {
    const baseStyle = {
      transition: 'all 0.3s ease-in-out',
      position: 'absolute',
      overflow: 'auto',
    };

    switch (activeRectangle) {
      case 'top':
        return { ...baseStyle, top: '50%', left: '0', width: '100%', height: '50%' };
      case 'right':
        return { ...baseStyle, top: '0', left: '0', width: '50%', height: '100%' };
      case 'bottom':
        return { ...baseStyle, top: '0', left: '0', width: '100%', height: '50%' };
      case 'left':
        return { ...baseStyle, top: '0', left: '50%', width: '50%', height: '100%' };
      default:
        return { ...baseStyle, top: '0', left: '0', width: '100%', height: '100%' };
    }
  };

  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative', overflow: 'hidden' }}>
      <div style={getMainContentStyle() as React.CSSProperties}>
        {children}
      </div>
      <RectangleComponent position="top" shortcut="w" />
      <RectangleComponent position="right" shortcut="d" />
      <RectangleComponent position="bottom" shortcut="s" />
      <RectangleComponent position="left" shortcut="a" />
    </div>
  );
};

export default AdaptiveLayout;
