"""
Main entry point for the AI-Smart-Career-Coach FastAPI application.

Initializes the FastAPI app with:
- Environment variable loading from .env
- CORS middleware configuration
- Exception handlers
- Route registration (blueprints)
- Health check endpoints
"""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes import health, users, assessments, recommendations, ai

# Load environment variables from .env file
load_dotenv()

# Environment configuration
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# CORS configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle management.
    Handles startup and shutdown events.
    """
    # Startup
    print(f"🚀 Starting AI-Smart-Career-Coach API in {ENVIRONMENT} mode")
    yield
    # Shutdown
    print("🛑 Shutting down API")


# Create FastAPI application
app = FastAPI(
    title="AI-Smart-Career-Coach API",
    description="Intelligent career coaching powered by AI",
    version="1.0.0",
    debug=DEBUG,
    lifespan=lifespan
)

# Configure CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected exceptions with proper error response."""
    print(f"❌ Exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if DEBUG else "An unexpected error occurred"
        }
    )


# Health check endpoints
@app.get("/ping")
async def ping():
    """
    Lightweight health check endpoint.
    Used by load balancers and monitoring services.
    """
    return {"status": "pong"}


@app.get("/")
async def root():
    """Root endpoint - API status and documentation links."""
    return {
        "service": "AI-Smart-Career-Coach API",
        "version": "1.0.0",
        "environment": ENVIRONMENT,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }


# Include route blueprints
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(assessments.router, prefix="/api/v1/assessments", tags=["assessments"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["recommendations"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=DEBUG,
        log_level="info"
    )
