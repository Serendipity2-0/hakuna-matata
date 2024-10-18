import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Loader2 } from 'lucide-react';
import EditableMarkdown from '@/components/EditableMarkdown';

export default function ScriptWriterInterface() {
  const [filePath, setFilePath] = useState('');
  const [guidelines, setGuidelines] = useState('');
  const [scriptOutline, setScriptOutline] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setScriptOutline('');

    try {
      const response = await fetch('http://localhost:8000/api/script_outline', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ directory: filePath, guidelines }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setScriptOutline(data.script_outline);
    } catch (error) {
      console.error('Error generating script outline:', error);
      setError('Failed to generate script outline. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="text-2xl font-bold">Script Writer</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="filePath" className="block text-sm font-medium text-gray-700 mb-1">
              Research File Path:
            </label>
            <Input
              id="filePath"
              value={filePath}
              onChange={(e) => setFilePath(e.target.value)}
              placeholder="e.g., /path/to/research/file.md"
              required
              className="w-full"
            />
          </div>
          <div>
            <label htmlFor="guidelines" className="block text-sm font-medium text-gray-700 mb-1">
              Script Guidelines (optional):
            </label>
            <Textarea
              id="guidelines"
              value={guidelines}
              onChange={(e) => setGuidelines(e.target.value)}
              placeholder="Enter any specific guidelines for the script..."
              className="w-full h-24"
            />
          </div>
          <Button type="submit" disabled={isLoading} className="w-full">
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generating...
              </>
            ) : (
              'Generate Script Outline'
            )}
          </Button>
        </form>

        {error && (
          <div className="mt-4 text-red-500">
            {error}
          </div>
        )}

        {scriptOutline && (
          <div className="mt-6">
            <h3 className="text-lg font-semibold mb-2">Generated Script Outline:</h3>
            <EditableMarkdown content={scriptOutline} onChange={setScriptOutline} />
          </div>
        )}
      </CardContent>
    </Card>
  );
}
