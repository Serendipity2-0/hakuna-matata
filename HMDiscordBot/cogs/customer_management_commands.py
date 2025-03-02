"""
Customer Management commands for the Discord bot.
This module implements Discord commands for interacting with the customer management database.
"""

import os
import logging
import sqlite3
import discord
from discord import app_commands
from discord.ext import commands
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timedelta
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('customer_management_commands')

class CustomerManagementDBHandler:
    """
    Handler for interacting with the Customer Management database.
    
    This class provides methods for CRUD operations on the customer management tables.
    """
    
    def __init__(self, db_path: str):
        """
        Initialize the database handler.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        logger.info(f"Initialized CustomerManagementDBHandler with database at {db_path}")
    
    def ensure_db_exists(self) -> None:
        """
        Ensure the database exists and has the correct schema.
        
        If the database doesn't exist, it will be created with the correct schema.
        """
        try:
            # Check if the database file exists
            db_dir = os.path.dirname(self.db_path)
            if not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
                logger.info(f"Created directory {db_dir}")
            
            # Create or connect to the database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create the customer management tables if they don't exist
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS PastClients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                last_purchase_date TEXT,
                purchase_history TEXT,
                reason_for_leaving TEXT
            );
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
            );
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
            );
            ''')
            
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
            );
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info(f"Ensured database exists at {self.db_path}")
            
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            raise
    
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
    
    # ===== Client Management Methods =====
    
    def add_client(self, client_type: str, client_data: Dict[str, Any]) -> int:
        """
        Add a new client to the database.
        
        Args:
            client_type: Type of client (Past, Active, Prospective)
            client_data: Dictionary containing client data
            
        Returns:
            The ID of the new client
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Determine the table based on client type
            if client_type.lower() == "past":
                table = "PastClients"
            elif client_type.lower() == "active":
                table = "ActiveClients"
            elif client_type.lower() == "prospective":
                table = "ProspectiveClients"
            else:
                raise ValueError(f"Invalid client type: {client_type}")
            
            # Build the SQL query
            columns = ", ".join([f'"{k}"' for k in client_data.keys()])
            placeholders = ", ".join(["?" for _ in client_data.keys()])
            
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            cursor.execute(query, list(client_data.values()))
            conn.commit()
            
            # Get the ID of the new client
            client_id = cursor.lastrowid
            conn.close()
            
            logger.info(f"Added new {client_type} client with ID {client_id}")
            return client_id
            
        except sqlite3.Error as e:
            logger.error(f"Error adding client: {e}")
            raise
    
    def get_all_clients(self, client_type: str) -> List[Dict[str, Any]]:
        """
        Get all clients of a specific type.
        
        Args:
            client_type: Type of client (Past, Active, Prospective)
            
        Returns:
            List of dictionaries containing client data
        """
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Determine the table based on client type
            if client_type.lower() == "past":
                table = "PastClients"
            elif client_type.lower() == "active":
                table = "ActiveClients"
            elif client_type.lower() == "prospective":
                table = "ProspectiveClients"
            else:
                raise ValueError(f"Invalid client type: {client_type}")
            
            cursor.execute(f"SELECT * FROM {table} ORDER BY id")
            
            clients = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            logger.info(f"Retrieved {len(clients)} {client_type} clients")
            return clients
            
        except sqlite3.Error as e:
            logger.error(f"Error getting clients: {e}")
            raise
    
    def get_client_by_id(self, client_type: str, client_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a client by ID.
        
        Args:
            client_type: Type of client (Past, Active, Prospective)
            client_id: The ID of the client
            
        Returns:
            Dictionary containing client data, or None if not found
        """
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Determine the table based on client type
            if client_type.lower() == "past":
                table = "PastClients"
            elif client_type.lower() == "active":
                table = "ActiveClients"
            elif client_type.lower() == "prospective":
                table = "ProspectiveClients"
            else:
                raise ValueError(f"Invalid client type: {client_type}")
            
            cursor.execute(f"SELECT * FROM {table} WHERE id = ?", (client_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                logger.info(f"Retrieved {client_type} client with ID {client_id}")
                return dict(row)
            else:
                logger.warning(f"{client_type} client with ID {client_id} not found")
                return None
                
        except sqlite3.Error as e:
            logger.error(f"Error getting client: {e}")
            raise
    
    def update_client(self, client_type: str, client_id: int, client_data: Dict[str, Any]) -> bool:
        """
        Update an existing client.
        
        Args:
            client_type: Type of client (Past, Active, Prospective)
            client_id: The ID of the client to update
            client_data: Dictionary containing updated client data
            
        Returns:
            True if the client was updated, False otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Determine the table based on client type
            if client_type.lower() == "past":
                table = "PastClients"
            elif client_type.lower() == "active":
                table = "ActiveClients"
            elif client_type.lower() == "prospective":
                table = "ProspectiveClients"
            else:
                raise ValueError(f"Invalid client type: {client_type}")
            
            # Build the SQL query
            set_clause = ", ".join([f'"{k}" = ?' for k in client_data.keys()])
            
            query = f"UPDATE {table} SET {set_clause} WHERE id = ?"
            
            cursor.execute(query, list(client_data.values()) + [client_id])
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Updated {client_type} client with ID {client_id}")
                result = True
            else:
                logger.warning(f"{client_type} client with ID {client_id} not found for update")
                result = False
                
            conn.close()
            return result
                
        except sqlite3.Error as e:
            logger.error(f"Error updating client: {e}")
            raise
    
    def delete_client(self, client_type: str, client_id: int) -> bool:
        """
        Delete a client from the database.
        
        Args:
            client_type: Type of client (Past, Active, Prospective)
            client_id: The ID of the client to delete
            
        Returns:
            True if the client was deleted, False otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Determine the table based on client type
            if client_type.lower() == "past":
                table = "PastClients"
            elif client_type.lower() == "active":
                table = "ActiveClients"
            elif client_type.lower() == "prospective":
                table = "ProspectiveClients"
            else:
                raise ValueError(f"Invalid client type: {client_type}")
            
            cursor.execute(f"DELETE FROM {table} WHERE id = ?", (client_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Deleted {client_type} client with ID {client_id}")
                result = True
            else:
                logger.warning(f"{client_type} client with ID {client_id} not found for deletion")
                result = False
                
            conn.close()
            return result
                
        except sqlite3.Error as e:
            logger.error(f"Error deleting client: {e}")
            raise
    
    # ===== Meeting Management Methods =====
    
    def add_meeting(self, meeting_data: Dict[str, Any]) -> int:
        """
        Add a new meeting to the database.
        
        Args:
            meeting_data: Dictionary containing meeting data
            
        Returns:
            The ID of the new meeting
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Build the SQL query
            columns = ", ".join([f'"{k}"' for k in meeting_data.keys()])
            placeholders = ", ".join(["?" for _ in meeting_data.keys()])
            
            query = f"INSERT INTO Meetings ({columns}) VALUES ({placeholders})"
            
            cursor.execute(query, list(meeting_data.values()))
            conn.commit()
            
            # Get the ID of the new meeting
            meeting_id = cursor.lastrowid
            conn.close()
            
            logger.info(f"Added new meeting with ID {meeting_id}")
            return meeting_id
            
        except sqlite3.Error as e:
            logger.error(f"Error adding meeting: {e}")
            raise
    
    def get_all_meetings(self) -> List[Dict[str, Any]]:
        """
        Get all meetings from the database.
        
        Returns:
            List of dictionaries containing meeting data
        """
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM Meetings ORDER BY meeting_date, meeting_time")
            
            meetings = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            logger.info(f"Retrieved {len(meetings)} meetings")
            return meetings
            
        except sqlite3.Error as e:
            logger.error(f"Error getting meetings: {e}")
            raise
    
    def get_meeting_by_id(self, meeting_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a meeting by ID.
        
        Args:
            meeting_id: The ID of the meeting
            
        Returns:
            Dictionary containing meeting data, or None if not found
        """
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM Meetings WHERE id = ?", (meeting_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                logger.info(f"Retrieved meeting with ID {meeting_id}")
                return dict(row)
            else:
                logger.warning(f"Meeting with ID {meeting_id} not found")
                return None
                
        except sqlite3.Error as e:
            logger.error(f"Error getting meeting: {e}")
            raise
    
    def get_meetings_by_date(self, date: datetime) -> List[Dict[str, Any]]:
        """
        Get meetings for a specific date.
        
        Args:
            date: The date to get meetings for
            
        Returns:
            List of dictionaries containing meeting data
        """
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            date_str = date.strftime("%Y-%m-%d")
            
            cursor.execute(
                "SELECT * FROM Meetings WHERE meeting_date = ? ORDER BY meeting_time",
                (date_str,)
            )
            
            meetings = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            logger.info(f"Retrieved {len(meetings)} meetings for date {date_str}")
            return meetings
                
        except sqlite3.Error as e:
            logger.error(f"Error getting meetings by date: {e}")
            raise
    
    def get_meetings_by_client(self, client_id: int, client_type: str) -> List[Dict[str, Any]]:
        """
        Get meetings for a specific client.
        
        Args:
            client_id: The ID of the client
            client_type: The type of client (Past, Active, Prospective)
            
        Returns:
            List of dictionaries containing meeting data
        """
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM Meetings WHERE client_id = ? AND client_type = ? ORDER BY meeting_date, meeting_time",
                (client_id, client_type)
            )
            
            meetings = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            logger.info(f"Retrieved {len(meetings)} meetings for {client_type} client with ID {client_id}")
            return meetings
                
        except sqlite3.Error as e:
            logger.error(f"Error getting meetings by client: {e}")
            raise
    
    def update_meeting(self, meeting_id: int, meeting_data: Dict[str, Any]) -> bool:
        """
        Update an existing meeting.
        
        Args:
            meeting_id: The ID of the meeting to update
            meeting_data: Dictionary containing updated meeting data
            
        Returns:
            True if the meeting was updated, False otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Build the SQL query
            set_clause = ", ".join([f'"{k}" = ?' for k in meeting_data.keys()])
            
            query = f"UPDATE Meetings SET {set_clause} WHERE id = ?"
            
            cursor.execute(query, list(meeting_data.values()) + [meeting_id])
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Updated meeting with ID {meeting_id}")
                result = True
            else:
                logger.warning(f"Meeting with ID {meeting_id} not found for update")
                result = False
                
            conn.close()
            return result
                
        except sqlite3.Error as e:
            logger.error(f"Error updating meeting: {e}")
            raise
    
    def delete_meeting(self, meeting_id: int) -> bool:
        """
        Delete a meeting from the database.
        
        Args:
            meeting_id: The ID of the meeting to delete
            
        Returns:
            True if the meeting was deleted, False otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM Meetings WHERE id = ?", (meeting_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Deleted meeting with ID {meeting_id}")
                result = True
            else:
                logger.warning(f"Meeting with ID {meeting_id} not found for deletion")
                result = False
                
            conn.close()
            return result
                
        except sqlite3.Error as e:
            logger.error(f"Error deleting meeting: {e}")
            raise
    
    def get_upcoming_meetings(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get upcoming meetings within a specified number of days.
        
        Args:
            days: Number of days to look ahead
            
        Returns:
            List of dictionaries containing meeting data
        """
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            today = datetime.now().strftime("%Y-%m-%d")
            future_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
            
            cursor.execute(
                "SELECT * FROM Meetings WHERE meeting_date >= ? AND meeting_date <= ? ORDER BY meeting_date, meeting_time",
                (today, future_date)
            )
            
            meetings = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            logger.info(f"Retrieved {len(meetings)} upcoming meetings within {days} days")
            return meetings
                
        except sqlite3.Error as e:
            logger.error(f"Error getting upcoming meetings: {e}")
            raise
    
    def update_meeting_reminder(self, meeting_id: int, reminder_sent: str) -> bool:
        """
        Update the reminder status of a meeting.
        
        Args:
            meeting_id: The ID of the meeting
            reminder_sent: The reminder status
            
        Returns:
            True if the meeting was updated, False otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE Meetings SET reminder_sent = ? WHERE id = ?",
                (reminder_sent, meeting_id)
            )
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Updated reminder status for meeting with ID {meeting_id}")
                result = True
            else:
                logger.warning(f"Meeting with ID {meeting_id} not found for reminder update")
                result = False
                
            conn.close()
            return result
                
        except sqlite3.Error as e:
            logger.error(f"Error updating meeting reminder: {e}")
            raise
    
    def update_meeting_follow_up(self, meeting_id: int, follow_up_actions: str) -> bool:
        """
        Update the follow-up actions of a meeting.
        
        Args:
            meeting_id: The ID of the meeting
            follow_up_actions: The follow-up actions
            
        Returns:
            True if the meeting was updated, False otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE Meetings SET follow_up_actions = ? WHERE id = ?",
                (follow_up_actions, meeting_id)
            )
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Updated follow-up actions for meeting with ID {meeting_id}")
                result = True
            else:
                logger.warning(f"Meeting with ID {meeting_id} not found for follow-up update")
                result = False
                
            conn.close()
            return result
                
        except sqlite3.Error as e:
            logger.error(f"Error updating meeting follow-up: {e}")
            raise


class ConfirmationView(discord.ui.View):
    """View for confirming an action."""
    
    def __init__(self, user: discord.User):
        super().__init__(timeout=60)
        self.user = user
        self.value = None
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Confirm the action."""
        if interaction.user != self.user:
            await interaction.response.send_message("This confirmation is not for you.", ephemeral=True)
            return
        
        self.value = True
        self.stop()
        await interaction.response.defer()
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Cancel the action."""
        if interaction.user != self.user:
            await interaction.response.send_message("This confirmation is not for you.", ephemeral=True)
            return
        
        self.value = False
        self.stop()
        await interaction.response.defer()


class ClientPaginator:
    """Paginator for displaying clients in a paginated manner (for prefix commands)."""
    
    def __init__(self, ctx: commands.Context, clients: List[Dict[str, Any]], title: str, client_type: str):
        """
        Initialize the paginator.
        
        Args:
            ctx: The command context
            clients: List of clients to paginate
            title: Title for the paginator
            client_type: Type of client (Past, Active, Prospective)
        """
        self.ctx = ctx
        self.clients = clients
        self.title = title
        self.client_type = client_type
        self.page = 0
        self.total_pages = len(clients)
        
    async def start(self):
        """Start the paginator."""
        if not self.clients:
            await self.ctx.send("No clients to display.")
            return
        
        # Create the message with the first page
        self.message = await self.ctx.send(embed=self.get_page_embed(), view=self.get_page_view())
    
    def get_page_embed(self) -> discord.Embed:
        """Get the embed for the current page."""
        client = self.clients[self.page]
        
        embed = discord.Embed(
            title=f"{self.title} (Page {self.page + 1}/{self.total_pages})",
            color=discord.Color.blue()
        )
        
        # Add client details to the embed based on client type
        embed.add_field(name="Client ID", value=client["id"], inline=True)
        embed.add_field(name="Name", value=client["name"], inline=True)
        
        if "email" in client and client["email"]:
            embed.add_field(name="Email", value=client["email"], inline=True)
        
        if "phone" in client and client["phone"]:
            embed.add_field(name="Phone", value=client["phone"], inline=True)
        
        if self.client_type.lower() == "past":
            if "last_purchase_date" in client and client["last_purchase_date"]:
                embed.add_field(name="Last Purchase Date", value=client["last_purchase_date"], inline=True)
            
            if "purchase_history" in client and client["purchase_history"]:
                embed.add_field(name="Purchase History", value=client["purchase_history"], inline=False)
            
            if "reason_for_leaving" in client and client["reason_for_leaving"]:
                embed.add_field(name="Reason for Leaving", value=client["reason_for_leaving"], inline=False)
                
        elif self.client_type.lower() == "active":
            if "join_date" in client and client["join_date"]:
                embed.add_field(name="Join Date", value=client["join_date"], inline=True)
            
            if "subscription_plan" in client and client["subscription_plan"]:
                embed.add_field(name="Subscription Plan", value=client["subscription_plan"], inline=True)
            
            if "renewal_date" in client and client["renewal_date"]:
                embed.add_field(name="Renewal Date", value=client["renewal_date"], inline=True)
                
        elif self.client_type.lower() == "prospective":
            if "lead_source" in client and client["lead_source"]:
                embed.add_field(name="Lead Source", value=client["lead_source"], inline=True)
            
            if "first_contact_date" in client and client["first_contact_date"]:
                embed.add_field(name="First Contact Date", value=client["first_contact_date"], inline=True)
            
            if "follow_up_required" in client and client["follow_up_required"]:
                embed.add_field(name="Follow-up Required", value=client["follow_up_required"], inline=True)
        
        return embed
    
    def get_page_view(self) -> discord.ui.View:
        """Get the view for the current page."""
        view = discord.ui.View(timeout=60)
        
        # Previous button
        previous_button = discord.ui.Button(
            label="Previous",
            style=discord.ButtonStyle.gray,
            disabled=self.page == 0
        )
        previous_button.callback = self.previous_page
        view.add_item(previous_button)
        
        # Next button
        next_button = discord.ui.Button(
            label="Next",
            style=discord.ButtonStyle.gray,
            disabled=self.page == self.total_pages - 1
        )
        next_button.callback = self.next_page
        view.add_item(next_button)
        
        # Schedule Meeting button
        schedule_button = discord.ui.Button(
            label="Schedule Meeting",
            style=discord.ButtonStyle.primary
        )
        schedule_button.callback = self.schedule_meeting
        view.add_item(schedule_button)
        
        return view
    
    async def previous_page(self, interaction: discord.Interaction):
        """Go to the previous page."""
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("This pagination is not for you.", ephemeral=True)
            return
        
        self.page = max(0, self.page - 1)
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self.get_page_view())
    
    async def next_page(self, interaction: discord.Interaction):
        """Go to the next page."""
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("This pagination is not for you.", ephemeral=True)
            return
        
        self.page = min(self.total_pages - 1, self.page + 1)
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self.get_page_view())
    
    async def schedule_meeting(self, interaction: discord.Interaction):
        """Schedule a meeting with the current client."""
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("This action is not for you.", ephemeral=True)
            return
        
        client = self.clients[self.page]
        
        # Create a modal for scheduling a meeting
        modal = ScheduleMeetingModal(
            client_id=client["id"],
            client_type=self.client_type,
            client_name=client["name"]
        )
        
        await interaction.response.send_modal(modal)


