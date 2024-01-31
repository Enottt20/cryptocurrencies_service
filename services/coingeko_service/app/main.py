from api.v1.coingeko_api import start_coingeko_service
import logging
import config
from broker.producer import MessageProducer

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z')
logger = logging.getLogger(__name__)


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

async def send_data(msg):
    await message_producer.send_message(msg)

start_coingeko_service(send_data)
