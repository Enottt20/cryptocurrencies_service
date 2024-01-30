import json

import uvicorn

import config
import logging
import asyncio
from fastapi import FastAPI
import broker, schemas
from app.api.v1.crud import update_courses
from app.api.v1.api import api_router


# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=2,
    format="%(levelname)-9s %(message)s"
)

app = FastAPI()

# load config
cfg: config.Config = config.load_config()

logger.info(
    'Service configuration loaded:\n' +
    f'{cfg.json()}'
)

ed: schemas.ExchangeData = None


async def consumer_coingeko_service():
    consumer = broker.Consumer(str(cfg.RABBITMQ_DSN), cfg.QUEUE_COINGEKO_NAME)
    consumer.add_callback(receiving_data_coingeko_service)
    await consumer.run()


async def consumer_binance_service():
    consumer = broker.Consumer(str(cfg.RABBITMQ_DSN), cfg.QUEUE_BINANCE_NAME)
    consumer.add_callback(receiving_data_binance_service)
    await consumer.run()


async def receiving_data_binance_service(data):
    data = json.loads(data)
    data = schemas.ExchangeData(**data)
    await update_courses(ed, data)


async def receiving_data_coingeko_service(data):
    data = json.loads(data)
    data = schemas.ExchangeData(**data)
    await update_courses(ed, data)

app.include_router(api_router, prefix='/pref')


async def main():
    # Запускаем оба консьюмера асинхронно
    await asyncio.gather(consumer_binance_service(), consumer_coingeko_service())


if __name__ == "__main__":
    # Запускаем FastAPI приложение
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

    # Запускаем основную асинхронную программу
    asyncio.run(main())