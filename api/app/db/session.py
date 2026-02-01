import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings
from app.db.base import Base


def _ensure_db_path(sqlite_path: str) -> str:
    """Ensure database directory exists.

    Args:
        sqlite_path: SQLite file path.
    Returns:
        str: Normalized sqlite path.
    Side Effects:
        Creates directories on the filesystem.
    Raises:
        OSError: If directory creation fails.
    """

    directory = os.path.dirname(sqlite_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    return sqlite_path


def get_engine():
    """Create SQLAlchemy engine for SQLite.

    Args:
        None.
    Returns:
        Engine: SQLAlchemy engine instance.
    Side Effects:
        Creates database directory if needed.
    Raises:
        OSError: If directory creation fails.
    """

    settings = get_settings()
    sqlite_path = _ensure_db_path(settings.sqlite_path)
    url = f"sqlite:///{sqlite_path}"
    return create_engine(url, connect_args={"check_same_thread": False})


def init_db() -> None:
    """Initialize database schema.

    Args:
        None.
    Returns:
        None.
    Side Effects:
        Creates database tables if missing.
    Raises:
        SQLAlchemyError: If schema creation fails.
    """

    engine = get_engine()
    Base.metadata.create_all(bind=engine)


def get_session() -> Session:
    """Create a new SQLAlchemy session.

    Args:
        None.
    Returns:
        Session: Database session instance.
    Side Effects:
        Creates database directory if needed.
    Raises:
        OSError: If directory creation fails.
    """

    engine = get_engine()
    session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    return session_factory()
