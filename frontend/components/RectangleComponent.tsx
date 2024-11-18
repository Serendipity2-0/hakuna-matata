'use client';

import React, { useState, useEffect } from 'react';
import AssistantChat from './AssistantChat';

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
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      transition: 'all 0.3s ease-in-out',
      zIndex: 1000,
      opacity: isVisible ? 0.9 : 1,
    };

    const getBackgroundColor = () => {
      switch (position) {
        case 'top':
          return 'linear-gradient(to bottom, #f0f0f0, #d0d0d0)';
        case 'right':
          return 'rgba(255, 200, 200, 1)';
        case 'bottom':
          return 'rgba(200, 255, 200, 1)';
        case 'left':
          return 'rgba(200, 200, 255, 1)';
      }
    };

    switch (position) {
      case 'top':
        return { ...baseStyle, top: isVisible ? '0' : '-100%', left: '0', width: '100%', height: '100%', background: getBackgroundColor() };
      case 'right':
        return { ...baseStyle, top: '0', right: isVisible ? '0' : '-100%', width: '100%', height: '100%', backgroundColor: getBackgroundColor() };
      case 'bottom':
        return { ...baseStyle, bottom: isVisible ? '0' : '-100%', left: '0', width: '100%', height: '100%', backgroundColor: getBackgroundColor() };
      case 'left':
        return { ...baseStyle, top: '0', left: isVisible ? '0' : '-100%', width: '100%', height: '100%', backgroundColor: getBackgroundColor() };
    }
  };

  return (
    <div style={getPositionStyle() as React.CSSProperties} data-testid={`${position}-rectangle`}>
      {position === 'bottom' ? (
        <AssistantChat />
      ) : (
        <button onClick={() => alert('To be implemented')}>
          Click me ({position})
        </button>
      )}
    </div>
  );
};

export default RectangleComponent;
