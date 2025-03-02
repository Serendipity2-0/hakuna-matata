"""
Main Discord bot module for Hakuna Matata.
This module implements a Discord bot that can interact with the Calendar database.
"""

import os
import sys
import asyncio
import logging
import wave
import pyaudio
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
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
logger_voice = logging.getLogger('discord_voice')

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

# Dictionary to track active voice connections and recordings
connections = {}
recordings = {}

# Get channel IDs from environment variables or use defaults
voice_channel_id = int(os.getenv('DISCORD_VOICE_CHANNEL_ID', '1344939398197805133'))
text_channel_id = int(os.getenv('DISCORD_TEXT_CHANNEL_ID', '1344939398197805133'))

# Create recordings directory if it doesn't exist
RECORDINGS_DIR = Path("recordings")
RECORDINGS_DIR.mkdir(exist_ok=True)

# Audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1  # Mono recording is more widely supported
RATE = 44100  # Standard sample rate that works on most systems

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

class VoiceRecorder:
    """
    Class to handle recording audio from a Discord voice channel.
    Uses PyAudio to capture and save the audio stream.
    """
    
    def __init__(self, voice_client, filename):
        """
        Initialize the recorder with a voice client and filename.
        
        Args:
            voice_client: Discord voice client connected to a channel
            filename: Base name for the recording file
        """
        self.voice_client = voice_client
        self.recording = False
        self.audio = pyaudio.PyAudio()
        
        # Create a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f"{filename}_{timestamp}.wav"
        self.filepath = RECORDINGS_DIR / self.filename
        
        # Find the best input device
        self.device_index = self._find_input_device()
        logger_voice.info(f"Using audio input device index: {self.device_index}")
        
        # List to track participants
        self.participants = set()
        
        # Set up the wave file
        self.wave_file = wave.open(str(self.filepath), 'wb')
        self.wave_file.setnchannels(CHANNELS)
        self.wave_file.setsampwidth(self.audio.get_sample_size(FORMAT))
        self.wave_file.setframerate(RATE)
        
        logger_voice.info(f"Initialized recorder for {filename}, saving to {self.filepath}")
        
        # Set up the audio stream with error handling
        try:
            self.stream = self.audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=self.device_index,
                frames_per_buffer=CHUNK
            )
            logger_voice.info(f"Successfully opened audio stream")
        except Exception as e:
            logger_voice.error(f"Error opening audio stream: {str(e)}")
            # Try with default device as fallback
            logger_voice.info("Trying with default device settings")
            self.stream = self.audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )
    
    def _find_input_device(self):
        """Find the best input device for recording."""
        # Default to None (system default)
        device_index = None
        
        # Log available devices for debugging
        info = self.audio.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        
        logger_voice.info(f"Available audio devices:")
        for i in range(num_devices):
            device_info = self.audio.get_device_info_by_index(i)
            logger_voice.info(f"  Device {i}: {device_info.get('name')}")
            logger_voice.info(f"    Max Input Channels: {device_info.get('maxInputChannels')}")
            
            # Look for a device with input channels
            if device_info.get('maxInputChannels') > 0:
                # Prefer devices with "mic" or "input" in the name
                device_name = device_info.get('name', '').lower()
                if 'mic' in device_name or 'input' in device_name:
                    device_index = i
                    logger_voice.info(f"  Selected device {i} as preferred input")
                    break
                # Otherwise, just use the first input device we find
                elif device_index is None:
                    device_index = i
                    logger_voice.info(f"  Selected device {i} as fallback input")
        
        return device_index
    
    def start(self):
        """Start recording audio."""
        self.recording = True
        threading.Thread(target=self._record).start()
        logger_voice.info(f"Started recording to {self.filename}")
    
    def _record(self):
        """Record audio in a separate thread."""
        try:
            while self.recording and self.voice_client.is_connected():
                # Read audio data from the stream
                data = self.stream.read(CHUNK, exception_on_overflow=False)
                self.wave_file.writeframes(data)
                
                # Add any speaking users to participants list
                for user_id, user in self.voice_client.channel.voice_states.items():
                    if user.self_mute is False:  # User is not muted
                        self.participants.add(user_id)
                
                # Small sleep to prevent high CPU usage
                time.sleep(0.01)
        except Exception as e:
            logger_voice.error(f"Error during recording: {str(e)}")
        finally:
            logger_voice.info("Recording thread stopped")
    
    def stop(self):
        """Stop recording and clean up resources."""
        if not self.recording:
            return
            
        self.recording = False
        
        # Close and clean up resources
        self.stream.stop_stream()
        self.stream.close()
        self.wave_file.close()
        self.audio.terminate()
        
        logger_voice.info(f"Stopped recording to {self.filename}")
        return self.filepath, self.participants

