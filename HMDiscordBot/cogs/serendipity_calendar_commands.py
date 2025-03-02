"""
Serendipity Calendar commands for the Discord bot.
This module implements Discord commands for interacting with the serendipity calendar database.
"""

import os
import logging
import sqlite3
import discord
from discord import app_commands
from discord.ext import commands
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('serendipity_calendar_commands')

class SerendipityCalendarDBHandler:
    """
    Handler for interacting with the Serendipity Calendar database.
    
    This class provides methods for CRUD operations on the serendipity calendar table.
    """
    
    def __init__(self, db_path: str):
        """
        Initialize the database handler.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        logger.info(f"Initialized SerendipityCalendarDBHandler with database at {db_path}")
    
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
            
            # Create the serendipity calendar table if it doesn't exist
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS AccountTasks (
                SerialNo INTEGER PRIMARY KEY AUTOINCREMENT,
                Date TEXT,
                AccountTask TEXT,
                AccountTaskDescription TEXT,
                AccountTaskStatus TEXT,
                AccountTaskDueDate TEXT,
                AccountTaskCompletedDate TEXT,
                AccountTaskAssignedTo TEXT,
                AccountProjectName TEXT,
                ReferenceLinks TEXT
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
    
    def add_task(self, task_data: Dict[str, Any]) -> int:
        """
        Add a new task to the calendar.
        
        Args:
            task_data: Dictionary containing task data
            
        Returns:
            The serial number of the new task
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Build the SQL query
            columns = ", ".join([f'"{k}"' for k in task_data.keys()])
            placeholders = ", ".join(["?" for _ in task_data.keys()])
            
            query = f"INSERT INTO AccountTasks ({columns}) VALUES ({placeholders})"
            
            cursor.execute(query, list(task_data.values()))
            conn.commit()
            
            # Get the serial number of the new task
            serial_no = cursor.lastrowid
            conn.close()
            
            logger.info(f"Added new task with SerialNo {serial_no}")
            return serial_no
            
        except sqlite3.Error as e:
            logger.error(f"Error adding task: {e}")
            raise
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """
        Get all tasks from the calendar.
        
        Returns:
            List of dictionaries containing task data
        """
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM AccountTasks ORDER BY Date, SerialNo")
            
            tasks = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            logger.info(f"Retrieved {len(tasks)} tasks")
            return tasks
            
        except sqlite3.Error as e:
            logger.error(f"Error getting tasks: {e}")
            raise
    
    def get_task_by_id(self, serial_no: int) -> Optional[Dict[str, Any]]:
        """
        Get a task by its serial number.
        
        Args:
            serial_no: The serial number of the task
            
        Returns:
            Dictionary containing task data, or None if not found
        """
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM AccountTasks WHERE SerialNo = ?", (serial_no,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                logger.info(f"Retrieved task with SerialNo {serial_no}")
                return dict(row)
            else:
                logger.warning(f"Task with SerialNo {serial_no} not found")
                return None
                
        except sqlite3.Error as e:
            logger.error(f"Error getting task: {e}")
            raise
    
    def get_tasks_by_date(self, date: datetime) -> List[Dict[str, Any]]:
        """
        Get tasks for a specific date.
        
        Args:
            date: The date to get tasks for
            
        Returns:
            List of dictionaries containing task data
        """
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            date_str = date.strftime("%Y-%m-%d")
            
            cursor.execute(
                "SELECT * FROM AccountTasks WHERE Date LIKE ? ORDER BY SerialNo",
                (f"{date_str}%",)
            )
            
            tasks = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            logger.info(f"Retrieved {len(tasks)} tasks for date {date_str}")
            return tasks
                
        except sqlite3.Error as e:
            logger.error(f"Error getting tasks by date: {e}")
            raise
    
    def get_tasks_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """
        Get tasks within a date range.
        
        Args:
            start_date: The start date of the range
            end_date: The end date of the range
            
        Returns:
            List of dictionaries containing task data
        """
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            start_str = start_date.strftime("%Y-%m-%d")
            end_str = end_date.strftime("%Y-%m-%d")
            
            cursor.execute(
                "SELECT * FROM AccountTasks WHERE Date >= ? AND Date <= ? ORDER BY Date, SerialNo",
                (f"{start_str} 00:00:00", f"{end_str} 23:59:59")
            )
            
            tasks = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            logger.info(f"Retrieved {len(tasks)} tasks for date range {start_str} to {end_str}")
            return tasks
                
        except sqlite3.Error as e:
            logger.error(f"Error getting tasks by date range: {e}")
            raise
    
    def update_task(self, serial_no: int, task_data: Dict[str, Any]) -> bool:
        """
        Update an existing task.
        
        Args:
            serial_no: The serial number of the task to update
            task_data: Dictionary containing updated task data
            
        Returns:
            True if the task was updated, False otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Build the SQL query
            set_clause = ", ".join([f'"{k}" = ?' for k in task_data.keys()])
            
            query = f"UPDATE AccountTasks SET {set_clause} WHERE SerialNo = ?"
            
            cursor.execute(query, list(task_data.values()) + [serial_no])
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Updated task with SerialNo {serial_no}")
                result = True
            else:
                logger.warning(f"Task with SerialNo {serial_no} not found for update")
                result = False
                
            conn.close()
            return result
                
        except sqlite3.Error as e:
            logger.error(f"Error updating task: {e}")
            raise
    
    def delete_task(self, serial_no: int) -> bool:
        """
        Delete a task from the calendar.
        
        Args:
            serial_no: The serial number of the task to delete
            
        Returns:
            True if the task was deleted, False otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM AccountTasks WHERE SerialNo = ?", (serial_no,))
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Deleted task with SerialNo {serial_no}")
                result = True
            else:
                logger.warning(f"Task with SerialNo {serial_no} not found for deletion")
                result = False
                
            conn.close()
            return result
                
        except sqlite3.Error as e:
            logger.error(f"Error deleting task: {e}")
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


