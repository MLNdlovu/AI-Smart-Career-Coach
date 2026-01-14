"""
User service for managing user-related business logic.

Handles user creation, retrieval, updates, and authentication.
Acts as the business logic layer between routes and database.
"""

from typing import Optional
from app.models.user import UserCreate, UserUpdate


class UserService:
    """Service for user management operations."""

    def __init__(self):
        """Initialize the UserService."""
        # In production, initialize database session here
        self.users_db = {}  # Placeholder for in-memory storage

    def create_user(self, user_data: UserCreate) -> dict:
        """
        Create a new user.

        Args:
            user_data: UserCreate schema with email, full_name, password

        Returns:
            Created user object
        """
        # TODO: Hash password and save to database
        user = {
            "id": len(self.users_db) + 1,
            "email": user_data.email,
            "full_name": user_data.full_name
        }
        self.users_db[user["id"]] = user
        return user

    def get_user(self, user_id: int) -> Optional[dict]:
        """
        Retrieve user by ID.

        Args:
            user_id: User ID

        Returns:
            User object or None if not found
        """
        return self.users_db.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[dict]:
        """
        Retrieve user by email.

        Args:
            email: User email address

        Returns:
            User object or None if not found
        """
        for user in self.users_db.values():
            if user.get("email") == email:
                return user
        return None

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[dict]:
        """
        Update user information.

        Args:
            user_id: User ID
            user_data: UserUpdate schema with optional fields

        Returns:
            Updated user object or None if not found
        """
        user = self.users_db.get(user_id)
        if not user:
            return None

        if user_data.full_name:
            user["full_name"] = user_data.full_name
        if user_data.email:
            user["email"] = user_data.email

        return user

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user.

        Args:
            user_id: User ID

        Returns:
            True if deleted, False if not found
        """
        if user_id in self.users_db:
            del self.users_db[user_id]
            return True
        return False
