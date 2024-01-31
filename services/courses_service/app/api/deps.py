import aioredis
from aioredis import Redis
from fastapi import Depends


async def connect_to_redis():
    return await aioredis.create_redis_pool('redis://localhost')