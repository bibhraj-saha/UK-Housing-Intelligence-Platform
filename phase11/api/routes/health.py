from datetime import datetime

from fastapi import APIRouter

from phase11.config import settings


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
def health():
    return {
        "status": "healthy",
        "application": settings.app_name,
        "environment": settings.app_env,
        "timestamp": datetime.utcnow().isoformat(),
    }