FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    libffi-dev \
    libnacl-dev \
    libopus-dev \
    libportaudio2 \
    portaudio19-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY HMDiscordBot/requirements.txt /app/HMDiscordBot/requirements.txt
COPY HMBeat/requirements.txt /app/HMBeat/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r HMDiscordBot/requirements.txt \
    && pip install --no-cache-dir -r HMBeat/requirements.txt \
    && pip install --no-cache-dir pyaudio PyNaCl flower

# Copy application code
COPY HMDiscordBot /app/HMDiscordBot
COPY HMBeat /app/HMBeat

# Make run_bot.py executable
RUN chmod +x /app/HMBeat/run_bot.py

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Create directory for recordings
RUN mkdir -p /app/recordings

# Default command
CMD ["celery", "-A", "HMBeat", "worker", "--loglevel=info"]
