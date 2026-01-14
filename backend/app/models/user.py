"""
User data models.

Includes Pydantic schemas for API requests/responses
and SQLAlchemy ORM model for database storage.
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# Pydantic models (API request/response schemas)
class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: EmailStr
    full_name: str
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(BaseModel):
    """Schema for returning user data in API responses."""
    id: int
    email: str
    full_name: str
    created_at: datetime

    class Config:
        from_attributes = True


# SQLAlchemy ORM model (uncomment when database is configured)
# from sqlalchemy import Column, Integer, String, DateTime
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
#
# class User(Base):
#     """User database model."""
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     full_name = Column(String)
#     hashed_password = Column(String)
#     created_at = Column(DateTime, default=datetime.utcnow)
