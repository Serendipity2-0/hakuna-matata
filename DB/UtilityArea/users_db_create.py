import sqlite3
import os

# Ensure the DB/Main directory exists
os.makedirs('DB/Main', exist_ok=True)

# Create and connect to the SQLite database
conn = sqlite3.connect('DB/Main/Users.db')
cursor = conn.cursor()

# Create the users table
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

# Create the typing_results table
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

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Users.db created successfully with users and typing_results tables.")
