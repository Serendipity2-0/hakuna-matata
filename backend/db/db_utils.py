from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey, Table
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import os

DATABASE_URL = "sqlite:///rbac_system.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
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


# Create the tables and initialize super admin
Base.metadata.create_all(bind=engine)