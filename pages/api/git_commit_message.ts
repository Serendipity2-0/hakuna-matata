import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'POST') {
    try {
      const { directory, guidelines } = req.body;
      
      console.log('Received request:', { directory, guidelines });

      // Make a request to your FastAPI backend
      const backendUrl = 'http://localhost:8000/api/git_commit_message';
      console.log('Sending request to backend:', backendUrl);

      const response = await fetch(backendUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ directory, guidelines }),
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Backend responded with an error:', response.status, errorText);
        throw new Error(`Backend error: ${response.status} ${errorText}`);
      }
      
      const data = await response.json();
      console.log('Received response from backend:', data);

      res.status(200).json(data);
    } catch (error) {
      console.error('Error in API route:', error);
      res.status(500).json({ error: 'Failed to generate commit message', details: error.message });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
