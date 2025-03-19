'use server'

import { auth, currentUser } from '@clerk/nextjs/server'
import { openDb } from '@/lib/db-utils'

// Save user info to the database
export async function saveUserInfo() {
  const user = await currentUser();
  if (!user) return { success: false, error: 'User not authenticated' };

  try {
    const db = await openDb();
    
    // Check if user already exists
    const existingUser = await db.get('SELECT * FROM users WHERE id = ?', user.id);
    
    if (!existingUser) {
      // Insert new user
      await db.run(
        'INSERT INTO users (id, email, username, first_name, last_name) VALUES (?, ?, ?, ?, ?)',
        user.id,
        user.emailAddresses[0]?.emailAddress || '',
        user.username || '',
        user.firstName || '',
        user.lastName || ''
      );
    }
    
    await db.close();
    return { success: true, userId: user.id };
  } catch (error) {
    console.error('Error saving user info:', error);
    return { success: false, error: String(error) };
  }
}

// Save typing test results
export async function saveTypingResults(wpm: number, accuracy: number, testDuration: number) {
  const session = await auth();
  const userId = session.userId;
  if (!userId) return { success: false, error: 'User not authenticated' };

  try {
    const db = await openDb();
    
    // Save typing results
    await db.run(
      'INSERT INTO typing_results (user_id, wpm, accuracy, test_duration) VALUES (?, ?, ?, ?)',
      userId,
      wpm,
      accuracy,
      testDuration
    );
    
    await db.close();
    return { success: true };
  } catch (error) {
    console.error('Error saving typing results:', error);
    return { success: false, error: String(error) };
  }
}

// Get user's typing history
export async function getTypingHistory() {
  const session = await auth();
  const userId = session.userId;
  if (!userId) return { success: false, error: 'User not authenticated', results: [] };

  try {
    const db = await openDb();
    
    // Get typing history
    const results = await db.all(
      'SELECT wpm, accuracy, test_duration, test_date FROM typing_results WHERE user_id = ? ORDER BY test_date DESC LIMIT 10',
      userId
    );
    
    await db.close();
    return { success: true, results };
  } catch (error) {
    console.error('Error getting typing history:', error);
    return { success: false, error: String(error), results: [] };
  }
}
