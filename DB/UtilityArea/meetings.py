import sqlite3

# Connect to the existing database
conn = sqlite3.connect('DB/Main/customer_management.db')
cursor = conn.cursor()

# Create the new table "Meetings"
# This table references clients from different tables (PastClients, ActiveClients, ProspectiveClients)
# via client_id and client_type, so you can track which table and row the meeting is associated with.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Meetings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        client_type TEXT NOT NULL,
        meeting_type TEXT NOT NULL,
        meeting_date TEXT NOT NULL,
        meeting_time TEXT NOT NULL,
        meeting_details TEXT,
        reminder_sent TEXT,
        follow_up_actions TEXT
    )
''')

# Sample data for the Meetings table
# client_id: ID of the client in their respective table (e.g., PastClients.id=1)
# client_type: The name of the table where the client lives (e.g., "PastClients", "ActiveClients", "ProspectiveClients")
meetings_data = [
    # 1) Scheduling a call with a past client (John Doe has ID=1 in PastClients from earlier script)
    (1, "PastClients", "Call", "2025-03-05", "10:00 AM", "Discuss possibility of re-subscription", "No", ""),
    
    # 2) Scheduling a meeting with an active client (Sarah Johnson might be ID=1 in ActiveClients)
    (1, "ActiveClients", "In-Person Meeting", "2025-03-08", "02:30 PM", "Review new features, gather feedback", "No", ""),
    
    # 3) Scheduling a call with a prospective client (Mark Lee might be ID=1 in ProspectiveClients)
    (1, "ProspectiveClients", "Call", "2025-03-10", "09:00 AM", "Initial demo, discuss proposals", "No", ""),
    
    # 4) A follow-up meeting to update details
    (2, "ActiveClients", "Video Conference", "2025-03-12", "11:00 AM", "Update subscription details & contract terms", "No", ""),
    
    # 5) Post-meeting follow-up action
    (2, "PastClients", "Call", "2025-03-15", "03:00 PM", "Discuss reactivating service, plan next steps", "No", "Send quote within 2 days")
]

# Insert the mock meetings data
cursor.executemany('''
    INSERT INTO Meetings (
        client_id, client_type, meeting_type, meeting_date, meeting_time, 
        meeting_details, reminder_sent, follow_up_actions
    ) 
    VALUES (?,?,?,?,?,?,?,?)
''', meetings_data)

# Commit changes and close
conn.commit()
conn.close()

print("Meetings table created/verified and mock data inserted into 'customer_management.db'.")
