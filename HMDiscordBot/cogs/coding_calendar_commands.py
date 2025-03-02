"""
Coding Calendar commands for the Discord bot.
This module implements Discord commands for interacting with the coding calendar database.
"""

import os
import logging
import sqlite3
import discord
from discord import app_commands
from discord.ext import commands
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timedelta

from HMDiscordBot.utils.db_handler import CalendarDBHandler
from HMDiscordBot.utils.config import ConfigManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('coding_calendar_commands')

class CodingCalendarCommands(commands.Cog):
    """
    Discord commands for interacting with the coding calendar database.
    
    This cog provides commands for adding, viewing, updating, and deleting coding tasks.
    """
    
    def __init__(self, bot: commands.Bot):
        """
        Initialize the coding calendar commands.
        
        Args:
            bot: The Discord bot instance
        """
        self.bot = bot
        self.config = ConfigManager()
        
        # Get the database path
        base_dir = os.getcwd()
        db_base_path = self.config.get('database', 'base_path', default='DB/Main')
        db_file = self.config.get('database', 'files', default={}).get('coding', 'CodingCalendar.db')
        self.db_path = os.path.join(base_dir, db_base_path, db_file)
        
        # Create a custom DB handler for the coding calendar
        self.db_handler = CodingCalendarDBHandler(self.db_path)
        
        # Get the coding calendar channel ID
        self.channel_id = int(os.getenv('DISCORD_CODING_CALENDAR_CHANNEL_ID', '0'))
        
        logger.info("Coding calendar commands initialized")
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Event handler that runs when the cog is loaded."""
        logger.info("Coding calendar commands cog is ready")
        
        # Create the database if it doesn't exist
        self.db_handler.ensure_db_exists()
        
        # Check if the database has data for March 2025
        if not self.db_handler.has_march_2025_data():
            logger.info("Creating mock data for March 2025")
            self.db_handler.create_march_2025_data()
    
    # ===== Prefix Commands =====
    
    @commands.command(name="coding_help")
    async def coding_help(self, ctx: commands.Context):
        """Display help information for coding calendar commands."""
        prefix = self.bot.command_prefix
        
        help_embed = discord.Embed(
            title="Coding Calendar Bot Commands",
            description="Here are the available coding calendar commands:",
            color=discord.Color.blue()
        )
        
        help_embed.add_field(
            name="Prefix Commands",
            value=(
                f"`{prefix}coding_help` - Show this help message\n"
                f"`{prefix}add_coding_task` - Add a new coding task (interactive)\n"
                f"`{prefix}view_coding_tasks` - View all coding tasks\n"
                f"`{prefix}view_coding_today` - View today's coding tasks\n"
                f"`{prefix}view_coding_week` - View this week's coding tasks\n"
                f"`{prefix}view_coding_date [YYYY-MM-DD]` - View coding tasks for a specific date\n"
                f"`{prefix}delete_coding_task [id]` - Delete a coding task\n"
                f"`{prefix}update_coding_task [id]` - Update a coding task (interactive)"
            ),
            inline=False
        )
        
        help_embed.add_field(
            name="Slash Commands",
            value=(
                "`/coding_help` - Show this help message\n"
                "`/add_coding_task` - Add a new coding task\n"
                "`/view_coding_tasks` - View all coding tasks\n"
                "`/view_coding_date` - View coding tasks for a specific date\n"
                "`/delete_coding_task` - Delete a coding task\n"
                "`/update_coding_task` - Update a coding task"
            ),
            inline=False
        )
        
        help_embed.set_footer(text="Use the buttons and dropdowns in responses for easier interaction")
        
        await ctx.send(embed=help_embed)
    
    @commands.command(name="add_coding_task")
    async def add_coding_task_prefix(self, ctx: commands.Context):
        """Add a new coding task to the calendar (interactive)."""
        # Check if the command is used in the correct channel
        if ctx.channel.id != self.channel_id and self.channel_id != 0:
            await ctx.send(f"Please use this command in the coding calendar channel.")
            return
        
        await ctx.send("Please use the `/add_coding_task` slash command to add a task with a form.")
    
    @commands.command(name="view_coding_tasks")
    async def view_coding_tasks_prefix(self, ctx: commands.Context):
        """View all coding tasks in the calendar."""
        # Check if the command is used in the correct channel
        if ctx.channel.id != self.channel_id and self.channel_id != 0:
            await ctx.send(f"Please use this command in the coding calendar channel.")
            return
        
        try:
            tasks = self.db_handler.get_all_tasks()
            
            if not tasks:
                await ctx.send("No coding tasks found in the calendar.")
                return
            
            # Create a paginator for the tasks
            paginator = CodingTaskPaginator(ctx, tasks, "All Coding Tasks")
            await paginator.start()
            
        except Exception as e:
            logger.error(f"Error viewing coding tasks: {str(e)}", exc_info=True)
            await ctx.send(f"Error viewing coding tasks: {str(e)}")
    
    @commands.command(name="view_coding_today")
    async def view_coding_today_prefix(self, ctx: commands.Context):
        """View today's coding tasks."""
        # Check if the command is used in the correct channel
        if ctx.channel.id != self.channel_id and self.channel_id != 0:
            await ctx.send(f"Please use this command in the coding calendar channel.")
            return
        
        try:
            today = datetime.now()
            tasks = self.db_handler.get_tasks_by_date(today)
            
            if not tasks:
                await ctx.send(f"No coding tasks found for today ({today.strftime('%Y-%m-%d')}).")
                return
            
            # Create a paginator for the tasks
            paginator = CodingTaskPaginator(ctx, tasks, f"Coding Tasks for {today.strftime('%Y-%m-%d')}")
            await paginator.start()
            
        except Exception as e:
            logger.error(f"Error viewing today's coding tasks: {str(e)}", exc_info=True)
            await ctx.send(f"Error viewing today's coding tasks: {str(e)}")
    
    @commands.command(name="view_coding_week")
    async def view_coding_week_prefix(self, ctx: commands.Context):
        """View this week's coding tasks."""
        # Check if the command is used in the correct channel
        if ctx.channel.id != self.channel_id and self.channel_id != 0:
            await ctx.send(f"Please use this command in the coding calendar channel.")
            return
        
        try:
            today = datetime.now()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            
            tasks = self.db_handler.get_tasks_by_date_range(start_of_week, end_of_week)
            
            if not tasks:
                await ctx.send(
                    f"No coding tasks found for this week "
                    f"({start_of_week.strftime('%Y-%m-%d')} to {end_of_week.strftime('%Y-%m-%d')})."
                )
                return
            
            # Create a paginator for the tasks
            paginator = CodingTaskPaginator(
                ctx, 
                tasks, 
                f"Coding Tasks for {start_of_week.strftime('%Y-%m-%d')} to {end_of_week.strftime('%Y-%m-%d')}"
            )
            await paginator.start()
            
        except Exception as e:
            logger.error(f"Error viewing this week's coding tasks: {str(e)}", exc_info=True)
            await ctx.send(f"Error viewing this week's coding tasks: {str(e)}")
    
    @commands.command(name="view_coding_date")
    async def view_coding_date_prefix(self, ctx: commands.Context, date_str: str = None):
        """
        View coding tasks for a specific date.
        
        Args:
            date_str: Date string in YYYY-MM-DD format
        """
        # Check if the command is used in the correct channel
        if ctx.channel.id != self.channel_id and self.channel_id != 0:
            await ctx.send(f"Please use this command in the coding calendar channel.")
            return
        
        if not date_str:
            await ctx.send("Please provide a date in YYYY-MM-DD format.")
            return
        
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            tasks = self.db_handler.get_tasks_by_date(date)
            
            if not tasks:
                await ctx.send(f"No coding tasks found for {date_str}.")
                return
            
            # Create a paginator for the tasks
            paginator = CodingTaskPaginator(ctx, tasks, f"Coding Tasks for {date_str}")
            await paginator.start()
            
        except ValueError:
            await ctx.send("Invalid date format. Please use YYYY-MM-DD.")
        except Exception as e:
            logger.error(f"Error viewing coding tasks for date: {str(e)}", exc_info=True)
            await ctx.send(f"Error viewing coding tasks for date: {str(e)}")
    
    @commands.command(name="delete_coding_task")
    async def delete_coding_task_prefix(self, ctx: commands.Context, task_id: int = None):
        """
        Delete a coding task from the calendar.
        
        Args:
            task_id: The serial number of the task to delete
        """
        # Check if the command is used in the correct channel
        if ctx.channel.id != self.channel_id and self.channel_id != 0:
            await ctx.send(f"Please use this command in the coding calendar channel.")
            return
        
        if not task_id:
            await ctx.send("Please provide a task ID to delete.")
            return
        
        try:
            # Get the task to confirm deletion
            task = self.db_handler.get_task_by_id(task_id)
            
            if not task:
                await ctx.send(f"Coding task with ID {task_id} not found.")
                return
            
            # Create a confirmation view
            view = ConfirmationView(ctx.author)
            
            # Create an embed for the task
            embed = discord.Embed(
                title=f"Confirm Deletion of Coding Task #{task_id}",
                description="Are you sure you want to delete this coding task?",
                color=discord.Color.red()
            )
            
            embed.add_field(name="Date", value=task["Date"].split()[0] if task["Date"] else "N/A", inline=True)
            embed.add_field(name="Task", value=task["CodingTask"], inline=True)
            embed.add_field(name="Project", value=task["CodingProjectName"], inline=True)
            
            message = await ctx.send(embed=embed, view=view)
            
            # Wait for the user to confirm
            await view.wait()
            
            if view.value is True:
                # Delete the task
                success = self.db_handler.delete_task(task_id)
                
                if success:
                    embed.title = f"Coding Task #{task_id} Deleted"
                    embed.description = "The coding task has been deleted successfully."
                    embed.color = discord.Color.green()
                else:
                    embed.title = f"Error Deleting Coding Task #{task_id}"
                    embed.description = "An error occurred while deleting the coding task."
                    embed.color = discord.Color.red()
                
                await message.edit(embed=embed, view=None)
            else:
                embed.title = "Deletion Cancelled"
                embed.description = "The coding task deletion was cancelled."
                embed.color = discord.Color.blue()
                await message.edit(embed=embed, view=None)
            
        except Exception as e:
            logger.error(f"Error deleting coding task: {str(e)}", exc_info=True)
            await ctx.send(f"Error deleting coding task: {str(e)}")
    
    @commands.command(name="update_coding_task")
    async def update_coding_task_prefix(self, ctx: commands.Context, task_id: int = None):
        """
        Update a coding task in the calendar.
        
        Args:
            task_id: The serial number of the task to update
        """
        # Check if the command is used in the correct channel
        if ctx.channel.id != self.channel_id and self.channel_id != 0:
            await ctx.send(f"Please use this command in the coding calendar channel.")
            return
        
        if not task_id:
            await ctx.send("Please provide a task ID to update.")
            return
        
        await ctx.send("Please use the `/update_coding_task` slash command to update a task with a form.")
    
    # ===== Slash Commands =====
    
    @app_commands.command(name="coding_help", description="Display help information for coding calendar commands")
    async def coding_help_slash(self, interaction: discord.Interaction):
        """Display help information for coding calendar commands."""
        # Check if the command is used in the correct channel
        if interaction.channel_id != self.channel_id and self.channel_id != 0:
            await interaction.response.send_message(
                f"Please use this command in the coding calendar channel.",
                ephemeral=True
            )
            return
        
        prefix = self.bot.command_prefix
        
        help_embed = discord.Embed(
            title="Coding Calendar Bot Commands",
            description="Here are the available coding calendar commands:",
            color=discord.Color.blue()
        )
        
        help_embed.add_field(
            name="Prefix Commands",
            value=(
                f"`{prefix}coding_help` - Show this help message\n"
                f"`{prefix}add_coding_task` - Add a new coding task (interactive)\n"
                f"`{prefix}view_coding_tasks` - View all coding tasks\n"
                f"`{prefix}view_coding_today` - View today's coding tasks\n"
                f"`{prefix}view_coding_week` - View this week's coding tasks\n"
                f"`{prefix}view_coding_date [YYYY-MM-DD]` - View coding tasks for a specific date\n"
                f"`{prefix}delete_coding_task [id]` - Delete a coding task\n"
                f"`{prefix}update_coding_task [id]` - Update a coding task (interactive)"
            ),
            inline=False
        )
        
        help_embed.add_field(
            name="Slash Commands",
            value=(
                "`/coding_help` - Show this help message\n"
                "`/add_coding_task` - Add a new coding task\n"
                "`/view_coding_tasks` - View all coding tasks\n"
                "`/view_coding_date` - View coding tasks for a specific date\n"
                "`/delete_coding_task` - Delete a coding task\n"
                "`/update_coding_task` - Update a coding task"
            ),
            inline=False
        )
        
        help_embed.set_footer(text="Use the buttons and dropdowns in responses for easier interaction")
        
        await interaction.response.send_message(embed=help_embed, ephemeral=True)
    
    @app_commands.command(name="add_coding_task", description="Add a new coding task to the calendar")
    async def add_coding_task_slash(self, interaction: discord.Interaction):
        """Add a new coding task to the calendar."""
        # Check if the command is used in the correct channel
        if interaction.channel_id != self.channel_id and self.channel_id != 0:
            await interaction.response.send_message(
                f"Please use this command in the coding calendar channel.",
                ephemeral=True
            )
            return
        
        # Create a modal for adding a task
        modal = AddCodingTaskModal(self.db_handler)
        await interaction.response.send_modal(modal)
    
    @app_commands.command(name="view_coding_tasks", description="View all coding tasks in the calendar")
    async def view_coding_tasks_slash(self, interaction: discord.Interaction):
        """View all coding tasks in the calendar."""
        # Check if the command is used in the correct channel
        if interaction.channel_id != self.channel_id and self.channel_id != 0:
            await interaction.response.send_message(
                f"Please use this command in the coding calendar channel.",
                ephemeral=True
            )
            return
        
        try:
            tasks = self.db_handler.get_all_tasks()
            
            if not tasks:
                await interaction.response.send_message("No coding tasks found in the calendar.")
                return
            
            # Create a paginator for the tasks
            paginator = CodingTaskPaginatorView(tasks, "All Coding Tasks")
            
            # Send the first page
            await interaction.response.send_message(
                embed=paginator.get_page_embed(),
                view=paginator
            )
            
        except Exception as e:
            logger.error(f"Error viewing coding tasks: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error viewing coding tasks: {str(e)}")
    
    @app_commands.command(name="view_coding_date", description="View coding tasks for a specific date")
    @app_commands.describe(
        date_option="Choose a date option",
        custom_date="Custom date in YYYY-MM-DD format (only needed for custom date option)"
    )
    @app_commands.choices(date_option=[
        app_commands.Choice(name="Today", value="today"),
        app_commands.Choice(name="This Week", value="week"),
        app_commands.Choice(name="Custom Date", value="custom")
    ])
    async def view_coding_date_slash(
        self, 
        interaction: discord.Interaction, 
        date_option: str,
        custom_date: Optional[str] = None
    ):
        """
        View coding tasks for a specific date.
        
        Args:
            date_option: Date option (today, week, custom)
            custom_date: Custom date in YYYY-MM-DD format
        """
        # Check if the command is used in the correct channel
        if interaction.channel_id != self.channel_id and self.channel_id != 0:
            await interaction.response.send_message(
                f"Please use this command in the coding calendar channel.",
                ephemeral=True
            )
            return
        
        try:
            tasks = []
            title = ""
            
            if date_option == "today":
                today = datetime.now()
                tasks = self.db_handler.get_tasks_by_date(today)
                title = f"Coding Tasks for Today ({today.strftime('%Y-%m-%d')})"
                
            elif date_option == "week":
                today = datetime.now()
                start_of_week = today - timedelta(days=today.weekday())
                end_of_week = start_of_week + timedelta(days=6)
                
                tasks = self.db_handler.get_tasks_by_date_range(start_of_week, end_of_week)
                title = f"Coding Tasks for This Week ({start_of_week.strftime('%Y-%m-%d')} to {end_of_week.strftime('%Y-%m-%d')})"
                
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
                    title = f"Coding Tasks for {custom_date}"
                except ValueError:
                    await interaction.response.send_message(
                        "Invalid date format. Please use YYYY-MM-DD.",
                        ephemeral=True
                    )
                    return
            
            if not tasks:
                await interaction.response.send_message(f"No coding tasks found for the selected date option.")
                return
            
            # Create a paginator for the tasks
            paginator = CodingTaskPaginatorView(tasks, title)
            
            # Send the first page
            await interaction.response.send_message(
                embed=paginator.get_page_embed(),
                view=paginator
            )
            
        except Exception as e:
            logger.error(f"Error viewing coding tasks for date: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error viewing coding tasks for date: {str(e)}")
    
    @app_commands.command(name="delete_coding_task", description="Delete a coding task from the calendar")
    @app_commands.describe(task_id="The ID of the coding task to delete")
    async def delete_coding_task_slash(self, interaction: discord.Interaction, task_id: int):
        """
        Delete a coding task from the calendar.
        
        Args:
            task_id: The serial number of the task to delete
        """
        # Check if the command is used in the correct channel
        if interaction.channel_id != self.channel_id and self.channel_id != 0:
            await interaction.response.send_message(
                f"Please use this command in the coding calendar channel.",
                ephemeral=True
            )
            return
        
        try:
            # Get the task to confirm deletion
            task = self.db_handler.get_task_by_id(task_id)
            
            if not task:
                await interaction.response.send_message(f"Coding task with ID {task_id} not found.", ephemeral=True)
                return
            
            # Create a confirmation view
            view = ConfirmationView(interaction.user)
            
            # Create an embed for the task
            embed = discord.Embed(
                title=f"Confirm Deletion of Coding Task #{task_id}",
                description="Are you sure you want to delete this coding task?",
                color=discord.Color.red()
            )
            
            embed.add_field(name="Date", value=task["Date"].split()[0] if task["Date"] else "N/A", inline=True)
            embed.add_field(name="Task", value=task["CodingTask"], inline=True)
            embed.add_field(name="Project", value=task["CodingProjectName"], inline=True)
            
            await interaction.response.send_message(embed=embed, view=view)
            
            # Wait for the user to confirm
            await view.wait()
            
            if view.value is True:
                # Delete the task
                success = self.db_handler.delete_task(task_id)
                
                if success:
                    embed.title = f"Coding Task #{task_id} Deleted"
                    embed.description = "The coding task has been deleted successfully."
                    embed.color = discord.Color.green()
                else:
                    embed.title = f"Error Deleting Coding Task #{task_id}"
                    embed.description = "An error occurred while deleting the coding task."
                    embed.color = discord.Color.red()
                
                await interaction.edit_original_response(embed=embed, view=None)
            else:
                embed.title = "Deletion Cancelled"
                embed.description = "The coding task deletion was cancelled."
                embed.color = discord.Color.blue()
                await interaction.edit_original_response(embed=embed, view=None)
            
        except Exception as e:
            logger.error(f"Error deleting coding task: {str(e)}", exc_info=True)
            if interaction.response.is_done():
                await interaction.edit_original_response(content=f"Error deleting coding task: {str(e)}")
            else:
                await interaction.response.send_message(f"Error deleting coding task: {str(e)}")
    
    @app_commands.command(name="update_coding_task", description="Update a coding task in the calendar")
    @app_commands.describe(task_id="The ID of the coding task to update")
    async def update_coding_task_slash(self, interaction: discord.Interaction, task_id: int):
        """
        Update a coding task in the calendar.
        
        Args:
            task_id: The serial number of the task to update
        """
        # Check if the command is used in the correct channel
        if interaction.channel_id != self.channel_id and self.channel_id != 0:
            await interaction.response.send_message(
                f"Please use this command in the coding calendar channel.",
                ephemeral=True
            )
            return
        
        try:
            # Get the task to update
            task = self.db_handler.get_task_by_id(task_id)
            
            if not task:
                await interaction.response.send_message(f"Coding task with ID {task_id} not found.", ephemeral=True)
                return
            
            # Create a modal for updating the task
            modal = UpdateCodingTaskModal(self.db_handler, task)
            await interaction.response.send_modal(modal)
            
        except Exception as e:
            logger.error(f"Error updating coding task: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error updating coding task: {str(e)}")


