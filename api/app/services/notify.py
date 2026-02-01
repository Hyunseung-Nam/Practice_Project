import json
import logging
import urllib.request

from app.core.config import get_settings

logger = logging.getLogger("notify")


def notify_feedback(payload: dict) -> None:
    """Send feedback notification to console or webhook.

    Args:
        payload: Feedback data payload.
    Returns:
        None.
    Side Effects:
        Logs or sends a webhook request.
    Raises:
        None. (Errors are logged internally.)
    """

    settings = get_settings()
    if settings.notify_mode == "console":
        logger.info("New feedback: %s", payload)
        return

    if settings.notify_mode != "webhook":
        return

    if not settings.webhook_url:
        logger.warning("WEBHOOK_URL is not set. Skipping webhook notification.")
        return

    try:
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            settings.webhook_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=5):
            logger.info("Webhook notification sent.")
    except Exception:
        logger.exception("Failed to send webhook notification.")
