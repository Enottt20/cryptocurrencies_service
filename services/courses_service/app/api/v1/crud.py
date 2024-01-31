import logging
from typing import Optional

from fastapi import HTTPException, Depends

from app.schemas import ExchangeData
from aioredis import Redis
from app.schemas import ExchangeData
from app.api.deps import connect_to_redis

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z')
logger = logging.getLogger(__name__)


def filter_courses_by_pair(data: ExchangeData, currency_pair: str) -> ExchangeData:
    if currency_pair:
        filtered_courses = [course for course in data.courses if course.direction == currency_pair]
        return ExchangeData(exchanger=data.exchanger, courses=filtered_courses)
    else:
        return data


async def get_courses(redis: Redis, currency_pair: Optional[str] = None) -> ExchangeData:
    data = await redis.get('courses')
    if data:
        data_str = data.decode('utf-8')  # Декодируем байты в строку
        exchange_data = ExchangeData.parse_raw(data_str)
        if currency_pair:
            return filter_courses_by_pair(exchange_data, currency_pair)
        else:
            return exchange_data
    else:
        raise HTTPException(status_code=404, detail="Exchange data not found")



async def update_courses(data: ExchangeData, redis: Redis):
    try:
        await redis.set('courses', data.json())
    except Exception as e:
        logger.error(e)
