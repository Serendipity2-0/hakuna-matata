"""
Calendar views for the Discord bot.
This module implements Discord UI components for interacting with the calendar database.
"""

import logging
import discord
from discord import app_commands
from discord.ext import commands
from typing import List, Dict, Any, Optional, Callable, Awaitable
from datetime import datetime, timedelta

from HMDiscordBot.utils.db_handler import CalendarDBHandler
from HMDiscordBot.models.calendar_event import CalendarEvent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('calendar_views')

class DateSelectView(discord.ui.View):
    """View for selecting a date option."""
    
    def __init__(self, callback: Callable[[str, Optional[str]], Awaitable[None]]):
        """
        Initialize the date select view.
        
        Args:
            callback: Callback function to call when a date option is selected
        """
        super().__init__(timeout=60)
        self.callback = callback
        
        # Add the date select dropdown
        self.add_item(DateSelectDropdown(self.on_select))
    
    async def on_select(self, interaction: discord.Interaction, option: str, custom_date: Optional[str] = None):
        """
        Handle date option selection.
        
        Args:
            interaction: The interaction that triggered this callback
            option: The selected date option
            custom_date: Custom date string (if applicable)
        """
        await self.callback(option, custom_date)
        self.stop()


class DateSelectDropdown(discord.ui.Select):
    """Dropdown for selecting a date option."""
    
    def __init__(self, callback: Callable[[discord.Interaction, str, Optional[str]], Awaitable[None]]):
        """
        Initialize the date select dropdown.
        
        Args:
            callback: Callback function to call when an option is selected
        """
        options = [
            discord.SelectOption(
                label="Today",
                description="View events for today",
                value="today"
            ),
            discord.SelectOption(
                label="This Week",
                description="View events for this week",
                value="week"
            ),
            discord.SelectOption(
                label="Custom Date",
                description="View events for a specific date",
                value="custom"
            )
        ]
        
        super().__init__(
            placeholder="Select a date option...",
            min_values=1,
            max_values=1,
            options=options
        )
        
        self.callback_func = callback
    
    async def callback(self, interaction: discord.Interaction):
        """Handle dropdown selection."""
        option = self.values[0]
        
        if option == "custom":
            # Create a modal for entering a custom date
            modal = CustomDateModal(self.callback_func)
            await interaction.response.send_modal(modal)
        else:
            await self.callback_func(interaction, option)


