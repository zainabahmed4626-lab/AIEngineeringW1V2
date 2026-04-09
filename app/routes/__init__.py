from fastapi import APIRouter

from app.routes import health, sentiment, summarize

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(summarize.router, tags=["summarize"])
api_router.include_router(sentiment.router, tags=["sentiment"])
