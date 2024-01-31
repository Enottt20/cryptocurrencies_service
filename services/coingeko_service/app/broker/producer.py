import logging
import aio_pika

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z')
logger = logging.getLogger(__name__)


class MessageProducer():
    def __init__(self, dsn, queue_name="notification", exchange_name="notification"):
        self.dsn = dsn
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.exchange = None
        self.queue = None

    async def connect(self):
        connection = await aio_pika.connect_robust(self.dsn)
        channel = await connection.channel()
        self.exchange = await channel.declare_exchange(self.exchange_name, aio_pika.ExchangeType.DIRECT, durable=True)
        queue_arguments = {
            "x-max-length": 1,
            "x-overflow": "drop-head"
        }
        self.queue = await channel.declare_queue(self.queue_name, durable=True, arguments=queue_arguments)
        await self.queue.bind(self.exchange)


    async def send_message(self, message):
        if self.exchange is None:
            await self.connect()

        message_body = message
        message = aio_pika.Message(body=message_body.encode())

        await self.exchange.publish(message, routing_key=self.queue_name)

