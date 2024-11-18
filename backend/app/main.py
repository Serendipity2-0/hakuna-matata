from fastapi import (
    FastAPI, Depends, HTTPException, status, Request,
    WebSocket, WebSocketDisconnect, UploadFile, File, Form
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
                         verify_password, create_access_token, require_role, get_db,User, Role, get_department_name,
                         get_all_departments)
import os
from typing import Optional
from pathlib import Path


current_dir = os.getcwd()
if os.path.basename(current_dir) == 'backend':
    # Go one folder back
    os.chdir('..')



DOCS_FOLDER_PATH = os.path.join(os.getcwd(), "docs")
print("DOCS_FOLDER_PATH", DOCS_FOLDER_PATH)


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


@app.post("/upload-file")
async def upload_file(
    file: UploadFile = File(...),
    file_path: str = Form(...),
    create_dir: Optional[bool] = Form(False),
    current_user: User = Depends(require_role(['Admin', 'Manager'])),
):
    """
    Upload an MD file to a specified directory.
    
    Args:
        file (UploadFile): The MD file to upload
        file_path (str): Destination path for the file
        create_dir (bool, optional): Whether to create directory if it doesn't exist
        current_user (User): Current authenticated user
        db (Session): Database session
    
    Returns:
        dict: Upload status and file details
    """
    # Validate file extension
    if not file.filename.endswith('.md'):
        raise HTTPException(
            status_code=400,
            detail="Only markdown (.md) files are allowed"
        )

    try:
        # Append department-specific path based on user role
        if current_user.role.name == 'Admin':
            dir_path = os.path.join(DOCS_FOLDER_PATH, file_path)
        elif current_user.role.name == 'Manager':
            department_id = current_user.department_id
            department_name = get_department_name(department_id)
            dir_path = os.path.join(DOCS_FOLDER_PATH, department_name, file_path)
        else:
            raise HTTPException(
                status_code=403,
                detail="User does not have permission to upload files"
            )

        # Ensure the directory path is absolute
        abs_path = os.path.abspath(dir_path)
        
        # Check if directory exists
        if not os.path.exists(dir_path):
            if not create_dir:
                return {
                    "status": "error",
                    "detail": "Directory does not exist",
                    "create_dir_option": True,
                    "path": dir_path
                }
            
            # Create directory if requested
            os.makedirs(dir_path, exist_ok=True)

        # Read and write file content
        file_content = await file.read()
        
        # Generate full file path including filename
        full_file_path = os.path.join(abs_path, file.filename)
        
        # Write file
        with open(full_file_path, "wb") as f:
            f.write(file_content)

        return {
            "status": "success",
            "detail": "File uploaded successfully",
            "filename": file.filename,
            "path": full_file_path
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading file: {str(e)}"
        )

@app.get("/view-docs")
async def view_docs(
    current_user: User = Depends(require_role(['Admin', 'Manager', 'User'])),
    db: Session = Depends(get_db)
):
    """
    Retrieve MD documents based on user's role and department.
    
    Args:
        current_user (User): Current authenticated user
        db (Session): Database session
    
    Returns:
        dict: List of documents with their metadata
    """
    try:
        # Initialize list to store document information
        documents = []
        
        # Define base path for document search
        if current_user.role.name == 'Admin':
            # Admin can see all documents
            search_path = Path(DOCS_FOLDER_PATH)
        else:
            # Other users can only see their department's documents
            department_name = get_department_name(current_user.department_id)
            search_path = Path(DOCS_FOLDER_PATH) / department_name
            
            # If department folder doesn't exist, return empty list
            if not search_path.exists():
                return {"documents": []}

        # Recursively find all .md files
        for md_file in search_path.rglob("*.md"):
            # Get relative path from docs folder
            rel_path = md_file.relative_to(Path(DOCS_FOLDER_PATH))
            
            # Get file stats
            stats = md_file.stat()
            
            documents.append({
                "name": md_file.name,
                "path": str(rel_path),
                "full_path": str(md_file),
                "modified_date": stats.st_mtime,
                "size": stats.st_size,
                "department": rel_path.parts[0] if len(rel_path.parts) > 1 else "root"
            })

        # Sort documents by modified date (newest first)
        documents.sort(key=lambda x: x["modified_date"], reverse=True)


        # For Admin, set department to "All Departments"
        if current_user.role.name == 'Admin':
            department = "All Departments"
        else:
            department = get_department_name(current_user.department_id)

        return {
            "documents": documents,
            "user_role": current_user.role.name,
            "department": department
        }

    except Exception as e:
        logger.error(f"Error fetching documents: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching documents: {str(e)}"
        )
    
@app.get("/list-of-departments")
async def list_of_departments(
    current_user: User = Depends(require_role(['Admin'])),
):
    return {"departments": get_all_departments()}

@app.get("/view-doc/{doc_path:path}")
async def read_document(
    doc_path: str,
    current_user: User = Depends(require_role(['Admin', 'Manager', 'User'])),
    db: Session = Depends(get_db)
):
    """
    Read and return the contents of a specific markdown document.
    
    Args:
        doc_path (str): Path to the document relative to DOCS_FOLDER_PATH
        current_user (User): Current authenticated user
        db (Session): Database session
    
    Returns:
        dict: Document content and metadata
    """
    try:
        # Construct full file path
        full_path = Path(DOCS_FOLDER_PATH) / doc_path

        # Security check: Ensure the file is within docs_folder_path
        if not str(full_path.resolve()).startswith(str(Path(DOCS_FOLDER_PATH).resolve())):
            raise HTTPException(
                status_code=403,
                detail="Access to this file path is forbidden"
            )

        # Check if file exists
        if not full_path.exists() or not full_path.is_file():
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

        # Check user permissions
        if current_user.role.name != 'Admin':
            department_name = get_department_name(current_user.department_id)
            # Check if the file is in user's department folder
            if department_name not in str(full_path):
                raise HTTPException(
                    status_code=403,
                    detail="You don't have permission to access this document"
                )

        # Read file content
        try:
            with open(full_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="File is not a valid text document"
            )

        # Get file stats
        stats = full_path.stat()

        return {
            "content": content,
            "metadata": {
                "name": full_path.name,
                "path": doc_path,
                "modified_date": stats.st_mtime,
                "size": stats.st_size
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reading document: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error reading document: {str(e)}"
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

