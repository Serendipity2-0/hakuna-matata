'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

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
   * Parses and formats the commit message for better readability.
   * 
   * @param {string} message - The raw commit message.
   * @returns {string} The formatted commit message.
   */
  const formatCommitMessage = (message: string): { title: string; body: string } => {
    try {
      const parsedMessage = JSON.parse(message);
      const actualMessage = parsedMessage.commit_message || parsedMessage;
      const cleanMessage = actualMessage.replace(/^```\n?|\n?```$/g, '').trim();
      const lines = cleanMessage.split('\n');
      const title = lines[0];
      const body = lines.slice(1).join('\n').trim();
      return { title, body };
    } catch (error) {
      console.error('Error formatting commit message:', error);
      return { title: 'Error parsing message', body: message };
    }
  };

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
      const formattedMessage = formatCommitMessage(JSON.stringify(data));
      setCommitMessage(JSON.stringify(formattedMessage));
    } catch (error) {
      console.error('Error generating commit message:', error);
      setError('Failed to generate commit message. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const { title, body } = commitMessage ? JSON.parse(commitMessage) : { title: '', body: '' };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Generate Git Commit Message</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="directory" className="block text-sm font-medium text-gray-700">Working Directory:</label>
            <Input
              id="directory"
              value={directory}
              onChange={(e) => setDirectory(e.target.value)}
              required
            />
          </div>
          <div>
            <label htmlFor="taskSummary" className="block text-sm font-medium text-gray-700">Task Summary (Commit Guidelines):</label>
            <Textarea
              id="taskSummary"
              value={taskSummary}
              onChange={(e) => setTaskSummary(e.target.value)}
              rows={4}
              required
            />
          </div>
          <Button type="submit" disabled={isLoading}>
            {isLoading ? 'Generating...' : 'Generate Commit Message'}
          </Button>
        </form>
        {error && (
          <div className="mt-4 text-red-500">
            {error}
          </div>
        )}
        {commitMessage && (
          <div className="mt-4">
            <h3 className="text-lg font-semibold mb-2">Generated Commit Message:</h3>
            <div className="bg-gray-100 p-4 rounded-md">
              <p className="font-bold">{title}</p>
              <p className="mt-2 whitespace-pre-wrap">{body}</p>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
