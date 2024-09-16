# Hakuna Matata Project

Welcome to the Hakuna Matata project! This document will guide you through the process of running the project using Docker and how to use its APIs.

## Prerequisites

- Docker installed on your system
- Bash shell (for Unix-based systems) or Git Bash (for Windows)

## Getting Started

To run the project, follow these simple steps:

1. Clone the repository to your local machine:
   ```
   git clone <repository-url>
   cd hakuna-matata
   ```

2. Make sure the `start_docker.sh` script is executable:
   ```
   chmod +x startup_control/start_docker.sh
   ```

3. Run the `start_docker.sh` script:
   ```
   ./startup_control/start_docker.sh
   ```

This script will:
- Build the Docker image if it doesn't exist
- Stop and remove any existing container with the same name
- Start a new container named "hakuna-matata"
- Map port 8000 from the container to port 8000 on your host machine
- Set the container to restart automatically unless stopped manually

## Accessing the Application

Once the container is running, you can access the application at:

## APIs Flow

The project provides two main API endpoints for processing meeting data and retrieving wisdom files. Here's how to use them:

### 1. Submit Meeting Transcription

**Endpoint:** `POST /meeting/submit-meeting`

This API allows you to submit a meeting for transcription and knowledge base building.

**Parameters:**
- `language` (string): The language of the meeting audio.
- `meeting_subject` (string): The subject or topic of the meeting.
- `knowledge_patterns` (array): List of knowledge patterns to extract.
- `department` (string): The department associated with the meeting.
- `audio_file` (file): The audio file of the meeting to be transcribed.

**Example using cURL:**
```
curl --location 'http://0.0.0.0:80/meeting/submit-meeting' \
--form 'audio_file=@"/Users/satyarthraghuvanshi/Downloads/sample_meeting.m4a"' \
--form 'language="en"' \
--form 'meeting_subject="Random Meetings"' \
--form 'knowledge_patterns="idea_compass, keynote"' \
--form 'department="trademan"'
```

### 2. Download Wisdom File

**Endpoint:** `GET /meeting/wisdom-file`

This API allows you to download a specific wisdom file.

**Parameters:**
- `file_path` (string): The path to the wisdom file you want to download.

**Example using cURL:**
```
curl --location 'http://0.0.0.0:80/meeting/wisdom-file/20240725_120000_UTC_idea_compass_trademan.md'
```
