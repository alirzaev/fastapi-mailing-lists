import aioredis

from application.core.config import config

redis_client = aioredis.from_url(config.REDIS_URL)
