"""
HMBeat package for running the Discord bot via Celery Beat.
"""

from HMBeat.celery_app import app as celery_app

__all__ = ['celery_app']
