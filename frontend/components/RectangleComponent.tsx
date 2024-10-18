'use client';

import React, { useState, useEffect } from 'react';

interface RectangleProps {
  position: 'top' | 'right' | 'bottom' | 'left';
  shortcut: string;
}

const RectangleComponent: React.FC<RectangleProps> = ({ position, shortcut }) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === shortcut) {
        event.preventDefault();
        setIsVisible((prev) => !prev);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [shortcut]);

  const getPositionStyle = () => {
    const baseStyle = {
      position: 'fixed',
      backgroundColor: 'rgba(0, 0, 255, 1)', // Fully opaque
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      transition: 'all 0.3s ease-in-out',
      zIndex: 1000,
    };

    switch (position) {
      case 'top':
        return { ...baseStyle, top: isVisible ? '0' : '-50%', left: '0', width: '100%', height: '50%' };
      case 'right':
        return { ...baseStyle, top: '0', right: isVisible ? '0' : '-50%', width: '50%', height: '100%' };
      case 'bottom':
        return { ...baseStyle, bottom: isVisible ? '0' : '-50%', left: '0', width: '100%', height: '50%' };
      case 'left':
        return { ...baseStyle, top: '0', left: isVisible ? '0' : '-50%', width: '50%', height: '100%' };
    }
  };

  return (
    <div style={getPositionStyle() as React.CSSProperties}>
      <button onClick={() => alert('To be implemented')}>
        Click me ({position})
      </button>
    </div>
  );
};

export default RectangleComponent;