# ===== UI Components =====

class AddCodingTaskModal(discord.ui.Modal, title="Add Coding Task"):
    """Modal for adding a new coding task to the calendar."""
    
    def __init__(self, db_handler: 'CodingCalendarDBHandler'):
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
            label="Coding Task",
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
                "CodingTask": self.task_input.value,
                "CodingTaskDescription": self.description_input.value,
                "CodingTaskStatus": "Pending",
                "CodingTaskDueDate": f"{self.date_input.value} 23:59:59",
                "CodingTaskCompletedDate": None,
                "CodingTaskAssignedTo": self.assigned_to_input.value,
                "CodingProjectName": self.project_input.value,
                "ReferenceLinks": "",
                "CreatedBy": interaction.user.name,
                "CreatedOn": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "UpdatedBy": interaction.user.name,
                "UpdatedOn": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Add the task to the database
            task_id = self.db_handler.add_task(task_data)
            
            # Create a success embed
            embed = discord.Embed(
                title="Coding Task Added Successfully",
                description=f"Coding task #{task_id} has been added to the calendar.",
                color=discord.Color.green()
            )
            
            embed.add_field(name="Date", value=self.date_input.value, inline=True)
            embed.add_field(name="Task", value=self.task_input.value, inline=True)
            embed.add_field(name="Project", value=self.project_input.value, inline=True)
            embed.add_field(name="Assigned To", value=self.assigned_to_input.value, inline=True)
            embed.add_field(name="Status", value="Pending", inline=True)
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            logger.error(f"Error adding coding task: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error adding coding task: {str(e)}")


