#!/usr/bin/env python3
"""
Script to run the Discord bot.
This script is a simple wrapper to run the Discord bot.
"""

import os
import sys
import logging
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('run_bot')

def main():
    """Main function to run the Discord bot."""
    try:
        # Check if the .env file exists
        if not os.path.exists('HMDiscordBot/.env'):
            logger.warning("No .env file found. Creating from example...")
            if os.path.exists('HMDiscordBot/.env.example'):
                with open('HMDiscordBot/.env.example', 'r') as example_file:
                    example_content = example_file.read()
                
                with open('HMDiscordBot/.env', 'w') as env_file:
                    env_file.write(example_content)
                
                logger.info("Created .env file from example. Please edit it with your Discord bot token.")
                logger.info("Exiting...")
                sys.exit(1)
            else:
                logger.error("No .env.example file found. Please create a .env file with your Discord bot token.")
                sys.exit(1)
        
        # Run the bot
        logger.info("Starting the Discord bot...")
        subprocess.run([sys.executable, "-m", "HMDiscordBot"])
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.error(f"Error running bot: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