async def load_cogs():
    """Load all cogs for the bot."""
    # List of cogs to load
    cogs = [
        'HMDiscordBot.cogs.calendar_commands',
        'HMDiscordBot.cogs.calendar_views',
        'HMDiscordBot.cogs.audio_transcript_commands',
        'HMDiscordBot.cogs.coding_calendar_commands',
        'HMDiscordBot.cogs.serendipity_calendar_commands',
        'HMDiscordBot.cogs.dms_commands'  # Add the DMS commands cog
        # 'HMDiscordBot.cogs.discordVc' is not loaded as its functionality is already in __main__.py
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
                await channel.send("Calendar Bot is now online! Use `/calendar_help` or `/coding_help` to see available commands.")
            else:
                logger.warning(f"Could not find channel with ID {channel_id}")
                
        # Send a message to the coding calendar channel if provided
        coding_channel_id = os.getenv('DISCORD_CODING_CALENDAR_CHANNEL_ID')
        if coding_channel_id and coding_channel_id != channel_id:
            coding_channel = bot.get_channel(int(coding_channel_id))
            if coding_channel:
                await coding_channel.send("Coding Calendar Bot is now online! Use `/coding_help` to see available commands.")
            else:
                logger.warning(f"Could not find coding calendar channel with ID {coding_channel_id}")
                
        # Send a message to the serendipity calendar channel if provided
        serendipity_channel_id = os.getenv('DISCORD_SERENDIPITY_CALENDAR_CHANNEL_ID')
        if serendipity_channel_id and serendipity_channel_id != channel_id and serendipity_channel_id != coding_channel_id:
            serendipity_channel = bot.get_channel(int(serendipity_channel_id))
            if serendipity_channel:
                await serendipity_channel.send("Serendipity Calendar Bot is now online! Use `/serendipity_help` to see available commands.")
            else:
                logger.warning(f"Could not find serendipity calendar channel with ID {serendipity_channel_id}")
                
        # Send a message to the DMS channel if provided
        dms_channel_id = os.getenv('DISCORD_DMS_CHANNEL_ID')
        if dms_channel_id and dms_channel_id != channel_id and dms_channel_id != coding_channel_id and dms_channel_id != serendipity_channel_id:
            dms_channel = bot.get_channel(int(dms_channel_id))
            if dms_channel:
                await dms_channel.send("Document Management System Bot is now online! Use `/dms_help` to see available commands.")
            else:
                logger.warning(f"Could not find DMS channel with ID {dms_channel_id}")
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

@bot.command()
async def join_and_record(ctx, *, meeting_name="meeting"):
    """
    Join a voice channel and start recording.
    
    Args:
        ctx: The command context
        meeting_name: Optional name for the recording file
    """
    # Check if the user is in a voice channel
    if not ctx.author.voice:
        await ctx.send("❌ You need to be in a voice channel first!")
        return
    
    # Get the user's voice channel
    voice_channel = ctx.author.voice.channel
    logger_voice.info(f"Joining voice channel: {voice_channel.name} (ID: {voice_channel.id})")
    
    try:
        # Connect to the voice channel
        vc = await voice_channel.connect()
        connections[ctx.guild.id] = vc
        
        # Create and start the recorder
        recorder = VoiceRecorder(vc, meeting_name)
        recorder.start()
        recordings[ctx.guild.id] = recorder
        
        # Send confirmation message
        await ctx.send(
            f"🎙️ Joined {voice_channel.name} and started recording!\n"
            f"Use `!stop_recording` when you're done."
        )
        logger_voice.info(f"Started recording in {voice_channel.name}")
        
    except Exception as e:
        logger_voice.error(f"Error joining voice channel: {str(e)}")
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
async def record_channel(ctx, channel_id=None):
    """
    Join a specific voice channel by ID and start recording.
    
    Args:
        ctx: The command context
        channel_id: ID of the voice channel to join (optional)
    """
    # Use provided channel ID or default from config
    target_channel_id = int(channel_id) if channel_id else voice_channel_id
    logger_voice.info(f"Attempting to join voice channel with ID: {target_channel_id}")
    
    try:
        # Get the voice channel
        voice_channel = bot.get_channel(target_channel_id)
        if voice_channel is None:
            voice_channel = await bot.fetch_channel(target_channel_id)
            
        if not isinstance(voice_channel, discord.VoiceChannel):
            await ctx.send(f"❌ Channel with ID {target_channel_id} is not a voice channel!")
            return
            
        # Connect to the voice channel
        vc = await voice_channel.connect()
        connections[ctx.guild.id] = vc
        
        # Create and start the recorder
        recorder = VoiceRecorder(vc, f"channel_{voice_channel.name}")
        recorder.start()
        recordings[ctx.guild.id] = recorder
        
        # Send confirmation message
        await ctx.send(
            f"🎙️ Joined {voice_channel.name} and started recording!\n"
            f"Use `!stop_recording` when you're done."
        )
        logger_voice.info(f"Started recording in channel {voice_channel.name}")
        
    except discord.errors.ClientException as e:
        logger_voice.error(f"Discord client error: {str(e)}")
        await ctx.send(f"❌ Error: {str(e)}")
    except Exception as e:
        logger_voice.error(f"Error recording channel: {str(e)}")
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
async def stop_recording(ctx):
    """Stop the current recording and disconnect from the voice channel."""
    if ctx.guild.id in recordings and ctx.guild.id in connections:
        # Get the recorder and voice client
        recorder = recordings[ctx.guild.id]
        vc = connections[ctx.guild.id]
        
        # Stop recording
        logger_voice.info("Stopping recording")
        filepath, participants = recorder.stop()
        
        # Format participant mentions
        participant_mentions = [f"<@{user_id}>" for user_id in participants]
        
        # Send notification to the text channel
        try:
            text_channel = bot.get_channel(text_channel_id)
            if text_channel is None:
                text_channel = await bot.fetch_channel(text_channel_id)
                
            await text_channel.send(
                f"⏹️ Recording stopped.\n"
                f"📼 Meeting recording saved to `{filepath.name}`\n"
                f"Participants: {', '.join(participant_mentions) if participant_mentions else 'None detected'}"
            )
        except Exception as e:
            logger_voice.error(f"Error sending stop message: {str(e)}")
            await ctx.send(
                f"⏹️ Recording stopped.\n"
                f"📼 Meeting recording saved to `{filepath.name}`"
            )
        
        # Disconnect from the voice channel
        await vc.disconnect()
        
        # Clean up
        del recordings[ctx.guild.id]
        del connections[ctx.guild.id]
    else:
        await ctx.send("❌ I am currently not recording in this server.")
        logger_voice.warning("Stop recording command received but no active recording found")

@bot.command()
async def list_recordings(ctx):
    """List all available recordings."""
    if not RECORDINGS_DIR.exists():
        await ctx.send("❌ No recordings directory found.")
        return
        
    recording_files = list(RECORDINGS_DIR.glob("*.wav"))
    
    if not recording_files:
        await ctx.send("📂 No recordings found.")
        return
        
    # Format the list of recordings
    recordings_list = "\n".join([f"- {rec.name}" for rec in recording_files])
    await ctx.send(f"📂 Available recordings:\n{recordings_list}")

@bot.command()
async def transcribe(ctx, *, recording_name=None):
    """
    Transcribe a recorded audio file using AssemblyAI.
    
    Args:
        ctx: The command context
        recording_name: Optional name of the recording to transcribe. 
                       If not provided, the most recent recording will be used.
    """
    # Check if recordings directory exists
    if not RECORDINGS_DIR.exists():
        await ctx.send("❌ No recordings directory found.")
        return
    
    # Get all WAV files in the recordings directory
    recording_files = list(RECORDINGS_DIR.glob("*.wav"))
    
    if not recording_files:
        await ctx.send("❌ No recordings found to transcribe.")
        return
    
    # Determine which file to transcribe
    if recording_name:
        # Find the file that matches the provided name
        matching_files = [f for f in recording_files if recording_name in f.name]
        if not matching_files:
            await ctx.send(f"❌ No recording found matching '{recording_name}'.")
            return
        file_to_transcribe = matching_files[0]
    else:
        # Use the most recent recording (based on file modification time)
        file_to_transcribe = max(recording_files, key=lambda f: f.stat().st_mtime)
    
    # Send a message indicating transcription has started
    processing_msg = await ctx.send(f"🔄 Starting transcription of `{file_to_transcribe.name}`...\nThis may take a few minutes depending on the length of the recording.")
    
    try:
        # Import the transcription module
        from backend.agents.tools.assemblyAudioTranscript import setup_environment, transcribe_audio, save_transcript
        
        # Initialize the transcription environment
        setup_environment()
        
        # Start the transcription process
        logger_voice.info(f"Starting transcription of {file_to_transcribe}")
        await processing_msg.edit(content=f"🔄 Transcribing `{file_to_transcribe.name}`...\nUploading to AssemblyAI...")
        
        # Run the transcription in a separate thread to avoid blocking the bot
        def run_transcription():
            try:
                # Transcribe the audio file
                transcript = transcribe_audio(str(file_to_transcribe))
                
                # Save the transcript to a file
                save_transcript(transcript, str(file_to_transcribe))
                
                return transcript, None
            except Exception as e:
                logger_voice.error(f"Transcription error: {str(e)}")
                return None, str(e)
        
        # Run the transcription in a thread pool to avoid blocking the bot
        transcript, error = await bot.loop.run_in_executor(None, run_transcription)
        
        if error:
            await processing_msg.edit(content=f"❌ Error during transcription: {error}")
            return
        
        # Get the path to the saved transcript file
        transcript_file_name = os.path.splitext(file_to_transcribe.name)[0]
        transcript_path = Path(f"DB/AudioTranscripts/{transcript_file_name}_transcript.md")
        
        if transcript_path.exists():
            # Read the first 1500 characters of the transcript to preview
            with open(transcript_path, 'r', encoding='utf-8') as f:
                content = f.read()
                preview = content[:1500] + "..." if len(content) > 1500 else content
            
            # Send the transcript preview
            await processing_msg.edit(content=f"✅ Transcription complete!\n\n**Preview:**\n```\n{preview}\n```\n\nFull transcript saved to `{transcript_path}`")
            
            # If the transcript is too long, also send it as a file
            if len(content) > 1500:
                await ctx.send(f"📄 Full transcript attached:", file=discord.File(transcript_path))
        else:
            await processing_msg.edit(content=f"✅ Transcription complete, but couldn't find the saved file at `{transcript_path}`.")
    
    except Exception as e:
        logger_voice.error(f"Error in transcribe command: {str(e)}")
        await processing_msg.edit(content=f"❌ Error: {str(e)}")

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
        name="Coding Calendar Commands",
        value=(
            f"{bot.command_prefix}coding_help - Show coding calendar commands\n"
            f"{bot.command_prefix}add_coding_task - Add a new coding task\n"
            f"{bot.command_prefix}view_coding_tasks - View all coding tasks\n"
            f"{bot.command_prefix}view_coding_today - View today's coding tasks\n"
            f"{bot.command_prefix}view_coding_week - View this week's coding tasks\n"
            f"{bot.command_prefix}view_coding_date [YYYY-MM-DD] - View coding tasks for a specific date\n"
            f"{bot.command_prefix}delete_coding_task [id] - Delete a coding task\n"
            f"{bot.command_prefix}update_coding_task [id] - Update a coding task\n"
            "/coding_help - Show coding calendar commands\n"
            "/add_coding_task - Add a new coding task\n"
            "/view_coding_tasks - View all coding tasks\n"
            "/view_coding_date - View coding tasks for a specific date\n"
            "/delete_coding_task - Delete a coding task\n"
            "/update_coding_task - Update a coding task"
        ),
        inline=False
    )
    
    help_embed.add_field(
        name="Serendipity Calendar Commands",
        value=(
            f"{bot.command_prefix}serendipity_help - Show serendipity calendar commands\n"
            f"{bot.command_prefix}add_serendipity_task - Add a new task\n"
            f"{bot.command_prefix}view_serendipity_tasks - View all tasks\n"
            f"{bot.command_prefix}view_serendipity_today - View today's tasks\n"
            f"{bot.command_prefix}view_serendipity_week - View this week's tasks\n"
            f"{bot.command_prefix}view_serendipity_date [YYYY-MM-DD] - View tasks for a specific date\n"
            f"{bot.command_prefix}delete_serendipity_task [id] - Delete a task\n"
            f"{bot.command_prefix}update_serendipity_task [id] - Update a task\n"
            "/serendipity_help - Show serendipity calendar commands\n"
            "/add_serendipity_task - Add a new task\n"
            "/view_serendipity_tasks - View all tasks\n"
            "/view_serendipity_date - View tasks for a specific date\n"
            "/delete_serendipity_task - Delete a task\n"
            "/update_serendipity_task - Update a task"
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
    
    help_embed.add_field(
        name="Document Management System (DMS) Commands",
        value=(
            f"{bot.command_prefix}dms_help - Show DMS commands\n"
            f"{bot.command_prefix}upload_document - Upload a new document\n"
            f"{bot.command_prefix}view_documents - View all documents\n"
            f"{bot.command_prefix}search_document [query] - Search for documents\n"
            f"{bot.command_prefix}update_document [id] - Update a document\n"
            f"{bot.command_prefix}download_document [id] - Download a document\n"
            "/dms_help - Show DMS commands\n"
            "/upload_document - Upload a new document\n"
            "/view_documents - View all documents\n"
            "/search_document - Search for documents\n"
            "/update_document - Update a document\n"
            "/download_document - Download a document"
        ),
        inline=False
    )
    
    help_embed.set_footer(text="Use the buttons and dropdowns in responses for easier interaction")
    
    await ctx.send(embed=help_embed)

def run_voice_bot():
    """Run the Discord voice recording bot with the token from environment variables."""
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger_voice.error("No Discord token found in environment variables")
        return
        
    logger_voice.info("Starting Discord voice recording bot")
    bot.run(token)

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
