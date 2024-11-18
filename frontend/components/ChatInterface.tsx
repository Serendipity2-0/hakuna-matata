'use client';

import { useState, useCallback } from 'react';
import dynamic from 'next/dynamic';
import ToolSelector from '@/components/ToolSelector';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { RefreshCw } from 'lucide-react';
import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts';

const RepoInfoInterface = dynamic(() => import('@/components/RepoInfoInterface'), { ssr: false });
const ReconciliationInterface = dynamic(() => import('@/components/ReconciliationInterface'), { ssr: false });
const ScriptWriterInterface = dynamic(() => import('@/components/ScriptWriterInterface'), { ssr: false });

/**
 * ChatInterface component
 * 
 * This component represents the main chat interface of the application.
 * It handles user input, message display, and integration with various modals.
 */
export default function ChatInterface() {
  const [selectedTool, setSelectedTool] = useState<string | null>(null);

  const resetApp = useCallback(() => {
    setSelectedTool(null);
  }, []);

  const openTelegramBubble = useCallback(() => {
    // This function will be implemented in TelegramChatBox
    window.dispatchEvent(new CustomEvent('openTelegramBubble'));
  }, []);

  useKeyboardShortcuts({
    resetToHome: resetApp,
    openTelegramBubble,
    closeModal: resetApp, // In this case, closing the modal is the same as resetting
  });

  const renderToolInterface = () => {
    switch (selectedTool) {
      case 'RepoInfoAgent':
        return <RepoInfoInterface />;
      case 'ReconciliationAgent':
        return <ReconciliationInterface />;
      case 'ScriptWriterAgent':
        return <ScriptWriterInterface />;
      default:
        return null;
    }
  };

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="text-2xl font-bold">Serendipity Task Assistant</CardTitle>
        {selectedTool && (
          <Button variant="outline" size="sm" onClick={resetApp}>
            <RefreshCw className="mr-2 h-4 w-4" /> Reset
          </Button>
        )}
      </CardHeader>
      <CardContent>
        {!selectedTool ? (
          <ToolSelector onToolSelect={setSelectedTool} />
        ) : (
          <div className="mt-8">
            <h2 className="text-xl font-semibold mb-4">{selectedTool}</h2>
            {renderToolInterface()}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
