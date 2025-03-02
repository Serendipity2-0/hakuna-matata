"""
Audio transcript commands for the Discord bot.
This module implements Discord commands for transcribing audio files.
"""

import os
import logging
import discord
from discord import app_commands
from discord.ext import commands
from typing import Dict, Any, Optional, Literal
from datetime import datetime
import shutil
import sys
import importlib.util
from pathlib import Path

from HMDiscordBot.utils.config import ConfigManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('audio_transcript_commands')

class AudioTranscriptCommands(commands.Cog):
    """
    Discord commands for transcribing audio files.
    
    This cog provides commands for transcribing audio files using different services
    and saving the transcriptions to a designated location.
    """
    
    def __init__(self, bot: commands.Bot):
        """
        Initialize the audio transcript commands.
        
        Args:
            bot: The Discord bot instance
        """
        self.bot = bot
        self.config = ConfigManager()
        
        # Get the audio meet channel ID from environment variables
        self.audiomeet_channel_id = int(os.getenv("DISCORD_AUDIOMEET_CHANNEL_ID"))
        
        # Define paths for saving files
        self.audio_dir = os.path.join("Assets", "AudioMeet")
        self.transcript_dir = os.path.join("DB", "AudioTranscripts")
        
        # Ensure directories exist
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.transcript_dir, exist_ok=True)
        
        logger.info("Audio transcript commands initialized")
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Event handler that runs when the cog is loaded."""
        logger.info("Audio transcript commands cog is ready")
    
    # ===== Prefix Commands =====
    
    @commands.command(name="transcribe_audio")
    async def transcribe_audio_prefix(self, ctx: commands.Context):
        """Transcribe an audio file (interactive)."""
        await ctx.send("Please use the `/transcribe_audio` slash command to transcribe an audio file.")
    
    # ===== Slash Commands =====
    
    @app_commands.command(name="transcribe_audio", description="Transcribe an audio file")
    @app_commands.describe(
        transcription_service="Choose the transcription service to use",
        audio_file="The audio file to transcribe"
    )
    @app_commands.choices(transcription_service=[
        app_commands.Choice(name="Assembly AI", value="assembly"),
        app_commands.Choice(name="Gemini", value="gemini")
    ])
    async def transcribe_audio_slash(
        self, 
        interaction: discord.Interaction, 
        transcription_service: str,
        audio_file: discord.Attachment
    ):
        """
        Transcribe an audio file.
        
        Args:
            interaction: The interaction object
            transcription_service: The transcription service to use (assembly or gemini)
            audio_file: The audio file to transcribe
        """
        # Defer the response to allow for longer processing time
        await interaction.response.defer(ephemeral=True, thinking=True)
        
        try:
            logger.info(f"Received audio file: {audio_file.filename} from {interaction.user.name}")
            logger.info(f"Using transcription service: {transcription_service}")
            
            # Generate a unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_filename = audio_file.filename
            file_extension = os.path.splitext(original_filename)[1]
            new_filename = f"{timestamp}_{original_filename}"
            audio_path = os.path.join(self.audio_dir, new_filename)
            
            # Create directories if they don't exist
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)
            
            # Save the file using a more robust method
            try:
                # First, save to a temporary location
                temp_path = f"temp_{new_filename}"
                await audio_file.save(temp_path)
                
                # Then move to the final location
                shutil.move(temp_path, audio_path)
                logger.info(f"Saved audio file to: {audio_path}")
            except Exception as e:
                logger.error(f"Error saving audio file: {str(e)}", exc_info=True)
                await interaction.followup.send(
                    f"Error saving audio file: {str(e)}. Please make sure the bot has write permissions.",
                    ephemeral=True
                )
                return
            
            # Process the transcription based on the selected service
            if transcription_service == "assembly":
                transcription = await self.transcribe_with_assembly(audio_path)
                service_name = "Assembly AI"
            else:  # gemini
                transcription = await self.transcribe_with_gemini(audio_path)
                service_name = "Gemini"
            
            logger.info(f"Transcription completed using {service_name}")
            
            # Save the transcription to a file
            output_path = self.save_transcription(audio_path, transcription, service_name)
            logger.info(f"Saved transcription to: {output_path}")
            
            # Send the transcription to the designated channel
            await self.send_to_channel(interaction, output_path, audio_path, service_name)
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}", exc_info=True)
            await interaction.followup.send(f"Error transcribing audio: {str(e)}", ephemeral=True)
    
    async def transcribe_with_assembly(self, audio_path: str) -> str:
        """
        Transcribe audio using Assembly AI.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            The transcription text
        """
        logger.info(f"Transcribing with Assembly AI: {audio_path}")
        
        # Import the assembly module
        try:
            # Add the backend directory to the path
            backend_dir = os.path.join(os.getcwd(), "backend")
            if backend_dir not in sys.path:
                sys.path.append(backend_dir)
            
            # Add the agents/tools directory to the path
            tools_dir = os.path.join(backend_dir, "agents", "tools")
            if tools_dir not in sys.path:
                sys.path.append(tools_dir)
            
            try:
                # Try to import directly from the tools directory
                sys.path.insert(0, tools_dir)
                import assemblyAudioTranscript
                
                # Use the existing script's functionality
                # But we need to modify it to use our audio path
                original_file_url = assemblyAudioTranscript.FILE_URL
                assemblyAudioTranscript.FILE_URL = audio_path
                
                # Run the transcription
                transcript = assemblyAudioTranscript.transcriber.transcribe(audio_path)
                
                # Restore the original FILE_URL
                assemblyAudioTranscript.FILE_URL = original_file_url
                
                if transcript.status == assemblyAudioTranscript.aai.TranscriptStatus.error:
                    raise Exception(f"Assembly AI transcription error: {transcript.error}")
                
                return transcript.text
                
            except (ImportError, AttributeError):
                # If direct import fails, try the standard way
                import assemblyai as aai
                import dotenv
                
                # Load environment variables
                dotenv.load_dotenv()
                
                # Set up the API key
                api_key = os.getenv("ASSEMBLYAI_API_KEY")
                if not api_key:
                    raise Exception("ASSEMBLYAI_API_KEY not found in environment variables")
                
                aai.settings.api_key = api_key
                
                # Transcribe the file
                transcriber = aai.Transcriber()
                transcript = transcriber.transcribe(audio_path)
                
                if transcript.status == aai.TranscriptStatus.error:
                    raise Exception(f"Assembly AI transcription error: {transcript.error}")
                
                return transcript.text
            
        except ImportError as e:
            logger.error(f"Error importing Assembly AI module: {str(e)}", exc_info=True)
            raise Exception(
                f"Error importing Assembly AI module: {str(e)}. "
                f"Please make sure the required packages are installed: pip install assemblyai"
            )
        except Exception as e:
            logger.error(f"Error in Assembly AI transcription: {str(e)}", exc_info=True)
            raise Exception(f"Error in Assembly AI transcription: {str(e)}")
    
    async def transcribe_with_gemini(self, audio_path: str) -> str:
        """
        Transcribe audio using Gemini.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            The transcription text
        """
        logger.info(f"Transcribing with Gemini: {audio_path}")
        
        try:
            # Add the backend directory to the path
            backend_dir = os.path.join(os.getcwd(), "backend")
            if backend_dir not in sys.path:
                sys.path.append(backend_dir)
            
            # Add the agents/tools directory to the path
            tools_dir = os.path.join(backend_dir, "agents", "tools")
            if tools_dir not in sys.path:
                sys.path.append(tools_dir)
            
            try:
                # Try to import directly from the tools directory
                sys.path.insert(0, tools_dir)
                import geminiAudiotranscript
                
                # Use the existing script's functionality
                # Convert the file format if needed
                file_extension = os.path.splitext(audio_path)[1].lower()
                if file_extension == '.m4a':
                    mp3_path = os.path.splitext(audio_path)[0] + '.mp3'
                    geminiAudiotranscript.convert_m4a_to_mp3(audio_path, mp3_path)
                    audio_path = mp3_path
                
                # Use the transcribe_audio function from the module
                transcription = geminiAudiotranscript.transcribe_audio(audio_path)
                return transcription
                
            except (ImportError, AttributeError) as e:
                logger.warning(f"Could not import geminiAudiotranscript directly: {str(e)}")
                logger.info("Falling back to standard implementation")
                
                # Import the necessary modules
                import dotenv
                from pydub import AudioSegment
                
                # Import the Google AI module the same way as in geminiAudiotranscript.py
                from google import genai
                from google.genai import types
                
                # Load environment variables
                dotenv.load_dotenv()
                
                # Set up the API key
                api_key = os.getenv("GEMINI_API_KEY")
                if not api_key:
                    raise Exception("GEMINI_API_KEY not found in environment variables")
                
                client = genai.Client(api_key=api_key)
                
                # Check if we need to convert the file format
                file_extension = os.path.splitext(audio_path)[1].lower()
                
                if file_extension == '.m4a':
                    # Convert m4a to mp3
                    logger.info(f"Converting M4A to MP3: {audio_path}")
                    mp3_path = os.path.splitext(audio_path)[0] + '.mp3'
                    
                    # Load the M4A file
                    sound = AudioSegment.from_file(audio_path)
                    
                    # Export the audio to MP3 format
                    sound.export(mp3_path, format="mp3")
                    logger.info(f"Converted to MP3: {mp3_path}")
                    
                    # Use the MP3 file for transcription
                    audio_path = mp3_path
                
                # Read the audio file
                with open(audio_path, 'rb') as f:
                    audio_bytes = f.read()
                
                # Generate the transcription
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=[
                        'Transcribe this audio clip entirely word for word',
                        types.Part.from_bytes(
                            data=audio_bytes,
                            mime_type='audio/mp3',
                        )
                    ]
                )
                
                return response.text
            
        except ImportError as e:
            logger.error(f"Error importing Gemini module: {str(e)}", exc_info=True)
            raise Exception(
                f"Error importing Gemini module: {str(e)}. "
                f"Please make sure the required packages are installed: "
                f"pip install google-generativeai pydub"
            )
        except Exception as e:
            logger.error(f"Error in Gemini transcription: {str(e)}", exc_info=True)
            raise Exception(f"Error in Gemini transcription: {str(e)}")
    
    def save_transcription(self, audio_path: str, transcription: str, service: str) -> str:
        """
        Save the transcription as an MD file.
        
        Args:
            audio_path: Path to the audio file
            transcription: The transcription text
            service: The transcription service used
            
        Returns:
            The path to the saved transcription file
        """
        # Generate the output filename
        base_filename = os.path.basename(audio_path)
        filename_without_ext = os.path.splitext(base_filename)[0]
        output_filename = f"{filename_without_ext}_{service.replace(' ', '_').lower()}_transcript.md"
        output_path = os.path.join(self.transcript_dir, output_filename)
        
        # Create the MD content
        md_content = f"# Audio Transcription\n\n"
        md_content += f"Source: {audio_path}\n"
        md_content += f"Transcription Service: {service}\n"
        md_content += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md_content += "## Content\n\n"
        md_content += transcription
        
        # Write to file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            logger.info(f"Transcription saved to: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error saving transcription: {str(e)}", exc_info=True)
            raise Exception(f"Error saving transcription: {str(e)}")
    
    async def send_to_channel(self, interaction: discord.Interaction, output_path: str, audio_path: str, service: str):
        """
        Send the transcription to the designated channel.
        
        Args:
            interaction: The interaction object
            output_path: Path to the transcription file
            audio_path: Path to the audio file
            service: The transcription service used
        """
        # Get the channel
        channel = self.bot.get_channel(self.audiomeet_channel_id)
        
        if not channel:
            logger.error(f"Could not find channel with ID {self.audiomeet_channel_id}")
            await interaction.followup.send(
                f"Error: Could not find channel with ID {self.audiomeet_channel_id}",
                ephemeral=True
            )
            return
        
        try:
            # Create an embed for the transcription
            embed = discord.Embed(
                title="Audio Transcription",
                description=f"Transcription of {os.path.basename(audio_path)}",
                color=discord.Color.blue()
            )
            
            embed.add_field(name="Transcription Service", value=service, inline=True)
            embed.add_field(name="Date", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), inline=True)
            embed.add_field(name="Requested By", value=interaction.user.mention, inline=True)
            
            # Read the transcription file to get a preview
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Get the actual transcription content (after the "## Content" line)
            content_parts = content.split("## Content\n\n")
            if len(content_parts) > 1:
                transcription_text = content_parts[1]
                
                # Add a preview of the transcription (first 1000 characters)
                preview = transcription_text[:1000] + ("..." if len(transcription_text) > 1000 else "")
                embed.add_field(name="Preview", value=preview, inline=False)
            
            # Send the transcription file
            try:
                # Check if file exists and is readable
                if not os.path.exists(output_path):
                    raise FileNotFoundError(f"Transcription file not found: {output_path}")
                
                # Check file size
                file_size = os.path.getsize(output_path)
                if file_size > 8 * 1024 * 1024:  # 8 MB limit for Discord attachments
                    logger.warning(f"File size ({file_size} bytes) exceeds Discord's limit")
                    # Split the file if it's too large
                    with open(output_path, 'r', encoding='utf-8') as f:
                        full_content = f.read()
                    
                    # Send the content as text if it's too large to attach
                    await channel.send(embed=embed)
                    
                    # Split content into chunks of 2000 characters (Discord message limit)
                    chunks = [full_content[i:i+1990] for i in range(0, len(full_content), 1990)]
                    for i, chunk in enumerate(chunks):
                        await channel.send(f"```md\n{chunk}\n``` (Part {i+1}/{len(chunks)})")
                else:
                    # Send as file attachment
                    discord_file = discord.File(output_path, filename=os.path.basename(output_path))
                    await channel.send(embed=embed, file=discord_file)
                
                logger.info(f"Transcription sent to channel: {channel.name} ({channel.id})")
            except Exception as e:
                logger.error(f"Error sending file to channel: {str(e)}", exc_info=True)
                # Try to send just the embed without the file
                await channel.send(
                    content=f"Error attaching transcription file: {str(e)}",
                    embed=embed
                )
            
            # Also send a confirmation to the user
            await interaction.followup.send(
                f"Transcription complete! The transcription has been sent to <#{self.audiomeet_channel_id}>.",
                ephemeral=True
            )
            
        except Exception as e:
            logger.error(f"Error sending transcription to channel: {str(e)}", exc_info=True)
            await interaction.followup.send(
                f"Error sending transcription to channel: {str(e)}",
                ephemeral=True
            )


async def setup(bot: commands.Bot):
    """Add the audio transcript commands cog to the bot."""
    await bot.add_cog(AudioTranscriptCommands(bot))
