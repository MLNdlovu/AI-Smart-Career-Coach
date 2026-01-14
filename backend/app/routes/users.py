"""
User management endpoints.

Handles user registration, profile retrieval, and updates.
Delegates business logic to the UserService.
"""

from fastapi import APIRouter, HTTPException, status
from app.models.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter()
user_service = UserService()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    """Register a new user."""
    existing_user = user_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return user_service.create_user(user_data)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Retrieve user by ID."""
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdate):
    """Update user information."""
    user = user_service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
