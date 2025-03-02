import sqlite3
import base64

# 1. Create and connect to the SQLite database
conn = sqlite3.connect('DB/Main/customer_management.db')
cursor = conn.cursor()

# 2. Create the tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS PastClients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        last_purchase_date TEXT,
        purchase_history TEXT,
        reason_for_leaving TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ActiveClients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        join_date TEXT,
        subscription_plan TEXT,
        renewal_date TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ProspectiveClients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        lead_source TEXT,
        first_contact_date TEXT,
        follow_up_required TEXT
    )
''')

# 3. Insert mock data into PastClients
past_clients_data = [
    ("John Doe", "[email protected]", "555-1111", "2023-01-10", "Laptop, Mouse", "Found cheaper service"),
    ("Jane Smith", "[email protected]", "555-2222", "2022-12-01", "Software subscription, Webinar", "Not satisfied with support"),
    ("Michael Brown", "[email protected]", "555-3333", "2021-06-07", "Annual Maintenance, PC Setup", "Retired"),
    ("Emily Davis", "[email protected]", "555-4444", "2021-09-15", "Consulting Services", "No longer needed services"),
    ("David Wilson", "[email protected]", "555-5555", "2020-02-28", "IT Audit", "Moved to competitor"),
]

cursor.executemany('''
    INSERT INTO PastClients (
        name, email, phone, last_purchase_date, purchase_history, reason_for_leaving
    ) VALUES (?,?,?,?,?,?)
''', past_clients_data)

# 4. Insert mock data into ActiveClients
active_clients_data = [
    ("Sarah Johnson", "[email protected]", "555-6666", "2023-02-01", "Premium Plan", "2024-02-01"),
    ("James Anderson", "[email protected]", "555-7777", "2022-11-15", "Basic Plan", "2023-11-15"),
    ("Patricia Thomas", "[email protected]", "555-8888", "2023-03-20", "Gold Plan", "2024-03-20"),
    ("Robert Taylor", "[email protected]", "555-9999", "2023-01-10", "Enterprise Plan", "2024-01-10"),
    ("Linda Martinez", "[email protected]", "555-0000", "2022-12-25", "Basic Plan", "2023-12-25"),
]

cursor.executemany('''
    INSERT INTO ActiveClients (
        name, email, phone, join_date, subscription_plan, renewal_date
    ) VALUES (?,?,?,?,?,?)
''', active_clients_data)

# 5. Insert mock data into ProspectiveClients
prospective_clients_data = [
    ("Mark Lee", "[email protected]", "555-1112", "Trade Show", "2023-04-02", "Yes"),
    ("Susan Clark", "[email protected]", "555-2212", "Website Inquiry", "2023-03-18", "No"),
    ("George Harris", "[email protected]", "555-3312", "Referral", "2023-01-22", "Yes"),
    ("Jessica Moore", "[email protected]", "555-4412", "Cold Email", "2023-04-10", "Yes"),
    ("Daniel Evans", "[email protected]", "555-5512", "Conference", "2023-02-05", "No"),
]

cursor.executemany('''
    INSERT INTO ProspectiveClients (
        name, email, phone, lead_source, first_contact_date, follow_up_required
    ) VALUES (?,?,?,?,?,?)
''', prospective_clients_data)

# 6. Commit the changes and close the connection
conn.commit()
conn.close()

# 7. Read the database file and encode it as base64
with open('DB/Main/customer_management.db', 'rb') as f:
    db_bytes = f.read()
    encoded_db = base64.b64encode(db_bytes).decode('utf-8')

print("Below is the Base64-encoded 'customer_management.db' file.\n")
print(encoded_db)
