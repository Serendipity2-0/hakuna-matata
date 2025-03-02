"""
Calendar commands for the Discord bot.
This module implements Discord commands for interacting with the calendar database.
"""

import os
import logging
import discord
from discord import app_commands
from discord.ext import commands
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timedelta

from HMDiscordBot.utils.db_handler import CalendarDBHandler
from HMDiscordBot.models.calendar_event import CalendarEvent
from HMDiscordBot.utils.config import ConfigManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('calendar_commands')

class CalendarCommands(commands.Cog):
    """
    Discord commands for interacting with the calendar database.
    
    This cog provides commands for adding, viewing, updating, and deleting events.
    """
    
    def __init__(self, bot: commands.Bot):
        """
        Initialize the calendar commands.
        
        Args:
            bot: The Discord bot instance
        """
        self.bot = bot
        self.config = ConfigManager()
        
        # Get the database path
        base_dir = os.getcwd()
        db_path = os.path.join(base_dir, "DB", "Main", "Calendar.db")
        self.db_handler = CalendarDBHandler(db_path)
        
        # Define the available platforms
        self.platforms = [
            "Twitter", "Facebook", "Instagram", "LinkedIn", "YouTube",
            "VC Pitch Deck", "Blog", "Email", "Podcast", "GeneralScripts"
        ]
        
        # Define the available creators
        self.creators = ["Omkar", "Snowy"]
        
        logger.info("Calendar commands initialized")
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Event handler that runs when the cog is loaded."""
        logger.info("Calendar commands cog is ready")
    
    # ===== Prefix Commands =====
    
    @commands.command(name="calendar_help")
    async def calendar_help(self, ctx: commands.Context):
        """Display help information for calendar commands."""
        prefix = self.bot.command_prefix
        
        help_embed = discord.Embed(
            title="Calendar Bot Commands",
            description="Here are the available calendar commands:",
            color=discord.Color.blue()
        )
        
        help_embed.add_field(
            name="Prefix Commands",
            value=(
                f"`{prefix}calendar_help` - Show this help message\n"
                f"`{prefix}add_event` - Add a new event (interactive)\n"
                f"`{prefix}view_events` - View all events\n"
                f"`{prefix}view_today` - View today's events\n"
                f"`{prefix}view_week` - View this week's events\n"
                f"`{prefix}view_date [YYYY-MM-DD]` - View events for a specific date\n"
                f"`{prefix}delete_event [id]` - Delete an event\n"
                f"`{prefix}update_event [id]` - Update an event (interactive)"
            ),
            inline=False
        )
        
        help_embed.add_field(
            name="Slash Commands",
            value=(
                "`/calendar help` - Show this help message\n"
                "`/add_event` - Add a new event\n"
                "`/view_events` - View all events\n"
                "`/view_date` - View events for a specific date\n"
                "`/delete_event` - Delete an event\n"
                "`/update_event` - Update an event"
            ),
            inline=False
        )
        
        help_embed.set_footer(text="Use the buttons and dropdowns in responses for easier interaction")
        
        await ctx.send(embed=help_embed)
    
    @commands.command(name="add_event")
    async def add_event_prefix(self, ctx: commands.Context):
        """Add a new event to the calendar (interactive)."""
        # Create a modal for adding an event
        modal = AddEventModal(self.db_handler, self.platforms, self.creators)
        await ctx.send("Please use the `/add_event` slash command to add an event with a form.")
    
    @commands.command(name="view_events")
    async def view_events_prefix(self, ctx: commands.Context):
        """View all events in the calendar."""
        try:
            events = self.db_handler.get_all_events()
            
            if not events:
                await ctx.send("No events found in the calendar.")
                return
            
            # Create a paginator for the events
            paginator = EventPaginator(ctx, events, "All Events")
            await paginator.start()
            
        except Exception as e:
            logger.error(f"Error viewing events: {str(e)}", exc_info=True)
            await ctx.send(f"Error viewing events: {str(e)}")
    
    @commands.command(name="view_today")
    async def view_today_prefix(self, ctx: commands.Context):
        """View today's events."""
        try:
            today = datetime.now()
            events = self.db_handler.get_events_by_date(today)
            
            if not events:
                await ctx.send(f"No events found for today ({today.strftime('%Y-%m-%d')}).")
                return
            
            # Create a paginator for the events
            paginator = EventPaginator(ctx, events, f"Events for {today.strftime('%Y-%m-%d')}")
            await paginator.start()
            
        except Exception as e:
            logger.error(f"Error viewing today's events: {str(e)}", exc_info=True)
            await ctx.send(f"Error viewing today's events: {str(e)}")
    
    @commands.command(name="view_week")
    async def view_week_prefix(self, ctx: commands.Context):
        """View this week's events."""
        try:
            today = datetime.now()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            
            events = self.db_handler.get_events_by_date_range(start_of_week, end_of_week)
            
            if not events:
                await ctx.send(
                    f"No events found for this week "
                    f"({start_of_week.strftime('%Y-%m-%d')} to {end_of_week.strftime('%Y-%m-%d')})."
                )
                return
            
            # Create a paginator for the events
            paginator = EventPaginator(
                ctx, 
                events, 
                f"Events for {start_of_week.strftime('%Y-%m-%d')} to {end_of_week.strftime('%Y-%m-%d')}"
            )
            await paginator.start()
            
        except Exception as e:
            logger.error(f"Error viewing this week's events: {str(e)}", exc_info=True)
            await ctx.send(f"Error viewing this week's events: {str(e)}")
    
    @commands.command(name="view_date")
    async def view_date_prefix(self, ctx: commands.Context, date_str: str = None):
        """
        View events for a specific date.
        
        Args:
            date_str: Date string in YYYY-MM-DD format
        """
        if not date_str:
            await ctx.send("Please provide a date in YYYY-MM-DD format.")
            return
        
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            events = self.db_handler.get_events_by_date(date)
            
            if not events:
                await ctx.send(f"No events found for {date_str}.")
                return
            
            # Create a paginator for the events
            paginator = EventPaginator(ctx, events, f"Events for {date_str}")
            await paginator.start()
            
        except ValueError:
            await ctx.send("Invalid date format. Please use YYYY-MM-DD.")
        except Exception as e:
            logger.error(f"Error viewing events for date: {str(e)}", exc_info=True)
            await ctx.send(f"Error viewing events for date: {str(e)}")
    
    @commands.command(name="delete_event")
    async def delete_event_prefix(self, ctx: commands.Context, event_id: int = None):
        """
        Delete an event from the calendar.
        
        Args:
            event_id: The serial number of the event to delete
        """
        if not event_id:
            await ctx.send("Please provide an event ID to delete.")
            return
        
        try:
            # Get the event to confirm deletion
            event = self.db_handler.get_event_by_id(event_id)
            
            if not event:
                await ctx.send(f"Event with ID {event_id} not found.")
                return
            
            # Create a confirmation view
            view = ConfirmationView(ctx.author)
            
            # Create an embed for the event
            embed = discord.Embed(
                title=f"Confirm Deletion of Event #{event_id}",
                description="Are you sure you want to delete this event?",
                color=discord.Color.red()
            )
            
            embed.add_field(name="Date", value=event["Date"], inline=True)
            embed.add_field(name="Content Type", value=event["ContentType "], inline=True)
            embed.add_field(name="Platform", value=event["Platform "], inline=True)
            
            message = await ctx.send(embed=embed, view=view)
            
            # Wait for the user to confirm
            await view.wait()
            
            if view.value is True:
                # Delete the event
                success = self.db_handler.delete_event(event_id)
                
                if success:
                    embed.title = f"Event #{event_id} Deleted"
                    embed.description = "The event has been deleted successfully."
                    embed.color = discord.Color.green()
                else:
                    embed.title = f"Error Deleting Event #{event_id}"
                    embed.description = "An error occurred while deleting the event."
                    embed.color = discord.Color.red()
                
                await message.edit(embed=embed, view=None)
            else:
                embed.title = "Deletion Cancelled"
                embed.description = "The event deletion was cancelled."
                embed.color = discord.Color.blue()
                await message.edit(embed=embed, view=None)
            
        except Exception as e:
            logger.error(f"Error deleting event: {str(e)}", exc_info=True)
            await ctx.send(f"Error deleting event: {str(e)}")
    
    @commands.command(name="update_event")
    async def update_event_prefix(self, ctx: commands.Context, event_id: int = None):
        """
        Update an event in the calendar.
        
        Args:
            event_id: The serial number of the event to update
        """
        if not event_id:
            await ctx.send("Please provide an event ID to update.")
            return
        
        await ctx.send("Please use the `/update_event` slash command to update an event with a form.")
    
    # ===== Slash Commands =====
    
    @app_commands.command(name="calendar_help", description="Display help information for calendar commands")
    async def calendar_help_slash(self, interaction: discord.Interaction):
        """Display help information for calendar commands."""
        prefix = self.bot.command_prefix
        
        help_embed = discord.Embed(
            title="Calendar Bot Commands",
            description="Here are the available calendar commands:",
            color=discord.Color.blue()
        )
        
        help_embed.add_field(
            name="Prefix Commands",
            value=(
                f"`{prefix}calendar_help` - Show this help message\n"
                f"`{prefix}add_event` - Add a new event (interactive)\n"
                f"`{prefix}view_events` - View all events\n"
                f"`{prefix}view_today` - View today's events\n"
                f"`{prefix}view_week` - View this week's events\n"
                f"`{prefix}view_date [YYYY-MM-DD]` - View events for a specific date\n"
                f"`{prefix}delete_event [id]` - Delete an event\n"
                f"`{prefix}update_event [id]` - Update an event (interactive)"
            ),
            inline=False
        )
        
        help_embed.add_field(
            name="Slash Commands",
            value=(
                "`/calendar_help` - Show this help message\n"
                "`/add_event` - Add a new event\n"
                "`/view_events` - View all events\n"
                "`/view_date` - View events for a specific date\n"
                "`/delete_event` - Delete an event\n"
                "`/update_event` - Update an event"
            ),
            inline=False
        )
        
        help_embed.set_footer(text="Use the buttons and dropdowns in responses for easier interaction")
        
        await interaction.response.send_message(embed=help_embed, ephemeral=True)
    
    @app_commands.command(name="add_event", description="Add a new event to the calendar")
    async def add_event_slash(self, interaction: discord.Interaction):
        """Add a new event to the calendar."""
        # Create a modal for adding an event
        modal = AddEventModal(self.db_handler, self.platforms, self.creators)
        await interaction.response.send_modal(modal)
    
    @app_commands.command(name="view_events", description="View all events in the calendar")
    async def view_events_slash(self, interaction: discord.Interaction):
        """View all events in the calendar."""
        try:
            events = self.db_handler.get_all_events()
            
            if not events:
                await interaction.response.send_message("No events found in the calendar.")
                return
            
            # Create a paginator for the events
            paginator = EventPaginatorView(events, "All Events")
            
            # Send the first page
            await interaction.response.send_message(
                embed=paginator.get_page_embed(),
                view=paginator
            )
            
        except Exception as e:
            logger.error(f"Error viewing events: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error viewing events: {str(e)}")
    
    @app_commands.command(name="view_date", description="View events for a specific date")
    @app_commands.describe(
        date_option="Choose a date option",
        custom_date="Custom date in YYYY-MM-DD format (only needed for custom date option)"
    )
    @app_commands.choices(date_option=[
        app_commands.Choice(name="Today", value="today"),
        app_commands.Choice(name="This Week", value="week"),
        app_commands.Choice(name="Custom Date", value="custom")
    ])
    async def view_date_slash(
        self, 
        interaction: discord.Interaction, 
        date_option: str,
        custom_date: Optional[str] = None
    ):
        """
        View events for a specific date.
        
        Args:
            date_option: Date option (today, week, custom)
            custom_date: Custom date in YYYY-MM-DD format
        """
        try:
            events = []
            title = ""
            
            if date_option == "today":
                today = datetime.now()
                events = self.db_handler.get_events_by_date(today)
                title = f"Events for Today ({today.strftime('%Y-%m-%d')})"
                
            elif date_option == "week":
                today = datetime.now()
                start_of_week = today - timedelta(days=today.weekday())
                end_of_week = start_of_week + timedelta(days=6)
                
                events = self.db_handler.get_events_by_date_range(start_of_week, end_of_week)
                title = f"Events for This Week ({start_of_week.strftime('%Y-%m-%d')} to {end_of_week.strftime('%Y-%m-%d')})"
                
            elif date_option == "custom":
                if not custom_date:
                    await interaction.response.send_message(
                        "Please provide a custom date in YYYY-MM-DD format.",
                        ephemeral=True
                    )
                    return
                
                try:
                    date = datetime.strptime(custom_date, "%Y-%m-%d")
                    events = self.db_handler.get_events_by_date(date)
                    title = f"Events for {custom_date}"
                except ValueError:
                    await interaction.response.send_message(
                        "Invalid date format. Please use YYYY-MM-DD.",
                        ephemeral=True
                    )
                    return
            
            if not events:
                await interaction.response.send_message(f"No events found for the selected date option.")
                return
            
            # Create a paginator for the events
            paginator = EventPaginatorView(events, title)
            
            # Send the first page
            await interaction.response.send_message(
                embed=paginator.get_page_embed(),
                view=paginator
            )
            
        except Exception as e:
            logger.error(f"Error viewing events for date: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error viewing events for date: {str(e)}")
    
    @app_commands.command(name="delete_event", description="Delete an event from the calendar")
    @app_commands.describe(event_id="The ID of the event to delete")
    async def delete_event_slash(self, interaction: discord.Interaction, event_id: int):
        """
        Delete an event from the calendar.
        
        Args:
            event_id: The serial number of the event to delete
        """
        try:
            # Get the event to confirm deletion
            event = self.db_handler.get_event_by_id(event_id)
            
            if not event:
                await interaction.response.send_message(f"Event with ID {event_id} not found.", ephemeral=True)
                return
            
            # Create a confirmation view
            view = ConfirmationView(interaction.user)
            
            # Create an embed for the event
            embed = discord.Embed(
                title=f"Confirm Deletion of Event #{event_id}",
                description="Are you sure you want to delete this event?",
                color=discord.Color.red()
            )
            
            embed.add_field(name="Date", value=event["Date"], inline=True)
            embed.add_field(name="Content Type", value=event["ContentType "], inline=True)
            embed.add_field(name="Platform", value=event["Platform "], inline=True)
            
            await interaction.response.send_message(embed=embed, view=view)
            
            # Wait for the user to confirm
            await view.wait()
            
            if view.value is True:
                # Delete the event
                success = self.db_handler.delete_event(event_id)
                
                if success:
                    embed.title = f"Event #{event_id} Deleted"
                    embed.description = "The event has been deleted successfully."
                    embed.color = discord.Color.green()
                else:
                    embed.title = f"Error Deleting Event #{event_id}"
                    embed.description = "An error occurred while deleting the event."
                    embed.color = discord.Color.red()
                
                await interaction.edit_original_response(embed=embed, view=None)
            else:
                embed.title = "Deletion Cancelled"
                embed.description = "The event deletion was cancelled."
                embed.color = discord.Color.blue()
                await interaction.edit_original_response(embed=embed, view=None)
            
        except Exception as e:
            logger.error(f"Error deleting event: {str(e)}", exc_info=True)
            if interaction.response.is_done():
                await interaction.edit_original_response(content=f"Error deleting event: {str(e)}")
            else:
                await interaction.response.send_message(f"Error deleting event: {str(e)}")
    
    @app_commands.command(name="update_event", description="Update an event in the calendar")
    @app_commands.describe(event_id="The ID of the event to update")
    async def update_event_slash(self, interaction: discord.Interaction, event_id: int):
        """
        Update an event in the calendar.
        
        Args:
            event_id: The serial number of the event to update
        """
        try:
            # Get the event to update
            event = self.db_handler.get_event_by_id(event_id)
            
            if not event:
                await interaction.response.send_message(f"Event with ID {event_id} not found.", ephemeral=True)
                return
            
            # Create a modal for updating the event
            modal = UpdateEventModal(self.db_handler, event, self.platforms, self.creators)
            await interaction.response.send_modal(modal)
            
        except Exception as e:
            logger.error(f"Error updating event: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error updating event: {str(e)}")
    
    @app_commands.command(name="create_march_2025", description="Create calendar entries for March 2025")
    async def create_march_2025_slash(self, interaction: discord.Interaction):
        """Create calendar entries for March 2025."""
        try:
            await interaction.response.defer(ephemeral=True)
            
            # Create the calendar entries
            self.db_handler.create_march_2025_calendar()
            
            await interaction.followup.send("Calendar entries for March 2025 have been created successfully.")
            
        except Exception as e:
            logger.error(f"Error creating March 2025 calendar: {str(e)}", exc_info=True)
            await interaction.followup.send(f"Error creating March 2025 calendar: {str(e)}")


