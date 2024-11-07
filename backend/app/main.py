from fastapi import (
    FastAPI, Depends, HTTPException, status, Request,
    WebSocket, WebSocketDisconnect
)
from fastapi.middleware.cors import CORSMiddleware
import logging
import json
from agents.coderunner import WebScraperAgent, AnalystAgent, CampaignIdeaAgent, CopywriterAgent
from agents.snowywriter import SnowyInterfaceAgent
from agents.amolgittur import UserInterfaceAgent
from agents.NikhilRaghu import NikhilRaghuAgent
from agents.Arjun import ArjunAgent
from agents.AssistantManager import generate_response, check_if_thread_exists, store_thread
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from db.db_utils import (UserCreate, UserOut, Token, get_password_hash, 
                         verify_password, create_access_token, require_role, get_db,User, Role)


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

# Registration endpoint
@app.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        user (UserCreate): User data to register.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the user already exists.

    Returns:
        UserOut: Registered user data.
    """
    db_user = db.query(User).filter(
        User.phone_number == user.phone_number
    ).first()
    if db_user:
        raise HTTPException(
            status_code=400, detail="Email already registered"
        )
    new_user = User(
        phone_number=user.phone_number,
        password=get_password_hash(user.password),
        name=user.name,
        email=user.email,
        department_id=user.department_id
    )
    user_role = db.query(Role).filter(Role.name == 'User').first()
    if not user_role:
        user_role = Role(name='User')
        db.add(user_role)
        db.commit()
        db.refresh(user_role)
    new_user.role = user_role

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Manager registration endpoint
@app.post("/register_manager", response_model=UserOut)
def register_manager(
    user: UserCreate,
    current_user: User = Depends(require_role(['Admin'])),
    db: Session = Depends(get_db)
):
    """
    Register a new manager user.

    Args:
        user (UserCreate): User data to register.
        current_user (User, optional): Current user. Defaults to Depends(require_role(['Admin'])).
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        UserOut: Registered user data.
    """
    print(f"Current user role: {current_user.role.name}")
    
    db_user = db.query(User).filter(
        User.phone_number == user.phone_number
    ).first()
    if db_user:
        raise HTTPException(
            status_code=400, detail="Email already registered"
        )
    new_user = User(
        phone_number=user.phone_number,
        password=get_password_hash(user.password),
        email=user.email,
        name=user.name,
        department_id=user.department_id
    )
    manager_role = db.query(Role).filter(Role.name == 'Manager').first()
    if not manager_role:
        manager_role = Role(name='Manager')
        db.add(manager_role)
        db.commit()
        db.refresh(manager_role)
    new_user.role = manager_role
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Login endpoint
@app.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login a user.

    Args:
        form_data (OAuth2PasswordRequestForm, optional): Login form data. Defaults to Depends().
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        Token: Access token.
    """
    # OAuth2PasswordRequestForm contains 'username' field, we'll use it for email
    user = db.query(User).filter(
        User.phone_number == form_data.username
    ).first()
    if not user or not verify_password(
        form_data.password, user.password
    ):
        raise HTTPException(
            status_code=400, detail="Incorrect email or password"
        )
    access_token = create_access_token(
        data={
            "sub": user.phone_number,
            "roles": [user.role.name] if user.role else []
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}


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
