'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Loader2 } from 'lucide-react';
import EditableMarkdown from '@/components/EditableMarkdown';

/**
 * GitCommitInterface component for generating git commit messages.
 * 
 * This component provides a form for users to input their working directory
 * and task summary, then generates a commit message based on this input.
 */
export default function GitCommitInterface() {
  const [directory, setDirectory] = useState('');
  const [taskSummary, setTaskSummary] = useState('');
  const [commitMessage, setCommitMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  /**
   * Handles the form submission to generate a commit message.
   * 
   * @param {React.FormEvent} e - The form submission event.
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setCommitMessage('');

    try {
      const response = await fetch('http://localhost:8000/api/git_commit_message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ directory, guidelines: taskSummary }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setCommitMessage(data.commit_message.commit_message);
    } catch (error) {
      console.error('Error generating commit message:', error);
      setError('Failed to generate commit message. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="text-2xl font-bold">Generate Git Commit Message</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="directory" className="block text-sm font-medium text-gray-700 mb-1">Working Directory:</label>
            <Input
              id="directory"
              value={directory}
              onChange={(e) => setDirectory(e.target.value)}
              placeholder="e.g., /path/to/your/repo"
              required
              className="w-full"
            />
          </div>
          <div>
            <label htmlFor="taskSummary" className="block text-sm font-medium text-gray-700 mb-1">Task Summary (Commit Guidelines):</label>
            <Textarea
              id="taskSummary"
              value={taskSummary}
              onChange={(e) => setTaskSummary(e.target.value)}
              placeholder="Enter a summary of the changes or task..."
              className="w-full h-24"
              required
            />
          </div>
          <Button type="submit" disabled={isLoading} className="w-full">
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generating...
              </>
            ) : (
              'Generate Commit Message'
            )}
          </Button>
        </form>

        {error && (
          <div className="mt-4 text-red-500">
            {error}
          </div>
        )}

        {commitMessage && (
          <div className="mt-6">
            <h3 className="text-lg font-semibold mb-2">Generated Commit Message:</h3>
            <EditableMarkdown content={commitMessage} onChange={setCommitMessage} />
          </div>
        )}
      </CardContent>
    </Card>
  );
}
