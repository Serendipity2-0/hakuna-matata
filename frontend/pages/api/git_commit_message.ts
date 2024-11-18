import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'POST') {
    try {
      const { directory, guidelines } = req.body;
      
      // Here, you would typically make a request to your backend server
      const response = await fetch('http://your-backend-url/api/git_commit_message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ directory, guidelines }),
      });
      
      const data = await response.json();
      
      res.status(200).json(data);
    } catch (error) {
      res.status(500).json({ error: 'Failed to generate commit message' });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
