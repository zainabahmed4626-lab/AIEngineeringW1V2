from __future__ import annotations

import json
import os
import re
from typing import Any

from openai import OpenAI
from dotenv import load_dotenv

from app.schemas.models import SentimentLabel, SentimentResponse

_DEFAULT_MODEL = "gpt-4.1-mini"


def _normalize_sentiment_label(value: str) -> SentimentLabel:
    """Map common model sentiment variants to supported labels."""
    normalized = re.sub(r"[^a-z]+", "_", value.strip().lower()).strip("_")
    if not normalized:
        raise RuntimeError("Invalid sentiment label returned by model")

    if normalized in {"positive", "pos", "somewhat_positive", "very_positive"}:
        return SentimentLabel.POSITIVE
    if normalized in {"negative", "neg", "somewhat_negative", "very_negative"}:
        return SentimentLabel.NEGATIVE
    if normalized in {"neutral", "mixed", "mixed_sentiment", "balanced"}:
        return SentimentLabel.NEUTRAL

    if "positive" in normalized:
        return SentimentLabel.POSITIVE
    if "negative" in normalized:
        return SentimentLabel.NEGATIVE
    if "neutral" in normalized or "mixed" in normalized:
        return SentimentLabel.NEUTRAL

    raise RuntimeError("Invalid sentiment label returned by model")


def _extract_text_from_response(response: Any) -> str:
    """Extract assistant text from OpenAI responses API output."""
    output = getattr(response, "output", None) or []
    chunks: list[str] = []

    for item in output:
        if getattr(item, "type", None) != "message":
            continue
        for content_part in getattr(item, "content", None) or []:
            if getattr(content_part, "type", None) == "output_text":
                text = getattr(content_part, "text", "")
                if text:
                    chunks.append(text)

    return "\n".join(chunks).strip()


def _parse_sentiment_response(raw_text: str) -> SentimentResponse:
    """Parse and validate model JSON output."""
    candidate = raw_text.strip()
    if candidate.startswith("```"):
        candidate = re.sub(r"^```(?:json)?\s*", "", candidate, flags=re.IGNORECASE)
        candidate = re.sub(r"\s*```$", "", candidate)

    # If extra text is present, recover the first JSON object.
    if "{" in candidate and "}" in candidate:
        first = candidate.find("{")
        last = candidate.rfind("}")
        candidate = candidate[first : last + 1]

    try:
        payload = json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Model did not return valid JSON for sentiment output") from exc

    if not isinstance(payload, dict):
        raise RuntimeError("Model response must be a JSON object")

    sentiment_raw = str(payload.get("sentiment", ""))
    sentiment = _normalize_sentiment_label(sentiment_raw)

    confidence_raw = payload.get("confidence")
    try:
        confidence = float(confidence_raw)
    except (TypeError, ValueError) as exc:
        raise RuntimeError("Invalid confidence value returned by model") from exc

    if confidence < 0.0 or confidence > 1.0:
        raise RuntimeError("Confidence must be between 0.0 and 1.0")

    explanation_raw = payload.get("explanation")
    if not isinstance(explanation_raw, str) or not explanation_raw.strip():
        raise RuntimeError("Explanation must be a non-empty string")

    return SentimentResponse(
        sentiment=sentiment,
        confidence=confidence,
        explanation=explanation_raw.strip(),
    )


def _analyze_sentiment(text: str) -> SentimentResponse:
    """Analyze sentiment with OpenAI and return strict JSON fields."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    model = os.getenv("OPENAI_MODEL", _DEFAULT_MODEL)
    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model=model,
        temperature=0,
        input=[
            {
                "role": "system",
                "content": (
                    "You are a senior developer sentiment analysis assistant. "
                    "Analyze sentiment and respond with strict JSON only."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Analyze the sentiment of the text entered in JSON. "
                    "Respond only in JSON with keys: sentiment, confidence, explanation. "
                    "The sentiment value must be exactly one of: positive, negative, neutral. "
                    "No extra text.\n\n"
                    f"Text:\n{text}"
                ),
            },
        ],
    )

    raw_output = _extract_text_from_response(response)
    if not raw_output:
        raise RuntimeError("No sentiment analysis returned from model")

    return _parse_sentiment_response(raw_output)
