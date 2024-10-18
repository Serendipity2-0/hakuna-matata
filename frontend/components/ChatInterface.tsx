'use client';

import { useState } from 'react';
import dynamic from 'next/dynamic';
import ToolSelector from '@/components/ToolSelector';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

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
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-center">Task Assistant</CardTitle>
      </CardHeader>
      <CardContent>
        <ToolSelector onToolSelect={setSelectedTool} />
        {selectedTool && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold mb-4">{selectedTool}</h2>
            {renderToolInterface()}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
