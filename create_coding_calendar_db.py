"""
Script to create and populate the CodingCalendar.db database with mock data for March 2025.
"""

import os
import sqlite3
import random
from datetime import datetime

def create_coding_calendar_db():
    """Create and populate the CodingCalendar.db database with mock data for March 2025."""
    # Define the database path
    db_dir = "DB/Main"
    db_path = os.path.join(db_dir, "CodingCalendar.db")
    
    # Ensure the directory exists
    os.makedirs(db_dir, exist_ok=True)
    
    # Connect to the database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the coding calendar table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS CodingCalendar (
        "SerialNo." INTEGER PRIMARY KEY,
        "Date" TIMESTAMP,
        "CodingTask" TEXT,
        "CodingTaskDescription" TEXT,
        "CodingTaskStatus" TEXT,
        "CodingTaskDueDate" TIMESTAMP,
        "CodingTaskCompletedDate" TIMESTAMP,
        "CodingTaskAssignedTo" TEXT,
        "CodingProjectName" TEXT,
        "ReferenceLinks" TEXT,
        "CreatedBy" TEXT,
        "CreatedOn" TIMESTAMP,
        "UpdatedBy" TEXT,
        "UpdatedOn" TIMESTAMP
    );
    ''')
    
    # Define project names
    projects = [
        "E-commerce Website", "Mobile App", "API Integration",
        "Database Migration", "UI Redesign", "Authentication System",
        "Payment Gateway", "Admin Dashboard", "User Management",
        "Reporting System"
    ]
    
    # Define assignees
    assignees = [
        "John Doe", "Jane Smith", "Bob Johnson", "Alice Williams",
        "Charlie Brown", "Diana Prince", "Bruce Wayne", "Clark Kent",
        "Peter Parker", "Tony Stark"
    ]
    
    # Define task statuses
    statuses = ["Pending", "In Progress", "Completed", "Blocked", "Deferred"]
    
    # Define coding tasks
    tasks = [
        "Implement user authentication", "Create responsive UI",
        "Optimize database queries", "Fix security vulnerabilities",
        "Add payment processing", "Implement search functionality",
        "Create admin dashboard", "Add user management features",
        "Implement reporting system", "Add data visualization",
        "Create API endpoints", "Implement caching",
        "Add unit tests", "Implement CI/CD pipeline",
        "Optimize performance", "Add logging system",
        "Implement error handling", "Add internationalization",
        "Create documentation", "Implement backup system",
        "Add analytics tracking", "Implement notifications",
        "Create mobile-friendly design", "Add social media integration",
        "Implement file upload", "Create email templates",
        "Add password reset functionality", "Implement role-based access control",
        "Create user profile page", "Add product catalog"
    ]
    
    # Define task descriptions
    descriptions = [
        "Implement secure user authentication using JWT tokens and password hashing.",
        "Create a responsive UI that works well on desktop, tablet, and mobile devices.",
        "Optimize database queries to improve performance and reduce load times.",
        "Fix security vulnerabilities identified in the security audit.",
        "Add payment processing functionality using Stripe API.",
        "Implement search functionality with filtering and sorting options.",
        "Create an admin dashboard with analytics and user management.",
        "Add user management features including role-based access control.",
        "Implement a reporting system with customizable reports and exports.",
        "Add data visualization using charts and graphs.",
        "Create RESTful API endpoints for mobile app integration.",
        "Implement caching to improve performance and reduce database load.",
        "Add unit tests to ensure code quality and prevent regressions.",
        "Implement CI/CD pipeline for automated testing and deployment.",
        "Optimize performance by reducing page load times and improving responsiveness.",
        "Add a comprehensive logging system for debugging and monitoring.",
        "Implement robust error handling and user-friendly error messages.",
        "Add internationalization support for multiple languages.",
        "Create comprehensive documentation for developers and users.",
        "Implement a backup system for data protection and disaster recovery.",
        "Add analytics tracking to monitor user behavior and engagement.",
        "Implement notifications for users and administrators.",
        "Create a mobile-friendly design using responsive CSS and media queries.",
        "Add social media integration for sharing and authentication.",
        "Implement file upload functionality with validation and storage.",
        "Create email templates for notifications and marketing.",
        "Add password reset functionality with email verification.",
        "Implement role-based access control for different user types.",
        "Create a user profile page with customization options.",
        "Add a product catalog with search and filtering capabilities."
    ]
    
    # Define reference links
    reference_links = [
        "https://github.com/example/repo",
        "https://docs.example.com/api",
        "https://example.atlassian.net/browse/PROJ-123",
        "https://example.com/design/mockups",
        "https://example.com/docs/requirements"
    ]
    
    # Get the current highest serial number
    cursor.execute("SELECT MAX(\"SerialNo.\") FROM CodingCalendar")
    result = cursor.fetchone()
    next_serial = 1 if result[0] is None else result[0] + 1
    
    # Create entries for each day in March 2025
    for day in range(1, 32):
        date = datetime(2025, 3, day)
        date_str = date.strftime("%Y-%m-%d")
        
        # Select random values for variety
        project = random.choice(projects)
        assignee = random.choice(assignees)
        status = random.choice(statuses)
        task = random.choice(tasks)
        description = random.choice(descriptions)
        reference_link = random.choice(reference_links)
        
        # Set completed date if status is "Completed"
        completed_date = None
        if status == "Completed":
            completed_date = f"{date_str} {random.randint(9, 17)}:00:00"
        
        # Create the task data
        task_data = {
            "SerialNo.": next_serial,
            "Date": f"{date_str} 00:00:00",
            "CodingTask": task,
            "CodingTaskDescription": description,
            "CodingTaskStatus": status,
            "CodingTaskDueDate": f"{date_str} 23:59:59",
            "CodingTaskCompletedDate": completed_date,
            "CodingTaskAssignedTo": assignee,
            "CodingProjectName": project,
            "ReferenceLinks": reference_link,
            "CreatedBy": "System",
            "CreatedOn": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "UpdatedBy": "System",
            "UpdatedOn": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Insert the task
        columns = ", ".join([f'"{k}"' for k in task_data.keys()])
        placeholders = ", ".join(["?" for _ in task_data.keys()])
        
        query = f"INSERT INTO CodingCalendar ({columns}) VALUES ({placeholders})"
        
        cursor.execute(query, list(task_data.values()))
        next_serial += 1
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    print(f"Created CodingCalendar.db with mock data for March 2025 at {db_path}")

if __name__ == "__main__":
    create_coding_calendar_db()
