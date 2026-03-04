from fastapi import APIRouter
from pydantic import BaseModel
from app.services.redis_service import redis_service
from app.core.config import settings
import httpx

router = APIRouter()


class HealthStatus(BaseModel):
    status: str
    redis: bool
    ollama: bool


@router.get("/health", response_model=HealthStatus)
async def health_check():
    redis_status = await redis_service.check_health()
    
    ollama_status = False
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.OLLAMA_HOST}/api/tags", timeout=5.0)
            ollama_status = response.status_code == 200
    except Exception:
        ollama_status = False
    
    overall_status = "healthy" if redis_status and ollama_status else "degraded"
    
    return HealthStatus(
        status=overall_status,
        redis=redis_status,
        ollama=ollama_status,
    )
