from __future__ import annotations

import os
from typing import Any

from openai import OpenAI
from dotenv import load_dotenv

_DEFAULT_MODEL = "gpt-4.1-mini"


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


def _get_summary(text: str, max_length: int) -> str:
    """Generate concise summary text with an OpenAI model."""
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
                    "You are a concise summarization assistant. "
                    "Return only the summary text with no preamble."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Summarize the text entered in JSON in under {max_length} words. "
                    "Return only the summary, no extra commentary.\n\n"
                    f"Text:\n{text}"
                ),
            },
        ],
    )

    summary = _extract_text_from_response(response)
    if not summary:
        raise RuntimeError("No summary text returned from model")
    return summary
