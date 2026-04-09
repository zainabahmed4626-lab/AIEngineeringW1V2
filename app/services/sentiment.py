from __future__ import annotations

from app.schemas.models import SentimentLabel, SentimentResponse


def _analyze_sentiment(text: str) -> SentimentResponse:
    """Placeholder heuristic; swap for a model or API as needed."""
    lower = text.lower()
    positive_hits = sum(1 for w in ("good", "great", "love", "excellent", "happy") if w in lower)
    negative_hits = sum(1 for w in ("bad", "hate", "awful", "terrible", "sad") if w in lower)

    if positive_hits > negative_hits:
        return SentimentResponse(
            sentiment=SentimentLabel.POSITIVE,
            confidence=0.75,
            explanation="More positive cue words than negative (placeholder).",
        )
    if negative_hits > positive_hits:
        return SentimentResponse(
            sentiment=SentimentLabel.NEGATIVE,
            confidence=0.75,
            explanation="More negative cue words than positive (placeholder).",
        )
    return SentimentResponse(
        sentiment=SentimentLabel.NEUTRAL,
        confidence=0.5,
        explanation="No strong positive/negative cues (placeholder).",
    )
