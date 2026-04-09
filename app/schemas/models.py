from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    timestamp: str


class SummarizeRequest(BaseModel):
    text: str = Field(min_length=1)
    max_length: int = Field(gt=0)


class SummarizeResponse(BaseModel):
    summary: str


class SentimentLabel(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class SentimentRequest(BaseModel):
    text: str = Field(min_length=1)


class SentimentResponse(BaseModel):
    sentiment: SentimentLabel
    confidence: float = Field(ge=0.0, le=1.0)
    explanation: str
