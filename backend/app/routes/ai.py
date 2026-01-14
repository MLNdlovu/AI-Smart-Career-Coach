"""
AI/LLM endpoints for testing and using the language model.

Provides endpoints for:
- Testing LLM connectivity
- Career analysis
- Interview preparation
- Learning path generation
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

from app.services.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()


# Request/Response schemas
class TestPromptRequest(BaseModel):
    """Request schema for testing LLM with a custom prompt."""
    prompt: str
    system_prompt: Optional[str] = None


class CareerAnalysisRequest(BaseModel):
    """Request schema for career profile analysis."""
    skills: List[str]
    experience_years: int
    goals: str


class InterviewPrepRequest(BaseModel):
    """Request schema for interview question generation."""
    role: str
    level: str  # junior, mid, senior


class LearningPathRequest(BaseModel):
    """Request schema for learning path generation."""
    current_skills: List[str]
    target_role: str


@router.post("/test")
async def test_llm(request: TestPromptRequest):
    """
    Test endpoint for LLM connectivity.

    Sends a prompt to the LLM and returns the response.
    Useful for testing API configuration and credentials.

    Args:
        request: Contains prompt and optional system_prompt

    Returns:
        LLM response with token usage
    """
    try:
        result = llm_service.generate_response(
            prompt=request.prompt,
            system_prompt=request.system_prompt
        )

        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"LLM Error: {result['error']}"
            )

        return {
            "status": "success",
            "data": result
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@router.post("/analyze-career")
async def analyze_career(request: CareerAnalysisRequest):
    """
    Analyze a user's career profile and generate insights.

    Provides:
    - Skill gap analysis
    - Career recommendations
    - Next steps

    Args:
        request: Career profile data (skills, experience, goals)

    Returns:
        AI-generated career analysis
    """
    try:
        result = llm_service.analyze_career_profile(
            skills=request.skills,
            experience_years=request.experience_years,
            goals=request.goals
        )

        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Analysis failed: {result['error']}"
            )

        return {
            "status": "success",
            "analysis": result["response"],
            "tokens_used": result["tokens"]["total"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Career analysis error: {str(e)}"
        )


@router.post("/interview-prep")
async def generate_interview_questions(request: InterviewPrepRequest):
    """
    Generate interview preparation questions.

    Creates realistic interview questions for interview preparation.

    Args:
        request: Role and experience level

    Returns:
        AI-generated interview questions
    """
    try:
        # Validate level
        valid_levels = ["junior", "mid", "senior"]
        if request.level.lower() not in valid_levels:
            raise ValueError(f"Level must be one of: {', '.join(valid_levels)}")

        result = llm_service.generate_interview_questions(
            role=request.role,
            level=request.level
        )

        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Interview prep failed: {result['error']}"
            )

        return {
            "status": "success",
            "role": request.role,
            "level": request.level,
            "questions": result["response"],
            "tokens_used": result["tokens"]["total"]
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Interview prep error: {str(e)}"
        )


@router.post("/learning-path")
async def generate_learning_path(request: LearningPathRequest):
    """
    Generate a personalized learning path.

    Creates a structured learning plan with milestones and resources.

    Args:
        request: Current skills and target role

    Returns:
        AI-generated learning path with milestones
    """
    try:
        result = llm_service.create_learning_path(
            current_skills=request.current_skills,
            target_role=request.target_role
        )

        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Learning path generation failed: {result['error']}"
            )

        return {
            "status": "success",
            "target_role": request.target_role,
            "learning_path": result["response"],
            "tokens_used": result["tokens"]["total"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Learning path error: {str(e)}"
        )


@router.get("/status")
async def llm_status():
    """
    Check LLM service status.

    Returns whether the LLM service is configured and ready.
    """
    return {
        "service": "LLM Service",
        "status": "connected" if llm_service.client else "not_configured",
        "model": llm_service.model,
        "temperature": llm_service.temperature,
        "max_tokens": llm_service.max_tokens,
        "message": "✅ Ready to process requests" if llm_service.client else "⚠️ API key not configured"
    }
