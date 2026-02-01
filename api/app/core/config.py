import os
from dataclasses import dataclass


def _split_csv(value: str) -> list[str]:
    """Split a CSV string into a list.

    Args:
        value: Raw CSV string.
    Returns:
        list[str]: Parsed list of values.
    Side Effects:
        None.
    Raises:
        None.
    """

    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    """Application settings container.

    역할 설명:
        환경 변수 기반 설정 값을 보관한다.
    책임 범위:
        설정 값의 구조와 타입을 정의한다.
    외부 의존성:
        없음.
    """

    app_name: str
    log_level: str
    sqlite_path: str
    allowed_origins: list[str]
    rate_limit_per_minute: int
    notify_mode: str
    webhook_url: str | None


def get_settings() -> Settings:
    """Load settings from environment variables with defaults.

    Args:
        None.
    Returns:
        Settings: Loaded settings object.
    Side Effects:
        Reads environment variables.
    Raises:
        None.
    """

    rate_limit_raw = os.getenv("RATE_LIMIT_PER_MINUTE", "30")
    try:
        rate_limit = max(1, int(rate_limit_raw))
    except ValueError:
        rate_limit = 30

    allowed_origins = _split_csv(os.getenv("ALLOWED_ORIGINS", ""))

    return Settings(
        app_name=os.getenv("APP_NAME", "Practice Feedback API"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        sqlite_path=os.getenv("SQLITE_PATH", "./data/feedback.db"),
        allowed_origins=allowed_origins,
        rate_limit_per_minute=rate_limit,
        notify_mode=os.getenv("NOTIFY_MODE", "console").lower(),
        webhook_url=os.getenv("WEBHOOK_URL"),
    )
