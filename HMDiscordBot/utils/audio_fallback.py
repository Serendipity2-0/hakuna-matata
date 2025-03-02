"""
Audio fallback module for Discord voice recording.
This module provides fallback mechanisms for audio recording when no physical audio device is available.
"""

import os
import logging
import wave
import struct
import time
import threading
from datetime import datetime

# Configure logging
logger = logging.getLogger('discord_audio_fallback')

class DummyAudioStream:
    """
    A dummy audio stream that generates silent audio data.
    Used as a fallback when no physical audio device is available.
    """
    
    def __init__(self, format, channels, rate, input_device_index=None, frames_per_buffer=1024):
        """
        Initialize the dummy audio stream.
        
        Args:
            format: Audio format (ignored in dummy implementation)
            channels: Number of audio channels
            rate: Sample rate
            input_device_index: Device index (ignored in dummy implementation)
            frames_per_buffer: Buffer size
        """
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self.running = False
        logger.info("Initialized dummy audio stream (fallback mode)")
    
    def read(self, chunk_size, exception_on_overflow=False):
        """
        Read audio data from the dummy stream (generates silence).
        
        Args:
            chunk_size: Number of frames to read
            exception_on_overflow: Whether to raise an exception on overflow (ignored)
            
        Returns:
            bytes: Silent audio data
        """
        # Generate silent audio data (all zeros)
        return b'\x00' * (chunk_size * self.channels * 2)  # 2 bytes per sample for 16-bit audio
    
    def stop_stream(self):
        """Stop the dummy stream."""
        self.running = False
        logger.info("Stopped dummy audio stream")
    
    def close(self):
        """Close the dummy stream."""
        self.running = False
        logger.info("Closed dummy audio stream")

class DummyPyAudio:
    """
    A dummy PyAudio implementation that provides fallback functionality.
    Used when the real PyAudio fails to initialize or find audio devices.
    """
    
    def __init__(self):
        """Initialize the dummy PyAudio object."""
        logger.info("Initialized dummy PyAudio (fallback mode)")
    
    def get_host_api_info_by_index(self, index):
        """
        Get host API info (dummy implementation).
        
        Args:
            index: API index
            
        Returns:
            dict: Dummy API info
        """
        return {'deviceCount': 1}
    
    def get_device_info_by_index(self, index):
        """
        Get device info (dummy implementation).
        
        Args:
            index: Device index
            
        Returns:
            dict: Dummy device info
        """
        return {
            'name': 'Dummy Audio Device',
            'maxInputChannels': 1,
            'maxOutputChannels': 1
        }
    
    def open(self, format, channels, rate, input=True, input_device_index=None, frames_per_buffer=1024):
        """
        Open a dummy audio stream.
        
        Args:
            format: Audio format
            channels: Number of audio channels
            rate: Sample rate
            input: Whether this is an input stream
            input_device_index: Device index
            frames_per_buffer: Buffer size
            
        Returns:
            DummyAudioStream: A dummy audio stream object
        """
        return DummyAudioStream(format, channels, rate, input_device_index, frames_per_buffer)
    
    def get_sample_size(self, format):
        """
        Get the sample size for the given format.
        
        Args:
            format: Audio format
            
        Returns:
            int: Sample size (always 2 for 16-bit audio)
        """
        return 2  # 16-bit audio = 2 bytes per sample
    
    def terminate(self):
        """Terminate the dummy PyAudio object."""
        logger.info("Terminated dummy PyAudio")

def create_silent_wav_file(filepath, channels=1, sample_rate=44100, duration_seconds=60):
    """
    Create a silent WAV file.
    
    Args:
        filepath: Path to save the WAV file
        channels: Number of audio channels
        sample_rate: Sample rate
        duration_seconds: Duration of the silent audio in seconds
        
    Returns:
        str: Path to the created WAV file
    """
    logger.info(f"Creating silent WAV file at {filepath}")
    
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Open the WAV file for writing
    with wave.open(filepath, 'wb') as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(2)  # 2 bytes for 16-bit audio
        wav_file.setframerate(sample_rate)
        
        # Calculate the number of frames
        n_frames = duration_seconds * sample_rate
        
        # Write silent frames (all zeros)
        for _ in range(0, n_frames, 1000):
            # Write 1000 frames at a time to avoid memory issues
            frames_to_write = min(1000, n_frames - _)
            wav_file.writeframes(b'\x00' * frames_to_write * channels * 2)
    
    logger.info(f"Created silent WAV file at {filepath}")
    return filepath
