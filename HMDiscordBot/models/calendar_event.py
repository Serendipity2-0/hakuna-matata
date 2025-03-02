"""
Calendar event model for the Discord bot.
This module defines the data model for calendar events.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class CalendarEvent:
    """
    Data model for a calendar event.
    
    This class represents an event in the calendar with all its attributes.
    """
    
    serial_no: Optional[int] = None
    date: datetime = field(default_factory=datetime.now)
    content_type: str = ""
    format: str = ""
    platform: str = ""
    schedule_time: str = "18:00:00"
    status: str = "Scheduled"
    created_by: str = ""
    created_on: datetime = field(default_factory=datetime.now)
    updated_by: str = ""
    updated_on: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """
        Convert the event to a dictionary for database storage.
        
        Returns:
            Dictionary representation of the event
        """
        return {
            "SerialNo.": self.serial_no,
            "Date": self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "ContentType ": self.content_type,
            "Format ": self.format,
            "Platform ": self.platform,
            "ScheduleTime ": self.schedule_time,
            "Status": self.status,
            "CreatedBy": self.created_by,
            "CreatedOn": self.created_on.strftime("%Y-%m-%d %H:%M:%S"),
            "UpdatedBy": self.updated_by,
            "UpdatedOn": self.updated_on.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CalendarEvent':
        """
        Create an event from a dictionary.
        
        Args:
            data: Dictionary containing event data
            
        Returns:
            A CalendarEvent instance
        """
        return cls(
            serial_no=data.get("SerialNo."),
            date=datetime.strptime(data.get("Date", ""), "%Y-%m-%d %H:%M:%S") if data.get("Date") else datetime.now(),
            content_type=data.get("ContentType ", ""),
            format=data.get("Format ", ""),
            platform=data.get("Platform ", ""),
            schedule_time=data.get("ScheduleTime ", "18:00:00"),
            status=data.get("Status", "Scheduled"),
            created_by=data.get("CreatedBy", ""),
            created_on=datetime.strptime(data.get("CreatedOn", ""), "%Y-%m-%d %H:%M:%S") if data.get("CreatedOn") else datetime.now(),
            updated_by=data.get("UpdatedBy", ""),
            updated_on=datetime.strptime(data.get("UpdatedOn", ""), "%Y-%m-%d %H:%M:%S") if data.get("UpdatedOn") else datetime.now()
        )
    
    def __str__(self) -> str:
        """
        Get a string representation of the event.
        
        Returns:
            String representation of the event
        """
        return (
            f"Event #{self.serial_no}: {self.content_type} on {self.date.strftime('%Y-%m-%d')} "
            f"at {self.schedule_time} ({self.platform})"
        )
