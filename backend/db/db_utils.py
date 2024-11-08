from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey, Table
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import os
from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException,status
from sqlalchemy.orm import Session

DIR_PATH = os.getcwd()

env_path = os.path.join(DIR_PATH, "kaas.env")

load_dotenv(dotenv_path = env_path)

DB_PATH = os.getenv("DB_PATH")

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=True, index=True)
    name = Column(String, nullable=True)
    department_id = Column(Integer, nullable=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=True)
    password = Column(String, nullable=False)
    # Relationships
    role = relationship('Role', back_populates='users')

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    # Relationships
    users = relationship('User', back_populates='role')


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

# Create the tables and initialize super admin
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key and algorithm
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set")
ALGORITHM = "HS256"

# Pydantic models
class UserCreate(BaseModel):
    phone_number: str
    password: str
    email: str
    name: Optional[str] = None
    department_id: Optional[int] = None

class UserOut(BaseModel):
    id: int
    phone_number: str
    name: Optional[str] = None
    department_id: Optional[int] = None
    role_id: Optional[int] = None

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Utility functions
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    # Optionally add expiration
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Authentication dependencies
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        phone_number: str = payload.get("sub")
        roles: List[str] = payload.get("roles", [])
        if phone_number is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(
        User.phone_number == phone_number
    ).first()
    if user is None:
        raise credentials_exception
    return user

def require_role(roles: List[str]):
    def role_checker(
        current_user: User = Depends(get_current_user)
    ):
        user_role = current_user.role.name if current_user.role else None
        if user_role not in roles:
            raise HTTPException(
                status_code=403, detail="Not enough permissions"
            )
        return current_user
    return role_checker

def get_department_name(department_id: int):
    """
    Fetch the department name by department id.

    Args:
        department_id (int): The ID of the department.
        db (Session): Database session.

    Returns:
        str: The name of the department.
    """
    db = SessionLocal()
    department = db.query(Department).filter(Department.id == department_id).first()
    if department:
        return department.name
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Department with id {department_id} not found"
        )
