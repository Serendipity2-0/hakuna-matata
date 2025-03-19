import sqlite3
import os
import sys
from datetime import datetime

def insert_test_data(db_path):
    """Insert test data into the Users.db file."""
    if not os.path.exists(db_path):
        print(f"Database file not found at: {db_path}")
        return
    
    print(f"Database file found at: {db_path}")
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("Users table does not exist. Creating it...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
        
        # Check if typing_results table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='typing_results'")
        if not cursor.fetchone():
            print("Typing results table does not exist. Creating it...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS typing_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    wpm INTEGER NOT NULL,
                    accuracy INTEGER NOT NULL,
                    test_duration INTEGER NOT NULL,
                    test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
        
        # Insert a test user
        test_user_id = "test_user_123"
        cursor.execute("SELECT id FROM users WHERE id = ?", (test_user_id,))
        if not cursor.fetchone():
            print("Inserting test user...")
            cursor.execute('''
                INSERT INTO users (id, email, username, first_name, last_name)
                VALUES (?, ?, ?, ?, ?)
            ''', (test_user_id, "test@example.com", "testuser", "Test", "User"))
        
        # Insert test typing results
        print("Inserting test typing results...")
        for i in range(5):
            wpm = 50 + i * 5
            accuracy = 85 + i
            test_duration = 60
            
            cursor.execute('''
                INSERT INTO typing_results (user_id, wpm, accuracy, test_duration)
                VALUES (?, ?, ?, ?)
            ''', (test_user_id, wpm, accuracy, test_duration))
        
        # Commit the changes
        conn.commit()
        print("Test data inserted successfully.")
        
        # Close the connection
        conn.close()
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Default path
    db_path = "DB/Main/Users.db"
    
    # Use command line argument if provided
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    
    # Insert test data
    insert_test_data(db_path)
