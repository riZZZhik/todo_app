"""This module is responsible for creating the API routes."""

from fastapi import APIRouter

from . import tasks

router = APIRouter()
router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])


@router.get("/health", name="health:check")
def health_check() -> dict[str, str]:
    """Check the health of the application."""
    return {"status": "ok"}
