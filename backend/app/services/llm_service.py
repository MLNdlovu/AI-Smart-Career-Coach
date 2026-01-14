"""
LLM (Language Model) service for AI interactions.

Handles connections to OpenAI API or other LLM providers.
Manages prompt engineering, token counting, and response parsing.
"""

import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class LLMService:
    """Service for interacting with Language Models (LLMs)."""

    def __init__(self):
        """Initialize LLM Service with API key from environment."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", "500"))

        if not self.api_key:
            logger.warning("⚠️ OPENAI_API_KEY not found in environment variables")
            self.client = None
        else:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
                logger.info(f"✅ LLM Service initialized with model: {self.model}")
            except ImportError:
                logger.error("❌ OpenAI library not installed. Run: pip install openai")
                self.client = None

    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> dict:
        """
        Generate a response from the LLM.

        Args:
            prompt: User prompt/question
            system_prompt: Optional system context for the model

        Returns:
            Dictionary with response, tokens used, and metadata

        Raises:
            ValueError: If API key not configured
            Exception: If API call fails
        """
        if not self.client:
            raise ValueError(
                "LLM Service not properly initialized. "
                "Ensure OPENAI_API_KEY is set in environment variables."
            )

        try:
            messages = []

            # Add system prompt if provided
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            # Add user prompt
            messages.append({"role": "user", "content": prompt})

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            # Extract response content
            content = response.choices[0].message.content

            logger.info(f"✅ LLM response generated ({response.usage.total_tokens} tokens)")

            return {
                "success": True,
                "response": content,
                "tokens": {
                    "prompt": response.usage.prompt_tokens,
                    "completion": response.usage.completion_tokens,
                    "total": response.usage.total_tokens
                },
                "model": self.model
            }

        except Exception as e:
            logger.error(f"❌ LLM API Error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "response": None
            }

    def analyze_career_profile(self, skills: list, experience_years: int, goals: str) -> dict:
        """
        Analyze a career profile and provide AI-powered insights.

        Args:
            skills: List of user skills
            experience_years: Years of experience
            goals: Career goals description

        Returns:
            Career analysis and recommendations
        """
        skills_text = ", ".join(skills) if skills else "None provided"

        system_prompt = (
            "You are an expert career coach with deep knowledge of industry trends, "
            "skills development, and career progression. Provide actionable insights."
        )

        prompt = f"""
        Please analyze this career profile and provide insights:

        Skills: {skills_text}
        Experience: {experience_years} years
        Goals: {goals}

        Provide:
        1. Skill gap analysis
        2. Career path recommendations
        3. Top 3 actionable next steps
        """

        return self.generate_response(prompt, system_prompt)

    def generate_interview_questions(self, role: str, level: str) -> dict:
        """
        Generate interview preparation questions for a specific role.

        Args:
            role: Job title/role
            level: Experience level (junior/mid/senior)

        Returns:
            List of interview questions
        """
        system_prompt = (
            "You are an experienced recruiter and technical interviewer. "
            "Generate thoughtful, realistic interview questions."
        )

        prompt = f"""
        Generate 5 interview questions for a {level}-level {role} position.
        Include a mix of technical and behavioral questions.
        Format each question clearly.
        """

        return self.generate_response(prompt, system_prompt)

    def create_learning_path(self, current_skills: list, target_role: str) -> dict:
        """
        Create a personalized learning path to reach a target role.

        Args:
            current_skills: Current skill set
            target_role: Target job role

        Returns:
            Structured learning path with milestones
        """
        skills_text = ", ".join(current_skills) if current_skills else "None"

        system_prompt = (
            "You are a learning and development specialist. "
            "Create structured, achievable learning paths with concrete milestones."
        )

        prompt = f"""
        Create a learning path from current skills to target role:

        Current Skills: {skills_text}
        Target Role: {target_role}

        Provide:
        1. Skills gap analysis
        2. Learning milestones (with timeframes)
        3. Recommended resources/courses
        4. Success metrics
        """

        return self.generate_response(prompt, system_prompt)
