import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as feedback_router
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.db.session import init_db

setup_logging()
logger = logging.getLogger("main")
settings = get_settings()

app = FastAPI(title=settings.app_name)

if settings.allowed_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["POST", "GET"],
        allow_headers=["*"],
    )


@app.on_event("startup")
def on_startup() -> None:
    """Initialize application resources.

    Args:
        None.
    Returns:
        None.
    Side Effects:
        Initializes database schema.
    Raises:
        SQLAlchemyError: If schema creation fails.
    """

    init_db()
    logger.info("Database initialized.")


@app.get("/health")
def health() -> dict:
    """Health check endpoint.

    Args:
        None.
    Returns:
        dict: Health status payload.
    Side Effects:
        None.
    Raises:
        None.
    """

    return {"status": "ok"}


app.include_router(feedback_router, prefix="/api")
