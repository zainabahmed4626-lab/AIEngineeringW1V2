from __future__ import annotations

import structlog
from fastapi import APIRouter, HTTPException

from app.schemas import SummarizeRequest, SummarizeResponse
from app.services.summarize import _get_summary

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.post("/summarize", response_model=SummarizeResponse)
def summarize(body: SummarizeRequest) -> SummarizeResponse:
    try:
        summary = _get_summary(body.text, body.max_length)
        return SummarizeResponse(summary=summary)
    except Exception as exc:
        logger.exception("summarize_failed", error=str(exc))
        raise HTTPException(status_code=500, detail="Summarization failed") from exc
