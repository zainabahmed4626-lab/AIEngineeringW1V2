from __future__ import annotations

import logging
import sys

import structlog
from fastapi import FastAPI

from app.routes import api_router


def configure_logging() -> None:
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title="Summarize & Sentiment API")
    app.include_router(api_router)
    return app


app = create_app()
