# HMBeat - Discord Bot with Celery Beat

This project runs the Discord bot via Celery Beat using Docker for scheduling and management.

## Project Structure

- `HMDiscordBot/`: The main Discord bot code
- `HMBeat/`: Celery configuration and tasks for running the Discord bot
- `Dockerfile`: Docker configuration for building the application container
- `docker-compose.yml`: Docker Compose configuration for orchestrating services
- `.env`: Environment variables for configuration

## Prerequisites

- Docker and Docker Compose installed
- Discord Bot Token (from Discord Developer Portal)

## Setup

1. Clone the repository
2. Update the `.env` file with your Discord Bot Token and channel IDs:
   ```
   DISCORD_TOKEN=your_discord_token_here
   DISCORD_VOICE_CHANNEL_ID=your_voice_channel_id
   DISCORD_TEXT_CHANNEL_ID=your_text_channel_id
   ```

## Running with Docker

1. Build and start the services:
   ```bash
   docker-compose up -d
   ```

2. Check the logs:
   ```bash
   docker-compose logs -f
   ```

3. Stop the services:
   ```bash
   docker-compose down
   ```

## Services

- **Redis**: Message broker for Celery
- **Worker**: Celery worker that executes the Discord bot task
- **Beat**: Celery Beat scheduler that triggers the Discord bot task periodically
- **Flower**: Web UI for monitoring Celery tasks (optional, available at http://localhost:5555)

## Monitoring

You can monitor the Celery tasks using Flower at http://localhost:5555

## Voice Channel Recording

The Discord bot includes voice channel recording functionality. The PyNaCl library is required for voice functionality and has been included in the Docker setup.

### Audio Fallback Mechanism

The system includes a fallback mechanism for environments where audio devices are not available (like in Docker containers). When no physical audio device is detected, the bot will automatically use a dummy audio implementation that generates silent recordings. This ensures the bot can still function in containerized environments without audio hardware access.

## Configuration

The Discord bot is scheduled to run every minute by default. You can change this in `HMBeat/celeryconfig.py`:

```python
beat_schedule = {
    'run-discord-bot': {
        'task': 'HMBeat.tasks.run_discord_bot',
        'schedule': timedelta(minutes=1),  # Change this to your desired schedule
        'options': {
            'expires': 60.0,
        },
    },
}
```

## Troubleshooting

- If the bot doesn't start, check the logs with `docker-compose logs -f worker`
- Ensure your Discord token is correct in the `.env` file
- Check if the Redis service is running with `docker-compose ps`
