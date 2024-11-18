# This is a simple telegram agent based on telthon api. It will take content and post it specific peer(channel or user) in telegram groups or individual users.

# Step 1: collect the text and send it to llm along with guidelines and get the formatted response
# Step 2: send the formatted response to telegram peer using telthon api

import os
import dotenv
from openai import OpenAI
from swarm import Agent
from telethon import TelegramClient
import asyncio
from pathlib import Path

# Get the directory of the current script
current_dir = Path(__file__).parent.absolute()

# Get the path to the .env file
env_path = Path(current_dir).parent.parent / 'kaas.env'

# Load environment variables from .env file
dotenv.load_dotenv(env_path)

# Initialize OpenAI client
TELEGRAM_API_ID = os.getenv("telegram_api_id")
TELEGRAM_API_HASH = os.getenv("telegram_api_hash")
TELEGRAM_PHONE_NUMBER = os.getenv("telegram_phone_number")
TELEGRAM_CHANNEL_ID = os.getenv("telegram_channel_id")
TELEGRAM_PEER_ID = os.getenv("telegram_peer_id")
EODMSGPATH = os.getenv("EODMSGGEN_PATH")
OPENAI_API_KEY = os.getenv("NEW_OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

client = OpenAI(api_key=OPENAI_API_KEY)

class TelegramAdapter:
    def __init__(self, api_id, api_hash, phone_number):
        self.client = TelegramClient('session_name', api_id, api_hash)
        self.phone_number = phone_number
        self.channel_id = -1001677058465

    async def start(self):
        await self.client.start(phone=self.phone_number)
        print("Client Started")

    async def stop(self):
        await self.client.disconnect()
        print("Client Stopped")

    async def send_message(self, message):
        if self.channel_id is None:
            raise ValueError("Channel ID is not set. Please set a channel first.")
        await self.client.send_message(self.channel_id, message)

# Function to generate EOD telegram message
def generate_eod_message(markdown_report, guidelines):
    print("Generating EOD message")
    eod_message = generate_completion(
        "Daily EOD Message Generator",
        "",
        f"Generated stats: {markdown_report}\n\nGuidelines: {guidelines}"
    )
    print("EOD message generated")
    return eod_message

# Function to generate completions using OpenAI
def generate_completion(role, task, content):
    print(f"Generating completion for {role}")
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": f"You are a {role}. {task}"},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content

class ArjunAgent(Agent):
    def __init__(self):
        super().__init__()
        # Load environment variables in the constructor
        self._telegram_api_id = TELEGRAM_API_ID
        self._telegram_api_hash = TELEGRAM_API_HASH
        self._telegram_phone_number = TELEGRAM_PHONE_NUMBER
        self._eodmsggen_path = os.path.normpath(EODMSGPATH)

    async def run_async(self, telegram_messages):
        try:
            if not os.path.exists(self._eodmsggen_path):
                raise FileNotFoundError(f"File not found: {self._eodmsggen_path}")
            
            with open(self._eodmsggen_path, "r") as file:
                guidelines = file.read()
                print(f"guidelines: {guidelines}")
            
            eod_message = generate_eod_message(telegram_messages, guidelines)
            print("ArjunAgent: Completed")
            print(f"eod_message: {eod_message}")
            
            # send the eod message to telegram
            telegram_adapter = TelegramAdapter(self._telegram_api_id, self._telegram_api_hash, self._telegram_phone_number)
            await telegram_adapter.start()
            await telegram_adapter.send_message(eod_message)
            await telegram_adapter.stop()
            
            return eod_message
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            print(error_message)
            return error_message

    def run(self, telegram_messages):
        return asyncio.get_event_loop().run_until_complete(self.run_async(telegram_messages))
