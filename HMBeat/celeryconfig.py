#!/usr/bin/env python3
"""
Celery configuration for HMBeat.
This module contains the configuration settings for Celery and Celery Beat.
"""

import os
from datetime import timedelta

# Broker settings
broker_url = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')

# Task serialization format
task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'

# Time zone settings
timezone = 'Asia/Calcutta'
enable_utc = True

# Task execution settings
worker_concurrency = 1  # Only run one Discord bot at a time
task_acks_late = True
worker_prefetch_multiplier = 1

# Beat schedule
beat_schedule = {
    'run-discord-bot': {
        'task': 'HMBeat.tasks.run_discord_bot',
        'schedule': timedelta(minutes=1),  # For testing, run every minute
        'options': {
            'expires': 60.0,  # Task expires after 60 seconds
        },
    },
}

# Task routes
task_routes = {
    'HMBeat.tasks.run_discord_bot': {'queue': 'discord_bot'},
}
