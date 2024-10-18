# This is an agent which will take the perplexity research link and provide script outline for dhoom studios

# Step 1: cd to the working directory
# Step 2: Run the GIT diff command and give git output and 'commitMessageGuidelines.md' as prompt to chat completion API to get the GIT commit message
# Step 3: Show the GIT commit message to the user for human review
# Step 4: Run the GIT commit command and ask for push

import os
import subprocess
import dotenv
from openai import OpenAI

from swarm import Agent
from fastapi import FastAPI

# Load environment variables from .env file
dotenv.load_dotenv(dotenv_path="kaas.env")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# read the md file and return formatted content
def get_perplexity_research_link(directory):
    with open(directory, "r") as file:
        content = file.read()
    return content
    
# Function to analyze and generate script outline   
def generate_script_outline(content, guidelines):
    """
    Analyze the perplexity research link and generate script outline for dhoom studios
    This function demonstrates how to use AI for content analysis.
    """
    print("Generating script outline")
    script_outline = generate_completion(
        "script writer",
        "Analyze the following perplexity research link and generate script outline for dhoom studios",
        f"perplexity research link: {content}\n\nGuidelines: {guidelines}"
    )
    print("script_outline:", script_outline)
    return script_outline

# Function to generate completions using OpenAI
def generate_completion(role, task, content):
    """
    Generate a completion using OpenAI's GPT model.
    This function demonstrates how to interact with OpenAI's API.
    """
    print(f"Generating completion for {role}")
    response = client.chat.completions.create(
        model="gpt-4",  # Using GPT-4 for high-quality responses
        messages=[
            {"role": "system", "content": f"You are a {role}. {task}"},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content




# Fast api will get working directory and guidelines from the user and pass it to this agent
class SnowyInterfaceAgent(Agent):
    def run(self, directory, guidelines):
        print("working directory:", directory)
        print("guidelines:", guidelines)
        perplexity_research_link = get_perplexity_research_link(directory)
        
        # If guidelines are not provided, load them from patterns/scriptGuide.md
        if not guidelines:
            with open("patterns/scriptGuide.md", "r") as file:
                guidelines = file.read()
        
        script_outline = generate_script_outline(perplexity_research_link, guidelines)
        print("script_outline:", script_outline)
        print("SnowyInterfaceAgent: Completed")
        return script_outline
