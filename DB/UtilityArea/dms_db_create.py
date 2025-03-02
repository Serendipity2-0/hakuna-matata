import sqlite3
import base64

# 1. Create and connect to the SQLite database
conn = sqlite3.connect('DB/Main/dms.db')
cursor = conn.cursor()

# 2. Create the tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS DMS (
        docid INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        tags TEXT,
        description TEXT,
        created_at DATETIME,
        department TEXT,
        created_by TEXT,
        updated_by TEXT,
        comments TEXT,
        last_updated_at DATETIME    -- Last column, no comma needed
    )
''')

# 3. Insert mock data into PastClients
dms_data = [
    ("Coding Standards", "Coding", "A intro to trading standards in TradeMan", "2025-03-02", "Development", "Omkar", "Omkar", "Comments", "2025-03-02"),
    ("Content Creation Guideline", "Dhoom Studios", "A guideline for content creation for Dhoom Studios", "2025-03-02", "Marketing", "Omkar", "Omkar", "Comments", "2025-03-02"),
    ("Serendipity Accounts Guidelines", "Serendipity", "A guideline for accounts for Serendipity", "2025-03-02", "Accounts", "Omkar", "Omkar", "Comments", "2025-03-02"),
]

cursor.executemany('''
    INSERT INTO DMS (
        name, tags, description, created_at, department, created_by, updated_by, comments, last_updated_at
    ) VALUES (?,?,?,?,?,?,?,?,?)
''', dms_data)

# 6. Commit the changes and close the connection
conn.commit()
conn.close()

# 7. Read the database file and encode it as base64
with open('DB/Main/dms.db', 'rb') as f:
    db_bytes = f.read()
    encoded_db = base64.b64encode(db_bytes).decode('utf-8')

print("Below is the Base64-encoded 'dms.db' file.\n")
print(encoded_db)
