import { NextApiRequest, NextApiResponse } from 'next';
import sqlite3 from 'sqlite3';
import { open } from 'sqlite';
import path from 'path';

// Helper function to format date from SQLite format to our desired format
function formatDate(dateStr: string): string {
  if (!dateStr) return '';
  
  try {
    // Parse the date string (assuming format like "2023-03-01 00:00:00")
    const date = new Date(dateStr);
    
    // Format to "DD-MMM-YY" (e.g., "01-Mar-25")
    const day = date.getDate().toString().padStart(2, '0');
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const month = monthNames[date.getMonth()];
    const year = date.getFullYear().toString().slice(2); // Get last 2 digits
    
    return `${day}-${month}-${year}`;
  } catch (e) {
    console.error('Error formatting date:', e);
    return dateStr; // Return original if parsing fails
  }
}

// Helper function to format time from SQLite format to our desired format
function formatTime(timeStr: string): string {
  if (!timeStr) return '';
  
  try {
    // Parse the time string (assuming format like "18:00:00.000000")
    const timeParts = timeStr.split(':');
    if (timeParts.length < 2) return timeStr;
    
    let hour = parseInt(timeParts[0]);
    const minute = parseInt(timeParts[1]);
    
    // Convert to 12-hour format with AM/PM
    const period = hour >= 12 ? 'PM' : 'AM';
    hour = hour % 12;
    hour = hour === 0 ? 12 : hour; // Convert 0 to 12 for 12 AM
    
    return `${hour}:${minute.toString().padStart(2, '0')} ${period}`;
  } catch (e) {
    console.error('Error formatting time:', e);
    return timeStr; // Return original if parsing fails
  }
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    // Open the database
    // When running in development, process.cwd() is the frontend directory
    // So we need to go up one level and then to DB/Calendar.db
    const dbPath = path.resolve(process.cwd(), '../DB/Calendar.db');
    console.log('Database path:', dbPath);
    const db = await open({
      filename: dbPath,
      driver: sqlite3.Database
    });

    // First, let's get the table names to understand the structure
    const tables = await db.all("SELECT name FROM sqlite_master WHERE type='table'");
    console.log('Tables in database:', tables);
    
    if (tables.length === 0) {
      return res.status(404).json({ error: 'No tables found in database' });
    }

    // Based on the screenshot, we know the table name is 'calendar'
    const tableName = 'calendar';
    console.log('Using table:', tableName);
    
    // Get all columns from the table
    const tableInfo = await db.all(`PRAGMA table_info(${tableName})`);
    console.log('Table columns:', tableInfo);
    
    // Query all data from the table
    const data = await db.all(`SELECT * FROM ${tableName}`);
    console.log('Data count:', data.length);
    
    if (data.length > 0) {
      console.log('Sample data item:', data[0]);
      
      // Transform the data to match our ContentPost interface
      const transformedData = data.map(item => ({
        serialNo: item['SerialNo.'] || 0,
        date: formatDate(item.Date),
        contentType: item['ContentType '] || '',
        format: item['Format '] || '',
        platform: item['Platform '] || '',
        scheduleTime: formatTime(item['ScheduleTime '] || '')
      }));
      
      // Close the database connection
      await db.close();
      
      // Return the transformed data
      return res.status(200).json({
        success: true,
        data: transformedData
      });
    } else {
      console.log('No data found in the database');
      
      // Close the database connection
      await db.close();
      
      return res.status(200).json({
        success: false,
        message: 'No data found in the database',
        data: []
      });
    }
  } catch (error: any) {
    console.error('Database error:', error);
    res.status(500).json({ error: 'Failed to fetch calendar data', details: error.message });
  }
}
