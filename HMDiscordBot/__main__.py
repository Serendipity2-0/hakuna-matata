"""
Main Discord bot module for Hakuna Matata.
This module implements a Discord bot that can interact with the Calendar database.
"""

import os
import sys
import asyncio
import logging
# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import discord
from discord.ext import commands
from dotenv import load_dotenv
from HMDiscordBot.utils.config import ConfigManager
from HMDiscordBot.utils.db_handler import CalendarDBHandler
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')

# Load environment variables
load_dotenv()

# Initialize Discord bot with all intents and proper reconnect settings
intents = discord.Intents.all()
# Get command prefix from config or use default
config = ConfigManager()
command_prefix = config.get('bot', 'command_prefix') or '!'  # Ensure default if None

bot = commands.Bot(
    command_prefix=command_prefix,
    intents=intents,
    reconnect=True,
    max_messages=10000,
    heartbeat_timeout=150.0,
    help_command=None  # Disable the default help command
)

def get_db_path(db_name='calendar'):
    """
    Get the full path to the database file.
    
    Args:
        db_name: Name of the database to get the path for
        
    Returns:
        Full path to the database file
    """
    base_dir = os.getcwd()
    db_base_path = config.get('database', 'base_path', 'DB/Main')
    db_file = config.get('database', 'files', db_name)
    full_path = os.path.join(base_dir, db_base_path, db_file)
    return full_path

async def load_cogs():
    """Load all cogs for the bot."""
    # List of cogs to load
    cogs = [
        'HMDiscordBot.cogs.calendar_commands',
        'HMDiscordBot.cogs.calendar_views',
        'HMDiscordBot.cogs.audio_transcript_commands'
    ]
    
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            logger.info(f"Loaded cog: {cog}")
        except Exception as e:
            logger.error(f"Error loading cog {cog}: {str(e)}", exc_info=True)

@bot.event
async def on_ready():
    """Event handler that runs when the Discord bot successfully connects."""
    logger.info(f'{bot.user} has connected to Discord!')
    try:
        # Load all cogs
        await load_cogs()
        
        # Set up slash commands
        await bot.tree.sync()
        logger.info("Slash commands synced")
        
        # Send a message to the specified channel if provided
        channel_id = os.getenv('DISCORD_CHANNEL_ID')
        if channel_id:
            channel = bot.get_channel(int(channel_id))
            if channel:
                await channel.send("Calendar Bot is now online! Use `/calendar_help` to see available commands.")
            else:
                logger.warning(f"Could not find channel with ID {channel_id}")
    except Exception as e:
        logger.error(f"Error in on_ready: {str(e)}", exc_info=True)

@bot.event
async def on_disconnect():
    """Event handler that runs when the bot disconnects from Discord."""
    logger.warning("Bot disconnected from Discord. Attempting to reconnect...")

@bot.event
async def on_error(event, *args, **kwargs):
    """Global error handler for all events."""
    logger.error(f"Error in {event}", exc_info=True)

@bot.event
async def on_message(message):
    """Process messages and commands."""
    if message.author == bot.user:
        return
    
    # Process commands first
    await bot.process_commands(message)

@bot.command(name='help')
async def help_command(ctx):
    """Display help information for available commands."""
    help_embed = discord.Embed(
        title="Calendar Bot Help",
        description="Here are the available commands:",
        color=discord.Color.blue()
    )
    
    help_embed.add_field(
        name="Calendar Commands",
        value=(
            f"{bot.command_prefix}calendar_help - Show calendar commands\n"
            f"{bot.command_prefix}add_event - Add a new event\n"
            f"{bot.command_prefix}view_events - View all events\n"
            f"{bot.command_prefix}view_today - View today's events\n"
            f"{bot.command_prefix}view_week - View this week's events\n"
            f"{bot.command_prefix}view_date [YYYY-MM-DD] - View events for a specific date\n"
            f"{bot.command_prefix}delete_event [id] - Delete an event\n"
            f"{bot.command_prefix}update_event [id] - Update an event"
        ),
        inline=False
    )
    
    help_embed.add_field(
        name="Slash Commands",
        value=(
            "/calendar_help - Show calendar commands\n"
            "/add_event - Add a new event\n"
            "/view_events - View all events\n"
            "/view_date - View events for a specific date\n"
            "/delete_event - Delete an event\n"
            "/update_event - Update an event\n"
            "/create_march_2025 - Create calendar entries for March 2025\n"
            "/transcribe_audio - Transcribe an audio file"
        ),
        inline=False
    )
    
    help_embed.add_field(
        name="Audio Transcription",
        value=(
            f"{bot.command_prefix}transcribe_audio - Transcribe an audio file\n"
            "/transcribe_audio - Transcribe an audio file with choice of transcription service"
        ),
        inline=False
    )
    
    help_embed.set_footer(text="Use the buttons and dropdowns in responses for easier interaction")
    
    await ctx.send(embed=help_embed)

def main():
    """Main function to run the bot with error handling and reconnection logic."""
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger.error("No Discord token found in environment variables")
        return

    while True:
        try:
            bot.run(token)
        except discord.errors.LoginFailure:
            logger.error("Invalid Discord token. Please check your .env file.")
            break
        except Exception as e:
            logger.error(f"Error running bot: {str(e)}", exc_info=True)
            logger.info("Attempting to reconnect in 5 seconds...")
            asyncio.sleep(5)
            continue

if __name__ == "__main__":
    main()
