"""
Health check endpoints.

Simple endpoints to verify the API is running and healthy.
Useful for load balancers, monitoring, and deployment checks.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "service": "AI-Smart-Career-Coach API"
    }


@router.get("/live")
async def liveness_probe():
    """Kubernetes liveness probe endpoint."""
    return {"status": "alive"}


@router.get("/ready")
async def readiness_probe():
    """Kubernetes readiness probe endpoint."""
    return {"status": "ready"}