class TaskPaginator:
    """Paginator for displaying tasks in a paginated manner (for prefix commands)."""
    
    def __init__(self, ctx: commands.Context, tasks: List[Dict[str, Any]], title: str):
        """
        Initialize the paginator.
        
        Args:
            ctx: The command context
            tasks: List of tasks to paginate
            title: Title for the paginator
        """
        self.ctx = ctx
        self.tasks = tasks
        self.title = title
        self.page = 0
        self.total_pages = len(tasks)
        
    async def start(self):
        """Start the paginator."""
        if not self.tasks:
            await self.ctx.send("No tasks to display.")
            return
        
        # Create the message with the first page
        self.message = await self.ctx.send(embed=self.get_page_embed(), view=self.get_page_view())
    
    def get_page_embed(self) -> discord.Embed:
        """Get the embed for the current page."""
        task = self.tasks[self.page]
        
        embed = discord.Embed(
            title=f"{self.title} (Page {self.page + 1}/{self.total_pages})",
            color=discord.Color.blue()
        )
        
        # Add task details to the embed
        embed.add_field(name="Task ID", value=task["SerialNo"], inline=True)
        embed.add_field(name="Date", value=task["Date"].split()[0] if task["Date"] else "N/A", inline=True)
        embed.add_field(name="Status", value=task["AccountTaskStatus"], inline=True)
        
        embed.add_field(name="Task", value=task["AccountTask"], inline=False)
        embed.add_field(name="Description", value=task["AccountTaskDescription"], inline=False)
        
        embed.add_field(name="Project", value=task["AccountProjectName"], inline=True)
        embed.add_field(name="Assigned To", value=task["AccountTaskAssignedTo"], inline=True)
        
        embed.add_field(name="Due Date", value=task["AccountTaskDueDate"].split()[0] if task["AccountTaskDueDate"] else "N/A", inline=True)
        
        if task["AccountTaskCompletedDate"]:
            embed.add_field(name="Completed Date", value=task["AccountTaskCompletedDate"].split()[0], inline=True)
        
        if task["ReferenceLinks"]:
            embed.add_field(name="Reference Links", value=task["ReferenceLinks"], inline=False)
        
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


class TaskPaginatorView(discord.ui.View):
    """Paginator view for displaying tasks in a paginated manner (for slash commands)."""
    
    def __init__(self, tasks: List[Dict[str, Any]], title: str):
        """
        Initialize the paginator view.
        
        Args:
            tasks: List of tasks to paginate
            title: Title for the paginator
        """
        super().__init__(timeout=60)
        self.tasks = tasks
        self.title = title
        self.page = 0
        self.total_pages = len(tasks)
    
    def get_page_embed(self) -> discord.Embed:
        """Get the embed for the current page."""
        task = self.tasks[self.page]
        
        embed = discord.Embed(
            title=f"{self.title} (Page {self.page + 1}/{self.total_pages})",
            color=discord.Color.blue()
        )
        
        # Add task details to the embed
        embed.add_field(name="Task ID", value=task["SerialNo"], inline=True)
        embed.add_field(name="Date", value=task["Date"].split()[0] if task["Date"] else "N/A", inline=True)
        embed.add_field(name="Status", value=task["AccountTaskStatus"], inline=True)
        
        embed.add_field(name="Task", value=task["AccountTask"], inline=False)
        embed.add_field(name="Description", value=task["AccountTaskDescription"], inline=False)
        
        embed.add_field(name="Project", value=task["AccountProjectName"], inline=True)
        embed.add_field(name="Assigned To", value=task["AccountTaskAssignedTo"], inline=True)
        
        embed.add_field(name="Due Date", value=task["AccountTaskDueDate"].split()[0] if task["AccountTaskDueDate"] else "N/A", inline=True)
        
        if task["AccountTaskCompletedDate"]:
            embed.add_field(name="Completed Date", value=task["AccountTaskCompletedDate"].split()[0], inline=True)
        
        if task["ReferenceLinks"]:
            embed.add_field(name="Reference Links", value=task["ReferenceLinks"], inline=False)
        
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