class UpdateCodingTaskModal(discord.ui.Modal, title="Update Coding Task"):
    """Modal for updating an existing coding task in the calendar."""
    
    def __init__(
        self, 
        db_handler: 'CodingCalendarDBHandler', 
        task: Dict[str, Any]
    ):
        super().__init__()
        self.db_handler = db_handler
        self.task = task
        self.task_id = task["SerialNo."]
        
        # Extract the date part from the timestamp
        date_str = task["Date"].split()[0] if task["Date"] else ""
        due_date_str = task["CodingTaskDueDate"].split()[0] if task["CodingTaskDueDate"] else ""
        
        # Create the form fields with current values
        self.date_input = discord.ui.TextInput(
            label="Date (YYYY-MM-DD)",
            placeholder="e.g., 2025-03-15",
            required=True,
            default=date_str
        )
        self.add_item(self.date_input)
        
        self.task_input = discord.ui.TextInput(
            label="Coding Task",
            placeholder="e.g., Implement user authentication",
            required=True,
            default=task["CodingTask"]
        )
        self.add_item(self.task_input)
        
        self.description_input = discord.ui.TextInput(
            label="Task Description",
            placeholder="Detailed description of the task",
            required=True,
            style=discord.TextStyle.paragraph,
            default=task["CodingTaskDescription"]
        )
        self.add_item(self.description_input)
        
        self.project_input = discord.ui.TextInput(
            label="Project Name",
            placeholder="e.g., E-commerce Website",
            required=True,
            default=task["CodingProjectName"]
        )
        self.add_item(self.project_input)
        
        self.status_input = discord.ui.TextInput(
            label="Status",
            placeholder="e.g., Pending, In Progress, Completed",
            required=True,
            default=task["CodingTaskStatus"]
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
                "CodingTask": self.task_input.value,
                "CodingTaskDescription": self.description_input.value,
                "CodingTaskStatus": self.status_input.value,
                "CodingTaskDueDate": f"{self.date_input.value} 23:59:59",
                "CodingProjectName": self.project_input.value,
                "UpdatedBy": interaction.user.name,
                "UpdatedOn": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # If the status is "Completed", set the completion date
            if self.status_input.value.lower() == "completed":
                task_data["CodingTaskCompletedDate"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Update the task in the database
            success = self.db_handler.update_task(self.task_id, task_data)
            
            if success:
                # Create a success embed
                embed = discord.Embed(
                    title="Coding Task Updated Successfully",
                    description=f"Coding task #{self.task_id} has been updated.",
                    color=discord.Color.green()
                )
                
                embed.add_field(name="Date", value=self.date_input.value, inline=True)
                embed.add_field(name="Task", value=self.task_input.value, inline=True)
                embed.add_field(name="Project", value=self.project_input.value, inline=True)
                embed.add_field(name="Status", value=self.status_input.value, inline=True)
                
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(
                    f"Error updating coding task #{self.task_id}. The task may have been deleted.",
                    ephemeral=True
                )
            
        except Exception as e:
            logger.error(f"Error updating coding task: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error updating coding task: {str(e)}")


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


class CodingTaskPaginator:
    """Paginator for displaying coding tasks in a paginated manner (for prefix commands)."""
    
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
            await self.ctx.send("No coding tasks to display.")
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
        embed.add_field(name="Task ID", value=task["SerialNo."], inline=True)
        embed.add_field(name="Date", value=task["Date"].split()[0] if task["Date"] else "N/A", inline=True)
        embed.add_field(name="Status", value=task["CodingTaskStatus"], inline=True)
        
        embed.add_field(name="Task", value=task["CodingTask"], inline=False)
        embed.add_field(name="Description", value=task["CodingTaskDescription"], inline=False)
        
        embed.add_field(name="Project", value=task["CodingProjectName"], inline=True)
        embed.add_field(name="Assigned To", value=task["CodingTaskAssignedTo"], inline=True)
        
        embed.add_field(name="Due Date", value=task["CodingTaskDueDate"].split()[0] if task["CodingTaskDueDate"] else "N/A", inline=True)
        
        if task["CodingTaskCompletedDate"]:
            embed.add_field(name="Completed Date", value=task["CodingTaskCompletedDate"].split()[0], inline=True)
        
        if task["ReferenceLinks"]:
            embed.add_field(name="Reference Links", value=task["ReferenceLinks"], inline=False)
            
        if "CreatedBy" in task and task["CreatedBy"]:
            embed.add_field(name="Created By", value=task["CreatedBy"], inline=True)
            
        if "CreatedOn" in task and task["CreatedOn"]:
            embed.add_field(name="Created On", value=task["CreatedOn"], inline=True)
            
        if "UpdatedBy" in task and task["UpdatedBy"]:
            embed.add_field(name="Updated By", value=task["UpdatedBy"], inline=True)
            
        if "UpdatedOn" in task and task["UpdatedOn"]:
            embed.add_field(name="Updated On", value=task["UpdatedOn"], inline=True)
        
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


class CodingTaskPaginatorView(discord.ui.View):
    """Paginator view for displaying coding tasks in a paginated manner (for slash commands)."""
    
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
        embed.add_field(name="Task ID", value=task["SerialNo."], inline=True)
        embed.add_field(name="Date", value=task["Date"].split()[0] if task["Date"] else "N/A", inline=True)
        embed.add_field(name="Status", value=task["CodingTaskStatus"], inline=True)
        
        embed.add_field(name="Task", value=task["CodingTask"], inline=False)
        embed.add_field(name="Description", value=task["CodingTaskDescription"], inline=False)
        
        embed.add_field(name="Project", value=task["CodingProjectName"], inline=True)
        embed.add_field(name="Assigned To", value=task["CodingTaskAssignedTo"], inline=True)
        
        embed.add_field(name="Due Date", value=task["CodingTaskDueDate"].split()[0] if task["CodingTaskDueDate"] else "N/A", inline=True)
        
        if task["CodingTaskCompletedDate"]:
            embed.add_field(name="Completed Date", value=task["CodingTaskCompletedDate"].split()[0], inline=True)
        
        if task["ReferenceLinks"]:
            embed.add_field(name="Reference Links", value=task["ReferenceLinks"], inline=False)
            
        if "CreatedBy" in task and task["CreatedBy"]:
            embed.add_field(name="Created By", value=task["CreatedBy"], inline=True)
            
        if "CreatedOn" in task and task["CreatedOn"]:
            embed.add_field(name="Created On", value=task["CreatedOn"], inline=True)
            
        if "UpdatedBy" in task and task["UpdatedBy"]:
            embed.add_field(name="Updated By", value=task["UpdatedBy"], inline=True)
            
        if "UpdatedOn" in task and task["UpdatedOn"]:
            embed.add_field(name="Updated On", value=task["UpdatedOn"], inline=True)
        
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


class CodingCalendarDBHandler:
    """
    Handler for interacting with the Coding Calendar database.
    
    This class provides methods for CRUD operations on the coding calendar table.
    """
    
    def __init__(self, db_path: str):
        """
        Initialize the database handler.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        logger.info(f"Initialized CodingCalendarDBHandler with database at {db_path}")
    
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
            
            # Create the coding calendar table if it doesn't exist
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
            
            conn.commit()
            conn.close()
            
            logger.info(f"Ensured database exists at {self.db_path}")
            
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            raise
    
    def has_march_2025_data(self) -> bool:
        """
        Check if the database has data for March 2025.
        
        Returns:
            True if data exists, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT COUNT(*) FROM CodingCalendar WHERE Date LIKE '2025-03-%'"
            )
            
            count = cursor.fetchone()[0]
            conn.close()
            
            return count > 0
            
        except sqlite3.Error as e:
            logger.error(f"Error checking for March 2025 data: {e}")
            return False
    
    def create_march_2025_data(self) -> None:
        """
        Create mock data for March 2025.
        
        This method populates the coding calendar table with entries for each day in March 2025.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
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
                import random
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
            
            conn.commit()
            conn.close()
            
            logger.info(f"Created mock data for March 2025 with 31 coding tasks")
                
        except sqlite3.Error as e:
            logger.error(f"Error creating March 2025 data: {e}")
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
        Add a new coding task to the calendar.
        
        Args:
            task_data: Dictionary containing task data
            
        Returns:
            The serial number of the new task
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get the next serial number
            cursor.execute("SELECT MAX(\"SerialNo.\") FROM CodingCalendar")
            result = cursor.fetchone()
            next_serial = 1 if result[0] is None else result[0] + 1
            
            # Set created/updated timestamps
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Prepare the task data
            task_data["SerialNo."] = next_serial
            if "CreatedOn" not in task_data:
                task_data["CreatedOn"] = now
            if "UpdatedOn" not in task_data:
                task_data["UpdatedOn"] = now
            
            # Build the SQL query
            columns = ", ".join([f'"{k}"' for k in task_data.keys()])
            placeholders = ", ".join(["?" for _ in task_data.keys()])
            
            query = f"INSERT INTO CodingCalendar ({columns}) VALUES ({placeholders})"
            
            cursor.execute(query, list(task_data.values()))
            conn.commit()
            conn.close()
            
            logger.info(f"Added new coding task with SerialNo. {next_serial}")
            return next_serial
            
        except sqlite3.Error as e:
            logger.error(f"Error adding coding task: {e}")
            raise
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """
        Get all coding tasks from the calendar.
        
        Returns:
            List of dictionaries containing task data
        """
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM CodingCalendar ORDER BY \"Date\", \"SerialNo.\"")
            
            tasks = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            logger.info(f"Retrieved {len(tasks)} coding tasks")
            return tasks
            
        except sqlite3.Error as e:
            logger.error(f"Error getting coding tasks: {e}")
            raise
    
    def get_task_by_id(self, serial_no: int) -> Optional[Dict[str, Any]]:
        """
        Get a coding task by its serial number.
        
        Args:
            serial_no: The serial number of the task
            
        Returns:
            Dictionary containing task data, or None if not found
        """
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM CodingCalendar WHERE \"SerialNo.\" = ?", (serial_no,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                logger.info(f"Retrieved coding task with SerialNo. {serial_no}")
                return dict(row)
            else:
                logger.warning(f"Coding task with SerialNo. {serial_no} not found")
                return None
                
        except sqlite3.Error as e:
            logger.error(f"Error getting coding task: {e}")
            raise
    
    def get_tasks_by_date(self, date: datetime) -> List[Dict[str, Any]]:
        """
        Get coding tasks for a specific date.
        
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
                "SELECT * FROM CodingCalendar WHERE Date LIKE ? ORDER BY \"SerialNo.\"",
                (f"{date_str}%",)
            )
            
            tasks = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            logger.info(f"Retrieved {len(tasks)} coding tasks for date {date_str}")
            return tasks
                
        except sqlite3.Error as e:
            logger.error(f"Error getting coding tasks by date: {e}")
            raise
    
    def get_tasks_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """
        Get coding tasks within a date range.
        
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
                "SELECT * FROM CodingCalendar WHERE Date >= ? AND Date <= ? ORDER BY \"Date\", \"SerialNo.\"",
                (f"{start_str} 00:00:00", f"{end_str} 23:59:59")
            )
            
            tasks = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            logger.info(f"Retrieved {len(tasks)} coding tasks for date range {start_str} to {end_str}")
            return tasks
                
        except sqlite3.Error as e:
            logger.error(f"Error getting coding tasks by date range: {e}")
            raise
    
    def update_task(self, serial_no: int, task_data: Dict[str, Any]) -> bool:
        """
        Update an existing coding task.
        
        Args:
            serial_no: The serial number of the task to update
            task_data: Dictionary containing updated task data
            
        Returns:
            True if the task was updated, False otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Set updated timestamp
            task_data["UpdatedOn"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Build the SQL query
            set_clause = ", ".join([f'"{k}" = ?' for k in task_data.keys()])
            
            query = f"UPDATE CodingCalendar SET {set_clause} WHERE \"SerialNo.\" = ?"
            
            cursor.execute(query, list(task_data.values()) + [serial_no])
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Updated coding task with SerialNo. {serial_no}")
                result = True
            else:
                logger.warning(f"Coding task with SerialNo. {serial_no} not found for update")
                result = False
                
            conn.close()
            return result
                
        except sqlite3.Error as e:
            logger.error(f"Error updating coding task: {e}")
            raise
    
    def delete_task(self, serial_no: int) -> bool:
        """
        Delete a coding task from the calendar.
        
        Args:
            serial_no: The serial number of the task to delete
            
        Returns:
            True if the task was deleted, False otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM CodingCalendar WHERE \"SerialNo.\" = ?", (serial_no,))
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Deleted coding task with SerialNo. {serial_no}")
                result = True
            else:
                logger.warning(f"Coding task with SerialNo. {serial_no} not found for deletion")
                result = False
                
            conn.close()
            return result
                
        except sqlite3.Error as e:
            logger.error(f"Error deleting coding task: {e}")
            raise


async def setup(bot: commands.Bot):
    """Add the coding calendar commands cog to the bot."""
    await bot.add_cog(CodingCalendarCommands(bot))