# ===== UI Components =====

class AddEventModal(discord.ui.Modal, title="Add Calendar Event"):
    """Modal for adding a new event to the calendar."""
    
    def __init__(self, db_handler: CalendarDBHandler, platforms: List[str], creators: List[str]):
        super().__init__()
        self.db_handler = db_handler
        self.platforms = platforms
        self.creators = creators
        
        # Create the form fields
        self.date_input = discord.ui.TextInput(
            label="Date (YYYY-MM-DD)",
            placeholder="e.g., 2025-03-15",
            required=True
        )
        self.add_item(self.date_input)
        
        self.content_type_input = discord.ui.TextInput(
            label="Content Type",
            placeholder="e.g., Industry Trends & News",
            required=True
        )
        self.add_item(self.content_type_input)
        
        self.format_input = discord.ui.TextInput(
            label="Format",
            placeholder="e.g., Post, Story, Reel",
            required=True
        )
        self.add_item(self.format_input)
        
        self.platform_input = discord.ui.TextInput(
            label="Platform",
            placeholder="e.g., Twitter, Facebook, Instagram",
            required=True
        )
        self.add_item(self.platform_input)
        
        self.time_input = discord.ui.TextInput(
            label="Schedule Time (HH:MM:SS)",
            placeholder="e.g., 18:00:00",
            required=True,
            default="18:00:00"
        )
        self.add_item(self.time_input)
    
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
            
            # Create the event data
            event_data = {
                "Date": f"{self.date_input.value} 00:00:00",
                "ContentType ": self.content_type_input.value,
                "Format ": self.format_input.value,
                "Platform ": self.platform_input.value,
                "ScheduleTime ": self.time_input.value,
                "Status": "Scheduled",
                "CreatedBy": interaction.user.name,
                "CreatedOn": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "UpdatedBy": interaction.user.name,
                "UpdatedOn": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Add the event to the database
            event_id = self.db_handler.add_event(event_data)
            
            # Create a success embed
            embed = discord.Embed(
                title="Event Added Successfully",
                description=f"Event #{event_id} has been added to the calendar.",
                color=discord.Color.green()
            )
            
            embed.add_field(name="Date", value=self.date_input.value, inline=True)
            embed.add_field(name="Content Type", value=self.content_type_input.value, inline=True)
            embed.add_field(name="Platform", value=self.platform_input.value, inline=True)
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            logger.error(f"Error adding event: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error adding event: {str(e)}")


class UpdateEventModal(discord.ui.Modal, title="Update Calendar Event"):
    """Modal for updating an existing event in the calendar."""
    
    def __init__(
        self, 
        db_handler: CalendarDBHandler, 
        event: Dict[str, Any],
        platforms: List[str], 
        creators: List[str]
    ):
        super().__init__()
        self.db_handler = db_handler
        self.event = event
        self.platforms = platforms
        self.creators = creators
        self.event_id = event["SerialNo."]
        
        # Extract the date part from the timestamp
        date_str = event["Date"].split()[0] if event["Date"] else ""
        
        # Create the form fields with current values
        self.date_input = discord.ui.TextInput(
            label="Date (YYYY-MM-DD)",
            placeholder="e.g., 2025-03-15",
            required=True,
            default=date_str
        )
        self.add_item(self.date_input)
        
        self.content_type_input = discord.ui.TextInput(
            label="Content Type",
            placeholder="e.g., Industry Trends & News",
            required=True,
            default=event["ContentType "]
        )
        self.add_item(self.content_type_input)
        
        self.format_input = discord.ui.TextInput(
            label="Format",
            placeholder="e.g., Post, Story, Reel",
            required=True,
            default=event["Format "]
        )
        self.add_item(self.format_input)
        
        self.platform_input = discord.ui.TextInput(
            label="Platform",
            placeholder="e.g., Twitter, Facebook, Instagram",
            required=True,
            default=event["Platform "]
        )
        self.add_item(self.platform_input)
        
        self.time_input = discord.ui.TextInput(
            label="Schedule Time (HH:MM:SS)",
            placeholder="e.g., 18:00:00",
            required=True,
            default=event["ScheduleTime "]
        )
        self.add_item(self.time_input)
    
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
            
            # Create the event data
            event_data = {
                "Date": f"{self.date_input.value} 00:00:00",
                "ContentType ": self.content_type_input.value,
                "Format ": self.format_input.value,
                "Platform ": self.platform_input.value,
                "ScheduleTime ": self.time_input.value,
                "Status": self.event["Status"],
                "UpdatedBy": interaction.user.name,
                "UpdatedOn": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Update the event in the database
            success = self.db_handler.update_event(self.event_id, event_data)
            
            if success:
                # Create a success embed
                embed = discord.Embed(
                    title="Event Updated Successfully",
                    description=f"Event #{self.event_id} has been updated.",
                    color=discord.Color.green()
                )
                
                embed.add_field(name="Date", value=self.date_input.value, inline=True)
                embed.add_field(name="Content Type", value=self.content_type_input.value, inline=True)
                embed.add_field(name="Platform", value=self.platform_input.value, inline=True)
                
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(
                    f"Error updating event #{self.event_id}. The event may have been deleted.",
                    ephemeral=True
                )
            
        except Exception as e:
            logger.error(f"Error updating event: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error updating event: {str(e)}")


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


class EventPaginator:
    """Paginator for displaying events in a paginated manner (for prefix commands)."""
    
    def __init__(self, ctx: commands.Context, events: List[Dict[str, Any]], title: str):
        """
        Initialize the paginator.
        
        Args:
            ctx: The command context
            events: List of events to paginate
            title: Title for the paginator
        """
        self.ctx = ctx
        self.events = events
        self.title = title
        self.page = 0
        self.total_pages = len(events)
        
    async def start(self):
        """Start the paginator."""
        if not self.events:
            await self.ctx.send("No events to display.")
            return
        
        # Create the message with the first page
        self.message = await self.ctx.send(embed=self.get_page_embed(), view=self.get_page_view())
    
    def get_page_embed(self) -> discord.Embed:
        """Get the embed for the current page."""
        event = self.events[self.page]
        
        embed = discord.Embed(
            title=f"{self.title} (Page {self.page + 1}/{self.total_pages})",
            color=discord.Color.blue()
        )
        
        # Add event details to the embed
        embed.add_field(name="Event ID", value=event["SerialNo."], inline=True)
        embed.add_field(name="Date", value=event["Date"].split()[0] if event["Date"] else "N/A", inline=True)
        embed.add_field(name="Time", value=event["ScheduleTime "], inline=True)
        
        embed.add_field(name="Content Type", value=event["ContentType "], inline=True)
        embed.add_field(name="Format", value=event["Format "], inline=True)
        embed.add_field(name="Platform", value=event["Platform "], inline=True)
        
        if "Status" in event and event["Status"]:
            embed.add_field(name="Status", value=event["Status"], inline=True)
        
        if "CreatedBy" in event and event["CreatedBy"]:
            embed.add_field(name="Created By", value=event["CreatedBy"], inline=True)
            
        if "CreatedOn" in event and event["CreatedOn"]:
            embed.add_field(name="Created On", value=event["CreatedOn"], inline=True)
            
        if "UpdatedBy" in event and event["UpdatedBy"]:
            embed.add_field(name="Updated By", value=event["UpdatedBy"], inline=True)
            
        if "UpdatedOn" in event and event["UpdatedOn"]:
            embed.add_field(name="Updated On", value=event["UpdatedOn"], inline=True)
        
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


class EventPaginatorView(discord.ui.View):
    """Paginator view for displaying events in a paginated manner (for slash commands)."""
    
    def __init__(self, events: List[Dict[str, Any]], title: str):
        """
        Initialize the paginator view.
        
        Args:
            events: List of events to paginate
            title: Title for the paginator
        """
        super().__init__(timeout=60)
        self.events = events
        self.title = title
        self.page = 0
        self.total_pages = len(events)
    
    def get_page_embed(self) -> discord.Embed:
        """Get the embed for the current page."""
        event = self.events[self.page]
        
        embed = discord.Embed(
            title=f"{self.title} (Page {self.page + 1}/{self.total_pages})",
            color=discord.Color.blue()
        )
        
        # Add event details to the embed
        embed.add_field(name="Event ID", value=event["SerialNo."], inline=True)
        embed.add_field(name="Date", value=event["Date"].split()[0] if event["Date"] else "N/A", inline=True)
        embed.add_field(name="Time", value=event["ScheduleTime "], inline=True)
        
        embed.add_field(name="Content Type", value=event["ContentType "], inline=True)
        embed.add_field(name="Format", value=event["Format "], inline=True)
        embed.add_field(name="Platform", value=event["Platform "], inline=True)
        
        if "Status" in event and event["Status"]:
            embed.add_field(name="Status", value=event["Status"], inline=True)
        
        if "CreatedBy" in event and event["CreatedBy"]:
            embed.add_field(name="Created By", value=event["CreatedBy"], inline=True)
            
        if "CreatedOn" in event and event["CreatedOn"]:
            embed.add_field(name="Created On", value=event["CreatedOn"], inline=True)
            
        if "UpdatedBy" in event and event["UpdatedBy"]:
            embed.add_field(name="Updated By", value=event["UpdatedBy"], inline=True)
            
        if "UpdatedOn" in event and event["UpdatedOn"]:
            embed.add_field(name="Updated On", value=event["UpdatedOn"], inline=True)
        
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


async def setup(bot: commands.Bot):
    """Add the calendar commands cog to the bot."""
    await bot.add_cog(CalendarCommands(bot))
