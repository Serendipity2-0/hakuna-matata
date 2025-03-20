# backend/app/routes/user_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..database_direct import get_user, create_or_update_user

router = APIRouter()

class UserCreate(BaseModel):
    id: str
    username: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

@router.post("/users/")
def create_user(user: UserCreate):
    """
    Create a new user or update if exists
    """
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }
    
    db_user = create_or_update_user(user_data)
    return {"id": db_user["id"], "username": db_user["username"]}

@router.get("/users/{user_id}")
def get_user_by_id(user_id: str):
    """
    Get user by ID
    """
    db_user = get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
