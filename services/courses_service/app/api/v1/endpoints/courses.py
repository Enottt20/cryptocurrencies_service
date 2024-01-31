from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Any, Optional
from app.api.deps import connect_to_redis


from app.api.v1.crud import get_courses
from app.schemas import ExchangeData, Course

router = APIRouter()


@router.get("/courses/", status_code=200)
async def read_courses(redis: Redis = Depends(connect_to_redis)) -> ExchangeData:
    return await get_courses(redis)
