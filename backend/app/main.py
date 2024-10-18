# backend/app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from agents.coderunner import WebScraperAgent, AnalystAgent, CampaignIdeaAgent, CopywriterAgent
from agents.amolgittur import UserInterfaceAgent

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/agents/scrape")
async def run_scraper(request: Request):
    data = await request.json()
    url = data.get("url")
    scraper_agent = WebScraperAgent()
    scraped_content, structured_content = await scraper_agent.run(url)
    return {"scraped_content": scraped_content, "structured_content": structured_content}

@app.post("/agents/analyze")
async def analyze_content(request: Request):
    data = await request.json()
    content = data.get("content")
    analyst_agent = AnalystAgent()
    analysis = await analyst_agent.run(content)
    return {"analysis": analysis}

@app.post("/agents/coding_outline")
async def generate_coding_outline(request: Request):
    data = await request.json()
    target_audience = data.get("target_audience")
    goals = data.get("goals")
    campaign_agent = CampaignIdeaAgent()
    outline = await campaign_agent.run(target_audience, goals)
    return {"coding_outline": outline}

@app.post("/agents/generate_copy")
async def generate_copy(request: Request):
    data = await request.json()
    brief = data.get("brief")
    copywriter_agent = CopywriterAgent()
    instructions = await copywriter_agent.run(brief)
    return {"coding_instructions": instructions}

@app.post("/api/git_commit_message")
async def generate_commit_message(request: Request):
    data = await request.json()
    directory = data.get("directory")
    guidelines = data.get("guidelines")
    ui_agent = UserInterfaceAgent()
    commit_message = ui_agent.run(directory, guidelines)
    return {"commit_message": commit_message}
