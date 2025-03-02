"""
Test script for the calendar database.
This script tests the database connection and basic CRUD operations.
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from HMDiscordBot.utils.config import ConfigManager
from HMDiscordBot.utils.db_handler import CalendarDBHandler
from HMDiscordBot.models.calendar_event import CalendarEvent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('test_db')

def get_db_path():
    """Get the full path to the database file."""
    config = ConfigManager()
    base_dir = os.getcwd()
    db_base_path = config.get('database', 'base_path', 'DB/Main')
    db_file = config.get('database', 'files', 'calendar')
    full_path = os.path.join(base_dir, db_base_path, db_file)
    return full_path

def test_database_connection():
    """Test the database connection."""
    try:
        db_path = get_db_path()
        logger.info(f"Testing database connection to {db_path}")
        
        db_handler = CalendarDBHandler(db_path)
        conn = db_handler.get_connection()
        conn.close()
        
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}", exc_info=True)
        return False

def test_crud_operations():
    """Test basic CRUD operations on the database."""
    try:
        db_path = get_db_path()
        db_handler = CalendarDBHandler(db_path)
        
        # Test adding an event
        logger.info("Testing add_event")
        event_data = {
            "Date": "2025-03-15 00:00:00",
            "ContentType ": "Test Content",
            "Format ": "Test Format",
            "Platform ": "Test Platform",
            "ScheduleTime ": "12:00:00",
            "Status": "Test",
            "CreatedBy": "Test User",
            "CreatedOn": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "UpdatedBy": "Test User",
            "UpdatedOn": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        event_id = db_handler.add_event(event_data)
        logger.info(f"Added event with ID {event_id}")
        
        # Test getting an event
        logger.info("Testing get_event_by_id")
        event = db_handler.get_event_by_id(event_id)
        if event:
            logger.info(f"Retrieved event: {event}")
        else:
            logger.error(f"Failed to retrieve event with ID {event_id}")
            return False
        
        # Test updating an event
        logger.info("Testing update_event")
        update_data = {
            "ContentType ": "Updated Test Content",
            "UpdatedBy": "Test User",
            "UpdatedOn": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        success = db_handler.update_event(event_id, update_data)
        if success:
            logger.info(f"Updated event with ID {event_id}")
        else:
            logger.error(f"Failed to update event with ID {event_id}")
            return False
        
        # Test getting all events
        logger.info("Testing get_all_events")
        events = db_handler.get_all_events()
        logger.info(f"Retrieved {len(events)} events")
        
        # Test getting events by date
        logger.info("Testing get_events_by_date")
        date_events = db_handler.get_events_by_date(datetime(2025, 3, 15))
        logger.info(f"Retrieved {len(date_events)} events for 2025-03-15")
        
        # Test deleting an event
        logger.info("Testing delete_event")
        success = db_handler.delete_event(event_id)
        if success:
            logger.info(f"Deleted event with ID {event_id}")
        else:
            logger.error(f"Failed to delete event with ID {event_id}")
            return False
        
        logger.info("All CRUD operations successful")
        return True
    except Exception as e:
        logger.error(f"CRUD operations failed: {str(e)}", exc_info=True)
        return False

def main():
    """Main function to run the tests."""
    if not test_database_connection():
        logger.error("Database connection test failed")
        sys.exit(1)
    
    if not test_crud_operations():
        logger.error("CRUD operations test failed")
        sys.exit(1)
    
    logger.info("All tests passed successfully")

if __name__ == "__main__":
    main()
