#!/usr/bin/env python3
"""
Script to initialize the database and create the March 2025 calendar data.
This script is a simple wrapper to run the database initialization and data creation.
"""

import os
import sys
import logging
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('init_db')

def main():
    """Main function to initialize the database and create the March 2025 calendar data."""
    try:
        # Run the test_db.py script to test the database connection and CRUD operations
        logger.info("Testing database connection and CRUD operations...")
        subprocess.run([sys.executable, "HMDiscordBot/scripts/test_db.py"])
        
        # Run the create_march_2025_calendar.py script to create the March 2025 calendar data
        logger.info("Creating March 2025 calendar data...")
        subprocess.run([sys.executable, "HMDiscordBot/scripts/create_march_2025_calendar.py"])
        
        logger.info("Database initialization and data creation completed successfully.")
        
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
