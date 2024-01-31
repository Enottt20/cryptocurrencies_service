import asyncio
from api.v1.binance_api import run_binance_subscription
from typing import List
from schemas import ExchangeData, Course
import json
import logging
import config
from broker.producer import MessageProducer


# # setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z')
logger = logging.getLogger(__name__)

# #load config
cfg: config.Config = config.load_config()

logger.info(
    'Service configuration loaded:\n' +
    f'{cfg.json()}'
)

message_producer = MessageProducer(
    dsn=cfg.RABBITMQ_DSN.unicode_string(),
    exchange_name='notification',
    queue_name=cfg.QUEUE_BINANCE_NAME,
)


def transform_data(input_data: List[Course], exchange_name):
    exchange_data = ExchangeData(exchanger=exchange_name, courses=[item for item in input_data])
    return json.dumps(exchange_data.dict(), indent=2)


def usdt_to_usd(course):
    if 'USDT' in course.direction:
        course.direction = course.direction.replace('USDT', 'USD')
    return course


def format_currency_pair(course):
    course.direction = f"{course.direction[:3]}-{course.direction[3:]}"
    return course


subscription_params = [
        "btcusdt@kline_1s",
        "ethusdt@kline_1s",
        "usdtrub@kline_1s",
        "btctrub@kline_1s",
        "ethtrub@kline_1s",
    ]


async def send_data(msg):
    data = [format_currency_pair(usdt_to_usd(Course(**item))) for item in msg]
    data.append(Course(direction='USDT-USD', value=1.0))
    data = transform_data(data, 'Binance')
    logger.info(data)
    await message_producer.send_message(data)

run_binance_subscription(subscription_params, send_data)
