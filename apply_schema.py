import sqlite3
import os

# Connect to the database
db_path = os.path.join('DB', 'Main', 'Users.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Read the schema file
with open(os.path.join('db', 'schema.sql'), 'r') as f:
    schema_sql = f.read()

# Execute the schema SQL
cursor.executescript(schema_sql)

# Commit the changes
conn.commit()

# Verify the tables were created
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database after schema application:")
for table in tables:
    print(f"- {table[0]}")

# Close the connection
conn.close()

print("Schema applied successfully!")
