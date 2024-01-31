import json
import logging
import uvicorn
import asyncio
from fastapi import FastAPI
import broker
import config
import schemas
from app.api.v1.api import api_router_v1
from app.api.v1.crud import update_courses
from contextlib import asynccontextmanager
from app.api.deps import connect_to_redis

# setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z')
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(consumer_coingeko_service())
    asyncio.create_task(consumer_binance_service())
    yield


app = FastAPI(lifespan=lifespan)

# load config
cfg: config.Config = config.load_config()

logger.info(
    'Service configuration loaded:\n' +
    f'{cfg.json()}'
)


async def consumer_coingeko_service():
    consumer = broker.Consumer(str(cfg.RABBITMQ_DSN), cfg.QUEUE_COINGEKO_NAME)
    consumer.add_callback(receiving_data_coingeko_service)
    print('consumer_coingeko_service')
    await consumer.run()


async def consumer_binance_service():
    consumer = broker.Consumer(str(cfg.RABBITMQ_DSN), cfg.QUEUE_BINANCE_NAME)
    consumer.add_callback(receiving_data_binance_service)
    print('consumer_binance_service')
    await consumer.run()


async def receiving_data_binance_service(data):
    data = json.loads(data)
    data = schemas.ExchangeData(**data)
    redis = await connect_to_redis()
    await update_courses(data, redis)


async def receiving_data_coingeko_service(data):
    data = json.loads(data)
    data = schemas.ExchangeData(**data)
    redis = await connect_to_redis()
    await update_courses(data, redis)


app.include_router(api_router_v1, prefix='/api/v1')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5002, log_level="info")
