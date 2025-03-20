# backend/app/main_simple.py
# A simplified version of main.py that doesn't import the agents
# This allows us to test the user synchronization functionality without
# having to install all the dependencies for the existing agents

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from .routes import user_routes

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

# Include routers
app.include_router(user_routes.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the User Sync API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
