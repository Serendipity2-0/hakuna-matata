#!/usr/bin/env python3
"""
Discord Voice Channel Recording Script

This script provides a standalone way to run the Discord voice channel recording functionality.
It imports the necessary modules and functions from the main bot code.
"""

import os
import sys
import logging
import asyncio

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the transcription module
from backend.agents.tools.assemblyAudioTranscript import setup_environment, transcribe_audio, save_transcript

# Import necessary modules from the main bot code
from HMDiscordBot.__main__ import (
    bot, 
    VoiceRecorder, 
    connections, 
    recordings, 
    voice_channel_id, 
    text_channel_id, 
    RECORDINGS_DIR
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord_voice')

def main():
    """Main function to run the Discord voice recording bot."""
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger.error("No Discord token found in environment variables")
        return 1
    
    logger.info("Starting Discord voice recording bot")
    
    try:
        # Run the bot
        bot.run(token)
    except Exception as e:
        logger.error(f"Error running bot: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
