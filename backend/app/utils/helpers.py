"""
Helper utilities for common operations.

Provides utility functions for logging, error handling, data transformation,
and other frequently used operations.
"""

import logging
from datetime import datetime
from typing import Any, Dict


# Configure logger
logger = logging.getLogger(__name__)


def format_response(data: Any, message: str = None, success: bool = True) -> Dict:
    """
    Format API response in a standard structure.

    Args:
        data: Response data
        message: Optional message
        success: Whether the operation was successful

    Returns:
        Formatted response dictionary
    """
    return {
        "success": success,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }


def log_operation(operation: str, user_id: int = None, details: str = None):
    """
    Log an operation for auditing and debugging.

    Args:
        operation: Operation name
        user_id: User ID if applicable
        details: Additional details
    """
    log_msg = f"Operation: {operation}"
    if user_id:
        log_msg += f" | User ID: {user_id}"
    if details:
        log_msg += f" | Details: {details}"
    logger.info(log_msg)


def calculate_match_score(profile1: Dict, profile2: Dict) -> float:
    """
    Calculate similarity score between two profiles.

    Args:
        profile1: First profile
        profile2: Second profile

    Returns:
        Match score between 0 and 1
    """
    # TODO: Implement similarity calculation (cosine similarity, etc.)
    return 0.0
