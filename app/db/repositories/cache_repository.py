from aioredis.client import Redis
from core.config import Config
from db.redis import get_redis
from fastapi import Depends

config = Config()


class CacheRepository:
    def __init__(self, client: Redis = Depends(get_redis)):
        self.redis = client

    async def get(self, key: str) -> bytes:
        response = await self.redis.get(name=key)
        return response

    async def set(self, key: str, value) -> bool:
        response = await self.redis.set(name=key, value=value, ex=config.redis.expire)
        return response

    async def delete(self, key: str) -> bool:
        response = await self.redis.delete(key)
        return response
