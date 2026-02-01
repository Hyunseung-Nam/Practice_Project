import logging

from app.core.config import get_settings


def setup_logging() -> None:
    """Configure application logging.

    Args:
        None.
    Returns:
        None.
    Side Effects:
        Sets global logging configuration.
    Raises:
        None.
    """

    settings = get_settings()
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
