#!/usr/bin/env python3
"""
Celery application configuration for HMBeat.
This module sets up the Celery application for scheduling and running the Discord bot.
"""

import os
from celery import Celery

# Set default Django settings module if using Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Create Celery app
app = Celery('hmbeat')

# Load configuration from environment variables with prefix CELERY_
app.config_from_object('HMBeat.celeryconfig')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks(['HMBeat'])

if __name__ == '__main__':
    app.start()
