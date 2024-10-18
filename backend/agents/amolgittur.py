# This is an agent which will run and review the GIT diff in the working directory using python subprocess shell 
# command and provide a GIT message based on the GIT commit guidelines. 
# Step 1: cd to the working directory
# Step 2: Run the GIT diff command and give git output and 'commitMessageGuidelines.md' as prompt to chat completion API to get the GIT commit message
# Step 3: Show the GIT commit message to the user for human review
# Step 4: Run the GIT commit command and ask for push

import os

import dotenv
from openai import OpenAI

from swarm import Agent
from fastapi import FastAPI

# Load environment variables from .env file
dotenv.load_dotenv(dotenv_path="kaas.env")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to cd to the working directory
def cd_to_working_directory(working_directory):
    os.chdir(working_directory)
    return "cd to working directory"

# Function to run the GIT diff command
def run_git_diff_command():
    return "git diff"

# Function to run the GIT commit command
def run_git_commit_command():
    return "git commit"

# Function to run the GIT push command
def run_git_push_command():
    return "git push"

# Function to run the GIT pull command
def run_git_pull_command():
    return "git pull"

# Function to run the GIT status command
def run_git_status_command():
    return "git status"

# Function to run all the shell command

# Function to beatify git diff output
def beatify_git_diff_output(git_diff_output):
    return git_diff_output

# Function to generate GIT commit message
def generate_git_commit_message(git_diff_output):
    return git_diff_output

# Function to beatify git diff output
def beatify_git_diff_output():
    pass

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

# Function to analyze git diff output
def analyze_git_diff_output(content):
    """
    Analyze the git diff output using OpenAI.
    This function demonstrates how to use AI for content analysis.
    """
    print("Analyzing git diff output")
    analysis = generate_completion(
        "code reviewer",
        "Analyze the following git diff output and provide output in markdown format",
        content
    )
    return {"analysis": analysis}


# Function to generate commit message
def generate_commit_message(brief):
    """
    Generate commit message based on a brief using OpenAI.
    This function shows how AI can be used for content creation.
    """
    print("Generating commit message")
    commit_message = generate_completion(
        "Senior Software Engineer",
        "Create compelling commit message based on the following git diff output presented",
        brief
    )
    return {"commit_message": commit_message}

# Fast api will get working directory and guidelines from the user and pass it to this agent
class UserInterfaceAgent(Agent):
    def run(self, directory, guidelines):
        print("working directory:", directory)
        print("guidelines:", guidelines)
        cd_to_working_directory(directory)
        git_diff_output = run_git_diff_command()
        print("git_diff_output:", git_diff_output)
        analysis = analyze_git_diff_output(git_diff_output)
        print("analysis:", analysis)
        commit_message = generate_commit_message(analysis)
        print("commit_message:", commit_message)
        print("UserInterfaceAgent: Completed")
        return {"commit_message": commit_message}
    
        
        
        

