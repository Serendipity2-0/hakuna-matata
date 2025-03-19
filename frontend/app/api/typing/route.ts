import { NextRequest, NextResponse } from 'next/server';
import { auth, currentUser } from '@clerk/nextjs/server';
import { openDb } from '@/lib/db-utils';

// Save user info to the database
export async function POST(request: NextRequest) {
  // Get the authenticated user if available
  const user = await currentUser();
  let userId = 'test_user_123'; // Default test user ID for testing
  
  if (user) {
    console.log('Authenticated user found:', user.id);
    userId = user.id;
  } else {
    console.log('No authenticated user found, using test user ID');
  }
  
  try {
    console.log('Opening database connection...');
    const db = await openDb();
    console.log('Database connection opened successfully');
    
    // Check if user already exists
    console.log('Checking if user exists in database...');
    const existingUser = await db.get('SELECT * FROM users WHERE id = ?', userId);
    
    if (!existingUser) {
      console.log('User does not exist, creating new user record...');
      // Insert new user (either the authenticated user or a test user)
      if (user) {
        await db.run(
          'INSERT INTO users (id, email, username, first_name, last_name) VALUES (?, ?, ?, ?, ?)',
          user.id,
          user.emailAddresses[0]?.emailAddress || '',
          user.username || '',
          user.firstName || '',
          user.lastName || ''
        );
      } else {
        await db.run(
          'INSERT INTO users (id, email, username, first_name, last_name) VALUES (?, ?, ?, ?, ?)',
          userId,
          'test@example.com',
          'testuser',
          'Test',
          'User'
        );
      }
      console.log('User record created successfully');
    } else {
      console.log('User already exists in database');
    }
    
    // Get the request body
    let body: { wpm?: number; accuracy?: number; testDuration?: number } = {};
    try {
      body = await request.json();
      console.log('Request body:', body);
    } catch (e) {
      console.log('No request body or invalid JSON');
      body = {};
    }
    
    const { wpm, accuracy, testDuration } = body;
    
    // If typing results are provided, save them
    if (wpm !== undefined && accuracy !== undefined && testDuration !== undefined) {
      console.log('Saving typing results:', { wpm, accuracy, testDuration });
      const result = await db.run(
        'INSERT INTO typing_results (user_id, wpm, accuracy, test_duration) VALUES (?, ?, ?, ?)',
        userId,
        wpm,
        accuracy,
        testDuration
      );
      console.log('Typing results saved successfully, last ID:', result.lastID);
    } else {
      console.log('No typing results provided in request');
    }
    
    await db.close();
    console.log('Database connection closed');
    
    return NextResponse.json({ success: true, userId });
  } catch (error) {
    console.error('Error saving data:', error);
    return NextResponse.json({ 
      success: false, 
      error: String(error),
      stack: error instanceof Error ? error.stack : undefined
    }, { status: 500 });
  }
}

// Get user's typing history
export async function GET() {
  console.log('GET request received for typing history');
  
  // Get the authenticated user if available
  const session = await auth();
  let userId = 'test_user_123'; // Default test user ID for testing
  
  if (session.userId) {
    console.log('Authenticated user found:', session.userId);
    userId = session.userId;
  } else {
    console.log('No authenticated user found, using test user ID');
  }

  console.log('Getting typing history for user:', userId);
  
  try {
    console.log('Opening database connection...');
    const db = await openDb();
    console.log('Database connection opened successfully');
    
    // Get typing history
    console.log('Querying typing results...');
    const results = await db.all(
      'SELECT wpm, accuracy, test_duration, test_date FROM typing_results WHERE user_id = ? ORDER BY test_date DESC LIMIT 10',
      userId
    );
    
    console.log(`Found ${results.length} typing results`);
    
    await db.close();
    console.log('Database connection closed');
    
    return NextResponse.json({ success: true, results });
  } catch (error) {
    console.error('Error getting typing history:', error);
    return NextResponse.json(
      { 
        success: false, 
        error: String(error),
        stack: error instanceof Error ? error.stack : undefined,
        results: [] 
      }, 
      { status: 500 }
    );
  }
}
