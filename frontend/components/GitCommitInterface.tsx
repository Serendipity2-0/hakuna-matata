'use client';

import { useState } from 'react';

export default function GitCommitInterface() {
  const [directory, setDirectory] = useState('');
  const [taskSummary, setTaskSummary] = useState('');
  const [commitMessage, setCommitMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:8000/api/git_commit_message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          directory,
          guidelines: taskSummary,
        }),
      });
      const data = await response.json();
      setCommitMessage(data.commit_message.commit_message);
    } catch (error) {
      console.error('Error generating commit message:', error);
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
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Generate Commit Message
        </button>
      </form>
      {commitMessage && (
        <div className="mt-4">
          <h3 className="text-xl font-bold mb-2">Generated Commit Message:</h3>
          <pre className="bg-gray-100 p-4 rounded">{commitMessage}</pre>
        </div>
      )}
    </div>
  );
}
