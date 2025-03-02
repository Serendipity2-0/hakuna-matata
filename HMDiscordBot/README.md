# Calendar Discord Bot

An interactive Discord bot for managing a calendar database with various features like adding, viewing, updating, and deleting events.

## Features

- **Add Events**: Add new events to the calendar with details like date, content type, format, platform, and schedule time.
- **View Events**: View all events or filter by date (today, this week, or custom date).
- **Update Events**: Update existing events with new information.
- **Delete Events**: Remove events from the calendar.
- **Interactive UI**: Uses Discord's UI components like buttons, dropdowns, and modals for a user-friendly experience.

## Prerequisites

- Python 3.8 or higher
- Discord.py 2.3.2 or higher
- SQLite3
- A Discord bot token (from the [Discord Developer Portal](https://discord.com/developers/applications))

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd hakuna-matata
   ```

2. Install the required dependencies:
   ```bash
   pip install -r HMDiscordBot/requirements.txt
   ```

3. Set up your environment variables:
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp HMDiscordBot/.env.example HMDiscordBot/.env
     ```
   - Edit the `.env` file and add your Discord bot token and optional channel ID.

4. Ensure the database exists:
   - The bot will automatically create the database if it doesn't exist.
   - To create the March 2025 calendar data, use the `/create_march_2025` command after the bot is running.

## Usage

### Starting the Bot

Run the bot using the following command:

```bash
python -m HMDiscordBot
```

### Available Commands

#### Prefix Commands (using the default prefix `!`)

- `!calendar_help` - Show calendar commands
- `!add_event` - Add a new event
- `!view_events` - View all events
- `!view_today` - View today's events
- `!view_week` - View this week's events
- `!view_date [YYYY-MM-DD]` - View events for a specific date
- `!delete_event [id]` - Delete an event
- `!update_event [id]` - Update an event

#### Slash Commands

- `/calendar_help` - Show calendar commands
- `/add_event` - Add a new event
- `/view_events` - View all events
- `/view_date` - View events for a specific date
- `/delete_event` - Delete an event
- `/update_event` - Update an event
- `/create_march_2025` - Create calendar entries for March 2025

### Interactive Features

The bot uses various interactive features to make it user-friendly:

- **Modals**: For entering event details when adding or updating events.
- **Buttons**: For navigating through paginated event lists and confirming actions.
- **Dropdowns**: For selecting date options, platforms, and events.

## Database Structure

The calendar database has the following columns:

- `SerialNo.` - Unique identifier for each event
- `Date` - Date of the event (YYYY-MM-DD)
- `ContentType` - Type of content for the event
- `Format` - Format of the content
- `Platform` - Platform for the content (e.g., Twitter, Facebook, Instagram)
- `ScheduleTime` - Time of the event (HH:MM:SS)
- `Status` - Status of the event (e.g., Scheduled, Completed)
- `CreatedBy` - User who created the event
- `CreatedOn` - Timestamp when the event was created
- `UpdatedBy` - User who last updated the event
- `UpdatedOn` - Timestamp when the event was last updated

## Platforms

The bot supports the following platforms:

- Twitter
- Facebook
- Instagram
- LinkedIn
- YouTube
- VC Pitch Deck
- Blog
- Email
- Podcast
- GeneralScripts

## Creators

The bot recognizes the following creators:

- Omkar
- Snowy

## Customization

You can customize the bot by editing the `config.yml` file in the `HMDiscordBot/config` directory. This file contains settings for:

- Command prefix
- Database paths
- Table names
- Formatting options
- Colors for embeds

## Troubleshooting

- **Bot not responding**: Ensure your Discord token is correct and the bot has the necessary permissions.
- **Database errors**: Check that the database path in the config file is correct.
- **Command errors**: Make sure you're using the correct command syntax and providing all required parameters.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
