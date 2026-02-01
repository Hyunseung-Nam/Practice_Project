import logging

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.exc import SQLAlchemyError

from app.core.rate_limit import enforce_rate_limit
from app.db.models import FeedbackEntry
from app.db.session import get_session
from app.services.notify import notify_feedback

logger = logging.getLogger("api")

router = APIRouter()


class FeedbackCreate(BaseModel):
    """Feedback creation payload model.

    역할 설명:
        API 요청 바디의 유효성을 검증한다.
    책임 범위:
        입력 필드 타입 및 제약을 정의한다.
    외부 의존성:
        Pydantic BaseModel.
    """

    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str = Field(..., min_length=1, max_length=50)
    organization: str | None = Field(None, max_length=200)
    message: str = Field(..., min_length=10)
    source_url: str | None = Field(None, max_length=500)


@router.post("/feedback")
def create_feedback(payload: FeedbackCreate, request: Request) -> dict:
    """Create a new feedback entry.

    Args:
        payload: Feedback creation request body.
        request: Incoming HTTP request.
    Returns:
        dict: Result payload containing status and id.
    Side Effects:
        Writes to the database and optionally sends notification.
    Raises:
        HTTPException: When validation fails or an error occurs.
    """

    enforce_rate_limit(request)

    session = get_session()
    try:
        entry = FeedbackEntry(
            name=payload.name,
            email=str(payload.email) if payload.email else None,
            phone=payload.phone,
            organization=payload.organization,
            message=payload.message,
            source_url=payload.source_url,
        )
        session.add(entry)
        session.commit()
        session.refresh(entry)

        notify_feedback(
            {
                "id": entry.id,
                "name": entry.name,
                "email": entry.email,
                "phone": entry.phone,
                "organization": entry.organization,
                "message": entry.message,
                "source_url": entry.source_url,
            }
        )
        return {"status": "ok", "id": entry.id}
    except SQLAlchemyError:
        session.rollback()
        logger.exception("Database error while creating feedback.")
        raise HTTPException(status_code=500, detail="요청 처리 중 오류가 발생했습니다.")
    except Exception:
        session.rollback()
        logger.exception("Unexpected error while creating feedback.")
        raise HTTPException(status_code=500, detail="요청 처리 중 오류가 발생했습니다.")
    finally:
        session.close()
