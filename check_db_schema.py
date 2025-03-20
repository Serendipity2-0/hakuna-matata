import sqlite3
import os

# Connect to the database
db_path = os.path.join('DB', 'Main', 'Users.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get the list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(f"- {table[0]}")
    # Get the schema for each table
    cursor.execute(f"PRAGMA table_info({table[0]})")
    columns = cursor.fetchall()
    for column in columns:
        print(f"  - {column[1]} ({column[2]})")

# Close the connection
conn.close()
