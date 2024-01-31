from api.v1.coingeko_api import start_coingeko_service
from typing import List
from schemas import ExchangeData, Course
import logging
import config
from broker.producer import MessageProducer

# setup logging
logger = logging.getLogger(__name__)

#load config
cfg: config.Config = config.load_config()

logger.info(
    'Service configuration loaded:\n' +
    f'{cfg.json()}'
)

message_producer = MessageProducer(
    dsn=cfg.RABBITMQ_DSN.unicode_string(),
    exchange_name='notification',
    queue_name=cfg.QUEUE_COINGEKO_NAME,
)

async def f(msg):
    await message_producer.send_message(msg)

start_coingeko_service(f)
