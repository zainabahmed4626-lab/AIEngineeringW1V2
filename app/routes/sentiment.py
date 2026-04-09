from __future__ import annotations

import structlog
from fastapi import APIRouter, HTTPException

from app.schemas import SentimentRequest, SentimentResponse
from app.services.sentiment import _analyze_sentiment

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.post("/analyze-sentiment", response_model=SentimentResponse)
def analyze_sentiment(body: SentimentRequest) -> SentimentResponse:
    try:
        return _analyze_sentiment(body.text)
    except Exception as exc:
        logger.exception("sentiment_failed", error=str(exc))
        raise HTTPException(status_code=500, detail="Sentiment analysis failed") from exc
