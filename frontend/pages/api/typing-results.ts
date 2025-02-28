import { NextApiRequest, NextApiResponse } from 'next';
import sqlite3 from 'sqlite3';
import { open } from 'sqlite';
import path from 'path';
import fs from 'fs';

// Interface for typing test results
interface TestResult {
  id?: number;
  user: string;
  wpm: number;
  accuracy: number;
  difficulty: string;
  date: string;
}

// Open SQLite database connection
async function openDb() {
  try {
    // Adjust the path to the database file
    // The DB directory is in the hakuna-matata root directory
    const dbPath = path.resolve(process.cwd(), '../DB/TypeNew.db');
    console.log('Database path:', dbPath);
    
    return open({
      filename: dbPath,
      driver: sqlite3.Database
    });
  } catch (error) {
    console.error('Error opening database:', error);
    throw error;
  }
}

// Initialize database if needed
async function initializeDb() {
  const db = await openDb();
  
  // Check if the table exists
  const tableExists = await db.get(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='typing_results'"
  );
  
  if (!tableExists) {
    // Create the table if it doesn't exist
    await db.exec(`
      CREATE TABLE typing_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        wpm INTEGER NOT NULL,
        accuracy REAL NOT NULL,
        difficulty TEXT NOT NULL,
        date TEXT NOT NULL
      )
    `);
    
    console.log('Created typing_results table');
  }
  
  return db;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const db = await initializeDb();
    
    // Handle GET request - retrieve all results
    if (req.method === 'GET') {
      const results = await db.all('SELECT * FROM typing_results ORDER BY date DESC');
      return res.status(200).json(results);
    }
    
    // Handle POST request - save a new result
    if (req.method === 'POST') {
      const { user, wpm, accuracy, difficulty, date } = req.body as TestResult;
      
      // Validate required fields
      if (!user || !wpm || !accuracy || !difficulty || !date) {
        return res.status(400).json({ error: 'Missing required fields' });
      }
      
      // Insert the new result
      const result = await db.run(
        'INSERT INTO typing_results (user, wpm, accuracy, difficulty, date) VALUES (?, ?, ?, ?, ?)',
        [user, wpm, accuracy, difficulty, date]
      );
      
      // Return the newly created result with its ID
      return res.status(201).json({
        id: result.lastID,
        user,
        wpm,
        accuracy,
        difficulty,
        date
      });
    }
    
    // Handle unsupported methods
    return res.status(405).json({ error: 'Method not allowed' });
  } catch (error) {
    console.error('API error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
