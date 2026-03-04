import redis
import json
from typing import Any, Optional
from app.core.config import settings


class RedisService:
    def __init__(self):
        self.client: Optional[redis.Redis] = None

    async def connect(self):
        try:
            self.client = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
            )
            self.client.ping()
        except Exception as e:
            raise Exception(f"Failed to connect to Redis: {e}")

    async def disconnect(self):
        if self.client:
            self.client.close()

    async def get(self, key: str) -> Optional[Any]:
        if not self.client:
            return None
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            raise Exception(f"Error getting key {key}: {e}")

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        if not self.client:
            return False
        try:
            serialized_value = json.dumps(value)
            if ttl:
                self.client.setex(key, ttl, serialized_value)
            else:
                self.client.set(key, serialized_value)
            return True
        except Exception as e:
            raise Exception(f"Error setting key {key}: {e}")

    async def delete(self, key: str) -> bool:
        if not self.client:
            return False
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            raise Exception(f"Error deleting key {key}: {e}")

    async def incr(self, key: str, amount: int = 1) -> int:
        if not self.client:
            return 0
        try:
            return self.client.incrby(key, amount)
        except Exception as e:
            raise Exception(f"Error incrementing key {key}: {e}")

    async def check_health(self) -> bool:
        if not self.client:
            return False
        try:
            self.client.ping()
            return True
        except Exception:
            return False


redis_service = RedisService()
