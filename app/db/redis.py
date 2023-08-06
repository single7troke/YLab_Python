from aioredis.client import Redis
from core.config import Config

config = Config()

redis = Redis.from_url(config.redis.url())


def get_redis() -> Redis:
    return redis
