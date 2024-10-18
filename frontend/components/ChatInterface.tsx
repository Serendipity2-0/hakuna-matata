'use client';

import { useState } from 'react';
import dynamic from 'next/dynamic';
import ToolSelector from '@/components/ToolSelector';

const GitCommitInterface = dynamic(() => import('@/components/GitCommitInterface'), { ssr: false });
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

  const renderToolInterface = () => {
    switch (selectedTool) {
      case 'GitCommitterAgent':
        return <GitCommitInterface />;
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
    <div className="flex flex-col space-y-4">
      <ToolSelector onToolSelect={setSelectedTool} />
      {selectedTool && (
        <div className="mt-8">
          <h2 className="text-2xl font-bold mb-4">{selectedTool}</h2>
          {renderToolInterface()}
        </div>
      )}
    </div>
  );
}