class ClientPaginatorView(discord.ui.View):
    """Paginator view for displaying clients in a paginated manner (for slash commands)."""
    
    def __init__(self, clients: List[Dict[str, Any]], title: str, client_type: str):
        """
        Initialize the paginator view.
        
        Args:
            clients: List of clients to paginate
            title: Title for the paginator
            client_type: Type of client (Past, Active, Prospective)
        """
        super().__init__(timeout=60)
        self.clients = clients
        self.title = title
        self.client_type = client_type
        self.page = 0
        self.total_pages = len(clients)
    
    def get_page_embed(self) -> discord.Embed:
        """Get the embed for the current page."""
        client = self.clients[self.page]
        
        embed = discord.Embed(
            title=f"{self.title} (Page {self.page + 1}/{self.total_pages})",
            color=discord.Color.blue()
        )
        
        # Add client details to the embed based on client type
        embed.add_field(name="Client ID", value=client["id"], inline=True)
        embed.add_field(name="Name", value=client["name"], inline=True)
        
        if "email" in client and client["email"]:
            embed.add_field(name="Email", value=client["email"], inline=True)
        
        if "phone" in client and client["phone"]:
            embed.add_field(name="Phone", value=client["phone"], inline=True)
        
        if self.client_type.lower() == "past":
            if "last_purchase_date" in client and client["last_purchase_date"]:
                embed.add_field(name="Last Purchase Date", value=client["last_purchase_date"], inline=True)
            
            if "purchase_history" in client and client["purchase_history"]:
                embed.add_field(name="Purchase History", value=client["purchase_history"], inline=False)
            
            if "reason_for_leaving" in client and client["reason_for_leaving"]:
                embed.add_field(name="Reason for Leaving", value=client["reason_for_leaving"], inline=False)
                
        elif self.client_type.lower() == "active":
            if "join_date" in client and client["join_date"]:
                embed.add_field(name="Join Date", value=client["join_date"], inline=True)
            
            if "subscription_plan" in client and client["subscription_plan"]:
                embed.add_field(name="Subscription Plan", value=client["subscription_plan"], inline=True)
            
            if "renewal_date" in client and client["renewal_date"]:
                embed.add_field(name="Renewal Date", value=client["renewal_date"], inline=True)
                
        elif self.client_type.lower() == "prospective":
            if "lead_source" in client and client["lead_source"]:
                embed.add_field(name="Lead Source", value=client["lead_source"], inline=True)
            
            if "first_contact_date" in client and client["first_contact_date"]:
                embed.add_field(name="First Contact Date", value=client["first_contact_date"], inline=True)
            
            if "follow_up_required" in client and client["follow_up_required"]:
                embed.add_field(name="Follow-up Required", value=client["follow_up_required"], inline=True)
        
        return embed
    
    @discord.ui.button(label="Previous", style=discord.ButtonStyle.gray)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Go to the previous page."""
        self.page = max(0, self.page - 1)
        
        # Update the button states
        self.previous_button.disabled = self.page == 0
        self.next_button.disabled = self.page == self.total_pages - 1
        
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)
    
    @discord.ui.button(label="Next", style=discord.ButtonStyle.gray)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Go to the next page."""
        self.page = min(self.total_pages - 1, self.page + 1)
        
        # Update the button states
        self.previous_button.disabled = self.page == 0
        self.next_button.disabled = self.page == self.total_pages - 1
        
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)
    
    @discord.ui.button(label="Schedule Meeting", style=discord.ButtonStyle.primary)
    async def schedule_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Schedule a meeting with the current client."""
        client = self.clients[self.page]
        
        # Create a modal for scheduling a meeting
        modal = ScheduleMeetingModal(
            client_id=client["id"],
            client_type=self.client_type,
            client_name=client["name"]
        )
        
        await interaction.response.send_modal(modal)


class MeetingPaginator:
    """Paginator for displaying meetings in a paginated manner (for prefix commands)."""
    
    def __init__(self, ctx: commands.Context, meetings: List[Dict[str, Any]], title: str, db_handler: CustomerManagementDBHandler):
        """
        Initialize the paginator.
        
        Args:
            ctx: The command context
            meetings: List of meetings to paginate
            title: Title for the paginator
            db_handler: Database handler for client lookups
        """
        self.ctx = ctx
        self.meetings = meetings
        self.title = title
        self.db_handler = db_handler
        self.page = 0
        self.total_pages = len(meetings)
        
    async def start(self):
        """Start the paginator."""
        if not self.meetings:
            await self.ctx.send("No meetings to display.")
            return
        
        # Create the message with the first page
        self.message = await self.ctx.send(embed=await self.get_page_embed(), view=self.get_page_view())
    
    async def get_page_embed(self) -> discord.Embed:
        """Get the embed for the current page."""
        meeting = self.meetings[self.page]
        
        embed = discord.Embed(
            title=f"{self.title} (Page {self.page + 1}/{self.total_pages})",
            color=discord.Color.blue()
        )
        
        # Add meeting details to the embed
        embed.add_field(name="Meeting ID", value=meeting["id"], inline=True)
        
        # Get client details
        client_type = meeting["client_type"]
        client_id = meeting["client_id"]
        client = self.db_handler.get_client_by_id(client_type, client_id)
        
        if client:
            embed.add_field(name="Client", value=f"{client['name']} (ID: {client_id})", inline=True)
        else:
            embed.add_field(name="Client ID", value=client_id, inline=True)
        
        embed.add_field(name="Client Type", value=client_type.capitalize(), inline=True)
        embed.add_field(name="Meeting Type", value=meeting["meeting_type"], inline=True)
        embed.add_field(name="Date", value=meeting["meeting_date"], inline=True)
        embed.add_field(name="Time", value=meeting["meeting_time"], inline=True)
        
        if "meeting_details" in meeting and meeting["meeting_details"]:
            embed.add_field(name="Details", value=meeting["meeting_details"], inline=False)
        
        if "reminder_sent" in meeting and meeting["reminder_sent"]:
            embed.add_field(name="Reminder Sent", value=meeting["reminder_sent"], inline=True)
        
        if "follow_up_actions" in meeting and meeting["follow_up_actions"]:
            embed.add_field(name="Follow-up Actions", value=meeting["follow_up_actions"], inline=False)
        
        return embed
    
    def get_page_view(self) -> discord.ui.View:
        """Get the view for the current page."""
        view = discord.ui.View(timeout=60)
        
        # Previous button
        previous_button = discord.ui.Button(
            label="Previous",
            style=discord.ButtonStyle.gray,
            disabled=self.page == 0
        )
        previous_button.callback = self.previous_page
        view.add_item(previous_button)
        
        # Next button
        next_button = discord.ui.Button(
            label="Next",
            style=discord.ButtonStyle.gray,
            disabled=self.page == self.total_pages - 1
        )
        next_button.callback = self.next_page
        view.add_item(next_button)
        
        # Update Meeting button
        update_button = discord.ui.Button(
            label="Update Meeting",
            style=discord.ButtonStyle.primary
        )
        update_button.callback = self.update_meeting
        view.add_item(update_button)
        
        # Add Follow-up button
        followup_button = discord.ui.Button(
            label="Add Follow-up",
            style=discord.ButtonStyle.success
        )
        followup_button.callback = self.add_followup
        view.add_item(followup_button)
        
        return view
    
    async def previous_page(self, interaction: discord.Interaction):
        """Go to the previous page."""
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("This pagination is not for you.", ephemeral=True)
            return
        
        self.page = max(0, self.page - 1)
        await interaction.response.edit_message(embed=await self.get_page_embed(), view=self.get_page_view())
    
    async def next_page(self, interaction: discord.Interaction):
        """Go to the next page."""
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("This pagination is not for you.", ephemeral=True)
            return
        
        self.page = min(self.total_pages - 1, self.page + 1)
        await interaction.response.edit_message(embed=await self.get_page_embed(), view=self.get_page_view())
    
    async def update_meeting(self, interaction: discord.Interaction):
        """Update the current meeting."""
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("This action is not for you.", ephemeral=True)
            return
        
        meeting = self.meetings[self.page]
        
        # Create a modal for updating the meeting
        modal = UpdateMeetingModal(
            meeting_id=meeting["id"],
            meeting=meeting
        )
        
        await interaction.response.send_modal(modal)
    
    async def add_followup(self, interaction: discord.Interaction):
        """Add follow-up actions to the current meeting."""
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("This action is not for you.", ephemeral=True)
            return
        
        meeting = self.meetings[self.page]
        
        # Create a modal for adding follow-up actions
        modal = FollowUpActionsModal(
            meeting_id=meeting["id"],
            current_actions=meeting.get("follow_up_actions", "")
        )
        
        await interaction.response.send_modal(modal)


class MeetingPaginatorView(discord.ui.View):
    """Paginator view for displaying meetings in a paginated manner (for slash commands)."""
    
    def __init__(self, meetings: List[Dict[str, Any]], title: str, db_handler: CustomerManagementDBHandler):
        """
        Initialize the paginator view.
        
        Args:
            meetings: List of meetings to paginate
            title: Title for the paginator
            db_handler: Database handler for client lookups
        """
        super().__init__(timeout=60)
        self.meetings = meetings
        self.title = title
        self.db_handler = db_handler
        self.page = 0
        self.total_pages = len(meetings)
    
    async def get_page_embed(self) -> discord.Embed:
        """Get the embed for the current page."""
        meeting = self.meetings[self.page]
        
        embed = discord.Embed(
            title=f"{self.title} (Page {self.page + 1}/{self.total_pages})",
            color=discord.Color.blue()
        )
        
        # Add meeting details to the embed
        embed.add_field(name="Meeting ID", value=meeting["id"], inline=True)
        
        # Get client details
        client_type = meeting["client_type"]
        client_id = meeting["client_id"]
        client = self.db_handler.get_client_by_id(client_type, client_id)
        
        if client:
            embed.add_field(name="Client", value=f"{client['name']} (ID: {client_id})", inline=True)
        else:
            embed.add_field(name="Client ID", value=client_id, inline=True)
        
        embed.add_field(name="Client Type", value=client_type.capitalize(), inline=True)
        embed.add_field(name="Meeting Type", value=meeting["meeting_type"], inline=True)
        embed.add_field(name="Date", value=meeting["meeting_date"], inline=True)
        embed.add_field(name="Time", value=meeting["meeting_time"], inline=True)
        
        if "meeting_details" in meeting and meeting["meeting_details"]:
            embed.add_field(name="Details", value=meeting["meeting_details"], inline=False)
        
        if "reminder_sent" in meeting and meeting["reminder_sent"]:
            embed.add_field(name="Reminder Sent", value=meeting["reminder_sent"], inline=True)
        
        if "follow_up_actions" in meeting and meeting["follow_up_actions"]:
            embed.add_field(name="Follow-up Actions", value=meeting["follow_up_actions"], inline=False)
        
        return embed
    
    @discord.ui.button(label="Previous", style=discord.ButtonStyle.gray)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Go to the previous page."""
        self.page = max(0, self.page - 1)
        
        # Update the button states
        self.previous_button.disabled = self.page == 0
        self.next_button.disabled = self.page == self.total_pages - 1
        
        await interaction.response.edit_message(embed=await self.get_page_embed(), view=self)
    
    @discord.ui.button(label="Next", style=discord.ButtonStyle.gray)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Go to the next page."""
        self.page = min(self.total_pages - 1, self.page + 1)
        
        # Update the button states
        self.previous_button.disabled = self.page == 0
        self.next_button.disabled = self.page == self.total_pages - 1
        
        await interaction.response.edit_message(embed=await self.get_page_embed(), view=self)
    
    @discord.ui.button(label="Update Meeting", style=discord.ButtonStyle.primary)
    async def update_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Update the current meeting."""
        meeting = self.meetings[self.page]
        
        # Create a modal for updating the meeting
        modal = UpdateMeetingModal(
            meeting_id=meeting["id"],
            meeting=meeting
        )
        
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="Add Follow-up", style=discord.ButtonStyle.success)
    async def followup_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Add follow-up actions to the current meeting."""
        meeting = self.meetings[self.page]
        
        # Create a modal for adding follow-up actions
        modal = FollowUpActionsModal(
            meeting_id=meeting["id"],
            current_actions=meeting.get("follow_up_actions", "")
        )
        
        await interaction.response.send_modal(modal)


class ClientTypeSelect(discord.ui.Select):
    """Dropdown for selecting client type."""
    
    def __init__(self, placeholder: str = "Select client type"):
        """
        Initialize the client type select.
        
        Args:
            placeholder: Placeholder text for the select
        """
        options = [
            discord.SelectOption(
                label="Active Clients",
                description="Currently active clients",
                value="active"
            ),
            discord.SelectOption(
                label="Past Clients",
                description="Former clients",
                value="past"
            ),
            discord.SelectOption(
                label="Prospective Clients",
                description="Potential future clients",
                value="prospective"
            )
        ]
        
        super().__init__(
            placeholder=placeholder,
            min_values=1,
            max_values=1,
            options=options
        )


class AddClientModal(discord.ui.Modal, title="Add New Client"):
    """Modal for adding a new client to the database."""
    
    def __init__(self, db_handler: CustomerManagementDBHandler, client_type: str):
        """
        Initialize the modal.
        
        Args:
            db_handler: Database handler for client operations
            client_type: Type of client (Past, Active, Prospective)
        """
        super().__init__()
        self.db_handler = db_handler
        self.client_type = client_type
        
        # Common fields for all client types
        self.name_input = discord.ui.TextInput(
            label="Client Name",
            placeholder="e.g., Acme Corporation",
            required=True
        )
        self.add_item(self.name_input)
        
        self.email_input = discord.ui.TextInput(
            label="Email",
            placeholder="e.g., contact@acme.com",
            required=False
        )
        self.add_item(self.email_input)
        
        self.phone_input = discord.ui.TextInput(
            label="Phone",
            placeholder="e.g., +1-555-123-4567",
            required=False
        )
        self.add_item(self.phone_input)
        
        # Type-specific fields
        if client_type.lower() == "past":
            self.last_purchase_date_input = discord.ui.TextInput(
                label="Last Purchase Date (YYYY-MM-DD)",
                placeholder="e.g., 2024-12-31",
                required=False
            )
            self.add_item(self.last_purchase_date_input)
            
            self.reason_for_leaving_input = discord.ui.TextInput(
                label="Reason for Leaving",
                placeholder="Why did the client leave?",
                required=False,
                style=discord.TextStyle.paragraph
            )
            self.add_item(self.reason_for_leaving_input)
            
        elif client_type.lower() == "active":
            self.join_date_input = discord.ui.TextInput(
                label="Join Date (YYYY-MM-DD)",
                placeholder="e.g., 2024-01-01",
                required=False
            )
            self.add_item(self.join_date_input)
            
            self.subscription_plan_input = discord.ui.TextInput(
                label="Subscription Plan",
                placeholder="e.g., Premium, Basic, Enterprise",
                required=False
            )
            self.add_item(self.subscription_plan_input)
            
            self.renewal_date_input = discord.ui.TextInput(
                label="Renewal Date (YYYY-MM-DD)",
                placeholder="e.g., 2025-01-01",
                required=False
            )
            self.add_item(self.renewal_date_input)
            
        elif client_type.lower() == "prospective":
            self.lead_source_input = discord.ui.TextInput(
                label="Lead Source",
                placeholder="e.g., Website, Referral, Conference",
                required=False
            )
            self.add_item(self.lead_source_input)
            
            self.first_contact_date_input = discord.ui.TextInput(
                label="First Contact Date (YYYY-MM-DD)",
                placeholder="e.g., 2025-01-15",
                required=False
            )
            self.add_item(self.first_contact_date_input)
            
            self.follow_up_required_input = discord.ui.TextInput(
                label="Follow-up Required",
                placeholder="e.g., Yes, No, Call next week",
                required=False
            )
            self.add_item(self.follow_up_required_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle form submission."""
        try:
            # Create the client data dictionary
            client_data = {
                "name": self.name_input.value,
                "email": self.email_input.value,
                "phone": self.phone_input.value
            }
            
            # Add type-specific fields
            if self.client_type.lower() == "past":
                client_data["last_purchase_date"] = self.last_purchase_date_input.value
                client_data["purchase_history"] = ""  # Default empty
                client_data["reason_for_leaving"] = self.reason_for_leaving_input.value
                
            elif self.client_type.lower() == "active":
                client_data["join_date"] = self.join_date_input.value
                client_data["subscription_plan"] = self.subscription_plan_input.value
                client_data["renewal_date"] = self.renewal_date_input.value
                
            elif self.client_type.lower() == "prospective":
                client_data["lead_source"] = self.lead_source_input.value
                client_data["first_contact_date"] = self.first_contact_date_input.value
                client_data["follow_up_required"] = self.follow_up_required_input.value
            
            # Add the client to the database
            client_id = self.db_handler.add_client(self.client_type, client_data)
            
            # Create a success embed
            embed = discord.Embed(
                title="Client Added Successfully",
                description=f"{self.client_type.capitalize()} client #{client_id} has been added to the database.",
                color=discord.Color.green()
            )
            
            embed.add_field(name="Name", value=self.name_input.value, inline=True)
            
            if self.email_input.value:
                embed.add_field(name="Email", value=self.email_input.value, inline=True)
            
            if self.phone_input.value:
                embed.add_field(name="Phone", value=self.phone_input.value, inline=True)
            
            # Add type-specific fields to the embed
            if self.client_type.lower() == "past":
                if self.last_purchase_date_input.value:
                    embed.add_field(name="Last Purchase Date", value=self.last_purchase_date_input.value, inline=True)
                
                if self.reason_for_leaving_input.value:
                    embed.add_field(name="Reason for Leaving", value=self.reason_for_leaving_input.value, inline=False)
                
            elif self.client_type.lower() == "active":
                if self.join_date_input.value:
                    embed.add_field(name="Join Date", value=self.join_date_input.value, inline=True)
                
                if self.subscription_plan_input.value:
                    embed.add_field(name="Subscription Plan", value=self.subscription_plan_input.value, inline=True)
                
                if self.renewal_date_input.value:
                    embed.add_field(name="Renewal Date", value=self.renewal_date_input.value, inline=True)
                
            elif self.client_type.lower() == "prospective":
                if self.lead_source_input.value:
                    embed.add_field(name="Lead Source", value=self.lead_source_input.value, inline=True)
                
                if self.first_contact_date_input.value:
                    embed.add_field(name="First Contact Date", value=self.first_contact_date_input.value, inline=True)
                
                if self.follow_up_required_input.value:
                    embed.add_field(name="Follow-up Required", value=self.follow_up_required_input.value, inline=True)
            
            # Add a button to schedule a meeting with this client
            view = discord.ui.View(timeout=60)
            schedule_button = discord.ui.Button(
                label="Schedule Meeting",
                style=discord.ButtonStyle.primary,
                custom_id=f"schedule_meeting_{client_id}_{self.client_type}"
            )
            
            async def schedule_callback(interaction: discord.Interaction):
                modal = ScheduleMeetingModal(
                    client_id=client_id,
                    client_type=self.client_type,
                    client_name=self.name_input.value
                )
                await interaction.response.send_modal(modal)
            
            schedule_button.callback = schedule_callback
            view.add_item(schedule_button)
            
            await interaction.response.send_message(embed=embed, view=view)
            
        except Exception as e:
            logger.error(f"Error adding client: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error adding client: {str(e)}")


