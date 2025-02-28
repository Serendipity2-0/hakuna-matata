from fastapi import APIRouter
from coderunner import WebScraperAgent

router = APIRouter()

@router.post("/agents/run")
async def run_agent():
    url = "https://docs.google.com/document/d/11IF4Mi8qNHI3jEmJg_6EzWBtfrqeiMRtK0mS80w8pKU/edit?pli=1&tab=t.0"
    agent = WebScraperAgent()
    result = await agent.run(url)
    print("result:", result)
    return {"result": result}