from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.exceptions import RequestValidationError
from app.api.v1.api import api_router
from app.core.config import settings
from app.services.redis_service import redis_service

app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter


@app.on_event("startup")
async def startup_event():
    await redis_service.connect()


@app.on_event("shutdown")
async def shutdown_event():
    await redis_service.disconnect()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")