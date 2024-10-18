import { useEffect, useCallback } from 'react';

type ShortcutHandlers = {
  resetToHome: () => void;
  openTelegramBubble: () => void;
  closeModal: () => void;
};

export const useKeyboardShortcuts = ({
  resetToHome,
  openTelegramBubble,
  closeModal,
}: ShortcutHandlers) => {
  const handleKeyPress = useCallback(
    (event: KeyboardEvent) => {
      if (event.ctrlKey && event.key === 'h') {
        event.preventDefault();
        resetToHome();
      } else if (event.ctrlKey && event.key === 't') {
        event.preventDefault();
        openTelegramBubble();
      } else if (event.key === 'Escape') {
        closeModal();
      }
    },
    [resetToHome, openTelegramBubble, closeModal]
  );

  useEffect(() => {
    window.addEventListener('keydown', handleKeyPress);
    return () => {
      window.removeEventListener('keydown', handleKeyPress);
    };
  }, [handleKeyPress]);
};
