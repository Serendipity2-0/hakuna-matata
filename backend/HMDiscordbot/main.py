"""
Main Discord bot module for SoM (System of Management).
This module implements a Discord bot that can fetch and display transaction data from a SQLite database.
"""

import os
import sys
import discord
from dotenv import load_dotenv
from .utils.config import ConfigManager
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from Kaas.discord_handler import KaasDiscordHandler 

# Load environment variables
load_dotenv()

# Initialize Discord client with all intents enabled
client = discord.Client(intents=discord.Intents.all())
config = ConfigManager()

# Initialize Kaas handler
kaas_handler = None

def get_db_path():
    """Get the full path to the database file."""
    base_dir = os.getcwd()
    db_base_path = 'DB/main'
    db_file = config.get('database', 'files', 'kaas')
    full_path = os.path.join(base_dir, db_base_path, db_file)
    return full_path

def init_kaas_handler():
    """Initialize the Kaas handler with the correct database path."""
    global kaas_handler
    if kaas_handler is None:
        db_path = get_db_path()
        currency_symbol = config.get('formatting', 'currency', 'symbol')
        kaas_handler = KaasDiscordHandler(db_path, currency_symbol)

@client.event
async def on_ready():
    """Event handler that runs when the Discord bot successfully connects."""
    print(f'{client.user} has connected to Discord!')
    init_kaas_handler()
    
    channel_id = os.getenv('DISCORD_CHANNEL_ID')
    if channel_id:
        channel = client.get_channel(int(channel_id))
        if channel:
            await kaas_handler.check_due_transactions(channel)

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return
    await kaas_handler.handle_reaction(reaction, user)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$chat:'):
        await kaas_handler.handle_message(message)
    elif message.content.startswith('$check'):
        channel_id = os.getenv('DISCORD_CHANNEL_ID')
        if channel_id:
            channel = client.get_channel(int(channel_id))
            if channel:
                await kaas_handler.check_due_transactions(channel)

# Start the Discord bot
client.run(os.getenv('DISCORD_TOKEN'))