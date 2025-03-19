import fs from 'fs';
import path from 'path';
import { open } from 'sqlite';
import sqlite3 from 'sqlite3';

// Function to get the path to the Users.db file
export async function ensureDbExists() {
  // Try different possible paths to find the database
  const possiblePaths = [
    path.resolve(process.cwd(), '../../DB/Main/Users.db'),
    path.resolve(process.cwd(), '../DB/Main/Users.db'),
    path.resolve(process.cwd(), 'DB/Main/Users.db'),
    path.resolve(process.cwd(), '/DB/Main/Users.db'),
    'C:/Users/seren/OneDrive/Desktop/hakuna-matata/DB/Main/Users.db' // Absolute path
  ];
  
  let dbPath = null;
  
  // Find the first path that exists
  for (const p of possiblePaths) {
    if (fs.existsSync(p)) {
      dbPath = p;
      console.log('Found existing database at:', dbPath);
      break;
    }
  }
  
  // If no database found, create one at the absolute path
  if (!dbPath) {
    dbPath = 'C:/Users/seren/OneDrive/Desktop/hakuna-matata/DB/Main/Users.db';
    console.log('Creating new database at:', dbPath);
    
    // Ensure the directory exists
    const dbDir = path.dirname(dbPath);
    if (!fs.existsSync(dbDir)) {
      fs.mkdirSync(dbDir, { recursive: true });
    }
    
    // Create a new SQLite database with the required schema
    const db = new sqlite3.Database(dbPath);
    
    db.serialize(() => {
      // Create users table
      db.run(`
        CREATE TABLE IF NOT EXISTS users (
          id TEXT PRIMARY KEY,
          email TEXT,
          username TEXT,
          first_name TEXT,
          last_name TEXT,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
      `);
      
      // Create typing_results table
      db.run(`
        CREATE TABLE IF NOT EXISTS typing_results (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id TEXT NOT NULL,
          wpm INTEGER NOT NULL,
          accuracy INTEGER NOT NULL,
          test_duration INTEGER NOT NULL,
          test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (user_id) REFERENCES users (id)
        )
      `);
    });
    
    db.close();
  }
  
  return dbPath;
}

// Helper function to open the database connection
export async function openDb() {
  const dbPath = await ensureDbExists();
  console.log('Using database at:', dbPath);
  
  return open({
    filename: dbPath,
    driver: sqlite3.Database
  });
}
