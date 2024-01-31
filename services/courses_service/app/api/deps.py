import aioredis
from aioredis import Redis
from fastapi import Depends

from app import config

cfg: config.Config = config.load_config()


async def connect_to_redis():
    return await aioredis.create_redis_pool(cfg.REDIS_URL)