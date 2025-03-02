#!/usr/bin/env python3
"""
Celery tasks for HMBeat.
This module contains the Celery tasks for running the Discord bot.
"""

import os
import sys
import logging
import subprocess
import signal
from celery import shared_task
from celery.utils.log import get_task_logger

# Configure logging
logger = get_task_logger(__name__)

@shared_task(bind=True, name='HMBeat.tasks.run_discord_bot')
def run_discord_bot(self):
    """
    Celery task to run the Discord bot.
    
    This task runs the Discord bot as a subprocess and monitors its execution.
    If the bot is already running (determined by a PID file), it will not start a new instance.
    
    Returns:
        dict: A dictionary containing the status of the task execution.
    """
    logger.info("Starting Discord bot task")
    
    # Check if bot is already running
    pid_file = '/tmp/discord_bot.pid'
    if os.path.exists(pid_file):
        try:
            with open(pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # Check if process is still running
            try:
                os.kill(pid, 0)  # Signal 0 is used to check if process exists
                logger.info(f"Discord bot is already running with PID {pid}")
                return {"status": "already_running", "pid": pid}
            except OSError:
                # Process is not running, remove stale PID file
                logger.warning(f"Removing stale PID file for {pid}")
                os.remove(pid_file)
        except (ValueError, IOError) as e:
            logger.error(f"Error reading PID file: {str(e)}")
            os.remove(pid_file)
    
    # Get the absolute path to the run_bot.py script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    run_bot_path = os.path.join(script_dir, 'run_bot.py')
    
    # Ensure the script is executable
    if not os.access(run_bot_path, os.X_OK):
        logger.info(f"Making {run_bot_path} executable")
        os.chmod(run_bot_path, 0o755)
    
    try:
        # Start the bot as a subprocess
        logger.info(f"Starting Discord bot using {run_bot_path}")
        
        # Use Popen to start the process
        process = subprocess.Popen(
            [sys.executable, run_bot_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            preexec_fn=os.setsid  # Use process group for proper termination
        )
        
        # Save the PID to a file
        with open(pid_file, 'w') as f:
            f.write(str(process.pid))
        
        logger.info(f"Discord bot started with PID {process.pid}")
        
        # Wait for a short time to check if the process crashes immediately
        try:
            return_code = process.wait(timeout=5)
            logger.error(f"Discord bot exited immediately with code {return_code}")
            
            # Read stderr for error information
            _, stderr = process.communicate()
            logger.error(f"Discord bot error output: {stderr}")
            
            # Remove PID file
            if os.path.exists(pid_file):
                os.remove(pid_file)
                
            return {"status": "failed", "return_code": return_code, "error": stderr}
        except subprocess.TimeoutExpired:
            # Process is still running, which is good
            logger.info("Discord bot is running successfully")
            return {"status": "started", "pid": process.pid}
            
    except Exception as e:
        logger.error(f"Error starting Discord bot: {str(e)}", exc_info=True)
        return {"status": "error", "message": str(e)}

@shared_task(bind=True, name='HMBeat.tasks.stop_discord_bot')
def stop_discord_bot(self):
    """
    Celery task to stop the Discord bot.
    
    This task stops the Discord bot process if it's running.
    
    Returns:
        dict: A dictionary containing the status of the task execution.
    """
    logger.info("Stopping Discord bot task")
    
    # Check if bot is running
    pid_file = '/tmp/discord_bot.pid'
    if not os.path.exists(pid_file):
        logger.info("Discord bot is not running (no PID file)")
        return {"status": "not_running"}
    
    try:
        # Read PID from file
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())
        
        # Try to terminate the process group
        try:
            os.killpg(os.getpgid(pid), signal.SIGTERM)
            logger.info(f"Sent SIGTERM to process group {pid}")
            
            # Remove PID file
            os.remove(pid_file)
            return {"status": "stopped", "pid": pid}
        except OSError as e:
            logger.error(f"Error stopping Discord bot: {str(e)}")
            
            # Remove PID file if process doesn't exist
            if e.errno == 3:  # No such process
                os.remove(pid_file)
                return {"status": "not_running", "message": "Process was not running"}
            
            return {"status": "error", "message": str(e)}
    except (ValueError, IOError) as e:
        logger.error(f"Error reading PID file: {str(e)}")
        
        # Remove invalid PID file
        os.remove(pid_file)
        return {"status": "error", "message": str(e)}
