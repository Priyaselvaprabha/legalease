from typing import Optional

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)


class ExplainRequest(BaseModel):
    text: str = Field(..., min_length=1)


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=1)


class GenerateRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    details: Optional[str] = ""


class AIResponse(BaseModel):
    success: bool
    answer: str


class HealthResponse(BaseModel):
    status: str
    service: str
    gemini_configured: bool
    model: str