class AddTaskModal(discord.ui.Modal, title="Add Task"):
    """Modal for adding a new task to the calendar."""
    
    def __init__(self, db_handler: SerendipityCalendarDBHandler):
        super().__init__()
        self.db_handler = db_handler
        
        # Create the form fields
        self.date_input = discord.ui.TextInput(
            label="Date (YYYY-MM-DD)",
            placeholder="e.g., 2025-03-15",
            required=True
        )
        self.add_item(self.date_input)
        
        self.task_input = discord.ui.TextInput(
            label="Task",
            placeholder="e.g., Implement user authentication",
            required=True
        )
        self.add_item(self.task_input)
        
        self.description_input = discord.ui.TextInput(
            label="Task Description",
            placeholder="Detailed description of the task",
            required=True,
            style=discord.TextStyle.paragraph
        )
        self.add_item(self.description_input)
        
        self.project_input = discord.ui.TextInput(
            label="Project Name",
            placeholder="e.g., E-commerce Website",
            required=True
        )
        self.add_item(self.project_input)
        
        self.assigned_to_input = discord.ui.TextInput(
            label="Assigned To",
            placeholder="e.g., John Doe",
            required=True
        )
        self.add_item(self.assigned_to_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle form submission."""
        try:
            # Parse the date
            try:
                date = datetime.strptime(self.date_input.value, "%Y-%m-%d")
            except ValueError:
                await interaction.response.send_message(
                    "Invalid date format. Please use YYYY-MM-DD.",
                    ephemeral=True
                )
                return
            
            # Create the task data
            task_data = {
                "Date": f"{self.date_input.value} 00:00:00",
                "AccountTask": self.task_input.value,
                "AccountTaskDescription": self.description_input.value,
                "AccountTaskStatus": "Pending",
                "AccountTaskDueDate": f"{self.date_input.value} 23:59:59",
                "AccountTaskCompletedDate": None,
                "AccountTaskAssignedTo": self.assigned_to_input.value,
                "AccountProjectName": self.project_input.value,
                "ReferenceLinks": ""
            }
            
            # Add the task to the database
            task_id = self.db_handler.add_task(task_data)
            
            # Create a success embed
            embed = discord.Embed(
                title="Task Added Successfully",
                description=f"Task #{task_id} has been added to the calendar.",
                color=discord.Color.green()
            )
            
            embed.add_field(name="Date", value=self.date_input.value, inline=True)
            embed.add_field(name="Task", value=self.task_input.value, inline=True)
            embed.add_field(name="Project", value=self.project_input.value, inline=True)
            embed.add_field(name="Assigned To", value=self.assigned_to_input.value, inline=True)
            embed.add_field(name="Status", value="Pending", inline=True)
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            logger.error(f"Error adding task: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error adding task: {str(e)}")


class UpdateTaskModal(discord.ui.Modal, title="Update Task"):
    """Modal for updating an existing task in the calendar."""
    
    def __init__(
        self, 
        db_handler: SerendipityCalendarDBHandler, 
        task: Dict[str, Any]
    ):
        super().__init__()
        self.db_handler = db_handler
        self.task = task
        self.task_id = task["SerialNo"]
        
        # Extract the date part from the timestamp
        date_str = task["Date"].split()[0] if task["Date"] else ""
        due_date_str = task["AccountTaskDueDate"].split()[0] if task["AccountTaskDueDate"] else ""
        
        # Create the form fields with current values
        self.date_input = discord.ui.TextInput(
            label="Date (YYYY-MM-DD)",
            placeholder="e.g., 2025-03-15",
            required=True,
            default=date_str
        )
        self.add_item(self.date_input)
        
        self.task_input = discord.ui.TextInput(
            label="Task",
            placeholder="e.g., Implement user authentication",
            required=True,
            default=task["AccountTask"]
        )
        self.add_item(self.task_input)
        
        self.description_input = discord.ui.TextInput(
            label="Task Description",
            placeholder="Detailed description of the task",
            required=True,
            style=discord.TextStyle.paragraph,
            default=task["AccountTaskDescription"]
        )
        self.add_item(self.description_input)
        
        self.project_input = discord.ui.TextInput(
            label="Project Name",
            placeholder="e.g., E-commerce Website",
            required=True,
            default=task["AccountProjectName"]
        )
        self.add_item(self.project_input)
        
        self.status_input = discord.ui.TextInput(
            label="Status",
            placeholder="e.g., Pending, In Progress, Completed",
            required=True,
            default=task["AccountTaskStatus"]
        )
        self.add_item(self.status_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle form submission."""
        try:
            # Parse the date
            try:
                date = datetime.strptime(self.date_input.value, "%Y-%m-%d")
            except ValueError:
                await interaction.response.send_message(
                    "Invalid date format. Please use YYYY-MM-DD.",
                    ephemeral=True
                )
                return
            
            # Create the task data
            task_data = {
                "Date": f"{self.date_input.value} 00:00:00",
                "AccountTask": self.task_input.value,
                "AccountTaskDescription": self.description_input.value,
                "AccountTaskStatus": self.status_input.value,
                "AccountTaskDueDate": f"{self.date_input.value} 23:59:59",
                "AccountProjectName": self.project_input.value
            }
            
            # If the status is "Completed", set the completion date
            if self.status_input.value.lower() == "completed":
                task_data["AccountTaskCompletedDate"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Update the task in the database
            success = self.db_handler.update_task(self.task_id, task_data)
            
            if success:
                # Create a success embed
                embed = discord.Embed(
                    title="Task Updated Successfully",
                    description=f"Task #{self.task_id} has been updated.",
                    color=discord.Color.green()
                )
                
                embed.add_field(name="Date", value=self.date_input.value, inline=True)
                embed.add_field(name="Task", value=self.task_input.value, inline=True)
                embed.add_field(name="Project", value=self.project_input.value, inline=True)
                embed.add_field(name="Status", value=self.status_input.value, inline=True)
                
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(
                    f"Error updating task #{self.task_id}. The task may have been deleted.",
                    ephemeral=True
                )
            
        except Exception as e:
            logger.error(f"Error updating task: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error updating task: {str(e)}")


class DateSelectionView(discord.ui.View):
    """View for selecting a date option."""
    
    def __init__(self, user: discord.User, callback):
        super().__init__(timeout=60)
        self.user = user
        self.callback = callback
        self.value = None
        self.custom_date = None
        
    @discord.ui.button(label="Today", style=discord.ButtonStyle.primary)
    async def today_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Select today's date."""
        if interaction.user != self.user:
            await interaction.response.send_message("This selection is not for you.", ephemeral=True)
            return
        
        self.value = "today"
        self.stop()
        await interaction.response.defer()
        await self.callback(interaction, self.value, None)
    
    @discord.ui.button(label="This Week", style=discord.ButtonStyle.primary)
    async def week_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Select this week's date range."""
        if interaction.user != self.user:
            await interaction.response.send_message("This selection is not for you.", ephemeral=True)
            return
        
        self.value = "week"
        self.stop()
        await interaction.response.defer()
        await self.callback(interaction, self.value, None)
    
    @discord.ui.button(label="Custom Date", style=discord.ButtonStyle.primary)
    async def custom_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Select a custom date."""
        if interaction.user != self.user:
            await interaction.response.send_message("This selection is not for you.", ephemeral=True)
            return
        
        # Create a modal for entering a custom date
        modal = CustomDateModal(self)
        await interaction.response.send_modal(modal)


class CustomDateModal(discord.ui.Modal, title="Enter Custom Date"):
    """Modal for entering a custom date."""
    
    def __init__(self, view: DateSelectionView):
        super().__init__()
        self.view = view
        
        self.date_input = discord.ui.TextInput(
            label="Date (YYYY-MM-DD)",
            placeholder="e.g., 2025-03-15",
            required=True
        )
        self.add_item(self.date_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle form submission."""
        try:
            # Parse the date
            try:
                date = datetime.strptime(self.date_input.value, "%Y-%m-%d")
            except ValueError:
                await interaction.response.send_message(
                    "Invalid date format. Please use YYYY-MM-DD.",
                    ephemeral=True
                )
                return
            
            self.view.value = "custom"
            self.view.custom_date = self.date_input.value
            self.view.stop()
            
            await interaction.response.defer()
            await self.view.callback(interaction, self.view.value, self.view.custom_date)
            
        except Exception as e:
            logger.error(f"Error processing custom date: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error processing custom date: {str(e)}")


class SerendipityCalendarCommands(commands.Cog):
    """
    Discord commands for interacting with the serendipity calendar database.
    
    This cog provides commands for adding, viewing, updating, and deleting tasks.
    """
    
    def __init__(self, bot: commands.Bot):
        """
        Initialize the serendipity calendar commands.
        
        Args:
            bot: The Discord bot instance
        """
        self.bot = bot
        
        # Get the database path
        base_dir = os.getcwd()
        db_path = os.path.join(base_dir, "DB", "Main", "SerendipityCalendar.db")
        
        # Create a custom DB handler for the serendipity calendar
        self.db_handler = SerendipityCalendarDBHandler(db_path)
        
        # Get the serendipity calendar channel ID
        self.channel_id = int(os.getenv('DISCORD_SERENDIPITY_CALENDAR_CHANNEL_ID', '0'))
        
        logger.info("Serendipity calendar commands initialized")
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Event handler that runs when the cog is loaded."""
        logger.info("Serendipity calendar commands cog is ready")
        
        # Create the database if it doesn't exist
        self.db_handler.ensure_db_exists()
    
    # ===== Prefix Commands =====
    
    @commands.command(name="serendipity_help")
    async def serendipity_help(self, ctx: commands.Context):
        """Display help information for serendipity calendar commands."""
        prefix = self.bot.command_prefix
        
        help_embed = discord.Embed(
            title="Serendipity Calendar Bot Commands",
            description="Here are the available serendipity calendar commands:",
            color=discord.Color.blue()
        )
        
        help_embed.add_field(
            name="Prefix Commands",
            value=(
                f"`{prefix}serendipity_help` - Show this help message\n"
                f"`{prefix}add_serendipity_task` - Add a new task (interactive)\n"
                f"`{prefix}view_serendipity_tasks` - View all tasks\n"
                f"`{prefix}view_serendipity_today` - View today's tasks\n"
                f"`{prefix}view_serendipity_week` - View this week's tasks\n"
                f"`{prefix}view_serendipity_date [YYYY-MM-DD]` - View tasks for a specific date\n"
                f"`{prefix}delete_serendipity_task [id]` - Delete a task\n"
                f"`{prefix}update_serendipity_task [id]` - Update a task (interactive)"
            ),
            inline=False
        )
        
        help_embed.add_field(
            name="Slash Commands",
            value=(
                "`/serendipity_help` - Show this help message\n"
                "`/add_serendipity_task` - Add a new task\n"
                "`/view_serendipity_tasks` - View all tasks\n"
                "`/view_serendipity_date` - View tasks for a specific date\n"
                "`/delete_serendipity_task` - Delete a task\n"
                "`/update_serendipity_task` - Update a task"
            ),
            inline=False
        )
        
        help_embed.set_footer(text="Use the buttons and dropdowns in responses for easier interaction")
        
        await ctx.send(embed=help_embed)
    
    @commands.command(name="add_serendipity_task")
    async def add_serendipity_task_prefix(self, ctx: commands.Context):
        """Add a new task to the calendar (interactive)."""
        # Check if the command is used in the correct channel
        if ctx.channel.id != self.channel_id and self.channel_id != 0:
            await ctx.send(f"Please use this command in the serendipity calendar channel.")
            return
        
        await ctx.send("Please use the `/add_serendipity_task` slash command to add a task with a form.")
    
    @commands.command(name="view_serendipity_tasks")
    async def view_serendipity_tasks_prefix(self, ctx: commands.Context):
        """View all tasks in the calendar."""
        # Check if the command is used in the correct channel
        if ctx.channel.id != self.channel_id and self.channel_id != 0:
            await ctx.send(f"Please use this command in the serendipity calendar channel.")
            return
        
        try:
            tasks = self.db_handler.get_all_tasks()
            
            if not tasks:
                await ctx.send("No tasks found in the calendar.")
                return
            
            # Create a paginator for the tasks
            paginator = TaskPaginator(ctx, tasks, "All Tasks")
            await paginator.start()
            
        except Exception as e:
            logger.error(f"Error viewing tasks: {str(e)}", exc_info=True)
            await ctx.send(f"Error viewing tasks: {str(e)}")
    
    @commands.command(name="view_serendipity_today")
    async def view_serendipity_today_prefix(self, ctx: commands.Context):
        """View today's tasks."""
        # Check if the command is used in the correct channel
        if ctx.channel.id != self.channel_id and self.channel_id != 0:
            await ctx.send(f"Please use this command in the serendipity calendar channel.")
            return
        
        try:
            today = datetime.now()
            tasks = self.db_handler.get_tasks_by_date(today)
            
            if not tasks:
                await ctx.send(f"No tasks found for today ({today.strftime('%Y-%m-%d')}).")
                return
            
            # Create a paginator for the tasks
            paginator = TaskPaginator(ctx, tasks, f"Tasks for {today.strftime('%Y-%m-%d')}")
            await paginator.start()
            
        except Exception as e:
            logger.error(f"Error viewing today's tasks: {str(e)}", exc_info=True)
            await ctx.send(f"Error viewing today's tasks: {str(e)}")
    
    @commands.command(name="view_serendipity_week")
    async def view_serendipity_week_prefix(self, ctx: commands.Context):
        """View this week's tasks."""
        # Check if the command is used in the correct channel
        if ctx.channel.id != self.channel_id and self.channel_id != 0:
            await ctx.send(f"Please use this command in the serendipity calendar channel.")
            return
        
        try:
            today = datetime.now()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            
            tasks = self.db_handler.get_tasks_by_date_range(start_of_week, end_of_week)
            
            if not tasks:
                await ctx.send(
                    f"No tasks found for this week "
                    f"({start_of_week.strftime('%Y-%m-%d')} to {end_of_week.strftime('%Y-%m-%d')})."
                )
                return
            
            # Create a paginator for the tasks
            paginator = TaskPaginator(
                ctx, 
                tasks, 
                f"Tasks for {start_of_week.strftime('%Y-%m-%d')} to {end_of_week.strftime('%Y-%m-%d')}"
            )
            await paginator.start()
            
        except Exception as e:
            logger.error(f"Error viewing this week's tasks: {str(e)}", exc_info=True)
            await ctx.send(f"Error viewing this week's tasks: {str(e)}")
    
    @commands.command(name="view_serendipity_date")
    async def view_serendipity_date_prefix(self, ctx: commands.Context, date_str: str = None):
        """
        View tasks for a specific date.
        
        Args:
            date_str: Date string in YYYY-MM-DD format
        """
        # Check if the command is used in the correct channel
        if ctx.channel.id != self.channel_id and self.channel_id != 0:
            await ctx.send(f"Please use this command in the serendipity calendar channel.")
            return
        
        if not date_str:
            await ctx.send("Please provide a date in YYYY-MM-DD format.")
            return
        
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            tasks = self.db_handler.get_tasks_by_date(date)
            
            if not tasks:
                await ctx.send(f"No tasks found for {date_str}.")
                return
            
            # Create a paginator for the tasks
            paginator = TaskPaginator(ctx, tasks, f"Tasks for {date_str}")
            await paginator.start()
            
        except ValueError:
            await ctx.send("Invalid date format. Please use YYYY-MM-DD.")
        except Exception as e:
            logger.error(f"Error viewing tasks for date: {str(e)}", exc_info=True)
            await ctx.send(f"Error viewing tasks for date: {str(e)}")
    
    @commands.command(name="delete_serendipity_task")
    async def delete_serendipity_task_prefix(self, ctx: commands.Context, task_id: int = None):
        """
        Delete a task from the calendar.
        
        Args:
            task_id: The serial number of the task to delete
        """
        # Check if the command is used in the correct channel
        if ctx.channel.id != self.channel_id and self.channel_id != 0:
            await ctx.send(f"Please use this command in the serendipity calendar channel.")
            return
        
        if not task_id:
            await ctx.send("Please provide a task ID to delete.")
            return
        
        try:
            # Get the task to confirm deletion
            task = self.db_handler.get_task_by_id(task_id)
            
            if not task:
                await ctx.send(f"Task with ID {task_id} not found.")
                return
            
            # Create a confirmation view
            view = ConfirmationView(ctx.author)
            
            # Create an embed for the task
            embed = discord.Embed(
                title=f"Confirm Deletion of Task #{task_id}",
                description="Are you sure you want to delete this task?",
                color=discord.Color.red()
            )
            
            embed.add_field(name="Date", value=task["Date"].split()[0] if task["Date"] else "N/A", inline=True)
            embed.add_field(name="Task", value=task["AccountTask"], inline=True)
            embed.add_field(name="Project", value=task["AccountProjectName"], inline=True)
            
            message = await ctx.send(embed=embed, view=view)
            
            # Wait for the user to confirm
            await view.wait()
            
            if view.value is True:
                # Delete the task
                success = self.db_handler.delete_task(task_id)
                
                if success:
                    embed.title = f"Task #{task_id} Deleted"
                    embed.description = "The task has been deleted successfully."
                    embed.color = discord.Color.green()
                else:
                    embed.title = f"Error Deleting Task #{task_id}"
                    embed.description = "An error occurred while deleting the task."
                    embed.color = discord.Color.red()
                
                await message.edit(embed=embed, view=None)
            else:
                embed.title = "Deletion Cancelled"
                embed.description = "The task deletion was cancelled."
                embed.color = discord.Color.blue()
                await message.edit(embed=embed, view=None)
            
        except Exception as e:
            logger.error(f"Error deleting task: {str(e)}", exc_info=True)
            await ctx.send(f"Error deleting task: {str(e)}")
    
    @commands.command(name="update_serendipity_task")
    async def update_serendipity_task_prefix(self, ctx: commands.Context, task_id: int = None):
        """
        Update a task in the calendar.
        
        Args:
            task_id: The serial number of the task to update
        """
        # Check if the command is used in the correct channel
        if ctx.channel.id != self.channel_id and self.channel_id != 0:
            await ctx.send(f"Please use this command in the serendipity calendar channel.")
            return
        
        if not task_id:
            await ctx.send("Please provide a task ID to update.")
            return
        
        await ctx.send("Please use the `/update_serendipity_task` slash command to update a task with a form.")
    
    # ===== Slash Commands =====
    
    @app_commands.command(name="serendipity_help", description="Display help information for serendipity calendar commands")
    async def serendipity_help_slash(self, interaction: discord.Interaction):
        """Display help information for serendipity calendar commands."""
        # Check if the command is used in the correct channel
        if interaction.channel_id != self.channel_id and self.channel_id != 0:
            await interaction.response.send_message(
                f"Please use this command in the serendipity calendar channel.",
                ephemeral=True
            )
            return
        
        prefix = self.bot.command_prefix
        
        help_embed = discord.Embed(
            title="Serendipity Calendar Bot Commands",
            description="Here are the available serendipity calendar commands:",
            color=discord.Color.blue()
        )
        
        help_embed.add_field(
            name="Prefix Commands",
            value=(
                f"`{prefix}serendipity_help` - Show this help message\n"
                f"`{prefix}add_serendipity_task` - Add a new task (interactive)\n"
                f"`{prefix}view_serendipity_tasks` - View all tasks\n"
                f"`{prefix}view_serendipity_today` - View today's tasks\n"
                f"`{prefix}view_serendipity_week` - View this week's tasks\n"
                f"`{prefix}view_serendipity_date [YYYY-MM-DD]` - View tasks for a specific date\n"
                f"`{prefix}delete_serendipity_task [id]` - Delete a task\n"
                f"`{prefix}update_serendipity_task [id]` - Update a task (interactive)"
            ),
            inline=False
        )
        
        help_embed.add_field(
            name="Slash Commands",
            value=(
                "`/serendipity_help` - Show this help message\n"
                "`/add_serendipity_task` - Add a new task\n"
                "`/view_serendipity_tasks` - View all tasks\n"
                "`/view_serendipity_date` - View tasks for a specific date\n"
                "`/delete_serendipity_task` - Delete a task\n"
                "`/update_serendipity_task` - Update a task"
            ),
            inline=False
        )
        
        help_embed.set_footer(text="Use the buttons and dropdowns in responses for easier interaction")
        
        await interaction.response.send_message(embed=help_embed, ephemeral=True)
    
    @app_commands.command(name="add_serendipity_task", description="Add a new task to the calendar")
    async def add_serendipity_task_slash(self, interaction: discord.Interaction):
        """Add a new task to the calendar."""
        # Check if the command is used in the correct channel
        if interaction.channel_id != self.channel_id and self.channel_id != 0:
            await interaction.response.send_message(
                f"Please use this command in the serendipity calendar channel.",
                ephemeral=True
            )
            return
        
        # Create a modal for adding a task
        modal = AddTaskModal(self.db_handler)
        await interaction.response.send_modal(modal)
    
    @app_commands.command(name="view_serendipity_tasks", description="View all tasks in the calendar")
    async def view_serendipity_tasks_slash(self, interaction: discord.Interaction):
        """View all tasks in the calendar."""
        # Check if the command is used in the correct channel
        if interaction.channel_id != self.channel_id and self.channel_id != 0:
            await interaction.response.send_message(
                f"Please use this command in the serendipity calendar channel.",
                ephemeral=True
            )
            return
        
        try:
            tasks = self.db_handler.get_all_tasks()
            
            if not tasks:
                await interaction.response.send_message("No tasks found in the calendar.")
                return
            
            # Create a paginator for the tasks
            paginator = TaskPaginatorView(tasks, "All Tasks")
            
            # Send the first page
            await interaction.response.send_message(
                embed=paginator.get_page_embed(),
                view=paginator
            )
            
        except Exception as e:
            logger.error(f"Error viewing tasks: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error viewing tasks: {str(e)}")
    
    @app_commands.command(name="view_serendipity_date", description="View tasks for a specific date")
    @app_commands.describe(
        date_option="Choose a date option",
        custom_date="Custom date in YYYY-MM-DD format (only needed for custom date option)"
    )
    @app_commands.choices(date_option=[
        app_commands.Choice(name="Today", value="today"),
        app_commands.Choice(name="This Week", value="week"),
        app_commands.Choice(name="Custom Date", value="custom")
    ])
    async def view_serendipity_date_slash(
        self, 
        interaction: discord.Interaction, 
        date_option: str,
        custom_date: Optional[str] = None
    ):
        """
        View tasks for a specific date.
        
        Args:
            date_option: Date option (today, week, custom)
            custom_date: Custom date in YYYY-MM-DD format
        """
        # Check if the command is used in the correct channel
        if interaction.channel_id != self.channel_id and self.channel_id != 0:
            await interaction.response.send_message(
                f"Please use this command in the serendipity calendar channel.",
                ephemeral=True
            )
            return
        
        try:
            tasks = []
            title = ""
            
            if date_option == "today":
                today = datetime.now()
                tasks = self.db_handler.get_tasks_by_date(today)
                title = f"Tasks for Today ({today.strftime('%Y-%m-%d')})"
                
            elif date_option == "week":
                today = datetime.now()
                start_of_week = today - timedelta(days=today.weekday())
                end_of_week = start_of_week + timedelta(days=6)
                
                tasks = self.db_handler.get_tasks_by_date_range(start_of_week, end_of_week)
                title = f"Tasks for This Week ({start_of_week.strftime('%Y-%m-%d')} to {end_of_week.strftime('%Y-%m-%d')})"
                
            elif date_option == "custom":
                if not custom_date:
                    await interaction.response.send_message(
                        "Please provide a custom date in YYYY-MM-DD format.",
                        ephemeral=True
                    )
                    return
                
                try:
                    date = datetime.strptime(custom_date, "%Y-%m-%d")
                    tasks = self.db_handler.get_tasks_by_date(date)
                    title = f"Tasks for {custom_date}"
                except ValueError:
                    await interaction.response.send_message(
                        "Invalid date format. Please use YYYY-MM-DD.",
                        ephemeral=True
                    )
                    return
            
            if not tasks:
                await interaction.response.send_message(f"No tasks found for the selected date option.")
                return
            
            # Create a paginator for the tasks
            paginator = TaskPaginatorView(tasks, title)
            
            # Send the first page
            await interaction.response.send_message(
                embed=paginator.get_page_embed(),
                view=paginator
            )
            
        except Exception as e:
            logger.error(f"Error viewing tasks for date: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error viewing tasks for date: {str(e)}")
    
    @app_commands.command(name="delete_serendipity_task", description="Delete a task from the calendar")
    @app_commands.describe(task_id="The ID of the task to delete")
    async def delete_serendipity_task_slash(self, interaction: discord.Interaction, task_id: int):
        """
        Delete a task from the calendar.
        
        Args:
            task_id: The serial number of the task to delete
        """
        # Check if the command is used in the correct channel
        if interaction.channel_id != self.channel_id and self.channel_id != 0:
            await interaction.response.send_message(
                f"Please use this command in the serendipity calendar channel.",
                ephemeral=True
            )
            return
        
        try:
            # Get the task to confirm deletion
            task = self.db_handler.get_task_by_id(task_id)
            
            if not task:
                await interaction.response.send_message(f"Task with ID {task_id} not found.", ephemeral=True)
                return
            
            # Create a confirmation view
            view = ConfirmationView(interaction.user)
            
            # Create an embed for the task
            embed = discord.Embed(
                title=f"Confirm Deletion of Task #{task_id}",
                description="Are you sure you want to delete this task?",
                color=discord.Color.red()
            )
            
            embed.add_field(name="Date", value=task["Date"].split()[0] if task["Date"] else "N/A", inline=True)
            embed.add_field(name="Task", value=task["AccountTask"], inline=True)
            embed.add_field(name="Project", value=task["AccountProjectName"], inline=True)
            
            await interaction.response.send_message(embed=embed, view=view)
            
            # Wait for the user to confirm
            await view.wait()
            
            if view.value is True:
                # Delete the task
                success = self.db_handler.delete_task(task_id)
                
                if success:
                    embed.title = f"Task #{task_id} Deleted"
                    embed.description = "The task has been deleted successfully."
                    embed.color = discord.Color.green()
                else:
                    embed.title = f"Error Deleting Task #{task_id}"
                    embed.description = "An error occurred while deleting the task."
                    embed.color = discord.Color.red()
                
                await interaction.edit_original_response(embed=embed, view=None)
            else:
                embed.title = "Deletion Cancelled"
                embed.description = "The task deletion was cancelled."
                embed.color = discord.Color.blue()
                await interaction.edit_original_response(embed=embed, view=None)
            
        except Exception as e:
            logger.error(f"Error deleting task: {str(e)}", exc_info=True)
            if interaction.response.is_done():
                await interaction.edit_original_response(content=f"Error deleting task: {str(e)}")
            else:
                await interaction.response.send_message(f"Error deleting task: {str(e)}")
    
    @app_commands.command(name="update_serendipity_task", description="Update a task in the calendar")
    @app_commands.describe(task_id="The ID of the task to update")
    async def update_serendipity_task_slash(self, interaction: discord.Interaction, task_id: int):
        """
        Update a task in the calendar.
        
        Args:
            task_id: The serial number of the task to update
        """
        # Check if the command is used in the correct channel
        if interaction.channel_id != self.channel_id and self.channel_id != 0:
            await interaction.response.send_message(
                f"Please use this command in the serendipity calendar channel.",
                ephemeral=True
            )
            return
        
        try:
            # Get the task to update
            task = self.db_handler.get_task_by_id(task_id)
            
            if not task:
                await interaction.response.send_message(f"Task with ID {task_id} not found.", ephemeral=True)
                return
            
            # Create a modal for updating the task
            modal = UpdateTaskModal(self.db_handler, task)
            await interaction.response.send_modal(modal)
            
        except Exception as e:
            logger.error(f"Error updating task: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error updating task: {str(e)}")


async def setup(bot: commands.Bot):
    """Add the serendipity calendar commands cog to the bot."""
    await bot.add_cog(SerendipityCalendarCommands(bot))
