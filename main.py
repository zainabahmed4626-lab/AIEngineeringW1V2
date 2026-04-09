"""Entrypoint for hosts that run `uvicorn main:app` (e.g. Render default)."""

from app.main import app

__all__ = ["app"]
