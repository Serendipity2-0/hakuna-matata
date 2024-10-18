'use client';

import { useState } from 'react';

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
  const formatCommitMessage = (message: string): string => {
    console.log('Raw message:', message);
    
    try {
      // Parse the JSON string
      const parsedMessage = JSON.parse(message);
      console.log('Parsed message:', parsedMessage);
      
      // Extract the actual commit message
      const actualMessage = parsedMessage.commit_message || parsedMessage;
      console.log('Actual message:', actualMessage);
      
      // Remove any remaining nested structures and backticks
      const cleanMessage = actualMessage.replace(/^```\n?|\n?```$/g, '').trim();
      console.log('Clean message:', cleanMessage);
      
      // Split the message into lines
      const lines = cleanMessage.split('\n');
      
      // Extract title and body
      const title = lines[0];
      const body = lines.slice(1).join('\n').trim();
      
      // Format the message
      return `${title}\n\n${body}`;
    } catch (error) {
      console.error('Error formatting commit message:', error);
      return message; // Return the original message if parsing fails
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
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          directory,
          guidelines: taskSummary,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('API Response:', data);

      let rawMessage = '';
      if (typeof data.commit_message === 'string') {
        rawMessage = data.commit_message;
      } else if (data.commit_message && typeof data.commit_message.commit_message === 'string') {
        rawMessage = data.commit_message.commit_message;
      } else {
        throw new Error('Unexpected response format');
      }

      const formattedMessage = formatCommitMessage(rawMessage);
      console.log('Formatted message:', formattedMessage);
      setCommitMessage(formattedMessage);
    } catch (error) {
      console.error('Error generating commit message:', error);
      setError('Failed to generate commit message. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="mt-8">
      <h2 className="text-2xl font-bold mb-4">Generate Git Commit Message</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="directory" className="block mb-1">Working Directory:</label>
          <input
            type="text"
            id="directory"
            value={directory}
            onChange={(e) => setDirectory(e.target.value)}
            className="w-full p-2 border rounded"
            required
          />
        </div>
        <div>
          <label htmlFor="taskSummary" className="block mb-1">Task Summary (Commit Guidelines):</label>
          <textarea
            id="taskSummary"
            value={taskSummary}
            onChange={(e) => setTaskSummary(e.target.value)}
            className="w-full p-2 border rounded"
            rows={4}
            required
          ></textarea>
        </div>
        <button 
          type="submit" 
          className="bg-blue-500 text-white px-4 py-2 rounded"
          disabled={isLoading}
        >
          {isLoading ? 'Generating...' : 'Generate Commit Message'}
        </button>
      </form>
      {error && (
        <div className="mt-4 text-red-500">
          {error}
        </div>
      )}
      {commitMessage && (
        <div className="mt-4">
          <h3 className="text-xl font-bold mb-2">Generated Commit Message:</h3>
          <pre className="bg-gray-100 p-4 rounded whitespace-pre-wrap font-mono text-sm leading-relaxed">
            {commitMessage.split('\n').map((line, index) => (
              <span key={index} className={index === 0 ? 'font-bold' : ''}>
                {line}
                {index === 0 && <br />}
                {index === 1 && <br />}
              </span>
            ))}
          </pre>
        </div>
      )}
    </div>
  );
}
