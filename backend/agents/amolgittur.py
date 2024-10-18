# This is an agent which will run and review the GIT diff in the working directory using python subprocess shell 
# command and provide a GIT message based on the GIT commit guidelines. 
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

# Function to get the GIT diff output using subprocess shell command    
def get_git_diff_output(directory):
    os.chdir(directory)
    return os.popen("git diff").read()


# Function to beautify git diff output in xml format    
def beautify_git_diff_output(git_diff_output):
    # Use a tool like 'xmllint' to format the XML output
    formatted_output = subprocess.run(['xmllint', '--format', '-'], input=git_diff_output, capture_output=True, text=True)
    return formatted_output.stdout

# Function to analyze git diff output
def analyze_git_diff_output(content, guidelines):
    """
    Analyze the git diff output using OpenAI.
    This function demonstrates how to use AI for content analysis.
    """
    print("Analyzing git diff output")
    commit_message = generate_completion(
        "code reviewer",
        "Analyze the following git diff output and use the git commit guidelines provided to output a nice and compelling git commit message",
        "git diff output: " + content + "\n" + "git commit guidelines: " + guidelines
    )
    print("commit_message:", commit_message)
    return {"commit_message": commit_message}


# Function to generate completions using OpenAI
def generate_completion(role, task, content):
    """
    Generate a completion using OpenAI's GPT model.
    This function demonstrates how to interact with OpenAI's API.
    """
    print(f"Generating completion for {role}")
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Using GPT-4o for high-quality responses
        messages=[
            {"role": "system", "content": f"You are a {role}. {task}"},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content




# Fast api will get working directory and guidelines from the user and pass it to this agent
class UserInterfaceAgent(Agent):
    def run(self, directory, guidelines):
        print("working directory:", directory)
        print("guidelines:", guidelines)
        git_diff_output = get_git_diff_output(directory)
        commit_message = analyze_git_diff_output(git_diff_output, guidelines)
        print("commit_message:", commit_message)
        print("UserInterfaceAgent: Completed")
        return {"commit_message": commit_message}
    
        
        
        
