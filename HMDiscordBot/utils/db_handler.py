"""
Database handler for the Calendar bot.
This module provides utilities for interacting with the Calendar database.
"""

import sqlite3
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('db_handler')

class CalendarDBHandler:
    """
    Handler for interacting with the Calendar database.
    
    This class provides methods for CRUD operations on the calendar table.
    """
    
    def __init__(self, db_path: str):
        """
        Initialize the database handler.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        logger.info(f"Initialized CalendarDBHandler with database at {db_path}")
        
        # Ensure the database exists and has the correct schema
        self._ensure_db_exists()
    
    def _ensure_db_exists(self) -> None:
        """
        Ensure the database exists and has the correct schema.
        
        If the database doesn't exist, it will be created with the correct schema.
        """
        try:
            # Check if the database file exists
            if not os.path.exists(self.db_path):
                logger.warning(f"Database file not found at {self.db_path}. Creating new database.")
                self._create_db()
            else:
                # Verify the schema
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Check if the calendar table exists
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='calendar';")
                if not cursor.fetchone():
                    logger.warning("Calendar table not found. Creating table.")
                    self._create_table(conn)
                else:
                    # Check if all required columns exist
                    cursor.execute("PRAGMA table_info(calendar);")
                    columns = [col[1] for col in cursor.fetchall()]
                    
                    required_columns = [
                        "SerialNo.", "Date", "ContentType ", "Format ", "Platform ", 
                        "ScheduleTime ", "Status", "CreatedBy", "CreatedOn", 
                        "UpdatedBy", "UpdatedOn"
                    ]
                    
                    missing_columns = [col for col in required_columns if col not in columns]
                    
                    if missing_columns:
                        logger.warning(f"Missing columns in calendar table: {missing_columns}")
                        for col in missing_columns:
                            col_type = "TIMESTAMP" if col in ["CreatedOn", "UpdatedOn"] else "TEXT"
                            try:
                                cursor.execute(f"ALTER TABLE calendar ADD COLUMN '{col}' {col_type};")
                                logger.info(f"Added column {col} to calendar table")
                            except sqlite3.Error as e:
                                logger.error(f"Error adding column {col}: {e}")
                
                conn.commit()
                conn.close()
                
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            raise
    
    def _create_db(self) -> None:
        """Create a new database with the required schema."""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            # Create the database and table
            conn = sqlite3.connect(self.db_path)
            self._create_table(conn)
            conn.close()
            
            logger.info(f"Created new database at {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Error creating database: {e}")
            raise
    
    def _create_table(self, conn: sqlite3.Connection) -> None:
        """
        Create the calendar table in the database.
        
        Args:
            conn: SQLite connection object
        """
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS calendar (
            "SerialNo." INTEGER,
            "Date" TIMESTAMP,
            "ContentType " TEXT,
            "Format " TEXT,
            "Platform " TEXT,
            "ScheduleTime " TIME,
            "Status" TEXT,
            "CreatedBy" TEXT,
            "CreatedOn" TIMESTAMP,
            "UpdatedBy" TEXT,
            "UpdatedOn" TIMESTAMP
        );
        ''')
        
        conn.commit()
        logger.info("Created calendar table")
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Get a connection to the database.
        
        Returns:
            A SQLite connection object
        """
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database: {e}")
            raise
    
    def add_event(self, event_data: Dict[str, Any]) -> int:
        """
        Add a new event to the calendar.
        
        Args:
            event_data: Dictionary containing event data
            
        Returns:
            The serial number of the new event
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get the next serial number
            cursor.execute("SELECT MAX(\"SerialNo.\") FROM calendar")
            result = cursor.fetchone()
            next_serial = 1 if result[0] is None else result[0] + 1
            
            # Set created/updated timestamps
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Prepare the event data
            event_data["SerialNo."] = next_serial
            if "CreatedOn" not in event_data:
                event_data["CreatedOn"] = now
            if "UpdatedOn" not in event_data:
                event_data["UpdatedOn"] = now
            
            # Build the SQL query
            columns = ", ".join([f'"{k}"' for k in event_data.keys()])
            placeholders = ", ".join(["?" for _ in event_data.keys()])
            
            query = f"INSERT INTO calendar ({columns}) VALUES ({placeholders})"
            
            cursor.execute(query, list(event_data.values()))
            conn.commit()
            conn.close()
            
            logger.info(f"Added new event with SerialNo. {next_serial}")
            return next_serial
            
        except sqlite3.Error as e:
            logger.error(f"Error adding event: {e}")
            raise
    
    def get_all_events(self) -> List[Dict[str, Any]]:
        """
        Get all events from the calendar.
        
        Returns:
            List of dictionaries containing event data
        """
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM calendar ORDER BY \"Date\", \"ScheduleTime \"")
            
            events = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            logger.info(f"Retrieved {len(events)} events")
            return events
            
        except sqlite3.Error as e:
            logger.error(f"Error getting events: {e}")
            raise
    
    def get_event_by_id(self, serial_no: int) -> Optional[Dict[str, Any]]:
        """
        Get an event by its serial number.
        
        Args:
            serial_no: The serial number of the event
            
        Returns:
            Dictionary containing event data, or None if not found
        """
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM calendar WHERE \"SerialNo.\" = ?", (serial_no,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                logger.info(f"Retrieved event with SerialNo. {serial_no}")
                return dict(row)
            else:
                logger.warning(f"Event with SerialNo. {serial_no} not found")
                return None
                
        except sqlite3.Error as e:
            logger.error(f"Error getting event: {e}")
            raise
    
    def get_events_by_date(self, date: datetime) -> List[Dict[str, Any]]:
        """
        Get events for a specific date.
        
        Args:
            date: The date to get events for
            
        Returns:
            List of dictionaries containing event data
        """
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            date_str = date.strftime("%Y-%m-%d")
            
            cursor.execute(
                "SELECT * FROM calendar WHERE Date LIKE ? ORDER BY \"ScheduleTime \"",
                (f"{date_str}%",)
            )
            
            events = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            logger.info(f"Retrieved {len(events)} events for date {date_str}")
            return events
                
        except sqlite3.Error as e:
            logger.error(f"Error getting events by date: {e}")
            raise
    
    def get_events_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """
        Get events within a date range.
        
        Args:
            start_date: The start date of the range
            end_date: The end date of the range
            
        Returns:
            List of dictionaries containing event data
        """
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            start_str = start_date.strftime("%Y-%m-%d")
            end_str = end_date.strftime("%Y-%m-%d")
            
            cursor.execute(
                "SELECT * FROM calendar WHERE Date >= ? AND Date <= ? ORDER BY Date, \"ScheduleTime \"",
                (f"{start_str} 00:00:00", f"{end_str} 23:59:59")
            )
            
            events = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            logger.info(f"Retrieved {len(events)} events between {start_str} and {end_str}")
            return events
                
        except sqlite3.Error as e:
            logger.error(f"Error getting events by date range: {e}")
            raise
    
    def update_event(self, serial_no: int, event_data: Dict[str, Any]) -> bool:
        """
        Update an existing event.
        
        Args:
            serial_no: The serial number of the event to update
            event_data: Dictionary containing updated event data
            
        Returns:
            True if the event was updated, False otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Set updated timestamp
            event_data["UpdatedOn"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Build the SQL query
            set_clause = ", ".join([f'"{k}" = ?' for k in event_data.keys()])
            
            query = f"UPDATE calendar SET {set_clause} WHERE \"SerialNo.\" = ?"
            
            cursor.execute(query, list(event_data.values()) + [serial_no])
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Updated event with SerialNo. {serial_no}")
                result = True
            else:
                logger.warning(f"Event with SerialNo. {serial_no} not found for update")
                result = False
                
            conn.close()
            return result
                
        except sqlite3.Error as e:
            logger.error(f"Error updating event: {e}")
            raise
    
    def delete_event(self, serial_no: int) -> bool:
        """
        Delete an event from the calendar.
        
        Args:
            serial_no: The serial number of the event to delete
            
        Returns:
            True if the event was deleted, False otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM calendar WHERE \"SerialNo.\" = ?", (serial_no,))
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Deleted event with SerialNo. {serial_no}")
                result = True
            else:
                logger.warning(f"Event with SerialNo. {serial_no} not found for deletion")
                result = False
                
            conn.close()
            return result
                
        except sqlite3.Error as e:
            logger.error(f"Error deleting event: {e}")
            raise
    
    def create_march_2025_calendar(self) -> None:
        """
        Create a calendar for March 2025 with one row per day.
        
        This method populates the calendar table with entries for each day in March 2025.
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Define the platforms and creators
            platforms = [
                "Twitter", "Facebook", "Instagram", "LinkedIn", "YouTube",
                "VC Pitch Deck", "Blog", "Email", "Podcast", "GeneralScripts"
            ]
            creators = ["Omkar", "Snowy"]
            
            # Define content types
            content_types = [
                "Industry Trends & News", "Business Tips & Hacks", "Case Studies",
                "Market Analysis", "Business Book Summaries", "Product Updates",
                "Customer Success Stories", "Behind the Scenes", "Team Spotlights",
                "Educational Content", "Thought Leadership", "Event Promotions"
            ]
            
            # Define formats
            formats = [
                "Post", "Story", "Reel", "Carousel", "Video", "Live Stream",
                "Infographic", "Poll", "Q&A", "Tutorial", "Interview", "Podcast Episode"
            ]
            
            # Get the current highest serial number
            cursor.execute("SELECT MAX(\"SerialNo.\") FROM calendar")
            result = cursor.fetchone()
            next_serial = 1 if result[0] is None else result[0] + 1
            
            # Create entries for each day in March 2025
            for day in range(1, 32):
                date = datetime(2025, 3, day)
                date_str = date.strftime("%Y-%m-%d")
                
                # Select random values for variety
                import random
                platform = platforms[day % len(platforms)]
                creator = creators[day % len(creators)]
                content_type = content_types[day % len(content_types)]
                format_type = formats[day % len(formats)]
                
                # Create the event data
                event_data = {
                    "SerialNo.": next_serial,
                    "Date": f"{date_str} 00:00:00",
                    "ContentType ": content_type,
                    "Format ": format_type,
                    "Platform ": platform,
                    "ScheduleTime ": "18:00:00",
                    "Status": "Scheduled",
                    "CreatedBy": creator,
                    "CreatedOn": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "UpdatedBy": creator,
                    "UpdatedOn": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Insert the event
                columns = ", ".join([f'"{k}"' for k in event_data.keys()])
                placeholders = ", ".join(["?" for _ in event_data.keys()])
                
                query = f"INSERT INTO calendar ({columns}) VALUES ({placeholders})"
                
                cursor.execute(query, list(event_data.values()))
                next_serial += 1
            
            conn.commit()
            conn.close()
            
            logger.info(f"Created calendar for March 2025 with 31 events")
                
        except sqlite3.Error as e:
            logger.error(f"Error creating March 2025 calendar: {e}")
            raise
