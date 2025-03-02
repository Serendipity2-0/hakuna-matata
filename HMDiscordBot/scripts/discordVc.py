"""
Discord Voice Channel Recording Module

This module provides functionality for a Discord bot to join voice channels
and record meetings to local files using PyAudio for audio capture.
"""

import discord
from discord.ext import commands
import os
import logging
import asyncio
import wave
import pyaudio
import threading
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord_voice')

# Load environment variables
load_dotenv()

# Set up intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to track active voice connections and recordings
connections = {}
recordings = {}

# Get channel IDs from environment variables or use defaults
voice_channel_id = int(os.getenv('DISCORD_CHANNEL_ID', '1342935986824413267'))
text_channel_id = int(os.getenv('DISCORD_TEXT_CHANNEL_ID', '1342935986824413267'))

# Create recordings directory if it doesn't exist
RECORDINGS_DIR = Path("recordings")
RECORDINGS_DIR.mkdir(exist_ok=True)

# Audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1  # Mono recording is more widely supported
RATE = 44100  # Standard sample rate that works on most systems

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
        logger.info(f"Using audio input device index: {self.device_index}")
        
        # List to track participants
        self.participants = set()
        
        # Set up the wave file
        self.wave_file = wave.open(str(self.filepath), 'wb')
        self.wave_file.setnchannels(CHANNELS)
        self.wave_file.setsampwidth(self.audio.get_sample_size(FORMAT))
        self.wave_file.setframerate(RATE)
        
        logger.info(f"Initialized recorder for {filename}, saving to {self.filepath}")
        
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
            logger.info(f"Successfully opened audio stream")
        except Exception as e:
            logger.error(f"Error opening audio stream: {str(e)}")
            # Try with default device as fallback
            logger.info("Trying with default device settings")
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
        
        logger.info(f"Available audio devices:")
        for i in range(num_devices):
            device_info = self.audio.get_device_info_by_index(i)
            logger.info(f"  Device {i}: {device_info.get('name')}")
            logger.info(f"    Max Input Channels: {device_info.get('maxInputChannels')}")
            
            # Look for a device with input channels
            if device_info.get('maxInputChannels') > 0:
                # Prefer devices with "mic" or "input" in the name
                device_name = device_info.get('name', '').lower()
                if 'mic' in device_name or 'input' in device_name:
                    device_index = i
                    logger.info(f"  Selected device {i} as preferred input")
                    break
                # Otherwise, just use the first input device we find
                elif device_index is None:
                    device_index = i
                    logger.info(f"  Selected device {i} as fallback input")
        
        return device_index
    
    def start(self):
        """Start recording audio."""
        self.recording = True
        threading.Thread(target=self._record).start()
        logger.info(f"Started recording to {self.filename}")
    
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
            logger.error(f"Error during recording: {str(e)}")
        finally:
            logger.info("Recording thread stopped")
    
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
        
        logger.info(f"Stopped recording to {self.filename}")
        return self.filepath, self.participants

@bot.event
async def on_ready():
    """Event handler that runs when the Discord bot successfully connects."""
    logger.info(f'{bot.user} has connected to Discord!')
    logger.info(f'Bot is active in {len(bot.guilds)} guilds')

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
    logger.info(f"Joining voice channel: {voice_channel.name} (ID: {voice_channel.id})")
    
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
        logger.info(f"Started recording in {voice_channel.name}")
        
    except Exception as e:
        logger.error(f"Error joining voice channel: {str(e)}")
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
    # target_channel_id = int(1342935986824413267) if channel_id else voice_channel_id
    target_channel_id = 1342935986824413267
    logger.info(f"Attempting to join voice channel with ID: {target_channel_id}")
    
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
        logger.info(f"Started recording in channel {voice_channel.name}")
        
    except discord.errors.ClientException as e:
        logger.error(f"Discord client error: {str(e)}")
        await ctx.send(f"❌ Error: {str(e)}")
    except Exception as e:
        logger.error(f"Error recording channel: {str(e)}")
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
async def stop_recording(ctx):
    """Stop the current recording and disconnect from the voice channel."""
    if ctx.guild.id in recordings and ctx.guild.id in connections:
        # Get the recorder and voice client
        recorder = recordings[ctx.guild.id]
        vc = connections[ctx.guild.id]
        
        # Stop recording
        logger.info("Stopping recording")
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
            logger.error(f"Error sending stop message: {str(e)}")
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
        logger.warning("Stop recording command received but no active recording found")

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

def run_bot():
    """Run the Discord bot with the token from environment variables."""
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger.error("No Discord token found in environment variables")
        return
        
    logger.info("Starting Discord voice recording bot")
    bot.run(token)

if __name__ == "__main__":
    run_bot()
