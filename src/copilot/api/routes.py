from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from copilot.api.schemas import HealthResponse
from copilot.config import get_settings
from copilot.db.session import get_db_session

router = APIRouter()
settings = get_settings()


@router.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check(
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> HealthResponse:
    """System health check endpoint verifying database connectivity."""
    db_status = "connected"
    try:
        await db.execute(text("SELECT 1"))
    except (SQLAlchemyError, OSError) as e:
        db_status = f"unreachable ({e.__class__.__name__})"

    return HealthResponse(
        status="healthy" if db_status == "connected" else "degraded",
        database=db_status,
        environment=settings.app_env,
        version="0.1.0",
    )
