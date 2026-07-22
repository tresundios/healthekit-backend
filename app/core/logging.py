import logging
import structlog
from app.core.config import settings


def configure_logging() -> None:
    logging.basicConfig(level=settings.LOG_LEVEL)
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer(),
        ]
    )
