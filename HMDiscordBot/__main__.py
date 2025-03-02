"""
Main Discord bot module for SoM (System of Management).
This module implements a Discord bot that can fetch and display transaction data from a SQLite database.
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
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from Kaas.discord_handler import KaasDiscordHandler

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

def get_db_path():
    """Get the full path to the database file."""
    base_dir = os.getcwd()
    db_base_path = 'DB/main'
    db_file = config.get('database', 'files', 'kaas')
    full_path = os.path.join(base_dir, db_base_path, db_file)
    return full_path

async def init_kaas_handler():
    """Initialize the Kaas handler with the correct database path."""
    db_path = get_db_path()
    currency_symbol = config.get('formatting', 'currency', 'symbol')
    # Add the cog to the bot
    await bot.add_cog(KaasDiscordHandler(bot, db_path, currency_symbol))

@bot.event
async def on_ready():
    """Event handler that runs when the Discord bot successfully connects."""
    logger.info(f'{bot.user} has connected to Discord!')
    try:
        await init_kaas_handler()
        
        channel_id = os.getenv('DISCORD_CHANNEL_ID')
        if channel_id:
            channel = bot.get_channel(int(channel_id))
            if channel:
                # Get the KaasDiscordHandler cog
                kaas_cog = bot.get_cog('KaasDiscordHandler')
                if kaas_cog:
                    await kaas_cog.check_due_transactions(channel)
                else:
                    logger.warning("KaasDiscordHandler cog not found")
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
    help_text = (
        "**Available Commands:**\n"
        f"{bot.command_prefix}chat [message] - Chat with the AI agent\n"
        f"{bot.command_prefix}query [sql] - Execute a SQL query\n"
        f"{bot.command_prefix}todayM - Show today's transactions\n"
        f"{bot.command_prefix}weekM - Show this week's transactions\n"
        f"{bot.command_prefix}check_due - Check for due transactions\n"
        f"{bot.command_prefix}help - Show this help message"
    )
    await ctx.send(help_text)

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