class ScheduleMeetingModal(discord.ui.Modal, title="Schedule Meeting"):
    """Modal for scheduling a meeting with a client."""
    
    def __init__(self, client_id: int, client_type: str, client_name: str):
        """
        Initialize the modal.
        
        Args:
            client_id: The ID of the client
            client_type: Type of client (Past, Active, Prospective)
            client_name: Name of the client
        """
        super().__init__()
        self.client_id = client_id
        self.client_type = client_type
        self.client_name = client_name
        
        # Create the form fields
        self.meeting_type_input = discord.ui.TextInput(
            label="Meeting Type",
            placeholder="e.g., Sales Call, Follow-up, Demo",
            required=True
        )
        self.add_item(self.meeting_type_input)
        
        self.meeting_date_input = discord.ui.TextInput(
            label="Meeting Date (YYYY-MM-DD)",
            placeholder="e.g., 2025-03-15",
            required=True
        )
        self.add_item(self.meeting_date_input)
        
        self.meeting_time_input = discord.ui.TextInput(
            label="Meeting Time (HH:MM)",
            placeholder="e.g., 14:30",
            required=True
        )
        self.add_item(self.meeting_time_input)
        
        self.meeting_details_input = discord.ui.TextInput(
            label="Meeting Details",
            placeholder="Details about the meeting",
            required=False,
            style=discord.TextStyle.paragraph
        )
        self.add_item(self.meeting_details_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle form submission."""
        try:
            # Parse the date and time
            try:
                date = datetime.strptime(self.meeting_date_input.value, "%Y-%m-%d")
                time = datetime.strptime(self.meeting_time_input.value, "%H:%M").time()
            except ValueError:
                await interaction.response.send_message(
                    "Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time.",
                    ephemeral=True
                )
                return
            
            # Create the meeting data
            meeting_data = {
                "client_id": self.client_id,
                "client_type": self.client_type,
                "meeting_type": self.meeting_type_input.value,
                "meeting_date": self.meeting_date_input.value,
                "meeting_time": self.meeting_time_input.value,
                "meeting_details": self.meeting_details_input.value,
                "reminder_sent": "No",
                "follow_up_actions": ""
            }
            
            # Get the database handler from the cog
            db_handler = None
            for cog in interaction.client.cogs.values():
                if isinstance(cog, CustomerManagementCommands):
                    db_handler = cog.db_handler
                    break
            
            if not db_handler:
                await interaction.response.send_message(
                    "Error: Could not find the database handler.",
                    ephemeral=True
                )
                return
            
            # Add the meeting to the database
            meeting_id = db_handler.add_meeting(meeting_data)
            
            # Create a success embed
            embed = discord.Embed(
                title="Meeting Scheduled Successfully",
                description=f"Meeting #{meeting_id} has been scheduled with {self.client_name}.",
                color=discord.Color.green()
            )
            
            embed.add_field(name="Client", value=f"{self.client_name} (ID: {self.client_id})", inline=True)
            embed.add_field(name="Client Type", value=self.client_type.capitalize(), inline=True)
            embed.add_field(name="Meeting Type", value=self.meeting_type_input.value, inline=True)
            embed.add_field(name="Date", value=self.meeting_date_input.value, inline=True)
            embed.add_field(name="Time", value=self.meeting_time_input.value, inline=True)
            
            if self.meeting_details_input.value:
                embed.add_field(name="Details", value=self.meeting_details_input.value, inline=False)
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            logger.error(f"Error scheduling meeting: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error scheduling meeting: {str(e)}")


class UpdateMeetingModal(discord.ui.Modal, title="Update Meeting"):
    """Modal for updating a meeting."""
    
    def __init__(self, meeting_id: int, meeting: Dict[str, Any]):
        """
        Initialize the modal.
        
        Args:
            meeting_id: The ID of the meeting
            meeting: Dictionary containing meeting data
        """
        super().__init__()
        self.meeting_id = meeting_id
        
        # Create the form fields with current values
        self.meeting_type_input = discord.ui.TextInput(
            label="Meeting Type",
            placeholder="e.g., Sales Call, Follow-up, Demo",
            required=True,
            default=meeting.get("meeting_type", "")
        )
        self.add_item(self.meeting_type_input)
        
        self.meeting_date_input = discord.ui.TextInput(
            label="Meeting Date (YYYY-MM-DD)",
            placeholder="e.g., 2025-03-15",
            required=True,
            default=meeting.get("meeting_date", "")
        )
        self.add_item(self.meeting_date_input)
        
        self.meeting_time_input = discord.ui.TextInput(
            label="Meeting Time (HH:MM)",
            placeholder="e.g., 14:30",
            required=True,
            default=meeting.get("meeting_time", "")
        )
        self.add_item(self.meeting_time_input)
        
        self.meeting_details_input = discord.ui.TextInput(
            label="Meeting Details",
            placeholder="Details about the meeting",
            required=False,
            style=discord.TextStyle.paragraph,
            default=meeting.get("meeting_details", "")
        )
        self.add_item(self.meeting_details_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle form submission."""
        try:
            # Parse the date and time
            try:
                date = datetime.strptime(self.meeting_date_input.value, "%Y-%m-%d")
                time = datetime.strptime(self.meeting_time_input.value, "%H:%M").
