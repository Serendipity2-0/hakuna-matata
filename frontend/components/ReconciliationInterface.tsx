import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Loader2 } from 'lucide-react';

export default function ReconciliationInterface() {
  const [filePath, setFilePath] = useState('');
  const [guidelines, setGuidelines] = useState('');
  const [analysisReport, setAnalysisReport] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setAnalysisReport('');

    try {
      const response = await fetch('http://localhost:8000/api/financial_analysis_report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ directory: filePath, guidelines }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setAnalysisReport(data.financial_analysis_report);
    } catch (error) {
      console.error('Error generating financial analysis report:', error);
      setError('Failed to generate financial analysis report. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="text-2xl font-bold">Financial Analysis</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="filePath" className="block text-sm font-medium text-gray-700 mb-1">
              Excel File Path:
            </label>
            <Input
              id="filePath"
              value={filePath}
              onChange={(e) => setFilePath(e.target.value)}
              placeholder="e.g., /path/to/financial/data.xlsx"
              required
              className="w-full"
            />
          </div>
          <div>
            <label htmlFor="guidelines" className="block text-sm font-medium text-gray-700 mb-1">
              Analysis Guidelines (optional):
            </label>
            <Textarea
              id="guidelines"
              value={guidelines}
              onChange={(e) => setGuidelines(e.target.value)}
              placeholder="Enter any specific guidelines for the analysis..."
              className="w-full h-24"
            />
          </div>
          <Button type="submit" disabled={isLoading} className="w-full">
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Analyzing...
              </>
            ) : (
              'Generate Financial Analysis'
            )}
          </Button>
        </form>

        {error && (
          <div className="mt-4 text-red-500">
            {error}
          </div>
        )}

        {analysisReport && (
          <div className="mt-6">
            <h3 className="text-lg font-semibold mb-2">Financial Analysis Report:</h3>
            <div className="prose max-w-none">
              <div dangerouslySetInnerHTML={{ __html: analysisReport }} />
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

