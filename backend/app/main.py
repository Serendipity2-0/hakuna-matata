# backend/app/main.py
from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging
import json
from agents.coderunner import WebScraperAgent, AnalystAgent, CampaignIdeaAgent, CopywriterAgent
from agents.snowywriter import SnowyInterfaceAgent
from agents.amolgittur import UserInterfaceAgent
from agents.NikhilRaghu import NikhilRaghuAgent
from agents.Arjun import ArjunAgent
from agents.AssistantManager import generate_response, check_if_thread_exists, store_thread

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

@app.post("/api/eod_message")
async def post_eod_message(request: Request):
    data = await request.json()
    eod_messages = data.get("eod_messages")
    
    if not eod_messages:
        raise HTTPException(status_code=400, detail="Missing telegram messages")
    
    arjun_agent = ArjunAgent()
    eod_telegram_message = await arjun_agent.run_async(eod_messages)
    return {"eod_telegram_message": eod_telegram_message}

@app.websocket("/ws/assistant")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    wa_id = None
    name = None

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message["type"] == "init":
                wa_id = message["wa_id"]
                name = message["name"]
                await websocket.send_json({"type": "init", "status": "success"})
            elif message["type"] == "message":
                if not wa_id or not name:
                    await websocket.send_json({"type": "error", "message": "Session not initialized"})
                else:
                    response = generate_response(message["content"], wa_id, name)
                    await websocket.send_json({"type": "message", "content": response})
            elif message["type"] == "reset":
                if wa_id:
                    store_thread(wa_id, None)
                    await websocket.send_json({"type": "reset", "status": "success"})
                else:
                    await websocket.send_json({"type": "error", "message": "Session not initialized"})
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for {name} with wa_id {wa_id}")
    finally:
        # Optionally, you can add cleanup code here if needed
        pass

@app.get("/api/assistant/thread_exists/{wa_id}")
async def thread_exists(wa_id: str):
    thread_id = check_if_thread_exists(wa_id)
    return {"exists": thread_id is not None}