class CustomDateModal(discord.ui.Modal, title="Enter Custom Date"):
    """Modal for entering a custom date."""
    
    def __init__(self, callback: Callable[[discord.Interaction, str, str], Awaitable[None]]):
        """
        Initialize the custom date modal.
        
        Args:
            callback: Callback function to call when the modal is submitted
        """
        super().__init__()
        self.callback_func = callback
        
        self.date_input = discord.ui.TextInput(
            label="Date (YYYY-MM-DD)",
            placeholder="e.g., 2025-03-15",
            required=True
        )
        self.add_item(self.date_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            # Validate the date format
            datetime.strptime(self.date_input.value, "%Y-%m-%d")
            
            # Call the callback with the custom date
            await self.callback_func(interaction, "custom", self.date_input.value)
            
        except ValueError:
            await interaction.response.send_message(
                "Invalid date format. Please use YYYY-MM-DD.",
                ephemeral=True
            )


class PlatformSelectView(discord.ui.View):
    """View for selecting a platform."""
    
    def __init__(self, platforms: List[str], callback: Callable[[str], Awaitable[None]]):
        """
        Initialize the platform select view.
        
        Args:
            platforms: List of available platforms
            callback: Callback function to call when a platform is selected
        """
        super().__init__(timeout=60)
        self.callback = callback
        
        # Add the platform select dropdown
        self.add_item(PlatformSelectDropdown(platforms, self.on_select))
    
    async def on_select(self, interaction: discord.Interaction, platform: str):
        """
        Handle platform selection.
        
        Args:
            interaction: The interaction that triggered this callback
            platform: The selected platform
        """
        await self.callback(platform)
        self.stop()


class PlatformSelectDropdown(discord.ui.Select):
    """Dropdown for selecting a platform."""
    
    def __init__(self, platforms: List[str], callback: Callable[[discord.Interaction, str], Awaitable[None]]):
        """
        Initialize the platform select dropdown.
        
        Args:
            platforms: List of available platforms
            callback: Callback function to call when a platform is selected
        """
        options = [
            discord.SelectOption(
                label=platform,
                value=platform
            )
            for platform in platforms
        ]
        
        super().__init__(
            placeholder="Select a platform...",
            min_values=1,
            max_values=1,
            options=options
        )
        
        self.callback_func = callback
    
    async def callback(self, interaction: discord.Interaction):
        """Handle dropdown selection."""
        await self.callback_func(interaction, self.values[0])


class CreatorSelectView(discord.ui.View):
    """View for selecting a creator."""
    
    def __init__(self, creators: List[str], callback: Callable[[str], Awaitable[None]]):
        """
        Initialize the creator select view.
        
        Args:
            creators: List of available creators
            callback: Callback function to call when a creator is selected
        """
        super().__init__(timeout=60)
        self.callback = callback
        
        # Add the creator select dropdown
        self.add_item(CreatorSelectDropdown(creators, self.on_select))
    
    async def on_select(self, interaction: discord.Interaction, creator: str):
        """
        Handle creator selection.
        
        Args:
            interaction: The interaction that triggered this callback
            creator: The selected creator
        """
        await self.callback(creator)
        self.stop()


class CreatorSelectDropdown(discord.ui.Select):
    """Dropdown for selecting a creator."""
    
    def __init__(self, creators: List[str], callback: Callable[[discord.Interaction, str], Awaitable[None]]):
        """
        Initialize the creator select dropdown.
        
        Args:
            creators: List of available creators
            callback: Callback function to call when a creator is selected
        """
        options = [
            discord.SelectOption(
                label=creator,
                value=creator
            )
            for creator in creators
        ]
        
        super().__init__(
            placeholder="Select a creator...",
            min_values=1,
            max_values=1,
            options=options
        )
        
        self.callback_func = callback
    
    async def callback(self, interaction: discord.Interaction):
        """Handle dropdown selection."""
        await self.callback_func(interaction, self.values[0])


class EventSelectView(discord.ui.View):
    """View for selecting an event."""
    
    def __init__(self, events: List[Dict[str, Any]], callback: Callable[[int], Awaitable[None]]):
        """
        Initialize the event select view.
        
        Args:
            events: List of events to select from
            callback: Callback function to call when an event is selected
        """
        super().__init__(timeout=60)
        self.callback = callback
        
        # Add the event select dropdown
        self.add_item(EventSelectDropdown(events, self.on_select))
    
    async def on_select(self, interaction: discord.Interaction, event_id: int):
        """
        Handle event selection.
        
        Args:
            interaction: The interaction that triggered this callback
            event_id: The ID of the selected event
        """
        await self.callback(event_id)
        self.stop()


class EventSelectDropdown(discord.ui.Select):
    """Dropdown for selecting an event."""
    
    def __init__(self, events: List[Dict[str, Any]], callback: Callable[[discord.Interaction, int], Awaitable[None]]):
        """
        Initialize the event select dropdown.
        
        Args:
            events: List of events to select from
            callback: Callback function to call when an event is selected
        """
        # Create options for each event (limit to 25 due to Discord's limit)
        options = []
        for i, event in enumerate(events[:25]):
            date_str = event["Date"].split()[0] if event["Date"] else "N/A"
            platform = event["Platform "]
            content_type = event["ContentType "]
            
            label = f"#{event['SerialNo.']} - {date_str}"
            description = f"{content_type} ({platform})"
            
            options.append(
                discord.SelectOption(
                    label=label,
                    description=description,
                    value=str(event["SerialNo."])
                )
            )
        
        super().__init__(
            placeholder="Select an event...",
            min_values=1,
            max_values=1,
            options=options
        )
        
        self.callback_func = callback
    
    async def callback(self, interaction: discord.Interaction):
        """Handle dropdown selection."""
        event_id = int(self.values[0])
        await self.callback_func(interaction, event_id)


async def setup(bot: commands.Bot):
    """Add the calendar views to the bot."""
    # This is a module of UI components, not a cog, so no need to add it to the bot
    pass
