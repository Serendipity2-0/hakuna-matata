import sqlite3
import os
import sys

def check_db(db_path):
    """Check the contents of the Users.db file."""
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
        if cursor.fetchone():
            print("\nUsers table exists.")
            # Get user count
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"Total users: {user_count}")
            
            # Get user data
            if user_count > 0:
                print("\nUser data:")
                cursor.execute("SELECT id, email, username, first_name, last_name, created_at FROM users")
                users = cursor.fetchall()
                for user in users:
                    print(f"ID: {user[0]}")
                    print(f"Email: {user[1]}")
                    print(f"Username: {user[2]}")
                    print(f"Name: {user[3]} {user[4]}")
                    print(f"Created: {user[5]}")
                    print("-" * 40)
        else:
            print("\nUsers table does not exist.")
        
        # Check if typing_results table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='typing_results'")
        if cursor.fetchone():
            print("\nTyping results table exists.")
            # Get result count
            cursor.execute("SELECT COUNT(*) FROM typing_results")
            result_count = cursor.fetchone()[0]
            print(f"Total typing results: {result_count}")
            
            # Get typing results data
            if result_count > 0:
                print("\nTyping results data:")
                cursor.execute("""
                    SELECT tr.id, tr.user_id, tr.wpm, tr.accuracy, tr.test_duration, tr.test_date, u.username 
                    FROM typing_results tr
                    LEFT JOIN users u ON tr.user_id = u.id
                    ORDER BY tr.test_date DESC
                """)
                results = cursor.fetchall()
                for result in results:
                    print(f"Result ID: {result[0]}")
                    print(f"User ID: {result[1]}")
                    print(f"Username: {result[6] or 'Unknown'}")
                    print(f"WPM: {result[2]}")
                    print(f"Accuracy: {result[3]}%")
                    print(f"Duration: {result[4]} seconds")
                    print(f"Date: {result[5]}")
                    print("-" * 40)
        else:
            print("\nTyping results table does not exist.")
        
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
    
    # Check the database
    check_db(db_path)
