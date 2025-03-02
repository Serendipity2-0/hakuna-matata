"""
Script to create the March 2025 calendar data.
This script populates the calendar table with entries for each day in March 2025.
"""

import os
import sys
import sqlite3
import logging
from datetime import datetime
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from HMDiscordBot.utils.config import ConfigManager
from HMDiscordBot.utils.db_handler import CalendarDBHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('create_calendar')

def get_db_path():
    """Get the full path to the database file."""
    config = ConfigManager()
    base_dir = os.getcwd()
    db_base_path = config.get('database', 'base_path', 'DB/Main')
    db_file = config.get('database', 'files', 'calendar')
    full_path = os.path.join(base_dir, db_base_path, db_file)
    return full_path

def main():
    """Main function to create the March 2025 calendar data."""
    try:
        # Get the database path
        db_path = get_db_path()
        logger.info(f"Using database at {db_path}")
        
        # Create the database handler
        db_handler = CalendarDBHandler(db_path)
        
        # Create the March 2025 calendar data
        db_handler.create_march_2025_calendar()
        
        logger.info("March 2025 calendar data created successfully")
        
    except Exception as e:
        logger.error(f"Error creating March 2025 calendar data: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
