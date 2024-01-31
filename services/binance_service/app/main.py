import asyncio

from api.v1.binance_api import run_binance_subscription
from typing import List
from schemas import ExchangeData, Course
import json
import logging
import config
from broker.producer import MessageProducer


# # setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=2,
    format="%(levelname)-9s %(message)s"
)

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


def fix_usdt(course):
    if 'USDT' in course.direction:
        course.direction = course.direction.replace('USDT', 'USD')
    return course

def format_currency_pair(course):
    course.direction = f"{course.direction[:3]}-{course.direction[3:]}"
    return course


# def convert_currencies_to_rub(input_data: List[Course], rub_to_usdt):
#     result_data = []
#
#     for item in input_data:
#         item = Course(**item)
#         if 'USDT' in item.direction:
#             direction = item.direction.replace('USDT', 'RUB')
#             value_in_rub = float(item.value) * rub_to_usdt
#             result_data.append(format_currency_pair(fix_usdt(Course(direction=direction, value=value_in_rub))))
#
#     return result_data



subscription_params = [
        "btcusdt@kline_1s",
        "ethusdt@kline_1s",
        "usdtrub@kline_1s",
        "btctrub@kline_1s",
        "ethtrub@kline_1s",
    ]

async def f(msg):
    b = [format_currency_pair(fix_usdt(Course(**item))) for item in msg]
    # a = convert_currencies_to_rub(msg, 100)
    b.append(Course(direction='USDT-USD', value=1.0))
    d = transform_data(b, 'Binance')
    #print(d)
    await message_producer.send_message(d)

run_binance_subscription(subscription_params, f)
