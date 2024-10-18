# backend/app/main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging
from agents.coderunner import WebScraperAgent, AnalystAgent, CampaignIdeaAgent, CopywriterAgent
from agents.snowywriter import SnowyInterfaceAgent
from agents.amolgittur import UserInterfaceAgent
from agents.NikhilRaghu import NikhilRaghuAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    try:
        logger.info("Received request for git commit message")
        data = await request.json()
        logger.info(f"Received data: {data}")
        
        directory = data.get("directory")
        guidelines = data.get("guidelines")
        
        if not directory or not guidelines:
            raise HTTPException(status_code=400, detail="Missing directory or guidelines")
        
        ui_agent = UserInterfaceAgent()
        commit_message = ui_agent.run(directory, guidelines)
        
        # Ensure the commit message is a string
        if not isinstance(commit_message, str):
            commit_message = str(commit_message)
        
        logger.info(f"Generated commit message: {commit_message}")
        return {"commit_message": {"commit_message": commit_message}}
    except Exception as e:
        logger.error(f"Error generating commit message: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/script_outline")
async def generate_script_outline(request: Request):
    data = await request.json()
    file_path = data.get("directory")  # We're using 'directory' as file_path now
    guidelines = data.get("guidelines", "")
    
    if not file_path:
        raise HTTPException(status_code=400, detail="Missing file path")
    
    ui_agent = SnowyInterfaceAgent()
    script_outline = ui_agent.run(file_path, guidelines)
    return {"script_outline": script_outline}

@app.post("/api/financial_analysis_report")
async def generate_financial_analysis_report(request: Request):
    try:
        data = await request.json()
        file_path = data.get("directory")
        guidelines = data.get("guidelines", "")
        
        if not file_path:
            raise HTTPException(status_code=400, detail="Missing file path")
        
        ui_agent = NikhilRaghuAgent()
        financial_analysis_report = ui_agent.run(file_path, guidelines)
        
        if financial_analysis_report.startswith("An error occurred:"):
            raise HTTPException(status_code=500, detail=financial_analysis_report)
        
        return {"financial_analysis_report": financial_analysis_report}
    except Exception as e:
        logger.error(f"Error generating financial analysis report: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
