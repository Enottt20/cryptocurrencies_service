from fastapi import HTTPException, Depends

from app.schemas import ExchangeData
from aioredis import Redis
from app.schemas import ExchangeData
from app.api.deps import connect_to_redis


async def get_courses(redis: Redis) -> ExchangeData:
    data = await redis.get('courses')
    if data:
        return ExchangeData.parse_raw(data)
    else:
        raise HTTPException(status_code=404, detail="Exchange data not found")


async def update_courses(data: ExchangeData, redis: Redis):
    try:
        await redis.set('courses', data.json())
        print('Данные о курсах успешно обновлены')
    except Exception as e:
        print(e)
